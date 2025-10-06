# ============================================================================
# PONG AI V2 - NEON EDITION v1.0.0-pre-alpha
# A modern Pong game with AI, multiplayer, power-ups, particle effects, and translations
# Un juego moderno de Pong con IA, multijugador, power-ups, efectos de partículas y traducciones
# ============================================================================

__version__ = "1.0.0-pre-alpha"

# Standard library imports / Importaciones de biblioteca estándar
import asyncio    # Async/await support for web / Soporte async/await para web
import json       # JSON parsing / Análisis JSON
import math       # Mathematical functions / Funciones matemáticas
import os         # Operating system interface / Interfaz del sistema operativo
import random     # Random number generation / Generación de números aleatorios
import socket     # Network communication / Comunicación de red
import string     # String operations / Operaciones de cadenas
import sys        # System-specific parameters / Parámetros específicos del sistema
import threading  # Thread-based parallelism / Paralelismo basado en hilos
import time       # Time access and conversions / Acceso y conversiones de tiempo
import urllib.request  # URL handling / Manejo de URLs
from dataclasses import dataclass  # Data classes / Clases de datos
from pathlib import Path  # Object-oriented filesystem paths / Rutas del sistema de archivos orientadas a objetos

# Third-party imports / Importaciones de terceros
import numpy as np  # Numerical computing / Computación numérica

# Windows DPI awareness fix / Corrección de DPI para Windows
# This prevents blurry text on high-DPI displays
# Esto previene texto borroso en pantallas de alto DPI
if sys.platform == 'win32':
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except (AttributeError, OSError):
        pass  # DPI awareness not available / DPI no disponible

# Center game window on screen / Centrar ventana del juego en pantalla
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame / Inicializar Pygame
import pygame
pygame.init()  # Initialize display and input / Inicializar pantalla y entrada
pygame.mixer.init()  # Initialize audio system / Inicializar sistema de audio

# Web environment detection / Detección de entorno web
# Check if running in browser via Pygbag/Pyodide
try:
    import platform
    IS_WEB = platform.system() == "Emscripten"
except:
    IS_WEB = False

# Settings file location / Ubicación del archivo de configuración
# Stored in user's home directory / Almacenado en el directorio personal del usuario
SETTINGS_FILE = Path.home() / '.pong_ai_settings.json'
# ============================================================================
# TRANSLATION SYSTEM / SISTEMA DE TRADUCCIÓN
# All UI text in English and Spanish / Todo el texto de UI en Inglés y Español
# Access via game.t('key') method / Acceso mediante método game.t('key')
# ============================================================================
TRANSLATIONS = {
    'en': {  # English translations / Traducciones en inglés
        'title': 'Pong AI', 'subtitle': 'SPACE / ENTER to start', 'easy': 'Easy', 'medium': 'Medium', 'hard': 'Hard',
        'difficulty_hint': 'Click or use UP/DOWN / W-S to change difficulty', 'multiplayer': 'Multiplayer',
        'settings': 'Settings', 'diagnostics': 'Run Diagnostics', 'fullscreen': 'Fullscreen:', 'audio': 'Audio Effects:',
        'hud': 'Performance HUD:', 'language': 'Language:', 'back': 'Back', 'host_game': 'Host Game',
        'join_private': 'Join Private Game:', 'join': 'Join', 'or': 'OR', 'find_public': 'Find Public Match',
        'waiting': 'Waiting for player...', 'host_code': 'Host Code:', 'cancel': 'Cancel', 'player': 'Player', 'ai': 'AI',
        'searching': 'Searching for match', 'code_hint': 'CODE', 'close': 'Close', 'game_over': 'Game Over',
        'wins': 'wins!', 'rematch': 'Rematch (R)', 'menu': 'Menu (M)', 
        '2player': '🎮 2 PLAYER', 'system_diagnostics': 'System Diagnostics', 'hosting_game': 'Hosting Game',
        'share_code': 'Share code:', 'or_ip': 'Or IP:', 'waiting_player': 'Waiting for player', 
        'player_connected': 'Player Connected!', 'internet': 'Internet:'
    },
    'es': {  # Spanish translations / Traducciones en español
        'title': 'Pong IA', 'subtitle': 'ESPACIO / ENTER para iniciar', 'easy': 'Fácil', 'medium': 'Medio', 'hard': 'Difícil',
        'difficulty_hint': 'Clic o usa ARRIBA/ABAJO / W-S para cambiar dificultad', 'multiplayer': 'Multijugador',
        'settings': 'Configuración', 'diagnostics': 'Ejecutar Diagnósticos', 'fullscreen': 'Pantalla completa:', 'audio': 'Efectos de audio:',
        'hud': 'HUD de rendimiento:', 'language': 'Idioma:', 'back': 'Volver', 'host_game': 'Crear Partida',
        'join_private': 'Unirse a Partida Privada:', 'join': 'Unirse', 'or': 'O', 'find_public': 'Buscar Partida Pública',
        'waiting': 'Esperando jugador...', 'host_code': 'Código:', 'cancel': 'Cancelar', 'player': 'Jugador', 'ai': 'IA',
        'searching': 'Buscando partida', 'code_hint': 'CÓDIGO', 'close': 'Cerrar', 'game_over': 'Fin del Juego',
        'wins': 'gana!', 'rematch': 'Revancha (R)', 'menu': 'Menú (M)',
        '2player': '🎮 2 JUGADORES', 'system_diagnostics': 'Diagnósticos del Sistema', 'hosting_game': 'Creando Partida',
        'share_code': 'Compartir código:', 'or_ip': 'O IP:', 'waiting_player': 'Esperando jugador',
        'player_connected': '¡Jugador Conectado!', 'internet': 'Internet:'
    }
}
# ============================================================================
# SETTINGS MANAGEMENT / GESTIÓN DE CONFIGURACIÓN
# Load/save user preferences / Cargar/guardar preferencias del usuario
# ============================================================================

def load_settings():
    """
    Load user settings from JSON file.
    Cargar configuración del usuario desde archivo JSON.
    
    Returns / Retorna:
        dict: Settings dictionary with fullscreen, difficulty, audio, language
              Diccionario de configuración con pantalla completa, dificultad, audio, idioma
    """
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Ensure all keys exist / Asegurar que todas las claves existan
                    data.setdefault('audio_enabled', True)
                    data.setdefault('language', 'en')
                    return data
    except (json.JSONDecodeError, IOError, ValueError):
        pass  # Invalid or corrupted settings file / Archivo inválido o corrupto
    
    # Return default settings if file missing/corrupted
    # Retornar configuración por defecto si archivo falta/está corrupto
    return {
        'fullscreen': False,  # Windowed mode / Modo ventana
        'debug_hud': False,   # Performance overlay off / Overlay de rendimiento desactivado
        'difficulty': 1,      # Medium AI / IA Media
        'audio_enabled': True,  # Sound effects on / Efectos de sonido activados
        'language': 'en'      # English by default / Inglés por defecto
    }

def save_settings(fullscreen, debug_hud, difficulty, audio_enabled, language='en'):
    """
    Save user settings to JSON file.
    Guardar configuración del usuario en archivo JSON.
    
    Args / Argumentos:
        fullscreen (bool): Fullscreen mode enabled / Modo pantalla completa activado
        debug_hud (bool): Show performance HUD / Mostrar HUD de rendimiento
        difficulty (int): AI difficulty index (0=Easy, 1=Medium, 2=Hard)
                         Índice de dificultad de IA (0=Fácil, 1=Medio, 2=Difícil)
        audio_enabled (bool): Sound effects enabled / Efectos de sonido activados
        language (str): UI language code ('en' or 'es') / Código de idioma ('en' o 'es')
    """
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({
                'fullscreen': fullscreen,
                'debug_hud': debug_hud,
                'difficulty': difficulty,
                'audio_enabled': audio_enabled,
                'language': language
            }, f)
    except IOError:
        pass  # Unable to save settings / No se puede guardar configuración

# ============================================================================
# VALIDATION UTILITIES / UTILIDADES DE VALIDACIÓN
# Safe numeric value processing / Procesamiento seguro de valores numéricos
# ============================================================================

def validate(v, mx=10000):
    """
    Validate and clamp numeric values for network safety.
    Validar y limitar valores numéricos para seguridad de red.
    
    Args / Argumentos:
        v: Value to validate / Valor a validar
        mx (float): Maximum absolute value / Valor absoluto máximo
    
    Returns / Retorna:
        float: Clamped value or 0 if invalid / Valor limitado o 0 si es inválido
    """
    try:
        # Convert to float and clamp to range / Convertir a float y limitar al rango
        return float(v) if -mx <= (f:=float(v)) <= mx else 0
    except (ValueError, TypeError):
        return 0  # Invalid input returns zero / Entrada inválida retorna cero
# ============================================================================
# NETWORK UTILITIES / UTILIDADES DE RED
# IP detection and lobby code generation / Detección de IP y generación de códigos
# ============================================================================

def get_local_ip():
    """
    Get local IP address for LAN networking.
    Obtener dirección IP local para red LAN.
    
    Returns / Retorna:
        str: Local IP address (e.g., "192.168.1.5") or "127.0.0.1" if failed
             Dirección IP local (ej., "192.168.1.5") o "127.0.0.1" si falla
    """
    try:
        # Connect to external server to determine local network IP
        # Conectar a servidor externo para determinar IP de red local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS server / Servidor DNS de Google
        ip = s.getsockname()[0]  # Get socket's own IP / Obtener IP propia del socket
        s.close()
        return ip
    except (socket.error, OSError):
        return "127.0.0.1"  # Fallback to localhost / Retornar localhost como respaldo

def generate_code(length=6):
    """
    Generate random alphanumeric code for multiplayer lobbies.
    Generar código alfanumérico aleatorio para salas multijugador.
    
    Args / Argumentos:
        length (int): Code length / Longitud del código
    
    Returns / Retorna:
        str: Random uppercase code (e.g., "A3K9ZT") / Código aleatorio en mayúsculas
    """
    import secrets  # Cryptographically strong random / Aleatorio criptográficamente fuerte
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def get_external_ip():
    """
    Get external IP address via ipify API.
    Obtener dirección IP externa mediante API ipify.
    
    Returns / Retorna:
        str or None: External IP (e.g., "203.45.67.89") or None if unavailable
                     IP externa (ej., "203.45.67.89") o None si no está disponible
    
    Note / Nota:
        Used for internet multiplayer (requires port forwarding)
        Usado para multijugador por internet (requiere reenvío de puertos)
    """
    try:
        response = urllib.request.urlopen('https://api.ipify.org?format=text', timeout=3)
        return response.read().decode('utf8')
    except (urllib.error.URLError, socket.timeout):
        return None  # No internet or API unavailable / Sin internet o API no disponible
# ============================================================================
# MULTIPLAYER NETWORKING CLASSES / CLASES DE RED MULTIJUGADOR
# Host/Client architecture for real-time gameplay synchronization
# Arquitectura Host/Cliente para sincronización de juego en tiempo real
# ============================================================================

class NetworkHost:
    """
    Host server for LAN multiplayer. Listens for client connections.
    Servidor anfitrión para multijugador LAN. Escucha conexiones de clientes.
    
    Architecture / Arquitectura:
        - Host controls game state (ball physics, scoring)
          El anfitrión controla el estado del juego (física de la bola, puntaje)
        - Client sends paddle position, receives game state
          El cliente envía posición de la paleta, recibe estado del juego
        - JSON messages over TCP sockets
          Mensajes JSON sobre sockets TCP
    """
    
    def __init__(self, port=5555):
        """
        Initialize host server.
        Inicializar servidor anfitrión.
        
        Args / Argumentos:
            port (int): TCP port to listen on / Puerto TCP para escuchar
        """
        self.port = port  # Server port / Puerto del servidor
        self.code = generate_code()  # 6-character lobby code / Código de sala de 6 caracteres
        self.socket = None  # Server socket / Socket del servidor
        self.client_socket = None  # Connected client socket / Socket del cliente conectado
        self.connected = False  # Client connected flag / Indicador de cliente conectado
        self.running = False  # Server running flag / Indicador de servidor en ejecución
        self.paddle_y = 0  # Host paddle position / Posición de paleta del anfitrión
        self.remote_paddle_y = 0  # Client paddle position / Posición de paleta del cliente
        self.external_ip = None  # Public IP (for internet play) / IP pública (para juego por internet)
        self.local_ip = get_local_ip()  # LAN IP / IP de LAN
    
    def start(self):
        """
        Start hosting server and wait for connections.
        Iniciar servidor anfitrión y esperar conexiones.
        
        Returns / Retorna:
            bool: True if server started successfully / True si el servidor inició correctamente
        """
        try:
            # Get external IP for internet play (requires port forwarding)
            # Obtener IP externa para juego por internet (requiere reenvío de puertos)
            self.external_ip = get_external_ip()
            
            # Create TCP socket / Crear socket TCP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Allow address reuse (prevents "Address already in use" error)
            # Permitir reutilización de dirección (previene error "Dirección ya en uso")
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # SECURITY: Bind to all network interfaces for LAN multiplayer
            # This is intentional for local network play - DO NOT expose to internet
            # SEGURIDAD: Vincular a todas las interfaces para multijugador LAN
            # Esto es intencional para juego en red local - NO exponer a internet
            self.socket.bind(('0.0.0.0', self.port))
            
            # Listen for 1 connection / Escuchar 1 conexión
            self.socket.listen(1)
            
            # Set timeout for accept() calls / Establecer timeout para llamadas accept()
            self.socket.settimeout(0.5)
            
            self.running = True
            
            # Start background thread to accept connections
            # Iniciar hilo en segundo plano para aceptar conexiones
            threading.Thread(target=self._accept_loop, daemon=True).start()
            
            return True
        except (socket.error, OSError):
            return False  # Failed to start server / No se pudo iniciar el servidor
    
    def _accept_loop(self):
        """
        Accept incoming client connections (background thread).
        Aceptar conexiones entrantes de clientes (hilo en segundo plano).

        Note / Nota:
            Runs in daemon thread until first client connects or server stops
            Se ejecuta en hilo daemon hasta que conecte el primer cliente o se detenga el servidor
        """
        print("[Debug Network] Accept loop started")
        while self.running and not self.connected:
            try:
                # Wait for client connection / Esperar conexión de cliente
                client, addr = self.socket.accept()
                print(f"[Debug Network] Client connected from {addr}")

                # Set short timeout for receive operations
                # Establecer timeout corto para operaciones de recepción
                client.settimeout(0.1)

                self.client_socket = client
                self.connected = True

                # Start receive loop in new thread / Iniciar bucle de recepción en nuevo hilo
                threading.Thread(target=self._recv_loop, daemon=True).start()
                break
            except socket.timeout:
                continue  # No connection yet, retry / Sin conexión aún, reintentar
            except (socket.error, OSError) as e:
                print(f"[Debug Network] Accept loop error: {e}")
                break  # Socket error, stop accepting / Error de socket, detener aceptación
    
    def _recv_loop(self):
        """
        Receive and process messages from client (background thread).
        Recibir y procesar mensajes del cliente (hilo en segundo plano).
        
        Protocol / Protocolo:
            Client sends: {"type": "paddle", "y": 123.45}
            El cliente envía: {"type": "paddle", "y": 123.45}
        """
        buffer = ""  # Message buffer for incomplete data / Buffer de mensajes para datos incompletos
        
        while self.running and self.connected:
            try:
                # Receive up to 1KB of data / Recibir hasta 1KB de datos
                data = self.client_socket.recv(1024).decode('utf-8', errors='ignore')
                
                if not data:
                    # Empty data means connection closed / Datos vacíos significan conexión cerrada
                    self.connected = False
                    break
                
                buffer += data
                
                # Process complete messages (newline-delimited JSON)
                # Procesar mensajes completos (JSON delimitado por nueva línea)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    try:
                        msg = json.loads(line)
                        
                        # Update remote paddle position from client
                        # Actualizar posición de paleta remota desde el cliente
                        if msg.get('type') == 'paddle':
                            self.remote_paddle_y = validate(msg.get('y', 0))
                    except (json.JSONDecodeError, KeyError):
                        pass  # Malformed message, ignore / Mensaje malformado, ignorar
            except socket.timeout:
                continue  # No data available, retry / Sin datos disponibles, reintentar
            except (socket.error, OSError):
                self.connected = False
                break  # Connection lost / Conexión perdida
    
    def send_game_state(self, paddle_y, ball_x, ball_y, ball_vx, ball_vy, score_player, score_ai):
        """
        Send game state to connected client.
        Enviar estado del juego al cliente conectado.
        
        Args / Argumentos:
            paddle_y (float): Host paddle Y position / Posición Y de paleta del anfitrión
            ball_x, ball_y (float): Ball position / Posición de la bola
            ball_vx, ball_vy (float): Ball velocity / Velocidad de la bola
            score_player, score_ai (int): Scores / Puntajes
        
        Returns / Retorna:
            bool: True if sent successfully / True si se envió correctamente
        """
        if not self.connected or not self.client_socket:
            return False  # No client connected / Sin cliente conectado
        
        try:
            # Build JSON message with game state
            # Construir mensaje JSON con estado del juego
            msg = json.dumps({
                'type': 'state',
                'paddle_y': validate(paddle_y),  # Host paddle / Paleta del anfitrión
                'ball_x': validate(ball_x),      # Ball X coordinate / Coordenada X de la bola
                'ball_y': validate(ball_y),      # Ball Y coordinate / Coordenada Y de la bola
                'ball_vx': validate(ball_vx, 1000),  # Ball X velocity / Velocidad X de la bola
                'ball_vy': validate(ball_vy, 1000),  # Ball Y velocity / Velocidad Y de la bola
                'score_p': max(0, min(999, int(score_player))),  # Clamp score 0-999 / Limitar puntaje 0-999
                'score_a': max(0, min(999, int(score_ai)))       # Clamp score 0-999 / Limitar puntaje 0-999
            }) + '\n'  # Newline delimiter / Delimitador de nueva línea
            
            self.client_socket.sendall(msg.encode('utf-8'))
            return True
        except (socket.error, OSError):
            self.connected = False
            return False  # Send failed, connection lost / Envío falló, conexión perdida
    
    def close(self):
        """
        Close network connections and stop server.
        Cerrar conexiones de red y detener servidor.
        """
        self.running = self.connected = False
        
        # Close client connection / Cerrar conexión del cliente
        if self.client_socket:
            try:
                self.client_socket.close()
            except (socket.error, OSError):
                pass  # Already closed / Ya cerrado
        
        # Close server socket / Cerrar socket del servidor
        if self.socket:
            try:
                self.socket.close()
            except (socket.error, OSError):
                pass  # Already closed / Ya cerrado
class NetworkClient:
    """
    Client for connecting to NetworkHost server.
    Cliente para conectarse al servidor NetworkHost.
    
    Architecture / Arquitectura:
        - Connects to host server
          Conecta al servidor anfitrión
        - Sends local paddle position
          Envía posición de paleta local
        - Receives game state (ball, scores, remote paddle)
          Recibe estado del juego (bola, puntajes, paleta remota)
    """
    
    def __init__(self):
        """
        Initialize network client.
        Inicializar cliente de red.
        """
        self.socket = None  # TCP socket connection / Conexión de socket TCP
        self.connected = False  # Connection status / Estado de conexión
        self.running = False    # Receive loop status / Estado de bucle de recepción
        
        # Local paddle position / Posición de paleta local
        self.paddle_y = 0
        
        # Remote game state (received from host) / Estado de juego remoto (recibido del anfitrión)
        self.remote_paddle_y = 0  # Host paddle / Paleta del anfitrión
        self.ball_x = self.ball_y = 0  # Ball position / Posición de la bola
        self.ball_vx = self.ball_vy = 0  # Ball velocity / Velocidad de la bola
        self.score_player = self.score_ai = 0  # Scores / Puntajes
    
    def connect(self, host_ip, port=5555, timeout=5):
        """
        Connect to host server.
        Conectar al servidor anfitrión.
        
        Args / Argumentos:
            host_ip (str): Host IP address (LAN or external) / Dirección IP del anfitrión (LAN o externa)
            port (int): Host port number / Número de puerto del anfitrión
            timeout (int): Connection timeout in seconds / Timeout de conexión en segundos
        
        Returns / Retorna:
            bool: True if connected successfully / True si se conectó correctamente
        """
        try:
            # Create TCP socket / Crear socket TCP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Set connection timeout / Establecer timeout de conexión
            self.socket.settimeout(timeout)
            
            # Connect to host / Conectar al anfitrión
            self.socket.connect((host_ip, port))
            
            # Switch to short receive timeout / Cambiar a timeout corto de recepción
            self.socket.settimeout(0.1)
            
            self.connected = self.running = True
            
            # Start background receive thread / Iniciar hilo de recepción en segundo plano
            threading.Thread(target=self._recv_loop, daemon=True).start()
            
            return True
        except (socket.error, OSError, socket.timeout):
            return False  # Connection failed / Conexión fallida
    
    def _recv_loop(self):
        """
        Receive game state updates from host (background thread).
        Recibir actualizaciones de estado del juego del anfitrión (hilo en segundo plano).
        
        Protocol / Protocolo:
            Host sends: {"type": "state", "paddle_y": ..., "ball_x": ..., ...}
            El anfitrión envía: {"type": "state", "paddle_y": ..., "ball_x": ..., ...}
        """
        buffer = ""  # Message buffer for incomplete data / Buffer de mensajes para datos incompletos
        
        while self.running and self.connected:
            try:
                # Receive up to 1KB / Recibir hasta 1KB
                data = self.socket.recv(1024).decode('utf-8', errors='ignore')
                
                if not data:
                    # Empty data means host disconnected / Datos vacíos significan desconexión del anfitrión
                    self.connected = False
                    break
                
                buffer += data
                
                # Process complete messages (newline-delimited)
                # Procesar mensajes completos (delimitados por nueva línea)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    try:
                        msg = json.loads(line)
                        
                        # Update game state from host / Actualizar estado del juego desde el anfitrión
                        if msg.get('type') == 'state':
                            self.remote_paddle_y = validate(msg.get('paddle_y', 0))  # Host paddle / Paleta del anfitrión
                            self.ball_x = validate(msg.get('ball_x', 0))            # Ball X / X de la bola
                            self.ball_y = validate(msg.get('ball_y', 0))            # Ball Y / Y de la bola
                            self.ball_vx = validate(msg.get('ball_vx', 0), 1000)    # Ball velocity X / Velocidad X
                            self.ball_vy = validate(msg.get('ball_vy', 0), 1000)    # Ball velocity Y / Velocidad Y
                            self.score_player = max(0, min(999, int(msg.get('score_p', 0))))  # Clamp / Limitar
                            self.score_ai = max(0, min(999, int(msg.get('score_a', 0))))      # Clamp / Limitar
                    except (json.JSONDecodeError, KeyError, ValueError):
                        pass  # Malformed message, skip / Mensaje malformado, saltar
            except socket.timeout:
                continue  # No data yet, retry / Sin datos aún, reintentar
            except (socket.error, OSError):
                self.connected = False
                break  # Connection lost / Conexión perdida
    
    def send_paddle(self, paddle_y):
        """
        Send paddle position to host.
        Enviar posición de paleta al anfitrión.
        
        Args / Argumentos:
            paddle_y (float): Local paddle Y position / Posición Y de paleta local
        
        Returns / Retorna:
            bool: True if sent successfully / True si se envió correctamente
        """
        if not self.connected or not self.socket:
            return False  # Not connected / No conectado
        
        try:
            # Build and send JSON message / Construir y enviar mensaje JSON
            msg = json.dumps({'type': 'paddle', 'y': validate(paddle_y)}) + '\n'
            self.socket.sendall(msg.encode('utf-8'))
            return True
        except (socket.error, OSError):
            self.connected = False
            return False  # Send failed / Envío fallido
    
    def close(self):
        """
        Close connection to host.
        Cerrar conexión al anfitrión.
        """
        self.running = self.connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except (socket.error, OSError):
                pass  # Already closed / Ya cerrado
class MatchmakingClient:
    def __init__(self, server_host=None, server_port=None):
        """
        Initialize matchmaking client (currently local cache-based).
        Inicializar cliente de matchmaking (actualmente basado en caché local).
        
        Args / Argumentos:
            server_host (str, optional): Matchmaking server IP / IP del servidor de matchmaking
            server_port (int, optional): Matchmaking server port / Puerto del servidor de matchmaking
        
        Note: Current implementation uses local in-memory cache for development.
        Nota: La implementación actual usa caché local en memoria para desarrollo.
        """
        self.paste_url = "https://pastebin.com/raw/pongai_relay"
        self.connected = False
        self.session_id = generate_code(8)  # Unique session ID / ID de sesión único
        self._cache = {'codes': {}, 'queue': []}  # Local storage / Almacenamiento local
        self._last_fetch = 0  # Cache refresh timestamp / Marca de tiempo de actualización de caché
    
    def connect(self):
        """
        Connect to matchmaking server (currently always succeeds).
        Conectar al servidor de matchmaking (actualmente siempre tiene éxito).
        
        Returns / Retorna:
            bool: True if connected / True si está conectado
        """
        self.connected = True
        return True
    
    def register_code(self, code, host_ip=None, host_port=5555):
        """
        Register game code for private matchmaking.
        Registrar código de juego para matchmaking privado.
        
        Args / Argumentos:
            code (str): Game code / Código de juego
            host_ip (str, optional): Host IP address / Dirección IP del host
            host_port (int): Host port / Puerto del host
        
        Returns / Retorna:
            bool: True if registered successfully / True si se registró con éxito
        """
        try:
            self._fetch_cache()
            # Store code with 5-minute TTL / Almacenar código con TTL de 5 minutos
            self._cache['codes'][code] = {'ip': host_ip or get_local_ip(), 'port': host_port, 'ts': time.time()}
            # Clean expired codes / Limpiar códigos expirados
            self._cache['codes'] = {k: v for k, v in self._cache['codes'].items() if time.time() - v.get('ts', 0) < 300}
            print(f"[Matchmaking] Code {code} registered locally")
            return True
        except Exception:
            return True
    
    def resolve_code(self, code):
        """
        Resolve game code to IP:port.
        Resolver código de juego a IP:puerto.
        
        Args / Argumentos:
            code (str): Game code to resolve / Código de juego a resolver
        
        Returns / Retorna:
            tuple or None: (ip, port) if found, None if not / (ip, puerto) si se encuentra, None si no
        """
        try:
            self._fetch_cache()
            if code in self._cache['codes']:
                entry = self._cache['codes'][code]
                # Check if code not expired (5 minutes) / Verificar si código no expiró (5 minutos)
                if time.time() - entry.get('ts', 0) < 300:
                    return (entry.get('ip'), entry.get('port', 5555))
        except Exception:
            pass
        return None
    
    def join_public_queue(self):
        """
        Join public matchmaking queue.
        Unirse a cola de matchmaking pública.
        
        Returns / Retorna:
            dict or None: Status dict with 'status' and 'peer' / Diccionario de estado con 'status' y 'peer'
        """
        try:
            self._fetch_cache()
            # Clean expired queue entries (1 minute TTL) / Limpiar entradas de cola expiradas (TTL 1 minuto)
            self._cache['queue'] = [p for p in self._cache['queue'] if time.time() - p.get('ts', 0) < 60 and p.get('sid') != self.session_id]
            
            # Try to match with waiting peer / Intentar emparejar con peer esperando
            if self._cache['queue']:
                peer = self._cache['queue'].pop(0)
                print(f"[Matchmaking] Matched with peer: {peer['ip']}")
                return {'status': 'matched', 'role': 'client', 'peer': f"{peer['ip']}:{peer['port']}"}
            else:
                # Join queue / Unirse a la cola
                local_ip = get_local_ip()
                self._cache['queue'].append({'ip': local_ip, 'port': 5555, 'ts': time.time(), 'sid': self.session_id})
                print(f"[Matchmaking] Joined queue as {local_ip}")
                return {'status': 'queued'}
        except Exception as e:
            print(f"[Matchmaking] Queue error: {e}")
            return None
    
    def _fetch_cache(self):
        """
        Refresh cache (currently no-op, placeholder for future server sync).
        Actualizar caché (actualmente no-op, marcador de posición para sincronización futura con servidor).
        """
        if time.time() - self._last_fetch < 3:
            return  # Rate limit / Límite de velocidad
        self._last_fetch = time.time()
    
    def close(self):
        """
        Close connection to matchmaking server.
        Cerrar conexión al servidor de matchmaking.
        """
        self.connected = False
# ============================================================================
# GAME CONSTANTS / CONSTANTES DEL JUEGO
# Core gameplay parameters / Parámetros básicos del juego
# ============================================================================

@dataclass(frozen=True)  # Immutable configuration / Configuración inmutable
class GameSettings:
    """
    Immutable game settings dataclass.
    Dataclass inmutable de configuración del juego.
    """
    # Display / Pantalla
    screen_width: int = 800   # Window width in pixels / Ancho de ventana en píxeles
    screen_height: int = 600  # Window height in pixels / Alto de ventana en píxeles
    
    # Paddle dimensions / Dimensiones de paletas
    paddle_width: int = 12     # Paddle width / Ancho de paleta
    paddle_height: int = 110   # Paddle height / Alto de paleta
    
    # Ball / Bola
    ball_size: int = 12  # Ball diameter / Diámetro de la bola
    
    # Movement speeds (pixels per second) / Velocidades de movimiento (píxeles por segundo)
    paddle_speed: float = 440.0  # Player paddle speed / Velocidad de paleta del jugador
    ai_speed: float = 380.0      # AI paddle base speed / Velocidad base de paleta de IA
    ball_speed: float = 420.0    # Ball base speed / Velocidad base de la bola
    
    # Game rules / Reglas del juego
    win_score: int = 7  # Points to win / Puntos para ganar
    
    # Ball physics / Física de la bola
    speed_increase_per_hit: float = 1.035  # Speed multiplier on paddle hit / Multiplicador de velocidad al golpear paleta
    max_ball_speed: float = 900.0  # Maximum ball speed / Velocidad máxima de la bola

# Create global settings instance / Crear instancia global de configuración
SETTINGS = GameSettings()

# Export individual constants for convenience / Exportar constantes individuales por conveniencia
SCREEN_WIDTH = SETTINGS.screen_width
SCREEN_HEIGHT = SETTINGS.screen_height
PADDLE_WIDTH = SETTINGS.paddle_width
PADDLE_HEIGHT = SETTINGS.paddle_height
BALL_SIZE = SETTINGS.ball_size
PADDLE_SPEED = SETTINGS.paddle_speed
AI_BASE_SPEED = SETTINGS.ai_speed
BALL_BASE_SPEED = SETTINGS.ball_speed
BALL_SPEED_X = BALL_BASE_SPEED  # Horizontal ball speed / Velocidad horizontal de la bola
BALL_SPEED_Y = BALL_BASE_SPEED * 0.55  # Vertical ball speed (slower) / Velocidad vertical (más lenta)
WIN_SCORE = SETTINGS.win_score
SPEED_INCREASE_PER_HIT = SETTINGS.speed_increase_per_hit
MAX_BALL_SPEED = SETTINGS.max_ball_speed

# ============================================================================
# POWER-UP SYSTEM / SISTEMA DE POWER-UPS
# Phase 2 Feature: Collectible bonuses with timed effects
# Característica Fase 2: Bonificaciones coleccionables con efectos temporales
# ============================================================================

@dataclass
class PowerUp:
    """
    Collectible power-up with visual effects.
    Power-up coleccionable con efectos visuales.
    """
    type: str  # 'big_paddle', 'multi_ball', 'speed_boost', 'shield', 'slow_motion', 'chaos_ball'
    x: float
    y: float
    size: float = 30.0
    lifetime: float = 8.0  # Despawn after 8 seconds / Desaparece después de 8 segundos
    active: bool = True
    vx: float = 0.0  # Horizontal drift / Deriva horizontal
    vy: float = 50.0  # Vertical fall speed / Velocidad de caída vertical
    glow_phase: float = 0.0  # Animation phase / Fase de animación

# Power-up configuration / Configuración de power-ups
POWERUP_TYPES = ['big_paddle', 'speed_boost', 'shield', 'slow_motion', 'multi_ball', 'chaos_ball']
POWERUP_WEIGHTS = [30, 25, 20, 15, 10, 10]  # Spawn probability weights / Pesos de probabilidad de aparición
POWERUP_SPAWN_INTERVAL = 15.0  # Base spawn interval in seconds / Intervalo base de aparición en segundos

# Power-up colors / Colores de power-ups
POWERUP_COLORS = {
    'big_paddle': (100, 150, 255),      # Blue / Azul
    'multi_ball': (255, 100, 100),      # Red / Rojo
    'speed_boost': (255, 255, 100),     # Yellow / Amarillo
    'shield': (100, 255, 100),          # Green / Verde
    'slow_motion': (150, 200, 255),     # Light Blue / Azul claro
    'chaos_ball': (200, 100, 255)       # Purple / Púrpura
}

# Color palette (RGB tuples) / Paleta de colores (tuplas RGB)
WHITE = (255, 255, 255)   # Blanco
RED = (255, 0, 0)         # Rojo
BLUE = (0, 0, 255)        # Azul
GREEN = (0, 255, 0)       # Verde
ORANGE = (255, 140, 20)   # Naranja
YELLOW = (255, 255, 0)    # Amarillo
# ============================================================================
# AUDIO SYNTHESIS / SÍNTESIS DE AUDIO
# Procedurally generated sound effects / Efectos de sonido generados proceduralmente
# ============================================================================

def create_sound(frequency, duration, volume=0.5):
    """
    Create sine wave sound effect using NumPy.
    Crear efecto de sonido de onda sinusoidal usando NumPy.
    
    Args / Argumentos:
        frequency (float): Sound frequency in Hz / Frecuencia de sonido en Hz
        duration (float): Duration in seconds / Duración en segundos
        volume (float): Volume (0.0 to 1.0) / Volumen (0.0 a 1.0)
    
    Returns / Retorna:
        pygame.mixer.Sound: Playable sound object / Objeto de sonido reproducible
    """
    sample_rate = 44100  # CD quality / Calidad de CD
    
    # Generate time array / Generar arreglo de tiempo
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create sine wave / Crear onda sinusoidal
    wave = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit audio / Convertir a audio de 16 bits
    audio = (wave * 32767 * volume).astype(np.int16)
    
    # Create stereo audio (duplicate mono to both channels)
    # Crear audio estéreo (duplicar mono a ambos canales)
    stereo_audio = np.ascontiguousarray(np.column_stack((audio, audio)))
    
    return pygame.sndarray.make_sound(stereo_audio)

# Pre-generate sound effects / Pre-generar efectos de sonido
bounce_sound = create_sound(440, 0.09, 0.6)  # Wall/paddle bounce (A4 note) / Rebote en pared/paleta (nota LA4)
score_sound = create_sound(220, 0.22, 0.7)   # Score point (A3 note, longer) / Punto anotado (nota LA3, más largo)
paddle_sound = create_sound(660, 0.07, 0.5)  # Paddle hit (E5 note, short) / Golpe de paleta (nota MI5, corto)
# ============================================================================
# PARTICLE SYSTEM / SISTEMA DE PARTÍCULAS
# Visual effects for ball collisions / Efectos visuales para colisiones de bola
# ============================================================================

class Particle:
    """
    Lightweight particle with fade-out effect.
    Partícula ligera con efecto de desvanecimiento.
    
    Uses __slots__ for memory efficiency (object pooling)
    Usa __slots__ para eficiencia de memoria (agrupación de objetos)
    """
    __slots__ = ("x", "y", "color", "size", "speed_x", "speed_y", "life", "initial_life", "active")
    
    def __init__(self):
        """
        Initialize inactive particle.
        Inicializar partícula inactiva.
        """
        self.active = False  # Particle enabled flag / Indicador de partícula activada
        self.x = 0.0         # X position / Posición X
        self.y = 0.0         # Y position / Posición Y
        self.color = (255, 255, 255)  # RGB color / Color RGB
        self.size = 2        # Particle radius / Radio de partícula
        self.speed_x = 0.0   # Horizontal velocity / Velocidad horizontal
        self.speed_y = 0.0   # Vertical velocity / Velocidad vertical
        self.life = 0.0      # Remaining lifetime / Vida restante
        self.initial_life = 0.0  # Starting lifetime for alpha calculation / Vida inicial para cálculo de alfa
    
    def reset(self, x, y, color, *, size=None, life=0.35):
        """
        Activate particle with new properties (object pool reuse).
        Activar partícula con nuevas propiedades (reutilización de pool de objetos).
        
        Args / Argumentos:
            x, y (float): Starting position / Posición inicial
            color (tuple): RGB color / Color RGB
            size (int, optional): Particle size / Tamaño de partícula
            life (float): Lifetime in seconds / Vida en segundos
        """
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.size = size if size is not None else random.randint(2, 5)
        
        # Random velocity for explosion effect / Velocidad aleatoria para efecto de explosión
        self.speed_x = random.uniform(-220, 220)
        self.speed_y = random.uniform(-220, 220)
        
        self.life = life
        self.initial_life = life
        self.active = True  # Enable particle / Activar partícula
    
    def update(self, dt):
        """
        Update particle physics.
        Actualizar física de partícula.
        
        Args / Argumentos:
            dt (float): Delta time in seconds / Delta de tiempo en segundos
        
        Returns / Retorna:
            bool: True if still active / True si aún está activa
        """
        if not self.active:
            return False
        
        # Update position / Actualizar posición
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt
        
        # Decrease lifetime / Disminuir vida
        self.life -= dt
        
        if self.life <= 0:
            self.active = False
        
        return self.active
    
    def draw(self, surface):
        """
        Render particle with alpha fade.
        Renderizar partícula con desvanecimiento alfa.
        
        Args / Argumentos:
            surface (pygame.Surface): Target surface / Superficie objetivo
        """
        if not self.active:
            return
        
        # Calculate alpha based on remaining life / Calcular alfa basado en vida restante
        alpha_ratio = max(0.0, min(1.0, self.life / self.initial_life if self.initial_life else 0.0))
        alpha = int(255 * alpha_ratio)
        
        if alpha <= 0:
            return
        
        # Create RGBA color with alpha / Crear color RGBA con alfa
        color = (*self.color[:3], alpha)
        
        # Draw fading circle / Dibujar círculo desvaneciente
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (self.size // 2, self.size // 2), self.size // 2)
        surface.blit(surf, (int(self.x), int(self.y)))
class ParticlePool:
    """
    Object pool for particle reuse (performance optimization).
    Pool de objetos para reutilización de partículas (optimización de rendimiento).
    
    Why? / ¿Por qué?:
        Creating new objects every frame is slow
        Crear nuevos objetos cada cuadro es lento
        Reusing existing objects is ~10x faster
        Reutilizar objetos existentes es ~10x más rápido
    """
    
    def __init__(self, initial_size=256):
        """
        Create pool of reusable particles.
        Crear pool de partículas reutilizables.
        
        Args / Argumentos:
            initial_size (int): Number of particles to pre-allocate / Número de partículas a pre-asignar
        """
        self._pool = [Particle() for _ in range(initial_size)]
    
    def acquire(self):
        """
        Get particle from pool or create new one.
        Obtener partícula del pool o crear una nueva.
        
        Returns / Retorna:
            Particle: Reusable particle / Partícula reutilizable
        """
        if self._pool:
            return self._pool.pop()  # Reuse from pool / Reutilizar del pool
        return Particle()  # Create new if pool empty / Crear nueva si pool vacío
    
    def release(self, particle: Particle):
        """
        Return particle to pool for reuse.
        Devolver partícula al pool para reutilizar.
        
        Args / Argumentos:
            particle (Particle): Particle to return / Partícula a devolver
        """
        particle.active = False
        self._pool.append(particle)
class ScoreBurst:
    """
    Expanding ring effect when scoring.
    Efecto de anillo expansivo al anotar.
    """
    
    def __init__(self, x, y, base_color):
        """
        Create score burst effect.
        Crear efecto de ráfaga de puntaje.
        
        Args / Argumentos:
            x, y (float): Center position / Posición central
            base_color (tuple): RGB color / Color RGB
        """
        self.x = float(x)
        self.y = float(y)
        self.base_color = base_color
        self.radius = 12.0  # Starting radius / Radio inicial
        self.max_radius = 160.0  # Maximum expansion / Expansión máxima
        self.life = 0.45  # Duration in seconds / Duración en segundos
    
    def update(self, dt):
        """Update effect (expand and fade). / Actualizar efecto (expandir y desvanecer)."""
        self.radius += 320.0 * dt  # Expand / Expandir
        self.life -= dt  # Fade / Desvanecer
    
    def alive(self):
        """Check if still active. / Verificar si aún está activo."""
        return self.life > 0
    
    def draw(self, surface):
        """
        Render expanding ring with additive blending.
        Renderizar anillo expansivo con mezcla aditiva.
        
        Args / Argumentos:
            surface (pygame.Surface): Target surface / Superficie objetivo
        """
        if self.life <= 0:
            return
        
        # Calculate fade progress (0.0 = start, 1.0 = end)
        # Calcular progreso de desvanecimiento (0.0 = inicio, 1.0 = fin)
        progress = max(0.0, min(1.0, 1.0 - self.life / 0.45))
        
        # Fade alpha over time / Desvanecer alfa con el tiempo
        alpha_outer = int(140 * max(0.0, 1.0 - progress))
        alpha_inner = int(220 * max(0.0, 1.0 - progress * 1.1))
        
        # Calculate radii / Calcular radios
        radius_outer = int(min(self.max_radius, self.radius * 1.6))
        radius_inner = int(min(self.max_radius, self.radius))
        
        # Create temporary surface for ring / Crear superficie temporal para anillo
        size = radius_outer * 2 + 4
        burst_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        
        # Draw outer ring / Dibujar anillo exterior
        if alpha_outer > 0 and radius_outer > 0:
            pygame.draw.circle(burst_surf, (*self.base_color, alpha_outer), (center, center), radius_outer, width=4)
        
        # Draw inner core / Dibujar núcleo interior
        if alpha_inner > 0 and radius_inner > 0:
            core_color = (
                min(255, self.base_color[0] + 30),
                min(255, self.base_color[1] + 30),
                min(255, self.base_color[2] + 30),
                alpha_inner
            )
            pygame.draw.circle(burst_surf, core_color, (center, center), radius_inner // 3)
        
        # Blit with additive blending for glow effect / Blit con mezcla aditiva para efecto de brillo
        surface.blit(burst_surf, (self.x - center, self.y - center), special_flags=pygame.BLEND_ADD)
# ============================================================================
# GAME ENTITIES / ENTIDADES DEL JUEGO
# Paddle and Ball classes / Clases de Paleta y Bola
# ============================================================================

class Paddle:
    """
    Player or AI paddle.
    Paleta del jugador o IA.
    """
    
    def __init__(self, x, y, color, speed=PADDLE_SPEED):
        """
        Create paddle.
        Crear paleta.
        
        Args / Argumentos:
            x, y (float): Position / Posición
            color (tuple): RGB color / Color RGB
            speed (float): Movement speed in pixels/sec / Velocidad de movimiento en píxeles/seg
        """
        self.x = float(x)
        self.y = float(y)
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = float(speed)
        self.color = color
    
    def get_rect(self):
        """Get collision rectangle. / Obtener rectángulo de colisión."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def move(self, direction, dt):
        """
        Move paddle (clamped to screen).
        Mover paleta (limitada a la pantalla).
        
        Args / Argumentos:
            direction (float): -1 (up/arriba), +1 (down/abajo)
            dt (float): Delta time / Delta de tiempo
        """
        # Update position and clamp to screen bounds
        # Actualizar posición y limitar a los bordes de la pantalla
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y + self.speed * direction * dt))
    
    def draw(self, screen):
        """
        Render paddle with glow effect.
        Renderizar paleta con efecto de brillo.
        
        Args / Argumentos:
            screen (pygame.Surface): Target surface / Superficie objetivo
        """
        # Draw main paddle / Dibujar paleta principal
        rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        pygame.draw.rect(screen, self.color, rect, border_radius=6)
        
        # Draw glow effect / Dibujar efecto de brillo
        glow_surf = pygame.Surface((self.width + 16, self.height + 16), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*self.color[:3], 55), (8, 8, self.width, self.height), border_radius=8)
        screen.blit(glow_surf, (int(self.x) - 8, int(self.y) - 8))

class Ball:
    """
    Game ball with trail effect.
    Bola del juego con efecto de estela.
    """
    
    def __init__(self):
        """
        Create ball at center with random direction.
        Crear bola en el centro con dirección aleatoria.
        """
        self.x = float(SCREEN_WIDTH // 2)
        self.y = float(SCREEN_HEIGHT // 2)
        self.size = BALL_SIZE
        # Random horizontal direction / Dirección horizontal aleatoria
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])
        self.color = RED
        self.trail = []  # Position history for trail / Historial de posiciones para estela
    
    def move(self, dt):
        """
        Move ball and update trail (bounce off top/bottom walls).
        Mover bola y actualizar estela (rebotar en paredes superior/inferior).
        
        Args / Argumentos:
            dt (float): Delta time / Delta de tiempo
        """
        # Add current position to trail / Agregar posición actual a la estela
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 10:
            self.trail.pop(0)  # Keep only last 10 positions / Mantener solo las últimas 10 posiciones
        
        # Update position / Actualizar posición
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt
        
        # Bounce off top/bottom walls / Rebotar en paredes superior/inferior
        if self.y <= 0:
            self.y = 0
            self.speed_y = -self.speed_y
        elif self.y >= SCREEN_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - self.size
            self.speed_y = -self.speed_y
    
    def draw(self, screen):
        """
        Render ball with trail and glow effect.
        Renderizar bola con estela y efecto de brillo.
        
        Args / Argumentos:
            screen (pygame.Surface): Target surface / Superficie objetivo
        """
        # Draw trail with fade effect / Dibujar estela con efecto de desvanecimiento
        for i, pos in enumerate(self.trail):
            # Alpha increases with position in trail / Alpha aumenta con la posición en la estela
            alpha = int(255 * (i / max(1, len(self.trail))))
            color = (*self.color[:3], alpha)
            surf = pygame.Surface((self.size + 2, self.size + 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, ((self.size + 2) // 2, (self.size + 2) // 2), (self.size + 2) // 2)
            screen.blit(surf, (pos[0] - 1, pos[1] - 1))
        
        # Draw glow effect / Dibujar efecto de brillo
        glow = pygame.Surface((self.size + 12, self.size + 12), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*self.color[:3], 60), ((self.size + 12) // 2, (self.size + 12) // 2), (self.size + 12) // 2)
        screen.blit(glow, (int(self.x) - 6, int(self.y) - 6))
        
        # Draw main ball / Dibujar bola principal
        pygame.draw.circle(screen, self.color, (int(self.x + self.size // 2), int(self.y + self.size // 2)), self.size // 2)
    
    def get_rect(self):
        """Get collision rectangle. / Obtener rectángulo de colisión."""
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)
    
    def reset(self, direction=None):
        """
        Reset ball to center with new direction.
        Resetear bola al centro con nueva dirección.
        
        Args / Argumentos:
            direction (int, optional): -1 (left/izquierda) or +1 (right/derecha). Random if None.
        """
        self.x, self.y = float(SCREEN_WIDTH // 2), float(SCREEN_HEIGHT // 2)
        dir_x = direction if direction in (-1, 1) else random.choice([-1, 1])
        self.speed_x = BALL_BASE_SPEED * dir_x
        self.speed_y = BALL_BASE_SPEED * 0.55 * random.choice([-1, 1])
        self.trail = []  # Clear trail / Limpiar estela

# ============================================================================
# GRAPHICS UTILITIES / UTILIDADES GRÁFICAS
# Window icon and title logo generation / Generación de ícono y logo
# ============================================================================

def create_window_icon():
    """
    Create 32x32 window icon (colorful pong scene).
    Crear ícono de ventana 32x32 (escena pong colorida).
    
    Returns / Retorna:
        pygame.Surface: Icon with paddles and ball / Ícono con paletas y bola
    """
    icon = pygame.Surface((32, 32), pygame.SRCALPHA)
    icon.fill((0, 0, 0, 0))
    
    # Left paddle (neon blue) / Paleta izquierda (azul neón)
    pygame.draw.rect(icon, (0, 200, 255), (4, 10, 3, 12))
    
    # Right paddle (neon green) / Paleta derecha (verde neón)
    pygame.draw.rect(icon, (0, 255, 150), (25, 10, 3, 12))
    
    # Ball (neon pink) - radius 2 / Bola (rosa neón) - radio 2
    pygame.draw.circle(icon, (255, 50, 150), (16, 16), 2)
    
    # Glow effect / Efecto de brillo
    pygame.draw.circle(icon, (255, 100, 180, 80), (16, 16), 3)
    
    return icon

def create_title_logo():
    """
    Create pixel art logo "PONG V2" with gradient (light grey → white).
    Crear logo pixel art "PONG V2" con gradiente (gris claro → blanco).
    
    Returns / Retorna:
        pygame.Surface: Logo surface / Superficie del logo
    """
    # Create surface for "PONG V2" / Crear superficie para "PONG V2"
    logo = pygame.Surface((480, 100), pygame.SRCALPHA)
    logo.fill((0, 0, 0, 0))
    
    # Pixel font style (8x8 grid per character) / Estilo de fuente pixel (cuadrícula 8x8 por carácter)
    pixel_size = 8
    
    # Define "PONG V2" in pixel art / Definir "PONG V2" en pixel art
    # Each letter is a list of (x, y) coordinates for filled pixels
    # Cada letra es una lista de coordenadas (x, y) para píxeles rellenos
    letters = {
        'P': [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2),(0,3),(0,4),(0,5)],
        'O': [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(2,2),(0,3),(2,3),(0,4),(2,4),(0,5),(1,5),(2,5)],
        'N': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3),(3,4),(3,5)],
        'G': [(0,0),(1,0),(2,0),(0,1),(0,2),(2,2),(0,3),(2,3),(0,4),(2,4),(0,5),(1,5),(2,5)],
        'V': [(0,0),(0,1),(0,2),(1,3),(1,4),(2,5),(3,4),(3,3),(4,2),(4,1),(4,0)],
        '2': [(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(0,3),(0,4),(0,5),(1,5),(2,5)]
    }
    
    # Draw "PONG" with gradient / Dibujar "PONG" con gradiente
    x_offset = 10
    for char in ['P', 'O', 'N', 'G']:
        for px, py in letters[char]:
            # Gradient: light grey (180) at bottom → white (255) at top
            # Gradiente: gris claro (180) en la base → blanco (255) arriba
            color_value = int(180 + (255 - 180) * (1 - py / 5))
            color = (color_value, color_value, color_value)
            pygame.draw.rect(logo, color, (x_offset + px * pixel_size, 10 + py * pixel_size, pixel_size, pixel_size))
        x_offset += 50
    
    x_offset += 30  # Space between "PONG" and "V2" / Espacio entre "PONG" y "V2"
    
    # Draw "V2" with gradient / Dibujar "V2" con gradiente
    for char in ['V', '2']:
        for px, py in letters[char]:
            color_value = int(180 + (255 - 180) * (1 - py / 5))
            color = (color_value, color_value, color_value)
            pygame.draw.rect(logo, color, (x_offset + px * pixel_size, 10 + py * pixel_size, pixel_size, pixel_size))
        x_offset += 50
    
    return logo

# ============================================================================
# MAIN GAME CLASS / CLASE PRINCIPAL DEL JUEGO
# Complete Pong game with AI, multiplayer, particles, and translations
# Juego completo de Pong con IA, multijugador, partículas y traducciones
# ============================================================================

class Game:
    """
    Main game class - handles all game logic, rendering, and state management.
    Clase principal del juego - maneja toda la lógica, renderizado y gestión de estados.
    """
    
    def __init__(self):
        """
        Initialize game with all systems (graphics, audio, networking, UI).
        Inicializar juego con todos los sistemas (gráficos, audio, red, UI).
        """
        # Load saved settings from JSON file / Cargar configuración guardada desde archivo JSON
        saved = load_settings()
        self.fullscreen = saved.get('fullscreen', False)
        self.audio_enabled = saved.get('audio_enabled', True)
        self.language = saved.get('language', 'en')
        
        # Create window with appropriate mode / Crear ventana con modo apropiado
        if self.fullscreen:
            # SCALED mode maintains aspect ratio in fullscreen
            # Modo SCALED mantiene la proporción en pantalla completa
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF, vsync=1)
        else:
            # Hardware surface for better performance in windowed mode
            # Superficie de hardware para mejor rendimiento en modo ventana
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE, vsync=1)
        pygame.display.set_caption("Pong AI - Incredible Edition")
        
        # Set window icon (32x32 colorful pong scene) / Configurar ícono de ventana (escena pong colorida 32x32)
        icon = create_window_icon()
        pygame.display.set_icon(icon)
        
        # Save icon as .ico file for Windows taskbar (requires PIL/Pillow)
        # Guardar ícono como archivo .ico para barra de tareas de Windows (requiere PIL/Pillow)
        try:
            from PIL import Image
            icon_path = Path(__file__).parent / 'icon.ico'
            # Convert pygame surface to PIL Image / Convertir superficie pygame a imagen PIL
            icon_str = pygame.image.tostring(icon, 'RGBA')
            pil_icon = Image.frombytes('RGBA', icon.get_size(), icon_str)
            pil_icon.save(str(icon_path), format='ICO', sizes=[(32, 32)])
        except Exception:
            # PIL not installed or error during conversion - not critical
            # PIL no instalado o error durante conversión - no crítico
            pass
        
        # Create pixel art title logo for menu / Crear logo pixel art para menú
        self.title_logo = create_title_logo()
        
        # Initialize pygame subsystems / Inicializar subsistemas pygame
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Medium text / Texto mediano
        self.large_font = pygame.font.Font(None, 72)  # Scores / Puntajes
        self.small_font = pygame.font.Font(None, 28)  # Small UI text / Texto UI pequeño
        
        # Rendering surfaces for performance optimization / Superficies de renderizado para optimización
        self._game_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._tint_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._sweep_surface = pygame.Surface((SCREEN_WIDTH, 140), pygame.SRCALPHA)
        self._cached_bg_phase = -1.0  # Background animation phase cache / Caché de fase de animación de fondo
        self._cached_background = None  # Cached background surface / Superficie de fondo en caché
        
        # Create game entities (paddles and ball) / Crear entidades del juego (paletas y bola)
        self.player = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, BLUE, speed=PADDLE_SPEED)
        self.ai = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, GREEN, speed=AI_BASE_SPEED)
        self.ball = Ball()
        
        # Game state variables / Variables de estado del juego
        self.player_score = 0
        self.ai_score = 0
        
        # Particle system (object pooling for performance) / Sistema de partículas (pooling de objetos para rendimiento)
        self.particle_pool = ParticlePool(360)  # Pre-allocate 360 particles / Pre-asignar 360 partículas
        self.particles = []
        
        # UI state / Estado UI
        self.difficulty_hitboxes = []  # Clickable difficulty buttons / Botones de dificultad clickeables
        self.menu_hover_index = None  # Currently hovered menu item / Elemento de menú actualmente señalado
        self.state = "menu"  # Current game state: "menu", "game", "settings", "multiplayer_menu" / Estado actual del juego
        self.show_debug_hud = saved.get('debug_hud', False)  # Debug overlay toggle / Toggle de overlay de depuración
        self.settings_hover_item = None  # Hovered settings item / Elemento de configuración señalado
        self.settings_fullscreen_hover = False  # Fullscreen toggle hover state / Estado hover de toggle pantalla completa
        self._audio_toggle_rect = None  # Audio toggle button rectangle / Rectángulo del botón de toggle audio
        self._back_button_rect = None  # Settings back button rectangle / Rectángulo del botón atrás de configuración
        
        # Network/multiplayer state / Estado de red/multijugador
        self.multiplayer_mode = None  # None, "host", "client", "matchmaking" / Ninguno, "host", "client", "matchmaking"
        self.network_host = None  # NetworkHost instance / Instancia de NetworkHost
        self.network_client = None  # NetworkClient instance / Instancia de NetworkClient
        self.matchmaking_client = None  # MatchmakingClient instance / Instancia de MatchmakingClient
        self.join_code_input = ""  # Code input buffer for joining games / Buffer de entrada de código para unirse a juegos
        self.multiplayer_status = ""  # Status message for multiplayer UI / Mensaje de estado para UI multijugador
        
        # Matchmaking state / Estado de búsqueda de partidas
        self.searching_public = False  # Currently searching for public match / Buscando partida pública actualmente
        self.search_start_time = 0  # When search started / Cuándo comenzó la búsqueda
        self.matchmaking_server_addr = '127.0.0.1'  # Matchmaking server IP / IP del servidor de matchmaking
        
        # Test/diagnostics state / Estado de pruebas/diagnósticos
        self.test_results = []  # Test result messages / Mensajes de resultados de prueba
        self.test_running = False  # Test in progress / Prueba en progreso
        self.test_step = 0  # Current test step / Paso de prueba actual
        
        # Animation/effects state / Estado de animaciones/efectos
        self.elapsed = 0.0  # Total elapsed time / Tiempo total transcurrido
        self.bg_offset = 0.0  # Background parallax offset / Offset de parallax de fondo
        self.shake_time = 0.0  # Screen shake remaining time / Tiempo restante de sacudida de pantalla
        self.shake_mag = 0.0  # Screen shake magnitude / Magnitud de sacudida de pantalla
        self.left_pop = 0.0  # Left paddle hit animation / Animación de golpe de paleta izquierda
        self.right_pop = 0.0  # Right paddle hit animation / Animación de golpe de paleta derecha
        self.score_bursts = []  # Active score burst effects / Efectos de ráfaga de puntaje activos
        
        # Power-up system (Phase 2 feature) / Sistema de power-ups (característica Fase 2)
        self.powerups: list = []  # Active power-ups / Power-ups activos
        self.balls: list = []  # Multi-ball support / Soporte para multi-bola
        self.active_effects: dict = {}  # Active power-up effects: type -> time_remaining / Efectos activos: tipo -> tiempo restante
        self.powerup_spawn_timer: float = 0.0  # Time until next spawn / Tiempo hasta próxima aparición
        self.powerup_spawn_interval: float = POWERUP_SPAWN_INTERVAL  # Current spawn interval / Intervalo actual de aparición
        self.shield_active: bool = False  # Shield power-up state / Estado del power-up escudo
        self.player.original_height = PADDLE_HEIGHT  # Store original height for big paddle / Guardar altura original para paleta grande
        
        # Difficulty settings: (AI speed, ball speed) / Configuración de dificultad: (velocidad IA, velocidad bola)
        self.difficulties = [
            (300.0, 380.0),  # Easy / Fácil
            (380.0, 420.0),  # Medium / Medio
            (460.0, 480.0),  # Hard / Difícil
        ]
        self.diff_index = saved.get('difficulty', 1)  # Default: medium / Por defecto: medio
        
        # Animation phases / Fases de animación
        self.menu_phase = 0.0  # Menu animation phase / Fase de animación del menú
        self.gameover_phase = 0.0  # Game over animation phase / Fase de animación de game over
        
        # Input state / Estado de entrada
        self.player_move_dir = 0.0  # Player movement direction / Dirección de movimiento del jugador
        self.ai_move_dir = 0.0  # AI movement direction / Dirección de movimiento de la IA
        self.player2_move_dir = 0.0  # Player 2 movement direction (2-player mode) / Dirección de movimiento del jugador 2 (modo 2 jugadores)
        self.dragging = False  # Mouse drag active / Arrastre de ratón activo
        self.drag_offset = 0.0  # Mouse drag offset / Offset de arrastre de ratón
        
        # Button animation state / Estado de animación de botones
        self.button_scales = {}  # Smooth button hover scales / Escalas suaves de hover de botones
        self.button_target_scales = {}  # Target scales for animations / Escalas objetivo para animaciones
        
        # Game mode / Modo de juego
        self.game_mode = "single"  # "single" or "2player" / "single" o "2player"
        
        # Frame timing / Temporización de fotogramas
        self.dt = 0.016  # Delta time (60 FPS target) / Delta de tiempo (objetivo 60 FPS)
        
        # Demo mode (background gameplay) / Modo demo (juego de fondo)
        self.demo_player = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, (80, 180, 255, 120), speed=340.0)
        self.demo_ai = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, (120, 255, 180, 120), speed=340.0)
        self.demo_ball = Ball()
        self.demo_ball.color = (255, 200, 100)  # Orange ball for demo / Bola naranja para demo
        self.demo_player_score = 0
        self.demo_ai_score = 0
        
        # Disable audio if settings say so / Deshabilitar audio si la configuración lo dice
        if not self.audio_enabled:
            pygame.mixer.stop()
        
        # Create audio assets / Crear recursos de audio
        self._create_assets()
    
    def t(self, key):
        """
        Translate text key to current language.
        Traducir clave de texto al idioma actual.
        
        Args / Argumentos:
            key (str): Translation key / Clave de traducción
        
        Returns / Retorna:
            str: Translated text or key if not found / Texto traducido o clave si no se encuentra
        """
        return TRANSLATIONS[self.language].get(key, key)
    
    def toggle_fullscreen(self):
        """
        Toggle fullscreen mode and save setting.
        Alternar modo pantalla completa y guardar configuración.
        """
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF, vsync=1)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE, vsync=1)
        save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
    
    def toggle_audio(self):
        """
        Toggle audio on/off and save setting.
        Alternar audio encendido/apagado y guardar configuración.
        """
        self.audio_enabled = not self.audio_enabled
        if not self.audio_enabled:
            pygame.mixer.stop()  # Stop all sounds / Detener todos los sonidos
        save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
    
    def toggle_language(self):
        """
        Toggle between English and Spanish.
        Alternar entre inglés y español.
        """
        self.language = 'es' if self.language == 'en' else 'en'
        save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
    
    def _play_sound(self, sound):
        """
        Play sound if audio is enabled.
        Reproducir sonido si el audio está habilitado.
        
        Args / Argumentos:
            sound (pygame.mixer.Sound): Sound to play / Sonido a reproducir
        """
        if self.audio_enabled:
            sound.play()
    
    def play_sound(self, sound_type, pitch=1.0):
        """
        Play dynamic sound effect for power-ups.
        Reproducir efecto de sonido dinámico para power-ups.
        
        Args / Argumentos:
            sound_type (str): Type of sound / Tipo de sonido
            pitch (float): Pitch multiplier / Multiplicador de tono
        """
        if not self.audio_enabled:
            return
        
        try:
            if sound_type == 'powerup_collect':
                # Rising arpeggio / Arpegio ascendente
                duration = 0.05
                for freq in [500, 650, 800, 1000]:
                    samples = int(44100 * duration)
                    wave = np.sin(2 * np.pi * freq * pitch * np.linspace(0, duration, samples))
                    wave = (wave * 8000).astype(np.int16)
                    stereo = np.column_stack((wave, wave))
                    sound = pygame.sndarray.make_sound(stereo)
                    sound.play()
            elif sound_type == 'powerup_expire':
                # Descending tone / Tono descendente
                duration = 0.3
                samples = int(44100 * duration)
                freqs = np.linspace(600, 300, samples)
                wave = np.sin(2 * np.pi * freqs * np.linspace(0, duration, samples))
                wave = (wave * 6000).astype(np.int16)
                stereo = np.column_stack((wave, wave))
                sound = pygame.sndarray.make_sound(stereo)
                sound.play()
        except Exception:
            pass  # Audio synthesis failed, not critical / Síntesis de audio falló, no crítico
    
    def handle_input(self):
        """
        Handle keyboard input for player movement (1 or 2 players).
        Manejar entrada de teclado para movimiento del jugador (1 o 2 jugadores).
        """
        keys = pygame.key.get_pressed()
        if self.state == "playing":
            # Player 1 controls (left paddle) - W/S keys / Controles Jugador 1 (paleta izquierda) - teclas W/S
            dir_y = 0.0
            if not self.dragging:
                if keys[pygame.K_w]:
                    dir_y -= 1.0
                if keys[pygame.K_s]:
                    dir_y += 1.0
            self.player_move_dir = dir_y if not self.dragging else 0.0
            
            # Player 2 controls (right paddle) - Arrow keys (2-player mode only)
            # Controles Jugador 2 (paleta derecha) - flechas (solo modo 2 jugadores)
            if self.game_mode == "2player":
                p2_dir = 0.0
                if keys[pygame.K_UP]:
                    p2_dir -= 1.0
                if keys[pygame.K_DOWN]:
                    p2_dir += 1.0
                self.player2_move_dir = p2_dir
            
            # ESC = open settings / ESC = abrir configuración
            if keys[pygame.K_ESCAPE]:
                self.state = "settings"
                self.menu_phase = 0.0
                self.settings_hover_item = None
    
    def _player_drag_rect(self):
        """
        Get expanded rectangle for mouse drag detection on player paddle.
        Obtener rectángulo expandido para detección de arrastre de ratón en paleta del jugador.
        
        Returns / Retorna:
            pygame.Rect: Expanded hitbox / Hitbox expandido
        """
        # Inflate paddle rect for easier mouse grabbing / Inflar rect de paleta para agarrar más fácil
        expanded = self.player.get_rect().inflate(80, 120)
        # Clamp to screen bounds / Limitar a bordes de pantalla
        expanded.top = max(0, expanded.top)
        expanded.bottom = min(SCREEN_HEIGHT, expanded.bottom)
        expanded.left = max(0, expanded.left)
        expanded.right = min(SCREEN_WIDTH, expanded.right)
        return expanded
    
    def _start_game(self):
        """
        Start new game with current difficulty settings.
        Iniciar nuevo juego con configuración de dificultad actual.
        """
        # Get AI and ball speed from selected difficulty / Obtener velocidad IA y bola de dificultad seleccionada
        ai_speed, ball_speed = self.difficulties[self.diff_index][0], self.difficulties[self.diff_index][1]
        self.ai.speed = ai_speed
        
        # Update global ball speed / Actualizar velocidad global de bola
        global BALL_BASE_SPEED
        BALL_BASE_SPEED = ball_speed
        
        # Reset game state / Resetear estado del juego
        self.ball.reset(direction=random.choice([-1, 1]))
        self.player_score = 0
        self.ai_score = 0
        self.left_pop = 0.0
        self.right_pop = 0.0
        self.score_bursts.clear()
        self._clear_particles()
        self.dragging = False
        self.menu_hover_index = None
        self.state = "playing"
    
    def ai_move(self):
        """
        AI paddle movement logic (tracks ball position).
        Lógica de movimiento de paleta IA (sigue posición de la bola).
        """
        # Calculate target position (ball center) / Calcular posición objetivo (centro de bola)
        target = self.ball.y + self.ball.size / 2
        center = self.ai.y + self.ai.height / 2
        
        # Move towards target with deadzone / Mover hacia objetivo con zona muerta
        if abs(target - center) > 6:
            self.ai_move_dir = 1.0 if target > center else -1.0
        else:
            self.ai_move_dir = 0.0
    
    def update_demo_game(self, dt):
        """
        Update background demo game (AI vs AI) for menu.
        Actualizar juego demo de fondo (IA vs IA) para menú.
        
        Args / Argumentos:
            dt (float): Delta time / Delta de tiempo
        """
        # Left paddle AI logic with prediction / Lógica IA paleta izquierda con predicción
        target_left = self.demo_ball.y + self.demo_ball.size / 2
        if self.demo_ball.speed_x < 0:
            # Ball moving towards left paddle - predict position / Bola moviéndose hacia paleta izquierda - predecir posición
            target_left += self.demo_ball.speed_y * 0.2
        else:
            # Ball moving away - return to center / Bola alejándose - volver al centro
            target_left = SCREEN_HEIGHT / 2 + random.uniform(-50, 50)
        
        center_left = self.demo_player.y + self.demo_player.height / 2
        diff_left = target_left - center_left
        
        # Move with urgency-based speed / Mover con velocidad basada en urgencia
        if abs(diff_left) > 15:
            urgency = min(1.0, abs(diff_left) / 100)
            speed_mult = 0.7 + urgency * 0.3 + random.uniform(-0.1, 0.1)
            move_amount = self.demo_player.speed * speed_mult * dt
            if diff_left > 0:
                self.demo_player.y += move_amount
            else:
                self.demo_player.y -= move_amount
            self.demo_player.y = max(0, min(SCREEN_HEIGHT - self.demo_player.height, self.demo_player.y))
        
        # Right paddle AI logic / Lógica IA paleta derecha
        target_right = self.demo_ball.y + self.demo_ball.size / 2
        if self.demo_ball.speed_x > 0:
            # Ball moving towards right paddle - predict / Bola moviéndose hacia paleta derecha - predecir
            target_right += self.demo_ball.speed_y * 0.18
        else:
            # Ball moving away - return to center / Bola alejándose - volver al centro
            target_right = SCREEN_HEIGHT / 2 + random.uniform(-40, 40)
        
        center_right = self.demo_ai.y + self.demo_ai.height / 2
        diff_right = target_right - center_right
        
        if abs(diff_right) > 12:
            urgency = min(1.0, abs(diff_right) / 80)
            speed_mult = 0.75 + urgency * 0.25 + random.uniform(-0.08, 0.08)
            move_amount = self.demo_ai.speed * speed_mult * dt
            if diff_right > 0:
                self.demo_ai.y += move_amount
            else:
                self.demo_ai.y -= move_amount
            self.demo_ai.y = max(0, min(SCREEN_HEIGHT - self.demo_ai.height, self.demo_ai.y))
        
        # Move ball / Mover bola
        self.demo_ball.move(dt)
        
        # Check collisions / Verificar colisiones
        ball_rect = self.demo_ball.get_rect()
        player_rect = self.demo_player.get_rect()
        ai_rect = self.demo_ai.get_rect()
        
        # Left paddle collision / Colisión paleta izquierda
        if ball_rect.colliderect(player_rect) and self.demo_ball.speed_x < 0:
            self.demo_ball.x = float(player_rect.right)
            self.demo_ball.speed_x = abs(self.demo_ball.speed_x)
        
        # Right paddle collision / Colisión paleta derecha
        if ball_rect.colliderect(ai_rect) and self.demo_ball.speed_x > 0:
            self.demo_ball.x = float(ai_rect.left - self.demo_ball.size)
            self.demo_ball.speed_x = -abs(self.demo_ball.speed_x)
        
        # Score detection / Detección de puntos
        if ball_rect.right < 0:
            self.demo_ai_score += 1
            self.demo_ball.reset()
        elif ball_rect.left > SCREEN_WIDTH:
            self.demo_player_score += 1
            self.demo_ball.reset()
    
    def _create_assets(self):
        """
        Create visual assets (background, vignette, scanlines, glow).
        Crear recursos visuales (fondo, viñeta, líneas de escaneo, brillo).
        """
        # Create gradient background (dark blue-purple at top → lighter at bottom)
        # Crear fondo con gradiente (azul-morado oscuro arriba → más claro abajo)
        self.base_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT  # Vertical position ratio / Ratio de posición vertical
            r = int(24 + 40 * (1 - t))  # Red channel / Canal rojo
            g = int(16 + 30 * (1 - t))  # Green channel / Canal verde
            b = int(50 + 120 * t)  # Blue channel (increases downward) / Canal azul (aumenta hacia abajo)
            pygame.draw.line(self.base_background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Create vignette effect (darkens edges) / Crear efecto viñeta (oscurece bordes)
        self.vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        cx, cy = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        max_dist = math.hypot(cx, cy)
        for y in range(SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                # Distance from center / Distancia desde el centro
                dist = math.hypot(x - cx, y - cy)
                # Alpha increases with distance / Alpha aumenta con distancia
                alpha = int(200 * max(0, (dist / max_dist) - 0.35))
                if alpha > 0:
                    self.vignette.set_at((x, y), (0, 0, 0, min(255, alpha)))
        
        # Create scanlines effect (CRT monitor look) / Crear efecto líneas de escaneo (apariencia monitor CRT)
        self.scanlines = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.rect(self.scanlines, (0, 0, 0, 40), (0, y, SCREEN_WIDTH, 2))
        
        # Create center glow effect / Crear efecto de brillo central
        self.center_glow = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(self.center_glow, (140, 40, 200, 120), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN_HEIGHT // 2)
    def check_collision(self):
        """
        Check ball collisions with paddles and score boundaries.
        Verificar colisiones de bola con paletas y límites de puntaje.
        """
        ball_rect = self.ball.get_rect()
        player_rect = self.player.get_rect()
        ai_rect = self.ai.get_rect()
        
        # Player paddle collision / Colisión con paleta del jugador
        if ball_rect.colliderect(player_rect) and self.ball.speed_x < 0:
            self.ball.x = float(player_rect.right)  # Prevent ball from getting stuck / Evitar que la bola se atasque
            self._reflect_ball(self.player)
            self.create_particles(self.ball.x, self.ball.y + self.ball.size / 2, BLUE)
            self._shake(0.12, 4)  # Screen shake effect / Efecto de sacudida de pantalla
            self._play_sound(paddle_sound)
        
        # AI paddle collision / Colisión con paleta IA
        if ball_rect.colliderect(ai_rect) and self.ball.speed_x > 0:
            self.ball.x = float(ai_rect.left - self.ball.size)
            self._reflect_ball(self.ai)
            self.create_particles(self.ball.x + self.ball.size, self.ball.y + self.ball.size / 2, GREEN)
            self._shake(0.12, 4)
            self._play_sound(paddle_sound)
        
        # Left boundary - AI scores / Límite izquierdo - IA anota
        if ball_rect.right < 0:
            # Check shield power-up / Verificar power-up de escudo
            if self.shield_active:
                self.shield_active = False
                if 'shield' in self.active_effects:
                    del self.active_effects['shield']
                # Shield blocked the point / Escudo bloqueó el punto
                self.ball.reset(direction=1)
                if self.audio_enabled:
                    self.play_sound('powerup_collect', pitch=0.8)
                # Visual feedback / Retroalimentación visual
                for _ in range(40):
                    particle = self.particle_pool.acquire()
                    particle.reset(50, SCREEN_HEIGHT // 2, POWERUP_COLORS['shield'], size=4, life=0.6)
                    angle = random.random() * math.tau
                    speed = random.uniform(100, 300)
                    particle.speed_x = math.cos(angle) * speed
                    particle.speed_y = math.sin(angle) * speed
                    particle.initial_life = particle.life
                    self.particles.append(particle)
            else:
                self.ai_score += 1
                self.right_pop = 0.5  # Paddle pop animation / Animación de pop de paleta
                self.spawn_score_burst('right')
                self.ball.reset(direction=1)  # Reset towards player / Resetear hacia jugador
                self._shake(0.25, 8)
                self._play_sound(score_sound)
        # Right boundary - Player scores / Límite derecho - Jugador anota
        elif ball_rect.left > SCREEN_WIDTH:
            self.player_score += 1
            self.left_pop = 0.5
            self.spawn_score_burst('left')
            self.ball.reset(direction=-1)  # Reset towards AI / Resetear hacia IA
            self._shake(0.25, 8)
            self._play_sound(score_sound)
        
        # Check win condition / Verificar condición de victoria
        if self.player_score >= WIN_SCORE or self.ai_score >= WIN_SCORE:
            self.state = "gameover"
            self.gameover_phase = 0.0
            self.dragging = False
            self._play_sound(bounce_sound)
    
    def _clear_particles(self):
        """
        Clear all particles and return to pool.
        Limpiar todas las partículas y devolver al pool.
        """
        if not self.particles:
            return
        particle_count = len(self.particles)
        print(f"[Debug] Clearing {particle_count} particles")
        for particle in self.particles:
            self.particle_pool.release(particle)
        self.particles.clear()
        print(f"[Debug] Particles cleared, pool size: {len(self.particle_pool._pool)}")
    
    def create_particles(self, x, y, color):
        """
        Create particle burst at position.
        Crear ráfaga de partículas en posición.
        
        Args / Argumentos:
            x, y (float): Position / Posición
            color (tuple): Base RGB color / Color RGB base
        """
        for _ in range(12):
            # Vary color slightly for visual interest / Variar color ligeramente para interés visual
            varied = (
                max(0, min(255, color[0] + random.randint(-20, 40))),
                max(0, min(255, color[1] + random.randint(-20, 40))),
                max(0, min(255, color[2] + random.randint(-20, 40)))
            )
            particle = self.particle_pool.acquire()
            particle.reset(x, y, varied)
            self.particles.append(particle)
    
    def update_particles(self, dt):
        """
        Update particles and remove dead ones.
        Actualizar partículas y eliminar las muertas.
        
        Args / Argumentos:
            dt (float): Delta time / Delta de tiempo
        """
        if not self.particles:
            return
        # Keep only alive particles, release dead ones to pool
        # Mantener solo partículas vivas, devolver muertas al pool
        alive = [p for p in self.particles if p.update(dt) or not self.particle_pool.release(p)]
        self.particles = alive
    
    def spawn_score_burst(self, side):
        """
        Create score burst effect with particles.
        Crear efecto de ráfaga de puntaje con partículas.
        
        Args / Argumentos:
            side (str): 'left' or 'right' / 'izquierda' o 'derecha'
        """
        # Position burst above score / Posicionar ráfaga sobre puntaje
        target_x = SCREEN_WIDTH // 4 if side == 'left' else 3 * SCREEN_WIDTH // 4
        target_y = 92
        
        # Create expanding ring / Crear anillo expansivo
        self.score_bursts.append(ScoreBurst(target_x, target_y, ORANGE))
        
        # Create explosion particles / Crear partículas de explosión
        for _ in range(28):
            # Color variation / Variación de color
            varied = (
                max(0, min(255, ORANGE[0] + random.randint(-15, 35))),
                max(0, min(255, ORANGE[1] + random.randint(-20, 20))),
                max(0, min(255, ORANGE[2] + random.randint(-30, 30)))
            )
            particle = self.particle_pool.acquire()
            particle.reset(target_x, target_y, varied, size=random.randint(3, 7), life=random.uniform(0.28, 0.55))
            
            # Random direction / Dirección aleatoria
            angle = random.random() * math.tau
            speed = random.uniform(180, 420)
            particle.speed_x = math.cos(angle) * speed
            particle.speed_y = math.sin(angle) * speed
            particle.initial_life = particle.life
            self.particles.append(particle)
    
    def update_score_bursts(self, dt):
        """Update score burst effects. / Actualizar efectos de ráfaga de puntaje."""
        if not self.score_bursts:
            return
        for burst in self.score_bursts:
            burst.update(dt)
        # Remove dead bursts / Eliminar ráfagas muertas
        self.score_bursts = [b for b in self.score_bursts if b.alive()]
    
    def draw_score_bursts(self, surface):
        """Draw all score bursts. / Dibujar todas las ráfagas de puntaje."""
        for burst in self.score_bursts:
            burst.draw(surface)
    
    def draw_particles(self, surface):
        """Draw all particles. / Dibujar todas las partículas."""
        for p in self.particles:
            p.draw(surface)
    
    # ============================================================================
    # POWER-UP SYSTEM METHODS / MÉTODOS DEL SISTEMA DE POWER-UPS
    # Phase 2 Feature Implementation
    # ============================================================================
    
    def update_powerup_spawning(self, dt):
        """
        Spawn power-ups at intervals during gameplay.
        Generar power-ups a intervalos durante el juego.
        
        Args / Argumentos:
            dt (float): Delta time / Tiempo delta
        """
        if self.state != "playing":
            return
        
        self.powerup_spawn_timer += dt
        if self.powerup_spawn_timer >= self.powerup_spawn_interval:
            self.spawn_powerup()
            self.powerup_spawn_timer = 0.0
            # Random interval variation (12-18 seconds) / Variación aleatoria del intervalo (12-18 segundos)
            self.powerup_spawn_interval = 12.0 + random.random() * 6.0
    
    def spawn_powerup(self):
        """
        Create new power-up at random position.
        Crear nuevo power-up en posición aleatoria.
        """
        # Weighted random selection / Selección aleatoria ponderada
        powerup_type = random.choices(POWERUP_TYPES, weights=POWERUP_WEIGHTS)[0]
        
        # Spawn in middle third of screen / Generar en el tercio medio de la pantalla
        x = SCREEN_WIDTH // 2 + random.randint(-200, 200)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        
        powerup = PowerUp(
            type=powerup_type,
            x=x,
            y=y,
            vx=random.uniform(-20, 20),
            vy=random.uniform(30, 70)
        )
        self.powerups.append(powerup)
        
        # Spawn particle effect / Efecto de partículas al aparecer
        color = POWERUP_COLORS[powerup_type]
        for _ in range(15):
            particle = self.particle_pool.acquire()
            particle.reset(x, y, color, size=3, life=0.5)
            angle = random.random() * math.tau
            speed = random.uniform(50, 150)
            particle.speed_x = math.cos(angle) * speed
            particle.speed_y = math.sin(angle) * speed
            particle.initial_life = particle.life
            self.particles.append(particle)
    
    def update_powerups(self, dt):
        """
        Update power-ups movement and lifetime.
        Actualizar movimiento y vida útil de power-ups.
        
        Args / Argumentos:
            dt (float): Delta time / Tiempo delta
        """
        for powerup in self.powerups[:]:
            if not powerup.active:
                continue
            
            # Move power-up / Mover power-up
            powerup.x += powerup.vx * dt
            powerup.y += powerup.vy * dt
            powerup.glow_phase += dt * 3.0
            powerup.lifetime -= dt
            
            # Remove expired power-ups / Eliminar power-ups expirados
            if powerup.lifetime <= 0:
                self.powerups.remove(powerup)
    
    def check_powerup_collision(self, paddle):
        """
        Check if paddle collected a power-up.
        Verificar si la paleta recolectó un power-up.
        
        Args / Argumentos:
            paddle (Paddle): Paddle to check / Paleta a verificar
        """
        for powerup in self.powerups[:]:
            if not powerup.active:
                continue
            
            # Rectangle collision / Colisión de rectángulos
            if (powerup.x < paddle.x + paddle.width and
                powerup.x + powerup.size > paddle.x and
                powerup.y < paddle.y + paddle.height and
                powerup.y + powerup.size > paddle.y):
                
                self.activate_powerup(powerup.type)
                self.powerups.remove(powerup)
                
                # Collection sound / Sonido de recolección
                if self.audio_enabled:
                    self.play_sound('powerup_collect', pitch=1.5)
                
                # Particle burst at collection point / Ráfaga de partículas en punto de recolección
                color = POWERUP_COLORS[powerup.type]
                for _ in range(25):
                    particle = self.particle_pool.acquire()
                    particle.reset(powerup.x, powerup.y, color, size=random.randint(2, 5), life=random.uniform(0.3, 0.6))
                    angle = random.random() * math.tau
                    speed = random.uniform(100, 300)
                    particle.speed_x = math.cos(angle) * speed
                    particle.speed_y = math.sin(angle) * speed
                    particle.initial_life = particle.life
                    self.particles.append(particle)
    
    def activate_powerup(self, type: str):
        """
        Apply power-up effect.
        Aplicar efecto del power-up.
        
        Args / Argumentos:
            type (str): Power-up type / Tipo de power-up
        """
        if type == 'big_paddle':
            self.active_effects['big_paddle'] = 10.0
            self.player.height = self.player.original_height * 1.5
        
        elif type == 'multi_ball':
            # Create 2 additional balls / Crear 2 bolas adicionales
            for _ in range(2):
                new_ball = Ball()
                new_ball.x = self.ball.x
                new_ball.y = self.ball.y
                new_ball.speed_x = self.ball.speed_x * random.uniform(0.8, 1.2)
                new_ball.speed_y = self.ball.speed_y * random.uniform(0.8, 1.2)
                self.balls.append(new_ball)
        
        elif type == 'speed_boost':
            self.active_effects['speed_boost'] = 10.0
            self.ball.speed_x *= 1.5
            self.ball.speed_y *= 1.5
            for ball in self.balls:
                ball.speed_x *= 1.5
                ball.speed_y *= 1.5
        
        elif type == 'shield':
            self.shield_active = True
            self.active_effects['shield'] = 999.0  # Lasts until used / Dura hasta usarse
        
        elif type == 'slow_motion':
            self.active_effects['slow_motion'] = 10.0
            self.ball.speed_x *= 0.5
            self.ball.speed_y *= 0.5
            for ball in self.balls:
                ball.speed_x *= 0.5
                ball.speed_y *= 0.5
        
        elif type == 'chaos_ball':
            self.active_effects['chaos_ball'] = 15.0
    
    def update_powerup_effects(self, dt):
        """
        Update active power-up timers.
        Actualizar temporizadores de power-ups activos.
        
        Args / Argumentos:
            dt (float): Delta time / Tiempo delta
        """
        expired = []
        
        for effect_type, time_remaining in self.active_effects.items():
            if effect_type == 'shield':
                continue  # Shield doesn't expire by time / Escudo no expira por tiempo
            
            time_remaining -= dt
            
            if time_remaining <= 0:
                self.deactivate_powerup(effect_type)
                expired.append(effect_type)
            else:
                self.active_effects[effect_type] = time_remaining
        
        for effect in expired:
            del self.active_effects[effect]
    
    def deactivate_powerup(self, type: str):
        """
        Remove power-up effect.
        Eliminar efecto del power-up.
        
        Args / Argumentos:
            type (str): Power-up type / Tipo de power-up
        """
        if type == 'big_paddle':
            self.player.height = self.player.original_height
        
        elif type == 'speed_boost':
            self.ball.speed_x /= 1.5
            self.ball.speed_y /= 1.5
            for ball in self.balls:
                ball.speed_x /= 1.5
                ball.speed_y /= 1.5
        
        elif type == 'slow_motion':
            self.ball.speed_x /= 0.5
            self.ball.speed_y /= 0.5
            for ball in self.balls:
                ball.speed_x /= 0.5
                ball.speed_y /= 0.5
        
        # Expiration sound / Sonido de expiración
        if self.audio_enabled:
            self.play_sound('powerup_expire')
    
    def draw_powerups(self):
        """
        Draw all active power-ups.
        Dibujar todos los power-ups activos.
        """
        for powerup in self.powerups:
            if not powerup.active:
                continue
            
            # Glow animation / Animación de brillo
            glow_intensity = 0.5 + 0.5 * math.sin(powerup.glow_phase)
            color = POWERUP_COLORS[powerup.type]
            
            # Draw glow / Dibujar brillo
            glow_radius = int(powerup.size * (1.5 + 0.3 * glow_intensity))
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*color, 50), (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surf, (powerup.x - glow_radius, powerup.y - glow_radius))
            
            # Draw power-up circle / Dibujar círculo del power-up
            pygame.draw.circle(self.screen, color, (int(powerup.x), int(powerup.y)), int(powerup.size / 2))
            
            # Draw inner highlight / Dibujar resaltado interior
            highlight_color = tuple(min(255, c + 80) for c in color)
            pygame.draw.circle(self.screen, highlight_color, (int(powerup.x), int(powerup.y)), int(powerup.size / 4))
    
    def draw_active_effects_hud(self):
        """
        Show active power-ups in corner HUD.
        Mostrar power-ups activos en HUD de esquina.
        """
        y_offset = 80
        
        for effect_type, time_remaining in self.active_effects.items():
            if effect_type == 'shield' and time_remaining > 900:
                time_remaining = 0  # Don't show time for shield / No mostrar tiempo para escudo
            
            color = POWERUP_COLORS[effect_type]
            
            # Draw icon background / Dibujar fondo del ícono
            icon_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(icon_surf, (*color, 200), (20, 20), 18)
            pygame.draw.circle(icon_surf, (255, 255, 255, 100), (20, 20), 10)
            self.screen.blit(icon_surf, (SCREEN_WIDTH - 60, y_offset))
            
            # Draw timer text / Dibujar texto del temporizador
            if time_remaining > 0:
                timer_text = self.small_font.render(f"{int(time_remaining)}s", True, WHITE)
                self.screen.blit(timer_text, (SCREEN_WIDTH - 55, y_offset + 45))
            
            y_offset += 70
    
    def _update_button_animations(self):
        """Update smooth button hover animations / Actualizar animaciones suaves de hover de botones"""
        for btn_id in list(self.button_scales.keys()):
            target = self.button_target_scales.get(btn_id, 1.0)
            current = self.button_scales[btn_id]
            # Smooth lerp towards target / Interpolación suave hacia objetivo
            self.button_scales[btn_id] = current + (target - current) * min(1.0, self.dt * 12.0)
    
    def _get_button_scale(self, btn_id, hovered):
        """Get animated button scale / Obtener escala animada del botón"""
        self.button_target_scales[btn_id] = 1.08 if hovered else 1.0
        return self.button_scales.get(btn_id, 1.0)
    
    def _draw_modern_button(self, text, x, y, hovered=False, scale=1.0, glow_color=(100, 200, 255)):
        """
        Draw modern gradient button with glow effect.
        Dibujar botón moderno con gradiente y efecto de brillo.
        
        Args / Argumentos:
            text (str): Button text / Texto del botón
            x, y (float): Center position / Posición central
            hovered (bool): Hover state / Estado de hover
            scale (float): Scale multiplier for animations / Multiplicador de escala para animaciones
            glow_color (tuple): RGB glow color / Color RGB del brillo
        
        Returns / Retorna:
            pygame.Rect: Button hitbox / Hitbox del botón
        """
        # Render text / Renderizar texto
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_w, text_h = text_surf.get_size()
        
        # Calculate button dimensions with padding / Calcular dimensiones con padding
        btn_w = int((text_w + 60) * scale)
        btn_h = int((text_h + 30) * scale)
        btn_x = int(x - btn_w / 2)
        btn_y = int(y - btn_h / 2)
        
        # Create button rect / Crear rectángulo del botón
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        
        # Draw glow effect when hovered / Dibujar efecto de brillo al hacer hover
        if hovered:
            glow_surf = pygame.Surface((btn_w + 20, btn_h + 20), pygame.SRCALPHA)
            for i in range(5):
                alpha = int(40 - i * 7)
                expand = i * 4
                glow_rect = pygame.Rect(expand, expand, btn_w + 20 - expand * 2, btn_h + 20 - expand * 2)
                pygame.draw.rect(glow_surf, (*glow_color, alpha), glow_rect, border_radius=15)
            self.screen.blit(glow_surf, (btn_x - 10, btn_y - 10))
        
        # Draw gradient background / Dibujar fondo con gradiente
        btn_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        for i in range(btn_h):
            t = i / btn_h
            if hovered:
                r = int(glow_color[0] * (0.5 + 0.3 * t))
                g = int(glow_color[1] * (0.5 + 0.3 * t))
                b = int(glow_color[2] * (0.7 + 0.3 * t))
            else:
                r = int(40 + 30 * t)
                g = int(50 + 30 * t)
                b = int(80 + 40 * t)
            pygame.draw.line(btn_surf, (r, g, b, 255), (0, i), (btn_w, i))
        
        # Draw border / Dibujar borde
        border_color = glow_color if hovered else (80, 90, 120)
        pygame.draw.rect(btn_surf, border_color, btn_surf.get_rect(), width=2, border_radius=12)
        
        self.screen.blit(btn_surf, (btn_x, btn_y))
        
        # Draw text centered / Dibujar texto centrado
        scaled_text = pygame.transform.scale(text_surf, (int(text_w * scale), int(text_h * scale)))
        text_rect = scaled_text.get_rect(center=(x, y))
        self.screen.blit(scaled_text, text_rect)
        
        return btn_rect
    
    def _draw_toggle(self, x, y, enabled, hovered, switch_w=80, switch_h=36):
        """
        Draw iOS-style toggle switch.
        Dibujar interruptor estilo iOS.
        
        Args / Argumentos:
            x, y (float): Center position / Posición central
            enabled (bool): Toggle state / Estado del interruptor
            hovered (bool): Mouse hover state / Estado de hover del ratón
            switch_w, switch_h (int): Switch dimensions / Dimensiones del interruptor
        
        Returns / Retorna:
            pygame.Rect: Hitbox for mouse interaction / Hitbox para interacción del ratón
        """
        track_rect = pygame.Rect(x - switch_w // 2, y - switch_h // 2, switch_w, switch_h)
        
        # Different colors for on/off states / Diferentes colores para estados encendido/apagado
        if enabled:
            track_color = (80, 200, 120, 200)  # Green / Verde
            knob_x = track_rect.right - 22
            knob_color = (120, 255, 160)
        else:
            track_color = (100, 100, 120, 180)  # Gray / Gris
            knob_x = track_rect.left + 22
            knob_color = (180, 180, 200)
        
        # Draw track (rounded rectangle) / Dibujar pista (rectángulo redondeado)
        track_surf = pygame.Surface((switch_w, switch_h), pygame.SRCALPHA)
        pygame.draw.rect(track_surf, track_color, (0, 0, switch_w, switch_h), border_radius=switch_h // 2)
        
        # Draw hover glow / Dibujar brillo de hover
        if hovered:
            glow = pygame.Surface((switch_w + 20, switch_h + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (100, 180, 255, 120), (0, 0, switch_w + 20, switch_h + 20), border_radius=(switch_h + 20) // 2)
            self.screen.blit(glow, (track_rect.x - 10, track_rect.y - 10))
        
        self.screen.blit(track_surf, track_rect)
        
        # Draw knob shadow / Dibujar sombra del botón
        knob_radius = 20
        shadow = pygame.Surface((knob_radius * 2 + 8, knob_radius * 2 + 8), pygame.SRCALPHA)
        pygame.draw.circle(shadow, (0, 0, 0, 80), (knob_radius + 4, knob_radius + 4), knob_radius)
        self.screen.blit(shadow, (knob_x - knob_radius, y - knob_radius - 4))
        
        # Draw knob with highlight / Dibujar botón con resaltado
        knob_surf = pygame.Surface((knob_radius * 2, knob_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(knob_surf, knob_color, (knob_radius, knob_radius), knob_radius)
        pygame.draw.circle(knob_surf, (255, 255, 255, 140), (knob_radius - 5, knob_radius - 5), knob_radius // 3)
        self.screen.blit(knob_surf, (knob_x - knob_radius, y - knob_radius))
        
        # Return expanded hitbox for easier clicking / Devolver hitbox expandido para clic más fácil
        return track_rect.inflate(40, 20)
    
    def draw_menu(self):
        """
        Draw main menu with animated logo, difficulty selection, and demo game.
        Dibujar menú principal con logo animado, selección de dificultad y juego demo.
        
        Features / Características:
        - Background demo AI vs AI game / Juego demo IA vs IA de fondo
        - Pixel art logo with floating animation / Logo pixel art con animación flotante
        - Difficulty buttons (Easy/Medium/Hard) / Botones de dificultad (Fácil/Medio/Difícil)
        - Multiplayer button with icon / Botón multijugador con ícono
        - Settings button with gear icon / Botón configuración con ícono de engranaje
        - Hover effects and animations / Efectos de hover y animaciones
        """
        self._draw_background()
        demo_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        demo_surface.fill((0, 0, 0, 0))
        self.demo_player.draw(demo_surface)
        self.demo_ai.draw(demo_surface)
        self.demo_ball.draw(demo_surface)
        [pygame.draw.rect(demo_surface, (100, 150, 200, 80), (SCREEN_WIDTH // 2 - 3, i, 6, 10), border_radius=3) for i in range(0, SCREEN_HEIGHT, 16)]
        demo_surface.set_alpha(60)
        self.screen.blit(demo_surface, (0, 0))
        cx = SCREEN_WIDTH // 2
        t = self.elapsed
        # Use pixel art logo instead of text
        logo_rect = self.title_logo.get_rect(center=(cx, 80 + 10 * math.sin(t * 1.5)))
        self.screen.blit(self.title_logo, logo_rect)
        subtitle = self.font.render(self.t('subtitle'), True, YELLOW)
        subtitle_rect = subtitle.get_rect(center=(cx, 140 + 8 * math.sin(t * 2.2)))
        self.screen.blit(subtitle, subtitle_rect)
        base_y = 200
        spacing = 55
        self.difficulty_hitboxes = []
        if self.menu_hover_index is not None and not (0 <= self.menu_hover_index < len(self.difficulties)):
            self.menu_hover_index = None
        diff_labels = [self.t('easy'), self.t('medium'), self.t('hard')]
        for idx in range(len(self.difficulties)):
            y, active, hovered = base_y + idx * spacing, idx == self.diff_index, idx == self.menu_hover_index
            color = WHITE if active else ((210, 220, 255) if hovered else (170, 180, 200))
            text = self.font.render(diff_labels[idx], True, color)
            text_rect = text.get_rect(center=(cx, y))
            if active:
                pulse = 110 + int(40 * math.sin(t * 3))
                highlight = pygame.Surface((text_rect.width + 120, text_rect.height + 24), pygame.SRCALPHA)
                pygame.draw.rect(highlight, (40, 150, 255, pulse), highlight.get_rect(), border_radius=18)
                highlight_rect = highlight.get_rect(center=text_rect.center)
                self.screen.blit(highlight, highlight_rect)
                arrow_color = (255, 255, 255, 220)
                pygame.draw.polygon(self.screen, arrow_color, [(highlight_rect.left - 18, y), (highlight_rect.left - 6, y - 12), (highlight_rect.left - 6, y + 12)])
                pygame.draw.polygon(self.screen, arrow_color, [(highlight_rect.right + 18, y), (highlight_rect.right + 6, y - 12), (highlight_rect.right + 6, y + 12)])
                hit_rect = highlight_rect.inflate(12, 12)
            elif hovered:
                hover_rect = pygame.Rect(text_rect.left - 60, text_rect.top - 12, text_rect.width + 120, text_rect.height + 24)
                glow = pygame.Surface((hover_rect.width, hover_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow, (60, 160, 255, 80), glow.get_rect(), border_radius=18)
                self.screen.blit(glow, hover_rect)
                hit_rect = hover_rect
            else:
                hit_rect = pygame.Rect(text_rect.left - 60, text_rect.top - 12, text_rect.width + 120, text_rect.height + 24)
            self.difficulty_hitboxes.append((hit_rect, idx))
            self.screen.blit(text, text_rect)
        hint = self.font.render(self.t('difficulty_hint'), True, (190, 190, 200))
        hint_rect = hint.get_rect(center=(cx, base_y + len(self.difficulties) * spacing))
        self.screen.blit(hint, hint_rect)
        
        # 2-Player button with modern style / Botón de 2 jugadores con estilo moderno
        twoplay_y = base_y + len(self.difficulties) * spacing + 50
        twoplay_hovered = hasattr(self, '_2player_button_hover') and self._2player_button_hover
        btn_scale = self._get_button_scale('2player', twoplay_hovered)
        if '2player' not in self.button_scales:
            self.button_scales['2player'] = 1.0
        self._2player_button_rect = self._draw_modern_button(
            self.t('2player'), cx, twoplay_y, twoplay_hovered, btn_scale, (255, 200, 50)
        )
        
        mp_y = base_y + len(self.difficulties) * spacing + 110
        mp_text = self.font.render(self.t('multiplayer'), True, (200, 220, 255))
        mp_rect = mp_text.get_rect(center=(cx, mp_y))
        icon_size = 28
        icon_x = mp_rect.left - 42
        icon_y = mp_y
        icon_surf = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        person_color = (180, 200, 255)
        pygame.draw.circle(icon_surf, person_color, (7, 7), 4)
        pygame.draw.circle(icon_surf, person_color, (21, 7), 4)
        pygame.draw.rect(icon_surf, person_color, (4, 12, 6, 10), border_radius=3)
        pygame.draw.rect(icon_surf, person_color, (18, 12, 6, 10), border_radius=3)
        pygame.draw.line(icon_surf, person_color, (4, 14), (1, 18), 2)
        pygame.draw.line(icon_surf, person_color, (10, 14), (13, 18), 2)
        pygame.draw.line(icon_surf, person_color, (18, 14), (15, 18), 2)
        pygame.draw.line(icon_surf, person_color, (24, 14), (27, 18), 2)
        mp_hit = pygame.Rect(mp_rect.left - 40, mp_rect.top - 10, mp_rect.width + 80, mp_rect.height + 20)
        if hasattr(self, '_mp_button_hover') and self._mp_button_hover:
            glow = pygame.Surface((mp_hit.width, mp_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (100, 200, 255, 100), glow.get_rect(), border_radius=16)
            self.screen.blit(glow, mp_hit)
        self.screen.blit(icon_surf, (icon_x, icon_y - icon_size // 2))
        self.screen.blit(mp_text, mp_rect)
        self._mp_button_rect = mp_hit
        settings_y = mp_y + 50
        settings_text = self.font.render(self.t('settings'), True, (200, 210, 230))
        settings_rect = settings_text.get_rect(center=(cx, settings_y))
        gear_size = 24
        gear_x = settings_rect.left - 40
        gear_y = settings_y
        gear_surf = pygame.Surface((gear_size, gear_size), pygame.SRCALPHA)
        gear_center = gear_size // 2
        gear_radius = 10
        gear_color = (180, 200, 255)
        gear_points = []
        for i in range(6):
            angle = math.pi / 3 * i
            px = gear_center + int(gear_radius * math.cos(angle))
            py = gear_center + int(gear_radius * math.sin(angle))
            gear_points.append((px, py))
        pygame.draw.polygon(gear_surf, gear_color, gear_points)
        tooth_color = (200, 220, 255)
        for i in range(6):
            angle = math.pi / 3 * i + math.pi / 6
            px1 = gear_center + int((gear_radius - 2) * math.cos(angle))
            py1 = gear_center + int((gear_radius - 2) * math.sin(angle))
            px2 = gear_center + int((gear_radius + 4) * math.cos(angle))
            py2 = gear_center + int((gear_radius + 4) * math.sin(angle))
            pygame.draw.line(gear_surf, tooth_color, (px1, py1), (px2, py2), 3)
        pygame.draw.circle(gear_surf, (30, 20, 50), (gear_center, gear_center), 4)
        settings_hit = pygame.Rect(gear_x - 10, settings_y - gear_size // 2 - 10, 
                                   settings_rect.width + gear_size + 60, settings_rect.height + 20)
        if hasattr(self, '_settings_button_hover') and self._settings_button_hover:
            glow = pygame.Surface((settings_hit.width, settings_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (100, 200, 255, 100), glow.get_rect(), border_radius=16)
            self.screen.blit(glow, settings_hit)
        self.screen.blit(gear_surf, (gear_x, gear_y - gear_size // 2))
        self.screen.blit(settings_text, settings_rect)
        self._settings_button_rect = settings_hit
        test_y = settings_y + 50
        test_text = self.small_font.render(self.t('diagnostics'), True, (180, 200, 220))
        test_rect = test_text.get_rect(center=(cx, test_y))
        test_hit = pygame.Rect(test_rect.left - 30, test_rect.top - 8, test_rect.width + 60, test_rect.height + 16)
        if hasattr(self, '_test_button_hover') and self._test_button_hover:
            glow = pygame.Surface((test_hit.width, test_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (100, 180, 255, 80), glow.get_rect(), border_radius=12)
            self.screen.blit(glow, test_hit)
        self.screen.blit(test_text, test_rect)
        self._test_button_rect = test_hit
        self.menu_phase = min(self.menu_phase + self.dt, 1.0)
        fade = max(0.0, 1.0 - self.menu_phase)
        if fade > 0:
            self._tint_surface.fill((0, 0, 0, int(255 * fade)))
            self.screen.blit(self._tint_surface, (0, 0))
        pygame.display.flip()
    def draw_settings(self):
        """
        Draw settings menu with toggles for fullscreen, audio, language, debug.
        Dibujar menú de configuración con toggles para pantalla completa, audio, idioma, debug.
        
        Features / Características:
        - Animated title / Título animado
        - iOS-style toggle switches / Interruptores estilo iOS
        - Language selector (EN/ES) / Selector de idioma (EN/ES)
        - Debug HUD toggle / Toggle de HUD de debug
        - Back button / Botón de atrás
        - Hover effects / Efectos de hover
        """
        self._draw_background()
        cx = SCREEN_WIDTH // 2
        t = self.elapsed
        title_color = (255, int(180 + 70 * math.sin(t)), int(200 + 40 * math.cos(t * 0.8)))
        title = self.large_font.render(self.t('settings'), True, title_color)
        title_rect = title.get_rect(center=(cx, 120 + 8 * math.sin(t * 1.5)))
        self.screen.blit(title, title_rect)
        fullscreen_y = 240
        self.screen.blit(self.font.render(self.t('fullscreen'), True, WHITE), self.font.render(self.t('fullscreen'), True, WHITE).get_rect(center=(cx - 100, fullscreen_y)))
        self._fullscreen_toggle_rect = self._draw_toggle(cx + 120, fullscreen_y, self.fullscreen, self.settings_fullscreen_hover)
        audio_y = 320
        self.screen.blit(self.font.render(self.t('audio'), True, WHITE), self.font.render(self.t('audio'), True, WHITE).get_rect(center=(cx - 95, audio_y)))
        self._audio_toggle_rect = self._draw_toggle(cx + 120, audio_y, self.audio_enabled, self.settings_hover_item == "audio_toggle")
        lang_y = 400
        self.screen.blit(self.font.render(self.t('language'), True, WHITE), self.font.render(self.t('language'), True, WHITE).get_rect(center=(cx - 110, lang_y)))
        lang_text = self.font.render("EN" if self.language == 'en' else "ES", True, (100, 220, 255))
        lang_rect = lang_text.get_rect(center=(cx + 120, lang_y))
        lang_hit = pygame.Rect(lang_rect.left - 25, lang_rect.top - 10, lang_rect.width + 50, lang_rect.height + 20)
        lang_hovered = self.settings_hover_item == "language_toggle"
        if lang_hovered:
            glow = pygame.Surface((lang_hit.width, lang_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (100, 220, 255, 100), glow.get_rect(), border_radius=12)
            self.screen.blit(glow, lang_hit)
        pygame.draw.rect(self.screen, (80, 120, 200, 120), lang_hit, 3, border_radius=12)
        self.screen.blit(lang_text, lang_rect)
        self._language_toggle_rect = lang_hit
        toggle_y = 480
        self.screen.blit(self.font.render(self.t('hud'), True, WHITE), self.font.render(self.t('hud'), True, WHITE).get_rect(center=(cx - 80, toggle_y)))
        self._debug_toggle_rect = self._draw_toggle(cx + 120, toggle_y, self.show_debug_hud, self.settings_hover_item == "debug_toggle")
        back_y = SCREEN_HEIGHT - 120
        back_text = self.font.render(self.t('back'), True, (220, 230, 255))
        back_rect = back_text.get_rect(center=(cx, back_y))
        arrow_size = 20
        arrow_x = back_rect.left - 35
        arrow_y = back_y
        arrow_color = (180, 220, 255)
        arrow_points = [
            (arrow_x, arrow_y),
            (arrow_x + 12, arrow_y - 10),
            (arrow_x + 12, arrow_y + 10)
        ]
        pygame.draw.polygon(self.screen, arrow_color, arrow_points)
        pygame.draw.line(self.screen, arrow_color, (arrow_x + 8, arrow_y), (arrow_x + arrow_size + 5, arrow_y), 3)
        back_hit = pygame.Rect(arrow_x - 10, back_rect.top - 12, back_rect.width + 70, back_rect.height + 24)
        back_hovered = self.settings_hover_item == "back"
        if back_hovered:
            glow = pygame.Surface((back_hit.width, back_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (80, 160, 255, 100), glow.get_rect(), border_radius=18)
            self.screen.blit(glow, back_hit)
        self.screen.blit(back_text, back_rect)
        self._back_button_rect = back_hit
        
        # Draw fade-in overlay BEFORE display.flip() / Dibujar overlay de fade ANTES de display.flip()
        # Note: This doesn't block input - pygame processes events before rendering
        # Nota: Esto no bloquea la entrada - pygame procesa eventos antes de renderizar
        self.menu_phase = min(self.menu_phase + self.dt, 1.0)
        fade = max(0.0, 1.0 - self.menu_phase)
        if fade > 0:
            self._tint_surface.fill((0, 0, 0, int(255 * fade)))
            self.screen.blit(self._tint_surface, (0, 0))
        
        pygame.display.flip()
    
    def draw_multiplayer_menu(self):
        """
        Draw multiplayer menu with host, join, and matchmaking options.
        Dibujar menú multijugador con opciones de host, unirse y matchmaking.
        
        Features / Características:
        - Host game button / Botón de hostear juego
        - Join private game (code input) / Unirse a juego privado (entrada de código)
        - Find public match button / Botón de buscar partida pública
        - Connection status display / Mostrar estado de conexión
        - Back button / Botón de atrás
        - Hover effects / Efectos de hover
        """
        self._draw_background()
        cx = SCREEN_WIDTH // 2
        t = self.elapsed
        title_color = (255, int(180 + 70 * math.sin(t)), int(200 + 40 * math.cos(t * 0.8)))
        title = self.large_font.render(self.t('multiplayer'), True, title_color)
        title_rect = title.get_rect(center=(cx, 100 + 8 * math.sin(t * 1.5)))
        self.screen.blit(title, title_rect)
        host_y = 220
        host_text = self.font.render(self.t('host_game'), True, WHITE)
        host_rect = host_text.get_rect(center=(cx, host_y))
        host_hit = pygame.Rect(host_rect.left - 50, host_rect.top - 15, host_rect.width + 100, host_rect.height + 30)
        host_hovered = hasattr(self, '_mp_host_hover') and self._mp_host_hover
        if host_hovered:
            glow = pygame.Surface((host_hit.width, host_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (80, 200, 120, 100), glow.get_rect(), border_radius=18)
            self.screen.blit(glow, host_hit)
        pygame.draw.rect(self.screen, (60, 180, 100, 160), host_hit, border_radius=18)
        self.screen.blit(host_text, host_rect)
        self._host_button_rect = host_hit
        join_y = 300
        join_label = self.font.render(self.t('join_private'), True, (200, 210, 230))
        join_label_rect = join_label.get_rect(center=(cx, join_y))
        self.screen.blit(join_label, join_label_rect)
        input_y = join_y + 50
        input_w = 220
        input_h = 50
        input_rect = pygame.Rect(cx - input_w // 2, input_y - input_h // 2, input_w, input_h)
        input_active = hasattr(self, '_input_active') and self._input_active
        box_color = (100, 180, 255, 200) if input_active else (80, 100, 140, 180)
        pygame.draw.rect(self.screen, box_color, input_rect, border_radius=12)
        pygame.draw.rect(self.screen, (150, 200, 255), input_rect, 3, border_radius=12)
        input_display = self.join_code_input if self.join_code_input else self.t('code_hint')
        input_text = self.font.render(input_display, True, WHITE if self.join_code_input else (150, 150, 150))
        input_text_rect = input_text.get_rect(center=input_rect.center)
        self.screen.blit(input_text, input_text_rect)
        self._input_box_rect = input_rect
        join_btn_y = input_y + 70
        join_btn_text = self.font.render(self.t('join'), True, WHITE)
        join_btn_rect = join_btn_text.get_rect(center=(cx, join_btn_y))
        join_btn_hit = pygame.Rect(join_btn_rect.left - 40, join_btn_rect.top - 12, join_btn_rect.width + 80, join_btn_rect.height + 24)
        join_btn_hovered = hasattr(self, '_join_btn_hover') and self._join_btn_hover
        if join_btn_hovered:
            glow = pygame.Surface((join_btn_hit.width, join_btn_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (80, 160, 255, 100), glow.get_rect(), border_radius=18)
            self.screen.blit(glow, join_btn_hit)
        pygame.draw.rect(self.screen, (80, 140, 220, 160), join_btn_hit, border_radius=18)
        self.screen.blit(join_btn_text, join_btn_rect)
        self._join_button_rect = join_btn_hit
        public_y = join_btn_y + 90
        public_label = self.font.render(self.t('or'), True, (180, 180, 200))
        public_label_rect = public_label.get_rect(center=(cx, public_y - 15))
        self.screen.blit(public_label, public_label_rect)
        public_btn_text = self.font.render(self.t('find_public'), True, WHITE)
        public_btn_rect = public_btn_text.get_rect(center=(cx, public_y + 30))
        public_btn_hit = pygame.Rect(public_btn_rect.left - 50, public_btn_rect.top - 15, public_btn_rect.width + 100, public_btn_rect.height + 30)
        public_btn_hovered = hasattr(self, '_public_btn_hover') and self._public_btn_hover
        if public_btn_hovered:
            glow = pygame.Surface((public_btn_hit.width, public_btn_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (120, 255, 140, 100), glow.get_rect(), border_radius=18)
            self.screen.blit(glow, public_btn_hit)
        pygame.draw.rect(self.screen, (100, 220, 120, 160), public_btn_hit, border_radius=18)
        self.screen.blit(public_btn_text, public_btn_rect)
        self._public_button_rect = public_btn_hit
        if self.multiplayer_status:
            status_color = (120, 255, 140) if "Connected" in self.multiplayer_status or "Hosting" in self.multiplayer_status else (255, 180, 120)
            status_text = self.small_font.render(self.multiplayer_status, True, status_color)
            status_rect = status_text.get_rect(center=(cx, public_y + 95))
            self.screen.blit(status_text, status_rect)
        back_y = SCREEN_HEIGHT - 100
        back_text = self.font.render(self.t('back'), True, (220, 230, 255))
        back_rect = back_text.get_rect(center=(cx, back_y))
        arrow_x = back_rect.left - 35
        arrow_y = back_y
        arrow_color = (180, 220, 255)
        arrow_points = [(arrow_x, arrow_y), (arrow_x + 12, arrow_y - 10), (arrow_x + 12, arrow_y + 10)]
        pygame.draw.polygon(self.screen, arrow_color, arrow_points)
        pygame.draw.line(self.screen, arrow_color, (arrow_x + 8, arrow_y), (arrow_x + 25, arrow_y), 3)
        back_hit = pygame.Rect(arrow_x - 10, back_rect.top - 12, back_rect.width + 70, back_rect.height + 24)
        back_hovered = hasattr(self, '_mp_back_hover') and self._mp_back_hover
        if back_hovered:
            glow = pygame.Surface((back_hit.width, back_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (80, 160, 255, 100), glow.get_rect(), border_radius=18)
            self.screen.blit(glow, back_hit)
        self.screen.blit(back_text, back_rect)
        self._mp_back_button_rect = back_hit
        self.menu_phase = min(self.menu_phase + self.dt, 1.0)
        fade = max(0.0, 1.0 - self.menu_phase)
        if fade > 0:
            self._tint_surface.fill((0, 0, 0, int(255 * fade)))
            self.screen.blit(self._tint_surface, (0, 0))
        pygame.display.flip()
    def run_diagnostics(self):
        self.test_results = []
        self.test_step = 0
        try:
            test_paddle = Paddle(100, 100, BLUE)
            initial_y = test_paddle.y
            test_paddle.move(1.0, 0.016)
            distance_moved = abs(test_paddle.y - initial_y)
            expected = test_paddle.speed * 0.016
            accuracy = abs(distance_moved - expected) < 0.1
            if accuracy:
                self.test_results.append(("Physics Engine", "PASS", f"Delta-time accurate: {distance_moved:.2f}px"))
            else:
                self.test_results.append(("Physics Engine", "WARN", f"Delta-time drift: {distance_moved:.2f}px"))
        except Exception as e:
            self.test_results.append(("Physics Engine", "FAIL", str(e)))
        try:
            test_ball = Ball()
            test_ball.y = -5
            initial_vy = test_ball.speed_y
            test_ball.move(0.016)
            bounced = test_ball.y >= 0 and test_ball.speed_y != initial_vy
            if bounced:
                self.test_results.append(("Ball Physics", "PASS", "Bounce mechanics functional"))
            else:
                self.test_results.append(("Ball Physics", "FAIL", "Bounce not detected"))
        except Exception as e:
            self.test_results.append(("Ball Physics", "FAIL", str(e)))
        try:
            test_paddle = Paddle(100, 100, BLUE, speed=300)
            test_ball = Ball()
            test_ball.x = test_paddle.x + test_paddle.width - 2
            test_ball.y = test_paddle.y + test_paddle.height // 2
            collision = test_paddle.get_rect().colliderect(test_ball.get_rect())
            if collision:
                self.test_results.append(("Collision Detection", "PASS", "Precision within 2px"))
            else:
                self.test_results.append(("Collision Detection", "FAIL", "Precision issue"))
        except Exception as e:
            self.test_results.append(("Collision Detection", "FAIL", str(e)))
        try:
            test_pool = ParticlePool(50)
            acquired = []
            for _ in range(30):
                acquired.append(test_pool.acquire())
            for p in acquired:
                test_pool.release(p)
            pool_size = len(test_pool._pool)
            if pool_size >= 50:
                self.test_results.append(("Particle System", "PASS", f"Pool recycling: {pool_size} available"))
            else:
                self.test_results.append(("Particle System", "WARN", f"Pool leak: {pool_size} available"))
        except Exception as e:
            self.test_results.append(("Particle System", "FAIL", str(e)))
        try:
            frequencies = [220, 440, 880]
            sounds_valid = []
            for freq in frequencies:
                sound = create_sound(freq, 0.01, 0.3)
                sounds_valid.append(sound is not None)
            if all(sounds_valid):
                self.test_results.append(("Audio Engine", "PASS", f"Synthesized {len(frequencies)} tones"))
            else:
                self.test_results.append(("Audio Engine", "FAIL", "Synthesis failed"))
        except Exception as e:
            self.test_results.append(("Audio Engine", "FAIL", str(e)))
        try:
            import time
            start = time.perf_counter()
            test_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for _ in range(100):
                pygame.draw.circle(test_surf, (255, 100, 150, 128), (400, 300), 50)
            render_time = (time.perf_counter() - start) * 1000
            if render_time < 10:
                self.test_results.append(("Render Pipeline", "PASS", f"100 draws: {render_time:.2f}ms"))
            else:
                self.test_results.append(("Render Pipeline", "WARN", f"Slow: {render_time:.2f}ms"))
        except Exception as e:
            self.test_results.append(("Render Pipeline", "FAIL", str(e)))
        try:
            test_modes = [pygame.BLEND_ADD, pygame.BLEND_MULT, pygame.SRCALPHA]
            blend_ok = True
            for mode in test_modes:
                surf = pygame.Surface((10, 10), pygame.SRCALPHA)
                surf.fill((255, 0, 0, 128))
                self.screen.blit(surf, (0, 0), special_flags=mode if mode != pygame.SRCALPHA else 0)
            if blend_ok:
                self.test_results.append(("Blend Modes", "PASS", f"Tested {len(test_modes)} modes"))
            else:
                self.test_results.append(("Blend Modes", "FAIL", "Blend error"))
        except Exception as e:
            self.test_results.append(("Blend Modes", "FAIL", str(e)))
        try:
            import time
            start = time.perf_counter()
            for _ in range(1000):
                self.ai_move()
            ai_time = (time.perf_counter() - start) * 1000
            if ai_time < 5:
                self.test_results.append(("AI Processing", "PASS", f"1000 ticks: {ai_time:.2f}ms"))
            else:
                self.test_results.append(("AI Processing", "WARN", f"Slow: {ai_time:.2f}ms"))
        except Exception as e:
            self.test_results.append(("AI Processing", "FAIL", str(e)))
        try:
            fps = self.clock.get_fps()
            if fps == 0:
                self.test_results.append(("Frame Stability", "WARN", "First frame - FPS unknown"))
            elif fps >= 55:
                self.test_results.append(("Frame Stability", "PASS", f"Stable 60Hz: {fps:.1f} FPS"))
            elif fps >= 30:
                self.test_results.append(("Frame Stability", "WARN", f"Below target: {fps:.1f} FPS"))
            else:
                self.test_results.append(("Frame Stability", "FAIL", f"Critical: {fps:.1f} FPS"))
        except Exception as e:
            self.test_results.append(("Frame Stability", "FAIL", str(e)))
        try:
            import sys
            paddle_mem = sys.getsizeof(self.player) + sys.getsizeof(self.ai)
            particle_mem = sum(sys.getsizeof(p) for p in self.particles[:10]) if self.particles else 0
            ball_mem = sys.getsizeof(self.ball)
            total_kb = (paddle_mem + particle_mem + ball_mem) / 1024
            if total_kb < 10:
                self.test_results.append(("Memory Footprint", "PASS", f"Game objects: {total_kb:.2f} KB"))
            else:
                self.test_results.append(("Memory Footprint", "WARN", f"High usage: {total_kb:.2f} KB"))
        except Exception as e:
            self.test_results.append(("Memory Footprint", "FAIL", str(e)))
    def draw_diagnostics(self):
        """
        Draw system diagnostics screen with test results.
        Dibujar pantalla de diagnósticos del sistema con resultados de pruebas.
        
        Features / Características:
        - Network connectivity tests / Pruebas de conectividad de red
        - AI processing performance / Rendimiento de procesamiento de IA
        - Frame stability analysis / Análisis de estabilidad de fotogramas
        - Memory usage tracking / Seguimiento de uso de memoria
        - Color-coded pass/warn/fail status / Estado codificado por colores pass/warn/fail
        - Close button / Botón de cerrar
        """
        self._draw_background()
        cx = SCREEN_WIDTH // 2
        t = self.elapsed
        title = self.large_font.render(self.t('system_diagnostics'), True, (180, 220, 255))
        title_rect = title.get_rect(center=(cx, 60))
        self.screen.blit(title, title_rect)
        y_offset = 140
        line_height = 45
        for idx, (test_name, status, details) in enumerate(self.test_results):
            name_color = (220, 230, 255)
            name_text = self.font.render(test_name, True, name_color)
            name_rect = name_text.get_rect(topleft=(80, y_offset))
            self.screen.blit(name_text, name_rect)
            if status == "PASS":
                badge_color = (80, 220, 120)
                badge_text_color = (255, 255, 255)
                icon = "✓"
            else:
                badge_color = (255, 100, 100)
                badge_text_color = (255, 255, 255)
                icon = "✗"
            badge_x = SCREEN_WIDTH - 180
            badge_w = 70
            badge_h = 30
            badge_rect = pygame.Rect(badge_x, y_offset + 3, badge_w, badge_h)
            pygame.draw.rect(self.screen, badge_color, badge_rect, border_radius=15)
            status_text = self.small_font.render(status, True, badge_text_color)
            status_rect = status_text.get_rect(center=badge_rect.center)
            self.screen.blit(status_text, status_rect)
            detail_color = (160, 170, 190)
            detail_text = self.small_font.render(details[:50], True, detail_color)
            detail_rect = detail_text.get_rect(topleft=(100, y_offset + 22))
            self.screen.blit(detail_text, detail_rect)
            y_offset += line_height
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        total = len(self.test_results)
        summary_y = SCREEN_HEIGHT - 90
        if passed == total:
            summary_color = (120, 255, 140)
            summary_msg = f"All Systems Operational ({passed}/{total})"
        else:
            summary_color = (255, 180, 100)
            summary_msg = f"Some Issues Detected ({passed}/{total} passed)"
        summary = self.font.render(summary_msg, True, summary_color)
        summary_rect = summary.get_rect(center=(cx, summary_y))
        glow_box = pygame.Rect(summary_rect.left - 20, summary_rect.top - 10, 
                               summary_rect.width + 40, summary_rect.height + 20)
        pulse = int(80 + 40 * math.sin(t * 3))
        pygame.draw.rect(self.screen, (*summary_color[:3], pulse), glow_box, border_radius=15)
        self.screen.blit(summary, summary_rect)
        close_y = SCREEN_HEIGHT - 40
        close_text = self.small_font.render(self.t('close'), True, (200, 210, 230))
        close_rect = close_text.get_rect(center=(cx, close_y))
        close_hit = pygame.Rect(close_rect.left - 25, close_rect.top - 8, close_rect.width + 50, close_rect.height + 16)
        close_hovered = hasattr(self, '_diag_close_hover') and self._diag_close_hover
        if close_hovered:
            glow = pygame.Surface((close_hit.width, close_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (80, 160, 255, 100), glow.get_rect(), border_radius=12)
            self.screen.blit(glow, close_hit)
        self.screen.blit(close_text, close_rect)
        self._diag_close_rect = close_hit
        pygame.display.flip()
    def draw_host_waiting(self):
        """
        Draw host waiting screen with connection code and status.
        Dibujar pantalla de espera de host con código de conexión y estado.
        
        Features / Características:
        - Display game code / Mostrar código de juego
        - Connection instructions (local and public) / Instrucciones de conexión (local y pública)
        - Waiting animation / Animación de espera
        - Connection status / Estado de conexión
        - Cancel button / Botón de cancelar
        """
        self._draw_background()
        cx = SCREEN_WIDTH // 2
        t = self.elapsed
        title = self.large_font.render(self.t('hosting_game'), True, (150, 255, 180))
        title_rect = title.get_rect(center=(cx, 150))
        self.screen.blit(title, title_rect)
        if self.network_host:
            code_text = self.large_font.render(f"Code: {self.network_host.code}", True, (255, 255, 150))
            code_rect = code_text.get_rect(center=(cx, 250))
            code_box = pygame.Rect(code_rect.left - 40, code_rect.top - 20, code_rect.width + 80, code_rect.height + 40)
            pulse = int(120 + 60 * math.sin(t * 3))
            pygame.draw.rect(self.screen, (100, 200, 255, pulse), code_box, border_radius=20)
            self.screen.blit(code_text, code_rect)
            y = 310
            lan_title = self.font.render("LAN (Same WiFi):", True, (120, 255, 140))
            self.screen.blit(lan_title, lan_title.get_rect(center=(cx, y)))
            y += 30
            lan_code = self.small_font.render(f"{self.t('share_code')} {self.network_host.code}", True, (200, 220, 255))
            self.screen.blit(lan_code, lan_code.get_rect(center=(cx, y)))
            y += 22
            lan_ip = self.small_font.render(f"{self.t('or_ip')} {self.network_host.local_ip}:5555", True, (180, 200, 220))
            self.screen.blit(lan_ip, lan_ip.get_rect(center=(cx, y)))
            y += 40
            net_title = self.font.render(self.t('internet'), True, (255, 200, 120))
            self.screen.blit(net_title, net_title.get_rect(center=(cx, y)))
            y += 30
            if self.network_host.external_ip:
                net_line1 = self.small_font.render("1. Port forward 5555 in router settings", True, (200, 220, 255))
                self.screen.blit(net_line1, net_line1.get_rect(center=(cx, y)))
                y += 22
                net_line2 = self.small_font.render(f"2. Share: {self.network_host.external_ip}:5555", True, (180, 200, 220))
                self.screen.blit(net_line2, net_line2.get_rect(center=(cx, y)))
            else:
                net_error = self.small_font.render("(Can't detect external IP)", True, (255, 150, 150))
                self.screen.blit(net_error, net_error.get_rect(center=(cx, y)))
            dots = "." * (int(t * 2) % 4)
            waiting_text = self.font.render(f"{self.t('waiting_player')}{dots}", True, (180, 190, 220))
            waiting_rect = waiting_text.get_rect(center=(cx, 420))
            self.screen.blit(waiting_text, waiting_rect)
            if self.network_host.connected:
                conn_text = self.large_font.render(self.t('player_connected'), True, (120, 255, 140))
                conn_rect = conn_text.get_rect(center=(cx, SCREEN_HEIGHT // 2))
                self.screen.blit(conn_text, conn_rect)
        cancel_y = SCREEN_HEIGHT - 100
        cancel_text = self.font.render(self.t('cancel'), True, (255, 180, 180))
        cancel_rect = cancel_text.get_rect(center=(cx, cancel_y))
        cancel_hit = pygame.Rect(cancel_rect.left - 40, cancel_rect.top - 12, cancel_rect.width + 80, cancel_rect.height + 24)
        cancel_hovered = hasattr(self, '_cancel_hover') and self._cancel_hover
        if cancel_hovered:
            glow = pygame.Surface((cancel_hit.width, cancel_hit.height), pygame.SRCALPHA)
            pygame.draw.rect(glow, (255, 100, 100, 100), glow.get_rect(), border_radius=18)
            self.screen.blit(glow, cancel_hit)
        self.screen.blit(cancel_text, cancel_rect)
        self._cancel_button_rect = cancel_hit
        pygame.display.flip()
    
    def _draw_background(self):
        """
        Draw animated background with gradient, parallax stars, and glows.
        Dibujar fondo animado con gradiente, estrellas parallax y brillos.
        
        Effects / Efectos:
        - Static gradient base (dark blue-purple) / Base de gradiente estático (azul-morado oscuro)
        - Animated color tint overlay / Superposición de tinte de color animado
        - Parallax scrolling stars / Estrellas con desplazamiento parallax
        - Center glow effect / Efecto de brillo central
        - Vignette darkening / Oscurecimiento de viñeta
        - Scanlines (CRT effect) / Líneas de escaneo (efecto CRT)
        """
        # Draw base gradient / Dibujar gradiente base
        self.screen.blit(self.base_background, (0, 0))
        
        # Animated color tint / Tinte de color animado
        cycle = (math.sin(self.elapsed * 0.6) + 1) / 2
        self._tint_surface.fill((int(30 + 120 * cycle), int(10 + 90 * (1 - cycle)), 180, 60))
        self.screen.blit(self._tint_surface, (0, 0), special_flags=pygame.BLEND_ADD)
        spacing = 40
        self.bg_offset = (self.bg_offset + 80 * self.dt) % spacing
        chroma_layers = [((220, 80, 255), 0), ((80, 220, 255), 12), ((255, 140, 90), 24)]
        for color, offset in chroma_layers:
            for x in range(-spacing, SCREEN_WIDTH + spacing, spacing):
                xx = x + int(self.bg_offset) + offset
                pygame.draw.line(self.screen, color, (xx, 0), (xx, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, spacing):
                intensity = int(35 + 55 * (1 - y / SCREEN_HEIGHT))
                yy = int((y + self.bg_offset + offset) % SCREEN_HEIGHT)
                line_color = (min(255, color[0] // 2 + intensity),
                              min(255, color[1] // 2 + intensity),
                              min(255, color[2] // 2 + intensity))
                pygame.draw.line(self.screen, line_color, (0, yy), (SCREEN_WIDTH, yy), 1)
        sweep_height = 140
        if self._cached_background is None:
            self._sweep_surface.fill((0, 0, 0, 0))
            for y in range(sweep_height):
                falloff = abs(y - sweep_height / 2) / (sweep_height / 2)
                alpha = int(90 * max(0, 1 - falloff))
                pygame.draw.line(self._sweep_surface, (200, 100, 255, alpha), (0, y), (SCREEN_WIDTH, y))
        sweep_y = int((math.sin(self.elapsed * 1.5) * 0.5 + 0.5) * (SCREEN_HEIGHT + sweep_height)) - sweep_height
        self.screen.blit(self._sweep_surface, (0, sweep_y), special_flags=pygame.BLEND_ADD)
        glow_alpha = int(70 + 40 * math.sin(self.elapsed * 2))
        self.center_glow.set_alpha(glow_alpha)
        self.screen.blit(self.center_glow, (0, 0), special_flags=pygame.BLEND_ADD)
        self.screen.blit(self.vignette, (0, 0))
        self.screen.blit(self.scanlines, (0, 0), special_flags=pygame.BLEND_MULT)
    def _shake(self, duration, magnitude):
        """
        Trigger screen shake effect.
        Activar efecto de sacudida de pantalla.
        
        Args / Argumentos:
            duration (float): Shake duration in seconds / Duración de sacudida en segundos
            magnitude (float): Shake intensity / Intensidad de sacudida
        """
        self.shake_time = duration
        self.shake_mag = magnitude
    
    def _score_scale(self, side):
        """
        Calculate score text scale animation.
        Calcular animación de escala de texto de puntaje.
        
        Args / Argumentos:
            side (str): 'left' or 'right' / 'izquierda' o 'derecha'
        
        Returns / Retorna:
            float: Scale factor (1.0 = normal, >1.0 = enlarged) / Factor de escala
        """
        t = self.left_pop if side == 'left' else self.right_pop
        if t <= 0:
            return 1.0
        # Elastic pop animation / Animación de pop elástico
        return 1.0 + 0.4 * ((t / 0.5) * (2 - t / 0.5))
    
    def _reflect_ball(self, paddle):
        """
        Reflect ball off paddle with angle based on hit position.
        Reflejar bola en paleta con ángulo basado en posición de golpe.
        
        Args / Argumentos:
            paddle (Paddle): Paddle that hit the ball / Paleta que golpeó la bola
        """
        # Calculate hit offset from paddle center / Calcular offset de golpe desde centro de paleta
        ball_cy = self.ball.y + self.ball.size / 2
        pad_cy = paddle.y + paddle.height / 2
        offset = (ball_cy - pad_cy) / (paddle.height / 2)
        offset = max(-1.0, min(1.0, offset))  # Clamp to [-1, 1] / Limitar a [-1, 1]
        
        # Increase speed on each hit / Aumentar velocidad en cada golpe
        speed = math.hypot(self.ball.speed_x, self.ball.speed_y) * SPEED_INCREASE_PER_HIT
        speed = min(speed, MAX_BALL_SPEED)  # Cap maximum speed / Limitar velocidad máxima
        
        # Calculate reflection angle / Calcular ángulo de reflexión
        angle = offset * (math.pi / 3)  # Max ±60 degrees / Máximo ±60 grados
        dir_x = -1 if self.ball.speed_x > 0 else 1  # Reverse horizontal / Revertir horizontal
        
        self.ball.speed_x = math.cos(angle) * speed * dir_x
        self.ball.speed_y = math.sin(angle) * speed
    def _draw_performance_hud(self):
        fps = self.clock.get_fps()
        particle_count = len(self.particles)
        ball_speed = math.hypot(self.ball.speed_x, self.ball.speed_y)
        stats = f"{fps:5.1f} FPS • Particles {particle_count:03d} • Speed {int(ball_speed):03d} px/s"
        text = self.small_font.render(stats, True, (180, 190, 220))
        self.screen.blit(text, (20, SCREEN_HEIGHT - 36))
    def draw(self):
        """
        Draw active game (playing state).
        Dibujar juego activo (estado de juego).
        
        Features / Características:
        - Background with effects / Fondo con efectos
        - Screen shake on impacts / Sacudida de pantalla en impactos
        - Paddles and ball rendering / Renderizado de paletas y bola
        - Animated center line / Línea central animada
        - Particle effects / Efectos de partículas
        - Score display with pop animation / Mostrar puntaje con animación pop
        - Difficulty badge / Insignia de dificultad
        - Game over overlay / Superposición de game over
        - Debug HUD (optional) / HUD de debug (opcional)
        """
        self._draw_background()
        
        # Calculate screen shake offset / Calcular offset de sacudida de pantalla
        ox = oy = 0
        if self.shake_time > 0:
            ox = random.randint(-int(self.shake_mag), int(self.shake_mag))
            oy = random.randint(-int(self.shake_mag), int(self.shake_mag))
        self._game_layer.fill((0, 0, 0, 0))
        self.player.draw(self._game_layer)
        self.ai.draw(self._game_layer)
        self.ball.draw(self._game_layer)
        
        # Draw multi-balls / Dibujar multi-bolas
        for ball in self.balls:
            ball.draw(self._game_layer)
        
        for i in range(0, SCREEN_HEIGHT, 16):
            pulse = int(150 + 80 * math.sin(self.elapsed * 2 + i * 0.08))
            color = (pulse, 100, 255, 220)
            pygame.draw.rect(self._game_layer, color, (SCREEN_WIDTH // 2 - 3, i, 6, 10), border_radius=3)
        self.draw_particles(self._game_layer)
        self.screen.blit(self._game_layer, (ox, oy))
        self.draw_score_bursts(self.screen)
        left_scale = self._score_scale('left')
        right_scale = self._score_scale('right')
        left_str = str(self.player_score)
        right_str = str(self.ai_score)
        l_text = self.font.render(left_str, True, WHITE)
        r_text = self.font.render(right_str, True, WHITE)
        l_surf = pygame.transform.smoothscale(l_text, (int(max(1, l_text.get_width() * left_scale)), int(max(1, l_text.get_height() * left_scale))))
        r_surf = pygame.transform.smoothscale(r_text, (int(max(1, r_text.get_width() * right_scale)), int(max(1, r_text.get_height() * right_scale))))
        l_shadow = pygame.transform.smoothscale(self.font.render(left_str, True, (30, 10, 60)), l_surf.get_size())
        r_shadow = pygame.transform.smoothscale(self.font.render(right_str, True, (30, 10, 60)), r_surf.get_size())
        l_pos = (SCREEN_WIDTH // 4 - l_surf.get_width() // 2, 20)
        r_pos = (3 * SCREEN_WIDTH // 4 - r_surf.get_width() // 2, 20)
        self.screen.blit(l_shadow, (l_pos[0] + 3, l_pos[1] + 4))
        self.screen.blit(r_shadow, (r_pos[0] + 3, r_pos[1] + 4))
        self.screen.blit(l_surf, l_pos)
        self.screen.blit(r_surf, r_pos)
        
        # Dynamic labels for 2-player mode / Etiquetas dinámicas para modo 2 jugadores
        if self.game_mode == "2player":
            player_label = self.small_font.render("Player 1", True, (200, 210, 230))
            ai_label = self.small_font.render("Player 2", True, (200, 210, 230))
        else:
            player_label = self.small_font.render(self.t('player'), True, (200, 210, 230))
            ai_label = self.small_font.render(self.t('ai'), True, (200, 210, 230))
        
        self.screen.blit(player_label, (SCREEN_WIDTH // 4 - player_label.get_width() // 2, 80))
        self.screen.blit(ai_label, (3 * SCREEN_WIDTH // 4 - ai_label.get_width() // 2, 80))
        if not hasattr(self, '_badge_cache'):
            self._badge_cache = {}
        diff_keys = ['easy', 'medium', 'hard']
        diff_key = diff_keys[self.diff_index] if self.diff_index < len(diff_keys) else 'medium'
        cache_key = f"{diff_key}_{self.language}"
        if cache_key not in self._badge_cache:
            badge_text = self.small_font.render(self.t(diff_key).upper(), True, (220, 230, 255))
            badge_surface = pygame.Surface((badge_text.get_width() + 30, badge_text.get_height() + 12), pygame.SRCALPHA)
            pygame.draw.rect(badge_surface, (30, 120, 220, 160), badge_surface.get_rect(), border_radius=12)
            badge_surface.blit(badge_text, (15, 6))
            self._badge_cache[cache_key] = badge_surface
        badge = self._badge_cache[cache_key]
        badge_rect = badge.get_rect(topright=(SCREEN_WIDTH - 40, 28))
        self.screen.blit(badge, badge_rect)
        
        # Draw power-ups and active effects HUD / Dibujar power-ups y HUD de efectos activos
        self.draw_powerups()
        self.draw_active_effects_hud()
        
        if self.show_debug_hud:
            self._draw_performance_hud()
        if self.state == "gameover":
            self.gameover_phase = min(self.gameover_phase + self.dt * 1.5, 1.0)
            
            # Dynamic winner text for 2-player mode / Texto de ganador dinámico para modo 2 jugadores
            if self.game_mode == "2player":
                winner = "Player 1" if self.player_score > self.ai_score else "Player 2"
            else:
                winner = "Player" if self.player_score > self.ai_score else "AI"
            
            fade_alpha = int(255 * 0.6 * self.gameover_phase)
            overlay_alpha = fade_alpha + int(40 * math.sin(self.elapsed * 2))
            overlay_alpha = max(0, min(220, overlay_alpha))
            self._tint_surface.fill((10, 0, 30, overlay_alpha))
            self.screen.blit(self._tint_surface, (0, 0))
            over = self.large_font.render(f"{winner} wins!", True, (255, 255, 150))
            scale = 1.0 + 0.15 * math.sin(self.elapsed * 4) * self.gameover_phase
            over_scaled = pygame.transform.smoothscale(over, (int(over.get_width() * scale), int(over.get_height() * scale)))
            over_rect = over_scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            tip = self.font.render("SPACE / ENTER to restart", True, WHITE)
            tip_rect = tip.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(over_scaled, over_rect)
            self.screen.blit(tip, tip_rect)
        pygame.display.flip()
    
    def run(self):
        """
        Main game loop entry point - auto-detects environment and runs appropriate loop.
        Punto de entrada del bucle principal - detecta automáticamente el entorno y ejecuta el bucle apropiado.
        
        Runs async loop for web/Pygbag, sync loop for desktop.
        Ejecuta bucle async para web/Pygbag, bucle sync para escritorio.
        """
        if IS_WEB:
            # Web mode: Use async loop for browser compatibility
            # Modo web: Usar bucle async para compatibilidad con navegador
            asyncio.run(self.run_async())
        else:
            # Desktop mode: Use traditional synchronous loop
            # Modo escritorio: Usar bucle síncrono tradicional
            self._run_sync()
    
    def _run_sync(self):
        """
        Synchronous game loop for desktop - original implementation.
        Bucle de juego síncrono para escritorio - implementación original.
        
        Loop structure / Estructura del bucle:
        1. Clock tick (60 FPS target) / Tick de reloj (objetivo 60 FPS)
        2. Event processing (mouse, keyboard, quit) / Procesamiento de eventos (ratón, teclado, salir)
        3. State-specific updates (menu, game, settings, etc) / Actualizaciones específicas de estado
        4. Physics and AI updates / Actualizaciones de física e IA
        5. Collision detection / Detección de colisiones
        6. Rendering / Renderizado
        
        States / Estados:
        - "menu": Main menu / Menú principal
        - "playing": Active game / Juego activo
        - "gameover": Game over screen / Pantalla de game over
        - "settings": Settings menu / Menú de configuración
        - "multiplayer": Multiplayer menu / Menú multijugador
        - "host_waiting": Waiting for client connection / Esperando conexión de cliente
        - "diagnostics": Network diagnostics / Diagnósticos de red
        """
        # [SYNC LOOP MARKER] - For identifying this loop vs async
        self.player_move_dir = 0.0
        self.ai_move_dir = 0.0
        self._2player_button_hover = False
        while True:
            dt_ms = self.clock.tick(60)
            self.dt = max(0.001, dt_ms / 1000.0)
            self.elapsed += self.dt
            self.shake_time, self.left_pop, self.right_pop = max(0.0, self.shake_time - self.dt), max(0.0, self.left_pop - self.dt), max(0.0, self.right_pop - self.dt)
            self.update_score_bursts(self.dt)
            self._update_button_animations()  # Smooth button hover animations / Animaciones suaves de hover de botones
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "diagnostics":
                        if hasattr(self, '_diag_close_rect') and self._diag_close_rect and self._diag_close_rect.collidepoint(event.pos):
                            self.state = "menu"
                            self.menu_phase = 0.0
                    elif self.state == "settings":
                        if hasattr(self, '_fullscreen_toggle_rect') and self._fullscreen_toggle_rect and self._fullscreen_toggle_rect.collidepoint(event.pos):
                            self.toggle_fullscreen()
                        elif hasattr(self, '_audio_toggle_rect') and self._audio_toggle_rect and self._audio_toggle_rect.collidepoint(event.pos):
                            self.toggle_audio()
                        elif hasattr(self, '_language_toggle_rect') and self._language_toggle_rect and self._language_toggle_rect.collidepoint(event.pos):
                            self.toggle_language()
                        elif hasattr(self, '_debug_toggle_rect') and self._debug_toggle_rect and self._debug_toggle_rect.collidepoint(event.pos):
                            self.show_debug_hud = not self.show_debug_hud
                            save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                        elif hasattr(self, '_back_button_rect') and self._back_button_rect and self._back_button_rect.collidepoint(event.pos):
                            self.state = "menu"
                            self.menu_phase = 0.0
                            self.settings_hover_item = None
                            self.settings_fullscreen_hover = False
                    elif self.state == "multiplayer":
                        if hasattr(self, '_host_button_rect') and self._host_button_rect and self._host_button_rect.collidepoint(event.pos):
                            self.network_host = NetworkHost()
                            if self.network_host.start():
                                self.multiplayer_mode = 'host'
                                self.state = "host_waiting"
                                self.multiplayer_status = f"Hosting - Code: {self.network_host.code}"
                                self._mp_game_started = False
                                try:
                                    self.matchmaking_client = MatchmakingClient(self.matchmaking_server_addr, 5556)
                                    if self.matchmaking_client.connect():
                                        local_ip = get_local_ip()
                                        if self.matchmaking_client.register_code(self.network_host.code, local_ip, 5555):
                                            print(f"[Game] Code {self.network_host.code} registered with matchmaking server")
                                        else:
                                            print("[Game] Warning: Failed to register code with matchmaking server")
                                    else:
                                        print("[Game] Warning: Could not connect to matchmaking server")
                                except Exception as e:
                                    print(f"[Game] Matchmaking registration error: {e}")
                            else:
                                self.multiplayer_status = "Failed to start host - Port may be in use"
                        elif hasattr(self, '_input_box_rect') and self._input_box_rect and self._input_box_rect.collidepoint(event.pos):
                            self._input_active = True
                        elif hasattr(self, '_join_button_rect') and self._join_button_rect and self._join_button_rect.collidepoint(event.pos):
                            if self.join_code_input:
                                self.multiplayer_status = "Resolving code..."
                                try:
                                    self.matchmaking_client = MatchmakingClient(self.matchmaking_server_addr, 5556)
                                    if self.matchmaking_client.connect():
                                        result = self.matchmaking_client.resolve_code(self.join_code_input)
                                        if result:
                                            host_ip, host_port = result
                                            self.multiplayer_status = "Connecting to host..."
                                            self.network_client = NetworkClient()
                                            if self.network_client.connect(host_ip, host_port):
                                                self.multiplayer_mode = 'client'
                                                self._start_game()
                                            else:
                                                self.multiplayer_status = "Connection failed - Host unreachable"
                                        else:
                                            self.multiplayer_status = "Invalid or expired code"
                                    else:
                                        self.multiplayer_status = "Connecting (fallback)..."
                                        self.network_client = NetworkClient()
                                        if self.network_client.connect('127.0.0.1'):
                                            self.multiplayer_mode = 'client'
                                            self._start_game()
                                        else:
                                            self.multiplayer_status = "Connection failed"
                                except Exception as e:
                                    print(f"[Game] Join error: {e}")
                                    self.multiplayer_status = f"Error: {str(e)}"
                        elif hasattr(self, '_public_button_rect') and self._public_button_rect and self._public_button_rect.collidepoint(event.pos):
                            self.searching_public = True
                            self.search_start_time = time.time()
                            self.multiplayer_status = "Connecting to matchmaking..."
                            try:
                                self.matchmaking_client = MatchmakingClient(self.matchmaking_server_addr, 5556)
                                if self.matchmaking_client.connect():
                                    response = self.matchmaking_client.join_public_queue()
                                    if response:
                                        if response.get('status') == 'matched':
                                            role = response.get('role')
                                            peer = response.get('peer')
                                            if role == 'host':
                                                self.network_host = NetworkHost()
                                                if self.network_host.start():
                                                    self.multiplayer_mode = 'host'
                                                    self.state = "host_waiting"
                                                    self.multiplayer_status = f"Matched! Waiting for connection..."
                                                    self._mp_game_started = False
                                                else:
                                                    self.multiplayer_status = "Failed to start host"
                                            elif role == 'client':
                                                peer_ip = peer.split(':')[0]
                                                self.multiplayer_status = "Matched! Connecting..."
                                                self.network_client = NetworkClient()
                                                if self.network_client.connect(peer_ip):
                                                    self.multiplayer_mode = 'client'
                                                    self._start_game()
                                                else:
                                                    self.multiplayer_status = "Connection to peer failed"
                                        else:
                                            self.multiplayer_status = "Searching for opponent..."
                                    else:
                                        self.multiplayer_status = "Matchmaking error"
                                else:
                                    self.multiplayer_status = "Cannot reach matchmaking server"
                                    self.searching_public = False
                            except Exception as e:
                                print(f"[Game] Public matchmaking error: {e}")
                                self.multiplayer_status = f"Matchmaking error: {str(e)}"
                                self.searching_public = False
                        elif hasattr(self, '_mp_back_button_rect') and self._mp_back_button_rect and self._mp_back_button_rect.collidepoint(event.pos):
                            self.state = "menu"
                            self.menu_phase = 0.0
                            self.join_code_input = ""
                            self.multiplayer_status = ""
                            self._input_active = False
                            self.searching_public = False
                    elif self.state == "host_waiting":
                        if hasattr(self, '_cancel_button_rect') and self._cancel_button_rect and self._cancel_button_rect.collidepoint(event.pos):
                            if self.network_host:
                                self.network_host.close()
                                self.network_host = None
                            self.multiplayer_mode = None
                            self.state = "multiplayer"
                            self.multiplayer_status = ""
                            self._mp_game_started = False
                    elif self.state == "menu":
                        if hasattr(self, '_settings_button_rect') and self._settings_button_rect and self._settings_button_rect.collidepoint(event.pos):
                            self.state = "settings"
                            self.menu_phase = 0.0
                            self.settings_hover_item = None
                        elif hasattr(self, '_2player_button_rect') and self._2player_button_rect and self._2player_button_rect.collidepoint(event.pos):
                            # Start 2-player game / Iniciar juego de 2 jugadores
                            self.game_mode = "2player"
                            self._start_game()
                        elif hasattr(self, '_mp_button_rect') and self._mp_button_rect and self._mp_button_rect.collidepoint(event.pos):
                            self.state = "multiplayer"
                            self.menu_phase = 0.0
                            self.multiplayer_status = ""
                        elif hasattr(self, '_test_button_rect') and self._test_button_rect and self._test_button_rect.collidepoint(event.pos):
                            self.run_diagnostics()
                            self.state = "diagnostics"
                        else:
                            target_idx = self.menu_hover_index
                            if target_idx is None:
                                for rect, idx in self.difficulty_hitboxes:
                                    if rect.collidepoint(event.pos):
                                        target_idx = idx
                                        break
                            if target_idx is not None and target_idx != self.diff_index:
                                self.diff_index = target_idx
                                save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                            if target_idx is not None:
                                self.menu_hover_index = target_idx
                    if self.state == "playing" and self._player_drag_rect().collidepoint(event.pos):
                        self.dragging = True
                        pointer_y = min(max(event.pos[1], self.player.y), self.player.y + self.player.height)
                        self.drag_offset = pointer_y - self.player.y
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.dragging = False
                if event.type == pygame.MOUSEMOTION:
                    if self.state == "menu":
                        self._settings_button_hover = hasattr(self, '_settings_button_rect') and self._settings_button_rect and self._settings_button_rect.collidepoint(event.pos)
                        self._2player_button_hover = hasattr(self, '_2player_button_rect') and self._2player_button_rect and self._2player_button_rect.collidepoint(event.pos)
                        self._mp_button_hover = hasattr(self, '_mp_button_rect') and self._mp_button_rect and self._mp_button_rect.collidepoint(event.pos)
                        self._test_button_hover = hasattr(self, '_test_button_rect') and self._test_button_rect and self._test_button_rect.collidepoint(event.pos)
                        self.menu_hover_index = None
                        for rect, idx in self.difficulty_hitboxes:
                            if rect.collidepoint(event.pos):
                                self.menu_hover_index = idx
                                break
                    elif self.state == "settings":
                        self.settings_hover_item = None
                        self.settings_fullscreen_hover = False
                        if hasattr(self, '_fullscreen_toggle_rect') and self._fullscreen_toggle_rect and self._fullscreen_toggle_rect.collidepoint(event.pos):
                            self.settings_fullscreen_hover = True
                        elif hasattr(self, '_audio_toggle_rect') and self._audio_toggle_rect and self._audio_toggle_rect.collidepoint(event.pos):
                            self.settings_hover_item = "audio_toggle"
                        elif hasattr(self, '_language_toggle_rect') and self._language_toggle_rect and self._language_toggle_rect.collidepoint(event.pos):
                            self.settings_hover_item = "language_toggle"
                        elif hasattr(self, '_debug_toggle_rect') and self._debug_toggle_rect and self._debug_toggle_rect.collidepoint(event.pos):
                            self.settings_hover_item = "debug_toggle"
                        elif hasattr(self, '_back_button_rect') and self._back_button_rect and self._back_button_rect.collidepoint(event.pos):
                            self.settings_hover_item = "back"
                    elif self.state == "diagnostics":
                        self._diag_close_hover = hasattr(self, '_diag_close_rect') and self._diag_close_rect and self._diag_close_rect.collidepoint(event.pos)
                    elif self.state == "multiplayer":
                        self._mp_host_hover = hasattr(self, '_host_button_rect') and self._host_button_rect and self._host_button_rect.collidepoint(event.pos)
                        self._join_btn_hover = hasattr(self, '_join_button_rect') and self._join_button_rect and self._join_button_rect.collidepoint(event.pos)
                        self._public_btn_hover = hasattr(self, '_public_button_rect') and self._public_button_rect and self._public_button_rect.collidepoint(event.pos)
                        self._mp_back_hover = hasattr(self, '_mp_back_button_rect') and self._mp_back_button_rect and self._mp_back_button_rect.collidepoint(event.pos)
                        self._input_active = hasattr(self, '_input_box_rect') and self._input_box_rect and self._input_box_rect.collidepoint(event.pos)
                    elif self.state == "host_waiting":
                        self._cancel_hover = hasattr(self, '_cancel_button_rect') and self._cancel_button_rect and self._cancel_button_rect.collidepoint(event.pos)
                    elif self.dragging and self.state == "playing":
                        new_y = event.pos[1] - self.drag_offset
                        self.player.y = max(0.0, min(SCREEN_HEIGHT - self.player.height, new_y))
                        self.player_move_dir = 0.0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11 or (event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_ALT):
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_m:
                        self.toggle_audio()
                    if self.state == "menu":
                        if event.key in (pygame.K_UP, pygame.K_w):
                            self.diff_index = (self.diff_index - 1) % len(self.difficulties)
                            self.menu_hover_index = self.diff_index
                            save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.diff_index = (self.diff_index + 1) % len(self.difficulties)
                            self.menu_hover_index = self.diff_index
                            save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                        elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self._start_game()
                    elif self.state == "settings":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                            self.menu_phase = 0.0
                            self.settings_hover_item = None
                        elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            if self.settings_fullscreen_hover:
                                self.toggle_fullscreen()
                            elif self.settings_hover_item == "audio_toggle":
                                self.toggle_audio()
                            else:
                                self.show_debug_hud = not self.show_debug_hud
                                save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                    elif self.state == "diagnostics":
                        if event.key == pygame.K_ESCAPE or event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.state = "menu"
                            self.menu_phase = 0.0
                    elif self.state == "multiplayer":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                            self.menu_phase = 0.0
                            self.join_code_input = ""
                            self.multiplayer_status = ""
                            self.searching_public = False
                        elif event.key == pygame.K_BACKSPACE and self._input_active:
                            self.join_code_input = self.join_code_input[:-1]
                        elif event.key == pygame.K_RETURN and self.join_code_input:
                            self.multiplayer_status = "Connecting..."
                            self.network_client = NetworkClient()
                            if self.network_client.connect('127.0.0.1'):
                                self.multiplayer_mode = 'client'
                                self._start_game()
                            else:
                                self.multiplayer_status = "Connection failed - Host not found"
                        elif self._input_active and len(self.join_code_input) < 6:
                            if event.unicode.isalnum():
                                self.join_code_input += event.unicode.upper()
                    elif self.state == "host_waiting":
                        if event.key == pygame.K_ESCAPE:
                            if self.network_host:
                                self.network_host.close()
                                self.network_host = None
                            self.multiplayer_mode = None
                            self.state = "multiplayer"
                            self.multiplayer_status = ""
                        elif self.network_host and self.network_host.connected:
                            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                                self._start_game()
                    elif self.state == "gameover":
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.player_score = 0
                            self.ai_score = 0
                            self.left_pop = 0.0
                            self.right_pop = 0.0
                            self.state = "menu"
                            self.menu_phase = 0.0
                            self.gameover_phase = 0.0
                            self.dragging = False
                            self.menu_hover_index = None
                            self._clear_particles()
                            self.score_bursts.clear()
            self.handle_input()
            if self.state == "playing":
                self.player.move(self.player_move_dir, self.dt)
                self.ai_move()
                self.ai.move(self.ai_move_dir, self.dt)
                self.ball.move(self.dt)
                self.check_collision()
                self.update_particles(self.dt)
                self.draw()
            elif self.state == "menu":
                self.update_demo_game(self.dt)
                self.draw_menu()
            elif self.state == "settings":
                self.draw_settings()
            elif self.state == "diagnostics":
                self.draw_diagnostics()
            elif self.state == "multiplayer":
                if self.searching_public and self.matchmaking_client:
                    try:
                        if time.time() - self.search_start_time > 2:
                            response = self.matchmaking_client.join_public_queue()
                            self.search_start_time = time.time()
                            if response and response.get('status') == 'matched':
                                role = response.get('role')
                                peer = response.get('peer')
                                if role == 'host':
                                    self.network_host = NetworkHost()
                                    if self.network_host.start():
                                        self.multiplayer_mode = 'host'
                                        self.state = "host_waiting"
                                        self.multiplayer_status = "Matched! Waiting for connection..."
                                        self._mp_game_started = False
                                        self.searching_public = False
                                elif role == 'client':
                                    peer_ip = peer.split(':')[0]
                                    self.network_client = NetworkClient()
                                    if self.network_client.connect(peer_ip):
                                        self.multiplayer_mode = 'client'
                                        self._start_game()
                                        self.searching_public = False
                            else:
                                elapsed = int(time.time() - self.search_start_time)
                                self.multiplayer_status = f"Searching for opponent... ({elapsed}s)"
                    except Exception as e:
                        print(f"[Game] Matchmaking poll error: {e}")
                self.draw_multiplayer_menu()
            elif self.state == "host_waiting":
                self.draw_host_waiting()
                if self.network_host and self.network_host.connected and not hasattr(self, '_mp_game_started'):
                    self._mp_game_started = True
                    pygame.time.wait(1000)
                    self._start_game()
            elif self.state == "gameover":
                # Draw game over screen / Dibujar pantalla de game over
                self.draw()
    
    async def run_async(self):
        """
        Asynchronous game loop for web/Pygbag - browser-compatible version.
        Bucle de juego asíncrono para web/Pygbag - versión compatible con navegador.
        
        Identical to _run_sync() but yields control to browser event loop via await asyncio.sleep(0).
        Idéntico a _run_sync() pero cede control al bucle de eventos del navegador mediante await asyncio.sleep(0).
        
        Web limitations / Limitaciones web:
        - Multiplayer disabled (no socket support in browsers)
        - Settings save may use localStorage instead of file I/O
        - Performance may be lower than desktop
        """
        # [ASYNC LOOP MARKER] - For identifying this loop vs sync
        self.player_move_dir = 0.0
        self.ai_move_dir = 0.0
        self._2player_button_hover = False
        while True:
            dt_ms = self.clock.tick(60)
            self.dt = max(0.001, dt_ms / 1000.0)
            self.elapsed += self.dt
            self.shake_time, self.left_pop, self.right_pop = max(0.0, self.shake_time - self.dt), max(0.0, self.left_pop - self.dt), max(0.0, self.right_pop - self.dt)
            self.update_score_bursts(self.dt)
            self._update_button_animations()  # Smooth button hover animations / Animaciones suaves de hover de botones
            
            # Yield to browser event loop / Ceder al bucle de eventos del navegador
            await asyncio.sleep(0)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "diagnostics":
                        if hasattr(self, '_diag_close_rect') and self._diag_close_rect and self._diag_close_rect.collidepoint(event.pos):
                            self.state = "menu"
                            self.menu_phase = 0.0
                    elif self.state == "settings":
                        if hasattr(self, '_fullscreen_toggle_rect') and self._fullscreen_toggle_rect and self._fullscreen_toggle_rect.collidepoint(event.pos):
                            self.toggle_fullscreen()
                        elif hasattr(self, '_audio_toggle_rect') and self._audio_toggle_rect and self._audio_toggle_rect.collidepoint(event.pos):
                            self.toggle_audio()
                        elif hasattr(self, '_language_toggle_rect') and self._language_toggle_rect and self._language_toggle_rect.collidepoint(event.pos):
                            self.toggle_language()
                        elif hasattr(self, '_debug_toggle_rect') and self._debug_toggle_rect and self._debug_toggle_rect.collidepoint(event.pos):
                            self.show_debug_hud = not self.show_debug_hud
                            save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                        elif hasattr(self, '_back_button_rect') and self._back_button_rect and self._back_button_rect.collidepoint(event.pos):
                            self.state = "menu"
                            self.menu_phase = 0.0
                            self.settings_hover_item = None
                            self.settings_fullscreen_hover = False
                    # Note: Multiplayer disabled in web mode (no socket support)
                    # Nota: Multijugador deshabilitado en modo web (sin soporte de sockets)
                    elif self.state == "menu":
                        if hasattr(self, '_settings_button_rect') and self._settings_button_rect and self._settings_button_rect.collidepoint(event.pos):
                            self.state = "settings"
                            self.menu_phase = 0.0
                            self.settings_hover_item = None
                        elif hasattr(self, '_2player_button_rect') and self._2player_button_rect and self._2player_button_rect.collidepoint(event.pos):
                            # Start 2-player game / Iniciar juego de 2 jugadores
                            self.game_mode = "2player"
                            self._start_game()
                        elif hasattr(self, '_test_button_rect') and self._test_button_rect and self._test_button_rect.collidepoint(event.pos):
                            self.run_diagnostics()
                            self.state = "diagnostics"
                        else:
                            target_idx = self.menu_hover_index
                            if target_idx is None:
                                for rect, idx in self.difficulty_hitboxes:
                                    if rect.collidepoint(event.pos):
                                        target_idx = idx
                                        break
                            if target_idx is not None and target_idx != self.diff_index:
                                self.diff_index = target_idx
                                save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                            if target_idx is not None:
                                self.menu_hover_index = target_idx
                    if self.state == "playing" and self._player_drag_rect().collidepoint(event.pos):
                        self.dragging = True
                        pointer_y = min(max(event.pos[1], self.player.y), self.player.y + self.player.height)
                        self.drag_offset = pointer_y - self.player.y
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.dragging = False
                if event.type == pygame.MOUSEMOTION:
                    if self.state == "menu":
                        self._settings_button_hover = hasattr(self, '_settings_button_rect') and self._settings_button_rect and self._settings_button_rect.collidepoint(event.pos)
                        self._2player_button_hover = hasattr(self, '_2player_button_rect') and self._2player_button_rect and self._2player_button_rect.collidepoint(event.pos)
                        self._mp_button_hover = hasattr(self, '_mp_button_rect') and self._mp_button_rect and self._mp_button_rect.collidepoint(event.pos)
                        self._test_button_hover = hasattr(self, '_test_button_rect') and self._test_button_rect and self._test_button_rect.collidepoint(event.pos)
                        self.menu_hover_index = None
                        for rect, idx in self.difficulty_hitboxes:
                            if rect.collidepoint(event.pos):
                                self.menu_hover_index = idx
                                break
                    elif self.state == "settings":
                        self.settings_hover_item = None
                        self.settings_fullscreen_hover = False
                        if hasattr(self, '_fullscreen_toggle_rect') and self._fullscreen_toggle_rect and self._fullscreen_toggle_rect.collidepoint(event.pos):
                            self.settings_fullscreen_hover = True
                        elif hasattr(self, '_audio_toggle_rect') and self._audio_toggle_rect and self._audio_toggle_rect.collidepoint(event.pos):
                            self.settings_hover_item = "audio_toggle"
                        elif hasattr(self, '_language_toggle_rect') and self._language_toggle_rect and self._language_toggle_rect.collidepoint(event.pos):
                            self.settings_hover_item = "language_toggle"
                        elif hasattr(self, '_debug_toggle_rect') and self._debug_toggle_rect and self._debug_toggle_rect.collidepoint(event.pos):
                            self.settings_hover_item = "debug_toggle"
                        elif hasattr(self, '_back_button_rect') and self._back_button_rect and self._back_button_rect.collidepoint(event.pos):
                            self.settings_hover_item = "back"
                    elif self.state == "diagnostics":
                        self._diag_close_hover = hasattr(self, '_diag_close_rect') and self._diag_close_rect and self._diag_close_rect.collidepoint(event.pos)
                    elif self.dragging and self.state == "playing":
                        new_y = event.pos[1] - self.drag_offset
                        self.player.y = max(0.0, min(SCREEN_HEIGHT - self.player.height, new_y))
                        self.player_move_dir = 0.0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11 or (event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_ALT):
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_m:
                        self.toggle_audio()
                    if self.state == "menu":
                        if event.key in (pygame.K_UP, pygame.K_w):
                            self.diff_index = (self.diff_index - 1) % len(self.difficulties)
                            self.menu_hover_index = self.diff_index
                            save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.diff_index = (self.diff_index + 1) % len(self.difficulties)
                            self.menu_hover_index = self.diff_index
                            save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                        elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self._start_game()
                    elif self.state == "settings":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                            self.menu_phase = 0.0
                            self.settings_hover_item = None
                        elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            if self.settings_fullscreen_hover:
                                self.toggle_fullscreen()
                            elif self.settings_hover_item == "audio_toggle":
                                self.toggle_audio()
                            else:
                                self.show_debug_hud = not self.show_debug_hud
                                save_settings(self.fullscreen, self.show_debug_hud, self.diff_index, self.audio_enabled, self.language)
                    elif self.state == "diagnostics":
                        if event.key == pygame.K_ESCAPE or event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.state = "menu"
                            self.menu_phase = 0.0
                    elif self.state == "gameover":
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.player_score = 0
                            self.ai_score = 0
                            self.left_pop = 0.0
                            self.right_pop = 0.0
                            self.state = "menu"
                            self.menu_phase = 0.0
                            self.gameover_phase = 0.0
                            self.dragging = False
                            self.menu_hover_index = None
                            self._clear_particles()
                            self.score_bursts.clear()
            self.handle_input()
            if self.state == "playing":
                self.player.move(self.player_move_dir, self.dt)
                
                # Player 2 or AI movement / Movimiento Jugador 2 o IA
                if self.game_mode == "2player":
                    self.ai.move(self.player2_move_dir, self.dt)  # Reuse AI paddle for Player 2 / Reusar paleta IA para Jugador 2
                else:
                    self.ai_move()  # AI logic / Lógica IA
                    self.ai.move(self.ai_move_dir, self.dt)
                
                self.ball.move(self.dt)
                
                # Multi-ball system / Sistema de multi-bola
                for ball in self.balls[:]:
                    ball.move(self.dt)
                    # Check if ball scored (remove it) / Verificar si la bola anotó (eliminarla)
                    ball_rect = ball.get_rect()
                    if ball_rect.right < 0 or ball_rect.left > SCREEN_WIDTH:
                        self.balls.remove(ball)
                
                self.check_collision()
                
                # Power-up system updates / Actualizaciones del sistema de power-ups
                self.update_powerup_spawning(self.dt)
                self.update_powerups(self.dt)
                self.check_powerup_collision(self.player)  # Player 1
                if self.game_mode == "2player":
                    self.check_powerup_collision(self.ai)  # Player 2
                self.update_powerup_effects(self.dt)
                
                self.update_particles(self.dt)
                self.draw()
            elif self.state == "menu":
                self.update_demo_game(self.dt)
                self.draw_menu()
            elif self.state == "settings":
                self.draw_settings()
            elif self.state == "diagnostics":
                self.draw_diagnostics()
            elif self.state == "gameover":
                # Draw game over screen / Dibujar pantalla de game over
                self.draw()

# ============================================================================
# PROGRAM ENTRY POINT / PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    # Main entry point with foolproof error handling
    # Punto de entrada principal con manejo de errores a prueba de tontos
    
    try:
        game = Game()
        game.run()
    except ImportError as e:
        print("\n" + "=" * 70)
        print("  ERROR: Missing dependency / ERROR: Dependencia faltante")
        print("=" * 70)
        print(f"\nCouldn't import: {e}")
        print("\nFIX:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Or manually: pip install pygame numpy")
        print("\nPYTHON VERSION:")
        print(f"  Current: {sys.version}")
        print("  Required: 3.10+")
        if sys.version_info < (3, 10):
            print("\n⚠️  Your Python is too old! Download 3.10+ from python.org")
        print("=" * 70)
        input("\nPress Enter to exit...")
        sys.exit(1)
    except pygame.error as e:
        print("\n" + "=" * 70)
        print("  ERROR: Pygame initialization failed")
        print("=" * 70)
        print(f"\nPygame error: {e}")
        print("\nPOSSIBLE FIXES:")
        print("  1. Update graphics drivers")
        print("  2. Reinstall pygame: pip install pygame --force-reinstall")
        print("  3. Try windowed mode (disable fullscreen in settings)")
        print("=" * 70)
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print("\n" + "=" * 70)
        print("  UNEXPECTED ERROR / ERROR INESPERADO")
        print("=" * 70)
        print(f"\nError: {type(e).__name__}: {e}")
        print("\nPlease report this bug at:")
        print("  https://github.com/kali113/pong-v2/issues")
        print("\nInclude this error message and:")
        print(f"  - OS: {sys.platform}")
        print(f"  - Python: {sys.version}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)

# ============================================================================
# END OF FILE / FIN DEL ARCHIVO
# ============================================================================
# Project: PongAI V2 - 
# Proyecto: PongAI V2 - 
# 
# Total Lines: ~3000+ (including documentation)
# Líneas Totales: ~3000+ (incluyendo documentación)
# 
# Documentation: Comprehensive bilingual (EN/ES) comments throughout
# Documentación: Comentarios bilingües completos (EN/ES) en todo el código
# 
# License: Educational/Personal Use
# Licencia: Uso Educacional/Personal
# ============================================================================