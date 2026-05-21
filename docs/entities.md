# Home Assistant entity model

The exact entity IDs will differ by installation. This file defines the conceptual entity model.

## Inputs

```yaml
sensor.shop_outdoor_temperature
sensor.shop_occupied_zone_temperature
sensor.shop_upper_zone_temperature
sensor.shop_outdoor_dew_point
sensor.shop_indoor_dew_point
binary_sensor.shop_manual_disable
input_boolean.shop_ventilation_force_purge
```

## Outputs

```yaml
switch.shop_damper
switch.shop_blower
```

## Helpers

```yaml
input_number.shop_purge_outdoor_margin
input_number.shop_purge_stratification_margin
input_number.shop_purge_comfort_threshold
input_number.shop_purge_upper_heat_threshold
input_number.shop_damper_open_delay_seconds
input_number.shop_blower_stop_delay_seconds
input_number.shop_minimum_runtime_minutes
input_number.shop_cooldown_minutes
input_number.shop_maximum_runtime_minutes
```

## Computed state

```yaml
binary_sensor.shop_purge_available
sensor.shop_ventilation_state
sensor.shop_ventilation_runtime
```

## Fault candidates

```yaml
binary_sensor.shop_blower_unexpected_power
binary_sensor.shop_damper_unexpected_power
binary_sensor.shop_ventilation_fault
```

Fault detection is optional in the initial version. It becomes useful after the expected power profiles of the damper and blower are measured.