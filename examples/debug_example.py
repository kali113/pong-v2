"""
Debug System Usage Example
Ejemplo de Uso del Sistema de Depuración

This example shows how to use the debug system in your code.
Este ejemplo muestra cómo usar el sistema de depuración en tu código.
"""

import os
import sys

# Add parent directory to path / Agregar directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set headless mode for this example / Establecer modo sin cabeza para este ejemplo
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from debug_config import (
    DEBUG_CONFIG,
    log_trace,
    log_debug,
    log_info,
    log_warning,
    log_error,
    PERFORMANCE_PROFILER,
    ERROR_TRACKER,
    enable_debug,
    disable_debug
)

def example_basic_logging():
    """
    Example: Basic logging at different levels
    Ejemplo: Registro básico en diferentes niveles
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Logging")
    print("=" * 70)
    
    log_info("Game starting...")
    log_debug("Initializing game state")
    log_warning("High particle count detected")
    log_error("Failed to connect to server", Exception("Connection refused"))
    
    print("\nLogs shown above ↑")

def example_performance_tracking():
    """
    Example: Track performance metrics
    Ejemplo: Rastrear métricas de rendimiento
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Performance Tracking")
    print("=" * 70)
    
    import time
    
    # Simulate game loop
    for frame in range(10):
        start = time.perf_counter()
        
        # Simulate game work
        time.sleep(0.016)  # ~60 FPS
        
        frame_time = time.perf_counter() - start
        PERFORMANCE_PROFILER.add_frame_time(frame_time)
        
        # Update other metrics
        PERFORMANCE_PROFILER.update_metric('particle_count', frame * 5)
        PERFORMANCE_PROFILER.update_metric('network_latency_ms', 25.0)
    
    # Get metrics
    metrics = PERFORMANCE_PROFILER.get_metrics()
    
    print("\nPerformance Metrics:")
    print(f"  FPS: {metrics['fps']:.1f}")
    print(f"  Frame Time: {metrics['frame_time_ms']:.2f}ms")
    print(f"  Particle Count: {metrics['particle_count']}")
    print(f"  Network Latency: {metrics['network_latency_ms']}ms")

def example_error_tracking():
    """
    Example: Track and analyze errors
    Ejemplo: Rastrear y analizar errores
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Error Tracking")
    print("=" * 70)
    
    # Simulate various errors
    ERROR_TRACKER.add_error("NetworkError", "Connection timeout", "Multiplayer")
    ERROR_TRACKER.add_error("NetworkError", "Connection timeout", "Matchmaking")
    ERROR_TRACKER.add_error("AudioError", "Failed to load sound", "Audio System")
    ERROR_TRACKER.add_error("NetworkError", "Connection timeout", "Host")
    
    # Get error summary
    summary = ERROR_TRACKER.get_error_summary()
    
    print("\nError Summary:")
    print(f"  Total Errors: {summary['total_errors']}")
    print(f"  Unique Errors: {summary['unique_errors']}")
    print("\n  Most Common Errors:")
    for error, count in summary['most_common']:
        print(f"    {count}x - {error}")
    
    # Get recent errors
    recent = ERROR_TRACKER.get_recent_errors(3)
    print("\n  Recent Errors:")
    for error in recent:
        print(f"    [{error['timestamp'].strftime('%H:%M:%S')}] {error['type']}: {error['message']}")

def example_debug_levels():
    """
    Example: Using different debug levels
    Ejemplo: Usar diferentes niveles de depuración
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Debug Levels")
    print("=" * 70)
    
    from debug_config import DEBUG_LEVELS
    
    print("\nWith INFO level (default):")
    DEBUG_CONFIG.level = DEBUG_LEVELS['INFO']
    log_trace("This won't show")
    log_debug("This won't show")
    log_info("This WILL show")
    log_warning("This WILL show")
    log_error("This WILL show")
    
    print("\nWith TRACE level (maximum verbosity):")
    DEBUG_CONFIG.level = DEBUG_LEVELS['TRACE']
    log_trace("This WILL show")
    log_debug("This WILL show")
    log_info("This WILL show")
    
    print("\nWith ERROR level (minimum verbosity):")
    DEBUG_CONFIG.level = DEBUG_LEVELS['ERROR']
    log_warning("This won't show")
    log_error("This WILL show")
    
    # Reset to INFO
    DEBUG_CONFIG.level = DEBUG_LEVELS['INFO']

def example_full_debug_mode():
    """
    Example: Enable full debug mode
    Ejemplo: Habilitar modo de depuración completo
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Full Debug Mode")
    print("=" * 70)
    
    print("\nBefore enabling full debug:")
    print(f"  Level: {DEBUG_CONFIG.level}")
    print(f"  Show FPS: {DEBUG_CONFIG.show_fps}")
    print(f"  Show Collision Boxes: {DEBUG_CONFIG.show_collision_boxes}")
    print(f"  Show AI Target: {DEBUG_CONFIG.show_ai_target}")
    
    # Enable everything
    enable_debug()
    
    print("\nAfter enabling full debug:")
    print(f"  Level: {DEBUG_CONFIG.level}")
    print(f"  Show FPS: {DEBUG_CONFIG.show_fps}")
    print(f"  Show Collision Boxes: {DEBUG_CONFIG.show_collision_boxes}")
    print(f"  Show AI Target: {DEBUG_CONFIG.show_ai_target}")
    print(f"  Log to File: {DEBUG_CONFIG.log_to_file}")
    
    # Disable everything
    disable_debug()
    
    print("\nAfter disabling debug:")
    print(f"  Level: {DEBUG_CONFIG.level}")
    print(f"  Show FPS: {DEBUG_CONFIG.show_fps}")

def main():
    """
    Run all examples
    Ejecutar todos los ejemplos
    """
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              DEBUG SYSTEM USAGE EXAMPLES                         ║
║              EJEMPLOS DE USO DEL SISTEMA DE DEPURACIÓN           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    example_basic_logging()
    example_performance_tracking()
    example_error_tracking()
    example_debug_levels()
    example_full_debug_mode()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("¡Todos los ejemplos completados!")
    print("\nFor more information, see:")
    print("- debug_config.py - Full API documentation")
    print("- DEBUGGING.md - Comprehensive debugging guide")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
