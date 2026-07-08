# Entity Map

Current v1 active entities:

- `switch.ac_heat_switch_switch`
- `binary_sensor.bay_door_opening`
- `sensor.outdoor_thermometer_temperature`
- `sensor.outdoor_thermometer_humidity`
- `sensor.floor_thermometer_temperature`
- `sensor.indoor_thermometer_temperature`
- `sensor.ceiling_thermometer_temperature`
- `switch.damper_switch`
- `switch.blower_switch`

Observed but not active in v1:

- `binary_sensor.back_left_window_opening`
- `binary_sensor.back_right_window_opening`
- `binary_sensor.door_opening`
- `sensor.indoor_thermometer_humidity`
- `sensor.ceiling_thermometer_humidity`
- `sensor.floor_thermometer_humidity`

Current v1 thresholds:

- Start opportunity: outdoor temperature has useful cooling value against at least one shop thermal reference:
  - `outdoor <= floor - 3°F`
  - `outdoor <= indoor - 3°F`
  - `outdoor <= ceiling - 5°F`
- Stop opportunity: useful cooling advantage is basically gone across the shop:
  - `outdoor >= floor - 1°F`
  - `outdoor >= indoor - 1.5°F`
  - `outdoor >= ceiling - 2.5°F`
- Humidity guardrail: outdoor relative humidity below 85% allows start; 85% or higher stops or blocks.

Historical prefix notes:

- `computers` -> `bench`
- `fridge_wall` -> `blower`
- `back_wall` -> `damper`
- `outdoor_temperature` -> `outdoor_thermometer`
- `shop_ceiling_thermometer` -> `ceiling_thermometer`
- `shop_floor` -> `floor_thermometer`
- `shop_door_window` -> `back_right_window`
- `shop_far_window` -> `back_left_window`

Notes:

- Active v1 output is now the paired extraction set: `switch.damper_switch` and `switch.blower_switch`.
- The start automation repairs mismatched active states such as damper on / blower off.
- The stop automation turns both outputs off and also cleans up mismatched active states.
- Rear window sensors remain observational only. Open windows are treated as a manual/passive ventilation state, not as an automation gate.
- Floor, indoor, and ceiling temperature sensors are all active thermal references after the July 2026 occupied/manual-cycle data pull.
- Dew point logic is still deferred; v1 continues using outdoor RH as a crude guardrail.
