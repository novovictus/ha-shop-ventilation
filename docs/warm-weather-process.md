# Warm-Weather Shop Purge Process

## Purpose

This document describes the current full-cycle test process for the high-ceiling shop purge automation. It is a reference design and field process, not a claim of universal correctness.

The goal is to remove useful overnight ceiling heat only when the shop has been manually prepared for purge. The current process is intentionally conservative: if the bay door opens, either rear window closes, the occupied zone is no longer protected, or cold-safety limits are reached, the automation shuts the purge devices off.

This is not a comfort thermostat. It is an observational thermal purge process for a shop with stratified heat, slab heat storage, passive high-window bleed, and solar gain that dominates daylight behavior.

## Current field-cycle posture

The previous multi-state warm-weather purge model has been retired for this test cycle. The current YAML is a simpler bounded night purge:

- No blower-only mode.
- No floor-pass mode.
- No daytime operation.
- No damper-only operation.
- No run based solely on indoor comfort.
- No sunrise trigger; the 06:30 cutoff is the hard morning boundary.

The intent is to run a complete field cycle before adding more interlocks, stale-sensor checks, switch-state triggers, notifications, or state-machine complexity.

## Entity list

Inputs:

- `binary_sensor.back_left_window_opening`
- `binary_sensor.back_right_window_opening`
- `binary_sensor.bay_door_opening`
- `sensor.outdoor_thermometer_temperature`
- `sensor.indoor_thermometer_temperature`
- `sensor.ceiling_thermometer_temperature`
- `sensor.floor_thermometer_temperature`

Outputs:

- `switch.damper_switch`
- `switch.blower_switch`

## Operating window

Purge is allowed only between:

```text
20:30 to 06:30
```

The automation may still evaluate outside that window when an input changes, but it will not start a purge outside the allowed window. At 06:30 it forces both purge devices off.

## Start requirements

A purge cycle may start only when all of the following are true:

- Time is within the allowed purge window.
- Bay door is closed.
- Left rear window is open.
- Right rear window is open.
- Outdoor, indoor, ceiling, and floor temperature sensors are valid.
- Outdoor temperature is above 50°F.
- Indoor temperature is above 50°F.
- Floor temperature is above 50°F.
- Ceiling temperature is at least 5°F warmer than floor temperature.
- Outdoor temperature is at least 5°F cooler than ceiling temperature.
- Outdoor temperature is not more than 1°F warmer than the indoor occupied-zone thermometer.

## Cycle behavior

When start requirements are met:

```text
damper on
blower on
run up to 10 minutes
damper off
blower off
rest 60 minutes
```

`mode: single` is intentional for this field cycle. During the 60-minute rest, repeated sensor updates are ignored so the cooldown is preserved.

## Immediate stop conditions

An active purge stops immediately when any of the following occur:

- 06:30 arrives.
- Bay door opens.
- Either rear window closes.
- Any required temperature sensor becomes invalid.
- Outdoor temperature is at or below 50°F.
- Indoor temperature is at or below 50°F.
- Floor temperature is at or below 50°F.
- Ceiling temperature is no longer warmer than floor temperature.
- Outdoor temperature is no longer cooler than ceiling temperature.
- Outdoor temperature rises more than 1°F above the indoor occupied-zone thermometer.

## Occupancy and manual-use boundary

For this cycle:

```text
bay door opened = occupied or manual-use mode
either rear window closed = occupied or manual-use mode
occupied/manual-use mode = purge off
```

The automation does not try to infer intent beyond those signals.

## Cold-safety boundary

50°F is the current cold-safety floor for this cycle:

```text
outdoor <= 50°F = block or stop purge
indoor <= 50°F = block or stop purge
floor <= 50°F = block or stop purge
```

This is intentionally conservative. If the shop is at or below that boundary, the automation should not mechanically accelerate cooling if windows were left open.

## Indoor sensor role

The indoor thermometer is not the primary purge trigger. It is used as a guardrail:

```text
if outdoor > indoor + 1°F, do not start or continue purge
```

This prevents the automation from chasing a hot ceiling layer while importing outdoor air that is already warmer than the occupied zone.

## Floor sensor role

The floor sensor is used for two checks:

- Start only if the ceiling is at least 5°F warmer than the floor.
- Block or stop purge if the floor is at or below 50°F.

The floor sensor is not currently used for a separate slab-purge stage.

## Known edge cases accepted for this cycle

- Manual switch-on correction is not yet included.
- Home Assistant restart recovery is not yet included.
- Stale sensor detection is not yet included.
- Notifications for open windows in cold conditions are not yet included.
- Cooldown triggers are ignored while `mode: single` is delaying, which is acceptable because the devices are already off during cooldown.

These are intentionally held for observation after one full cycle run.

## YAML usage

The YAML file is written as a Home Assistant automation definition. If used inside a package file, wrap it under `automation:`.

## Sensor placement

Sensor placement matters. The outdoor reference should be shaded and not heat-soaked by the rear wall or upper window area. The ceiling sensor should measure upper-air temperature, not roof or wall surface temperature. The floor/slab sensor is slow-moving and should not be treated like an occupied-zone comfort sensor.

## Safety boundary

This repository documents architecture, control logic, sensor placement, and Home Assistant implementation. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.
