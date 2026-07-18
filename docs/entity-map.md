# Entity Map

## Status

These entities belong to the July 2026 working baseline. The corresponding Home Assistant automations are currently disabled while the system is under review.

## Baseline control entities

Inputs:

- `switch.ac_heat_switch_switch`
- `binary_sensor.bay_door_opening`
- `sensor.outdoor_thermometer_temperature`
- `sensor.outdoor_thermometer_humidity`
- `sensor.floor_thermometer_temperature`
- `sensor.indoor_thermometer_temperature`
- `sensor.ceiling_thermometer_temperature`

Outputs:

- `switch.damper_switch`
- `switch.blower_switch`

## Observed but not used for baseline control

- `binary_sensor.back_left_window_opening`
- `binary_sensor.back_right_window_opening`
- `binary_sensor.door_opening`
- `sensor.indoor_thermometer_humidity`
- `sensor.ceiling_thermometer_humidity`
- `sensor.floor_thermometer_humidity`

## Baseline thresholds

Start is allowed when outdoor temperature has useful cooling value against at least one thermal reference:

```text
outdoor <= floor - 3°F
OR outdoor <= indoor - 3°F
OR outdoor <= ceiling - 5°F
```

Stop occurs when useful cooling advantage is gone across all three references:

```text
outdoor >= floor - 1°F
AND outdoor >= indoor - 1.5°F
AND outdoor >= ceiling - 2.5°F
```

Outdoor RH below 85% allows start. Outdoor RH at or above 85% blocks or stops extraction.

Detailed behavior is documented in [`night-purge-process.md`](night-purge-process.md).
