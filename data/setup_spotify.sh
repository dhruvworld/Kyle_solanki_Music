#!/bin/bash
# Setup script for Spotify API credentials
# Run this script to set your Spotify API credentials

echo "=========================================="
echo "Spotify API Credentials Setup"
echo "=========================================="
echo ""
echo "To get your Spotify API credentials:"
echo "1. Go to: https://developer.spotify.com/dashboard"
echo "2. Log in with your Spotify account"
echo "3. Click 'Create App'"
echo "4. Fill in the app details and save"
echo "5. Copy your Client ID and Client Secret"
echo ""
echo "Then run:"
echo "  export SPOTIFY_CLIENT_ID='your_client_id_here'"
echo "  export SPOTIFY_CLIENT_SECRET='your_client_secret_here'"
echo ""
echo "Or set them now:"
echo ""
read -p "Enter your Spotify Client ID: " CLIENT_ID
read -sp "Enter your Spotify Client Secret: " CLIENT_SECRET
echo ""

export SPOTIFY_CLIENT_ID="$CLIENT_ID"
export SPOTIFY_CLIENT_SECRET="$CLIENT_SECRET"

echo ""
echo "Credentials set! Now you can run:"
echo "  python fetch_songs_data.py"
echo ""

