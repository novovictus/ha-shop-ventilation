# 2026-07-12/13 Night Extraction Good Run

## Summary

This artifact records the first clean long automated night-extraction run after the July 2026 paired-control update.

The run is considered a good reference case because the automation maintained the intended paired active-extraction state for the full run: damper on, blower on, AC/heat off, bay door closed, and no damper-on / blower-off mismatch.

## Source

- Source export: Home Assistant history CSV provided after the run.
- Export window: 2026-07-12 07:42:35 EDT through 2026-07-13 14:42:50 EDT.
- Analysis timezone: America/New_York.
- Raw CSV is intentionally not committed here. This file preserves the reduced field metrics.

## Run window

| Metric | Value |
|---|---:|
| Start | 2026-07-12 21:20:00 EDT |
| Stop | 2026-07-13 04:40:54 EDT |
| Runtime | 7 h 20 m 54 s |
| Runtime decimal | 7.35 h |
| Start trigger interpretation | Outdoor air was usefully cooler than indoor/ceiling air |
| Stop interpretation | Outdoor RH crossed the 85% guardrail |

## Control-state validation

| Entity | State during run |
|---|---|
| `switch.damper_switch` | `on` for full run |
| `switch.blower_switch` | `on` for full run |
| `switch.ac_heat_switch_switch` | `off` for full run |
| `binary_sensor.bay_door_opening` | `off` / closed for full run |
| `binary_sensor.back_left_window_opening` | `on` / open for full run |
| `binary_sensor.back_right_window_opening` | `on` / open for full run |
| `binary_sensor.door_opening` | `off` / closed for full run |

## Temperature and humidity deltas

| Sensor | Start | Stop | Change |
|---|---:|---:|---:|
| Outdoor temperature | 75.9°F | 66.2°F | -9.7°F |
| Floor temperature | 78.3°F | 74.5°F | -3.8°F |
| Indoor temperature | 79.3°F | 73.0°F | -6.3°F |
| Ceiling temperature | 80.1°F | 73.6°F | -6.5°F |
| Outdoor RH | 63.7% | 85.3% | +21.6 points |
| Floor RH | 62.0% | 61.9% | -0.1 points |
| Indoor RH | 58.0% | 64.0% | +6.0 points |
| Ceiling RH | 53.4% | 57.9% | +4.5 points |

## Hourly trace

| Time | Outdoor | Floor | Indoor | Ceiling | Outdoor RH |
|---|---:|---:|---:|---:|---:|
| 2026-07-12 21:20 | 75.9°F | 78.3°F | 79.3°F | 80.1°F | 63.7% |
| 2026-07-12 22:20 | 74.7°F | 77.9°F | 77.7°F | 78.3°F | 65.7% |
| 2026-07-12 23:20 | 72.3°F | 77.4°F | 76.6°F | 77.4°F | 67.8% |
| 2026-07-13 00:20 | 70.9°F | 76.8°F | 75.9°F | 76.5°F | 69.8% |
| 2026-07-13 01:20 | 70.9°F | 76.1°F | 75.0°F | 75.7°F | 74.5% |
| 2026-07-13 02:20 | 70.9°F | 75.7°F | 74.3°F | 75.0°F | 72.5% |
| 2026-07-13 03:20 | 70.0°F | 75.2°F | 73.8°F | 74.5°F | 75.2% |
| 2026-07-13 04:20 | 67.3°F | 74.7°F | 73.2°F | 73.9°F | 81.2% |
| 2026-07-13 04:40 | 66.2°F | 74.5°F | 73.0°F | 73.6°F | 85.3% |

## Cooling performance

| Reference | Change | Average rate |
|---|---:|---:|
| Outdoor | -9.7°F | -1.32°F/h |
| Floor | -3.8°F | -0.52°F/h |
| Indoor | -6.3°F | -0.86°F/h |
| Ceiling | -6.5°F | -0.88°F/h |

The air layers responded faster than the floor, which matches the expected thermal-mass model. The floor still moved nearly 4°F, which makes this a useful overnight heat-removal result rather than only an air-temperature artifact.

## Electrical metrics

| Metric | Damper | Blower | Combined |
|---|---:|---:|---:|
| Average power while running | 34.2 W | 188.0 W | 222.2 W |
| Observed max power while running | 35.0 W | 192.0 W | 227.0 W |
| Estimated run energy | 0.25 kWh | 1.38 kWh | 1.63 kWh |

Energy estimate is based on one-minute forward-filled power samples during the active run window.

## Why this run matters

The older floor-only rule would not have started immediately at 21:20.

At start:

```text
outdoor = 75.9°F
floor   = 78.3°F
delta   = 2.4°F
```

The old start rule required:

```text
outdoor <= floor - 3°F
```

That condition was not yet true.

The revised logic allowed the run because the outdoor air was usefully cooler than the shop air layer:

```text
indoor  = 79.3°F -> outdoor was 3.4°F cooler
ceiling = 80.1°F -> outdoor was 4.2°F cooler
```

This validates the July 2026 change from floor-only damper control to paired damper/blower extraction with floor, indoor, and ceiling thermal references.

## Observations

- The paired-output repair logic worked: damper and blower switched on at the same time and stayed paired.
- The bay door remained closed, avoiding uncontrolled daytime-style purge behavior.
- AC/heat remained off, avoiding conflict between extraction and conditioned cooling.
- Rear windows were open for the full run. This did not prevent active extraction, and the blower still produced useful cooling.
- The run stopped on humidity, not on temperature convergence. At stop, outdoor air was still materially cooler than the shop, so the RH guardrail was the controlling limiter.

## Field conclusion

This is a canonical good automated run for the current v1 paired-extraction model.

Practical result:

```text
7.35 hours of paired damper/blower runtime
1.63 kWh estimated energy
-6.3°F indoor
-6.5°F ceiling
-3.8°F floor
clean humidity stop at 85.3% outdoor RH
```

Keep this run as the baseline for comparing future threshold changes, especially any later move from raw outdoor RH to dew-point-based control.
