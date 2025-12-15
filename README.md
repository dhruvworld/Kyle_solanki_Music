# Pop vs Non-Pop Genre Classification

**Authors:** Kyle Furey & Dhruv Solanki

## Project Overview

This project classifies tracks as **Pop** or **Non-pop** using Spotify metadata, audio features, safe genre signals, and a **stacking ensemble** (XGBoost, LightGBM, GradientBoosting, CatBoost, and a balanced neural net). The ensemble outperforms any single model.

## Dataset

- **Total Samples:** 40,000 tracks
- **Train/Val/Test Split:** 85% / 10% / 5% (34,000 / 4,000 / 2,000)
- **Class Distribution:** ~16% Pop, ~84% Non-pop (imbalanced dataset)

## Feature Engineering (non-leaky)

- **Numeric & audio:** popularity, year, tempo, explicit flag, position, danceability, energy, valence, acousticness, time_of_day dummies.
- **Derived:** is_highly_popular, is_moderately_popular, popularity_normalized, is_recent, is_very_recent, decade, tempo_normalized, is_daytime, is_not_explicit.
- **Safe genre TF-IDF:** up to 15 tokens with “pop” keywords removed to avoid leakage.
- **Excluded (leaky):** has_pop_genre, popular_recent, mainstream_pop_signal, tempo_is_pop_range, genre_count.

## Models

- **Model 1: Base FFN** — minimal (4 core features: popularity, year, tempo, explicit).  
- **Model 2: Light FFN** — base + audio (danceability, energy, valence, acousticness).  
- **Model 3: Higher FFN** — all non-leaky numeric + safe genre TF-IDF.  
- **Smart Ensemble (best):** stacking of XGBoost, LightGBM, GradientBoosting, CatBoost (optional), and a balanced neural net, with XGBoost as meta-learner.

## Training Configuration (current)

- **Feature selection:** top-25 non-leaky features via ANOVA F-score.  
- **Balancing:** SMOTE to 50/50 for boosters and NN.  
- **Boosters:** tuned XGBoost / LightGBM / GradientBoosting; CatBoost optional.  
- **Neural net:** trained on SMOTE-balanced data with BN + Dropout.  
- **Meta-learner:** XGBoost stacking over base model probabilities (fallback: logistic regression).  
- **Primary metric:** ROC AUC; we also track accuracy, precision, recall, F1.

## Data Preprocessing

1. **Data Quality Check:**
   - Removes NaN and Inf values
   - Uses RobustScaler for feature scaling
   - Handles missing values

2. **Feature Scaling:**
   - StandardScaler for numeric features
   - One-hot encoding for categorical features
   - TF-IDF vectorization for genre text

3. **Train/Val/Test Split:**
   - Stratified split to maintain class distribution
   - 85% train, 10% validation, 5% test

## Test Set Performance (latest)

| Model | ROC AUC |
| --- | --- |
| Model 1: Base | 0.673 |
| Model 2: Light | 0.681 |
| Model 3: Higher | 0.739 |
| **Smart Ensemble (SMOTE Model)** | **0.774** |

**🏆 Best Model:** Smart Ensemble (SMOTE Model) — stacking with XGBoost meta-learner.

## Key Design Decisions

### Why 3 Models?
- **Model 1:** Simple baseline to establish minimum performance
- **Model 2:** Optimal balance of complexity and performance
- **Model 3:** Explores deeper architectures (currently being optimized)

### Why These Features?
- **Metadata features:** Readily available, no API calls needed
- **Audio features:** Direct musical characteristics
- **Safe genre features:** Genre information without data leakage
- **Derived features:** Capture domain knowledge (popularity thresholds, temporal patterns)

### Regularization Strategy
- **Model 1:** Minimal (only dropout)
- **Model 2:** Moderate (L2 + BatchNorm + Dropout)
- **Model 3:** Balanced (reduced from original to prevent underfitting)

## Running the Notebook

1. **Prerequisites:**
   ```bash
   pip install tensorflow pandas numpy scikit-learn matplotlib
   ```

2. **Data Path:**
   - Ensure `../data/spotify_final_with_behavior.csv` exists
   - Should contain 40,000 rows with required columns

3. **Execution:**
   - Run cells sequentially
   - Models will train automatically
   - Results and plots will be generated

4. **Output:**
   - Training curves for all 3 models
   - Confusion matrices
   - ROC curves comparison
   - Classification reports
   - Best model checkpoints saved

## File Structure

```
Kyle_solanki_Music/
├── Furey_Solanki_PopMusicFFNN.ipynb.ipynb  # Main notebook
├── README.md                                 # This file
├── data/
│   └── spotify_final_with_behavior.csv      # Dataset
└── best_model*.h5                            # Saved model checkpoints
```

## Architecture Understanding (current best)

- Inputs: all non-leaky numeric + safe genre TF-IDF; top-25 selected.  
- Base models: XGBoost, LightGBM, GradientBoosting, CatBoost (optional), balanced FFN.  
- Meta-learner: XGBoost over base-model probabilities (fallback: logistic regression).  
- Balancing: SMOTE for boosters and NN.  
- Threshold: default 0.5; adjust per precision/recall needs.

## Future Improvements

1. Tune top-k features and booster hyperparameters.  
2. Add SHAP for explainability.  
3. Further threshold optimization per business need.  
4. Calibrated stacking (Platt/Isotonic) if required.  
5. Multi-class: extend beyond Pop/Non-pop.

## Contact

For questions about the architecture or implementation, refer to the notebook comments or contact the authors.

---

**Last Updated:** December 2025  
**Notebook Version:** Smart Ensemble with stacking + SMOTE + safe genre TF-IDF

