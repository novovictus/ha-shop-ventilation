# Home Assistant Shop Ventilation Controller

A Home Assistant reference design for staged warm-weather thermal purge in a high-ceiling shop using a powered damper/fan, supplemental blower, rear-window intent sensors, layered thermometers, and fail-off control logic.

This project treats shop cooling as a thermal management problem, not a simple comfort thermostat. In a high-bay shop, warm air pools near the ceiling, the concrete slab stores and releases heat, and opening the bay door is not always practical. A single indoor thermometer can miss the upper heat reservoir that drives discomfort and overnight heat carryover.

The current process is intentionally simple and observational. A rear window open state is the manual arming signal. Ceiling temperature delta is the primary reason to run. The damper/fan runs only when outdoor air is useful, while the blower can run by itself to mix trapped ceiling heat. A floor/slab pass is included as a secondary stage after the ceiling zone has equalized.

## Project status

Initial field-tested warm-weather process. The current YAML is being held deliberately simple so real usage can expose bugs, bad assumptions, and tuning needs before adding more lockouts or state-machine complexity.

## Initial field observation

An initial warm-weather test showed strong stratification: the ceiling zone cooled substantially over the evening while the floor/slab sensor moved only slightly. That observation supports the current ceiling-first purge model, with the floor pass treated as a slower secondary stage. See `docs/warm-weather-process.md` for the detailed field-process notes.

## System goals

- Remove trapped high-bay heat when outdoor air is favorable.
- Use outdoor, indoor, ceiling, and floor temperature layers to account for stratification and slab heat.
- Use either rear window as the human intent signal.
- Keep the damper/fan off unless outside air is useful.
- Allow blower-only mixing when the ceiling is hot but outside air is not useful.
- Include a secondary floor/slab purge after the ceiling zone has equalized.
- Shut down both switches when no rear window is open or required sensor values are invalid.
- Document the design as a reusable Home Assistant reference pattern, not a universal wiring guide.

## Hardware baseline

- Powered damper/fan controlled by Home Assistant as `switch.damper_switch`.
- Supplemental ceiling-heat mixing blower controlled as `switch.blower_switch`.
- Rear window opening sensors:
  - `binary_sensor.back_left_window_opening`
  - `binary_sensor.back_right_window_opening`
- Temperature sensors:
  - `sensor.outdoor_thermometer_temperature`
  - `sensor.indoor_thermometer_temperature`
  - `sensor.ceiling_thermometer_temperature`
  - `sensor.floor_thermometer_temperature`
- Home Assistant automation using Shelly and Zigbee entity naming as installed.

## Current control model

```text
DISARMED
  no rear window open, or invalid sensor values
  damper/fan off, blower off

CEILING_PURGE
  rear window open, ceiling hot, outside air useful
  damper/fan on, blower on

BLOWER_ONLY_MIX
  rear window open, ceiling hot, outside air not useful
  damper/fan off, blower on

FLOOR_PASS
  rear window open, ceiling equalized, floor/slab still warm, outside air useful for floor purge
  damper/fan on, blower off

DONE
  rear window open, ceiling equalized, floor pass no longer useful
  damper/fan off, blower off
```

## Current implementation

- `home-assistant/shop-warm-weather-purge.yaml` contains the current warm-weather purge automation.
- `docs/warm-weather-process.md` documents the operating model, derived values, thresholds, field observations, and control boundaries.
- `docs/entity-map.md` records the current entity IDs and historical renamed prefixes.

The YAML file is written as a Home Assistant automation definition. If used inside a package file, wrap it under `automation:`.

## Current non-goals

- Do not run based only on indoor thermometer comfort.
- Do not automatically decide that the shop needs AC.
- Do not use bay door state until that sensor/interlock is intentionally added.
- Do not treat the floor pass as proven optimal yet.

## Known future work

These are intentionally not active requirements in the current automation:

- Bay door sensor gate. When added, the intended armed condition is: at least one rear window open and bay door closed.
- Further tuning after more field observations.

## Repository layout

```text
docs/              Design notes, process documentation, entity map
home-assistant/    Home Assistant automation YAML
data/              Bench-test and power-profile data
scripts/           Small analysis helpers
site/              Website/article draft material
photos/            Placeholders for bench-test and installation photos
```

## Safety boundary

This repository documents architecture, control logic, sensor placement, and Home Assistant implementation. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.

## License

MIT. See [LICENSE](LICENSE).
