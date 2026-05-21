# Home Assistant Shop Ventilation Controller

A Home Assistant reference design for staged thermal-purge ventilation in a high-ceiling shop using a powered intake damper, blower, environmental sensors, and fail-closed control logic.

This project treats shop cooling as a thermal management problem, not a simple fan automation. In a high-bay shop, warm air pools near the ceiling, the concrete slab stores and releases heat, and opening the bay door is not always practical. A single occupied-zone temperature sensor can miss the upper heat reservoir that drives discomfort and overnight heat carryover.

The controller compares outdoor ambient temperature, occupied-zone temperature, and upper-zone temperature. When outside air is useful, Home Assistant opens a powered shutter damper, waits for it to open, starts the blower, monitors runtime and thermal conditions, then shuts down in reverse order.

## Project status

Early reference scaffold. Bench testing and installation data will be added as the physical system is validated.

## System goals

- Remove trapped high-bay heat when outdoor air is favorable.
- Use more than one indoor temperature layer to account for stratification.
- Open the damper before starting the blower.
- Stop the blower before allowing the damper to spring closed.
- Enforce minimum runtime, cooldown, and manual override behavior.
- Keep the building envelope fail-closed on power or control loss.
- Document the design as a reusable Home Assistant pattern, not a universal wiring guide.

## Hardware baseline

- J&D VRSG12A-PS 12 inch motorized aluminum intake shutter.
- Shelly 1PM Gen4 for control and power observation.
- Existing 120V blower, observed around 180 to 192 W and 1.8 to 1.9 A while running.
- Dedicated 120V branch circuit with GFCI protection, installed and verified according to local code.
- Outdoor shaded, occupied-zone, and upper-zone temperature sensors.

## Control sequence

```text
IDLE
  -> PURGE_AVAILABLE
  -> DAMPER_OPENING
  -> BLOWER_RUNNING
  -> BLOWER_STOPPING
  -> DAMPER_CLOSING
  -> COOLDOWN
  -> IDLE
```

Start sequence:

```text
1. Confirm purge conditions.
2. Energize damper.
3. Wait for damper open time.
4. Start blower.
5. Monitor runtime and temperature trend.
```

Stop sequence:

```text
1. Stop blower.
2. Wait for airflow to settle.
3. De-energize damper.
4. Allow spring return to close the shutter.
5. Enter cooldown or lockout period.
```

## Repository layout

```text
docs/              Design notes, architecture, safety boundary, state machine
home-assistant/    Starter package and dashboard examples
data/              Bench-test and power-profile data
scripts/           Small analysis helpers
site/              Website/article draft material
photos/            Placeholders for bench-test and installation photos
```

## Safety boundary

This repository documents architecture, control logic, sensor placement, and Home Assistant implementation. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.

## License

MIT. See [LICENSE](LICENSE).
