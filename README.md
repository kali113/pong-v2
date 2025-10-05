# 🎮 Pong AI V2 - Incredible Neon Edition ✨

**Completely vibe coded with Claude Sonnet 4.5 in Copilot Chat with agent mode and TaskSync V5 from user 4regab.**

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## ✨ Features

- **🤖 Smart AI** - 3 difficulty levels (Easy/Medium/Hard)
- **🎨 Neon Effects** - Particles, glows, screen shake, gradient backgrounds
- **🌍 Bilingual** - English/Spanish UI toggle
- **⚙️ Settings** - Fullscreen, audio, language persistence
- **🖱️ Controls** - Mouse drag or W/S keyboard
- **🔊 Audio** - Procedural sound synthesis

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/kali113/pong-v2.git
cd pong-v2

# Install
pip install -r requirements.txt

# Run
python main.py
```

## 🕹️ Controls

- **W/S** or **↑/↓** - Move paddle
- **Mouse drag** - Direct control
- **ESC** - Settings
- **Space/Enter** - Start/Restart

## 📦 Requirements

- Python 3.10+
- pygame >= 2.6.0
- numpy >= 1.24.0

## 🏗️ Build

```bash
# Windows .exe
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico --name="PongAI-Neon" main.py

# Android APK (Linux/WSL)
pip install buildozer
buildozer android debug
```

## 🐛 Troubleshooting

**No sound?** Check Settings → Audio toggle

**Low FPS?** Disable debug HUD in settings

**Won't start?** Reinstall: `pip install -r requirements.txt --force-reinstall`

**More help:** Run in-game diagnostics from main menu

## 📁 Project

- `main.py` - 3,047 lines, fully EN/ES documented
- `icon.ico` - 32x32 window icon
- 1,200+ lines of bilingual comments
- 50+ fixed exceptions

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

1. Fork → Clone → Branch
2. Bilingual comments (EN/ES)
3. Test thoroughly
4. PR with `feat:`/`fix:`/`docs:` prefix

See CONTRIBUTING.md

## 🌟 Support

⭐ Star the repo | 🐛 Report bugs | ✨ Request features

---

**Made with ❤️ and lots of ☕**
