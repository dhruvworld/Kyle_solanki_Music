# Guide: Fetching 35,000-40,000 Songs from Spotify

## Overview

This guide explains how to fetch a large dataset of songs (35k-40k) from Spotify API, similar to how the original `songs.csv` was created.

## Prerequisites

### 1. Install Required Packages

```bash
pip install spotipy pandas tqdm
```

### 2. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in:
   - App name: (e.g., "Music Data Fetcher")
   - App description: (e.g., "Fetching songs for research")
   - Redirect URI: `http://localhost:8888/callback`
5. Click "Save"
6. Copy your **Client ID** and **Client Secret**

### 3. Set Environment Variables

```bash
export SPOTIFY_CLIENT_ID='your_client_id_here'
export SPOTIFY_CLIENT_SECRET='your_client_secret_here'
```

Or on Windows:
```cmd
set SPOTIFY_CLIENT_ID=your_client_id_here
set SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

## Usage

### Run the Script

```bash
cd /Users/dhruvsolanki/Desktop/Fury_Solanki/data
python fetch_songs_data.py
```

### What It Does

The script fetches songs using three methods:

1. **Featured Playlists** - Gets songs from Spotify's featured playlists
2. **Category Playlists** - Fetches from playlists across different genres (pop, rock, hip-hop, etc.)
3. **Search** - Uses search queries to find popular tracks

### Output

The script creates:
- `songs_fetched.csv` - Contains 35k-40k songs with columns:
  - `spotify_id` - Unique Spotify track ID
  - `name` - Song name
  - `artist` - Artist name(s)
  - `position` - Position number
  - `genre_name` - Genre classification

## Rate Limiting

Spotify API has rate limits:
- **Default**: 10,000 requests per hour per user
- The script includes delays (`time.sleep()`) to respect these limits
- Fetching 40k songs may take **2-4 hours** depending on API response times

## Alternative: Using Existing Data

If you want to work with the existing dataset:

```python
import pandas as pd

# Load existing songs
songs_df = pd.read_csv('songs.csv', sep=';')

# Sample 35k-40k songs
sampled = songs_df.sample(n=40000, random_state=42)
sampled.to_csv('songs_sampled.csv', sep=';', index=False)
```

## Troubleshooting

### Error: "Invalid client credentials"
- Check that your Client ID and Secret are correct
- Make sure environment variables are set properly
- Verify your Spotify app is active in the dashboard

### Error: "Rate limit exceeded"
- Wait an hour and try again
- Reduce the `TARGET_SONGS` value
- Increase `time.sleep()` delays in the script

### Error: "Module not found"
- Install missing packages: `pip install spotipy pandas tqdm`

## Next Steps

After fetching songs, you may want to:

1. **Fetch Tags from Last.FM** (similar to original process)
   - Requires Last.FM API key
   - See `DATA_SOURCE_README.md` for details

2. **Combine with Behavioral Data**
   - Use `create_combined_dataset.ipynb` to merge with behavioral data

3. **Filter by Genre**
   - Focus on specific genres if needed

## Notes

- The script fetches unique songs (removes duplicates)
- Songs are fetched from multiple sources to ensure diversity
- The output format matches the original `songs.csv` structure
- You can modify `TARGET_SONGS` in the script to change the number

