# Problem statement

Most shop fan automations reduce the problem to a single rule: if inside is hot and outside is cooler, turn on a fan.

That is insufficient for this shop.

The actual environment has several coupled constraints:

- A 24+ ft ceiling allows heat to stratify high above the occupied zone.
- A concrete slab stores and releases heat, delaying temperature response.
- The bay door cannot remain open overnight.
- Existing high rear windows provide limited passive ventilation.
- The blower can move air, but it needs a controlled intake path.
- The wall penetration should fail closed when power or control is lost.
- Motors and dampers should not be short-cycled.

The control problem is therefore not simply comfort cooling. It is controlled removal of trapped thermal energy when outdoor conditions are favorable.

## Goal

Build a Home Assistant controlled ventilation pattern that:

1. Detects when a thermal purge is useful.
2. Opens a powered intake damper before starting airflow.
3. Runs a blower only while outdoor air can remove heat.
4. Shuts down in a safe reverse sequence.
5. Exposes state, runtime, and fault information in Home Assistant.
