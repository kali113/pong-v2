# 📱 Mobile Build Guide (Android APK)

This guide explains how to build Pong AI V2 for Android devices.

## ⚠️ Important Notes

**Pygame on Android has limitations:**
- Touch input only (no keyboard/mouse cursor)
- Reduced performance on older devices
- Limited audio codec support
- Some Pygame features unsupported

**Recommended approach:**
Consider rewriting with Kivy for better mobile support, or adapt the game for touch-only controls.

## 🛠️ Prerequisites

### System Requirements
- **Linux** or **WSL** (Windows Subsystem for Linux)
- **Python 3.10+**
- **Git**
- **Java JDK 17**
- **20GB+ free disk space**

### Install Dependencies (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y git zip unzip openjdk-17-jdk build-essential \
  libssl-dev libffi-dev python3-dev autoconf libtool pkg-config \
  zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake \
  libffi-dev libssl-dev wget curl

# Install Python 3.10+ if not present
sudo apt install -y python3.10 python3.10-venv python3.10-dev

# Install Buildozer
pip3 install --user buildozer

# Install Cython
pip3 install --user cython
```

## 📦 Building APK

### Step 1: Prepare Environment

```bash
# Navigate to project directory
cd pong-ai-v2

# Ensure buildozer.spec exists
ls buildozer.spec

# Initialize build environment (first time only)
buildozer init
```

### Step 2: Configure buildozer.spec

The `buildozer.spec` file is already configured. Key settings:

```ini
[app]
title = Pong AI V2
package.name = pongaiv2
package.domain = com.pongai
version = 2.0.0
requirements = python3,pygame,numpy,pillow
orientation = landscape
```

### Step 3: Build Debug APK

```bash
# Build debug APK (takes 30-60 minutes first time)
buildozer android debug

# Output will be in: bin/pongaiv2-2.0.0-armeabi-v7a-debug.apk
```

### Step 4: Deploy to Device

```bash
# Enable USB debugging on Android device
# Connect device via USB

# Deploy and run
buildozer android deploy run

# Or manually install
adb install bin/pongaiv2-2.0.0-armeabi-v7a-debug.apk
```

## 🔧 Troubleshooting

### Build Fails

**Issue**: "No such file or directory"
```bash
# Solution: Clean build
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

**Issue**: "NDK not found"
```bash
# Solution: Let buildozer download it
buildozer android debug  # Will auto-download NDK
```

**Issue**: "SDK license not accepted"
```bash
# Solution: Accept licenses
yes | $HOME/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager --licenses
```

### App Crashes on Device

**Check logs:**
```bash
# View Android logs
adb logcat | grep python

# Or use buildozer
buildozer android logcat
```

**Common issues:**
- Missing Python modules → Add to `requirements` in buildozer.spec
- Unsupported Pygame features → Adapt code for mobile
- Out of memory → Reduce particle count, optimize graphics

## 🎮 Adapting for Mobile

### Touch Controls

Modify `main.py` to support touch:

```python
# In handle_input() or event loop
if event.type == pygame.FINGERDOWN:
    # Touch position
    touch_x = event.x * SCREEN_WIDTH
    touch_y = event.y * SCREEN_HEIGHT
    
    # Move paddle to touch position
    self.player.y = touch_y - PADDLE_HEIGHT // 2
```

### Performance Optimization

```python
# Reduce particles for mobile
self.particle_pool = ParticlePool(60)  # Instead of 360

# Lower FPS if needed
self.clock.tick(30)  # Instead of 60

# Disable some effects
self.show_particles = False
```

### Screen Orientation

Lock to landscape in buildozer.spec:
```ini
orientation = landscape
```

## 📱 Alternative: Progressive Web App (PWA)

Consider Pygame Web (Emscripten) for browser-based mobile play:

```bash
# Install Pygame Web
pip install pygame-web

# Build for web
pygbag main.py
```

Advantages:
- No installation required
- Works on iOS and Android
- Better compatibility

## 🔄 Continuous Integration

Add to `.github/workflows/android-build.yml`:

```yaml
name: Android Build

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build APK
        run: |
          pip install buildozer
          buildozer android debug
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: PongAI-Android
          path: bin/*.apk
```

## 📖 Resources

- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Python for Android](https://python-for-android.readthedocs.io/)
- [Pygame Subset for Android](https://pygame.org/wiki/pgs4a)
- [Kivy (Alternative Framework)](https://kivy.org/)

## ⚡ Quick Commands Reference

```bash
# Clean build
buildozer android clean

# Debug APK
buildozer android debug

# Release APK (signed)
buildozer android release

# Deploy to device
buildozer android deploy run

# View logs
buildozer android logcat

# List connected devices
adb devices

# Install APK manually
adb install bin/yourapp.apk

# Uninstall
adb uninstall com.pongai.pongaiv2
```

## 🎯 Expected Results

**First build**: 30-60 minutes (downloads SDK/NDK/dependencies)
**Subsequent builds**: 5-10 minutes
**APK size**: ~30-50 MB (includes Python interpreter + libraries)

---

**Note**: Building for iOS requires macOS and is more complex. Consider alternative approaches for iOS deployment.
