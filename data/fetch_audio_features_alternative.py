"""
Alternative Approaches to Fetch Spotify Audio Features

This script tries multiple methods to fetch audio features:
1. Direct HTTP requests to Spotify API
2. Individual track requests (instead of batches)
3. Using track endpoint to check for available data
"""

import os
import time
import pandas as pd
import requests
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from pathlib import Path
from tqdm import tqdm

# Configuration
CSV_PATH = Path('spotify_final_with_behavior.csv')
OUTPUT_PATH = Path('spotify_final_with_behavior.csv')
SLEEP_SECONDS = 0.1

def get_access_token(client_id, client_secret):
    """Get access token directly via HTTP"""
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

def fetch_audio_features_http(access_token, track_ids):
    """Fetch audio features using direct HTTP requests"""
    url = "https://api.spotify.com/v1/audio-features"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Try with comma-separated IDs
    ids_str = ",".join(track_ids)
    params = {"ids": ids_str}
    
    response = requests.get(url, headers=headers, params=params)
    return response

def fetch_audio_features_single(access_token, track_id):
    """Fetch audio features for a single track"""
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    return response

def main():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("SPOTIFY_CLIENT_ID / SECRET not set")

    # Load existing CSV
    print(f"Loading {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df):,} tracks")
    
    # Get unique track IDs
    track_ids = df['song_spotify_id'].dropna().astype(str).unique().tolist()
    print(f"Fetching audio features for {len(track_ids):,} unique tracks...")
    
    # Initialize columns if they don't exist
    audio_feature_cols = ['danceability', 'energy', 'valence', 'acousticness']
    for col in audio_feature_cols:
        if col not in df.columns:
            df[col] = None
    
    # Try Method 1: Direct HTTP with access token
    print("\n=== Method 1: Direct HTTP Requests ===")
    try:
        access_token = get_access_token(client_id, client_secret)
        print("✅ Got access token")
        
        # Try a small batch first
        test_batch = track_ids[:10]
        response = fetch_audio_features_http(access_token, test_batch)
        
        if response.status_code == 200:
            print("✅ HTTP method works! Fetching all tracks...")
            audio_features_dict = {}
            
            # Fetch in batches of 100
            batch_size = 100
            for i in tqdm(range(0, len(track_ids), batch_size), desc="Fetching features"):
                batch = track_ids[i:i+batch_size]
                response = fetch_audio_features_http(access_token, batch)
                
                if response.status_code == 200:
                    features = response.json().get('audio_features', [])
                    for j, track_id in enumerate(batch):
                        if j < len(features) and features[j] is not None:
                            audio_features_dict[track_id] = {
                                'danceability': features[j].get('danceability'),
                                'energy': features[j].get('energy'),
                                'valence': features[j].get('valence'),
                                'acousticness': features[j].get('acousticness'),
                            }
                elif response.status_code == 403:
                    print(f"\n❌ 403 Forbidden on batch {i//batch_size + 1}")
                    print("   Trying single-track method...")
                    break
                else:
                    print(f"\n⚠️  Error {response.status_code}: {response.text[:200]}")
                
                time.sleep(SLEEP_SECONDS)
            
            # Map features to dataframe
            if audio_features_dict:
                for idx, row in df.iterrows():
                    track_id = str(row['song_spotify_id'])
                    if track_id in audio_features_dict:
                        features = audio_features_dict[track_id]
                        df.at[idx, 'danceability'] = features.get('danceability')
                        df.at[idx, 'energy'] = features.get('energy')
                        df.at[idx, 'valence'] = features.get('valence')
                        df.at[idx, 'acousticness'] = features.get('acousticness')
                
                success_count = df['danceability'].notna().sum()
                print(f"\n✅ Successfully fetched {success_count:,}/{len(df):,} tracks")
                df.to_csv(OUTPUT_PATH, index=False)
                print(f"✅ Saved to {OUTPUT_PATH}")
                return
        elif response.status_code == 403:
            print("❌ 403 Forbidden - trying single-track method...")
        else:
            print(f"❌ HTTP method failed: {response.status_code} - {response.text[:200]}")
    except Exception as e:
        print(f"❌ HTTP method error: {e}")
    
    # Try Method 2: Single track requests
    print("\n=== Method 2: Single Track Requests ===")
    try:
        access_token = get_access_token(client_id, client_secret)
        audio_features_dict = {}
        success_count = 0
        
        # Test with first 10 tracks
        for track_id in tqdm(track_ids[:100], desc="Testing single-track method"):
            response = fetch_audio_features_single(access_token, track_id)
            
            if response.status_code == 200:
                features = response.json()
                audio_features_dict[track_id] = {
                    'danceability': features.get('danceability'),
                    'energy': features.get('energy'),
                    'valence': features.get('valence'),
                    'acousticness': features.get('acousticness'),
                }
                success_count += 1
            elif response.status_code == 403:
                print(f"\n❌ 403 Forbidden even for single tracks")
                print("   This endpoint requires different permissions.")
                break
            elif response.status_code == 429:
                print(f"\n⚠️  Rate limited, waiting...")
                time.sleep(60)
            else:
                print(f"\n⚠️  Error {response.status_code} for track {track_id}")
            
            time.sleep(SLEEP_SECONDS)
        
        if success_count > 0:
            print(f"\n✅ Single-track method works! Fetched {success_count} tracks")
            print("   This method is slow - would take ~11 hours for 40k tracks")
            print("   Consider using batch method if it works")
        else:
            print("❌ Single-track method also failed")
    except Exception as e:
        print(f"❌ Single-track method error: {e}")
    
    # Try Method 3: Using spotipy with different approach
    print("\n=== Method 3: Spotipy with Different Batch Size ===")
    try:
        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret,
            )
        )
        
        # Try smaller batches
        test_ids = track_ids[:5]
        features = sp.audio_features(test_ids)
        
        if features and features[0] is not None:
            print("✅ Spotipy works with small batches!")
            print("   The issue might be batch size or rate limiting")
        else:
            print("❌ Spotipy still fails")
    except SpotifyException as e:
        if e.http_status == 403:
            print("❌ 403 Forbidden - authentication/permission issue")
            print("\n💡 SOLUTION: Your Spotify app may need:")
            print("   1. Check Spotify Developer Dashboard")
            print("   2. Ensure 'Web API' is enabled")
            print("   3. Try creating a new app with different settings")
            print("   4. The audio_features endpoint should work with Client Credentials")
        else:
            print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("SUMMARY: All methods failed to fetch audio features")
    print("="*60)
    print("\nPossible solutions:")
    print("1. Check Spotify Developer Dashboard permissions")
    print("2. Verify your app has 'Web API' access enabled")
    print("3. Try creating a new Spotify app")
    print("4. Contact Spotify API support if issue persists")
    print("\nNote: The audio_features endpoint should work with Client Credentials")
    print("      If it doesn't, there may be an account/app configuration issue.")

if __name__ == "__main__":
    main()

