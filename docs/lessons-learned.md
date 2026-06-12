# Lessons learned

This file captures field lessons from bench testing, installation, and live shop operation.

## Initial implementation lessons

- The blower is a smaller sustained load than expected based on smart-plug telemetry.
- Smart-plug telemetry is useful for steady-state characterization but may miss motor inrush.
- Upper-zone temperature sensing is central to the control model.
- The project should be framed as thermal-purge control, not simply fan automation.
- Electrical implementation details should remain site-specific and electrician-validated.

## Warm/humid field-cycle lessons

Observed during a hot, humid operating day with AC use, video-call noise constraints, dog/door interruptions, rear-window shutdown behavior, and an evening storm/cooldown.

### Occupied comfort

- Closed shop plus AC can create a cool, dry occupied-zone bubble even while the ceiling layer remains very hot.
- Turning AC off for meeting noise can allow the occupied-zone temperature and humidity to ramp quickly because the shop shell, slab, roof, and upper air remain heat-soaked.
- For occupied work, the controlling comfort variable is the occupied-zone dry-air condition, not the ceiling temperature.
- The useful mental model is: protect the dry work-area bubble while occupied.

### Blower behavior

- Blower operation during hot/humid occupied conditions can raise work-area humidity without meaningfully stopping upper-zone heat gain.
- The blower is not automatically helpful just because the ceiling is hot.
- The blower/damper combo should be reserved for unoccupied purge opportunities where outdoor air is thermally useful and the moisture penalty is acceptable.

### Door and window interpretation

- The standard side door is an occupancy/recent-activity signal, not a major ventilation strategy.
- A standard side-door opening is smaller than a bay-door event, but it usually means entry, exit, dog movement, loading, or shutdown activity.
- Rear windows open after shutdown are a manual purge-preparation signal, not proof of occupancy.
- Bay door open remains a strong occupied/manual-use boundary.

### Humidity and storms

- A storm or evening cooldown can provide useful temperature drop while still carrying high moisture.
- Window opening can lower upper-zone temperature while making the working layer more humid.
- After-hours humidity increase may be an acceptable trade if the space is unoccupied and the goal is to dump stored upper heat.
- Forced purge should stop once the ceiling layer is mostly destratified; otherwise the system may continue importing wet air after the useful heat-removal benefit is gone.

### Current control consequence

- Evening start was moved to 18:00, but with stronger thermal and humidity guardrails.
- Normal purge requires a 10°F ceiling/floor and outdoor/ceiling thermal opportunity.
- Extreme purge allows a larger humidity penalty only when the ceiling heat delta is larger.
- The cycle now treats AC/heat on, bay door open, and recent side-door movement as occupancy/manual-use lockouts.
