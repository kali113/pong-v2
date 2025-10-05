# 🎮 Pong AI V2 - Incredible Neon Edition ✨

A stunning modern Pong remake with AI opponent, bilingual UI, comprehensive documentation, and beautiful neon aesthetics.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)

## 🌟 Latest Updates (v2.0.0)
- **✅ Comprehensive Bilingual Documentation** - 1,200+ lines of EN/ES comments
- **✅ Code Quality Improvements** - Fixed 50+ bare exceptions with specific error handling
- **✅ Pixel Art Logo** - Beautiful "PONG V2" gradient title screen
- **✅ Custom 32x32 Icon** - Colorful neon window icon (`.ico` file included)
- **✅ Settings Persistence** - Auto-save all preferences (fullscreen, audio, language, difficulty)
- **✅ Bilingual UI** - Full English/Spanish translation system
- **✅ Performance Optimized** - Object pooling for particles (~10x faster)

## � Features

### Core Gameplay
- **🤖 Smart AI Opponent** with 3 difficulty levels (Easy / Medium / Hard)
- **🖱️ Intuitive Controls** - Mouse drag or keyboard (W/S, Arrow keys)
- **⚡ Smooth 60 FPS** - Delta-time physics for consistent gameplay
- **🔊 Procedural Audio** - Real-time sound synthesis with NumPy

### 🎨 Visual Effects
- **✨ Neon Aesthetics** - Animated gradient backgrounds with parallax stars
- **💫 Particle System** - Explosion effects on collisions (object pooling optimization)
- **🌟 Glow Effects** - Dynamic lighting on paddles and ball
- **📈 Score Bursts** - Expanding ring effects when scoring
- **🎭 Screen Shake** - Impact feedback on paddle hits
- **🖼️ Pixel Art Logo** - Custom "PONG V2" title with gradient
- **🪟 Custom Icon** - 32x32 colorful window icon with .ico file

### 🌍 Internationalization
- **🇬🇧 English UI** - Complete interface translation
- **🇪🇸 Spanish UI** - Full UI en español
- **⚙️ Language Toggle** - Switch languages in settings menu
- **📚 Code Documentation** - All code commented in EN/ES

### ⚙️ Settings & Configuration
- **💾 Persistent Settings** - JSON-based preference storage
- **🖥️ Fullscreen Toggle** - Seamless mode switching
- **🔊 Audio Control** - Enable/disable sound effects
- **🐛 Debug HUD** - Performance metrics overlay
- **🎚️ Difficulty Selector** - Visual difficulty picker in menu

## 🕹️ Controls

### In-Game
| Key | Action |
|-----|--------|
| **W** / **↑** | Move paddle up |
| **S** / **↓** | Move paddle down |
| **Mouse Drag** | Direct paddle control |
| **ESC** | Open settings menu |
| **Space** / **Enter** | Start game / Restart |

### Menu Navigation
| Key | Action |
|-----|--------|
| **Mouse Click** | Select buttons |
| **↑** / **↓** | Change difficulty |
| **W** / **S** | Change difficulty |
| **Space** / **Enter** | Confirm selection |

## 📦 Installation

### Prerequisites
- **Python 3.10+** (Download from [python.org](https://www.python.org/downloads/))
- **pip** package manager (included with Python)
- **Git** (optional, for cloning)

### 🚀 Quick Start

#### Windows (PowerShell)
```powershell
# Clone repository
git clone https://github.com/yourusername/pong-ai-v2.git
cd pong-ai-v2

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

#### Linux/MacOS (Bash)
```bash
# Clone repository
git clone https://github.com/yourusername/pong-ai-v2.git
cd pong-ai-v2

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### 📥 Download Without Git
1. Download ZIP from GitHub (green "Code" button)
2. Extract to desired folder
3. Follow installation steps above (skip `git clone`)

## � How to Play

### Single Player Mode
1. Launch the game: `python main.py`
2. Select difficulty (Easy/Medium/Hard)
3. Press **SPACE** or **ENTER** to start
4. Use **W/S** or **mouse drag** to control your paddle
5. First to 7 points wins!

### Game Modes
- **🤖 VS AI** - Play against computer opponent
- **⚙️ Settings** - Configure fullscreen, audio, language, debug HUD
- **🔧 Diagnostics** - Run system tests and performance checks

## � Requirements

### Python Packages
| Package | Version | Purpose |
|---------|---------|---------|
| **pygame** | >= 2.6.0 | Graphics, input, audio engine |
| **numpy** | >= 1.24.0 | Mathematical operations, audio synthesis |
| **Pillow** | (optional) | Icon.ico file generation |

Install all: `pip install -r requirements.txt`

## 🏗️ Building Standalone Executable

### Windows (.exe)
Package as standalone executable for distribution:

```powershell
# Install PyInstaller
pip install pyinstaller

# Build single-file executable
pyinstaller --onefile --windowed --icon=icon.ico --name="PongAI-Neon" main.py

# Output: dist/PongAI-Neon.exe
```

### Advanced Build Options
```powershell
# Using build script (if available)
.\scripts\build_exe.ps1 -OneFile

# Manual with more options
pyinstaller --onefile --windowed --icon=icon.ico `
  --name="PongAI-Neon" `
  --add-data="icon.ico;." `
  main.py
```

### � Android APK (Experimental)
Building for Android requires additional setup:

1. **Install Buildozer** (Linux/WSL recommended):
```bash
pip install buildozer
```

2. **Create buildozer.spec** configuration file

3. **Build APK**:
```bash
buildozer android debug
```

> ⚠️ Note: Pygame on Android has limitations. Controller support required.

## 🧪 Testing

### Syntax Validation
```bash
# Check syntax errors
python -m py_compile main.py

# Run with verbose output
python -v main.py
```

### In-Game Diagnostics
1. Launch game: `python main.py`
2. Main Menu → **Run Diagnostics** button
3. View 10+ system tests with performance metrics

### Manual Testing
- Test all difficulty levels
- Test fullscreen toggle
- Test audio toggle
- Test language switching (EN/ES)
- Test settings persistence (restart game)

## 📁 Project Structure

```
pong-ai-v2/
├── main.py                      # Core game (3,000+ lines, fully documented EN/ES)
├── icon.ico                     # Window icon (32x32 colorful pong scene)
├── requirements.txt             # Python dependencies
├── README.md                    # This documentation
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore patterns
├── .github/
│   ├── copilot-instructions.md  # AI development guidelines
│   └── workflows/               # (Optional) CI/CD automation
├── scripts/
│   └── build_exe.ps1           # Windows executable build script
├── build/                       # Build artifacts (gitignored)
├── dist/                        # Distribution files (gitignored)
└── __pycache__/                 # Python cache (gitignored)
```

## �️ Architecture

### Core Design Philosophy
- **Single-file simplicity** - All game logic in `main.py` (3,000+ lines)
- **Zero external assets** - All graphics procedurally generated at runtime
- **Comprehensive documentation** - 1,200+ lines of bilingual (EN/ES) comments
- **Modern Python** - Type hints, dataclasses, f-strings, walrus operator

### Main Components

#### Game Class (`main.py`)
The heart of the application with 50+ methods:
- **State Management** - Menu, settings, diagnostics, playing, gameover
- **Game Loop** - 60 FPS with delta-time physics
- **Input Handling** - Keyboard, mouse (drag & click), events
- **Rendering Pipeline** - Layered surfaces, alpha blending, particle system
- **AI Logic** - Predictive movement with difficulty levels
- **Audio Synthesis** - Real-time sine wave generation with NumPy

#### Entity Classes
- **`Paddle`** - Player/AI paddles with glow effects
- **`Ball`** - Ball with trail and collision physics
- **`Particle`** - Lightweight particle with fade-out
- **`ParticlePool`** - Object pool for particle reuse (~10x performance)
- **`ScoreBurst`** - Expanding ring effect on scoring

#### Utility Systems
- **Translation System** - `TRANSLATIONS` dict + `t()` method
- **Settings Management** - JSON persistence in user home directory
- **Graphics Generation** - `create_window_icon()`, `create_title_logo()`
- **Audio Synthesis** - `create_sound()` with NumPy waveform generation

### Code Quality Features
- **✅ Specific Exception Handling** - 50+ fixed bare except clauses
- **✅ Organized Imports** - Stdlib/third-party separation with comments
- **✅ Comprehensive Docstrings** - Every function and class documented
- **✅ Bilingual Comments** - EN/ES inline comments throughout
- **✅ Type Safety** - Immutable `GameSettings` dataclass
- **✅ Performance Optimized** - Object pooling, cached backgrounds

## 🐛 Troubleshooting

### ❌ Game Won't Start

**Issue**: Import errors or missing modules
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify Python version (requires 3.10+)
python --version
```

**Issue**: "No module named 'pygame'"
```bash
# Solution: Activate virtual environment first
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Linux/MacOS
source .venv/bin/activate

# Then install
pip install pygame
```

### 🎮 Gameplay Issues

**Issue**: Low FPS or stuttering
- Close background applications (browsers, Discord, etc.)
- Update graphics drivers
- Disable debug HUD (Settings → Performance HUD → OFF)
- Check Task Manager for high CPU usage

**Issue**: Controls not responding
- Ensure window has focus (click on it)
- Try different control method (mouse vs keyboard)
- Check if ESC key is stuck (reopens settings menu)

### 🔊 Audio Problems

**Issue**: No sound effects
```python
# Check NumPy installation
python -c "import numpy; print(numpy.__version__)"

# Should output: 1.24.0 or higher
```

**Solution**: 
- Enable audio in Settings menu
- Check system volume mixer
- Verify audio devices are working

### 🖥️ Display Issues

**Issue**: Blurry text on high-DPI displays
- The game includes DPI awareness fix for Windows
- Try toggling fullscreen mode (Settings → Fullscreen)

**Issue**: Window too large/small
- Game uses fixed 800x600 resolution
- Use fullscreen mode for better fit

### 🪟 Windows-Specific

**Issue**: "VCRUNTIME140.dll is missing"
- Install Microsoft Visual C++ Redistributable
- Download from [Microsoft](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)

### 🐧 Linux-Specific

**Issue**: Pygame installation fails
```bash
# Install system dependencies first
sudo apt-get install python3-dev libsdl2-dev libsdl2-mixer-dev

# Then install pygame
pip install pygame
```

### 💾 Settings Not Saving

**Issue**: Settings reset every launch
- Check file permissions in home directory
- Settings file location: `~/.pong_ai_settings.json`
- Manually verify file exists and is writable

### 🔍 Getting Help

Still having issues?
1. Run in-game diagnostics: Main Menu → **Run Diagnostics**
2. Check Python and package versions: `pip list`
3. Open an issue on GitHub with diagnostic results
4. Include error messages and system info (OS, Python version)

## ⚙️ Advanced Configuration

All configuration is in `main.py`. Here are some customization options:

### 🎚️ Difficulty Settings
Edit the difficulty tuples (around line 1350):
```python
self.difficulties = [
    (300.0, 380.0),   # Easy:   (ai_speed, ball_speed)
    (380.0, 420.0),   # Medium: (ai_speed, ball_speed)  
    (460.0, 480.0),   # Hard:   (ai_speed, ball_speed)
]
```

### 🎨 Visual Customization
```python
# GameSettings dataclass (line ~690)
@dataclass(frozen=True)
class GameSettings:
    screen_width: int = 800        # Change window width
    screen_height: int = 600       # Change window height
    paddle_width: int = 12         # Change paddle width
    paddle_height: int = 110       # Change paddle height
    ball_size: int = 12            # Change ball size
    paddle_speed: float = 440.0    # Change paddle speed
    win_score: int = 7             # Change points to win
```

### 🎵 Audio Customization
```python
# Sound generation (line ~770)
bounce_sound = create_sound(440, 0.09, 0.6)  # (frequency_hz, duration_s, volume)
score_sound = create_sound(220, 0.22, 0.7)
paddle_sound = create_sound(660, 0.07, 0.5)
```

### 🌐 Translation System
Add new languages in `TRANSLATIONS` dict (line ~50):
```python
TRANSLATIONS = {
    'en': { 'title': 'Pong AI', ... },
    'es': { 'title': 'Pong IA', ... },
    'fr': { 'title': 'Pong IA', ... },  # Add French
}
```

### 💾 Settings File Location
Settings saved to: `~/.pong_ai_settings.json`
- Windows: `C:\Users\YourName\.pong_ai_settings.json`
- Linux/Mac: `/home/yourname/.pong_ai_settings.json`

## � Project Statistics

| Metric | Value |
|--------|-------|
| **Total Lines** | 3,047 |
| **Code Lines** | ~1,800 |
| **Documentation Lines** | ~1,200 |
| **Classes** | 8 (Game, Paddle, Ball, Particle, ParticlePool, ScoreBurst, etc.) |
| **Methods** | 50+ |
| **Functions** | 15+ |
| **Languages** | Python 3.10+ |
| **Dependencies** | 2 (pygame, numpy) |
| **Documentation** | EN/ES Bilingual |

## �📝 License

**MIT License**

Copyright (c) 2025 Pong AI V2 Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🙏 Credits & Acknowledgments

### Technologies
- **Python 3.10+** - Core language
- **Pygame 2.6+** - Graphics engine, input handling, audio system
- **NumPy 1.24+** - Mathematical operations, audio synthesis
- **Pillow** - Icon file generation (optional)

### Development
- **Comprehensive Documentation** - 1,200+ lines of bilingual comments
- **Code Quality** - 50+ exception handling improvements
- **Pixel Art** - Custom logo and icon design
- **Performance Optimization** - Object pooling for particle system

### Special Thanks
- Pygame community for excellent documentation
- NumPy developers for high-performance computing tools
- Beta testers for feedback and bug reports

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### 🐛 Bug Reports
1. Check existing issues on GitHub
2. Run in-game diagnostics (Diagnostic Test)
3. Include error messages and system info
4. Describe steps to reproduce

### ✨ Feature Requests
Ideas for improvement:
- 🌐 Online multiplayer (WebSocket-based)
- 👤 Player profiles and statistics
- 🏆 Achievements and unlockables
- 🎨 Theme customization
- 🎮 Game mode variations (power-ups, obstacles)
- 📱 Mobile port (Android/iOS)
- 🎵 Music tracks
- 🌍 More language translations

### � Code Contributions
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Follow existing code style (bilingual comments, docstrings)
4. Test thoroughly
5. Submit pull request with detailed description

### 📖 Documentation
- Improve README clarity
- Add tutorials or guides
- Translate to more languages
- Record video tutorials

## 📞 Support & Community

### Getting Help
1. **In-Game Diagnostics** - Run from main menu
2. **Troubleshooting Section** - Check above
3. **GitHub Issues** - [Open an issue](https://github.com/yourusername/pong-ai-v2/issues)
4. **Documentation** - Read all comments in `main.py`

### Stay Updated
- ⭐ Star the repository on GitHub
- 👀 Watch for updates
- 🔔 Enable notifications for releases

### Share Your Experience
- 📸 Share screenshots
- 🎥 Record gameplay videos
- ⭐ Leave a review
- 🔄 Fork and customize

## 🌟 Show Your Support

If you found this project helpful:
- ⭐ Star the repository
- 🍴 Fork and customize
- 📢 Share with friends
- 💬 Leave feedback
- 🐛 Report bugs
- ✨ Contribute improvements

---

<div align="center">

### 🎮 **Enjoy the game!** ✨

**Made with ❤️ and lots of ☕**

![Pong](https://img.shields.io/badge/Pong-AI%20V2-blue?style=for-the-badge&logo=gamepad)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-orange?style=for-the-badge)

[⬆ Back to Top](#-pong-ai-v2---incredible-neon-edition-)

</div>