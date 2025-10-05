# 🚀 QUICK START GUIDE

## For Complete Beginners

### Windows Users

**Option 1: Just Play** (Easiest)
1. Install Python from https://www.python.org/downloads/
   - Click "Add Python to PATH" during installation!
2. Double-click `RUN.bat`
3. Play!

**Option 2: Build Standalone EXE** (No Python needed to run)
1. Install Python from https://www.python.org/downloads/
2. Double-click `BUILD-WINDOWS.bat`
3. Wait 2-5 minutes
4. Run `dist\PongAI-Neon.exe`
5. Share the .exe with friends!

### Mac/Linux Users

**Option 1: Just Play**
```bash
chmod +x run.sh
./run.sh
```

**Option 2: Build APK for Android** (Requires Linux or WSL)
```bash
chmod +x build-apk.sh
./build-apk.sh
```

---

## Controls

- **W** or **↑** = Move paddle up
- **S** or **↓** = Move paddle down
- **Mouse** = Drag paddle OR click buttons
- **ESC** = Settings
- **Space/Enter** = Start/Restart

---

## Common Issues

**"Python not found"**
→ Install Python 3.10+ from python.org

**"Module not found"**
→ Run: `pip install -r requirements.txt`

**"Permission denied" (Linux/Mac)**
→ Run: `chmod +x run.sh` or `chmod +x build-apk.sh`

**Game runs but has no sound**
→ Check Settings menu → Enable Audio

**Game is laggy**
→ Settings → Disable Performance HUD
→ Close other apps

---

## Need Help?

- Read `BUILD.md` for detailed instructions
- Open an issue: https://github.com/kali113/pong-v2/issues
- Check troubleshooting in `BUILD.md`

---

## File Guide

| File | Purpose |
|------|---------|
| `RUN.bat` | Windows launcher |
| `run.sh` | Linux/Mac launcher |
| `BUILD-WINDOWS.bat` | Build Windows EXE |
| `build-exe.ps1` | EXE build script (PowerShell) |
| `build-apk.sh` | Build Android APK |
| `BUILD.md` | Detailed build instructions |
| `main.py` | The game (run with Python) |
| `requirements.txt` | Dependencies list |

---

**That's it! Double-click and play!** 🎮
