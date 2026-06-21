# Sample Seed Data — Offline Mini Arcade

## App Profile

```json
{
  "name": "Offline Mini Arcade",
  "package_name": "com.example.offlineminiarcade",
  "play_store_url": "https://play.google.com/store/apps/details?id=com.example.offlineminiarcade",
  "category": "Arcade",
  "app_type": "Game",
  "primary_positioning": "Lightweight offline-first mini arcade with Pulse Orbit, Lane Drift, and Stack Drop. Built for quick sessions and low-end Android devices.",
  "target_countries": "Pakistan, India, Philippines, Indonesia, United States, United Kingdom",
  "monetization_model": "Free / non-aggressive monetization",
  "current_version": "1.0.0"
}
```

## Sample Daily Metrics

```csv
date,installs,uninstalls,store_visitors,listing_conversion_rate,active_users,day_1_retention,day_7_retention,average_session_length,game_starts,retry_count,daily_challenge_opens,daily_challenge_completions,premium_clicks,premium_purchases,notes
2026-06-01,4,1,80,5.0,12,20.0,8.0,130,32,18,2,1,0,0,Launch week baseline
2026-06-02,6,1,95,6.3,16,22.0,8.5,145,44,21,3,1,0,0,Slight improvement
2026-06-03,5,2,100,5.0,15,18.0,7.0,125,39,19,3,1,0,0,Conversion still low
```

## Sample Reviews

```csv
date,rating,reviewer_name,review_text,device,app_version,language
2026-06-02,5,User A,"Nice small games and works offline.",TECNO CH6i,1.0.0,en
2026-06-03,3,User B,"Stack game controls feel a little cramped on my phone.",Samsung A10,1.0.0,en
2026-06-04,4,User C,"Good for short breaks. Please add more levels.",Redmi 9A,1.0.0,en
```

## First Expected Diagnosis

If visitors are present but conversion remains low, the system should suggest a store conversion problem rather than an ads push.

## First Expected Recommendations

1. Improve screenshot captions to explain the three games faster.
2. Add clearer offline-first wording in the short description.
3. Avoid increasing ads budget until listing conversion improves.
4. Track conversion for 7–14 days after manual listing update.
