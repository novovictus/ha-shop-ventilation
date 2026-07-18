# July 12-13, 2026 Night Extraction Run

## Summary

This engineering record documents the first clean long automated night-extraction run after the July 2026 paired-control update.

The automation maintained the intended active state for the full run: damper on, blower on, AC/heat off, bay door closed, and no damper/blower mismatch.

## Source

- Source: Home Assistant history CSV supplied after the run
- Export window: July 12, 2026 07:42:35 EDT through July 13, 2026 14:42:50 EDT
- Analysis timezone: America/New_York
- The raw CSV is not committed; this note preserves the reduced field evidence

## Run window

| Metric | Value |
|---|---:|
| Start | July 12, 2026 21:20:00 EDT |
| Stop | July 13, 2026 04:40:54 EDT |
| Runtime | 7 h 20 m 54 s |
| Runtime decimal | 7.35 h |
| Start interpretation | Outdoor air was usefully cooler than indoor and ceiling air |
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
| Jul 12 21:20 | 75.9°F | 78.3°F | 79.3°F | 80.1°F | 63.7% |
| Jul 12 22:20 | 74.7°F | 77.9°F | 77.7°F | 78.3°F | 65.7% |
| Jul 12 23:20 | 72.3°F | 77.4°F | 76.6°F | 77.4°F | 67.8% |
| Jul 13 00:20 | 70.9°F | 76.8°F | 75.9°F | 76.5°F | 69.8% |
| Jul 13 01:20 | 70.9°F | 76.1°F | 75.0°F | 75.7°F | 74.5% |
| Jul 13 02:20 | 70.9°F | 75.7°F | 74.3°F | 75.0°F | 72.5% |
| Jul 13 03:20 | 70.0°F | 75.2°F | 73.8°F | 74.5°F | 75.2% |
| Jul 13 04:20 | 67.3°F | 74.7°F | 73.2°F | 73.9°F | 81.2% |
| Jul 13 04:40 | 66.2°F | 74.5°F | 73.0°F | 73.6°F | 85.3% |

## Cooling performance

| Reference | Change | Average rate |
|---|---:|---:|
| Outdoor | -9.7°F | -1.32°F/h |
| Floor | -3.8°F | -0.52°F/h |
| Indoor | -6.3°F | -0.86°F/h |
| Ceiling | -6.5°F | -0.88°F/h |

The air layers responded faster than the floor, consistent with the expected thermal-mass behavior. The floor still moved nearly 4°F, showing that the result was more than an air-temperature artifact.

## Electrical metrics

| Metric | Damper | Blower | Combined |
|---|---:|---:|---:|
| Average power while running | 34.2 W | 188.0 W | 222.2 W |
| Observed maximum while running | 35.0 W | 192.0 W | 227.0 W |
| Estimated run energy | 0.25 kWh | 1.38 kWh | 1.63 kWh |

The energy estimate uses one-minute forward-filled power samples during the active run window.

## Why this run matters

The older floor-only rule would not have started at 21:20:

```text
outdoor = 75.9°F
floor   = 78.3°F
delta   = 2.4°F
```

The old rule required outdoor air to be at least 3°F cooler than the floor. The paired baseline started because outdoor air was 3.4°F cooler than the indoor layer and 4.2°F cooler than the ceiling layer.

This supports the change from floor-only damper control to paired damper/blower extraction using floor, indoor, and ceiling references.

## Field observations

- The paired-output repair logic worked: damper and blower switched on together and remained paired.
- AC/heat remained off and the bay door remained closed, avoiding conflict with occupied cooling or uncontrolled bay ventilation.
- Rear windows were open for the full run and did not prevent useful extraction.
- The run ended on humidity rather than temperature convergence. Outdoor air was still materially cooler than the shop at shutdown.
- Air-layer temperatures changed faster than the floor, confirming that the slab and lower building mass respond more slowly.

## Related warm/humid lessons

Other field cycles showed that a cool, dry occupied-zone bubble can coexist with a much hotter ceiling layer. Turning AC off can produce rapid rebound because the roof, shell, slab, and upper air remain heat-loaded.

Blower or outside-air operation is not automatically beneficial merely because the ceiling is hot. During warm, humid occupied conditions, forced airflow can raise work-area humidity without materially controlling the upper heat reservoir. The damper/blower pair is therefore best reserved for unoccupied periods when outdoor air has useful thermal value and the moisture tradeoff is acceptable.

Evening storms and cooldowns can provide useful temperature reduction while carrying high moisture. Temperature benefit and humidity cost must be evaluated together; continued forced purge after the useful heat-removal phase can import wet air without proportionate cooling benefit.

## Conclusion

This run is the reference case for the July 2026 paired-extraction baseline:

```text
7.35 hours paired runtime
1.63 kWh estimated energy
-6.3°F indoor
-6.5°F ceiling
-3.8°F floor
humidity stop at 85.3% outdoor RH
```

It provides the comparison point for future threshold changes, especially any move from raw outdoor RH to dew-point-based control.