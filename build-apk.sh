#!/bin/bash
# ============================================================================
# Android APK Auto-Builder for Pong AI V2
# Builds an APK using Buildozer (Linux/WSL required)
# ============================================================================

echo "================================================================================"
echo "  Pong AI V2 - Android APK Auto-Builder"
echo "================================================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Step 1: Check if running on Linux
echo -e "${YELLOW}[1/8] Checking system...${NC}"
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}ERROR: This script requires Linux or WSL${NC}"
    echo -e "${YELLOW}Windows users: Install WSL2 with Ubuntu${NC}"
    echo -e "${YELLOW}Guide: https://docs.microsoft.com/en-us/windows/wsl/install${NC}"
    exit 1
fi
echo -e "${GREEN}  Running on Linux/WSL${NC}"

# Step 2: Check Python
echo -e "${YELLOW}[2/8] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 not found${NC}"
    echo -e "${YELLOW}Install: sudo apt update && sudo apt install python3 python3-pip${NC}"
    exit 1
fi
python_version=$(python3 --version | grep -oP '\d+\.\d+')
echo -e "${GREEN}  Python $python_version found${NC}"

# Step 3: Check if main.py exists
echo -e "${YELLOW}[3/8] Checking project files...${NC}"
if [ ! -f "main.py" ]; then
    echo -e "${RED}ERROR: main.py not found. Run this from project root.${NC}"
    exit 1
fi
echo -e "${GREEN}  Found main.py${NC}"

# Step 4: Install system dependencies
echo -e "${YELLOW}[4/8] Installing system dependencies...${NC}"
echo -e "${CYAN}  This may take 5-10 minutes on first run...${NC}"
sudo apt-get update -qq
sudo apt-get install -y -qq \
    python3-pip \
    build-essential \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}  System dependencies installed${NC}"
else
    echo -e "${RED}ERROR: Failed to install system dependencies${NC}"
    exit 1
fi

# Step 5: Install/upgrade pip
echo -e "${YELLOW}[5/8] Upgrading pip...${NC}"
python3 -m pip install --upgrade pip --quiet
echo -e "${GREEN}  pip upgraded${NC}"

# Step 6: Install Buildozer and dependencies
echo -e "${YELLOW}[6/8] Installing Buildozer and Cython...${NC}"
echo -e "${CYAN}  This may take 2-5 minutes...${NC}"
pip3 install --upgrade buildozer cython --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}  Buildozer installed${NC}"
else
    echo -e "${RED}ERROR: Failed to install Buildozer${NC}"
    exit 1
fi

# Step 7: Check/create buildozer.spec
echo -e "${YELLOW}[7/8] Configuring build...${NC}"
if [ ! -f "buildozer.spec" ]; then
    echo -e "${CYAN}  Creating buildozer.spec...${NC}"
    buildozer init
    # Modify buildozer.spec
    sed -i 's/title = .*/title = Pong AI V2/' buildozer.spec
    sed -i 's/package.name = .*/package.name = pongaiv2/' buildozer.spec
    sed -i 's/package.domain = .*/package.domain = com.pongai/' buildozer.spec
    sed -i 's/requirements = .*/requirements = python3,kivy,pygame,numpy/' buildozer.spec
    sed -i 's/orientation = .*/orientation = landscape/' buildozer.spec
else
    echo -e "${GREEN}  Found existing buildozer.spec${NC}"
fi

# Step 8: Build APK
echo -e "${YELLOW}[8/8] Building APK (this will take 10-30 minutes first time)...${NC}"
echo -e "${CYAN}  Buildozer will download Android SDK/NDK (1-2 GB)${NC}"
echo -e "${CYAN}  Grab a coffee! ☕${NC}"
echo ""

buildozer android debug

if [ $? -eq 0 ]; then
    # Find the APK
    apk_path=$(find bin -name "*.apk" | head -n 1)
    if [ -f "$apk_path" ]; then
        apk_size=$(du -h "$apk_path" | cut -f1)
        echo ""
        echo -e "${GREEN}================================================================================${NC}"
        echo -e "${GREEN}  BUILD SUCCESSFUL!${NC}"
        echo -e "${GREEN}================================================================================${NC}"
        echo ""
        echo -e "${CYAN}  Output: $apk_path${NC}"
        echo -e "${CYAN}  Size: $apk_size${NC}"
        echo ""
        echo -e "${YELLOW}To install on Android device:${NC}"
        echo -e "${YELLOW}1. Enable Developer Options on your Android device${NC}"
        echo -e "${YELLOW}2. Enable USB Debugging${NC}"
        echo -e "${YELLOW}3. Connect via USB${NC}"
        echo -e "${YELLOW}4. Run: buildozer android deploy run${NC}"
        echo ""
        echo -e "${YELLOW}Or transfer $apk_path to your device and install manually${NC}"
        echo ""
    else
        echo -e "${RED}ERROR: APK not found after build${NC}"
        exit 1
    fi
else
    echo -e "${RED}ERROR: Build failed. Check logs above.${NC}"
    echo -e "${YELLOW}Common fixes:${NC}"
    echo -e "${YELLOW}  - Ensure you have 10+ GB free space${NC}"
    echo -e "${YELLOW}  - Check internet connection (downloads SDK/NDK)${NC}"
    echo -e "${YELLOW}  - Run: buildozer android clean${NC}"
    exit 1
fi
