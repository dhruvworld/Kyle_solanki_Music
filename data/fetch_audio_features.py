"""
Fetch Priority Spotify Audio Features for Pop Classification

This script fetches the 4 most important audio features for pop vs non-pop classification:
- danceability: How suitable a track is for dancing (0.0-1.0) - Pop is typically high (>0.6)
- energy: Perceptual measure of intensity and power (0.0-1.0) - Pop is typically high (>0.5)
- valence: Musical positiveness (0.0-1.0) - Pop is typically positive/happy (>0.5)
- acousticness: Confidence measure of whether track is acoustic (0.0-1.0) - Pop is typically low (<0.5)

These features are added to spotify_final_with_behavior.csv
"""

import os
import time
import pandas as pd
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from pathlib import Path
from tqdm import tqdm

# Configuration
CSV_PATH = Path('spotify_final_with_behavior.csv')
OUTPUT_PATH = Path('spotify_final_with_behavior.csv')
BATCH_SIZE = 100  # Spotify allows up to 100 tracks per audio_features call
SLEEP_SECONDS = 0.1  # Small delay to respect rate limits

def chunked(seq, size):
    """Split sequence into chunks of given size"""
    for idx in range(0, len(seq), size):
        yield seq[idx: idx + size]

def main():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("SPOTIFY_CLIENT_ID / SECRET not set. Run: source setup_spotify.sh")

    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
    )

    # Load existing CSV
    print(f"Loading {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df):,} tracks")
    
    # Get unique track IDs
    track_ids = df['song_spotify_id'].dropna().astype(str).unique().tolist()
    print(f"Fetching audio features for {len(track_ids):,} unique tracks...")
    
    # Dictionary to store audio features
    audio_features_dict = {}
    
    # Fetch audio features in batches
    error_403_count = 0
    for idx, batch in enumerate(tqdm(chunked(track_ids, BATCH_SIZE), desc="Fetching audio features"), start=1):
        try:
            features = sp.audio_features(batch)
            
            for i, track_id in enumerate(batch):
                if features[i] is not None:
                    # Fetch only the 4 priority features for pop classification
                    audio_features_dict[track_id] = {
                        'danceability': features[i].get('danceability'),
                        'energy': features[i].get('energy'),
                        'valence': features[i].get('valence'),
                        'acousticness': features[i].get('acousticness'),
                    }
                else:
                    # Track not found or no features available
                    audio_features_dict[track_id] = None
            
            if idx % 10 == 0:
                print(f"  Processed {min(idx * BATCH_SIZE, len(track_ids)):,}/{len(track_ids):,} tracks")
            
            time.sleep(SLEEP_SECONDS)
            
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 403:
                error_403_count += 1
                if error_403_count == 1:
                    print(f"\n⚠️  WARNING: 403 Forbidden error on audio_features endpoint.")
                    print("   This endpoint requires additional permissions that may not be available")
                    print("   with your current Spotify API credentials.")
                    print("   The script will continue but may not be able to fetch audio features.")
                if error_403_count >= 5:
                    print(f"\n❌ Too many 403 errors. Stopping fetch.")
                    print("   Audio features cannot be fetched with current credentials.")
                    print("   You may need to use a different authentication method or check API permissions.")
                    break
            else:
                print(f"Error processing batch {idx}: {e}")
            continue
        except Exception as e:
            print(f"Error processing batch {idx}: {e}")
            continue
    
    # Add audio features to dataframe
    print("\nAdding audio features to dataframe...")
    
    # Initialize new columns - only the 4 priority features
    audio_feature_cols = ['danceability', 'energy', 'valence', 'acousticness']
    
    # Only add columns if they don't already exist
    for col in audio_feature_cols:
        if col not in df.columns:
            df[col] = None
    
    # Map features to dataframe
    for idx, row in df.iterrows():
        track_id = str(row['song_spotify_id'])
        if track_id in audio_features_dict and audio_features_dict[track_id] is not None:
            features = audio_features_dict[track_id]
            df.at[idx, 'danceability'] = features.get('danceability')
            df.at[idx, 'energy'] = features.get('energy')
            df.at[idx, 'valence'] = features.get('valence')
            df.at[idx, 'acousticness'] = features.get('acousticness')
    
    # Calculate success rate
    success_count = df['danceability'].notna().sum()
    print(f"\nSuccessfully fetched features for {success_count:,}/{len(df):,} tracks ({100*success_count/len(df):.1f}%)")
    
    # Save updated CSV
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✅ Saved updated dataset to {OUTPUT_PATH}")
    print(f"   Added {len(audio_feature_cols)} new audio feature columns")
    
    # Show summary statistics
    print("\nAudio Features Summary:")
    print(df[audio_feature_cols].describe())

if __name__ == "__main__":
    main()

