# Shop Night Heat Extraction Process

## Purpose

This document describes the current v1 field-cycle process for the shop heat-extraction automation.

The goal is to reduce hot mornings after high heat-load days. The automation uses the damper/fan only when outdoor air is meaningfully cooler than the shop floor and outdoor humidity is within the v1 guardrail.

This is not a comfort thermostat. It is a nighttime thermal-state safeguard for a shop with slab heat storage, stratified ceiling heat, passive equalization behavior, manual window operation, and daytime AC use.

## Current posture

The previous rear-window, supplemental-blower, ceiling-delta, and dew-point purge model has been retired for this test cycle.

Current v1 characteristics:

- Damper/fan only.
- No supplemental blower.
- No window automation.
- No side-door logic.
- No ceiling-triggered purge stage.
- No dew-point calculation.
- No maximum runtime.
- No AC automation.

## Active entities

Inputs used by v1:

- `switch.ac_heat_switch_switch`
- `binary_sensor.bay_door_opening`
- `sensor.outdoor_thermometer_temperature`
- `sensor.outdoor_thermometer_humidity`
- `sensor.floor_thermometer_temperature`

Output used by v1:

- `switch.damper_switch`

Observed but not active in v1:

- `binary_sensor.back_left_window_opening`
- `binary_sensor.back_right_window_opening`
- `binary_sensor.door_opening`
- `sensor.indoor_thermometer_temperature`
- `sensor.indoor_thermometer_humidity`
- `sensor.ceiling_thermometer_temperature`
- `sensor.ceiling_thermometer_humidity`
- `sensor.floor_thermometer_humidity`
- `switch.blower_switch`

## Operating window

Heat extraction is allowed only between:

```text
sunset + 20 minutes to sunrise
```

The automation evaluates at sunset plus 20 minutes and every 20 minutes overnight.

## Start requirements

A heat-extraction run may start only when all of the following are true:

- Time is after sunset plus 20 minutes and before sunrise.
- Damper/fan switch is off.
- AC/heat switch is off.
- Bay door is closed.
- Outdoor temperature is at least 3°F below the floor temperature.
- Outdoor RH is below 85%.

Temperature rule:

```text
outdoor <= floor - 3°F
```

## Run behavior

When start requirements are met:

```text
damper/fan on
```

There is no maximum runtime in v1. If favorable conditions persist all night, the system may continue running. This is intentional for the heatwave data-collection cycle.

## Stop conditions

An active extraction run stops when any of the following are true:

- Sunrise occurs.
- AC/heat switch turns on.
- Bay door opens.
- Outdoor temperature is no longer usefully cooler than the floor.
- Outdoor RH reaches the 85% cutoff.

Temperature stop rule:

```text
outdoor >= floor - 1°F
```

Humidity stop rule:

```text
outdoor RH >= 85%
```

## Accepted non-start condition

Non-operation is a valid result.

If the shop passively equalizes, the outdoor/floor delta may never justify running the fan. That is not a failure. It means the building handled the heat dump without additional electricity.

## Field model

Practical rule:

```text
Daytime: protect the work-area AC condition.
Night: extract stored floor/slab heat only when outdoor conditions are favorable.
Passive success: if the shop equalizes on its own, do nothing.
```

## Humidity role

V1 uses relative humidity as a crude guardrail because dew point is not implemented in the deployed UI automations.

```text
outdoor RH < 85% = allow start
outdoor RH >= 85% = stop or block
```

Dew point logic is deferred until after the heatwave test.

## Floor sensor role

The floor sensor is the main thermal reference for v1.

- Start only if outdoor air is at least 3°F cooler than the floor.
- Stop once outdoor air is within 1°F below the floor.
- Do not chase ceiling temperature in v1.

## Accepted edge cases

- Manual switch-on correction is limited to normal stop automation behavior.
- Home Assistant restart recovery is not yet included.
- Stale sensor detection is not yet included.
- Dew point calculation is not yet included.
- Occupancy or motion detection is not yet included.
- AC automation is not yet included.
- The time-pattern check may start or stop on a single 20-minute sample rather than a continuous 20-minute verified condition.

## YAML usage

The YAML file is written as two Home Assistant automation definitions stored together for repository tracking. If importing through the Home Assistant Automation UI, paste the start and stop automations separately.

## Sensor placement

The outdoor thermometer is mounted high under an eave. Its reading may lag or differ from public weather forecasts, especially around sunset and after solar loading. The automation uses the observed local sensor rather than forecast values.
