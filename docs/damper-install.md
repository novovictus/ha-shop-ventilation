# Damper Install

## Status

This note documents the physical intake shutter and aperture fan used by the July 2026 working baseline. The associated Home Assistant automations are currently disabled while the system is under review.

## Purpose

The damper installation provides a controlled exterior air path for nighttime heat extraction. It is not a comfort thermostat and is not intended to operate during occupied daytime AC use.

The physical subsystem:

- opens a powered exterior shutter;
- runs a small fan through that aperture;
- provides a controlled intake path for the larger extraction blower;
- fails closed when power is removed.

## Primary components

- J & D Aluminum Intake Motorized Power Shutter, 12 inch, VRSG12A-PS
- Sarasota Breeze Box Fan, 10 inch
- THIRDREALITY ZigBee Smart Plug with real-time energy monitoring, 15A outlet
- 2x4 framing
- Lexel all-weather sealant
- Amerimax 1.5 in. x 12 ft white aluminum J-channel trim
- Reused hex-head fasteners with rubber sealing washers
- Blue Hawk 10 ft x 3 ft galvanized steel hardware cloth

## Wall penetration

The corrugated shop wall was cut with an angle grinder. The opening was framed with 2x4s, and the interior plywood wall was opened to a 12 in. x 12 in. aperture.

## Exterior sealing and protection

The shutter was sealed with Lexel all-weather sealant. White aluminum J-channel trim and reused hex-head fasteners with rubber sealing washers provide weather-resistant fastening.

Galvanized steel hardware cloth protects the exterior aperture.

## Fan mounting

A 10 inch Sarasota Breeze box fan was mounted inside the 12 inch shutter path. Wire from the hardware cloth installation was reused to secure the fan.

## Electrical and fail-state behavior

The motorized shutter and small aperture fan are powered together through one THIRDREALITY ZigBee smart plug exposed to Home Assistant as:

```text
switch.damper_switch
```

When the switch turns on, the shutter opens and the aperture fan runs. The damper motor holds the shutter open while powered.

When the switch turns off, the fan stops and the shutter spring-returns closed. The subsystem is therefore fail-off and fail-closed on power loss, smart-plug shutdown, or automation stop.

## Relationship to the extraction blower

The larger extraction blower is controlled separately as:

```text
switch.blower_switch
```

The July 2026 baseline operates `switch.damper_switch` and `switch.blower_switch` together as one active extraction pair. The intake shutter/fan provides the controlled air path; the separate blower provides the primary extraction airflow.

Current control behavior and thresholds are documented in [`night-purge-process.md`](night-purge-process.md).

## Safety boundary

This document records the installed physical arrangement. It is not an electrical wiring guide. Mains-voltage work should be designed, installed, and verified according to local code by a qualified electrician.
