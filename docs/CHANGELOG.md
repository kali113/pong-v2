# Changelog

All notable changes to Pong AI V2 will be documented in this file.

**Versioning**: 
- Major releases: v1.0, v2.0, v3.0 (breaking changes or complete rewrites)
- Minor releases: v1.1, v1.2, v1.3 (new features, significant changes)
- Patch releases: v1.0.1, v1.0.2, v1.0.3 (bugfixes, small improvements)

## [1.0.0-pre-alpha] - 2025-10-06

### 🚀 Pre-Alpha Release - Power-Ups & 2-Player Mode

#### Added
- ⚡ **Power-Ups System** - 6 collectible bonuses with timed effects
  - 🟦 Big Paddle (+50% size for 10s)
  - 🔴 Multi-Ball (splits into 2-3 balls)
  - ⚡ Speed Boost (+50% ball speed for 10s)
  - 🛡️ Shield (blocks next point loss, 1 use)
  - 🎯 Slow Motion (-50% ball speed for 10s)
  - 🌀 Chaos Ball (erratic bouncing for 15s)
- 👥 **Local 2-Player Mode** - Play with friend on same keyboard
  - Player 1: W/S keys (left paddle)
  - Player 2: Arrow keys (right paddle)
  - Menu option to select 2-player mode
- 🎨 **Power-Up Visual Effects**
  - Pulsing glow animations
  - Color-coded power-ups (blue, red, yellow, green, purple)
  - Particle effects on spawn and collection
  - Active effects HUD in corner
- 🔊 **Dynamic Sound Synthesis**
  - Power-up collection sounds (rising arpeggio)
  - Power-up expiration sounds (descending tone)
  - Pitch variations based on events
- 🌐 **Web Version Support** - Dual-mode async/sync game loop
  - AsyncGameWrapper for Pygbag compatibility
  - Browser event loop integration
  - Network features disabled in web mode
- 📝 **Comprehensive Root README** - Complete bilingual documentation at project root
- 📁 **Organized Documentation Structure**
  - `docs/` folder with README, CHANGELOG, SECURITY
  - `docs/dev/` for developer guides
  - `docs/guides/` for feature implementation plans
  - `memory/` for session tracking

#### Fixed
- 🐛 **Multi-Ball Score Logic** - Shield now correctly blocks scoring
- 🔧 **2-Player Control Conflicts** - Separate input handling for both players
- 📝 **Version Consistency** - Aligned version numbers across all files
- 🎨 **Power-Up Collision Detection** - Improved hitbox accuracy
- ⚡ **Performance** - Optimized particle pooling for power-up effects

#### Changed
- 📏 **File Size** - main.py grew from 3,047 to 3,730+ lines
- 🏗️ **Game Loop Architecture** - Split into sync (_run_sync) and async (run_async) modes
- 🎮 **Game Modes** - Added game_mode variable ("single" / "2player")
- 📊 **Version Number** - Updated to 1.0.0-pre-alpha across all files
- 📖 **Documentation** - Moved docs to `/docs` folder for better organization

#### Technical Improvements
- 🔄 **Dual-Mode Game Loop** - Synchronous for desktop, async for web
- 🎯 **PowerUp Dataclass** - Type-safe power-up representation
- 📚 **Active Effects Tracking** - Dictionary-based effect timer management
- 🎨 **Multi-Ball System** - List-based ball management for dynamic gameplay
- 🔊 **Audio Synthesis Enhancement** - NumPy-based dynamic sound generation
- 🌐 **Environment Detection** - IS_WEB flag for platform-specific code paths

### Code Quality Metrics (Update)
- **Total Lines**: 3,730+ (was 3,047)
- **Documentation Lines**: ~1,300 (was ~1,200)
- **Code Lines**: ~2,430 (was ~1,800)
- **Classes**: 12 (added: PowerUp, AsyncGameWrapper)
- **Methods**: 65+ (was 50+)
- **Functions**: 22+ (was 15+)
- **Power-Up Types**: 6
- **Game Modes**: 2 (single, 2player)
- **Documentation Coverage**: 85%+

### Breaking Changes
None - Fully backward compatible with v1.0.0-alpha settings

### Known Issues
- 🐛 Web version multiplayer disabled (sockets not available in browser)
- ⚠️ Multi-ball can cause performance drops with too many particles
- 📝 Phase 2C (Game Modes) not yet implemented

---

## [1.0.0-alpha] - 2025-01-XX

### 🎉 Initial Alpha Release

#### Added
- ✨ **Comprehensive Bilingual Documentation** - 1,200+ lines of EN/ES comments throughout entire codebase
- 🎨 **Pixel Art Logo** - Custom "PONG V2" gradient title screen (light grey → white)
- 🪟 **Custom 32x32 Icon** - Colorful neon window icon with .ico file generation
- 🌍 **Full Bilingual UI** - Complete English/Spanish translation system
- 💾 **Settings Persistence** - JSON-based settings storage in user home directory
- 🎚️ **Language Toggle** - Switch between EN/ES in settings menu
- 🔊 **Audio Toggle** - Enable/disable sound effects in settings
- 🐛 **Debug HUD Toggle** - Performance metrics overlay in settings
- 📊 **Diagnostics System** - 10+ system tests with detailed results
- ⚙️ **Settings Menu** - Comprehensive configuration interface
- 🎮 **Difficulty Selector** - Visual difficulty picker with hover effects
- 💫 **Particle System** - Object pooling optimization (~10x performance improvement)
- 🌟 **Score Bursts** - Expanding ring effects when scoring
- 🎨 **Glow Effects** - Dynamic lighting on paddles and ball
- 📈 **Trail Effect** - Motion blur trail on ball
- 🖱️ **Mouse Controls** - Click and drag paddle control
- 🎹 **Keyboard Controls** - W/S and Arrow key support
- 📁 **Project Structure** - Organized single-file architecture with clear sections

#### Fixed
- 🐛 **50+ Exception Handling Fixes** - Replaced bare `except:` with specific exception types
  - `json.JSONDecodeError` for JSON parsing
  - `socket.error` for network operations
  - `OSError` for system operations
  - `ValueError` for invalid values
  - `TypeError` for type errors
  - `IOError` for file operations
  - `AttributeError` for missing attributes
- 🔧 **Import Organization** - Separated stdlib and third-party imports with comments
- 📝 **Code Quality** - Added docstrings to all functions and classes
- ⚡ **Performance** - Implemented particle object pooling for better FPS
- 🎨 **Icon Generation** - Fixed ball size in 32x32 icon (radius 4 → 2)
- 💬 **Comment Coverage** - Added bilingual inline comments throughout

#### Changed
- 📏 **File Size** - Grew from 1,780 to 3,047 lines (71% increase, mostly documentation)
- 🏗️ **Architecture** - Improved code organization with clear section markers
- 🎨 **Visual Style** - Enhanced neon aesthetic with better gradients
- 📦 **Dependencies** - Updated requirements.txt with version constraints
- 📖 **README** - Completely rewritten with comprehensive documentation

#### Technical Improvements
- 🔒 **Type Safety** - Immutable `GameSettings` dataclass with frozen=True
- 🎯 **Code Organization** - Clear section markers with ASCII art headers
- 📚 **Documentation Format** - Consistent EN/ES bilingual comment style
- 🔄 **State Management** - Clear state machine with documented transitions
- 🎨 **Procedural Graphics** - All visuals generated at runtime (zero assets)
- 🔊 **Audio Synthesis** - Real-time sine wave generation with NumPy
- 💾 **Settings Storage** - Robust JSON persistence with error handling
- 🌐 **Translation System** - Clean TRANSLATIONS dict with t() helper method

### Code Quality Metrics
- **Total Lines**: 3,047 (was 1,780)
- **Documentation Lines**: ~1,200 (new)
- **Code Lines**: ~1,800
- **Classes**: 8 (Game, Paddle, Ball, Particle, ParticlePool, ScoreBurst, etc.)
- **Methods**: 50+
- **Functions**: 15+
- **Exception Fixes**: 50+
- **Documentation Coverage**: 80-85%

### Breaking Changes
None - Fully backward compatible with saved settings

### Known Issues
None currently reported

---

## Future Releases

### Planned Features
- 🌐 Online multiplayer
- 🏆 Achievements
- 🎵 Music
- 📱 Mobile port
