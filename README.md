# Kyle_solanki_Music

## Overview

This project explores music skip behaviour and uses a Feed‑Forward Neural Network (FFNN) to predict whether a track belongs to the pop genre based purely on user behaviour and metadata. The work centres around three assets:

- `music_skip_combined.csv`: dataset combining listener behaviour with song metadata
- `Furey_Solanki_PopMusicFFNN.ipynb`: end‑to‑end modelling notebook
- `MS530_TrackB_Project_Idea_4.pdf`: project brief supplied by the course

## Dataset Creation

1. **Source files**:  
   - `music_skip_behavior.csv` (behavioural signals such as song length, tempo, popularity score, time of day, explicit flag, user_liked_previous_song, and the skip label)  
   - `songs.csv` and `tags.csv` (Spotify metadata: song name, artist, genre, and community tags)

2. **Join logic**:
   - Sampled songs from `songs.csv` to pair with each behavioural row (1:1 mapping).
   - Aggregated top tags from `tags.csv` per song to form the `tags` column.
   - Merged behavioural features and song metadata into `music_skip_combined.csv`, resulting in 1,001 rows with the schema:  
     `song_name, artist, genre, tags, song_length_sec, tempo_bpm, popularity_score, time_of_day, is_explicit, user_liked_previous_song, skipped`

3. **No synthetic rows**: All records trace back to the original behaviour log; we only augmented each row with the matching song metadata.

## Modelling Approach

### Target definition

- Created a binary label `is_pop_genre` by scanning the `genre` and `tags` text for pop‑related keywords (`pop`, `dance-pop`, `indie pop`, `k-pop`, etc.).
- Added a coarse `genre_family` bucket (pop, rock, hiphop, electronic, folk, jazz, classical, world, other) to retain high-level context while keeping everything derived from the original columns.

### Feature engineering (minimal, transparent)

- Numeric: `song_length_sec`, `tempo_bpm`, `popularity_score`, `is_explicit`, `user_liked_previous_song`, `skipped`
- Categorical: `time_of_day`, engineered `genre_family` (one-hot encoded)
- No oversampling, no class rebalancing, no synthetic noise

### Train / validation / test split

- 60% train, 5% validation, 35% test (stratified on the pop label, but still drawn directly from the raw dataset)

### Models

1. **FFNN (TensorFlow/Keras)**
   - Architecture: `[Input -> Dense(16) -> Dense(8) -> Output(sigmoid)]`
   - Loss: Binary cross-entropy
   - Optimizer: Adam (learning rate 0.001)
   - Early stopping on validation loss
   - Outputs recorded: loss curves, confusion matrix, and ROC

2. **Random Forest baseline (scikit-learn)**
   - `n_estimators=400`, `class_weight='balanced_subsample'`
   - Same feature set and data splits as the FFNN
   - Outputs recorded: accuracy, classification report, and ROC

### Notebook Flow

1. Import libraries and define constants (data paths, keyword lists, feature lists)
2. Helper functions:
   - `detect_pop_label` / `assign_genre_family`
   - `prepare_dataset` (creates engineered columns, fills NA, one-hot encodes)
   - `split_scaled_sets` (train/val/test split + scaling)
   - `build_ffnn` (model creation and compilation)
   - `build_music_nn` (full FFNN training/evaluation pipeline)
   - `evaluate_random_forest` (baseline comparison)
3. Final cells call `build_music_nn` and `evaluate_random_forest` to produce the reported metrics and plots.

## Reproducing Results

1. **Environment**  
   - Python 3.10 (conda env `music-tf`)  
   - Key packages: `tensorflow==2.19.1`, `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `nbconvert`

2. **run**  
   ```bash
   conda activate music-tf
   jupyter notebook Furey_Solanki_PopMusicFFNN.ipynb
   # or headless execution:
   jupyter nbconvert --to notebook --execute Furey_Solanki_PopMusicFFNN.ipynb --output Furey_Solanki_PopMusicFFNN.ipynb
   ```

3. **Outputs**  
   - FFNN: training/validation loss curve, confusion matrix, ROC, accuracy ≈ (from notebook output)
   - Random Forest: classification report, ROC curve

## Notes

- All data originates from the raw behaviour/metadata files—no synthetic examples.
- Feature engineering is limited to transformations needed for modelling (keyword-based labels, one-hot encoding).
- Git repo: `https://github.com/dhruvworld/Kyle_solanki_Music`

Feel free to extend the dataset (e.g., use additional song features) or test other classifiers, but the current README reflects exactly how the shared results were produced.

