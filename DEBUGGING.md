# Debugging Guide for Pong AI V2
# Guía de Depuración para Pong AI V2

This document provides comprehensive debugging information for Pong AI V2.
Este documento proporciona información completa de depuración para Pong AI V2.

## Table of Contents / Tabla de Contenido

1. [Quick Start](#quick-start)
2. [Test Suite](#test-suite)
3. [Debug Configuration](#debug-configuration)
4. [Common Issues](#common-issues)
5. [Performance Profiling](#performance-profiling)
6. [Network Debugging](#network-debugging)
7. [Web Version Debugging](#web-version-debugging)

---

## Quick Start

### Running Tests / Ejecutar Pruebas

```bash
# Run comprehensive test suite
python test_suite.py

# Output shows pass/fail for each component
# La salida muestra pass/fail para cada componente
```

### Enable Debug Mode / Habilitar Modo Debug

In Python:
```python
from debug_config import enable_debug
enable_debug()
```

In game:
- Press `F3` to toggle debug HUD
- Press `F12` to run diagnostics
- Presiona `F3` para alternar HUD de depuración
- Presiona `F12` para ejecutar diagnósticos

---

## Test Suite

### Automated Testing / Pruebas Automatizadas

The `test_suite.py` file provides comprehensive testing:

#### Test Categories:
1. **Module Imports** - Verify all dependencies load correctly
2. **Constants** - Check all game constants are defined
3. **Classes** - Test class instantiation
4. **Functions** - Validate utility functions
5. **Game Logic** - Test ball, paddle, collision detection
6. **Translations** - Verify bilingual support
7. **Network Classes** - Test multiplayer components
8. **File Structure** - Ensure all required files exist

#### Running Tests:

```bash
# Run all tests
python test_suite.py

# Expected output:
# ✓ ALL TESTS PASSED!
# Total: 34, Passed: 34 (100.0%)
```

#### Adding New Tests:

```python
def test_your_feature(results: TestResults):
    """Test your new feature"""
    try:
        # Your test code here
        result = your_function()
        if result == expected:
            results.add_pass("Your Test", "Test passed")
        else:
            results.add_fail("Your Test", f"Expected {expected}, got {result}")
    except Exception as e:
        results.add_fail("Your Test", str(e))
```

---

## Debug Configuration

### Debug Config System / Sistema de Configuración de Debug

The `debug_config.py` module provides:

#### Debug Levels:
- `NONE` (0) - No debug output
- `ERROR` (1) - Only errors
- `WARNING` (2) - Errors and warnings
- `INFO` (3) - General information
- `DEBUG` (4) - Detailed debug info
- `TRACE` (5) - Everything including traces

#### Using the Logger:

```python
from debug_config import log_debug, log_info, log_warning, log_error

log_info("Game starting...")
log_debug(f"Ball position: {ball.x}, {ball.y}")
log_warning("High particle count detected")
log_error("Failed to connect", exception=e)
```

#### Performance Profiler:

```python
from debug_config import PERFORMANCE_PROFILER

# Track frame time
PERFORMANCE_PROFILER.add_frame_time(dt)

# Update metrics
PERFORMANCE_PROFILER.update_metric('particle_count', len(particles))

# Get all metrics
metrics = PERFORMANCE_PROFILER.get_metrics()
print(f"FPS: {metrics['fps']:.1f}")
```

#### Error Tracker:

```python
from debug_config import ERROR_TRACKER

# Record errors
ERROR_TRACKER.add_error("NetworkError", "Connection timeout", "Multiplayer")

# Get error summary
summary = ERROR_TRACKER.get_error_summary()
print(f"Total errors: {summary['total_errors']}")
```

---

## Common Issues

### Issue: Game Won't Start

**Symptom:** Black screen or immediate crash

**Solutions:**
1. Check dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Verify Python version:
   ```bash
   python --version  # Should be 3.10+
   ```

3. Test imports:
   ```bash
   python -c "import pygame; import numpy; print('OK')"
   ```

### Issue: Audio Not Working

**Symptom:** No sound effects

**Solutions:**
1. Check audio driver:
   ```python
   import pygame
   pygame.mixer.init()
   print(pygame.mixer.get_init())
   ```

2. Toggle audio in settings (press Settings → Audio)

3. Check system audio output is not muted

### Issue: Poor Performance / FPS Drops

**Symptom:** Game runs slowly, frame rate < 60 FPS

**Solutions:**
1. Enable debug HUD (press `F3`) to see actual FPS

2. Reduce particle count:
   ```python
   # In main.py, reduce PARTICLE_COUNT
   PARTICLE_COUNT = 30  # Instead of 60
   ```

3. Disable visual effects temporarily to isolate issue

4. Check CPU/GPU usage in system monitor

### Issue: Multiplayer Connection Failed

**Symptom:** "Connection failed" error when trying to join

**Solutions:**
1. Check firewall settings (allow port 5555)

2. Verify both players on same network:
   ```bash
   ping <host_ip_address>
   ```

3. Try direct IP connection instead of matchmaking

4. Check network logs:
   ```python
   from debug_config import enable_debug
   enable_debug()
   # Try connecting again
   ```

### Issue: Web Version Not Loading

**Symptom:** Blank page or errors in browser

**Solutions:**
1. Check browser console (F12) for errors

2. Verify files are in correct location:
   - `docs/game/index.html`
   - `docs/game/pong.ai.v2.apk`

3. Use modern browser (Chrome 90+, Firefox 88+)

4. Clear browser cache and reload

---

## Performance Profiling

### Built-in Diagnostics

Press `F12` or select "Diagnostics" from menu to run comprehensive system tests:

#### Tests Performed:
- Render pipeline check
- Audio synthesis validation
- Collision detection accuracy
- Particle system performance
- Network capabilities
- AI computation speed
- Blend mode support

#### Interpreting Results:

```
✓ PASS - Component works correctly
⚠ WARN - Component works but with issues
✗ FAIL - Component has critical error
```

### Custom Profiling

Add profiling to your code:

```python
import time

start = time.perf_counter()
# Your code here
elapsed = time.perf_counter() - start
print(f"Operation took {elapsed*1000:.2f}ms")
```

### Frame Time Analysis

Enable debug HUD (F3) to see:
- **FPS** - Frames per second (target: 60)
- **Frame Time** - Time per frame in ms (target: <16ms)
- **Particle Count** - Active particles
- **Network Latency** - Ping time (multiplayer only)

---

## Network Debugging

### Local Network Testing

1. Start host:
   ```bash
   # Terminal 1
   python main.py
   # Select "Multiplayer" → "Host Game"
   ```

2. Connect client:
   ```bash
   # Terminal 2
   python main.py
   # Select "Multiplayer" → "Join Private Game"
   # Enter the 6-digit code shown on host
   ```

### Network Logs

Enable detailed network logging:

```python
from debug_config import DEBUG_CONFIG, log_debug

# Enable trace level for network debugging
DEBUG_CONFIG.level = 5  # TRACE

# Now network operations will be logged
```

### Port Forwarding (Internet Play)

If hosting over internet:

1. Forward port 5555 (TCP) on router
2. Get external IP: https://whatismyipaddress.com/
3. Share external IP + port 5555 with client
4. Client connects using: `<external_ip>:5555`

**Security Note:** Only play with trusted players when using port forwarding.

---

## Web Version Debugging

### Browser Console

1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for failed requests

### Common Web Issues

#### Issue: Controls Not Working

**Solution:** Click on game canvas to focus it

#### Issue: Slow Performance

**Solutions:**
- Use Chrome/Firefox (best WebAssembly support)
- Close other browser tabs
- Disable browser extensions
- Check hardware acceleration is enabled

#### Issue: Multiplayer Disabled

**Note:** Multiplayer is intentionally disabled in web version (no WebSocket support in current build)

### Web-Specific Logs

```javascript
// In browser console
python.config.debug = true;  // Enable debug mode
```

---

## Debug Utilities

### Verify Installation

```bash
python -c "
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import main
print('✓ Version:', main.__version__)
print('✓ Web mode:', main.IS_WEB)
print('✓ Screen:', f'{main.SCREEN_WIDTH}x{main.SCREEN_HEIGHT}')
"
```

### Check All Components

```bash
python test_suite.py
```

### Syntax Check

```bash
python -m py_compile main.py main_web.py
```

### Code Quality Check (if available)

```bash
# Install linters (optional)
pip install flake8 pylint

# Run checks
flake8 main.py --max-line-length=120
pylint main.py --max-line-length=120
```

---

## Troubleshooting Checklist

When encountering issues, check:

- [ ] Python 3.10+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] No syntax errors (`python -m py_compile main.py`)
- [ ] Test suite passes (`python test_suite.py`)
- [ ] Display driver available (or set dummy for headless)
- [ ] Audio driver available (or set dummy for headless)
- [ ] Firewall allows port 5555 (for multiplayer)
- [ ] No conflicting processes on port 5555
- [ ] Sufficient disk space for settings file
- [ ] Write permissions in home directory

---

## Getting Help

If issues persist:

1. **Check existing issues:** Look for similar problems in GitHub issues
2. **Run diagnostics:** Press F12 in game or run `python test_suite.py`
3. **Collect information:**
   - Python version (`python --version`)
   - OS and version
   - Error messages (full traceback)
   - Test suite output
   - Debug logs (if enabled)

4. **Create detailed issue report with:**
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - System information
   - Debug output

---

## Debug Keyboard Shortcuts

In-game shortcuts for debugging:

- `F3` - Toggle performance HUD
- `F12` - Run diagnostics
- `ESC` - Return to menu / Cancel operation
- `Ctrl+Q` - Quick exit (emergency)

---

## Advanced Debugging

### Enabling Maximum Debug Output

```python
from debug_config import DEBUG_CONFIG, DEBUG_LOGGER

# Maximum verbosity
DEBUG_CONFIG.enable_full_debug()
DEBUG_CONFIG.log_to_file = True
DEBUG_CONFIG.show_collision_boxes = True
DEBUG_CONFIG.show_ai_target = True
DEBUG_CONFIG.show_particle_count = True
DEBUG_CONFIG.show_network_stats = True

# Now run your code
```

### Creating Debug Builds

For detailed debugging, create a debug build:

```bash
# Set environment variables for verbose output
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
export PYTHONVERBOSE=1
export PYGAME_DEBUG=1

python main.py
```

### Memory Profiling (Advanced)

```python
import tracemalloc

# Start tracking
tracemalloc.start()

# Run your code
game = Game()

# Check memory usage
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory: {peak / 1024 / 1024:.1f} MB")

tracemalloc.stop()
```

---

## Conclusion

This debugging guide should help you identify and resolve most issues with Pong AI V2. For additional help, consult the main README.md or open an issue on GitHub.

Esta guía de depuración debería ayudarte a identificar y resolver la mayoría de los problemas con Pong AI V2. Para ayuda adicional, consulta el README.md principal o abre un issue en GitHub.

**Happy Debugging! / ¡Feliz Depuración!** 🎮🐛
