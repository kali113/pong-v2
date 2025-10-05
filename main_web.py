# ============================================================================
# PONG AI V2 - WEB EDITION (Pygbag Compatible)
# Browser-playable version using WebAssembly
# ============================================================================

__version__ = "1.0.0-alpha-web"

import asyncio
import sys

# Check if running in browser (Pyodide environment)
try:
    import platform
    IS_WEB = platform.system() == "Emscripten"
except:
    IS_WEB = False

# Import the main game (we'll patch it for web compatibility)
from main import *

# ============================================================================
# WEB-SPECIFIC OVERRIDES
# ============================================================================

# Disable socket networking for web version
if IS_WEB:
    print("[Web] Running in browser mode - multiplayer disabled")
    # Patch NetworkHost and NetworkClient to be no-ops
    class NetworkHost:
        def start(self): return False
        def stop(self): pass
    
    class NetworkClient:
        def connect(self, host, port=5555): return False
        def disconnect(self): pass
    
    class MatchmakingClient:
        def __init__(self, *args): pass
        def connect(self): return False
        def disconnect(self): pass

# ============================================================================
# ASYNC GAME LOOP WRAPPER
# ============================================================================

class AsyncGameWrapper:
    """
    Wraps the synchronous Game class with async event loop for web compatibility.
    """
    def __init__(self):
        self.game = Game()
        self.running = True
    
    async def run(self):
        """
        Async main loop - required for Pygbag/WebAssembly
        """
        self.game.player_move_dir = 0.0
        self.game.ai_move_dir = 0.0
        
        while self.running:
            # Frame timing
            dt_ms = self.game.clock.tick(60)
            self.game.dt = max(0.001, dt_ms / 1000.0)
            self.game.elapsed += self.game.dt
            
            # Update timers
            self.game.shake_time = max(0.0, self.game.shake_time - self.game.dt)
            self.game.left_pop = max(0.0, self.game.left_pop - self.game.dt)
            self.game.right_pop = max(0.0, self.game.right_pop - self.game.dt)
            self.game.update_score_bursts(self.game.dt)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                
                # Delegate event handling to game
                self.handle_event(event)
            
            # State-specific updates
            if self.game.state == "menu":
                self.game.draw_menu()
            elif self.game.state == "playing":
                self.game.update_gameplay()
                self.game.draw_gameplay()
            elif self.game.state == "gameover":
                self.game.draw_gameover()
            elif self.game.state == "settings":
                self.game.draw_settings()
            elif self.game.state == "multiplayer":
                self.game.draw_multiplayer()
            elif self.game.state == "host_waiting":
                self.game.draw_multiplayer_waiting()
            elif self.game.state == "diagnostics":
                self.game.draw_diagnostics()
            
            # Update display
            pygame.display.flip()
            
            # CRITICAL: Yield control to browser event loop
            await asyncio.sleep(0)
    
    def handle_event(self, event):
        """Handle pygame events (extracted from original run loop)"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game.state == "diagnostics":
                if hasattr(self.game, '_diag_close_rect') and self.game._diag_close_rect.collidepoint(event.pos):
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0
            elif self.game.state == "settings":
                if hasattr(self.game, '_fullscreen_toggle_rect') and self.game._fullscreen_toggle_rect.collidepoint(event.pos):
                    self.game.toggle_fullscreen()
                elif hasattr(self.game, '_audio_toggle_rect') and self.game._audio_toggle_rect and self.game._audio_toggle_rect.collidepoint(event.pos):
                    self.game.toggle_audio()
                elif hasattr(self.game, '_language_toggle_rect') and self.game._language_toggle_rect.collidepoint(event.pos):
                    self.game.toggle_language()
                elif hasattr(self.game, '_debug_toggle_rect') and self.game._debug_toggle_rect.collidepoint(event.pos):
                    self.game.show_debug_hud = not self.game.show_debug_hud
                    save_settings(self.game.fullscreen, self.game.show_debug_hud, self.game.diff_index, self.game.audio_enabled, self.game.language)
                elif hasattr(self.game, '_back_button_rect') and self.game._back_button_rect.collidepoint(event.pos):
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0
                    self.game.settings_hover_item = None
                    self.game.settings_fullscreen_hover = False
            elif self.game.state == "multiplayer":
                # Multiplayer disabled in web version
                pass
            elif self.game.state == "menu":
                # Menu interactions
                pass
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.game.state == "settings":
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0
                elif self.game.state == "playing":
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0

# ============================================================================
# WEB ENTRY POINT
# ============================================================================

async def main():
    """
    Async entry point for Pygbag
    """
    try:
        print(f"[Web] Pong AI V2 {__version__} - Starting...")
        print(f"[Web] Browser mode: {IS_WEB}")
        
        wrapper = AsyncGameWrapper()
        await wrapper.run()
        
    except Exception as e:
        print(f"[Web] Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

# Run the async main function
if __name__ == "__main__":
    if IS_WEB:
        # In browser - asyncio loop is managed by Pygbag
        asyncio.run(main())
    else:
        # Desktop testing - run with asyncio
        asyncio.run(main())
