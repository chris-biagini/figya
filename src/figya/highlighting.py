"""Syntax highlighting via Pygments lexer + One Dark-inspired color theme."""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Token, Number, Name, Operator, Punctuation, Keyword, String

from prompt_toolkit.styles import Style


class FigyaLexer(RegexLexer):
    name = "Figya"
    tokens = {
        "root": [
            # Commands
            (r'\b(help|list|save|restore|delete|clear|quit|exit)\b', Keyword),
            # Unit conversion keywords
            (r'\b(in|to)\b', Keyword),
            # Numbers (including decimals and negative)
            (r'-?\d+\.?\d*(?:e[+-]?\d+)?', Number),
            # Variables
            (r'\$[a-zA-Z_]\w*|\$\d+', Name.Variable),
            # Functions
            (r'\b(sin|cos|tan|asin|acos|atan|sqrt|log|log2|ln|exp|abs|round|floor|ceil|factorial|degrees|radians|gcd|lcm|min|max|hex|oct|bin)\b', Name.Function),
            # Constants
            (r'\b(pi|tau|e|inf)\b', Name.Constant),
            # Operators
            (r'[+\-*/^%=!]', Operator),
            # Parentheses
            (r'[()]', Punctuation),
            # Unit names (catch-all for words)
            (r'[a-zA-Z_]\w*', Name),
        ],
    }


# One Dark-inspired palette
FIGYA_STYLE = Style.from_dict({
    # Prompt
    "prompt": "#61afef bold",

    # Input highlighting
    "pygments.keyword": "#c678dd",
    "pygments.number": "#d19a66",
    "pygments.name.variable": "#e06c75",
    "pygments.name.function": "#61afef",
    "pygments.name.constant": "#d19a66 bold",
    "pygments.operator": "#56b6c2",
    "pygments.punctuation": "#abb2bf",
    "pygments.name": "#98c379",

    # Toolbar
    "bottom-toolbar": "bg:#21252b #abb2bf",
    "bottom-toolbar.text": "#abb2bf",
    "bottom-toolbar.key": "#61afef bold",

    # Completion menu
    "completion-menu.completion": "bg:#282c34 #abb2bf",
    "completion-menu.completion.current": "bg:#3e4451 #61afef",
})
