# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Install

```bash
# Install globally (recommended)
pipx install .

# Or in a venv (non-editable — editable installs break on iCloud paths with spaces)
python3 -m venv .venv && source .venv/bin/activate && pip install .

# Reinstall after code changes (must re-run since editable installs don't work)
pip install --force-reinstall --no-deps .

# Build for PyPI
pyproject-build && twine upload dist/*
```

Version is tracked in two places: `pyproject.toml` and `src/figya/__init__.py`. Keep them in sync.

## Architecture

**Three entry modes** (all in `cli.py`): interactive REPL, `-e` flag, piped stdin. All share the same evaluation core.

**Expression routing** (`evaluator.py:Evaluator.evaluate`) — the central dispatch:
1. Variable assignment (`$name = expr`) → store in VariableStore
2. Unit conversion (`<expr> in|to <unit>`) → Pint, with temperature alias mapping (fahrenheit→degF, etc.). Uses `ureg.Quantity()` not `parse_expression()` for offset units.
3. Math fallback → simpleeval with `^` remapped to exponentiation

**Preprocessing** happens before math eval: `5!` → `factorial(5)`, `2pi` → `2*pi`

**Module dependencies flow one direction**: `cli` → `repl` → `evaluator`/`commands` → `variables`/`persistence`. The shared `format_number()` lives in `evaluator.py` and is imported by `commands.py` and `repl.py`.

## Key Technical Constraints

- Pint's `UnitRegistry` is lazy-loaded (first unit conversion has a small delay)
- `!` has special meaning in bash — test factorial expressions via `subprocess` or single-quoted strings, not double-quoted `figya -e` calls
- Data directory: `~/.local/share/figya/` (override with `FIGYA_DATA_DIR` env var)
- Autosave runs after every expression in REPL and pipe modes; `-e` mode does not autosave
