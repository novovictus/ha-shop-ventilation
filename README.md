# Home Assistant Shop Ventilation Controller

A Home Assistant reference design for a high-ceiling shop night-purge controller using rear-window intent sensors, a bay-door occupancy boundary, layered temperature sensors, and fail-off control logic.

The project treats the shop as a thermal-mass problem, not a comfort thermostat. The goal is to remove useful overnight ceiling heat without fighting daylight solar gain or mechanically pulling in air that makes the occupied zone worse.

## Project status

Current field-cycle test: bounded night purge.

The active Home Assistant implementation is treated as ground truth. This repository now tracks the current `Shop Night Purge` automation rather than the older disabled/retained automations still present locally for posterity.

The earlier multi-mode framing has been retired for this cycle. The current automation is intentionally smaller so one full run can expose real behavior before adding stale-sensor checks, notifications, restart recovery, or more state-machine complexity.

## Current behavior

Purge may start only when all of the following are true:

- Time is between 20:30 and 06:30.
- Bay door is closed.
- Both rear windows are open.
- Outdoor, indoor, ceiling, and floor sensors are valid.
- Outdoor, indoor, and floor temperatures are all above 50°F.
- Ceiling is at least 5°F warmer than floor.
- Outdoor is at least 5°F cooler than ceiling.
- Outdoor is not more than 1°F warmer than the indoor occupied-zone thermometer.

When those conditions are met:

```text
damper on
blower on
run up to 10 minutes
damper off
blower off
rest 60 minutes
```

An active purge stops immediately if 06:30 arrives, the bay door opens, either rear window closes, a required sensor becomes invalid, any 50°F cold-safety boundary is reached, or the useful thermal advantage disappears.

## Hardware baseline

The control logic is Home Assistant entity based and relay agnostic. It does not assume Shelly hardware.

- Powered damper/fan controlled by Home Assistant as `switch.damper_switch`.
- Supplemental blower controlled by Home Assistant as `switch.blower_switch`.
- Rear window opening sensors:
  - `binary_sensor.back_left_window_opening`
  - `binary_sensor.back_right_window_opening`
- Bay door opening sensor:
  - `binary_sensor.bay_door_opening`
- Temperature sensors:
  - `sensor.outdoor_thermometer_temperature`
  - `sensor.indoor_thermometer_temperature`
  - `sensor.ceiling_thermometer_temperature`
  - `sensor.floor_thermometer_temperature`

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
- `docs/warm-weather-process.md` documents the current operating model, boundaries, and accepted edge cases.
- `docs/entity-map.md` records the Home Assistant entity IDs used by the automation.

The YAML file is written as a Home Assistant automation definition. If used inside a package file, wrap it under `automation:`.

## Current non-goals

- Do not run during daylight.
- Do not use blower-only or damper-only modes.
- Do not perform a separate floor/slab purge stage.
- Do not use the indoor thermometer as the main trigger.
- Do not automatically decide that the shop needs AC.
- Do not add more recovery/notification logic until the current cycle has been observed.
- Do not assume a specific relay/switch vendor.
- Do not document disabled legacy local automations as current behavior.

## Safety boundary

This repository documents architecture, control logic, sensor placement, and Home Assistant implementation. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.

## License

MIT. See [LICENSE](LICENSE).
