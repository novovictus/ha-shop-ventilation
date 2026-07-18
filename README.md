# Home Assistant Shop Ventilation

Home Assistant configuration and field notes for a nighttime heat-extraction system in a high-ceiling shop.

The system uses a powered intake shutter with a small aperture fan, a separate extraction blower, and local temperature and humidity sensors. It is intended to remove stored heat when outdoor air is useful, not to act as a comfort thermostat or general HVAC controller.

## Status

The July 2026 paired-output configuration is the last working baseline. Both automations are currently disabled in Home Assistant while the system is under review.

- [Start automation](home-assistant/shop-night-heat-extraction-start.yaml)
- [Stop automation](home-assistant/shop-night-heat-extraction-stop.yaml)

These are separate Home Assistant UI automation exports and should be imported separately.

## Physical system

- `switch.damper_switch` controls a J & D VRSG12A-PS 12-inch powered intake shutter and a 10-inch Sarasota Breeze aperture fan through a THIRDREALITY ZigBee smart plug.
- `switch.blower_switch` controls the larger extraction blower.
- The baseline operates both outputs together as one extraction pair.
- Loss of power stops both fans and allows the spring-return shutter to close.

The shutter was installed in a framed 12 x 12-inch wall opening with aluminum trim, weather sealant, and galvanized hardware cloth protecting the exterior aperture.

## Baseline control model

The start automation evaluates at sunset plus 20 minutes, every 20 minutes overnight, and when either controlled output turns off. A run may start only when:

- the bay door is closed;
- AC/heat is off;
- outdoor RH is below 85%; and
- outdoor air is sufficiently cooler than at least one shop reference.

```text
outdoor <= floor - 3°F
OR outdoor <= indoor - 3°F
OR outdoor <= ceiling - 5°F
```

When valid, both the damper and blower turn on. A mismatched state is treated as repairable.

The stop automation turns both outputs off at sunrise, when AC/heat starts, when the bay opens, when outdoor RH reaches 85%, or when useful cooling advantage is gone across all three shop references.

```text
outdoor >= floor - 1°F
AND outdoor >= indoor - 1.5°F
AND outdoor >= ceiling - 2.5°F
```

There is no maximum runtime in this preserved baseline. Non-operation is also valid when the shop passively equalizes before the thresholds are met.

## Entities

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

Rear-window and indoor humidity sensors are observed but are not automation gates in this baseline. Dew-point, occupancy, stale-sensor, restart-recovery, window-control, and AC-control logic are not included.

## Reference field run

The first clean long paired-extraction run occurred overnight on July 12-13, 2026.

| Metric | Result |
|---|---:|
| Runtime | 7 h 20 m 54 s |
| Estimated energy | 1.63 kWh |
| Indoor temperature change | -6.3°F |
| Ceiling temperature change | -6.5°F |
| Floor temperature change | -3.8°F |
| Stop condition | Outdoor RH reached 85.3% |

The run maintained damper on, blower on, AC/heat off, and bay closed for the full interval. Rear windows were open and did not prevent useful extraction. The run started because indoor and ceiling air had sufficient temperature advantage even though the older floor-only rule would not yet have triggered.

## Repository layout

```text
README.md
LICENSE
home-assistant/
  shop-night-heat-extraction-start.yaml
  shop-night-heat-extraction-stop.yaml
```

## Safety

This repository records control logic and an installed physical arrangement. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.

## License

MIT. See [LICENSE](LICENSE).
