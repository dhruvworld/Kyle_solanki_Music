#!/bin/bash
# Script to check the progress of song fetching

echo "=========================================="
echo "Spotify Data Fetch Progress Checker"
echo "=========================================="
echo ""

cd /Users/dhruvsolanki/Desktop/Fury_Solanki/data

# Check if process is running
if pgrep -f "fetch_songs_data.py" > /dev/null; then
    echo "✅ Script is running in background"
else
    echo "❌ Script is not running"
fi

echo ""

# Check log file
if [ -f "fetch_output.log" ]; then
    echo "📊 Last 10 lines of log:"
    tail -10 fetch_output.log
    echo ""
fi

# Check output file
if [ -f "songs_fetched.csv" ]; then
    FILE_SIZE=$(ls -lh songs_fetched.csv | awk '{print $5}')
    LINE_COUNT=$(wc -l < songs_fetched.csv 2>/dev/null || echo "0")
    echo "📁 Output file: songs_fetched.csv"
    echo "   Size: $FILE_SIZE"
    echo "   Lines: $LINE_COUNT (approximately $(($LINE_COUNT - 1)) songs)"
else
    echo "📁 Output file: Not created yet"
fi

echo ""
echo "To view full log: tail -f fetch_output.log"
echo "To stop the process: pkill -f fetch_songs_data.py"

