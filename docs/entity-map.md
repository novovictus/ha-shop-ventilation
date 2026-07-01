# Entity Map

Current v1 active entities:

- `switch.ac_heat_switch_switch`
- `binary_sensor.bay_door_opening`
- `sensor.outdoor_thermometer_temperature`
- `sensor.outdoor_thermometer_humidity`
- `sensor.floor_thermometer_temperature`
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

Current v1 thresholds:

- Start opportunity: outdoor temperature is at least 3°F below floor temperature.
- Stop opportunity: outdoor temperature is within 1°F below floor temperature.
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

- The active v1 output is `switch.damper_switch` only.
- `switch.blower_switch` is retained for future experiments but is not active in v1.
- Window, indoor, ceiling, and floor-humidity sensors remain useful for observation and later tuning.
- Dew point logic is deferred until after the heatwave test.
