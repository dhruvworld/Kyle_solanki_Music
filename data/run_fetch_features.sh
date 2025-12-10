#!/bin/bash
# Script to fetch the 4 priority audio features

echo "=========================================="
echo "Fetching Priority Audio Features"
echo "=========================================="
echo ""
echo "This will fetch:"
echo "  - danceability (pop typically >0.6)"
echo "  - energy (pop typically >0.5)"
echo "  - valence (pop typically >0.5)"
echo "  - acousticness (pop typically <0.5)"
echo ""

# Check if credentials are set
if [ -z "$SPOTIFY_CLIENT_ID" ] || [ -z "$SPOTIFY_CLIENT_SECRET" ]; then
    echo "⚠️  Credentials not set in environment."
    echo ""
    echo "Please set them now:"
    echo ""
    read -p "Enter Spotify Client ID: " CLIENT_ID
    read -sp "Enter Spotify Client Secret: " CLIENT_SECRET
    echo ""
    echo ""
    
    export SPOTIFY_CLIENT_ID="$CLIENT_ID"
    export SPOTIFY_CLIENT_SECRET="$CLIENT_SECRET"
fi

echo "Starting feature fetch..."
echo "This will take approximately 10-15 minutes for 40,000 tracks..."
echo ""

cd /Users/dhruvsolanki/Desktop/Fury_Solanki/data
conda run -n ai-music-proj-env python fetch_audio_features.py

echo ""
echo "✅ Done! Check spotify_final_with_behavior.csv for the new columns."

