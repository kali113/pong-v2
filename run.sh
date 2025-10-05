#!/bin/bash
# Simple launcher for Linux/Mac
# Run: chmod +x run.sh && ./run.sh

echo "============================================================"
echo "  Pong AI V2 Launcher"
echo "============================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found"
    echo ""
    echo "Install Python:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo ""
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.10"

if ! awk -v ver="$python_version" -v req="$required_version" 'BEGIN { if (ver < req) exit 1 }'; then
    echo "WARNING: Python $python_version found, but 3.10+ recommended"
    echo ""
fi

# Try to run the game
echo "Running Pong AI V2..."
echo ""
python3 main.py

# Check exit code
if [ $? -ne 0 ]; then
    echo ""
    echo "============================================================"
    echo "  Game exited with errors"
    echo "============================================================"
    echo ""
    echo "Try installing dependencies:"
    echo "  pip3 install -r requirements.txt"
    echo ""
    echo "Or see BUILD.md for detailed instructions."
    echo "============================================================"
    read -p "Press Enter to exit..."
fi
