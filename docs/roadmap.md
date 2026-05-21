# Roadmap

## Phase 0: Scaffold

- Document the project framing.
- Capture hardware baseline.
- Add starter Home Assistant package.
- Add safety boundary.

## Phase 1: Bench validation

- Measure damper open and close timing.
- Measure damper current and holding behavior.
- Confirm blower steady-state profile with current controller.
- Confirm Shelly restore behavior and local control behavior.

## Phase 2: Physical installation

- Install damper and control enclosure.
- Validate branch circuit and controls before automation is enabled.
- Capture photos and as-built notes.
- Add actual entity IDs and dashboard screenshots.

## Phase 3: Automation hardening

- Replace placeholder YAML with validated Home Assistant package.
- Add minimum runtime and cooldown enforcement based on real behavior.
- Add fault detection from expected power draw.
- Add manual override and lockout status.

## Phase 4: Results

- Record before/after thermal profiles.
- Compare occupied-zone and upper-zone response during purge.
- Document what changed after installation.
- Publish a concise article for ninja-neer.net.
