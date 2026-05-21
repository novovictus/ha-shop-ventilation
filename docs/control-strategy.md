# Control strategy

The controller should answer four questions before running:

1. Is the shop hotter than desired?
2. Is the upper zone holding trapped heat?
3. Is outdoor air useful for removing that heat?
4. Has the system respected minimum runtime and cooldown limits?

## Start sequence

```text
1. Confirm purge conditions.
2. Energize damper.
3. Wait 15 to 30 seconds, or measured damper open time plus margin.
4. Start blower.
5. Hold minimum runtime.
6. Continue while purge remains useful and maximum runtime has not been reached.
```

## Stop sequence

```text
1. Stop blower.
2. Wait 15 to 30 seconds for airflow to settle.
3. De-energize damper.
4. Allow spring return to close shutter.
5. Enter cooldown.
```

## Candidate purge conditions

Initial condition set:

```text
outdoor_temp + margin < occupied_zone_temp
upper_zone_temp > occupied_zone_temp + stratification_margin
occupied_zone_temp > comfort_threshold OR upper_zone_temp > upper_heat_threshold
system not in cooldown
manual disable is off
```

Future condition set:

```text
outdoor_dew_point acceptable
rain or storm condition acceptable
bay door/window state compatible
blower and damper power draw within expected range
```

## Runtime protection

Recommended helpers:

- Minimum blower runtime.
- Minimum off time.
- Maximum purge runtime.
- Manual disable.
- Manual force purge.
- Fault lockout.

Short cycling should be avoided even when temperature conditions bounce around thresholds.
