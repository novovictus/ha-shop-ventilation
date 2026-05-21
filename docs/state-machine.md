# State machine

This project is best modeled as a small state machine instead of a single automation trigger.

```text
IDLE
  -> PURGE_AVAILABLE
  -> DAMPER_OPENING
  -> BLOWER_RUNNING
  -> BLOWER_STOPPING
  -> DAMPER_CLOSING
  -> COOLDOWN
  -> IDLE
```

## IDLE

Default state. Damper and blower are off. The damper should be closed by spring return.

Transitions to `PURGE_AVAILABLE` when environmental conditions justify purge and manual disable is off.

## PURGE_AVAILABLE

A computed state indicating that outside air is useful and the shop has removable heat.

This may be represented as a template binary sensor in Home Assistant.

## DAMPER_OPENING

Damper is energized. Blower remains off while the shutter opens.

Exit after measured damper open time plus margin.

## BLOWER_RUNNING

Blower is energized. Damper remains energized open.

Exit when one of these occurs:

- Minimum runtime has elapsed and purge is no longer useful.
- Maximum runtime has elapsed.
- Manual disable is turned on.
- Fault condition occurs.

## BLOWER_STOPPING

Blower is turned off. Damper remains open briefly so airflow can settle.

## DAMPER_CLOSING

Damper is de-energized and allowed to spring closed.

## COOLDOWN

System remains off for a minimum period to prevent rapid cycling.

## FAULT or LOCKOUT

Optional future state. Entered when commanded state and observed power draw disagree, or when a safety interlock is triggered.
