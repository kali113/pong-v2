# Phase 2: Power-Ups System Implementation

**Priority**: ⭐⭐⭐ (Highest Impact)
**Estimated Time**: 4-5 hours
**Status**: IN PROGRESS

---

## 🎯 Objectives

Create a dynamic power-up system that spawns collectible bonuses during gameplay, adding strategic depth and excitement.

---

## 🔷 Power-Up Types (6 Total)

1. **Big Paddle** 🟦
   - Effect: +50% paddle height for 10 seconds
   - Visual: Blue glow
   - Rarity: Common (30%)
   
2. **Multi-Ball** 🔴
   - Effect: Splits ball into 2-3 balls
   - Visual: Red glow with split icon
   - Rarity: Rare (15%)
   - Challenge: All balls must be managed
   
3. **Speed Boost** ⚡
   - Effect: Ball speed +50% for 10 seconds
   - Visual: Yellow lightning bolt
   - Rarity: Common (25%)
   
4. **Shield** 🛡️
   - Effect: Next point loss doesn't count (1 use)
   - Visual: Green shield icon
   - Rarity: Uncommon (20%)
   
5. **Slow Motion** 🎯
   - Effect: Ball speed -50% for 10 seconds
   - Visual: Blue clock icon
   - Rarity: Uncommon (15%)
   
6. **Chaos Ball** 🌀
   - Effect: Ball bounces erratically for 15 seconds
   - Visual: Purple spiral
   - Rarity: Rare (10%)

---

## 📐 Technical Design

### PowerUp Class
```python
@dataclass
class PowerUp:
    type: str  # 'big_paddle', 'multi_ball', etc.
    x: float
    y: float
    size: float = 30.0
    lifetime: float = 8.0  # Despawn after 8 seconds
    active: bool = True
    vx: float = 0.0  # Slow horizontal drift
    vy: float = 50.0  # Slow downward fall
    glow_phase: float = 0.0  # For pulsing animation
```

### Game Class Additions
```python
class Game:
    def __init__(self):
        # Existing code...
        self.powerups: List[PowerUp] = []
        self.active_effects: Dict[str, float] = {}  # type -> time_remaining
        self.powerup_spawn_timer: float = 0.0
        self.powerup_spawn_interval: float = 15.0  # Spawn every 15 seconds
        self.balls: List[Ball] = []  # Multi-ball support
        self.shield_active: bool = False
```

### Core Methods

#### 1. Spawning System
```python
def update_powerup_spawning(self, dt):
    """Spawn power-ups at intervals"""
    if self.state != "playing":
        return
    
    self.powerup_spawn_timer += dt
    if self.powerup_spawn_timer >= self.powerup_spawn_interval:
        self.spawn_powerup()
        self.powerup_spawn_timer = 0.0
        # Random interval variation (12-18 seconds)
        self.powerup_spawn_interval = 12.0 + random.random() * 6.0
```

#### 2. Spawn Logic
```python
def spawn_powerup(self):
    """Create new power-up at random position"""
    # Weighted random selection
    types = ['big_paddle', 'speed_boost', 'shield', 'slow_motion', 'multi_ball', 'chaos_ball']
    weights = [30, 25, 20, 15, 15, 10]
    
    powerup_type = random.choices(types, weights=weights)[0]
    
    # Spawn in middle third of screen
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
```

#### 3. Collision Detection
```python
def check_powerup_collision(self, paddle):
    """Check if paddle collected a power-up"""
    for powerup in self.powerups[:]:
        if not powerup.active:
            continue
        
        # Rectangle collision
        if (powerup.x < paddle.x + paddle.width and
            powerup.x + powerup.size > paddle.x and
            powerup.y < paddle.y + paddle.height and
            powerup.y + powerup.size > paddle.y):
            
            self.activate_powerup(powerup.type)
            self.powerups.remove(powerup)
            self.play_sound('powerup_collect', pitch=1.5)
            
            # Particle burst at collection point
            self.add_particles(powerup.x, powerup.y, count=20, color=self.get_powerup_color(powerup.type))
```

#### 4. Activation System
```python
def activate_powerup(self, type: str):
    """Apply power-up effect"""
    if type == 'big_paddle':
        self.active_effects['big_paddle'] = 10.0
        self.player.height = self.player.original_height * 1.5
    
    elif type == 'multi_ball':
        # Create 2 additional balls
        for _ in range(2):
            new_ball = Ball(
                x=self.ball.x,
                y=self.ball.y,
                vx=self.ball.vx * random.uniform(0.8, 1.2),
                vy=self.ball.vy * random.uniform(0.8, 1.2)
            )
            self.balls.append(new_ball)
    
    elif type == 'speed_boost':
        self.active_effects['speed_boost'] = 10.0
        self.ball.vx *= 1.5
        self.ball.vy *= 1.5
    
    elif type == 'shield':
        self.shield_active = True
    
    elif type == 'slow_motion':
        self.active_effects['slow_motion'] = 10.0
        self.ball.vx *= 0.5
        self.ball.vy *= 0.5
    
    elif type == 'chaos_ball':
        self.active_effects['chaos_ball'] = 15.0
```

#### 5. Update Effects
```python
def update_powerup_effects(self, dt):
    """Update active power-up timers"""
    expired = []
    
    for effect_type, time_remaining in self.active_effects.items():
        time_remaining -= dt
        
        if time_remaining <= 0:
            self.deactivate_powerup(effect_type)
            expired.append(effect_type)
        else:
            self.active_effects[effect_type] = time_remaining
    
    for effect in expired:
        del self.active_effects[effect]
```

#### 6. Deactivation
```python
def deactivate_powerup(self, type: str):
    """Remove power-up effect"""
    if type == 'big_paddle':
        self.player.height = self.player.original_height
    
    elif type == 'speed_boost':
        self.ball.vx /= 1.5
        self.ball.vy /= 1.5
    
    elif type == 'slow_motion':
        self.ball.vx /= 0.5
        self.ball.vy /= 0.5
```

#### 7. Rendering
```python
def draw_powerups(self):
    """Draw all active power-ups"""
    for powerup in self.powerups:
        if not powerup.active:
            continue
        
        # Update glow animation
        powerup.glow_phase += self.dt * 3
        glow_intensity = 0.5 + 0.5 * math.sin(powerup.glow_phase)
        
        color = self.get_powerup_color(powerup.type)
        
        # Draw glow
        glow_radius = int(powerup.size * (1.5 + 0.3 * glow_intensity))
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, 50), (glow_radius, glow_radius), glow_radius)
        self.screen.blit(glow_surf, (powerup.x - glow_radius, powerup.y - glow_radius))
        
        # Draw power-up
        pygame.draw.circle(self.screen, color, (int(powerup.x), int(powerup.y)), int(powerup.size / 2))
        
        # Draw icon
        self.draw_powerup_icon(powerup)
```

#### 8. HUD Display
```python
def draw_active_effects_hud(self):
    """Show active power-ups in corner"""
    y_offset = 80
    
    for effect_type, time_remaining in self.active_effects.items():
        color = self.get_powerup_color(effect_type)
        
        # Draw icon
        icon_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(icon_surf, color, (20, 20), 15)
        self.screen.blit(icon_surf, (SCREEN_WIDTH - 60, y_offset))
        
        # Draw timer
        timer_text = self.small_font.render(f"{int(time_remaining)}s", True, WHITE)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 55, y_offset + 45))
        
        y_offset += 70
```

---

## 🎨 Visual Design

### Colors
- Big Paddle: `(100, 150, 255)` - Blue
- Multi-Ball: `(255, 100, 100)` - Red
- Speed Boost: `(255, 255, 100)` - Yellow
- Shield: `(100, 255, 100)` - Green
- Slow Motion: `(150, 200, 255)` - Light Blue
- Chaos Ball: `(200, 100, 255)` - Purple

### Animations
- Pulsing glow (sin wave)
- Slow drift and fall
- Sparkle particles on spawn
- Burst particles on collection

---

## 🔊 Audio

### New Sounds
- **powerup_spawn**: High pitch tone (frequency: 800 Hz)
- **powerup_collect**: Rising arpeggio (500 → 1000 Hz over 0.2s)
- **powerup_expire**: Descending tone (600 → 300 Hz over 0.3s)

### Implementation
```python
def play_sound(self, sound_type, pitch=1.0):
    if sound_type == 'powerup_collect':
        # Rising arpeggio
        for freq in [500, 650, 800, 1000]:
            tone = self.generate_tone(freq * pitch, 0.05)
            self.play_audio(tone)
```

---

## 🧪 Testing Checklist

- [ ] Power-ups spawn at correct intervals
- [ ] Collision detection works for both paddles
- [ ] All 6 types activate correctly
- [ ] Effects expire after duration
- [ ] Multi-ball creates additional balls
- [ ] Shield blocks one point
- [ ] HUD displays active effects
- [ ] Visual effects (glow, particles) work
- [ ] Sounds play correctly
- [ ] No memory leaks (power-ups get cleaned up)
- [ ] Web version compatible (async loop works)
- [ ] Desktop version compatible

---

## 📝 Implementation Steps

1. ✅ Create PowerUp dataclass
2. ✅ Add powerups list to Game.__init__
3. ✅ Implement spawning system
4. ✅ Add collision detection
5. ✅ Implement activation logic
6. ✅ Add effect timers and updates
7. ✅ Implement deactivation
8. ✅ Add visual rendering
9. ✅ Create HUD display
10. ✅ Add sound effects
11. ✅ Test all types
12. ✅ Test multi-ball edge cases
13. ✅ Balance spawn rates

---

## 🚀 Next Phase

After power-ups complete:
- Phase 2B: Local 2-Player Mode (3-4 hours)
- Phase 2C: New Game Modes (5-6 hours)

**Total Phase 2 Time**: 12-15 hours
