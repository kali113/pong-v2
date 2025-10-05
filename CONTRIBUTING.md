# Contributing to Pong AI V2

**Completely vibe coded with Claude Sonnet 4.5 in Copilot Chat with agent mode and TaskSync V5 from user 4regab.**

## Quick Start

1. Fork → Clone: `git clone https://github.com/yourusername/pong-v2.git`
2. Virtual env: `python -m venv .venv` (activate: `source .venv/bin/activate` or `.\.venv\Scripts\Activate.ps1`)
3. Install: `pip install -r requirements.txt`
4. Create branch: `git checkout -b feature/your-feature`
5. Make changes, test, commit: `git commit -m "feat: Description"`
6. Push and open PR

## Code Style

- **Bilingual comments** (EN/ES): `# English / Español`
- **Docstrings** with brief EN/ES descriptions
- **Specific exceptions** (no bare `except:`)
- `snake_case` functions, `PascalCase` classes

Example:
```python
def example(param):
    """Brief description. / Breve descripción."""
    # Comment / Comentario
    pass
```

## PR Guidelines

**Title**: `feat:` / `fix:` / `docs:` + description

**Checklist**:
- [ ] Bilingual comments
- [ ] Tested thoroughly
- [ ] No new errors

## Bug Reports

Include OS, Python version, steps to reproduce, error messages.

## Feature Ideas

Online multiplayer, achievements, themes, new game modes, more languages.

Thank you! 🚀
