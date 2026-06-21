# CSV Templates

## daily_metrics.csv

```csv
app_package,date,installs,uninstalls,store_visitors,listing_conversion_rate,active_users,day_1_retention,day_7_retention,average_session_length,game_starts,retry_count,daily_challenge_opens,daily_challenge_completions,premium_clicks,premium_purchases,notes
com.example.offlineminiarcade,2026-06-01,4,1,80,5.0,12,20.0,8.0,130,32,18,2,1,0,0,Launch week baseline
```

## reviews.csv

```csv
app_package,date,rating,reviewer_name,review_text,device,app_version,language
com.example.offlineminiarcade,2026-06-02,5,User A,"Nice small games and works offline.",TECNO CH6i,1.0.0,en
```

## android_vitals.csv

```csv
app_package,date,crash_rate,anr_rate,slow_rendering_rate,excessive_wakeups,affected_devices_json,notes
com.example.offlineminiarcade,2026-06-01,0.4,0.1,2.2,0,"[]",No major issue
```

## ads.csv

```csv
app_package,date,campaign_name,country_code,spend,impressions,clicks,installs,cpi,conversions,retention_d1,retention_d7,notes
com.example.offlineminiarcade,2026-06-01,Launch Test,PK,2.5,1200,80,5,0.5,0,20.0,8.0,Small test only
```
