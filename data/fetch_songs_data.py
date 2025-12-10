"""
Fetch 35,000-40,000 songs from Spotify API
Similar to the original data collection process but using Spotify API directly
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import json
from tqdm import tqdm
import os

# Configuration
TARGET_SONGS = 40000  # Target number of songs to fetch
OUTPUT_DIR = "."  # Current directory (data folder)
SONGS_OUTPUT = os.path.join(OUTPUT_DIR, "songs_fetched.csv")
TAGS_OUTPUT = os.path.join(OUTPUT_DIR, "tags_fetched.csv")

# Spotify API credentials (you'll need to set these)
# Get them from: https://developer.spotify.com/dashboard
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '')

def setup_spotify_client():
    """Initialize Spotify API client"""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError(
            "Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.\n"
            "Get them from: https://developer.spotify.com/dashboard"
        )
    
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def fetch_songs_from_playlists(sp, target_count):
    """
    Fetch songs from various Spotify playlists to reach target count
    Uses popular playlists across different genres
    """
    songs_data = []
    
    # Popular playlist IDs from Spotify (these are actual playlist IDs)
    popular_playlists = [
        '37i9dQZF1DXcBWIGoYBM5M',  # Today's Top Hits
        '37i9dQZF1DX0XUsuxWHRQd',  # RapCaviar
        '37i9dQZF1DX4o1oenSJRJd',  # All Out 80s
        '37i9dQZF1DX76t638VZCAQ',  # Rock Classics
        '37i9dQZF1DXbITWG1ZJKYt',  # Jazz Classics
        '37i9dQZF1DX4sWSpwq3LiO',  # Peaceful Piano
        '37i9dQZF1DX4sSPT1KXqQO',  # Country Top 50
        '37i9dQZF1DX4JAvHpjipBk',  # New Music Friday
        '37i9dQZF1DXcF6B6QPhFDv',  # Hot Country
        '37i9dQZF1DX10zKzsJ2jqH',  # Pop Rising
        '37i9dQZF1DX0kbJZpiYdSz',  # Hip-Hop Central
        '37i9dQZF1DX76t638VZCAQ',  # Rock This
        '37i9dQZF1DX4dyzvuaRJ0n',  # Chill Hits
        '37i9dQZF1DX4UtSsGT1Sbe',  # All New Indie
        '37i9dQZF1DX2sUQwD7tbmL',  # Feel Good Friday
        '37i9dQZF1DXcBWIGoYBM5M',  # Pop Mix
        '37i9dQZF1DX0XUsuxWHRQd',  # Hip Hop Mix
        '37i9dQZF1DX76t638VZCAQ',  # Rock Mix
        '37i9dQZF1DXbITWG1ZJKYt',  # Jazz Mix
        '37i9dQZF1DX4sSPT1KXqQO',  # Country Mix
    ]
    
    print(f"Fetching songs from popular Spotify playlists...")
    print(f"Target: {target_count:,} songs")
    
    for playlist_id in tqdm(popular_playlists, desc="Playlists"):
                if len(songs_data) >= target_count:
                    break
                
        try:
            # Get playlist info
            playlist = sp.playlist(playlist_id)
                playlist_name = playlist['name']
                
                    # Get tracks from playlist
                    results = sp.playlist_tracks(playlist_id, limit=100)
                    
                    while results and len(songs_data) < target_count:
                        for item in results['items']:
                            if len(songs_data) >= target_count:
                                break
                            
                            if item['track'] and item['track']['id']:
                                track = item['track']
                                
                        # Skip if track is None or local
                        if not track or track.get('is_local', False):
                            continue
                        
                        # Extract genre from playlist name or use default
                        genre = 'mixed'
                        if 'pop' in playlist_name.lower():
                            genre = 'pop'
                        elif 'rock' in playlist_name.lower():
                            genre = 'rock'
                        elif 'hip' in playlist_name.lower() or 'rap' in playlist_name.lower():
                            genre = 'hip hop'
                        elif 'jazz' in playlist_name.lower():
                            genre = 'jazz'
                        elif 'country' in playlist_name.lower():
                            genre = 'country'
                        elif 'electronic' in playlist_name.lower() or 'edm' in playlist_name.lower():
                            genre = 'electronic'
                                
                                songs_data.append({
                                    'spotify_id': track['id'],
                                    'name': track['name'],
                                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                                    'position': len(songs_data) + 1,
                                    'genre_name': genre,
                                    'popularity': track.get('popularity', 0),
                                    'duration_ms': track.get('duration_ms', 0),
                                    'album': track['album']['name'] if track.get('album') else '',
                                    'playlist_name': playlist_name
                                })
                        
                        # Get next page if available
                        if results['next'] and len(songs_data) < target_count:
                            results = sp.next(results)
                    time.sleep(0.1)  # Rate limiting
                        else:
                    break
        
        except Exception as e:
            print(f"Error fetching playlist {playlist_id}: {e}")
            continue
    
    return songs_data

def fetch_songs_from_featured_playlists(sp, target_count):
    """
    Fetch from popular Spotify playlists using direct playlist IDs
    """
    songs_data = []
    
    print("Fetching from popular Spotify playlists...")
    
    # More popular playlist IDs
    popular_playlist_ids = [
        '37i9dQZF1DXcBWIGoYBM5M',  # Today's Top Hits
        '37i9dQZF1DX0XUsuxWHRQd',  # RapCaviar
        '37i9dQZF1DX4o1oenSJRJd',  # All Out 80s
        '37i9dQZF1DX76t638VZCAQ',  # Rock Classics
        '37i9dQZF1DXbITWG1ZJKYt',  # Jazz Classics
        '37i9dQZF1DX4sWSpwq3LiO',  # Peaceful Piano
        '37i9dQZF1DX4sSPT1KXqQO',  # Country Top 50
        '37i9dQZF1DX4JAvHpjipBk',  # New Music Friday
    ]
    
    for playlist_id in tqdm(popular_playlist_ids, desc="Featured playlists"):
            if len(songs_data) >= target_count:
                break
            
        try:
            playlist = sp.playlist(playlist_id)
            playlist_name = playlist['name']
                results = sp.playlist_tracks(playlist_id, limit=100)
                
                while results and len(songs_data) < target_count:
                    for item in results['items']:
                        if len(songs_data) >= target_count:
                            break
                        
                        if item['track'] and item['track']['id']:
                            track = item['track']
                            
                        if not track or track.get('is_local', False):
                            continue
                        
                            songs_data.append({
                                'spotify_id': track['id'],
                                'name': track['name'],
                                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                                'position': len(songs_data) + 1,
                                'genre_name': 'featured',
                                'popularity': track.get('popularity', 0),
                                'duration_ms': track.get('duration_ms', 0),
                                'album': track['album']['name'] if track.get('album') else '',
                                'playlist_name': playlist_name
                            })
                    
                    if results['next'] and len(songs_data) < target_count:
                        results = sp.next(results)
                    time.sleep(0.1)
                    else:
                        break
            
            except Exception as e:
            print(f"Error with playlist {playlist_id}: {e}")
                continue
    
    return songs_data

def fetch_songs_from_search(sp, target_count, current_count, existing_ids=None):
    """
    Fetch songs by searching for popular tracks with extensive search terms
    """
    if existing_ids is None:
        existing_ids = set()
    
    songs_data = []
    search_terms = []
    
    # Years - expand range
    for year in range(1960, 2025, 5):  # Every 5 years
        search_terms.append(f'year:{year}')
    
    # Popular artists - expanded list
    popular_artists = [
        'Taylor Swift', 'Drake', 'The Weeknd', 'Ed Sheeran', 'Ariana Grande',
        'Post Malone', 'Billie Eilish', 'Dua Lipa', 'Bad Bunny', 'The Beatles',
        'Queen', 'Eminem', 'Kanye West', 'Rihanna', 'Beyonce', 'Justin Bieber',
        'Bruno Mars', 'Adele', 'Coldplay', 'Imagine Dragons', 'Maroon 5',
        'Kendrick Lamar', 'Travis Scott', 'J. Cole', 'SZA', 'Doja Cat',
        'Olivia Rodrigo', 'Harry Styles', 'Lana Del Rey', 'The Weeknd',
        'Michael Jackson', 'Elvis Presley', 'Madonna', 'Prince', 'David Bowie',
        'Bob Dylan', 'The Rolling Stones', 'Led Zeppelin', 'Pink Floyd',
        'Nirvana', 'Radiohead', 'U2', 'Red Hot Chili Peppers', 'Foo Fighters',
        'Linkin Park', 'Green Day', 'Blink-182', 'Metallica', 'AC/DC',
        'Jay-Z', 'Nas', 'Tupac', 'Biggie', '50 Cent', 'Snoop Dogg',
        'Frank Sinatra', 'Ella Fitzgerald', 'Louis Armstrong', 'Miles Davis',
        'John Coltrane', 'Duke Ellington', 'Charlie Parker', 'Thelonious Monk'
    ]
    
    for artist in popular_artists:
        search_terms.append(f'artist:{artist}')
    
    # Genres - expanded
    genres = ['pop', 'rock', 'hip hop', 'rap', 'electronic', 'edm', 'house', 'techno',
              'jazz', 'country', 'r&b', 'soul', 'reggae', 'indie', 'alternative',
              'metal', 'punk', 'folk', 'blues', 'classical', 'k-pop', 'j-pop',
              'latin', 'salsa', 'bossa nova', 'funk', 'disco', 'gospel', 'bluegrass']
    for genre in genres:
        search_terms.append(f'genre:{genre}')
    
    # Popular keywords
    keywords = ['hits', 'popular', 'top', 'best', 'classic', 'new', 'trending', 
                'viral', 'chart', 'billboard', 'hot', 'fresh', 'latest']
    for keyword in keywords:
        search_terms.append(keyword)
    
    print("Fetching songs via search...")
    print(f"Total search terms: {len(search_terms)}")
    
    for term in tqdm(search_terms, desc="Search terms"):
        if current_count + len(songs_data) >= target_count:
            break
        
        try:
            # Search with offset to get more results per term
            offset = 0
            max_offset = 1000  # Spotify allows up to 1000 results per search
            
            while offset < max_offset and current_count + len(songs_data) < target_count:
                results = sp.search(q=term, type='track', limit=50, offset=offset, market='US')
            
                if not results['tracks']['items']:
                    break
                
                new_songs_this_batch = 0
            for track in results['tracks']['items']:
                if current_count + len(songs_data) >= target_count:
                    break
                
                    if track['id'] and track['id'] not in existing_ids:
                        # Extract genre from search term
                        genre = 'mixed'
                        if ':' in term:
                            genre = term.split(':')[1].strip()
                        elif term in genres:
                            genre = term
                        
                        existing_ids.add(track['id'])  # Mark as seen
                    songs_data.append({
                        'spotify_id': track['id'],
                        'name': track['name'],
                        'artist': ', '.join([artist['name'] for artist in track['artists']]),
                        'position': current_count + len(songs_data) + 1,
                            'genre_name': genre,
                        'popularity': track.get('popularity', 0),
                        'duration_ms': track.get('duration_ms', 0),
                        'album': track['album']['name'] if track.get('album') else '',
                        'playlist_name': 'search'
                    })
                        new_songs_this_batch += 1
                
                # If no new songs in this batch, break to avoid infinite loop
                if new_songs_this_batch == 0:
                    break
                
                offset += 50
                time.sleep(0.1)  # Rate limiting
                
                # Print progress every 10 offsets
                if offset % 500 == 0:
                    print(f"  Progress: {len(songs_data):,} new songs found so far (term: {term[:30]}...)")
            
            time.sleep(0.1)  # Additional delay between search terms
        
        except Exception as e:
            print(f"Error searching for {term}: {e}")
            continue
    
    return songs_data

def fetch_songs_from_search_with_saving(sp, target_count, current_count, existing_ids, existing_songs_list):
    """
    Fetch songs with periodic saving to track progress
    """
    songs_data = []
    search_terms = []
    
    # Years - expand range
    for year in range(1960, 2025, 5):
        search_terms.append(f'year:{year}')
    
    # Popular artists
    popular_artists = [
        'Taylor Swift', 'Drake', 'The Weeknd', 'Ed Sheeran', 'Ariana Grande',
        'Post Malone', 'Billie Eilish', 'Dua Lipa', 'Bad Bunny', 'The Beatles',
        'Queen', 'Eminem', 'Kanye West', 'Rihanna', 'Beyonce', 'Justin Bieber',
        'Bruno Mars', 'Adele', 'Coldplay', 'Imagine Dragons', 'Maroon 5',
        'Kendrick Lamar', 'Travis Scott', 'J. Cole', 'SZA', 'Doja Cat',
        'Olivia Rodrigo', 'Harry Styles', 'Lana Del Rey', 'The Weeknd',
        'Michael Jackson', 'Elvis Presley', 'Madonna', 'Prince', 'David Bowie',
        'Bob Dylan', 'The Rolling Stones', 'Led Zeppelin', 'Pink Floyd',
        'Nirvana', 'Radiohead', 'U2', 'Red Hot Chili Peppers', 'Foo Fighters',
        'Linkin Park', 'Green Day', 'Blink-182', 'Metallica', 'AC/DC',
        'Jay-Z', 'Nas', 'Tupac', 'Biggie', '50 Cent', 'Snoop Dogg',
        'Frank Sinatra', 'Ella Fitzgerald', 'Louis Armstrong', 'Miles Davis',
        'John Coltrane', 'Duke Ellington', 'Charlie Parker', 'Thelonious Monk'
    ]
    
    for artist in popular_artists:
        search_terms.append(f'artist:{artist}')
    
    # Genres
    genres = ['pop', 'rock', 'hip hop', 'rap', 'electronic', 'edm', 'house', 'techno',
              'jazz', 'country', 'r&b', 'soul', 'reggae', 'indie', 'alternative',
              'metal', 'punk', 'folk', 'blues', 'classical', 'k-pop', 'j-pop',
              'latin', 'salsa', 'bossa nova', 'funk', 'disco', 'gospel', 'bluegrass']
    for genre in genres:
        search_terms.append(f'genre:{genre}')
    
    # Popular keywords
    keywords = ['hits', 'popular', 'top', 'best', 'classic', 'new', 'trending', 
                'viral', 'chart', 'billboard', 'hot', 'fresh', 'latest']
    for keyword in keywords:
        search_terms.append(keyword)
    
    print("Fetching songs via search...")
    print(f"Total search terms: {len(search_terms)}")
    
    save_counter = 0
    for term_idx, term in enumerate(tqdm(search_terms, desc="Search terms")):
        if current_count + len(songs_data) >= target_count:
            break
        
        try:
            offset = 0
            max_offset = 1000
            
            while offset < max_offset and current_count + len(songs_data) < target_count:
                results = sp.search(q=term, type='track', limit=50, offset=offset, market='US')
                
                if not results['tracks']['items']:
                    break
                
                new_songs_this_batch = 0
                for track in results['tracks']['items']:
                    if current_count + len(songs_data) >= target_count:
                        break
                    
                    if track['id'] and track['id'] not in existing_ids:
                        genre = 'mixed'
                        if ':' in term:
                            genre = term.split(':')[1].strip()
                        elif term in genres:
                            genre = term
                        
                        existing_ids.add(track['id'])
                        songs_data.append({
                            'spotify_id': track['id'],
                            'name': track['name'],
                            'artist': ', '.join([artist['name'] for artist in track['artists']]),
                            'position': current_count + len(songs_data) + 1,
                            'genre_name': genre,
                            'popularity': track.get('popularity', 0),
                            'duration_ms': track.get('duration_ms', 0),
                            'album': track['album']['name'] if track.get('album') else '',
                            'playlist_name': 'search'
                        })
                        new_songs_this_batch += 1
                
                if new_songs_this_batch == 0:
                    break
                
                offset += 50
                time.sleep(0.1)
                
                # Save every 100 new songs or every 5 search terms
                save_counter += new_songs_this_batch
                if save_counter >= 100 or (term_idx + 1) % 5 == 0:
                    # Save current progress
                    all_current_songs = existing_songs_list + songs_data
                    df_temp = pd.DataFrame(all_current_songs)
                    if len(df_temp) > 0:
                        df_temp = df_temp[['spotify_id', 'name', 'artist', 'position', 'genre_name']].copy()
                        df_temp['position'] = range(1, len(df_temp) + 1)
                        df_temp.to_csv(SONGS_OUTPUT, sep=';', index=False, quoting=1)
                        print(f"\n💾 Progress saved: {len(df_temp):,} total songs (just added {new_songs_this_batch} new)")
                    save_counter = 0
        
        except Exception as e:
            print(f"Error searching for {term}: {e}")
            continue
    
    return songs_data

def main():
    """Main function to fetch songs data"""
    print("=" * 60)
    print("Spotify Songs Data Fetcher")
    print(f"Target: {TARGET_SONGS:,} songs")
    print("=" * 60)
    
    # Setup
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sp = setup_spotify_client()
    
    all_songs = []
    
    # Primary method: Use search (most reliable)
    print("\n[Method 1] Fetching songs via search (primary method)...")
    print("Note: Songs will be saved periodically to track progress")
    
    # Load existing songs if file exists
    existing_ids = set()
    existing_songs_list = []
    if os.path.exists(SONGS_OUTPUT):
        try:
            existing_df = pd.read_csv(SONGS_OUTPUT, sep=';')
            existing_ids = set(existing_df['spotify_id'].astype(str))
            for _, row in existing_df.iterrows():
                existing_songs_list.append({
                    'spotify_id': row['spotify_id'],
                    'name': row['name'],
                    'artist': row['artist'],
                    'position': len(existing_songs_list) + 1,
                    'genre_name': row['genre_name']
                })
            print(f"Found existing file with {len(existing_ids):,} unique songs")
        except:
            pass
    
    # Fetch songs with periodic saving
    songs1 = fetch_songs_from_search_with_saving(sp, TARGET_SONGS, len(existing_ids), existing_ids, existing_songs_list)
    all_songs.extend(songs1)
    print(f"Fetched {len(songs1):,} new songs via search")
    
    # Method 2: Try featured playlists if we need more
    if len(all_songs) < TARGET_SONGS:
        print(f"\n[Method 2] Fetching from featured playlists...")
        songs2 = fetch_songs_from_featured_playlists(sp, TARGET_SONGS - len(all_songs))
        all_songs.extend(songs2)
        print(f"Fetched {len(songs2):,} additional songs from featured playlists")
    
    # Method 3: Try category playlists if we still need more
    if len(all_songs) < TARGET_SONGS:
        print(f"\n[Method 3] Fetching from category playlists...")
        songs3 = fetch_songs_from_playlists(sp, TARGET_SONGS - len(all_songs))
        all_songs.extend(songs3)
        print(f"Fetched {len(songs3):,} additional songs from categories")
    
    # Remove duplicates based on spotify_id
    print(f"\nRemoving duplicates...")
    seen_ids = set()
    unique_songs = []
    
    # Add existing songs if file exists
    if os.path.exists(SONGS_OUTPUT):
        try:
            existing_df = pd.read_csv(SONGS_OUTPUT, sep=';')
            for _, row in existing_df.iterrows():
                if row['spotify_id'] not in seen_ids:
                    seen_ids.add(row['spotify_id'])
                    unique_songs.append({
                        'spotify_id': row['spotify_id'],
                        'name': row['name'],
                        'artist': row['artist'],
                        'position': len(unique_songs) + 1,
                        'genre_name': row['genre_name']
                    })
        except:
            pass
    
    # Add new songs
    for song in all_songs:
        if song['spotify_id'] not in seen_ids:
            seen_ids.add(song['spotify_id'])
            unique_songs.append(song)
    
    print(f"Total unique songs: {len(unique_songs):,}")
    
    # Convert to DataFrame
    df = pd.DataFrame(unique_songs)
    
    # Reorder and select columns matching original format
    df_output = df[['spotify_id', 'name', 'artist', 'position', 'genre_name']].copy()
    df_output.columns = ['spotify_id', 'name', 'artist', 'position', 'genre_name']
    
    # Update positions
    df_output['position'] = range(1, len(df_output) + 1)
    
    # Save to CSV with semicolon delimiter (matching original format)
    df_output.to_csv(SONGS_OUTPUT, sep=';', index=False, quoting=1)
    print(f"\n✅ Saved {len(df_output):,} songs to {SONGS_OUTPUT}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Total songs fetched: {len(df_output):,}")
    print(f"  Genres: {df_output['genre_name'].nunique()}")
    print(f"  Artists: {df_output['artist'].nunique()}")
    print("=" * 60)
    
    return df_output

if __name__ == "__main__":
    try:
        df = main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Installed required packages: pip install spotipy pandas tqdm")
        print("2. Set environment variables:")
        print("   export SPOTIFY_CLIENT_ID='your_client_id'")
        print("   export SPOTIFY_CLIENT_SECRET='your_client_secret'")
        print("3. Created a Spotify app at: https://developer.spotify.com/dashboard")

