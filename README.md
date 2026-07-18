# Home Assistant Shop Ventilation

Documentation, working configuration, and field results from a Home Assistant-controlled nighttime heat-extraction system built for a high-ceiling shop.

The system uses a powered intake damper, a separate extraction blower, local environmental sensors, and conservative fail-off logic to remove stored heat when outdoor conditions are favorable. It is a thermal-management experiment, not a comfort thermostat or general HVAC controller.

## Current status

The July 2026 paired-output configuration is the last working baseline. Both Home Assistant automations are currently disabled while the system is under review.

The repository preserves that known-good configuration for inspection, testing, and eventual re-enablement. Disabled does not mean obsolete: these files represent the configuration that produced the documented field run.

## Control model

During the overnight window, the start automation periodically checks that the bay is closed, AC/heat is off, outdoor humidity is acceptable, and outdoor air is sufficiently cooler than at least one shop thermal reference. When those conditions are met, the damper and blower run as a pair.

The stop automation turns both outputs off at sunrise, when AC/heat starts, when the bay opens, when outdoor relative humidity reaches 85%, or when useful temperature advantage has been lost across the floor, indoor, and ceiling references.

Detailed behavior and thresholds are documented in [`docs/night-purge-process.md`](docs/night-purge-process.md).

## Working baseline

- [Start automation](home-assistant/automations/shop-night-heat-extraction-start.yaml)
- [Stop automation](home-assistant/automations/shop-night-heat-extraction-stop.yaml)
- [Home Assistant baseline notes](home-assistant/README.md)

The files are separate Home Assistant UI automation exports and should be imported as two separate automations.

## Physical system

- `switch.damper_switch` controls the powered intake shutter and its small aperture fan.
- `switch.blower_switch` controls the larger extraction blower.
- The July 2026 baseline operates both outputs together as the active extraction pair.
- Loss of power closes the spring-return intake shutter and stops airflow equipment.

Physical installation details are recorded in [`docs/damper-install.md`](docs/damper-install.md).

## Field result

The first clean long automated paired-extraction run lasted 7.35 hours and used an estimated 1.63 kWh. During the run:

- Indoor temperature fell 6.3°F.
- Ceiling temperature fell 6.5°F.
- Floor temperature fell 3.8°F.
- The automation stopped when outdoor RH reached 85.3%.

See [`data/field-runs/2026-07-12-night-extraction-good-run.md`](data/field-runs/2026-07-12-night-extraction-good-run.md) for the reduced field evidence.

## Repository contents

```text
home-assistant/    Last working Home Assistant automation baseline
docs/              Control, entity, and physical-install documentation
data/              Reduced field-run evidence
```

Key documents:

- [`docs/night-purge-process.md`](docs/night-purge-process.md): baseline operating model and thresholds.
- [`docs/entity-map.md`](docs/entity-map.md): Home Assistant entities used by the baseline.
- [`docs/damper-install.md`](docs/damper-install.md): physical intake shutter and fan installation.

## Non-goals

- Occupied comfort thermostat control.
- Automatic window operation.
- Automatic AC decisions.
- Dew-point control in the preserved baseline.
- Occupancy or motion logic.

## Safety boundary

This repository documents control logic, sensor use, physical installation, and observed results. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.

## License

MIT. See [LICENSE](LICENSE).
