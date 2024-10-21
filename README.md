# PRC Data Challenge

Contribution of Malte Cordts, Sabrina Kerz, and Dennis Schorn to the [PRC Data Challenge 2024](https://ansperformance.eu/study/data-challenge/).

## Next Meeting
Monday, October 10 19:00 lcl (17:00 UTC)

## Current rankings

Available [here](https://datacomp.opensky-network.org/api/rankings)

<!--result-start-->
| Rank | Team Name | RMSE | File Version |
| ---- | --------- | ---- | ------------ |
| 1 | team_likable_jelly | 1735.32 | v8 |
| 2 | team_brave_pillow | 2257.19 | v42 |
| 3 | team_motivated_quicksand | 2391.47 | v7 |
| 4 | team_tiny_rainbow | 2396.82 | v72 |
| 5 | team_youthful_xerox | 2408.33 | v29 |
| 6 | team_honest_turtle | 2593.61 | v10 |
| 7 | team_gentle_wreath | 2706.15 | v19 |
| 8 | team_amazing_forest | 2730.61 | v17 |
| 9 | team_mindful_donkey | 2768.36 | v8 |
| 10 | team_diligent_igloo | 2790.44 | v11 |
| 11 | team_affectionate_bridge | 2857.86 | v3 |
| 12 | team_diligent_volcano | 2879.83 | v10 |
| 13 | team_patient_net | 2928.35 | v1 |
| 14 | team_honest_cactus | 2986.09 | v1 |
| 15 | team_faithful_engine | 3152.34 | v0 |
| 16 | team_elegant_lemon | 3209.46 | v11 |
| 17 | team_inventive_emu | 3326.31 | v5 |
| 18 | team_mellow_barn | 3387.23 | v2 |
| 19 | team_faithful_napkin | 3438.97 | v2 |
| 20 | **team_organized_volcano** | 3502.38 | v5 |
| 21 | team_nice_wolf | 3532.55 | v0 |
| 22 | team_bubbly_island | 3649.9 | v1 |
| 23 | team_quick_candle | 3875.77 | v10 |
| 24 | team_loyal_hippo | 3904.92 | v3 |
| 25 | team_amiable_garden | 3944.4 | v3 |
| 26 | team_modest_scooter | 3968.61 | v1 |
| 27 | team_bold_emu | 4010.81 | v2 |
| 28 | team_genuine_emu | 4042.14 | v4 |
| 29 | team_respectful_kangaroo | 4052.19 | v5 |
| 30 | team_strong_fossil | 4067.41 | v1 |
| 31 | team_zesty_ostrich | 4168.98 | v2 |
| 32 | team_zippy_river | 4228.78 | v6 |
| 33 | team_outspoken_engine | 4395.36 | v0 |
| 34 | team_refreshing_unicorn | 4680.25 | v0 |
| 35 | team_knowledgeable_jungle | 5429.2 | v5 |
| 36 | team_exuberant_scooter | 5438.55 | v0 |
| 37 | team_gentle_dragon | 5990.08 | v1 |
| 38 | team_jolly_koala | 8107.64 | v1 |
| 39 | team_versatile_yacht | 10077.68 | v08 |
| 40 | team_sincere_quicksand | 10740.28 | v0 |
| 41 | team_zippy_horse | 12583.67 | v1 |
| 42 | team_energetic_quiver | 16265.46 | v3 |
| 43 | team_unbelievable_donkey | 19825.11 | v4 |
| 44 | team_affectionate_whistle | 33779.26 | v0 |
| 45 | team_nice_hippo | 49433.98 | v1 |
<!--result-end-->

## KPIs 
### 1. Model (Flight List Based Model, Gradient Boost)
RMSE Train: 3360.5953623984747 kg 

RMSE Test:3695.7355259853975 kg 

## Notebooks
[Initial Data Review](https://colab.research.google.com/drive/1WMxJp5L7vl9GBKhZzXFJeXjvI1MgSNON#scrollTo=p6q00gZ2aoNO) 

[Flight List Based Model](https://colab.research.google.com/drive/1h_4Kw_Kx4-c8agqgn95yTxK5HRhB2JIF)

[Script for training and predicting the model](https://colab.research.google.com/drive/1mKO-b7YfdCXVuNLkEvr6OccVzr4FLsp0?usp=sharing)

## Documentation

[Flight List Based Model](https://docs.google.com/document/d/1--aCGaPIoykFuH6jPuZkSNKuL8PHXe96vltabt59e6Y/edit)

## Information
[Data Explanation](https://drive.google.com/file/d/1qJPLEoQPBFM8mL6tLpiV-vdHZd88V_wM/view?usp=drive_link) 

[Introduction Slides](https://drive.google.com/file/d/1aDVe83t2N_of7b_DXSE8yEuQ1MaV0RpH/view?usp=drive_link) 

Command to set up an alias for the data location:

mc alias set dc24 https://s3.opensky-network.org/ ZG58zJvKhts2bkOX eU95azmBpK82kg96mE0TNzsWov3OvP2d

## Goal
**We aim to hand in a solution before the final deadline!**

## Decisions & Plans
- We want to start with a simple model, using only the flight list
- Then iterate & improve it by adding handcrafted features
- Next include data from the actual trajectories, without temporal features
- Then move to more complex models if necessary, eventually ending up with a transformer
- Optimise for RMSE, since this is used in the final scoring of our submission
- 

# Model Features Overview
## FightList
This table lists all the features in the flightlist and indicates whether each feature is used in the models.

### Raw Features
| Feature          | 1. HGBR Model |
| ---------------------------------------- | ------- |
| flight_id (unique ID)                    | ❌      |
| callsign (obfuscated callsign)           | ❌      |
| adep (Aerodrome of DEParture)            | ❌      |
| ades (Aerodrome of DEStination)          | ❌      |
| name_adep (ADEP airport name)            | ❌      |
| name_ades (ADES airport name)            | ❌      |
| country_code_adep (ADEP country code)    | ✅      |
| country_code_ades (ADES country code)    | ✅      |
| date (date of flight)                    | ❌      |
| actual_offblock_time (AOBT)              | ❌      |
| arrival_time (ARVT)                      | ❌      |
| aircraft_type (aircraft type code)       | ✅      |
| wtc (Wake Turbulence Category)           | ✅      |
| airline (Aircraft Operator code)         | ✅      |
| flight_duration (flight duration in mins)| ✅      |
| taxiout_time (taxi-out time in mins)     | ✅      |
| flown_distance (route length in nmi)     | ✅      |

### Engineered Features
| Feature                                  | 1. HGBR Model |
| ---------------------------------------- | ------- |
|weekday                                 | ✅      |
| year sin                                | ✅      |
| arrival day sin                         | ✅      |
| start_hour                              | ✅      |

## Trajectories

### Engineered Features
| Feature                                  | 1. HGBR Model |
| ---------------------------------------- | ------- |
|Average climb rate, 1st flight phase   | ✅      |
|Average climb rate, 3rd flight phase    | ✅     |
|Average altitude, 2nd flight phase    | ✅     |


## Expected trajectories in final submission

Old: We have 474972 and missed 52191 flights

New: We have 464592 and missed 69525 flights
