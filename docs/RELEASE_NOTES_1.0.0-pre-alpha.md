# Pong AI V2 - Release Notes v1.0.0-pre-alpha

**Release Date**: October 6, 2025  
**Branch**: `feature/phase2-powerups`  
**Status**: Pre-Alpha (Testing Phase)

---

## 🎉 What's New in v1.0.0-pre-alpha

This pre-alpha release introduces **major gameplay enhancements** with power-ups, 2-player mode, and comprehensive documentation improvements.

---

## ⚡ Major Features

### 1. Power-Ups System (Phase 2A)
Collectible bonuses that spawn during gameplay, adding strategic depth and excitement.

**6 Power-Up Types**:
- 🟦 **Big Paddle** - Increases paddle size by 50% for 10 seconds
- 🔴 **Multi-Ball** - Splits the ball into 2-3 balls until scored
- ⚡ **Speed Boost** - Increases ball speed by 50% for 10 seconds
- 🛡️ **Shield** - Blocks the next point loss (1-time use)
- 🎯 **Slow Motion** - Decreases ball speed by 50% for 10 seconds
- 🌀 **Chaos Ball** - Makes ball bounce erratically for 15 seconds

**Features**:
- Weighted random spawning (every 12-18 seconds)
- Color-coded visual effects (pulsing glow animations)
- Collision detection for both paddles
- Active effects HUD in corner showing timers
- Particle effects on spawn and collection
- Dynamic sound synthesis (collection/expiration sounds)

### 2. Local 2-Player Mode (Phase 2B)
Play with a friend on the same keyboard!

**Controls**:
- **Player 1** (Left Paddle): W/S keys
- **Player 2** (Right Paddle): Arrow keys (↑/↓)

**Features**:
- Menu option to select 2-player mode
- Disables AI when 2-player mode is active
- Both players have full control of their paddles
- Shared score tracking

### 3. Web Version Support (Phase 1)
The game now runs in web browsers via Pygbag/WebAssembly!

**Features**:
- Dual-mode game loop (sync for desktop, async for web)
- Environment detection (`IS_WEB` flag)
- Network features disabled in web mode
- Browser event loop integration
- Full backward compatibility with desktop version

---

## 📝 Documentation Improvements

### New Documentation Structure
- **Root README.md** - Comprehensive 450+ line guide (EN/ES bilingual)
- **docs/** - Organized documentation folder
  - `docs/README.md` - Detailed game documentation
  - `docs/CHANGELOG.md` - Version history
  - `docs/SECURITY.md` - Security policy
  - `docs/dev/` - Developer guides (BUILD, CONTRIBUTING, MANUAL_SETUP)
  - `docs/guides/` - Feature implementation plans

### Updated Documentation
- **CHANGELOG.md** - Added v1.0.0-pre-alpha section with all changes
- **Version Consistency** - Updated across all files (main.py, main_web.py, build/version.txt)
- **Bilingual Comments** - Ensured 85%+ coverage throughout codebase

---

## 🔧 Technical Improvements

### Code Architecture
- **Dual-Mode Game Loop** - `_run_sync()` for desktop, `run_async()` for web
- **PowerUp Dataclass** - Type-safe power-up representation
- **Multi-Ball System** - List-based ball management for dynamic gameplay
- **Active Effects Tracking** - Dictionary-based effect timer management

### Performance
- **Particle Pooling** - Reuses particle objects for better performance
- **Optimized Rendering** - Cached surfaces for backgrounds and effects

### Code Quality
- **Type Hints** - Added to key functions and classes
- **Error Handling** - 50+ specific exception catches
- **Documentation Coverage** - 85%+ with bilingual comments (EN/ES)

---

## 🐛 Bug Fixes

- **Multi-Ball Score Logic** - Shield now correctly blocks scoring for all balls
- **2-Player Control Conflicts** - Separate input handling for both players
- **Power-Up Collision Detection** - Improved hitbox accuracy
- **Version Consistency** - Aligned version numbers across all files

---

## 📊 Code Metrics

| Metric | Value | Change from v1.0.0-alpha |
|--------|-------|--------------------------|
| Total Lines (main.py) | 3,730+ | +683 lines (+22%) |
| Documentation Lines | 1,300+ | +100 lines |
| Code Lines | 2,430+ | +583 lines |
| Classes | 12 | +4 classes |
| Methods | 65+ | +15 methods |
| Functions | 22+ | +7 functions |
| Power-Up Types | 6 | New feature |
| Game Modes | 2 | +1 mode (2-player) |
| Documentation Coverage | 85%+ | +5% |

---

## 🎮 How to Use New Features

### Power-Ups
1. Start a game (single or 2-player mode)
2. Power-ups will spawn randomly during gameplay (every 12-18 seconds)
3. Move your paddle to collect them
4. Active effects are shown in the top-right corner with timers
5. Effects automatically expire after their duration

### 2-Player Mode
1. From the main menu, click "🎮 2 PLAYER" button
2. Player 1 uses W/S keys (left paddle)
3. Player 2 uses Arrow keys (right paddle)
4. Play until one player reaches 7 points

### Web Version
1. Build: `python -m pygbag main_web.py`
2. Serve: `python -m http.server -d build/web`
3. Open browser to `http://localhost:8000`
4. Note: Multiplayer networking disabled in web version

---

## 📦 Installation & Upgrade

### New Installation
```bash
git clone https://github.com/kali113/pong-v2.git
cd pong-v2
pip install -r requirements.txt
python main.py
```

### Upgrading from v1.0.0-alpha
```bash
git pull origin feature/phase2-powerups
pip install -r requirements.txt --upgrade
python main.py
```

**Note**: Settings are fully backward compatible. Your saved preferences will be preserved.

---

## ⚠️ Known Issues

1. **Web Version Multiplayer** - Network features (host/join games) are disabled in web version due to WebSocket limitations in browsers.

2. **Multi-Ball Performance** - With many power-ups active simultaneously, particle effects may cause slight FPS drops on older hardware. This will be optimized in future releases.

3. **Phase 2C Not Implemented** - New game modes (Tournament, Time Attack, Survival, etc.) are planned but not yet implemented in this release.

---

## 🔮 Planned for Next Release (v1.0.0-beta)

### Phase 2C: New Game Modes (5-6 hours)
- **Tournament Mode** - Best of 3/5/7 with bracket display
- **Time Attack** - Score max points in 60 seconds
- **Survival Mode** - Ball gets faster every 10 seconds
- **Endless Mode** - No score limit, track high score
- **Practice Mode** - Ball doesn't score, just bounce

### Phase 3: Enhanced AI (4-5 hours)
- Adaptive difficulty that learns from player performance
- AI personality modes (Aggressive, Defensive, Balanced)
- Realistic reaction time simulation
- Mistake system based on difficulty

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](dev/CONTRIBUTING.md) for guidelines.

**How to Help**:
1. Test the game and report bugs
2. Suggest new power-ups or game modes
3. Improve documentation (especially translations)
4. Optimize performance
5. Add new features

---

## 📞 Support & Feedback

- **GitHub Issues**: [Report bugs or request features](https://github.com/kali113/pong-v2/issues)
- **Repository**: [github.com/kali113/pong-v2](https://github.com/kali113/pong-v2)
- **Branch**: `feature/phase2-powerups`

---

## 📜 Changelog Summary

```
v1.0.0-pre-alpha (2025-10-06)
├── feat: Power-Ups System (6 types with visual effects)
├── feat: Local 2-Player Mode (W/S and Arrow keys)
├── feat: Web version support with dual async/sync game loop
├── docs: Comprehensive documentation reorganization
├── docs: New root README.md (450+ lines, bilingual)
├── docs: Updated CHANGELOG.md with detailed version history
├── chore: Version update to 1.0.0-pre-alpha across all files
├── chore: Removed redundant backup files
├── fix: Multi-ball score logic with shield
├── fix: 2-player control conflicts
└── fix: Power-up collision detection accuracy
```

---

## 🙏 Acknowledgments

- **Created with**: Claude Sonnet 4.5 (Anthropic)
- **Method**: "Vibe coding" with AI assistance
- **TaskSync V5**: By user [4regab](https://github.com/4regab)
- **Inspiration**: Classic Pong (Atari, 1972)
- **Community**: Thanks to all testers and contributors!

---

## 📄 License

MIT License - See [LICENSE](../LICENSE) file for details.

---

<div align="center">

**Made with ❤️ and lots of ☕**

**Hecho con ❤️ y mucho ☕**

[⬆ Back to top](#pong-ai-v2---release-notes-v100-pre-alpha)

</div>
