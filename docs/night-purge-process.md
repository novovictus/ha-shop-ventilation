# Shop Night Heat Extraction Process

## Status

This document describes the July 2026 working baseline for the shop nighttime heat-extraction system.

The corresponding Home Assistant automations are currently disabled while the system is under review. The preserved baseline files are:

- [`../home-assistant/automations/shop-night-heat-extraction-start.yaml`](../home-assistant/automations/shop-night-heat-extraction-start.yaml)
- [`../home-assistant/automations/shop-night-heat-extraction-stop.yaml`](../home-assistant/automations/shop-night-heat-extraction-stop.yaml)

## Purpose

The system reduces hot mornings after high heat-load days by removing stored heat when outdoor air has a useful temperature advantage. It is not a comfort thermostat.

The baseline treats the powered intake damper and the separate extraction blower as one active extraction pair. Rear windows remain manual and observational. Dew-point calculation, occupancy logic, and AC automation are not part of this baseline.

## Baseline entities

Inputs:

- `switch.ac_heat_switch_switch`
- `binary_sensor.bay_door_opening`
- `sensor.outdoor_thermometer_temperature`
- `sensor.outdoor_thermometer_humidity`
- `sensor.floor_thermometer_temperature`
- `sensor.indoor_thermometer_temperature`
- `sensor.ceiling_thermometer_temperature`

Outputs:

- `switch.damper_switch`
- `switch.blower_switch`

## Operating window

Heat extraction is allowed only from sunset plus 20 minutes until sunrise.

The start automation evaluates at sunset plus 20 minutes, every 20 minutes overnight, and whenever either controlled output is turned off. This allows it to repair a mismatched damper/blower state while valid extraction conditions remain true.

The 20-minute cadence is intentional. The baseline uses simple gates, building thermal mass, and scheduled evaluation rather than helper state, rolling averages, or a formal debounce timer.

## Start requirements

A run may start only when all of the following are true:

- It is after sunset plus 20 minutes and before sunrise.
- Either the damper or blower is off.
- AC/heat is off.
- The bay door is closed.
- Outdoor RH is below 85%.
- Outdoor air is usefully cooler than at least one active shop thermal reference.

Temperature start rule:

```text
outdoor <= floor - 3°F
OR outdoor <= indoor - 3°F
OR outdoor <= ceiling - 5°F
```

When the requirements are met:

```text
damper on
blower on
```

A damper-on/blower-off or blower-on/damper-off state is treated as a repairable mismatch, not a valid active state.

## Stop conditions

A run stops when any of the following are true:

- Sunrise occurs.
- AC/heat turns on.
- The bay door opens.
- Outdoor RH reaches 85%.
- Outdoor air no longer has useful cooling advantage across the shop.

Temperature stop rule:

```text
outdoor >= floor - 1°F
AND outdoor >= indoor - 1.5°F
AND outdoor >= ceiling - 2.5°F
```

When a stop condition is met:

```text
damper off
blower off
```

The stop automation turns both outputs off if either output is on, which also cleans up mismatched active states.

## Runtime behavior

There is no maximum runtime in the preserved baseline. If conditions remain favorable, the pair may run all night.

Non-operation is also a valid outcome. If the shop passively equalizes before the thresholds are met, the automation does nothing.

## Humidity role

The baseline uses outdoor relative humidity as a crude guardrail:

```text
outdoor RH < 85%  = start allowed
outdoor RH >= 85% = stop or block
```

Dew-point logic remains deferred.

## Sensor roles

- **Floor:** conservative slab and thermal-mass reference.
- **Indoor:** occupied-zone and general shop-air reference.
- **Ceiling:** upper-layer stored-heat reference.

Start can be justified by any one reference. Stop requires convergence across all three so extraction does not stop while removable heat remains in another layer.

## Window role

Rear windows are manual/passive ventilation paths. They are not automation gates in this baseline. Open windows do not block paired extraction when the active conditions are otherwise satisfied.

## Accepted limitations

- Home Assistant restart recovery relies on normal scheduled rechecks.
- Stale-sensor detection is not included.
- Dew-point calculation is not included.
- Occupancy or motion detection is not included.
- AC automation is not included.
- Manual off may be repaired while valid extraction conditions remain true.
- Manual on may be corrected when stop conditions are true.

## Field reference

The July 12–13, 2026 good run is documented in [`../data/field-runs/2026-07-12-night-extraction-good-run.md`](../data/field-runs/2026-07-12-night-extraction-good-run.md).

The outdoor thermometer is mounted high under an eave. The baseline uses that observed local sensor rather than public forecast data.
