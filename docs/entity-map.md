# Entity Map

This document records the current Home Assistant entity IDs used by the shop night-purge automation and the historical prefixes used before the current naming pass.

## Current entities

| Role | Entity ID |
| --- | --- |
| AC/heat occupied-comfort switch | `switch.ac_heat_switch_switch` |
| Rear left window open sensor | `binary_sensor.back_left_window_opening` |
| Rear right window open sensor | `binary_sensor.back_right_window_opening` |
| Bay door open sensor | `binary_sensor.bay_door_opening` |
| Standard side-door open sensor | `binary_sensor.door_opening` |
| Outdoor temperature | `sensor.outdoor_thermometer_temperature` |
| Outdoor humidity | `sensor.outdoor_thermometer_humidity` |
| Indoor occupied-zone temperature | `sensor.indoor_thermometer_temperature` |
| Indoor occupied-zone humidity | `sensor.indoor_thermometer_humidity` |
| Ceiling thermometer temperature | `sensor.ceiling_thermometer_temperature` |
| Ceiling thermometer humidity | `sensor.ceiling_thermometer_humidity` |
| Floor thermometer temperature | `sensor.floor_thermometer_temperature` |
| Floor thermometer humidity | `sensor.floor_thermometer_humidity` |
| Powered damper/fan switch | `switch.damper_switch` |
| Supplemental blower switch | `switch.blower_switch` |

## Current interpretation

| Signal | Interpretation |
| --- | --- |
| `switch.ac_heat_switch_switch` on | Occupied comfort mode. Block or stop purge. |
| `binary_sensor.bay_door_opening` on | Occupied or manual-use mode. Block or stop purge. |
| `binary_sensor.door_opening` changed within last hour | Occupied or recently occupied. Block purge starts. |
| Both rear windows open | Manual purge preparation signal, not proof that the shop is unoccupied. |
| Either rear window closed | Manual-use or shutdown of purge path. Stop purge. |
| Ceiling/floor thermal delta | Primary heat-purge opportunity signal. |
| Outdoor/ceiling thermal delta | Whether outdoor air can remove upper-zone heat. |
| Outdoor vs indoor dew point | Moisture penalty guardrail. |

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
- Bay door opening, AC/heat switch-on, side-door movement, and either rear window closing are treated as manual-use or occupancy boundaries for the current purge cycle.
- Humidity sensors are used only to estimate dew point for purge/no-purge guardrails; they are not comfort targets.
