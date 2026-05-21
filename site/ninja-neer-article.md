# Building a Home Assistant Controlled Ventilation System for a High-Ceiling Shop

## Subtitle

Why this is a thermal-purge controller, not just a fan automation.

## Draft

A high-ceiling shop does not behave like a normal room. Heat can collect far above the occupied zone, the slab stores energy, and opening the bay door is not always practical. A thermostat at working height can say the room is acceptable while a large heat reservoir remains trapped near the ceiling.

This project uses Home Assistant to manage that problem as a staged control loop. Outdoor air temperature, occupied-zone temperature, and upper-zone temperature are compared before the system runs. If a purge is useful, Home Assistant opens a powered shutter damper, waits for the damper to open, starts a blower, and then shuts the system down in reverse order.

The goal is not to create a universal HVAC product. The goal is to document a practical reference pattern for high-bay shops, garages, barns, and similar workspaces where stratification and thermal mass matter.

## Article outline

1. The problem: high ceilings hide heat.
2. Why normal thermostat logic is insufficient.
3. Hardware architecture.
4. Damper and blower sequencing.
5. Sensor placement.
6. Home Assistant control model.
7. Bench testing.
8. Power profile observations.
9. First deployment results.
10. Lessons learned.
