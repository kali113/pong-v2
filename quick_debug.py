#!/usr/bin/env python3
"""
Quick Debug Script for Pong AI V2
Script de Depuración Rápida para Pong AI V2

Run this script for instant diagnosis of common issues.
Ejecuta este script para un diagnóstico instantáneo de problemas comunes.
"""

import sys
import os
from pathlib import Path

# Set headless mode / Establecer modo sin cabeza
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

def print_header(text):
    """Print section header / Imprimir encabezado de sección"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_python_version():
    """Check Python version / Verificar versión de Python"""
    print_header("PYTHON VERSION / VERSIÓN DE PYTHON")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("⚠ WARNING: Python 3.10+ recommended")
        print("⚠ ADVERTENCIA: Se recomienda Python 3.10+")
        return False
    else:
        print("✓ Python version OK")
        return True

def check_dependencies():
    """Check required dependencies / Verificar dependencias requeridas"""
    print_header("DEPENDENCIES / DEPENDENCIAS")
    
    deps = [
        ('pygame', 'pygame', True),
        ('numpy', 'numpy', True),
        ('PIL', 'Pillow', False),
    ]
    
    all_ok = True
    for module, package, required in deps:
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            status = "✓" if required else "⊙"
            print(f"{status} {package}: {version}")
        except ImportError:
            if required:
                print(f"✗ {package}: NOT INSTALLED (required)")
                all_ok = False
            else:
                print(f"⊙ {package}: not installed (optional)")
    
    return all_ok

def check_files():
    """Check required files exist / Verificar que existan archivos requeridos"""
    print_header("PROJECT FILES / ARCHIVOS DEL PROYECTO")
    
    files = [
        ('main.py', True),
        ('main_web.py', True),
        ('requirements.txt', True),
        ('debug_config.py', False),
        ('test_suite.py', False),
        ('README.md', True),
    ]
    
    all_ok = True
    for file, required in files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"✓ {file} ({size:,} bytes)")
        else:
            status = "✗" if required else "⊙"
            print(f"{status} {file}: not found")
            if required:
                all_ok = False
    
    return all_ok

def test_imports():
    """Test critical imports / Probar importaciones críticas"""
    print_header("IMPORT TEST / PRUEBA DE IMPORTACIÓN")
    
    try:
        import main
        print(f"✓ main.py imports successfully (v{main.__version__})")
        return True
    except Exception as e:
        print(f"✗ Failed to import main.py: {e}")
        return False

def test_basic_functionality():
    """Test basic game components / Probar componentes básicos del juego"""
    print_header("FUNCTIONALITY TEST / PRUEBA DE FUNCIONALIDAD")
    
    try:
        import main
        
        # Test settings
        settings = main.load_settings()
        print(f"✓ Settings system: {len(settings)} settings loaded")
        
        # Test particle pool
        pool = main.ParticlePool(10)
        p = pool.acquire()
        pool.release(p)
        print("✓ Particle system: OK")
        
        # Test ball
        ball = main.Ball()
        ball.move(0.016)
        print("✓ Ball physics: OK")
        
        # Test paddle
        paddle = main.Paddle(50, 300, (255, 255, 255))
        paddle.move(1.0, 0.016)
        print("✓ Paddle movement: OK")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_test_suite():
    """Run full test suite if available / Ejecutar suite completa si está disponible"""
    print_header("RUNNING TEST SUITE / EJECUTANDO SUITE DE PRUEBAS")
    
    if not Path('test_suite.py').exists():
        print("⊙ Test suite not found (optional)")
        return True
    
    try:
        import test_suite
        result = test_suite.run_all_tests()
        return result == 0
    except Exception as e:
        print(f"⚠ Test suite error: {e}")
        return False

def check_permissions():
    """Check file permissions / Verificar permisos de archivo"""
    print_header("PERMISSIONS / PERMISOS")
    
    # Check write permission in home directory
    settings_file = Path.home() / '.pong_ai_test_write'
    try:
        settings_file.write_text("test")
        settings_file.unlink()
        print("✓ Home directory writable")
        return True
    except Exception as e:
        print(f"✗ Cannot write to home directory: {e}")
        return False

def check_display():
    """Check display availability / Verificar disponibilidad de display"""
    print_header("DISPLAY / PANTALLA")
    
    # Already in headless mode for this script
    print("⊙ Running in headless mode for testing")
    
    try:
        import pygame
        # Try to get video info
        info = pygame.display.Info()
        print(f"✓ Display driver: {pygame.display.get_driver()}")
        return True
    except Exception as e:
        print(f"⚠ Display check: {e}")
        print("  (This is normal in headless environments)")
        return True

def provide_recommendations(results):
    """Provide recommendations based on results / Proporcionar recomendaciones basadas en resultados"""
    print_header("RECOMMENDATIONS / RECOMENDACIONES")
    
    failed_checks = [name for name, status in results.items() if not status]
    
    if not failed_checks:
        print("✓ ALL CHECKS PASSED!")
        print("✓ ¡TODAS LAS VERIFICACIONES PASARON!")
        print("\nYour installation appears to be working correctly.")
        print("Tu instalación parece estar funcionando correctamente.")
        print("\nYou can run the game with:")
        print("Puedes ejecutar el juego con:")
        print("  python main.py")
        return
    
    print("Some issues were detected. Here's what to do:")
    print("Se detectaron algunos problemas. Aquí está qué hacer:")
    print()
    
    if 'dependencies' in failed_checks:
        print("📦 DEPENDENCIES / DEPENDENCIAS:")
        print("   Install missing packages:")
        print("   Instalar paquetes faltantes:")
        print("   pip install -r requirements.txt")
        print()
    
    if 'python_version' in failed_checks:
        print("🐍 PYTHON VERSION / VERSIÓN DE PYTHON:")
        print("   Update to Python 3.10 or newer")
        print("   Actualizar a Python 3.10 o más nuevo")
        print("   Download from: https://www.python.org/downloads/")
        print()
    
    if 'files' in failed_checks:
        print("📁 PROJECT FILES / ARCHIVOS DEL PROYECTO:")
        print("   Make sure you're in the correct directory")
        print("   Asegúrate de estar en el directorio correcto")
        print("   cd /path/to/pong-v2")
        print()
    
    if 'imports' in failed_checks:
        print("⚠ IMPORTS / IMPORTACIONES:")
        print("   Check for syntax errors:")
        print("   Verificar errores de sintaxis:")
        print("   python -m py_compile main.py")
        print()
    
    if 'permissions' in failed_checks:
        print("🔒 PERMISSIONS / PERMISOS:")
        print("   Check file system permissions")
        print("   Verificar permisos del sistema de archivos")
        print()

def main():
    """
    Main diagnostic function.
    Función principal de diagnóstico.
    """
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              PONG AI V2 - QUICK DIAGNOSTICS                      ║
║              PONG AI V2 - DIAGNÓSTICO RÁPIDO                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    # Run all checks / Ejecutar todas las verificaciones
    results = {
        'python_version': check_python_version(),
        'dependencies': check_dependencies(),
        'files': check_files(),
        'imports': test_imports(),
        'functionality': test_basic_functionality(),
        'permissions': check_permissions(),
        'display': check_display(),
    }
    
    # Summary / Resumen
    print_header("SUMMARY / RESUMEN")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}")
    print(f"Verificaciones pasadas: {passed}/{total}")
    
    if passed == total:
        print("\n✓ STATUS: HEALTHY / ESTADO: SALUDABLE")
    else:
        print(f"\n⚠ STATUS: {total - passed} ISSUES FOUND / {total - passed} PROBLEMAS ENCONTRADOS")
    
    # Recommendations / Recomendaciones
    provide_recommendations(results)
    
    print("\n" + "=" * 70)
    print("For more detailed debugging, see DEBUGGING.md")
    print("Para depuración más detallada, ver DEBUGGING.md")
    print("=" * 70 + "\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
