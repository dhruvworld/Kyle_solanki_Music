# Model Classification Workflow (Smart Ensemble)

## Overview
End-to-end flow for Pop vs Non-pop classification using all non-leaky features, SMOTE balancing, and a stacking ensemble (XGBoost, LightGBM, GradientBoosting, CatBoost optional, neural net with XGBoost meta-learner).

---

## Pipeline
1) **Ingest & clean data**
   - Load `spotify_final_with_behavior.csv`
   - Drop/replace NaN/Inf, add `is_explicit_binary`
2) **Remove leaky features**
   - Exclude: `has_pop_genre`, `popular_recent`, `mainstream_pop_signal`, `tempo_is_pop_range`, `genre_count`
3) **Build feature sets**
   - Base: popularity, year, tempo, explicit
   - Light: base + audio (danceability, energy, valence, acousticness)
   - Full: all non-leaky numeric + safe genre TF-IDF (pop terms removed), top-25 selected via ANOVA
4) **Balance classes**
   - SMOTE to 50/50 for boosters and neural net training
5) **Train base models**
   - XGBoost, LightGBM, GradientBoosting, CatBoost (if installed), balanced FFN
6) **Stacking meta-learner**
   - XGBoost over base-model probabilities (fallback: logistic regression)
7) **Evaluate**
   - ROC AUC, confusion matrices, precision/recall/F1
   - Plot ROC curves and per-model confusion matrices

---

## Feature Summary (used in ensemble)
- Core: `spotify_popularity`, `album_release_year`, `tempo_bpm_synth`, `is_explicit_binary`, `position`
- Audio: `danceability`, `energy`, `valence`, `acousticness`
- Derived: `is_highly_popular`, `is_moderately_popular`, `popularity_normalized`, `is_recent`, `is_very_recent`, `decade`, `tempo_normalized`, `is_daytime`, `is_not_explicit`
- Safe genre TF-IDF (pop terms removed, max_features=15)

---

## Models
- Base FFN (4 features)
- Light FFN (base + audio)
- Higher FFN (all non-leaky + safe genre TF-IDF)
- Smart Ensemble (best): XGBoost + LightGBM + GradientBoosting + CatBoost (optional) + balanced FFN → XGBoost meta-learner

---

## Performance (test ROC AUC)
- Base: 0.673
- Light: 0.681
- Higher: 0.739
- **Smart Ensemble (SMOTE Model):** 0.774 (best)

---

## Decision Threshold
- Default 0.5; adjust (e.g., 0.4–0.6) to trade precision vs recall for Pop.

---

## Limitations
- Binary only (Pop vs Non-pop)
- Performance capped by current feature richness; adding more audio fields (speechiness, instrumentalness, loudness, liveness) could help
- Ensemble adds training complexity/compute

---

**Last Updated:** December 2025

