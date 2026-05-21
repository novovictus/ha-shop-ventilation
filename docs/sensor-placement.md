# Sensor placement

The key differentiator in this project is measuring more than one thermal layer.

## Required sensors

### Outdoor shaded ambient

Use an outdoor temperature source that is not sun-loaded and is representative of air available to the intake.

Avoid:

- Direct sunlight.
- Surfaces that radiate stored heat.
- Enclosures that trap heat.

### Occupied-zone indoor

Place near normal working height and away from direct blower discharge, direct AC output, and wall surfaces that skew the reading.

This sensor represents comfort and the temperature a person feels while working.

### Upper-zone indoor

Place high enough to detect trapped heat above the occupied zone. For this shop, the likely target is the top third of the space, roughly 18 to 22 ft up.

This sensor should not be directly in the blower jet unless the intent is to measure moving air after purge starts. The goal is to detect the heat reservoir before ventilation begins.

## Optional sensors

- Slab or low-zone temperature.
- Indoor humidity and dew point.
- Outdoor humidity and dew point.
- Door/window state.
- Damper and blower power draw.

## Why upper-zone sensing matters

A comfortable occupied-zone temperature can coexist with a large heat reservoir near the ceiling. Without an upper-zone sensor, the automation may stop too early or fail to run when a night purge would remove stored heat before it migrates downward.