# 🎮 Pong AI V2 - Incredible Neon Edition ✨

**Completely vibe coded with Claude Sonnet 4.5 in Copilot Chat with agent mode and TaskSync V5 from user 4regab.**

![Version](https://img.shields.io/badge/version-1.0.0--pre--alpha-blue.svg)
![Status](https://img.shields.io/badge/status-pre--alpha-yellow.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Web-lightgrey.svg)

> A modern, feature-rich Pong game with AI opponents, power-ups, particle effects, and full bilingual support (EN/ES)
> 
> Un juego moderno de Pong rico en características con oponentes IA, power-ups, efectos de partículas y soporte bilingüe completo (EN/ES)

---

## ✨ Features / Características

### 🎮 Core Gameplay / Juego Principal
- **🤖 Smart AI** - 3 difficulty levels: Easy/Medium/Hard
- **🎯 Precise Controls** - Mouse drag or keyboard (W/S, Arrow keys)
- **👥 2-Player Local Mode** - Play with a friend on the same keyboard
- **⚡ Power-Ups System** - 6 collectible bonuses that change gameplay

### 💫 Visual Effects / Efectos Visuales
- **🎨 Neon Aesthetic** - Dynamic glows, particles, and screen shake
- **✨ Particle System** - Optimized particle pooling (~10x performance)
- **🌈 Score Bursts** - Expanding ring effects when scoring
- **📈 Ball Trail** - Motion blur effect on ball

### 🌍 Localization / Localización
- **🇬🇧🇪🇸 Bilingual UI** - Complete English/Spanish translation system
- **📝 Bilingual Code** - 1,200+ lines of EN/ES comments throughout codebase
- **🔄 Language Toggle** - Switch languages in settings menu

### ⚙️ Settings & Features / Configuración y Características
- **💾 Persistent Settings** - JSON-based settings storage
- **🔊 Audio System** - Procedural sound synthesis (toggle on/off)
- **🪟 Display Options** - Fullscreen toggle, custom window icon
- **📊 Performance HUD** - Debug overlay with FPS and metrics
- **🛠️ Diagnostics** - Built-in system tests with detailed results

---

## 🎯 Power-Ups System / Sistema de Power-Ups

| Icon | Name | Effect (EN) | Efecto (ES) | Duration |
|------|------|-------------|-------------|----------|
| 🟦 | **Big Paddle** | +50% paddle size | +50% tamaño de paleta | 10s |
| 🔴 | **Multi-Ball** | Splits into 2-3 balls | Divide en 2-3 bolas | Until scored |
| ⚡ | **Speed Boost** | +50% ball speed | +50% velocidad de bola | 10s |
| 🛡️ | **Shield** | Blocks next point loss | Bloquea próxima pérdida | 1 use |
| 🎯 | **Slow Motion** | -50% ball speed | -50% velocidad de bola | 10s |
| 🌀 | **Chaos Ball** | Erratic bouncing | Rebotes erráticos | 15s |

---

## 🚀 Quick Start / Inicio Rápido

### Windows (One-Click) / Windows (Un Clic)

```batch
RUN.bat
```

### Linux/Mac

```bash
chmod +x run.sh
./run.sh
```

### Manual Installation / Instalación Manual

```bash
# Clone repository / Clonar repositorio
git clone https://github.com/kali113/pong-v2.git
cd pong-v2

# Create virtual environment / Crear entorno virtual
python -m venv .venv

# Activate (Windows) / Activar (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac) / Activar (Linux/Mac)
source .venv/bin/activate

# Install dependencies / Instalar dependencias
pip install -r requirements.txt

# Run game / Ejecutar juego
python main.py
```

---

## 🕹️ Controls / Controles

### Single Player / Un Jugador
- **W/S** or **↑/↓** - Move paddle / Mover paleta
- **Mouse drag** - Direct paddle control / Control directo de paleta
- **Space/Enter** - Start game / Iniciar juego
- **ESC** - Open settings / Abrir configuración

### 2-Player Mode / Modo 2 Jugadores
- **Player 1 / Jugador 1**: W/S keys
- **Player 2 / Jugador 2**: Arrow keys (↑/↓)

### Global Shortcuts / Atajos Globales
- **F11** - Toggle fullscreen / Alternar pantalla completa
- **M** - Toggle audio / Alternar audio
- **ESC** - Pause/Settings / Pausa/Configuración

---

## 📦 Requirements / Requisitos

### System Requirements / Requisitos del Sistema
- **Python**: 3.10 or higher / 3.10 o superior
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **RAM**: 512 MB minimum / 512 MB mínimo
- **Display**: 800x600 minimum resolution / Resolución mínima 800x600

### Python Dependencies / Dependencias Python
```
pygame>=2.6.0      # Graphics engine / Motor gráfico
numpy>=1.24.0      # Math operations / Operaciones matemáticas
Pillow>=10.0.0     # Icon generation / Generación de íconos (opcional)
```

---

## 🏗️ Build Standalone Executables / Compilar Ejecutables

### Windows EXE
```powershell
.\build-exe.ps1
```
**Output**: `dist/Pong_AI_V2.exe` (~15-20 MB)

**Time**: 2-5 minutes / minutos

### Android APK (Experimental)
```bash
chmod +x build-apk.sh
./build-apk.sh
```
**Requirements**: 
- Buildozer
- Android SDK/NDK
- Linux/macOS (Windows via WSL)

**Time**: 10-30 minutes first build / Primera compilación: 10-30 minutos

---

## 🌐 Web Version / Versión Web

The game supports web deployment via Pygbag:

```bash
# Install Pygbag
pip install pygbag

# Build web version
python -m pygbag main_web.py

# Serve locally (http://localhost:8000)
python -m http.server -d build/web
```

**Live Demo**: [Coming soon / Próximamente]

---

## 📁 Project Structure / Estructura del Proyecto

```
pong-v2/
├── main.py                 # Main game (3,730+ lines) / Juego principal
├── main_web.py             # Web version wrapper / Wrapper versión web
├── requirements.txt        # Python dependencies / Dependencias Python
├── icon.ico               # Window icon / Ícono de ventana
├── RUN.bat                # Windows launcher / Lanzador Windows
├── run.sh                 # Linux/Mac launcher / Lanzador Linux/Mac
├── build-exe.ps1          # Windows build script / Script compilación Windows
├── build-apk.sh           # Android build script / Script compilación Android
├── BUILD-WINDOWS.bat      # Alternative Windows builder / Compilador alternativo
├── build/
│   ├── version.txt        # Current version / Versión actual
│   └── web/               # Web build output / Salida compilación web
├── docs/
│   ├── README.md          # Detailed documentation / Documentación detallada
│   ├── CHANGELOG.md       # Version history / Historial de versiones
│   ├── SECURITY.md        # Security policy / Política de seguridad
│   ├── dev/               # Developer docs / Docs desarrollador
│   │   ├── BUILD.md
│   │   ├── CONTRIBUTING.md
│   │   └── MANUAL_SETUP.md
│   └── guides/            # Feature guides / Guías de características
│       ├── MEGA_UPGRADE_PLAN.md
│       ├── PHASE2_POWERUPS.md
│       └── PHASE2B_LOCAL_2PLAYER.md
└── .github/
    ├── copilot-instructions.md  # AI instructions / Instrucciones IA
    └── workflows/               # CI/CD pipelines

```

---

## 🐛 Troubleshooting / Solución de Problemas

### Common Issues / Problemas Comunes

#### ❌ **No sound / Sin sonido**
✅ **Solution / Solución**: Check Settings → Audio toggle or press **M**

#### ❌ **Low FPS / FPS bajo**
✅ **Solution / Solución**: 
- Disable debug HUD in settings
- Close other applications
- Update graphics drivers / Actualizar drivers gráficos

#### ❌ **Game won't start / El juego no inicia**
✅ **Solution / Solución**: 
```bash
pip install -r requirements.txt --force-reinstall
```

#### ❌ **Import errors / Errores de importación**
✅ **Solution / Solución**: 
- Ensure Python 3.10+ installed / Asegurar Python 3.10+
- Verify virtual environment activated / Verificar entorno virtual activado
- Reinstall dependencies / Reinstalar dependencias

### More Help / Más Ayuda
- **In-Game Diagnostics**: Main Menu → Run Diagnostics
- **GitHub Issues**: [Report a bug / Reportar error](https://github.com/kali113/pong-v2/issues)
- **Documentation**: See `/docs` folder

---

## 📊 Code Metrics / Métricas del Código

| Metric | Value |
|--------|-------|
| **Total Lines** | 3,730+ |
| **Documentation Lines** | 1,200+ (32%) |
| **Code Lines** | 2,530+ |
| **Classes** | 12 |
| **Methods** | 60+ |
| **Functions** | 20+ |
| **Languages** | Python, Markdown, PowerShell, Bash |
| **Documentation Coverage** | 85%+ |
| **Exception Handling** | 50+ specific catches |

---

## 🤝 Contributing / Contribuir

We welcome contributions! / ¡Bienvenidas las contribuciones!

1. **Fork** the repository / Hacer fork del repositorio
2. **Create** a feature branch / Crear rama de característica
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Add** bilingual comments (EN/ES) / Agregar comentarios bilingües
4. **Test** thoroughly / Probar exhaustivamente
5. **Commit** with conventional commits / Commit con commits convencionales
   ```bash
   git commit -m "feat: add amazing feature"
   ```
6. **Push** to branch / Enviar a rama
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open** a Pull Request / Abrir Pull Request

### Commit Conventions / Convenciones de Commit
- `feat:` - New feature / Nueva característica
- `fix:` - Bug fix / Corrección de error
- `docs:` - Documentation / Documentación
- `refactor:` - Code refactoring / Refactorización
- `test:` - Tests / Pruebas
- `chore:` - Maintenance / Mantenimiento

See [CONTRIBUTING.md](docs/dev/CONTRIBUTING.md) for detailed guidelines.

---

## 📝 License / Licencia

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## 🌟 Acknowledgments / Agradecimientos

- **Created with**: Claude Sonnet 4.5 (Anthropic)
- **Method**: "Vibe coding" with AI assistance
- **TaskSync V5**: By user [4regab](https://github.com/4regab)
- **Inspiration**: Classic Pong (Atari, 1972)
- **Community**: Thanks to all contributors / Gracias a todos los contribuidores

---

## 📈 Roadmap / Hoja de Ruta

### Current Version: 1.0.0-pre-alpha

- ✅ Phase 1: Web Conversion
- ✅ Phase 2A: Power-Ups System
- ✅ Phase 2B: Local 2-Player Mode
- ⏳ Phase 2C: New Game Modes (Tournament, Time Attack, Survival)
- 📋 Phase 3: Enhanced AI with adaptive difficulty
- 📋 Phase 4: Achievement System
- 📋 Phase 5: Statistics Tracking
- 📋 Phase 6: Online Leaderboards
- 📋 Version 1.0.0: Stable release

---

## 🆘 Support / Soporte

- **⭐ Star** this repository / Marca con estrella este repositorio
- **🐛 Report** bugs / Reporta errores
- **✨ Request** features / Solicita características
- **📖 Read** documentation / Lee la documentación
- **🤝 Contribute** code / Contribuye código

---

## 📞 Contact / Contacto

- **GitHub**: [@kali113](https://github.com/kali113)
- **Repository**: [pong-v2](https://github.com/kali113/pong-v2)
- **Issues**: [Bug Reports](https://github.com/kali113/pong-v2/issues)

---

<div align="center">

**Made with ❤️ and lots of ☕**

**Hecho con ❤️ y mucho ☕**

[⬆ Back to top / Volver arriba](#-pong-ai-v2---incredible-neon-edition-)

</div>
