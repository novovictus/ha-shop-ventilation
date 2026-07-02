# Home Assistant Shop Ventilation Controller

A Home Assistant reference design for a high-ceiling shop nighttime heat-extraction controller using bay-door state, AC/heat state, floor temperature, outdoor temperature, outdoor humidity, and fail-off control logic.

The project treats the shop as a thermal-mass problem, not a comfort thermostat. The goal is to remove useful stored heat from the building mass when outside air has a clear advantage, while avoiding daylight solar gain, occupied AC operation, and unnecessary fan runtime when the shop passively equalizes on its own.

## Project status

Current field-cycle test: v1 heatwave nighttime floor/slab heat extraction with a simple RH guardrail.

The active Home Assistant implementation is treated as ground truth. This repository tracks the currently deployed `Shop Night Heat Extraction` start/stop automations rather than older disabled/retained automations still present locally for posterity.

The earlier rear-window, blower, ceiling-delta, and dew-point cycle has been retired for this test. The current automation remains intentionally simple: damper/fan only, nighttime only, bay closed, AC/heat off, outdoor air at least 3°F cooler than the floor, and outdoor RH below 85%.

## Active versus reference YAML

The active field-cycle implementation is:

```text
home-assistant/shop-night-purge.yaml
```

Despite the retained filename, this file now contains the v1 `Shop Night Heat Extraction` start and stop automations. It is the current field-cycle ground truth.

The package file below is a non-active architectural/starter reference and should not be loaded alongside the active field-cycle automation without reconciling overlapping damper/blower control, helper entities, thresholds, and sequencing assumptions:

```text
home-assistant/packages/shop_ventilation.yaml
```

During field testing, the active automation may intentionally differ from older architecture, package, or state-machine notes. When there is a conflict, treat `home-assistant/shop-night-purge.yaml` as ground truth for the current cycle.

## Current behavior

The damper/fan may start only when all of the following are true:

- Time is after sunset plus 20 minutes and before sunrise.
- AC/heat switch is off.
- Bay door is closed.
- Damper/fan switch is off.
- Outdoor temperature is at least 3°F cooler than the floor temperature.
- Outdoor relative humidity is below 85%.

When those conditions are met:

```text
damper/fan on
```

The automation evaluates the start case at sunset plus 20 minutes and every 20 minutes overnight.

An active extraction run stops if any of the following are true:

- Sunrise occurs.
- AC/heat switch turns on.
- Bay door opens.
- Outdoor temperature rises to within 1°F below floor temperature.
- Outdoor relative humidity reaches the 85% cutoff.

There is no maximum runtime in this cycle. If conditions remain favorable all night, the system may run all night. If the shop equalizes passively and conditions never justify the fan, non-operation is a valid successful outcome.

## Field observations captured in this cycle

- Closed shop plus AC protects the occupied-zone dry bubble even while the upper layer remains very hot.
- Turning AC off for meeting noise allows the occupied-zone comfort bubble to collapse quickly on hot-soaked days.
- Blower use during occupied humid conditions can raise work-area humidity without meaningfully arresting upper-zone heat gain.
- Rear-window opening can lower the upper layer, but if outdoor dew point is high it may make the working layer feel worse.
- Door-open plus blower/damper can provide useful purge when there is a real air path, but daytime openings fight AC and solar gain.
- Closed-shop passive equalization can collapse ceiling stratification after the shop is shut down.
- The current v1 automation exists to catch nights when the shop would otherwise wake up hot despite cool outside air.

## Hardware baseline

The control logic is Home Assistant entity based and relay agnostic. It does not assume Shelly hardware.

Active v1 output:

- Powered damper/fan controlled by Home Assistant as `switch.damper_switch`.
- Physical damper/fan build details are documented in `docs/damper-install.md`.

Available but not used in v1:

- Supplemental blower controlled by Home Assistant as `switch.blower_switch`.

Input entities used by v1:

- AC/heat occupancy/control switch:
  - `switch.ac_heat_switch_switch`
- Bay door opening sensor:
  - `binary_sensor.bay_door_opening`
- Outdoor temperature and humidity sensors:
  - `sensor.outdoor_thermometer_temperature`
  - `sensor.outdoor_thermometer_humidity`
- Floor temperature sensor:
  - `sensor.floor_thermometer_temperature`

Observed but not active v1 control inputs:

- Rear window opening sensors:
  - `binary_sensor.back_left_window_opening`
  - `binary_sensor.back_right_window_opening`
- Standard side-door opening sensor:
  - `binary_sensor.door_opening`
- Indoor and ceiling temperature/humidity sensors:
  - `sensor.indoor_thermometer_temperature`
  - `sensor.indoor_thermometer_humidity`
  - `sensor.ceiling_thermometer_temperature`
  - `sensor.ceiling_thermometer_humidity`
  - `sensor.floor_thermometer_humidity`

## Repository layout

```text
docs/              Design notes, process documentation, entity map, physical install notes
home-assistant/    Home Assistant automation YAML
data/              Bench-test and power-profile data
scripts/           Small analysis helpers
site/              Website/article draft material
photos/            Placeholders for bench-test and installation photos
```

## Current implementation

- `home-assistant/shop-night-purge.yaml` contains the active v1 field-cycle automations mirrored from Home Assistant.
- `docs/night-purge-process.md` documents the current operating model, boundaries, and accepted edge cases.
- `docs/entity-map.md` records the Home Assistant entity IDs used by the automation.
- `docs/damper-install.md` documents the physical shutter, fan, wall penetration, smart-plug control, and fail-closed behavior of the damper/fan subsystem.
- `docs/2026-06-30-heatwave-test.md` records the current heatwave test intent and deferred work.
- `home-assistant/packages/shop_ventilation.yaml` is a non-active starter/reference package and is not current field-cycle ground truth.

The YAML file is written as Home Assistant automation definitions. If importing into the Automation UI, paste the start and stop automations separately.

## Current non-goals

- Do not run as an occupied comfort thermostat.
- Do not use blower-only or separate blower modes.
- Do not automate window operation.
- Do not perform a separate ceiling-driven purge stage in v1.
- Do not use the indoor thermometer as the main trigger.
- Do not automatically decide that the shop needs AC.
- Do not add dew-point calculation until the simple RH-guarded test has been observed.
- Do not add occupancy/motion logic until sensors are integrated.
- Do not add more recovery/notification logic until the current cycle has been observed.
- Do not assume a specific relay/switch vendor.
- Do not document disabled legacy local automations as current behavior.

## Safety boundary

This repository documents architecture, control logic, sensor placement, and Home Assistant implementation. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.

## License

MIT. See [LICENSE](LICENSE).