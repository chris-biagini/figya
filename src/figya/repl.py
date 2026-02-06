"""prompt_toolkit REPL session + main loop."""

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.lexers import PygmentsLexer

from figya.config import HISTORY_FILE, DATA_DIR
from figya.variables import VariableStore
from figya.evaluator import Evaluator, format_number
from figya.commands import handle_command
from figya.persistence import autosave, autoload
from figya.completions import FigyaCompleter
from figya.highlighting import FigyaLexer, FIGYA_STYLE


def run_repl():
    """Start the interactive REPL."""
    variables = VariableStore()
    evaluator = Evaluator(variables)

    # Load previous session
    autoload(variables)

    # Ensure history dir exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    def toolbar():
        last = variables.last
        last_str = format_number(last) if last is not None else "—"
        count = variables.count
        return HTML(
            f'<b>$_</b> = {last_str}  |  '
            f'{count} var{"s" if count != 1 else ""}'
            f'  |  <b>help</b> for commands'
        )

    session: PromptSession = PromptSession(
        history=FileHistory(str(HISTORY_FILE)),
        auto_suggest=AutoSuggestFromHistory(),
        completer=FigyaCompleter(variables),
        lexer=PygmentsLexer(FigyaLexer),
        style=FIGYA_STYLE,
        bottom_toolbar=toolbar,
        complete_while_typing=False,
    )

    while True:
        try:
            line = session.prompt([("class:prompt", "figya> ")])
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        line = line.strip()
        if not line:
            continue

        # Try commands first
        cmd_result = handle_command(line, variables)
        if cmd_result is not None:
            print(cmd_result)
            autosave(variables)
            continue

        # Evaluate expression
        try:
            result = evaluator.evaluate(line)
            if result is not None:
                print(result)
                autosave(variables)
        except ValueError as e:
            print(f"  error: {e}")
        except Exception as e:
            print(f"  error: {e}")
