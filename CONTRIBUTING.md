# Contributing to Pong AI V2

Thank you for your interest in contributing to Pong AI V2! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/pong-ai-v2.git
   cd pong-ai-v2
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .\.venv\Scripts\Activate.ps1  # Windows
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔀 Workflow

1. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines below

3. **Test your changes** thoroughly:
   - Run the game and test all features
   - Test on different difficulty levels
   - Test settings persistence
   - Run in-game diagnostics

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Add awesome feature"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## 📝 Code Style Guidelines

### General Principles
- **Follow existing style** - Match the coding patterns already in the project
- **Write bilingual comments** - All comments should be in English and Spanish
- **Add docstrings** - Document all functions and classes
- **Use type hints** where appropriate

### Documentation Format
```python
def example_function(param1, param2):
    """
    Brief description in English.
    Breve descripción en español.
    
    Args / Argumentos:
        param1 (type): Description / Descripción
        param2 (type): Description / Descripción
    
    Returns / Retorna:
        type: Description / Descripción
    """
    pass
```

### Inline Comments
```python
# English comment / Comentario en español
variable = value
```

### Exception Handling
- Use **specific exception types**, not bare `except:`
- Provide fallback behavior when appropriate

```python
try:
    risky_operation()
except ValueError as e:
    # Handle specific error / Manejar error específico
    fallback_behavior()
except IOError:
    pass  # Silent fail is acceptable here / Fallo silencioso es aceptable aquí
```

### Naming Conventions
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names (not `x`, `y` unless coordinates)

## 🐛 Bug Reports

When reporting bugs, please include:

1. **System Information**:
   - OS (Windows/Linux/Mac)
   - Python version: `python --version`
   - Package versions: `pip list`

2. **Steps to Reproduce**:
   - Detailed steps to trigger the bug
   - Expected behavior
   - Actual behavior

3. **Error Messages**:
   - Full error traceback
   - Screenshots if applicable

4. **In-Game Diagnostics**:
   - Run Main Menu → Diagnostics
   - Include test results

## ✨ Feature Requests

When suggesting features:

1. **Describe the feature** clearly
2. **Explain the use case** - Why is it needed?
3. **Provide examples** if possible
4. **Consider complexity** - Is it feasible?

### Feature Ideas We'd Love
- 🌐 WebSocket-based online multiplayer
- 👤 Player profiles and statistics
- 🏆 Achievement system
- 🎨 Theme customization
- 🎮 New game modes (power-ups, obstacles)
- 📱 Mobile port
- 🎵 Background music
- 🌍 Additional language translations

## 🧪 Testing Guidelines

### Manual Testing Checklist
- [ ] Game launches without errors
- [ ] All menu buttons work
- [ ] Settings save and load correctly
- [ ] All difficulty levels work
- [ ] Fullscreen toggle works
- [ ] Audio toggle works
- [ ] Language switch works (EN/ES)
- [ ] Game over and restart work
- [ ] Diagnostics complete successfully
- [ ] No visual glitches

### Performance Testing
- [ ] Maintains 60 FPS during gameplay
- [ ] No memory leaks (check with Task Manager)
- [ ] Particle system doesn't lag
- [ ] Settings changes apply immediately

## 📦 Pull Request Guidelines

### PR Title Format
Use conventional commit format:
- `feat: Add new feature`
- `fix: Fix bug description`
- `docs: Update documentation`
- `style: Code style changes`
- `refactor: Code refactoring`
- `perf: Performance improvement`
- `test: Add tests`

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
Describe how you tested the changes

## Screenshots (if applicable)
Add screenshots for visual changes

## Checklist
- [ ] Code follows project style
- [ ] Comments are bilingual (EN/ES)
- [ ] Docstrings added
- [ ] Tested thoroughly
- [ ] No new warnings/errors
```

## 🌍 Translation Contributions

Adding a new language:

1. **Add to TRANSLATIONS dict** in `main.py`:
```python
TRANSLATIONS = {
    'en': { ... },
    'es': { ... },
    'fr': {  # Add French
        'title': 'Pong IA',
        'subtitle': 'ESPACE / ENTRÉE pour commencer',
        # ... all other keys
    }
}
```

2. **Update language toggle** in `toggle_language()` method

3. **Test all UI elements** with new language

## 💻 Development Environment

### Recommended Tools
- **Python 3.10+** (required)
- **VS Code** with Python extension
- **Git** for version control
- **Virtual environment** for isolation

### Helpful VS Code Extensions
- Python
- Pylance
- GitLens
- Error Lens

## 🤝 Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on what's best for the project
- Accept constructive criticism gracefully
- Help others learn and improve

## 📞 Getting Help

- **GitHub Discussions** - Ask questions
- **GitHub Issues** - Report bugs
- **Pull Request Comments** - Code-specific questions

## 🎉 Recognition

Contributors will be:
- Listed in README.md
- Credited in commit history
- Thanked in release notes

Thank you for contributing! 🚀
