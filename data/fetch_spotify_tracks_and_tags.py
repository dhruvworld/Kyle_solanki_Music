"""
Fetch Spotify track metadata and artist genres for songs_fetched.csv.
Outputs:
  - songs_track_metadata.csv
  - spotify_tags.csv  (song_spotify_id, tag, popularity)
Requires SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET env vars.
"""

import os
import time
from typing import List

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SONGS_FILE = "songs_fetched.csv"
TRACK_OUTPUT = "spotify_track_metadata.csv"
TAGS_OUTPUT = "spotify_tags.csv"
BATCH_SIZE = 50
SLEEP_SECONDS = 0.1


def chunked(seq: List[str], size: int):
    for idx in range(0, len(seq), size):
        yield seq[idx: idx + size]


def main():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("SPOTIFY_CLIENT_ID / SECRET not set")

    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
    )

    songs = pd.read_csv(SONGS_FILE, sep=";")
    track_ids = songs["spotify_id"].dropna().astype(str).unique().tolist()
    print(f"Loaded {len(track_ids):,} tracks from {SONGS_FILE}")

    track_rows = []
    artist_ids = set()

    for idx, batch in enumerate(chunked(track_ids, BATCH_SIZE), start=1):
        data = sp.tracks(batch)
        for track in data["tracks"]:
            if track is None:
                continue
            tid = track["id"]
            artists = track.get("artists", [])
            artist_id_list = [artist["id"] for artist in artists if artist and artist.get("id")]
            artist_ids.update(artist_id_list)
            track_rows.append(
                {
                    "spotify_id": tid,
                    "track_name": track["name"],
                    "track_popularity": track.get("popularity"),
                    "explicit": track.get("explicit"),
                    "album_name": track["album"]["name"] if track.get("album") else None,
                    "album_release_date": track["album"].get("release_date") if track.get("album") else None,
                    "artist_ids": "|".join(artist_id_list),
                }
            )
        if idx % 50 == 0:
            print(f"Track metadata: processed {min(idx * BATCH_SIZE, len(track_ids)):,}/{len(track_ids):,}")
        time.sleep(SLEEP_SECONDS)

    track_df = pd.DataFrame(track_rows)
    track_df.to_csv(TRACK_OUTPUT, index=False)
    print(f"Saved track metadata to {TRACK_OUTPUT} ({len(track_df):,} rows)")

    artist_ids = [aid for aid in artist_ids if aid]
    print(f"Fetching genres for {len(artist_ids):,} artist IDs")
    artist_rows = []
    for idx, batch in enumerate(chunked(artist_ids, BATCH_SIZE), start=1):
        data = sp.artists(batch)
        for artist in data["artists"]:
            if artist is None:
                continue
            genres = artist.get("genres", [])
            for genre in genres:
                artist_rows.append(
                    {
                        "artist_id": artist["id"],
                        "artist_name": artist["name"],
                        "genre_tag": genre,
                    }
                )
        if idx % 50 == 0:
            print(f"Artist genres: processed {min(idx * BATCH_SIZE, len(artist_ids)):,}/{len(artist_ids):,}")
        time.sleep(SLEEP_SECONDS)

    artist_genres_df = pd.DataFrame(artist_rows)
    artist_genres_df.to_csv("artist_genres_temp.csv", index=False)
    print(f"Saved artist genres snapshot (debug) with {len(artist_genres_df):,} rows")

    artist_genre_map = artist_genres_df.groupby("artist_id")["genre_tag"].apply(list).to_dict()
    tag_rows = []
    for _, row in track_df.iterrows():
        popularity = row.get("track_popularity", 0)
        for aid in (row["artist_ids"] or "").split("|"):
            for genre in artist_genre_map.get(aid, []):
                tag_rows.append(
                    {
                        "song_spotify_id": row["spotify_id"],
                        "tag": genre,
                        "popularity": popularity if pd.notna(popularity) else 0,
                    }
                )

    tags_df = pd.DataFrame(tag_rows)
    tags_df.to_csv(TAGS_OUTPUT, index=False)
    print(f"Saved Spotify tags to {TAGS_OUTPUT} ({len(tags_df):,} rows)")


if __name__ == "__main__":
    main()

