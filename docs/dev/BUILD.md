# Build Instructions

## Windows EXE (One-Click)

### Requirements
- Windows 10/11
- Python 3.10+ installed from [python.org](https://www.python.org/downloads/)

### Build Steps
1. Open PowerShell in project folder
2. Run: `.\build-exe.ps1`
3. Wait 2-5 minutes
4. Find executable in `dist\PongAI-Neon.exe`

**That's it!** The script handles everything automatically.

---

## Android APK (One-Click)

### Requirements
- Linux or WSL2 (Windows Subsystem for Linux)
- 10+ GB free space
- Good internet connection (first build downloads 1-2 GB)

### Build Steps
1. Open terminal in project folder
2. Run: `chmod +x build-apk.sh && ./build-apk.sh`
3. Wait 10-30 minutes (first time only, future builds are faster)
4. Find APK in `bin/*.apk`

**That's it!** The script handles all dependencies automatically.

---

## Troubleshooting

### Windows EXE
**"Python not found"**
- Install Python from [python.org](https://www.python.org/downloads/)
- Check "Add to PATH" during installation

**"Build failed"**
- Close the game if it's running
- Delete `build` and `dist` folders
- Run script again

### Android APK
**"This script requires Linux or WSL"**
- Windows users: Install WSL2 with Ubuntu
- Guide: https://docs.microsoft.com/en-us/windows/wsl/install

**"Build failed" or "Download error"**
- Ensure 10+ GB free space
- Check internet connection
- Run: `buildozer android clean` then try again

**First build takes forever**
- Normal! First build downloads Android SDK/NDK (1-2 GB)
- Future builds take only 2-5 minutes
- Grab a coffee! ☕

---

## Manual Build (Advanced)

### Windows EXE (Manual)
```powershell
pip install pyinstaller pygame numpy
pyinstaller --onefile --windowed --icon=icon.ico --name="PongAI-Neon" main.py
```

### Android APK (Manual)
```bash
sudo apt install python3-pip openjdk-17-jdk
pip3 install buildozer cython
buildozer init
buildozer android debug
```

---

## File Sizes
- **Windows EXE**: ~25-35 MB (includes Python + all libraries)
- **Android APK**: ~20-30 MB (includes all dependencies)

Both are standalone and don't require Python or any other installations!
