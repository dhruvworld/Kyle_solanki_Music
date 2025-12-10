# Quick Guide: Fetch the 4 Priority Audio Features

## What We're Fetching

These 4 features are **most predictive** for pop vs non-pop classification:

1. **danceability** (0.0-1.0) - Pop is typically high (>0.6)
2. **energy** (0.0-1.0) - Pop is typically high (>0.5)  
3. **valence** (0.0-1.0) - Pop is typically positive/happy (>0.5)
4. **acousticness** (0.0-1.0) - Pop is typically low (<0.5, more electronic)

## How to Run

### Option 1: Interactive Script (Easiest)
```bash
cd /Users/dhruvsolanki/Desktop/Fury_Solanki/data
./run_fetch_features.sh
```

This will prompt you for credentials if not set.

### Option 2: Set Credentials First
```bash
cd /Users/dhruvsolanki/Desktop/Fury_Solanki/data

# Set your credentials
export SPOTIFY_CLIENT_ID='your_client_id_here'
export SPOTIFY_CLIENT_SECRET='your_client_secret_here'

# Run the fetch
conda run -n ai-music-proj-env python fetch_audio_features.py
```

### Option 3: One-Line with Credentials
```bash
cd /Users/dhruvsolanki/Desktop/Fury_Solanki/data && \
SPOTIFY_CLIENT_ID='your_id' SPOTIFY_CLIENT_SECRET='your_secret' \
conda run -n ai-music-proj-env python fetch_audio_features.py
```

## What Happens

1. Script loads `spotify_final_with_behavior.csv` (40,000 tracks)
2. Fetches audio features from Spotify API in batches of 100
3. Adds 4 new columns: `danceability`, `energy`, `valence`, `acousticness`
4. Saves updated CSV
5. Takes ~10-15 minutes (respects API rate limits)

## Expected Output

After running, your CSV will have these new columns:
- `danceability` - Float (0.0 to 1.0)
- `energy` - Float (0.0 to 1.0)
- `valence` - Float (0.0 to 1.0)
- `acousticness` - Float (0.0 to 1.0)

## Verify It Worked

```bash
# Check if columns were added
head -1 spotify_final_with_behavior.csv | tr ',' '\n' | grep -E 'danceability|energy|valence|acousticness'

# Or in Python
python -c "import pandas as pd; df = pd.read_csv('spotify_final_with_behavior.csv'); print('Columns:', [c for c in df.columns if c in ['danceability', 'energy', 'valence', 'acousticness']])"
```

## Next Steps

After fetching, update your notebook to use these features:
1. Add them to `numeric_features` list
2. They'll be automatically scaled with StandardScaler
3. Model should improve significantly!

