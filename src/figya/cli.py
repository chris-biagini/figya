"""argparse, -e/pipe/repl dispatch."""

import argparse
import sys

from figya import __version__
from figya.variables import VariableStore
from figya.evaluator import Evaluator
from figya.persistence import autoload, autosave


def _eval_and_print(expr: str, evaluator: Evaluator):
    """Evaluate a single expression and print the result."""
    try:
        result = evaluator.evaluate(expr)
        if result is not None:
            print(result.strip())
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="figya",
        description="A modern terminal calculator",
    )
    parser.add_argument("-e", "--eval", metavar="EXPR", help="evaluate expression and exit")
    parser.add_argument("-V", "--version", action="version", version=f"figya {__version__}")
    parser.add_argument(
        "--about", action="store_true",
        help="show info about figya",
    )

    args = parser.parse_args()

    if args.about:
        print(f"figya {__version__}")
        print("A modern terminal calculator with unit conversions.")
        print("https://github.com/chris-biagini/figya")
        return

    variables = VariableStore()
    evaluator = Evaluator(variables)

    # -e flag: evaluate and exit
    if args.eval:
        _eval_and_print(args.eval, evaluator)
        return

    # Piped input: evaluate each line
    if not sys.stdin.isatty():
        from figya.commands import handle_command
        autoload(variables)
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            # Try commands first
            cmd_result = handle_command(line, variables)
            if cmd_result is not None:
                print(cmd_result.strip())
                continue
            try:
                result = evaluator.evaluate(line)
                if result is not None:
                    print(result.strip())
            except (ValueError, Exception) as e:
                print(f"error: {e}", file=sys.stderr)
        autosave(variables)
        return

    # Interactive REPL
    from figya.repl import run_repl
    run_repl()
