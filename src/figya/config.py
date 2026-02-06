"""Paths, constants, version string."""

import os
from pathlib import Path

from figya import __version__

VERSION = __version__

# XDG-compliant data directory
DATA_DIR = Path(os.environ.get("FIGYA_DATA_DIR", Path.home() / ".local" / "share" / "figya"))
AUTOSAVE_FILE = DATA_DIR / "autosave.json"
WORKSPACES_DIR = DATA_DIR / "workspaces"
HISTORY_FILE = DATA_DIR / "history"
