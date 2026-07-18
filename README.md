# Home Assistant Shop Ventilation Controller

A Home Assistant reference design for a high-ceiling shop nighttime heat-extraction controller using bay-door state, AC/heat state, floor temperature, indoor temperature, ceiling temperature, outdoor temperature, outdoor humidity, and fail-off control logic.

The project treats the shop as a thermal-mass problem, not a comfort thermostat. The goal is to remove useful stored heat from the building mass when outside air has a clear advantage, while avoiding daylight solar gain, occupied AC operation, and unnecessary fan runtime when the shop passively equalizes on its own.

## Project status

Current field-cycle test: v1 nighttime heat extraction with paired damper/blower control and a simple RH guardrail.

The active Home Assistant implementation is treated as ground truth. This repository tracks the currently deployed `Shop Night Heat Extraction` start/stop automations rather than older disabled/retained automations still present locally for posterity.

The July 2026 occupied/manual-cycle data pull changed the active model from floor-only damper control to paired active extraction. The current automation remains intentionally simple: nighttime only, bay closed, AC/heat off, outdoor air meaningfully cooler than the shop, and outdoor RH below 85%.

## Active versus reference YAML

The active field-cycle implementation is:

```text
home-assistant/shop-night-purge.yaml
```

Despite the retained filename, this file now contains the v1 `Shop Night Heat Extraction` start and stop automations. It is the current field-cycle ground truth.

The package file below is a non-active starter/reference package and should not be loaded alongside the active field-cycle automation without reconciling overlapping damper/blower control, helper entities, thresholds, and sequencing assumptions:

```text
home-assistant/packages/shop_ventilation.yaml
```

When documentation conflicts with the active implementation, treat `home-assistant/shop-night-purge.yaml` as ground truth for the current cycle.

## Current behavior

The active extraction pair may start only when all of the following are true:

- Time is after sunset plus 20 minutes and before sunrise.
- AC/heat switch is off.
- Bay door is closed.
- Damper or blower is off.
- Outdoor relative humidity is below 85%.
- Outdoor air has useful cooling value against floor, indoor, or ceiling temperature.

Temperature start rule:

```text
outdoor <= floor - 3°F
OR outdoor <= indoor - 3°F
OR outdoor <= ceiling - 5°F
```

When those conditions are met:

```text
damper on
blower on
```

The automation evaluates the start case at sunset plus 20 minutes, every 20 minutes overnight, and when either controlled output is turned off. This lets it repair mismatched active states such as damper on / blower off.

An active extraction run stops if any of the following are true:

- Sunrise occurs.
- AC/heat switch turns on.
- Bay door opens.
- Outdoor relative humidity reaches the 85% cutoff.
- Outdoor air no longer has useful cooling advantage across floor, indoor, and ceiling references.

Temperature stop rule:

```text
outdoor >= floor - 1°F
AND outdoor >= indoor - 1.5°F
AND outdoor >= ceiling - 2.5°F
```

When stop conditions are met:

```text
damper off
blower off
```

There is no maximum runtime in this cycle. If conditions remain favorable all night, the system may run all night. If the shop equalizes passively and conditions never justify the blower, non-operation is a valid successful outcome.

## Field observations captured in this cycle

- Closed shop plus AC protects the occupied-zone dry bubble even while the upper layer remains very hot.
- Turning AC off for meeting noise allows the occupied-zone comfort bubble to collapse quickly on hot-soaked days.
- Blower plus damper provides useful nighttime heat extraction when there is a real outdoor temperature advantage and the shop is closed enough to create directed airflow.
- Damper-only operation is weak and should not be treated as active extraction.
- Rear-window opening can passively lower the upper layer, but it does not replace active extraction when indoor/ceiling air remains meaningfully warmer than outdoor air.
- Door-open plus blower/damper can provide useful purge when there is a real air path, but daytime openings fight AC and solar gain.
- Closed-shop passive equalization can collapse ceiling stratification after the shop is shut down.
- The current v1 automation exists to catch nights when the shop would otherwise wake up hot despite cool outside air.

## Hardware baseline

The control logic is Home Assistant entity based and relay agnostic. It does not assume Shelly hardware.

Active v1 outputs:

- Powered damper controlled by Home Assistant as `switch.damper_switch`.
- Blower controlled by Home Assistant as `switch.blower_switch`.
- Physical damper/fan build details are documented in `docs/damper-install.md`.

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
- Indoor temperature sensor:
  - `sensor.indoor_thermometer_temperature`
- Ceiling temperature sensor:
  - `sensor.ceiling_thermometer_temperature`

Observed but not active v1 control inputs:

- Rear window opening sensors:
  - `binary_sensor.back_left_window_opening`
  - `binary_sensor.back_right_window_opening`
- Standard side-door opening sensor:
  - `binary_sensor.door_opening`
- Humidity sensors not used for active control:
  - `sensor.indoor_thermometer_humidity`
  - `sensor.ceiling_thermometer_humidity`
  - `sensor.floor_thermometer_humidity`

## Repository layout

```text
docs/              Current process, entity, installation, safety, and field-test documentation
home-assistant/    Home Assistant automation YAML
data/              Bench-test, field-run, and power-profile data
scripts/           Small analysis helpers
photos/            Bench-test and installation photos or placeholders
```

## Current implementation

- `home-assistant/shop-night-purge.yaml` contains the active v1 field-cycle automations mirrored from Home Assistant.
- `docs/night-purge-process.md` documents the current operating model, boundaries, visual flow map, and accepted edge cases.
- `docs/entity-map.md` records the Home Assistant entity IDs used by the automation.
- `docs/damper-install.md` documents the physical shutter, fan, wall penetration, smart-plug control, and fail-closed behavior of the damper/fan subsystem.
- `docs/2026-06-30-heatwave-test.md` records the current heatwave test intent and deferred work.
- `home-assistant/packages/shop_ventilation.yaml` is a non-active starter/reference package and is not current field-cycle ground truth.

## Field run artifacts

- `data/field-runs/2026-07-12-night-extraction-good-run.md` records the first clean long automated paired damper/blower run: 7.35 hours, 1.63 kWh estimated energy, -6.3°F indoor, -6.5°F ceiling, -3.8°F floor, and a humidity stop at 85.3% outdoor RH.

The YAML file is written as Home Assistant automation definitions. If importing into the Automation UI, paste the start and stop automations separately.

## Current non-goals

- Do not run as an occupied comfort thermostat.
- Do not use blower-only or separate blower modes.
- Do not automate window operation.
- Do not automatically close or open windows.
- Do not automatically decide that the shop needs AC.
- Do not add dew-point calculation until the simple RH-guarded paired-extraction test has been observed.
- Do not add occupancy/motion logic until sensors are integrated.
- Do not assume a specific relay/switch vendor.
- Do not document disabled legacy local automations as current behavior.

## Safety boundary

This repository documents architecture, control logic, sensor placement, and Home Assistant implementation. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.

## License

MIT. See [LICENSE](LICENSE).
