# Model Classification Workflow: How Pop vs Non-Pop Classification Works

## Overview

This document explains how our Feedforward Neural Network (FFN) models classify music tracks as "Pop" or "Non-pop" based on Spotify metadata and audio features.

---

## Classification Process

### Step 1: Feature Input (45 Features)

The model receives **45 features** for each track:

#### **Metadata Features (8)**
- `spotify_popularity` - Track popularity score (0-100)
- `album_release_year` - Year of album release
- `tempo_bpm_synth` - Tempo in beats per minute
- `position` - Track position in playlist/album
- `danceability` - How suitable for dancing (0-1)
- `energy` - Perceptual intensity (0-1)
- `valence` - Musical positiveness/happiness (0-1)
- `acousticness` - Confidence track is acoustic (0-1)

#### **Derived Features (8)**
- `is_highly_popular` - Popularity > 70 (binary)
- `is_moderately_popular` - Popularity 50-70 (binary)
- `popularity_normalized` - Normalized popularity (0-1)
- `is_recent` - Released 2020+ (binary)
- `is_very_recent` - Released 2022+ (binary)
- `tempo_normalized` - Normalized tempo
- `is_daytime` - Played during day/afternoon (binary)
- `is_not_explicit` - Non-explicit content flag (binary)

#### **Interaction Features (2)**
- `popularity_x_year` - Popularity × Release Year
- `tempo_x_year` - Tempo × Release Year

#### **Temporal Features (2)**
- `release_month` - Month of release (1-12)
- `release_decade` - Decade of release (e.g., 2020, 2010)

#### **Categorical Features (4)**
- `time_of_day_synth` - One-hot encoded (morning, afternoon, evening, night)

#### **Safe Genre Features (20)**
- TF-IDF features from genre text with "pop" keywords removed
- Examples: "rock", "country", "hip hop", "jazz", "latin", "electronic", etc.
- These capture genre patterns without data leakage

#### **Additional Features (1)**
- `is_explicit_binary` - Explicit content flag (0/1)

---

### Step 2: Neural Network Processing

The model processes these features through multiple layers:

#### **Model Architecture (Model 2 - Best Performing)**

```
Input Layer (45 features)
    ↓
Dense(128) + ReLU + L2 Regularization
    ↓
BatchNormalization (stabilizes training)
    ↓
Dropout(0.4) (prevents overfitting)
    ↓
Dense(64) + ReLU + L2 Regularization
    ↓
BatchNormalization
    ↓
Dropout(0.3)
    ↓
Dense(32) + ReLU
    ↓
Dropout(0.2)
    ↓
Output Layer: Dense(1) + Sigmoid
    ↓
Output: Probability (0.0 to 1.0)
```

#### **What Happens in Each Layer:**

1. **Dense Layers**: Combine features through weighted sums and non-linear transformations
   - Each neuron learns to detect patterns in the input features
   - ReLU activation introduces non-linearity (allows complex decision boundaries)

2. **BatchNormalization**: Normalizes activations to stabilize training
   - Helps the model learn faster and more reliably

3. **Dropout**: Randomly sets some neurons to zero during training
   - Prevents the model from memorizing training data
   - Forces the model to learn robust patterns

4. **L2 Regularization**: Penalizes large weights
   - Prevents the model from overfitting to training data

5. **Sigmoid Output**: Converts the final value to a probability (0.0 to 1.0)
   - 0.0 = Very unlikely to be Pop
   - 1.0 = Very likely to be Pop
   - 0.5 = Uncertain/balanced

---

### Step 3: Decision Threshold

The model outputs a **probability** between 0.0 and 1.0. The final classification uses a threshold:

```
IF probability >= 0.5:
    → Classify as "Pop"
ELSE:
    → Classify as "Non-pop"
```

**Note:** The threshold of 0.5 is the default, but it can be optimized based on the trade-off between precision and recall.

---

## What Features Drive the Classification?

### Most Important Features (Typical Patterns)

Based on the model's learned patterns, these features are typically most influential:

#### **High Positive Correlation (More likely Pop):**
1. **High Popularity** - Pop tracks tend to be more popular
2. **High Danceability** - Pop music is designed to be danceable
3. **High Energy** - Pop tracks are typically upbeat and energetic
4. **High Valence** - Pop music is generally positive/happy
5. **Recent Release** - Modern pop trends
6. **Low Acousticness** - Pop is usually electronic/produced, not acoustic
7. **Genre patterns** - Certain genre TF-IDF features (without "pop" keyword)

#### **High Negative Correlation (More likely Non-pop):**
1. **Low Popularity** - Less mainstream tracks
2. **High Acousticness** - Acoustic/folk genres
3. **Older Release Year** - Classic/older music
4. **Genre patterns** - Rock, country, jazz, classical genres

---

## Example Classification

### Example 1: High Confidence Pop
```
Features:
  - popularity: 85
  - danceability: 0.85
  - energy: 0.90
  - valence: 0.80
  - acousticness: 0.10
  - release_year: 2023
  - genre_features: [electronic patterns, dance patterns]

Model Processing:
  → Dense layers combine these features
  → Output probability: 0.92

Decision:
  → 0.92 >= 0.5 → Classified as "Pop" ✓
  → High confidence (92%)
```

### Example 2: High Confidence Non-Pop
```
Features:
  - popularity: 25
  - danceability: 0.30
  - energy: 0.40
  - valence: 0.35
  - acousticness: 0.85
  - release_year: 1975
  - genre_features: [classical patterns, folk patterns]

Model Processing:
  → Dense layers combine these features
  → Output probability: 0.08

Decision:
  → 0.08 < 0.5 → Classified as "Non-pop" ✓
  → High confidence (92% non-pop)
```

### Example 3: Uncertain Case
```
Features:
  - popularity: 55
  - danceability: 0.60
  - energy: 0.65
  - valence: 0.55
  - acousticness: 0.50
  - release_year: 2015
  - genre_features: [mixed patterns]

Model Processing:
  → Dense layers combine these features
  → Output probability: 0.48

Decision:
  → 0.48 < 0.5 → Classified as "Non-pop"
  → Low confidence (close to threshold)
```

---

## Model Performance

### Best Model: Model 2 (Medium FFN)

**Test Set Performance:**
- **Accuracy:** 87.2%
- **Precision (Pop):** 57.3% - When model says "Pop", it's correct 57% of the time
- **Recall (Pop):** 79.8% - Model catches 80% of all Pop tracks
- **F1-Score:** 66.7% - Balanced measure of precision and recall
- **ROC AUC:** 94.2% - Excellent discrimination ability

### What This Means:

1. **High Accuracy (87%)**: Model correctly classifies 87 out of 100 tracks
2. **Good Recall (80%)**: Catches most Pop tracks (doesn't miss many)
3. **Moderate Precision (57%)**: Some false positives (classifies non-pop as pop)
4. **Excellent ROC AUC (94%)**: Very good at distinguishing Pop from Non-pop

---

## Decision Threshold Optimization

The default threshold is **0.5**, but this can be adjusted:

### Lower Threshold (e.g., 0.3)
- **More Pop predictions** (higher recall)
- **More false positives** (lower precision)
- Use when: You want to catch more Pop tracks, even if some are wrong

### Higher Threshold (e.g., 0.7)
- **Fewer Pop predictions** (lower recall)
- **Fewer false positives** (higher precision)
- Use when: You want to be very sure when predicting Pop

### Optimal Threshold
- Typically around **0.4-0.6** for balanced precision/recall
- Can be found using precision-recall curve analysis

---

## Key Insights

### Why the Model Works:

1. **Multiple Feature Types**: Uses metadata, audio features, and genre patterns
2. **Non-linear Combinations**: Neural network learns complex feature interactions
3. **Regularization**: Prevents overfitting, ensures generalization
4. **Class Balancing**: Uses class weights to handle imbalanced data (16% Pop, 84% Non-pop)

### What Makes a Track "Pop"?

Based on learned patterns, Pop tracks typically have:
- ✅ High popularity (>60)
- ✅ High danceability (>0.6)
- ✅ High energy (>0.6)
- ✅ High valence (>0.5) - positive/happy
- ✅ Low acousticness (<0.3) - electronic/produced
- ✅ Recent release (2020+)
- ✅ Genre patterns matching mainstream pop

### What Makes a Track "Non-Pop"?

Non-pop tracks typically have:
- ❌ Lower popularity
- ❌ Lower danceability
- ❌ Lower energy or valence
- ❌ Higher acousticness (folk, acoustic genres)
- ❌ Older release years
- ❌ Genre patterns like rock, country, jazz, classical

---

## Limitations

1. **Binary Classification**: Only predicts Pop or Non-pop (no sub-genres)
2. **Threshold Dependent**: Performance varies with threshold choice
3. **Feature Dependent**: Requires all 45 features to be available
4. **Training Data**: Performance limited by quality and size of training data
5. **No Explainability**: Neural networks are "black boxes" - hard to explain individual decisions

---

## Future Improvements

1. **Feature Importance Analysis**: Use SHAP values or permutation importance
2. **Threshold Optimization**: Find optimal threshold for specific use case
3. **Ensemble Methods**: Combine predictions from all 3 models
4. **Explainable AI**: Add attention mechanisms or feature attribution
5. **Multi-class Classification**: Extend to classify specific genres, not just Pop vs Non-pop

---

**Last Updated:** December 2024

