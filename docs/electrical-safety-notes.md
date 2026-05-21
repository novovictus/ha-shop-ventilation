# Electrical safety notes

This repository is not an electrical wiring guide.

The project involves mains-voltage equipment, motorized loads, a powered damper, and a dedicated branch circuit. Electrical work should be designed, installed, inspected, and verified according to local code by a qualified electrician.

## Project-level assumptions

- The blower and damper are 120V loads.
- The circuit is dedicated.
- GFCI protection is planned.
- The physical installation will be validated before energizing.
- The damper should fail closed when power is lost.

## Documentation boundary

This repository documents:

- Control architecture.
- Home Assistant logic.
- Sensor placement.
- State-machine behavior.
- Bench-test results.
- Observed power profiles.

This repository does not provide:

- Site-specific electrical design.
- Code interpretation for a jurisdiction.
- Instructions for energized work.
- A guarantee that a wiring method is compliant in all locations.

## Practical design concerns

- Use dedicated neutral and ground handling appropriate to the circuit.
- Avoid shared neutrals unless specifically designed for that use.
- Protect exposed wiring from physical damage.
- Use enclosures with adequate space for splices, controls, labels, and service loops.
- Provide a manual service or disable method appropriate to the installation.
- Label automated loads clearly.
