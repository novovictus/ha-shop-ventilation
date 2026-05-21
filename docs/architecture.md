# Architecture

The system is a staged controller, not a single switch.

```text
Outdoor shaded temperature
Occupied-zone shop temperature
Upper-zone shop temperature
        |
        v
Home Assistant purge decision
        |
        v
Damper opens
        |
        v
Delay for open travel
        |
        v
Blower starts
        |
        v
Runtime and thermal trend monitoring
        |
        v
Blower stops
        |
        v
Delay for airflow settling
        |
        v
Damper de-energizes and spring-closes
```

## Major components

- Sensors provide environmental context.
- Home Assistant owns the state machine and runtime rules.
- The Shelly module provides controlled switching and power observation.
- The powered shutter damper creates a controlled intake path.
- The blower moves air through the shop after the damper is open.

## Design principles

- Fail closed where possible.
- Avoid simultaneous damper and blower transitions.
- Do not rely on one indoor temperature sensor.
- Use minimum runtime and cooldown rules to avoid short cycling.
- Keep electrical implementation separate from automation logic.
