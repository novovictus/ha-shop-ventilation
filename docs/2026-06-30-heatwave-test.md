# 2026-06-30 Heatwave Test

## Purpose

Record the current v1 nighttime heat-extraction test deployed before the Lancaster heatwave.

The goal is not to automate comfort. The goal is to prevent hot mornings when outdoor air was cool enough overnight to help remove stored heat from the shop floor/slab and building mass.

## Current deployed control

The deployed Home Assistant logic uses two UI automations:

- `Shop Night Heat Extraction - Start`
- `Shop Night Heat Extraction - Stop`

The current repo mirror is:

```text
home-assistant/shop-night-purge.yaml
```

The retained filename is historical. The active logic is now v1 heat extraction, not the older rear-window/blower purge cycle.

## Start intent

Start only when all of the following are true:

- After sunset plus 20 minutes.
- Before sunrise.
- Bay door closed.
- AC/heat switch off.
- Damper/fan switch off.
- Outdoor temperature is at least 3°F below floor temperature.
- Outdoor RH is below 85%.

## Stop intent

Stop when any of the following are true:

- Sunrise.
- Bay door opens.
- AC/heat switch turns on.
- Outdoor temperature rises to within 1°F below floor temperature.
- Outdoor RH reaches the 85% cutoff.

## Expected valid outcomes

Valid outcomes include:

- The automation never starts because the shop passively equalizes well enough.
- The automation starts briefly when the outdoor/floor delta becomes favorable.
- The automation runs for a long period if the floor remains heat-loaded and outdoor conditions remain useful.

A non-start is not a failure. It means the shop did not need electricity for that interval.

## Deferred work

Deferred until after this heatwave test:

- Dew point calculation.
- Window automation.
- Motion or occupancy integration.
- AC automation after sunrise.
- Ceiling-driven purge logic.
- Supplemental blower control.
- Stale-sensor handling.
- Restart recovery.
- Notifications.

## Next phase concept

After the heatwave, evaluate whether the night extraction cycle reduces hot mornings. If it does, keep the night extraction logic conservative and separate.

The next likely phase is AC automation after sunrise when observed outdoor conditions indicate the shop is about to become heat-soaked. That should remain a separate automation phase from nighttime extraction.
