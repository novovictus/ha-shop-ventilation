# Damper Install

This note documents the physical damper/fan subsystem used by the current shop heat-extraction automation.

The Home Assistant control logic treats this subsystem as one output:

```text
switch.damper_switch
```

In v1, that output energizes the exterior shutter and fan together for nighttime heat extraction when outdoor air is cooler than the shop floor and humidity is acceptable.

## Purpose

The damper install provides a controlled exterior air path for the shop heat-extraction system. It is not a comfort thermostat and is not intended to run during occupied daytime AC operation.

The subsystem is used to:

- open a powered exterior shutter;
- run a small fan through that air path;
- remove useful stored heat from the shop floor, slab, and lower building mass when outdoor conditions are favorable;
- fail closed when power is removed.

## Primary components

- J & D Aluminum Intake Motorized Power Shutter, 12 inch, VRSG12A-PS
- Sarasota Breeze Box Fan, 10 inch
- THIRDREALITY ZigBee Smart Plug with real-time energy monitoring, 15A outlet
- 2x4 framing
- Lexel all-weather sealant
- Amerimax 1.5 in. x 12 ft white aluminum J-channel trim
- Reused hex-head fasteners with rubber sealing washers from the window install
- Blue Hawk 10 ft x 3 ft galvanized steel hardware cloth

## Wall penetration

The corrugated shop wall was cut with an angle grinder. The opening was framed with 2x4s. The interior plywood wall was cut open to a 12 in. x 12 in. aperture.

## Exterior sealing and trim

The shutter was sealed with Lexel all-weather sealant. Amerimax white aluminum J-channel trim was installed before the sealant dried. Reused hex-head fasteners with rubber sealing washers from the window install were used for weather-resistant fastening.

## Exterior screen and protection

Blue Hawk galvanized steel hardware cloth was screwed outside the framed opening to protect the exterior aperture.

## Fan mounting

A 10 inch Sarasota Breeze box fan was mounted inside the 12 inch shutter path. Wire wrapping from the Blue Hawk hardware cloth was reused to mount the fan.

## Electrical and fail-state behavior

The J & D motorized shutter and the 10 inch Sarasota Breeze fan are powered together from a single THIRDREALITY ZigBee smart plug with real-time energy monitoring. Home Assistant exposes that plug as:

```text
switch.damper_switch
```

When `switch.damper_switch` turns on, the motorized shutter opens and the fan runs. The damper motor holds the shutter open while powered.

When `switch.damper_switch` turns off, the fan stops and the shutter spring-returns closed. The subsystem is therefore fail-off and fail-closed on power loss, smart-plug shutdown, or automation stop.

## Home Assistant role

The current v1 automation treats `switch.damper_switch` as a combined damper/fan output.

It may start only when:

- time is after sunset plus 20 minutes and before sunrise;
- AC/heat is off;
- bay door is closed;
- outdoor temperature is at least 3°F cooler than the floor temperature;
- outdoor relative humidity is below 85%.

It stops when sunrise occurs, AC/heat turns on, the bay door opens, outdoor air loses the required temperature advantage, or outdoor relative humidity reaches the cutoff.

## Design notes

This subsystem is the existing powered aperture in the shop ventilation design. Future hopper-window automation should be treated as a separate passive or semi-passive air-path subsystem, not as a replacement for this damper/fan path.

Because the damper/fan path fails closed, future window automation should meet a similar safety standard: confirmed closed state, weather guardrails, and a conservative failure mode.