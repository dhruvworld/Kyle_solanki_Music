# Pop vs Non-Pop Genre Classification

**Authors:** Kyle Furey & Dhruv Solanki

## Project Overview

This project implements Feedforward Neural Networks (FFN) to classify music tracks as "Pop" or "Non-pop" based on Spotify metadata and audio features. The models use a dataset of 40,000 tracks with various features including popularity, release year, tempo, audio characteristics, and genre information.

## Dataset

- **Total Samples:** 40,000 tracks
- **Train/Val/Test Split:** 85% / 10% / 5% (34,000 / 4,000 / 2,000)
- **Class Distribution:** ~16% Pop, ~84% Non-pop (imbalanced dataset)

## Feature Engineering

### Features Used (45 total)

#### 1. Base Numeric Features (8)
- `spotify_popularity` - Track popularity score (0-100)
- `album_release_year` - Year of album release
- `tempo_bpm_synth` - Tempo in beats per minute
- `position` - Track position in playlist/album
- `danceability` - How suitable for dancing (0-1)
- `energy` - Perceptual intensity (0-1)
- `valence` - Musical positiveness (0-1)
- `acousticness` - Confidence track is acoustic (0-1)

#### 2. Derived Features (8)
- `is_highly_popular` - Popularity > 70
- `is_moderately_popular` - Popularity 50-70
- `popularity_normalized` - Normalized popularity
- `is_recent` - Released 2020+
- `is_very_recent` - Released 2022+
- `tempo_normalized` - Normalized tempo
- `is_daytime` - Played during day/afternoon
- `is_not_explicit` - Non-explicit content flag

#### 3. Interaction Features (2)
- `popularity_x_year` - Popularity × Release Year
- `tempo_x_year` - Tempo × Release Year

#### 4. Temporal Features (2)
- `release_month` - Month of release
- `release_decade` - Decade of release

#### 5. Categorical Features (4)
- `time_of_day_synth` - One-hot encoded (morning, afternoon, evening, night)

#### 6. Safe Genre Features (20)
- TF-IDF features from genre text with "pop" keywords removed
- Prevents data leakage while capturing genre patterns
- Examples: "rock", "country", "hip hop", "jazz", "latin", etc.

### Data Leakage Prevention

**Removed Features (to prevent leakage):**
- ❌ `tempo_is_pop_range` - Directly targets pop BPM range
- ❌ `mainstream_pop_signal` - Engineered to predict pop
- ❌ `popular_recent` - Composite feature targeting pop
- ❌ `has_pop_genre` - Directly from genre column
- ❌ Genre TF-IDF with "pop" keywords - Would leak target information

**Safe Genre Features:**
- ✅ Genre TF-IDF with "pop" keywords removed
- ✅ Captures genre patterns without direct leakage

## Model Architectures

### Model 1: Shallow FFN
**Architecture:**
```
Input (45 features)
  ↓
Dense(64) + ReLU
  ↓
Dropout(0.3)
  ↓
Dense(32) + ReLU
  ↓
Dropout(0.2)
  ↓
Output (1) + Sigmoid
```

**Characteristics:**
- Simple 2-layer architecture
- Fast training
- Good baseline performance
- Total parameters: ~3,000

### Model 2: Medium FFN ⭐ (Best Performing)
**Architecture:**
```
Input (45 features)
  ↓
Dense(128) + ReLU + L2(1e-4)
  ↓
BatchNormalization
  ↓
Dropout(0.4)
  ↓
Dense(64) + ReLU + L2(1e-4)
  ↓
BatchNormalization
  ↓
Dropout(0.3)
  ↓
Dense(32) + ReLU
  ↓
Dropout(0.2)
  ↓
Output (1) + Sigmoid
```

**Characteristics:**
- 3 hidden layers with BatchNorm
- L2 regularization on first 2 layers
- Best F1-Score: 0.6667
- Best ROC AUC: 0.9417
- Total parameters: ~15,000

### Model 3: Deep FFN (Optimized)
**Architecture:**
```
Input (45 features)
  ↓
Dense(128) + ReLU + L2(5e-5)
  ↓
BatchNormalization
  ↓
Dropout(0.3)
  ↓
Dense(96) + ReLU + L2(5e-5)
  ↓
BatchNormalization
  ↓
Dropout(0.25)
  ↓
Dense(64) + ReLU + L2(5e-5)
  ↓
BatchNormalization
  ↓
Dropout(0.2)
  ↓
Dense(32) + ReLU
  ↓
Dropout(0.15)
  ↓
Output (1) + Sigmoid
```

**Characteristics:**
- 4 hidden layers with BatchNorm
- Reduced regularization (optimized to prevent underfitting)
- Progressive dropout rates (0.3 → 0.25 → 0.2 → 0.15)
- Lighter L2 regularization (5e-5)
- Total parameters: ~25,000

## Training Configuration

### Common Settings
- **Optimizer:** Adam (lr=0.001, beta_1=0.9, beta_2=0.999)
- **Loss:** Binary Cross-Entropy
- **Metrics:** Accuracy, Precision, Recall
- **Batch Size:** 256
- **Max Epochs:** 150
- **Class Weights:** Balanced (handles imbalanced dataset)

### Callbacks
- **Early Stopping:** 
  - Patience: 20 epochs (Model 1 & 2), 25 epochs (Model 3)
  - Monitor: `val_loss`
  - Restores best weights
- **Learning Rate Reduction:**
  - Factor: 0.5
  - Patience: 8 epochs (Model 1 & 2), 10 epochs (Model 3)
  - Min LR: 1e-7
- **Model Checkpoint:** Saves best model based on `val_loss`

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

## Model Performance

### Test Set Results

| Model | Accuracy | Precision | Recall | F1-Score | ROC AUC |
|-------|----------|-----------|--------|----------|---------|
| Model 1: Shallow FFN | 0.753 | 0.372 | 0.779 | 0.504 | 0.866 |
| **Model 2: Medium FFN** | **0.872** | **0.573** | **0.798** | **0.667** | **0.942** |
| Model 3: Deep FFN | 0.850 | 0.553 | 0.355 | 0.433 | 0.801 |

**🏆 Best Model: Model 2 (Medium FFN)**
- Best overall performance
- Good balance between precision and recall
- Highest ROC AUC score

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

## Notes for Partners

### Architecture Understanding

1. **Input Layer:** 45 features (all preprocessed and scaled)
2. **Hidden Layers:** 
   - ReLU activation for non-linearity
   - BatchNormalization for stable training
   - Dropout for regularization
3. **Output Layer:** Single neuron with sigmoid (binary classification)

### Why Model 2 Performs Best

- **Optimal Complexity:** Not too simple (Model 1) or too complex (Model 3)
- **Good Regularization:** Prevents overfitting while allowing learning
- **Feature Utilization:** Effectively uses all 45 features

### Model 3 Issues (Fixed)

- **Original Problem:** Too much regularization → stopped at epoch 2
- **Fix:** Reduced dropout rates, smaller first layer, lighter L2
- **Result:** Now trains properly with better patience settings

## Future Improvements

1. **Hyperparameter Tuning:** Grid search for optimal learning rates, dropout rates
2. **Feature Engineering:** Additional interaction features
3. **Ensemble Methods:** Combine predictions from all 3 models
4. **Threshold Optimization:** Find optimal classification threshold (not just 0.5)

## Contact

For questions about the architecture or implementation, refer to the notebook comments or contact the authors.

---

**Last Updated:** December 2024
**Notebook Version:** Optimized with safe genre features and fixed Model 3

