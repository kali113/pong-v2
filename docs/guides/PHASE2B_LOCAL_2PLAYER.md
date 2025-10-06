# Phase 2B: Local 2-Player Mode Implementation

**Priority**: ⭐⭐⭐ (High Impact)
**Estimated Time**: 3-4 hours
**Status**: IN PROGRESS

---

## 🎯 Objectives

Add local 2-player mode where two players can compete on the same keyboard with split controls.

---

## 🎮 Control Scheme

### Player 1 (Left Paddle):
- **W** - Move up
- **S** - Move down
- **Mouse Drag** - Alternative control (optional)

### Player 2 (Right Paddle):
- **Arrow Up** - Move up
- **Arrow Down** - Move down

---

## 📐 Technical Design

### Game Mode State
```python
# Add to Game.__init__
self.game_mode = "single"  # "single" or "2player"
self.player2_move_dir = 0.0  # Player 2 input direction
```

### Menu Integration
- Add "2 Player" button to main menu
- Position between "Single Player" difficulties and "Multiplayer"
- Visual: Bright yellow/orange color for high visibility
- Click starts 2-player game immediately

### Gameplay Changes
- **AI Disabled**: Right paddle controlled by Player 2
- **Scoring**: Track "Player 1" vs "Player 2" instead of "Player" vs "AI"
- **Power-ups**: Both players can collect (adds strategic depth)
- **Win Condition**: First to 7 points (same as single player)

---

## 🛠️ Implementation Steps

### 1. Add Game Mode Variable
```python
# In Game.__init__
self.game_mode = "single"  # "single", "2player"
self.player2_move_dir = 0.0
```

### 2. Create Menu Button
```python
# In draw_menu(), after difficulty buttons
def _draw_2player_button(self):
    \"\"\"Draw 2-player mode button.\"\"\"
    button_y = SCREEN_HEIGHT // 2 + 180
    button_width = 300
    button_height = 60
    
    button_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - button_width // 2,
        button_y,
        button_width,
        button_height
    )
    
    # Hover effect
    hovered = hasattr(self, '_2player_hover') and self._2player_hover
    color = (255, 200, 50) if hovered else (255, 150, 20)
    
    # Draw button
    pygame.draw.rect(self.screen, color, button_rect, border_radius=15)
    pygame.draw.rect(self.screen, WHITE, button_rect, width=3, border_radius=15)
    
    # Draw text
    text = self.font.render("🎮 2 PLAYER", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    self.screen.blit(text, text_rect)
    
    return button_rect
```

### 3. Handle Button Click
```python
# In event handling (MOUSEBUTTONDOWN)
elif hasattr(self, '_2player_button_rect') and self._2player_button_rect.collidepoint(event.pos):
    self.game_mode = "2player"
    self._start_game()
```

### 4. Update Input Handling
```python
def handle_input(self):
    \"\"\"Handle keyboard input for 1 or 2 players.\"\"\"
    keys = pygame.key.get_pressed()
    
    if self.state == "playing":
        # Player 1 (left paddle) - W/S keys
        dir_y = 0.0
        if not self.dragging:
            if keys[pygame.K_w]:
                dir_y -= 1.0
            if keys[pygame.K_s]:
                dir_y += 1.0
        self.player_move_dir = dir_y if not self.dragging else 0.0
        
        # Player 2 (right paddle) - Arrow keys (only in 2-player mode)
        if self.game_mode == "2player":
            p2_dir = 0.0
            if keys[pygame.K_UP]:
                p2_dir -= 1.0
            if keys[pygame.K_DOWN]:
                p2_dir += 1.0
            self.player2_move_dir = p2_dir
        
        # ESC = settings
        if keys[pygame.K_ESCAPE]:
            self.state = "settings"
            self.menu_phase = 0.0
```

### 5. Update Game Loop
```python
# In run() - playing state
if self.state == "playing":
    # Player 1 movement
    self.player.move(self.player_move_dir, self.dt)
    
    # Player 2 or AI movement
    if self.game_mode == "2player":
        self.ai.move(self.player2_move_dir, self.dt)  # Reuse AI paddle for Player 2
    else:
        self.ai_move()  # AI logic
        self.ai.move(self.ai_move_dir, self.dt)
    
    # Rest of game logic...
```

### 6. Update Score Display
```python
# In draw()
if self.game_mode == "2player":
    player1_label = self.small_font.render("Player 1", True, (200, 210, 230))
    player2_label = self.small_font.render("Player 2", True, (200, 210, 230))
else:
    player_label = self.small_font.render("Player", True, (200, 210, 230))
    ai_label = self.small_font.render("AI", True, (200, 210, 230))
```

### 7. Update Game Over Screen
```python
# In draw() - gameover state
if self.game_mode == "2player":
    if self.player_score > self.ai_score:
        winner = "Player 1"
    else:
        winner = "Player 2"
else:
    winner = "Player" if self.player_score > self.ai_score else "AI"
```

### 8. Power-Up Collection for Both Players
```python
# In check_powerup_collision - call for both paddles
if self.state == "playing":
    self.check_powerup_collision(self.player)  # Player 1
    if self.game_mode == "2player":
        self.check_powerup_collision(self.ai)  # Player 2 (using ai paddle)
```

### 9. Reset Game Mode on Menu Return
```python
# When returning to menu
def _return_to_menu(self):
    self.state = "menu"
    self.game_mode = "single"
    self.player_score = 0
    self.ai_score = 0
    self.menu_phase = 0.0
```

---

## 🎨 Visual Design

### Button Style:
- **Color**: Orange/yellow gradient (255, 200, 50)
- **Border**: White 3px
- **Hover**: Brighten color by 20%
- **Icon**: 🎮 emoji
- **Position**: Below difficulty selection, above multiplayer button

### In-Game Labels:
- **2-Player Mode**: "Player 1" and "Player 2"
- **Single Player Mode**: "Player" and "AI"
- **Color**: Same as current (white with slight blue tint)

---

## 🧪 Testing Checklist

- [ ] 2-Player button appears in menu
- [ ] Button hover effect works
- [ ] Clicking button starts 2-player game
- [ ] Player 1 controls (W/S) work
- [ ] Player 2 controls (Arrow keys) work
- [ ] Both players can collect power-ups
- [ ] Scoring works correctly
- [ ] Labels show "Player 1" and "Player 2"
- [ ] Game over shows correct winner
- [ ] Returning to menu resets mode
- [ ] AI doesn't interfere in 2-player mode
- [ ] Difficulty selection still works for single player
- [ ] Web version compatible

---

## 📝 Key Changes Summary

**Files Modified:**
- main.py: ~150 lines added
  - New game_mode variable
  - 2-player button rendering
  - Split input handling
  - Conditional AI logic
  - Updated labels and winner text

**No Breaking Changes:**
- Single player mode unchanged
- All existing features work in both modes
- Power-ups work for both players

---

## 🚀 Next Phase

After 2-player mode:
- Phase 2C: New Game Modes (Tournament, Time Attack, Survival) - 5-6 hours

**Total Phase 2 Time**: 10-12 hours (Power-Ups: 2h, 2-Player: 3h, Game Modes: 5-6h)
