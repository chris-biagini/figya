"""Auto-save, named workspaces, JSON persistence."""

import json

from figya.config import AUTOSAVE_FILE, WORKSPACES_DIR
from figya.variables import VariableStore


def _ensure_dirs():
    AUTOSAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)


def autosave(variables: VariableStore):
    """Write current state to autosave file."""
    _ensure_dirs()
    data = variables.to_dict()
    AUTOSAVE_FILE.write_text(json.dumps(data, indent=2))


def autoload(variables: VariableStore):
    """Load state from autosave file if it exists."""
    if AUTOSAVE_FILE.exists():
        try:
            data = json.loads(AUTOSAVE_FILE.read_text())
            variables.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            pass


def save_workspace(name: str, variables: VariableStore):
    _ensure_dirs()
    path = WORKSPACES_DIR / f"{name}.json"
    data = variables.to_dict()
    path.write_text(json.dumps(data, indent=2))


def restore_workspace(name: str, variables: VariableStore) -> bool:
    path = WORKSPACES_DIR / f"{name}.json"
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text())
        variables.from_dict(data)
        return True
    except (json.JSONDecodeError, KeyError):
        return False


def delete_workspace(name: str) -> bool:
    path = WORKSPACES_DIR / f"{name}.json"
    if path.exists():
        path.unlink()
        return True
    return False


def list_workspaces() -> list[str]:
    _ensure_dirs()
    return sorted(p.stem for p in WORKSPACES_DIR.glob("*.json"))
