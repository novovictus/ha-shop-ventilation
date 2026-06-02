# Entity Map

This document records the current Home Assistant entity IDs used by the shop night-purge automation and the historical prefixes used before the current naming pass.

## Current entities

| Role | Entity ID |
| --- | --- |
| Rear left window open sensor | `binary_sensor.back_left_window_opening` |
| Rear right window open sensor | `binary_sensor.back_right_window_opening` |
| Bay door open sensor | `binary_sensor.bay_door_opening` |
| Outdoor temperature | `sensor.outdoor_thermometer_temperature` |
| Indoor occupied-zone temperature | `sensor.indoor_thermometer_temperature` |
| Ceiling thermometer temperature | `sensor.ceiling_thermometer_temperature` |
| Floor thermometer temperature | `sensor.floor_thermometer_temperature` |
| Powered damper/fan switch | `switch.damper_switch` |
| Supplemental blower switch | `switch.blower_switch` |

## Historical and renamed prefixes

| Historical prefix | Current prefix |
| --- | --- |
| `computers` | `bench` |
| `fridge_wall` | `blower` |
| `back_wall` | `damper` |
| `outdoor_temperature` | `outdoor_thermometer` |
| `shop_ceiling_thermometer` | `ceiling_thermometer` |
| `shop_floor` | `floor_thermometer` |
| `shop_door_window` | `back_right_window` |
| `shop_far_window` | `back_left_window` |

## Notes

- The current automation uses the installed Home Assistant entity IDs directly.
- The indoor thermometer remains `indoor_thermometer` in YAML, but its current role is a guardrail for the occupied zone, not the primary purge trigger.
- The damper is treated as a combined powered damper/fan in the current control model.
- Bay door opening and either rear window closing are treated as manual-use or occupancy signals for the current purge cycle.
