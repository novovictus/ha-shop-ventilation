# Home Assistant Shop Ventilation Controller

A Home Assistant reference design for a high-ceiling shop evening/night-purge controller using rear-window intent sensors, bay-door and side-door occupancy boundaries, AC/heat state, layered temperature and humidity sensors, and fail-off control logic.

The project treats the shop as a thermal-mass problem, not a comfort thermostat. The goal is to remove useful stored upper-zone heat without fighting daylight solar gain, defeating occupied-zone comfort, or mechanically pulling in air after the useful destratification benefit has been spent.

## Project status

Current field-cycle test: bounded evening/night purge with humidity guardrail.

The active Home Assistant implementation is treated as ground truth. This repository tracks the current `Shop Night Purge` automation rather than older disabled/retained automations still present locally for posterity.

The earlier multi-mode framing has been retired for this cycle. The current automation remains intentionally bounded: short purge cycles, explicit manual preparation, conservative occupancy lockouts, and no attempt to become a full comfort thermostat.

## Active versus reference YAML

The active field-cycle implementation is:

```text
home-assistant/shop-night-purge.yaml
```

The package file below is a non-active architectural/starter reference and should not be loaded alongside the active field-cycle automation without reconciling overlapping damper/blower control, helper entities, thresholds, and sequencing assumptions:

```text
home-assistant/packages/shop_ventilation.yaml
```

During field testing, the active automation may intentionally differ from older architecture, package, or state-machine notes. When there is a conflict, treat `home-assistant/shop-night-purge.yaml` as ground truth for the current cycle.

## Current behavior

Purge may start only when all of the following are true:

- Time is between 18:00 and 06:30.
- AC/heat switch is off.
- Bay door is closed.
- Standard side door has not changed state within the last hour.
- Both rear windows are open.
- Outdoor, indoor, ceiling, and floor temperature and humidity sensors are valid.
- Outdoor, indoor, and floor temperatures are all above 50°F.
- Outdoor is not more than 1°F warmer than the indoor occupied-zone thermometer.
- Normal purge case: ceiling is at least 10°F warmer than floor, outdoor is at least 10°F cooler than ceiling, and outdoor dew point is no more than 2°F above the indoor/floor reference dew point.
- Extreme heat-purge case: ceiling is at least 15°F warmer than floor, outdoor is at least 15°F cooler than ceiling, and outdoor dew point is no more than 6°F above the indoor/floor reference dew point.

When those conditions are met:

```text
damper on
blower on
run up to 10 minutes
damper off
blower off
rest 60 minutes
```

An active purge stops immediately if 06:30 arrives, AC/heat turns on, the bay door opens, the side door changes state, either rear window closes, a required sensor becomes invalid, any 50°F cold-safety boundary is reached, the useful outdoor/ceiling delta is mostly spent, or the ceiling has mostly destratified relative to the floor/indoor sensors.

## Field observations captured in this cycle

- Closed shop plus AC protects the occupied-zone dry bubble even while the upper layer remains very hot.
- Turning AC off for meeting noise allows the occupied-zone comfort bubble to collapse quickly on hot-soaked days.
- Blower use during occupied humid conditions can raise work-area humidity without meaningfully arresting upper-zone heat gain.
- Rear-window opening can lower the upper layer, but if outdoor dew point is high it may make the working layer feel worse.
- A standard side-door opening is treated as occupancy/recent activity, not as a major ventilation path.
- After-hours window opening can be useful as passive heat purge when the space is unoccupied, but forced damper/fan purge should stop once the upper layer is mostly destratified.

## Hardware baseline

The control logic is Home Assistant entity based and relay agnostic. It does not assume Shelly hardware.

- Powered damper/fan controlled by Home Assistant as `switch.damper_switch`.
- Supplemental blower controlled by Home Assistant as `switch.blower_switch`.
- AC/heat occupancy/control switch:
  - `switch.ac_heat_switch_switch`
- Rear window opening sensors:
  - `binary_sensor.back_left_window_opening`
  - `binary_sensor.back_right_window_opening`
- Bay door opening sensor:
  - `binary_sensor.bay_door_opening`
- Standard side-door opening sensor:
  - `binary_sensor.door_opening`
- Temperature and humidity sensors:
  - `sensor.outdoor_thermometer_temperature`
  - `sensor.outdoor_thermometer_humidity`
  - `sensor.indoor_thermometer_temperature`
  - `sensor.indoor_thermometer_humidity`
  - `sensor.ceiling_thermometer_temperature`
  - `sensor.ceiling_thermometer_humidity`
  - `sensor.floor_thermometer_temperature`
  - `sensor.floor_thermometer_humidity`

## Repository layout

```text
docs/              Design notes, process documentation, entity map
home-assistant/    Home Assistant automation YAML
data/              Bench-test and power-profile data
scripts/           Small analysis helpers
site/              Website/article draft material
photos/            Placeholders for bench-test and installation photos
```

## Current implementation

- `home-assistant/shop-night-purge.yaml` contains the active field-cycle automation mirrored from Home Assistant.
- `docs/night-purge-process.md` documents the current operating model, boundaries, and accepted edge cases.
- `docs/entity-map.md` records the Home Assistant entity IDs used by the automation.
- `home-assistant/packages/shop_ventilation.yaml` is a non-active starter/reference package and is not current field-cycle ground truth.

The YAML file is written as a Home Assistant automation definition. If used inside a package file, wrap it under `automation:`.

## Current non-goals

- Do not run as an occupied comfort thermostat.
- Do not use blower-only or damper-only modes.
- Do not perform a separate floor/slab purge stage.
- Do not use the indoor thermometer as the main trigger.
- Do not automatically decide that the shop needs AC.
- Do not chase ceiling temperature after the useful destratification opportunity is mostly consumed.
- Do not add more recovery/notification logic until the current cycle has been observed.
- Do not assume a specific relay/switch vendor.
- Do not document disabled legacy local automations as current behavior.

## Safety boundary

This repository documents architecture, control logic, sensor placement, and Home Assistant implementation. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.

## License

MIT. See [LICENSE](LICENSE).
