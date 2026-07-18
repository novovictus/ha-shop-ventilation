# Damper Installation Engineering Note

This note records the physical intake damper and aperture-fan subsystem used by the shop heat-extraction system.

Home Assistant exposes the subsystem as one output:

```text
switch.damper_switch
```

When energized, that output opens the exterior shutter and runs the small aperture fan. The separate extraction blower is controlled as `switch.blower_switch`.

## Purpose

The installation provides a controlled exterior air path for nighttime heat extraction. It is not a comfort thermostat and is not intended to operate during occupied daytime AC use.

The subsystem is intended to:

- open a powered exterior shutter;
- run a small fan through the intake path;
- provide makeup airflow for removal of stored shop heat when outdoor conditions are favorable; and
- fail closed when power is removed.

## Primary components

- J & D Aluminum Intake Motorized Power Shutter, 12 inch, model VRSG12A-PS
- Sarasota Breeze Box Fan, 10 inch
- THIRDREALITY ZigBee Smart Plug with real-time energy monitoring, 15 A outlet
- 2x4 framing
- Lexel all-weather sealant
- Amerimax 1.5 inch x 12 ft white aluminum J-channel trim
- Reused hex-head fasteners with rubber sealing washers from the window installation
- Blue Hawk 10 ft x 3 ft galvanized steel hardware cloth

## Wall penetration

The corrugated shop wall was cut with an angle grinder. The opening was framed with 2x4 lumber, and the interior plywood wall was opened to a 12 inch x 12 inch aperture.

## Exterior sealing and trim

The shutter was sealed with Lexel all-weather sealant. Amerimax white aluminum J-channel trim was installed before the sealant cured. Reused hex-head fasteners with rubber sealing washers from the window installation were used for weather-resistant fastening.

## Exterior screen and protection

Blue Hawk galvanized steel hardware cloth was fastened outside the framed opening to protect the exterior aperture.

## Fan mounting

A 10 inch Sarasota Breeze box fan was mounted inside the 12 inch shutter path. Wire left from the hardware-cloth installation was reused to secure the fan.

## Electrical and fail-state behavior

The J & D motorized shutter and the 10 inch Sarasota Breeze fan are powered together from a single THIRDREALITY ZigBee smart plug with real-time energy monitoring. Home Assistant exposes that plug as:

```text
switch.damper_switch
```

When `switch.damper_switch` turns on, the motorized shutter opens and the aperture fan runs. The damper motor remains energized to hold the shutter open.

When `switch.damper_switch` turns off, the fan stops and the shutter spring-returns closed. The subsystem is therefore fail-off and fail-closed on power loss, smart-plug shutdown, or automation stop.

## Home Assistant integration

The preserved July 2026 baseline treats the intake subsystem and the larger extraction blower as one active extraction pair:

```text
switch.damper_switch
switch.blower_switch
```

The detailed operating thresholds remain in the root README and the two baseline automation exports. Keeping those rules out of this note prevents the physical installation record from becoming stale when control logic changes.

## Design notes

This subsystem is the existing powered aperture in the shop ventilation design. Any future powered-window or hopper-window system should be treated as a separate passive or semi-passive air-path subsystem, not as a replacement for the damper/fan path.

Because the damper/fan path fails closed, any future powered opening should meet a similar safety standard: confirmed closed state, weather guardrails, and a conservative failure mode.
