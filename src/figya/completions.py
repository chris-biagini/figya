"""Tab completion for prompt_toolkit."""

from prompt_toolkit.completion import Completer, Completion

from figya.variables import VariableStore


# Curated list — common functions, constants, commands, units
COMPLETIONS = [
    # Functions
    "sin(", "cos(", "tan(", "asin(", "acos(", "atan(",
    "sqrt(", "log(", "log2(", "ln(", "exp(",
    "abs(", "round(", "floor(", "ceil(",
    "factorial(", "degrees(", "radians(",
    "gcd(", "lcm(", "min(", "max(",
    "hex(", "oct(", "bin(",
    # Constants
    "pi", "tau", "inf",
    # Commands
    "help", "list", "save ", "restore ", "delete ", "clear", "quit", "exit",
    # Common units
    "feet", "meters", "inches", "centimeters", "miles", "kilometers",
    "pounds", "kilograms", "ounces", "grams",
    "fahrenheit", "celsius", "kelvin",
    "liters", "gallons", "cups", "tablespoons", "teaspoons",
    "seconds", "minutes", "hours", "days",
    "mph", "kph",
]


class FigyaCompleter(Completer):
    def __init__(self, variables: VariableStore):
        self.variables = variables

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor(WORD=True)
        if not word:
            return

        word_lower = word.lower()

        # Complete variable names
        if word.startswith("$"):
            for name, _ in self.variables.items():
                if name.startswith(word):
                    yield Completion(name, start_position=-len(word))
            if "$_".startswith(word):
                yield Completion("$_", start_position=-len(word))
            return

        # Complete from curated list
        for item in COMPLETIONS:
            if item.lower().startswith(word_lower):
                yield Completion(item, start_position=-len(word))
