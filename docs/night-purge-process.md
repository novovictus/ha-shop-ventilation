# Shop Night Heat Extraction Process

## Purpose

This document describes the current v1 field-cycle process for the shop heat-extraction automation.

The goal is to reduce hot mornings after high heat-load days. The automation uses a paired damper and blower only when outdoor air is meaningfully cooler than the shop and outdoor humidity is within the v1 guardrail.

This is not a comfort thermostat. It is a nighttime thermal-state safeguard for a shop with slab heat storage, stratified ceiling heat, passive equalization behavior, manual window operation, and daytime AC use.

## Current posture

The previous rear-window, supplemental-blower, dew-point, and multi-stage purge model remains retired for this test cycle.

The July 2026 occupied/manual-cycle pull changed the active v1 model from floor-only damper control to paired active extraction:

- The damper and blower are now treated as one active extraction pair.
- The floor sensor remains a conservative thermal-mass reference.
- Indoor temperature is active because it better reflects occupied-zone recovery.
- Ceiling temperature is active because it exposes stored upper-layer heat.
- Rear window sensors remain observational only.
- Dew-point calculation remains deferred.
- Outdoor RH remains the crude humidity guardrail.
- There is still no maximum runtime.
- There is still no AC automation.

## Active entities

Inputs used by v1:

- `switch.ac_heat_switch_switch`
- `binary_sensor.bay_door_opening`
- `sensor.outdoor_thermometer_temperature`
- `sensor.outdoor_thermometer_humidity`
- `sensor.floor_thermometer_temperature`
- `sensor.indoor_thermometer_temperature`
- `sensor.ceiling_thermometer_temperature`

Outputs used by v1:

- `switch.damper_switch`
- `switch.blower_switch`

Observed but not active in v1:

- `binary_sensor.back_left_window_opening`
- `binary_sensor.back_right_window_opening`
- `binary_sensor.door_opening`
- `sensor.indoor_thermometer_humidity`
- `sensor.ceiling_thermometer_humidity`
- `sensor.floor_thermometer_humidity`

## Operating window

Heat extraction is allowed only between:

```text
sunset + 20 minutes to sunrise
```

The automation evaluates at sunset plus 20 minutes and every 20 minutes overnight. It also re-evaluates if either controlled output is turned off while active-extraction conditions still apply.

## Start requirements

A heat-extraction run may start only when all of the following are true:

- Time is after sunset plus 20 minutes and before sunrise.
- Damper or blower is off.
- AC/heat switch is off.
- Bay door is closed.
- Outdoor RH is below 85%.
- Outdoor air is usefully cooler than at least one active shop thermal reference.

Temperature start rule:

```text
outdoor <= floor - 3°F
OR outdoor <= indoor - 3°F
OR outdoor <= ceiling - 5°F
```

This replaces the older floor-only start rule.

## Run behavior

When start requirements are met:

```text
damper on
blower on
```

The active extraction state is now paired. A damper-on / blower-off state is treated as a repairable mismatch, not as a valid active state.

There is no maximum runtime in v1. If favorable conditions persist all night, the system may continue running. This is intentional for the heatwave data-collection cycle.

## Stop conditions

An active extraction run stops when any of the following are true:

- Sunrise occurs.
- AC/heat switch turns on.
- Bay door opens.
- Outdoor RH reaches the 85% cutoff.
- Outdoor air no longer has useful cooling advantage across the shop.

Temperature stop rule:

```text
outdoor >= floor - 1°F
AND outdoor >= indoor - 1.5°F
AND outdoor >= ceiling - 2.5°F
```

This intentionally does not stop merely because the floor has converged. The July 2026 pull showed the floor can be stable while indoor and ceiling air still hold removable heat.

Humidity stop rule:

```text
outdoor RH >= 85%
```

When stop requirements are met:

```text
damper off
blower off
```

The stop automation also cleans up mismatched active states by turning both outputs off if either output is on.

## Visual flow map

Start flow:

```text
                         ┌──────────────────────────────┐
                         │  Every 20 min OR sunset+20   │
                         │  OR damper/blower turned off │
                         └───────────────┬──────────────┘
                                         │
                                         v
                              ┌─────────────────────┐
                              │ Is either device off?│
                              │ damper OR blower     │
                              └──────────┬──────────┘
                                         │ no
                                         v
                                      Do nothing

                                         │ yes
                                         v
                              ┌─────────────────────┐
                              │ Is it night?         │
                              │ sunset+20 to sunrise │
                              └──────────┬──────────┘
                                         │ no
                                         v
                                      Do nothing

                                         │ yes
                                         v
                              ┌─────────────────────┐
                              │ Bay door closed?     │
                              └──────────┬──────────┘
                                         │ no
                                         v
                                      Do nothing

                                         │ yes
                                         v
                              ┌─────────────────────┐
                              │ AC / heat off?       │
                              └──────────┬──────────┘
                                         │ no
                                         v
                                      Do nothing

                                         │ yes
                                         v
                              ┌─────────────────────┐
                              │ Outdoor RH < 85%?    │
                              └──────────┬──────────┘
                                         │ no
                                         v
                                      Do nothing

                                         │ yes
                                         v
                    ┌────────────────────────────────────────┐
                    │ Is outdoor air usefully cooler?         │
                    │                                        │
                    │ outdoor <= floor - 3°F                 │
                    │ OR outdoor <= indoor - 3°F              │
                    │ OR outdoor <= ceiling - 5°F             │
                    └───────────────────┬────────────────────┘
                                        │ no
                                        v
                                     Do nothing

                                        │ yes
                                        v
                    ┌────────────────────────────────────────┐
                    │ TURN ON:                               │
                    │ - damper                               │
                    │ - blower                               │
                    └────────────────────────────────────────┘
```

Stop flow:

```text
                         ┌──────────────────────────────┐
                         │  Bay opens                   │
                         │  OR AC/heat turns on          │
                         │  OR sunrise                   │
                         │  OR every 20 min              │
                         │  OR temp/RH changes           │
                         └───────────────┬──────────────┘
                                         │
                                         v
                              ┌─────────────────────┐
                              │ Is either device on? │
                              │ damper OR blower     │
                              └──────────┬──────────┘
                                         │ no
                                         v
                                      Do nothing

                                         │ yes
                                         v
                    ┌────────────────────────────────────────┐
                    │ Stop if ANY are true:                  │
                    │                                        │
                    │ bay door open                          │
                    │ OR AC/heat on                          │
                    │ OR daytime                             │
                    │ OR outdoor RH >= 85%                   │
                    │ OR cooling advantage is gone           │
                    └───────────────────┬────────────────────┘
                                        │ no
                                        v
                              Keep damper + blower on

                                        │ yes
                                        v
                    ┌────────────────────────────────────────┐
                    │ TURN OFF:                              │
                    │ - damper                               │
                    │ - blower                               │
                    └────────────────────────────────────────┘
```

## Accepted non-start condition

Non-operation is a valid result.

If the shop passively equalizes, the outdoor/shop delta may never justify running the blower. That is not a failure. It means the building handled the heat dump without additional electricity.

## Field model

Practical rule:

```text
Daytime: protect the work-area AC condition.
Night: extract stored heat only when outdoor conditions are favorable.
Passive success: if the shop equalizes on its own, do nothing.
Active extraction: when the delta is real, run damper and blower together.
```

## Humidity role

V1 uses relative humidity as a crude guardrail because dew point is not implemented in the deployed UI automations.

```text
outdoor RH < 85% = allow start
outdoor RH >= 85% = stop or block
```

Dew point logic remains deferred until after more paired-extraction observation.

## Floor, indoor, and ceiling sensor roles

The v1 thermal model now uses three active temperature references:

- Floor: conservative thermal-mass/slab reference.
- Indoor: occupied-zone and general shop-air reference.
- Ceiling: stored upper-layer heat reference.

Start can be triggered by any one of these references showing useful outdoor advantage. Stop requires convergence across all three references so the automation does not quit while removable heat remains above the occupied layer.

## Window role

Rear windows are still manual/passive ventilation. They are not an automation gate in v1.

Window-open operation is allowed if all active extraction conditions are otherwise true. Open windows are not interpreted as a reason to block the blower; they are simply an existing passive air path.

## Accepted edge cases

- Home Assistant restart recovery is not yet explicitly handled beyond normal time-pattern rechecks.
- Stale sensor detection is not yet included.
- Dew point calculation is not yet included.
- Occupancy or motion detection is not yet included.
- AC automation is not yet included.
- The time-pattern check may start or stop on a single sample rather than a continuous verified condition.
- Manual off during valid extraction conditions may be repaired by the start automation.
- Manual on during stop conditions may be corrected by the stop automation.

## YAML usage

The YAML file is written as two Home Assistant automation definitions stored together for repository tracking. If importing through the Home Assistant Automation UI, paste the start and stop automations separately.

## Sensor placement

The outdoor thermometer is mounted high under an eave. Its reading may lag or differ from public weather forecasts, especially around sunset and after solar loading. The automation uses the observed local sensor rather than forecast values.
