# Bench testing

Bench testing should happen before cutting the wall or permanently mounting controls.

## Damper tests

Record:

- Model and nameplate photo.
- Voltage and lead selection for 120V use.
- Open time.
- Close time after power removal.
- Running watts and current while opening.
- Holding watts and current after fully open, if the motor remains energized.
- Motor temperature after 30 to 60 minutes held open.
- Any chatter, binding, stall, or incomplete close behavior.

## Blower tests

Record:

- Nameplate photo if accessible.
- Startup behavior.
- Running watts and current after 10 seconds.
- Running watts and current after 5 minutes.
- Longest continuous run.
- Plug, cord, receptacle, and controller temperature during operation.

## Controller tests

Record:

- Shelly relay behavior.
- Power restore behavior.
- Home Assistant entity names.
- Manual override behavior.
- Network outage behavior if practical.

## Acceptance criteria

- Damper opens and closes reliably.
- Damper closes when power is removed.
- Blower does not start until damper open delay has elapsed.
- Blower stops before the damper closes.
- No unexpected heat, chatter, reset, or nuisance trip occurs during a representative runtime.
