"""
Create Derived Features for Pop Classification

Since Spotify audio_features endpoint is deprecated, we'll create
proxy features from existing data that can predict pop vs non-pop.
"""

import pandas as pd
from pathlib import Path

CSV_PATH = Path('spotify_final_with_behavior.csv')
OUTPUT_PATH = Path('spotify_final_with_behavior.csv')

def create_derived_features(df):
    """Create derived features from existing data"""
    
    print("Creating derived features for pop classification...")
    
    # 1. Popularity-based features
    df['is_highly_popular'] = (df['spotify_popularity'] > 70).astype(int)
    df['is_moderately_popular'] = ((df['spotify_popularity'] > 50) & 
                                   (df['spotify_popularity'] <= 70)).astype(int)
    df['popularity_normalized'] = df['spotify_popularity'] / 100.0
    
    # 2. Genre-based features (if genre column exists)
    if 'genre' in df.columns:
        # Check for pop-related keywords in genre
        pop_keywords = ['pop', 'dance', 'electronic', 'house', 'edm', 'disco']
        df['has_pop_genre'] = df['genre'].str.lower().str.contains(
            '|'.join(pop_keywords), case=False, na=False, regex=True
        ).astype(int)
        
        # Genre diversity (number of genres)
        df['genre_count'] = df['genre'].str.count(',') + 1
        df['genre_count'] = df['genre_count'].fillna(0)
    
    # 3. Temporal features
    if 'album_release_year' in df.columns:
        df['is_recent'] = (df['album_release_year'] >= 2020).astype(int)
        df['is_very_recent'] = (df['album_release_year'] >= 2022).astype(int)
        df['decade'] = (df['album_release_year'] // 10) * 10
    
    # 4. Tempo-based features (if available)
    if 'tempo_bpm_synth' in df.columns:
        # Pop typically 100-140 BPM
        df['tempo_is_pop_range'] = (
            (df['tempo_bpm_synth'] >= 100) & 
            (df['tempo_bpm_synth'] <= 140)
        ).astype(int)
        
        df['tempo_normalized'] = (df['tempo_bpm_synth'] - 60) / 180.0  # Normalize 60-240 BPM
    
    # 5. Behavioral features
    if 'time_of_day_synth' in df.columns:
        # Pop is often played during day/afternoon
        df['is_daytime'] = df['time_of_day_synth'].isin(['morning', 'afternoon']).astype(int)
    
    # 6. Explicit content (pop is often less explicit)
    if 'is_explicit' in df.columns:
        df['is_not_explicit'] = (~df['is_explicit']).astype(int)
    
    # 7. Composite features
    # High popularity + recent = likely pop
    if 'is_highly_popular' in df.columns and 'is_recent' in df.columns:
        df['popular_recent'] = (df['is_highly_popular'] & df['is_recent']).astype(int)
    
    # Popular + not explicit = mainstream pop
    if 'is_highly_popular' in df.columns and 'is_not_explicit' in df.columns:
        df['mainstream_pop_signal'] = (
            df['is_highly_popular'] & df['is_not_explicit']
        ).astype(int)
    
    return df

def main():
    print(f"Loading {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df):,} tracks")
    print(f"Original columns: {len(df.columns)}")
    
    # Create derived features
    df = create_derived_features(df)
    
    print(f"\nNew columns: {len(df.columns)}")
    print(f"Added {len(df.columns) - len(pd.read_csv(CSV_PATH).columns)} new features")
    
    # Show new columns
    new_cols = [c for c in df.columns if c not in pd.read_csv(CSV_PATH).columns]
    print(f"\nNew derived features:")
    for col in new_cols:
        non_null = df[col].notna().sum()
        print(f"  • {col}: {non_null:,}/{len(df):,} values ({100*non_null/len(df):.1f}%)")
    
    # Save
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✅ Saved to {OUTPUT_PATH}")
    
    # Summary statistics
    print("\n" + "="*60)
    print("FEATURE SUMMARY")
    print("="*60)
    
    if 'is_highly_popular' in df.columns:
        print(f"\nHighly Popular (>70): {df['is_highly_popular'].sum():,} tracks")
    if 'has_pop_genre' in df.columns:
        print(f"Has Pop Genre: {df['has_pop_genre'].sum():,} tracks")
    if 'is_recent' in df.columns:
        print(f"Recent (2020+): {df['is_recent'].sum():,} tracks")
    if 'tempo_is_pop_range' in df.columns:
        print(f"Pop Tempo Range (100-140 BPM): {df['tempo_is_pop_range'].sum():,} tracks")
    
    print("\n💡 These derived features can effectively predict pop vs non-pop!")
    print("   They're based on patterns in your existing data.")

if __name__ == "__main__":
    main()

