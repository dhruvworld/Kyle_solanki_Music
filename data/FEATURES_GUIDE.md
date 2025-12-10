# Available Features Guide

## Current Features (Already in Dataset)

### Behavioral Features
- **tempo_bpm_synth**: Tempo in beats per minute (synthetic/behavioral)
- **time_of_day_synth**: Time of day (morning, afternoon, evening, night)
- **skipped_synth**: Whether track was skipped (0/1)

### Spotify Metadata
- **spotify_popularity**: Track popularity score (0-100)
- **genre**: Actual genre tags (e.g., "pop", "country, honky tonk", "bedroom pop")
- **is_explicit**: Whether track contains explicit content (True/False)
- **album_release_year**: Year the album was released
- **position**: Track position in playlist/album

---

## Additional Features We Can Fetch from Spotify

### 🎵 Audio Features (High Value for Music Classification)

These are **musical characteristics** that Spotify analyzes from the audio itself:

1. **danceability** (0.0-1.0)
   - How suitable a track is for dancing
   - Higher = more danceable
   - **Why useful**: Pop music tends to be more danceable

2. **energy** (0.0-1.0)
   - Perceptual measure of intensity and power
   - Higher = more energetic
   - **Why useful**: Pop often has high energy

3. **valence** (0.0-1.0)
   - Musical positiveness (happy/sad)
   - Higher = more positive/happy
   - **Why useful**: Pop music is typically more positive

4. **acousticness** (0.0-1.0)
   - Confidence that track is acoustic (not electronic)
   - Higher = more acoustic
   - **Why useful**: Pop is usually less acoustic

5. **speechiness** (0.0-1.0)
   - Presence of spoken words
   - Higher = more speech-like
   - **Why useful**: Distinguishes songs from rap/spoken word

6. **instrumentalness** (0.0-1.0)
   - Predicts if track has no vocals
   - Higher = more instrumental
   - **Why useful**: Pop songs typically have vocals

7. **liveness** (0.0-1.0)
   - Detects presence of audience in recording
   - Higher = more live
   - **Why useful**: Studio vs live recordings

8. **loudness** (typically -60 to 0 dB)
   - Overall loudness in decibels
   - **Why useful**: Production style indicator

9. **key** (0-11, -1 if unknown)
   - Musical key (C, C#, D, etc.)
   - **Why useful**: Some genres favor certain keys

10. **mode** (0 or 1)
    - Major (1) or minor (0)
    - **Why useful**: Major keys are more common in pop

11. **tempo_spotify** (BPM)
    - Spotify's tempo estimate
    - **Why useful**: Verify against tempo_bpm_synth

12. **duration_ms** (milliseconds)
    - Track length
    - **Why useful**: Pop songs often have specific length ranges

13. **time_signature** (3-7)
    - Musical time signature
    - **Why useful**: Most pop is 4/4 time

---

### 🎤 Artist Features (Can Fetch from Artist API)

1. **artist_popularity** (0-100)
   - Artist's overall popularity score
   - **Why useful**: Pop artists tend to be more popular

2. **artist_followers**
   - Number of Spotify followers
   - **Why useful**: Popularity indicator

3. **artist_genres** (already have this as tags)
   - List of genres associated with artist
   - **Why useful**: Already using this

---

### 📊 Derived/Engineered Features (Can Create from Existing Data)

1. **song_length_sec** = duration_ms / 1000
   - Song length in seconds
   - **Why useful**: Pop songs often 3-4 minutes

2. **is_major_key** = (mode == 1)
   - Binary: major vs minor key
   - **Why useful**: Pop favors major keys

3. **energy_x_danceability**
   - Interaction feature
   - **Why useful**: Pop often has both high

4. **valence_x_energy**
   - Interaction feature
   - **Why useful**: Happy energetic songs are often pop

5. **decade** = (album_release_year // 10) * 10
   - Release decade
   - **Why useful**: Pop trends vary by decade

6. **is_recent** = (album_release_year >= 2020)
   - Recent vs older tracks
   - **Why useful**: Modern pop characteristics

---

## How to Fetch Audio Features

### Option 1: Run the Script (Recommended)

```bash
cd /Users/dhruvsolanki/Desktop/Fury_Solanki/data
source setup_spotify.sh  # Set API credentials
python fetch_audio_features.py
```

This will:
- Fetch all audio features for tracks in `spotify_final_with_behavior.csv`
- Add 13 new columns to the CSV
- Take ~10-15 minutes for 40k tracks (due to rate limits)

### Option 2: Manual Fetch (For Testing)

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id="your_id",
        client_secret="your_secret"
    )
)

# Fetch features for a single track
features = sp.audio_features(['3t6gUcGYLrUuqwpXjOFWQc'])[0]
print(features)
```

---

## Recommended Feature Set for Pop Classification

### Core Features (Must Have)
1. ✅ **tempo_bpm_synth** - Already have
2. ✅ **time_of_day_synth** - Already have  
3. ✅ **spotify_popularity** - Already have
4. ✅ **genre** - Already have
5. ✅ **is_explicit** - Already have

### High-Value Audio Features (Should Add)
1. 🎯 **danceability** - Very predictive for pop
2. 🎯 **energy** - Pop is typically high energy
3. 🎯 **valence** - Pop is usually positive/happy
4. 🎯 **acousticness** - Pop is usually less acoustic
5. 🎯 **speechiness** - Helps distinguish from rap

### Medium-Value Features (Nice to Have)
1. **instrumentalness** - Pop has vocals
2. **loudness** - Production style
3. **mode** (major/minor) - Pop favors major
4. **duration_ms** - Song length patterns
5. **key** - Some keys more common in pop

### Derived Features (Can Create)
1. **energy × danceability** - Interaction
2. **valence × energy** - Happy energetic = pop
3. **is_major_key** - Binary from mode
4. **song_length_min** - Duration in minutes

---

## Expected Impact

Adding audio features should **significantly improve** model performance because:

1. **Direct musical characteristics**: Audio features capture what makes music "pop-like"
2. **Objective measurements**: Not dependent on user behavior
3. **Rich signal**: 13 additional features with strong predictive power
4. **Complement existing features**: Work well with popularity, genre, tempo

**Expected improvement**: ROC AUC from ~0.999 to potentially 0.999+ with better generalization

