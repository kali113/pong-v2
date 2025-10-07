# ============================================================================
# PONG AI V2 - WEB EDITION (Pygbag Compatible)
# Browser-playable version using WebAssembly
# ============================================================================

__version__ = "1.0.0-pre-alpha-web"

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
        print("[Web Debug] AsyncGameWrapper.run() started")
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

            # Handle continuous input (keyboard state)
            self.game.handle_input()

            # State-specific updates (mirroring _run_sync logic)
            if self.game.state == "playing":
                self.game.player.move(self.game.player_move_dir, self.game.dt)
                self.game.ai_move()
                self.game.ai.move(self.game.ai_move_dir, self.game.dt)
                self.game.ball.move(self.game.dt)
                self.game.check_collision()
                self.game.update_particles(self.game.dt)
                self.game.draw()
            elif self.game.state == "menu":
                self.game.update_demo_game(self.game.dt)
                self.game.draw_menu()
            elif self.game.state == "settings":
                self.game.draw_settings()
            elif self.game.state == "diagnostics":
                self.game.draw_diagnostics()
            elif self.game.state == "multiplayer":
                # Multiplayer disabled in web, but draw the menu anyway
                self.game.draw_multiplayer_menu()
            elif self.game.state == "host_waiting":
                self.game.draw_host_waiting()
            elif self.game.state == "gameover":
                self.game.draw()

            # Update display
            pygame.display.flip()

            # CRITICAL: Yield control to browser event loop
            await asyncio.sleep(0)
    
    def handle_event(self, event):
        """Handle pygame events (mirroring _run_sync logic)"""
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
                elif hasattr(self.game, '_theme_toggle_rect') and self.game._theme_toggle_rect.collidepoint(event.pos):
                    self.game.toggle_theme()
                elif hasattr(self.game, '_debug_toggle_rect') and self.game._debug_toggle_rect.collidepoint(event.pos):
                    self.game.show_debug_hud = not self.game.show_debug_hud
                    save_settings(self.game.fullscreen, self.game.show_debug_hud, self.game.diff_index, self.game.audio_enabled, self.game.language, self.game.theme)
                elif hasattr(self.game, '_back_button_rect') and self.game._back_button_rect.collidepoint(event.pos):
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0
                    self.game.settings_hover_item = None
                    self.game.settings_fullscreen_hover = False
            elif self.game.state == "multiplayer":
                # Multiplayer disabled in web version, but handle menu navigation
                if hasattr(self.game, '_mp_back_button_rect') and self.game._mp_back_button_rect.collidepoint(event.pos):
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0
                    self.game.join_code_input = ""
                    self.game.multiplayer_status = ""
                    self.game.searching_public = False
            elif self.game.state == "host_waiting":
                if hasattr(self.game, '_cancel_button_rect') and self.game._cancel_button_rect.collidepoint(event.pos):
                    if self.game.network_host:
                        self.game.network_host.close()
                        self.game.network_host = None
                    self.game.multiplayer_mode = None
                    self.game.state = "multiplayer"
                    self.game.multiplayer_status = ""
            elif self.game.state == "menu":
                if hasattr(self.game, '_settings_button_rect') and self.game._settings_button_rect.collidepoint(event.pos):
                    self.game.state = "settings"
                    self.game.menu_phase = 0.0
                    self.game.settings_hover_item = None
                elif hasattr(self.game, '_2player_button_rect') and self.game._2player_button_rect.collidepoint(event.pos):
                    self.game.game_mode = "2player"
                    self.game._start_game()
                elif hasattr(self.game, '_mp_button_rect') and self.game._mp_button_rect.collidepoint(event.pos):
                    self.game.state = "multiplayer"
                    self.game.menu_phase = 0.0
                    self.game.multiplayer_status = ""
                elif hasattr(self.game, '_test_button_rect') and self.game._test_button_rect.collidepoint(event.pos):
                    self.game.run_diagnostics()
                    self.game.state = "diagnostics"
                else:
                    target_idx = self.game.menu_hover_index
                    if target_idx is None:
                        for rect, idx in self.game.difficulty_hitboxes:
                            if rect.collidepoint(event.pos):
                                target_idx = idx
                                break
                    if target_idx is not None and target_idx != self.game.diff_index:
                        self.game.diff_index = target_idx
                        save_settings(self.game.fullscreen, self.game.show_debug_hud, self.game.diff_index, self.game.audio_enabled, self.game.language, self.game.theme)
                    if target_idx is not None:
                        self.game.menu_hover_index = target_idx
            if self.game.state == "playing" and self.game._player_drag_rect().collidepoint(event.pos):
                self.game.dragging = True
                pointer_y = min(max(event.pos[1], self.game.player.y), self.game.player.y + self.game.player.height)
                self.game.drag_offset = pointer_y - self.game.player.y

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.game.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.game.state == "menu":
                self.game._settings_button_hover = hasattr(self.game, '_settings_button_rect') and self.game._settings_button_rect.collidepoint(event.pos)
                self.game._2player_button_hover = hasattr(self.game, '_2player_button_rect') and self.game._2player_button_rect.collidepoint(event.pos)
                self.game._mp_button_hover = hasattr(self.game, '_mp_button_rect') and self.game._mp_button_rect.collidepoint(event.pos)
                self.game._test_button_hover = hasattr(self.game, '_test_button_rect') and self.game._test_button_rect.collidepoint(event.pos)
                self.game.menu_hover_index = None
                for rect, idx in self.game.difficulty_hitboxes:
                    if rect.collidepoint(event.pos):
                        self.game.menu_hover_index = idx
                        break
            elif self.game.state == "settings":
                self.game.settings_hover_item = None
                self.game.settings_fullscreen_hover = False
                if hasattr(self.game, '_fullscreen_toggle_rect') and self.game._fullscreen_toggle_rect.collidepoint(event.pos):
                    self.game.settings_fullscreen_hover = True
                elif hasattr(self.game, '_audio_toggle_rect') and self.game._audio_toggle_rect and self.game._audio_toggle_rect.collidepoint(event.pos):
                    self.game.settings_hover_item = "audio_toggle"
                elif hasattr(self.game, '_language_toggle_rect') and self.game._language_toggle_rect.collidepoint(event.pos):
                    self.game.settings_hover_item = "language_toggle"
                elif hasattr(self.game, '_theme_toggle_rect') and self.game._theme_toggle_rect.collidepoint(event.pos):
                    self.game.settings_hover_item = "theme_toggle"
                elif hasattr(self.game, '_debug_toggle_rect') and self.game._debug_toggle_rect.collidepoint(event.pos):
                    self.game.settings_hover_item = "debug_toggle"
                elif hasattr(self.game, '_back_button_rect') and self.game._back_button_rect.collidepoint(event.pos):
                    self.game.settings_hover_item = "back"
            elif self.game.state == "diagnostics":
                self.game._diag_close_hover = hasattr(self.game, '_diag_close_rect') and self.game._diag_close_rect.collidepoint(event.pos)
            elif self.game.state == "multiplayer":
                self.game._mp_host_hover = hasattr(self.game, '_host_button_rect') and self.game._host_button_rect.collidepoint(event.pos)
                self.game._join_btn_hover = hasattr(self.game, '_join_button_rect') and self.game._join_button_rect.collidepoint(event.pos)
                self.game._public_btn_hover = hasattr(self.game, '_public_button_rect') and self.game._public_button_rect.collidepoint(event.pos)
                self.game._mp_back_hover = hasattr(self.game, '_mp_back_button_rect') and self.game._mp_back_button_rect.collidepoint(event.pos)
                self.game._input_active = hasattr(self.game, '_input_box_rect') and self.game._input_box_rect.collidepoint(event.pos)
            elif self.game.state == "host_waiting":
                self.game._cancel_hover = hasattr(self.game, '_cancel_button_rect') and self.game._cancel_button_rect.collidepoint(event.pos)
            elif self.game.dragging and self.game.state == "playing":
                new_y = event.pos[1] - self.game.drag_offset
                self.game.player.y = max(0.0, min(SCREEN_HEIGHT - self.game.player.height, new_y))
                self.game.player_move_dir = 0.0

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11 or (event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_ALT):
                self.game.toggle_fullscreen()
            elif event.key == pygame.K_m:
                self.game.toggle_audio()
            if self.game.state == "menu":
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.game.diff_index = (self.game.diff_index - 1) % len(self.game.difficulties)
                    self.game.menu_hover_index = self.game.diff_index
                    save_settings(self.game.fullscreen, self.game.show_debug_hud, self.game.diff_index, self.game.audio_enabled, self.game.language, self.game.theme)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.game.diff_index = (self.game.diff_index + 1) % len(self.game.difficulties)
                    self.game.menu_hover_index = self.game.diff_index
                    save_settings(self.game.fullscreen, self.game.show_debug_hud, self.game.diff_index, self.game.audio_enabled, self.game.language, self.game.theme)
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.game.game_mode = "single"  # Set to single player mode
                    self.game._start_game()
            elif self.game.state == "settings":
                if event.key == pygame.K_ESCAPE:
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0
                    self.game.settings_hover_item = None
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if self.game.settings_fullscreen_hover:
                        self.game.toggle_fullscreen()
                    elif self.game.settings_hover_item == "audio_toggle":
                        self.game.toggle_audio()
                    else:
                        self.game.show_debug_hud = not self.game.show_debug_hud
                        save_settings(self.game.fullscreen, self.game.show_debug_hud, self.game.diff_index, self.game.audio_enabled, self.game.language, self.game.theme)
            elif self.game.state == "diagnostics":
                if event.key == pygame.K_ESCAPE or event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0
            elif self.game.state == "multiplayer":
                if event.key == pygame.K_ESCAPE:
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0
                    self.game.join_code_input = ""
                    self.game.multiplayer_status = ""
                    self.game.searching_public = False
            elif self.game.state == "host_waiting":
                if event.key == pygame.K_ESCAPE:
                    if self.game.network_host:
                        self.game.network_host.close()
                        self.game.network_host = None
                    self.game.multiplayer_mode = None
                    self.game.state = "multiplayer"
                    self.game.multiplayer_status = ""
                elif self.game.network_host and self.game.network_host.connected:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.game._start_game()
            elif self.game.state == "gameover":
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.game.player_score = 0
                    self.game.ai_score = 0
                    self.game.left_pop = 0.0
                    self.game.right_pop = 0.0
                    self.game.state = "menu"
                    self.game.menu_phase = 0.0
                    self.game.gameover_phase = 0.0
                    self.game.dragging = False
                    self.game.menu_hover_index = None
                    self.game._clear_particles()
                    self.game.score_bursts.clear()

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
