#!/bin/bash
# Quick script to fetch audio features with credential setup

cd /Users/dhruvsolanki/Desktop/Fury_Solanki/data

echo "=========================================="
echo "Fetching 4 Priority Audio Features"
echo "=========================================="
echo ""
echo "Features to fetch:"
echo "  • danceability (pop typically >0.6)"
echo "  • energy (pop typically >0.5)"
echo "  • valence (pop typically >0.5)"
echo "  • acousticness (pop typically <0.5)"
echo ""

# Check if credentials are already set
if [ -z "$SPOTIFY_CLIENT_ID" ] || [ -z "$SPOTIFY_CLIENT_SECRET" ]; then
    echo "⚠️  Credentials not found in environment."
    echo ""
    echo "Please enter your Spotify API credentials:"
    echo "(Get them from: https://developer.spotify.com/dashboard)"
    echo ""
    read -p "Spotify Client ID: " CLIENT_ID
    read -sp "Spotify Client Secret: " CLIENT_SECRET
    echo ""
    echo ""
    
    export SPOTIFY_CLIENT_ID="$CLIENT_ID"
    export SPOTIFY_CLIENT_SECRET="$CLIENT_SECRET"
else
    echo "✅ Using credentials from environment"
    echo ""
fi

echo "Starting fetch... This will take ~10-15 minutes for 40,000 tracks"
echo "Progress will be shown below:"
echo ""

conda run -n ai-music-proj-env python fetch_audio_features.py

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! Audio features added to CSV"
    echo "=========================================="
    echo ""
    echo "New columns added:"
    echo "  • danceability"
    echo "  • energy"
    echo "  • valence"
    echo "  • acousticness"
    echo ""
    echo "File: spotify_final_with_behavior.csv"
else
    echo ""
    echo "=========================================="
    echo "❌ ERROR: Fetch failed"
    echo "=========================================="
    echo ""
    echo "Check the error messages above."
    echo "Common issues:"
    echo "  • Invalid credentials"
    echo "  • Network issues"
    echo "  • Rate limiting (wait a few minutes)"
fi

