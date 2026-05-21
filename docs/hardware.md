# Hardware

## Damper

J&D VRSG12A-PS 12 inch motorized aluminum intake shutter.

Relevant project assumptions:

- 120V operation will be used.
- Power-open, spring-return behavior is expected.
- Energized means open.
- De-energized means spring return to closed.
- Power or control loss should close the intake path.

Bench testing should confirm lead selection, current draw, open time, close time, and motor temperature during an extended open period.

## Blower

Existing 120V blower previously operated through a THIRDREALITY Zigbee smart plug with power monitoring.

Observed running profile from Home Assistant history:

- Current: approximately 1.8 to 1.9 A.
- Power: approximately 180 to 192 W.
- Frequency: 60 Hz.
- Long continuous runs were observed without obvious abnormal telemetry.

The smart-plug data is useful for steady-state load characterization, but it may not capture first-cycle motor inrush.

## Controller

Shelly 1PM Gen4 is the initial control and monitoring module.

Preferred rugged architecture keeps the control logic separate from the motor switching decision. The Shelly may directly switch small loads, but a motor-rated relay or contactor remains cleaner for permanent blower control.

## Sensors

Minimum viable sensors:

- Outdoor shaded ambient temperature.
- Occupied-zone shop temperature.
- Upper-zone shop temperature.

Optional future sensors:

- Indoor and outdoor humidity/dew point.
- Slab or low-zone temperature.
- Door/window state.
- Damper and blower power monitoring.
