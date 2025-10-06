"""
Debug Configuration System for Pong AI V2
Sistema de Configuración de Depuración para Pong AI V2

This module provides comprehensive debugging utilities and configuration.
Este módulo proporciona utilidades de depuración y configuración completas.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# DEBUG LEVELS / NIVELES DE DEPURACIÓN
# ============================================================================

DEBUG_LEVELS = {
    'NONE': 0,      # No debug output / Sin salida de depuración
    'ERROR': 1,     # Only errors / Solo errores
    'WARNING': 2,   # Errors and warnings / Errores y advertencias
    'INFO': 3,      # General information / Información general
    'DEBUG': 4,     # Detailed debug info / Información de depuración detallada
    'TRACE': 5      # Everything including traces / Todo incluyendo trazas
}

# ============================================================================
# DEBUG CONFIGURATION / CONFIGURACIÓN DE DEPURACIÓN
# ============================================================================

class DebugConfig:
    """
    Central debug configuration.
    Configuración de depuración central.
    """
    
    def __init__(self):
        self.level = DEBUG_LEVELS['INFO']
        self.log_to_file = False
        self.log_to_console = True
        self.show_fps = True
        self.show_collision_boxes = False
        self.show_ai_target = False
        self.show_particle_count = False
        self.show_network_stats = False
        self.pause_on_error = False
        self.screenshot_on_error = False
        self.log_file_path = Path.home() / '.pong_ai_debug.log'
        self.max_log_size = 1024 * 1024  # 1MB
        
    def enable_full_debug(self):
        """Enable all debug features / Habilitar todas las características de depuración"""
        self.level = DEBUG_LEVELS['TRACE']
        self.log_to_file = True
        self.show_fps = True
        self.show_collision_boxes = True
        self.show_ai_target = True
        self.show_particle_count = True
        self.show_network_stats = True
        
    def disable_debug(self):
        """Disable all debug features / Deshabilitar todas las características de depuración"""
        self.level = DEBUG_LEVELS['NONE']
        self.log_to_file = False
        self.show_fps = False
        self.show_collision_boxes = False
        self.show_ai_target = False
        self.show_particle_count = False
        self.show_network_stats = False

# ============================================================================
# DEBUG LOGGER / REGISTRADOR DE DEPURACIÓN
# ============================================================================

class DebugLogger:
    """
    Centralized logging system.
    Sistema de registro centralizado.
    """
    
    def __init__(self, config: DebugConfig):
        self.config = config
        self.logger = logging.getLogger('PongAI')
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler / Manejador de consola
        if config.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            console_format = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_format)
            self.logger.addHandler(console_handler)
        
        # File handler / Manejador de archivo
        if config.log_to_file:
            try:
                file_handler = logging.FileHandler(config.log_file_path)
                file_handler.setLevel(logging.DEBUG)
                file_format = logging.Formatter(
                    '[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_format)
                self.logger.addHandler(file_handler)
            except IOError as e:
                print(f"Warning: Could not create log file: {e}")
    
    def trace(self, message: str):
        """Log trace message / Registrar mensaje de traza"""
        if self.config.level >= DEBUG_LEVELS['TRACE']:
            self.logger.debug(f"[TRACE] {message}")
    
    def debug(self, message: str):
        """Log debug message / Registrar mensaje de depuración"""
        if self.config.level >= DEBUG_LEVELS['DEBUG']:
            self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message / Registrar mensaje de información"""
        if self.config.level >= DEBUG_LEVELS['INFO']:
            self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message / Registrar mensaje de advertencia"""
        if self.config.level >= DEBUG_LEVELS['WARNING']:
            self.logger.warning(message)
    
    def error(self, message: str, exception: Exception = None):
        """Log error message / Registrar mensaje de error"""
        if self.config.level >= DEBUG_LEVELS['ERROR']:
            if exception:
                self.logger.error(f"{message}: {exception}", exc_info=True)
            else:
                self.logger.error(message)

# ============================================================================
# PERFORMANCE PROFILER / PERFILADOR DE RENDIMIENTO
# ============================================================================

class PerformanceProfiler:
    """
    Track performance metrics.
    Rastrear métricas de rendimiento.
    """
    
    def __init__(self):
        self.frame_times = []
        self.max_samples = 60
        self.metrics = {
            'fps': 0.0,
            'frame_time_ms': 0.0,
            'draw_time_ms': 0.0,
            'update_time_ms': 0.0,
            'particle_count': 0,
            'network_latency_ms': 0.0
        }
    
    def add_frame_time(self, frame_time: float):
        """
        Add frame time sample.
        Agregar muestra de tiempo de frame.
        
        Args:
            frame_time: Frame time in seconds / Tiempo de frame en segundos
        """
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)
        
        if self.frame_times:
            avg_time = sum(self.frame_times) / len(self.frame_times)
            self.metrics['fps'] = 1.0 / avg_time if avg_time > 0 else 60.0
            self.metrics['frame_time_ms'] = avg_time * 1000.0
    
    def update_metric(self, key: str, value: float):
        """Update specific metric / Actualizar métrica específica"""
        if key in self.metrics:
            self.metrics[key] = value
    
    def get_metrics(self) -> dict:
        """Get all current metrics / Obtener todas las métricas actuales"""
        return self.metrics.copy()

# ============================================================================
# ERROR TRACKER / RASTREADOR DE ERRORES
# ============================================================================

class ErrorTracker:
    """
    Track and report errors.
    Rastrear y reportar errores.
    """
    
    def __init__(self, max_errors: int = 100):
        self.errors = []
        self.max_errors = max_errors
        self.error_counts = {}
    
    def add_error(self, error_type: str, message: str, context: str = ""):
        """
        Record an error.
        Registrar un error.
        
        Args:
            error_type: Type of error / Tipo de error
            message: Error message / Mensaje de error
            context: Context information / Información de contexto
        """
        timestamp = datetime.now()
        error_entry = {
            'timestamp': timestamp,
            'type': error_type,
            'message': message,
            'context': context
        }
        
        self.errors.append(error_entry)
        if len(self.errors) > self.max_errors:
            self.errors.pop(0)
        
        # Count occurrences
        key = f"{error_type}:{message}"
        self.error_counts[key] = self.error_counts.get(key, 0) + 1
    
    def get_recent_errors(self, count: int = 10):
        """Get most recent errors / Obtener errores más recientes"""
        return self.errors[-count:]
    
    def get_error_summary(self):
        """Get error summary / Obtener resumen de errores"""
        return {
            'total_errors': len(self.errors),
            'unique_errors': len(self.error_counts),
            'most_common': sorted(
                self.error_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
    
    def clear(self):
        """Clear all recorded errors / Limpiar todos los errores registrados"""
        self.errors.clear()
        self.error_counts.clear()

# ============================================================================
# GLOBAL DEBUG INSTANCE / INSTANCIA GLOBAL DE DEPURACIÓN
# ============================================================================

# Create global debug config / Crear configuración global de depuración
DEBUG_CONFIG = DebugConfig()
DEBUG_LOGGER = DebugLogger(DEBUG_CONFIG)
PERFORMANCE_PROFILER = PerformanceProfiler()
ERROR_TRACKER = ErrorTracker()

# ============================================================================
# CONVENIENCE FUNCTIONS / FUNCIONES DE CONVENIENCIA
# ============================================================================

def log_trace(message: str):
    """Log trace message / Registrar mensaje de traza"""
    DEBUG_LOGGER.trace(message)

def log_debug(message: str):
    """Log debug message / Registrar mensaje de depuración"""
    DEBUG_LOGGER.debug(message)

def log_info(message: str):
    """Log info message / Registrar mensaje de información"""
    DEBUG_LOGGER.info(message)

def log_warning(message: str):
    """Log warning message / Registrar mensaje de advertencia"""
    DEBUG_LOGGER.warning(message)

def log_error(message: str, exception: Exception = None):
    """Log error message / Registrar mensaje de error"""
    DEBUG_LOGGER.error(message, exception)
    ERROR_TRACKER.add_error('ERROR', message, str(exception) if exception else "")

def enable_debug():
    """Enable full debug mode / Habilitar modo de depuración completo"""
    DEBUG_CONFIG.enable_full_debug()
    log_info("Full debug mode enabled")

def disable_debug():
    """Disable debug mode / Deshabilitar modo de depuración"""
    DEBUG_CONFIG.disable_debug()
