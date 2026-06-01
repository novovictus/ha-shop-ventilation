# Warm-Weather Shop Purge Process

## Purpose

This document describes the current warm-weather purge process for the high-ceiling shop. It is a reference design and field process, not a claim of universal correctness.

The goal is to remove useful heat from the shop when a human has intentionally opened at least one rear window. The process focuses on ceiling-zone heat first, then allows a secondary floor/slab pass when conditions remain useful.

This is not a comfort thermostat. It is an observational thermal purge process for a shop with stratified heat and slab heat storage.

## Entity list

Inputs:

- `binary_sensor.back_left_window_opening`
- `binary_sensor.back_right_window_opening`
- `sensor.outdoor_thermometer_temperature`
- `sensor.indoor_thermometer_temperature`
- `sensor.ceiling_thermometer_temperature`
- `sensor.floor_thermometer_temperature`

Outputs:

- `switch.damper_switch`
- `switch.blower_switch`

## Derived values

- `any_rear_window_open`: true when either rear window sensor is open.
- `ceiling_delta`: `ceiling_temp - indoor_temp`.
- `floor_delta`: `floor_temp - outside_temp`.
- `sensors_valid`: true only when required temperature sensors and derived deltas are available.
- `outside_useful_on`: true when outdoor temperature is less than or equal to indoor temperature plus 2 degrees.
- `outside_useful_off`: true when outdoor temperature is greater than or equal to indoor temperature plus 3 degrees.
- `outside_floor_useful`: true when outdoor temperature is less than or equal to indoor temperature minus 2 degrees.

## Thresholds

| Name | Value | Meaning |
| --- | ---: | --- |
| `ceiling_hot_start` | 6 | Start ceiling purge or blower-only mix when ceiling is this much hotter than the indoor thermometer. |
| `ceiling_hot_stop` | 3 | Treat the ceiling zone as equalized when the ceiling delta falls to this value or lower. |
| `floor_purge_start` | 3 | Start floor/slab pass when the floor remains this much warmer than outside. |
| `floor_purge_stop` | 1 | Treat the floor/slab pass as no longer useful when floor delta falls to this value or lower. |
| `outside_useful_on` | `outside_temp <= indoor_temp + 2` | Outdoor air is useful enough to run the damper/fan during ceiling purge. |
| `outside_useful_off` | `outside_temp >= indoor_temp + 3` | Outdoor air is no longer useful enough to keep purging. |
| `outside_floor_useful` | `outside_temp <= indoor_temp - 2` | Outdoor air is useful enough for the secondary floor/slab pass. |

## Operating states

### Disarmed

Condition:

- No rear window is open, or required sensors are invalid.

Action:

- Turn off `switch.damper_switch`.
- Turn off `switch.blower_switch`.

The rear window state is the human intent signal. If no rear window is open, the automation should not run ventilation hardware.

### Ceiling purge

Condition:

- A rear window is open.
- The ceiling delta is at or above `ceiling_hot_start`.
- Outdoor air is useful for ceiling purge.

Action:

- Turn on `switch.damper_switch`.
- Turn on `switch.blower_switch`.

This is the main purge mode. The damper is treated as a combined powered damper/fan, and the blower supplements mixing of trapped ceiling heat.

### Blower-only mix

Condition:

- A rear window is open.
- The ceiling delta is at or above `ceiling_hot_start`.
- Outdoor air is not useful for ceiling purge.

Action:

- Turn off `switch.damper_switch`.
- Turn on `switch.blower_switch`.

This mode mixes trapped ceiling heat without pulling in outdoor air that is not useful.

### Floor pass

Condition:

- A rear window is open.
- The ceiling has equalized.
- The floor/slab is still warm relative to outside.
- Outdoor air is useful for floor purge.

Action:

- Turn on `switch.damper_switch`.
- Turn off `switch.blower_switch`.

This is a secondary stage after ceiling equalization. It lets the system continue moving useful outdoor air across the lower/slab zone without running the ceiling blower.

### Done

Condition:

- A rear window is open.
- The ceiling has equalized.
- The floor pass is no longer useful because the floor has equalized, outside air is no longer useful for the floor pass, or outside air has reached the purge-off threshold.

Action:

- Turn off `switch.damper_switch`.
- Turn off `switch.blower_switch`.

## Known future lockouts

These are known additions, but they are not active requirements in the current automation:

- Bay door sensor.
- Rain lockout.
- AC active lockout.

## Notes

- This is not a comfort thermostat.
- Window open is the human intent signal.
- Either rear window can arm the process.
- If no rear window is open, both controlled switches must be off.
- The indoor thermometer remains named `indoor_thermometer` in YAML and documentation.
- The current YAML is intentionally simple so real field usage can expose bugs and tuning needs.
- Thresholds are expected to be tuned after more field observations.
