"""REPL commands: help, list, save, restore, delete, clear, quit."""

from figya.variables import VariableStore
from figya.evaluator import format_number
from figya.persistence import save_workspace, restore_workspace, delete_workspace, list_workspaces


HELP_TEXT = """\
  figya — terminal calculator

  Expressions:
    2 + 2              arithmetic
    sin(pi/4)          functions (sin, cos, tan, sqrt, log, ln, exp, ...)
    2^10               exponentiation
    5!                 factorial
    2pi                implicit multiplication

  Unit conversions:
    5 feet in meters
    100 kg to pounds
    72 fahrenheit in celsius

  Variables:
    $radius = 5        named variable
    $1, $2, ...        auto-named results
    $_                 last result

  Commands:
    help               this message
    list               show all variables
    save <name>        save workspace
    restore <name>     restore workspace
    delete $var        delete a variable
    delete ws <name>   delete a workspace
    clear              clear all variables
    quit / exit        quit figya\
"""


def handle_command(line: str, variables: VariableStore) -> str | None:
    """Handle a command. Returns output string, or None if not a command."""
    cmd = line.strip().lower()

    if cmd in ("quit", "exit"):
        raise SystemExit(0)

    if cmd == "help":
        return HELP_TEXT

    if cmd == "list":
        items = variables.items()
        if not items:
            return "  no variables"
        lines = [f"  {name} = {format_number(value)}" for name, value in items]
        return "\n".join(lines)

    if cmd == "clear":
        variables.clear()
        return "  cleared"

    if cmd.startswith("delete "):
        target = cmd[7:].strip()
        if target.startswith("ws "):
            ws_name = target[3:].strip()
            if delete_workspace(ws_name):
                return f"  workspace '{ws_name}' deleted"
            return f"  workspace '{ws_name}' not found"
        if not target.startswith("$"):
            target = f"${target}"
        if variables.delete(target):
            return f"  {target} deleted"
        return f"  {target} not found"

    if cmd == "save":
        return "  usage: save <name>"

    if cmd.startswith("save "):
        name = line.strip()[5:].strip()
        save_workspace(name, variables)
        return f"  workspace '{name}' saved"

    if cmd == "restore":
        names = list_workspaces()
        if not names:
            return "  no saved workspaces"
        return "  workspaces: " + ", ".join(names)

    if cmd.startswith("restore "):
        name = line.strip()[8:].strip()
        if restore_workspace(name, variables):
            return f"  workspace '{name}' restored ({variables.count} variables)"
        return f"  workspace '{name}' not found"

    return None
