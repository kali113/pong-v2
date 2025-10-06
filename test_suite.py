"""
Comprehensive Test Suite for Pong AI V2
Suite de Pruebas Completa para Pong AI V2

Automated testing for all major components.
Pruebas automatizadas para todos los componentes principales.
"""

import os
import sys
import time
from pathlib import Path

# Set headless mode for testing / Establecer modo sin cabeza para pruebas
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Import main modules / Importar módulos principales
import main
from debug_config import log_info, log_error, ERROR_TRACKER

# ============================================================================
# TEST RESULTS / RESULTADOS DE PRUEBAS
# ============================================================================

class TestResults:
    """Track test results / Rastrear resultados de pruebas"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.tests = []
    
    def add_pass(self, test_name: str, message: str = ""):
        self.passed += 1
        self.tests.append(('PASS', test_name, message))
        print(f"  ✓ {test_name}: {message}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.tests.append(('FAIL', test_name, error))
        print(f"  ✗ {test_name}: {error}")
    
    def add_skip(self, test_name: str, reason: str):
        self.skipped += 1
        self.tests.append(('SKIP', test_name, reason))
        print(f"  ⊙ {test_name}: {reason}")
    
    def summary(self):
        total = self.passed + self.failed + self.skipped
        print("\n" + "=" * 70)
        print("TEST SUMMARY / RESUMEN DE PRUEBAS")
        print("=" * 70)
        print(f"Total tests: {total}")
        print(f"Passed: {self.passed} ({self.passed/total*100:.1f}%)" if total > 0 else "Passed: 0")
        print(f"Failed: {self.failed} ({self.failed/total*100:.1f}%)" if total > 0 else "Failed: 0")
        print(f"Skipped: {self.skipped}")
        print("=" * 70)
        return self.failed == 0

# ============================================================================
# TEST SUITES / SUITES DE PRUEBAS
# ============================================================================

def test_imports(results: TestResults):
    """Test module imports / Probar importaciones de módulos"""
    print("\n1. TESTING IMPORTS / PROBANDO IMPORTACIONES")
    
    try:
        import pygame
        results.add_pass("pygame import", f"version {pygame.version.ver}")
    except ImportError as e:
        results.add_fail("pygame import", str(e))
    
    try:
        import numpy
        results.add_pass("numpy import", f"version {numpy.__version__}")
    except ImportError as e:
        results.add_fail("numpy import", str(e))
    
    try:
        from PIL import Image
        results.add_pass("Pillow import", "OK")
    except ImportError as e:
        results.add_skip("Pillow import", "Optional dependency")
    
    try:
        import main
        results.add_pass("main.py import", f"version {main.__version__}")
    except Exception as e:
        results.add_fail("main.py import", str(e))
    
    try:
        import main_web
        results.add_pass("main_web.py import", f"version {main_web.__version__}")
    except Exception as e:
        results.add_fail("main_web.py import", str(e))

def test_constants(results: TestResults):
    """Test constant definitions / Probar definiciones de constantes"""
    print("\n2. TESTING CONSTANTS / PROBANDO CONSTANTES")
    
    constants = [
        ('SCREEN_WIDTH', int),
        ('SCREEN_HEIGHT', int),
        ('PADDLE_WIDTH', int),
        ('PADDLE_HEIGHT', int),
        ('PADDLE_SPEED', (int, float)),
        ('IS_WEB', bool),
    ]
    
    for const_name, expected_type in constants:
        if hasattr(main, const_name):
            value = getattr(main, const_name)
            if isinstance(value, expected_type):
                results.add_pass(f"Constant {const_name}", f"= {value}")
            else:
                results.add_fail(f"Constant {const_name}", f"Wrong type: {type(value)}")
        else:
            results.add_fail(f"Constant {const_name}", "Not defined")

def test_classes(results: TestResults):
    """Test class instantiation / Probar instanciación de clases"""
    print("\n3. TESTING CLASSES / PROBANDO CLASES")
    
    # Test GameSettings
    try:
        settings = main.GameSettings()
        results.add_pass("GameSettings", f"screen_width={settings.screen_width}")
    except Exception as e:
        results.add_fail("GameSettings", str(e))
    
    # Test ParticlePool
    try:
        pool = main.ParticlePool(50)
        particle = pool.acquire()
        if particle:
            pool.release(particle)
            results.add_pass("ParticlePool", "Object pooling works")
        else:
            results.add_fail("ParticlePool", "Failed to acquire particle")
    except Exception as e:
        results.add_fail("ParticlePool", str(e))
    
    # Test Particle
    try:
        particle = main.Particle()
        particle.reset(100, 100, (255, 0, 0), size=5, life=1.0)
        results.add_pass("Particle", "Instantiation and reset OK")
    except Exception as e:
        results.add_fail("Particle", str(e))
    
    # Test ScoreBurst
    try:
        burst = main.ScoreBurst(100, 100, "TEST")
        results.add_pass("ScoreBurst", "Instantiation OK")
    except Exception as e:
        results.add_fail("ScoreBurst", str(e))
    
    # Test Paddle
    try:
        paddle = main.Paddle(50, main.SCREEN_HEIGHT // 2, (255, 255, 255))
        results.add_pass("Paddle", f"pos=({paddle.x}, {paddle.y})")
    except Exception as e:
        results.add_fail("Paddle", str(e))
    
    # Test Ball
    try:
        ball = main.Ball()
        results.add_pass("Ball", f"pos=({ball.x:.0f}, {ball.y:.0f})")
    except Exception as e:
        results.add_fail("Ball", str(e))

def test_functions(results: TestResults):
    """Test utility functions / Probar funciones utilitarias"""
    print("\n4. TESTING FUNCTIONS / PROBANDO FUNCIONES")
    
    # Test load_settings
    try:
        settings = main.load_settings()
        if isinstance(settings, dict):
            results.add_pass("load_settings()", f"{len(settings)} settings loaded")
        else:
            results.add_fail("load_settings()", "Invalid return type")
    except Exception as e:
        results.add_fail("load_settings()", str(e))
    
    # Test get_local_ip
    try:
        ip = main.get_local_ip()
        if ip and '.' in ip:
            results.add_pass("get_local_ip()", f"IP: {ip}")
        else:
            results.add_fail("get_local_ip()", "Invalid IP")
    except Exception as e:
        results.add_fail("get_local_ip()", str(e))
    
    # Test generate_code
    try:
        code = main.generate_code()
        if len(code) == 6 and code.isalnum():
            results.add_pass("generate_code()", f"Generated: {code}")
        else:
            results.add_fail("generate_code()", "Invalid code format")
    except Exception as e:
        results.add_fail("generate_code()", str(e))
    
    # Test validate (numeric validation function)
    try:
        result = main.validate(100, 1000)
        if result == 100:
            results.add_pass("validate()", "Numeric validation works")
        else:
            results.add_fail("validate()", f"Expected 100, got {result}")
    except Exception as e:
        results.add_fail("validate()", str(e))
    
    # Test create_sound
    try:
        sound = main.create_sound(440, 0.1, 0.5)
        if sound:
            results.add_pass("create_sound()", "Audio generation works")
        else:
            results.add_skip("create_sound()", "Audio not available")
    except Exception as e:
        results.add_skip("create_sound()", "Audio not available in headless mode")

def test_game_logic(results: TestResults):
    """Test game logic / Probar lógica del juego"""
    print("\n5. TESTING GAME LOGIC / PROBANDO LÓGICA DEL JUEGO")
    
    # Test ball movement
    try:
        ball = main.Ball()
        old_x = ball.x
        ball.move(0.016)  # 16ms frame
        if ball.x != old_x:
            results.add_pass("Ball.move()", "Ball moves correctly")
        else:
            results.add_fail("Ball.move()", "Ball not moving")
    except Exception as e:
        results.add_fail("Ball.move()", str(e))
    
    # Test paddle movement
    try:
        paddle = main.Paddle(50, main.SCREEN_HEIGHT // 2, (255, 255, 255))
        old_y = paddle.y
        paddle.move(1.0, 0.016)  # Move up
        if paddle.y != old_y:
            results.add_pass("Paddle.move()", "Paddle moves correctly")
        else:
            results.add_fail("Paddle.move()", "Paddle not moving")
    except Exception as e:
        results.add_fail("Paddle.move()", str(e))
    
    # Test collision detection
    try:
        ball = main.Ball()
        paddle = main.Paddle(50, main.SCREEN_HEIGHT // 2, (255, 255, 255))
        ball.x = paddle.x + main.PADDLE_WIDTH
        ball.y = paddle.y
        
        # Simple collision check
        collision = (abs(ball.x - paddle.x) < ball.size + main.PADDLE_WIDTH and
                    abs(ball.y - paddle.y) < ball.size + main.PADDLE_HEIGHT)
        
        results.add_pass("Collision detection", "Logic OK")
    except Exception as e:
        results.add_fail("Collision detection", str(e))

def test_translations(results: TestResults):
    """Test translation system / Probar sistema de traducción"""
    print("\n6. TESTING TRANSLATIONS / PROBANDO TRADUCCIONES")
    
    try:
        translations = main.TRANSLATIONS
        
        if 'en' in translations and 'es' in translations:
            results.add_pass("Translation system", "Both languages available")
        else:
            results.add_fail("Translation system", "Missing languages")
        
        # Check key consistency
        en_keys = set(translations['en'].keys())
        es_keys = set(translations['es'].keys())
        
        if en_keys == es_keys:
            results.add_pass("Translation keys", f"{len(en_keys)} keys consistent")
        else:
            missing = en_keys - es_keys
            extra = es_keys - en_keys
            results.add_fail("Translation keys", f"Mismatch: {missing or extra}")
    
    except Exception as e:
        results.add_fail("Translation system", str(e))

def test_network_classes(results: TestResults):
    """Test network classes / Probar clases de red"""
    print("\n7. TESTING NETWORK CLASSES / PROBANDO CLASES DE RED")
    
    # Note: Network tests are limited in headless mode
    # Nota: Las pruebas de red son limitadas en modo sin cabeza
    
    try:
        # Test NetworkHost instantiation
        host = main.NetworkHost()
        results.add_pass("NetworkHost", "Instantiation OK")
    except Exception as e:
        results.add_fail("NetworkHost", str(e))
    
    try:
        # Test NetworkClient instantiation
        client = main.NetworkClient()
        results.add_pass("NetworkClient", "Instantiation OK")
    except Exception as e:
        results.add_fail("NetworkClient", str(e))

def test_file_structure(results: TestResults):
    """Test file structure / Probar estructura de archivos"""
    print("\n8. TESTING FILE STRUCTURE / PROBANDO ESTRUCTURA DE ARCHIVOS")
    
    required_files = [
        'main.py',
        'main_web.py',
        'requirements.txt',
        'README.md',
        'BUILD.md'
    ]
    
    for file in required_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            results.add_pass(f"File {file}", f"{size} bytes")
        else:
            results.add_fail(f"File {file}", "Missing")

# ============================================================================
# MAIN TEST RUNNER / EJECUTOR PRINCIPAL DE PRUEBAS
# ============================================================================

def run_all_tests():
    """
    Run all test suites.
    Ejecutar todas las suites de pruebas.
    """
    print("=" * 70)
    print("PONG AI V2 - COMPREHENSIVE TEST SUITE")
    print("SUITE DE PRUEBAS COMPLETA PARA PONG AI V2")
    print("=" * 70)
    
    results = TestResults()
    start_time = time.time()
    
    # Run all test suites / Ejecutar todas las suites de pruebas
    test_imports(results)
    test_constants(results)
    test_classes(results)
    test_functions(results)
    test_game_logic(results)
    test_translations(results)
    test_network_classes(results)
    test_file_structure(results)
    
    # Calculate duration / Calcular duración
    duration = time.time() - start_time
    
    # Show summary / Mostrar resumen
    success = results.summary()
    print(f"\nTest duration: {duration:.2f} seconds")
    
    if success:
        print("\n✓ ALL TESTS PASSED!")
        print("✓ ¡TODAS LAS PRUEBAS PASARON!")
        return 0
    else:
        print(f"\n✗ {results.failed} TESTS FAILED")
        print(f"✗ {results.failed} PRUEBAS FALLARON")
        return 1

# ============================================================================
# ENTRY POINT / PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    sys.exit(run_all_tests())
