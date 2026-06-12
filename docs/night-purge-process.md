# Shop Night Purge Process

## Purpose

This document describes the current field-cycle process for the high-ceiling shop purge automation. The active Home Assistant implementation is the ground truth. The repository mirrors the active `Shop Night Purge` automation and does not treat older disabled local automations as current behavior.

The goal is to remove useful evening and overnight ceiling heat only when the shop has been manually prepared for purge and appears unoccupied. The process is intentionally conservative: if AC/heat turns on, the bay door opens, the standard side door changes state, either rear window closes, the useful thermal advantage disappears, or cold-safety limits are reached, the automation shuts the purge devices off.

This is not a comfort thermostat. It is an observational thermal purge process for a shop with stratified heat, slab heat storage, passive high-window bleed, humidity-sensitive occupied comfort, and daylight solar gain that dominates daytime behavior.

## Current field-cycle posture

The previous multi-state warm-weather purge model has been retired for this test cycle. The current automation is a bounded evening/night purge:

- No blower-only mode.
- No floor-pass mode.
- No damper-only operation.
- No run based solely on indoor comfort.
- No occupied meeting-mode comfort control.
- No sunrise trigger; the 06:30 cutoff is the hard morning boundary.
- Evening start is allowed at 18:00, but only with stronger thermal and humidity guardrails.

The intent is to observe field behavior before adding stale-sensor checks, restart recovery, manual switch-on correction, notifications, or more state-machine complexity.

## Hardware and entity posture

The control logic is Home Assistant entity based and relay agnostic. It does not assume Shelly hardware or any other specific switch vendor.

The bay door sensor is treated as a strong occupancy/manual-use boundary. The AC/heat switch is treated as a strong occupied-comfort signal. The standard side door is treated as recent occupancy when it has changed state within the last hour.

Rear windows are not treated as proof of occupancy. In the current operating model, open rear windows are interpreted as manual preparation for passive or mechanical purge, provided the stronger occupied/recently occupied signals are absent.

## Entity list

Inputs:

- `switch.ac_heat_switch_switch`
- `binary_sensor.back_left_window_opening`
- `binary_sensor.back_right_window_opening`
- `binary_sensor.bay_door_opening`
- `binary_sensor.door_opening`
- `sensor.outdoor_thermometer_temperature`
- `sensor.outdoor_thermometer_humidity`
- `sensor.indoor_thermometer_temperature`
- `sensor.indoor_thermometer_humidity`
- `sensor.ceiling_thermometer_temperature`
- `sensor.ceiling_thermometer_humidity`
- `sensor.floor_thermometer_temperature`
- `sensor.floor_thermometer_humidity`

Outputs:

- `switch.damper_switch`
- `switch.blower_switch`

## Operating window

Purge is allowed only between:

```text
18:00 to 06:30
```

The automation may still evaluate outside that window when an input changes, but it will not start a purge outside the allowed window. At 06:30 it forces both purge devices off.

## Start requirements

A purge cycle may start only when all of the following are true:

- Time is within the allowed purge window.
- AC/heat switch is off.
- Bay door is closed.
- Standard side door has not changed state within the last hour.
- Left rear window is open.
- Right rear window is open.
- Outdoor, indoor, ceiling, and floor temperature and humidity sensors are valid.
- Outdoor temperature is above 50°F.
- Indoor temperature is above 50°F.
- Floor temperature is above 50°F.
- Outdoor temperature is not more than 1°F warmer than the indoor occupied-zone thermometer.

Normal purge case:

- Ceiling temperature is at least 10°F warmer than floor temperature.
- Outdoor temperature is at least 10°F cooler than ceiling temperature.
- Outdoor dew point is no more than 2°F above the indoor/floor reference dew point.

Extreme heat-purge case:

- Ceiling temperature is at least 15°F warmer than floor temperature.
- Outdoor temperature is at least 15°F cooler than ceiling temperature.
- Outdoor dew point is no more than 6°F above the indoor/floor reference dew point.

The automation uses a simple approximate dew point calculation from temperature and relative humidity. It is intended as a practical purge/no-purge guardrail, not a laboratory psychrometric calculation.

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

`mode: single` is intentional for this field cycle. During the 60-minute rest, repeated sensor updates are ignored so the cooldown is preserved. The purge devices are already off during the cooldown.

## Immediate stop conditions

An active purge stops immediately when any of the following occur:

- 06:30 arrives.
- AC/heat switch turns on.
- Bay door opens.
- Standard side door changes state.
- Either rear window closes.
- Any required temperature or humidity sensor becomes invalid.
- Outdoor temperature is at or below 50°F.
- Indoor temperature is at or below 50°F.
- Floor temperature is at or below 50°F.
- Ceiling temperature is within 3°F of floor temperature.
- Ceiling temperature is within 3°F of indoor temperature.
- Outdoor temperature is no longer at least 3°F cooler than ceiling temperature.
- Outdoor temperature rises more than 1°F above the indoor occupied-zone thermometer.
- Outdoor dew point is more than 6°F above the indoor/floor reference dew point and the ceiling/floor delta is no longer extreme.
- The 10-minute run timeout expires.

## Occupancy and manual-use boundary

For this cycle:

```text
bay door open = occupied or manual-use mode
AC/heat on = occupied comfort mode
side door changed within 1 hour = occupied or recently occupied
both rear windows open = purge permission, not proof of unoccupancy
occupied/manual-use mode = purge off
```

The side-door interpretation is intentionally conservative. A standard side-door change usually means entry, exit, dog movement, loading, shutdown, or near-term human activity. That suppresses mechanical purge until the one-hour recent-occupancy window expires.

## Field-observation model

Observed shop behavior from the current warm/humid test day:

- Closed shop plus AC can cool and dry the occupied work area even while the ceiling layer remains hot.
- Turning AC off for video-call noise allows the occupied-zone dry/cool bubble to collapse quickly under hot-soaked conditions.
- Blower operation during occupied humid conditions can raise work-area humidity without meaningfully stopping upper-zone temperature rise.
- Rear-window opening can reduce upper-zone temperature but may degrade work-area comfort if outdoor dew point is high.
- A standard side-door opening is a small operational disturbance, not equivalent to a bay-door ventilation event.
- When unoccupied, open rear windows and bounded fan/damper purge may be useful to dump stored upper heat, but only until the upper layer is mostly destratified.

The practical rule is:

```text
Occupied mode: protect the dry work-area bubble.
Unoccupied evening/night mode: remove stored upper heat, then stop.
```

## Humidity and dew point role

Relative humidity alone is not used as the decision metric because cooler outdoor air can show high RH while still carrying a different moisture load than warmer indoor air. The current automation estimates dew point from temperature and RH, then compares outdoor dew point against the indoor/floor reference.

The humidity guardrail is deliberately asymmetric:

- Normal thermal opportunity requires outdoor dew point to be no more than 2°F above the indoor/floor reference.
- Extreme ceiling heat allows a larger humidity penalty, up to 6°F above the reference.
- Once the heat delta is mostly consumed, the automation stops instead of continuing to import wet air.

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

The floor sensor is used for three checks:

- Start only if the ceiling is substantially warmer than the floor.
- Stop when the ceiling is mostly destratified relative to the floor.
- Block or stop purge if the floor is at or below 50°F.

The floor sensor is not currently used for a separate slab-purge stage.

## Accepted edge cases for this cycle

- Manual switch-on correction is not yet included beyond the automation's normal default turn-off path.
- Home Assistant restart recovery is not yet included.
- Stale sensor detection is not yet included.
- Notifications for open windows in cold conditions are not yet included.
- Cooldown triggers are ignored while `mode: single` is delaying, which is acceptable because the devices are already off during cooldown.

These are intentionally held until after field observation of the current humidity-aware cycle.

## YAML usage

The YAML file is written as a Home Assistant automation definition. If used inside a package file, wrap it under `automation:`.

## Sensor placement

Sensor placement matters. The outdoor reference should be shaded and not heat-soaked by the rear wall or upper window area. The ceiling sensor should measure upper-air temperature, not roof or wall surface temperature. The floor/slab sensor is slow-moving and should not be treated like an occupied-zone comfort sensor.

## Safety boundary

This repository documents architecture, control logic, sensor placement, and Home Assistant implementation. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.
