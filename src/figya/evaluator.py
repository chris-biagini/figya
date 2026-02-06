"""Expression routing: units vs math."""

import math
import re

from simpleeval import SimpleEval, NameNotDefined, FunctionNotDefined

from figya.variables import VariableStore


MATH_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sqrt": math.sqrt,
    "log": math.log10,
    "log2": math.log2,
    "ln": math.log,
    "exp": math.exp,
    "abs": abs,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
    "factorial": math.factorial,
    "degrees": math.degrees,
    "radians": math.radians,
    "gcd": math.gcd,
    "lcm": math.lcm,
    "min": min,
    "max": max,
    "hex": hex,
    "oct": oct,
    "bin": bin,
}

MATH_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "inf": math.inf,
}

# Pattern for unit conversion: <expr> in|to <unit>
UNIT_CONVERSION_RE = re.compile(r'^(.+?)\s+(?:in|to)\s+(.+)$', re.IGNORECASE)


def _preprocess_factorial(expr: str) -> str:
    """Convert 5! to factorial(5)."""
    return re.sub(r'(\d+)!', r'factorial(\1)', expr)


def _preprocess_implicit_multiplication(expr: str) -> str:
    """Convert 2pi to 2*pi, 3sin(x) to 3*sin(x), etc."""
    # number followed by letter (variable or function)
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    # closing paren followed by opening paren or letter
    expr = re.sub(r'\)(\()', r')*\1', expr)
    expr = re.sub(r'\)([a-zA-Z])', r')*\1', expr)
    return expr


class Evaluator:
    def __init__(self, variables: VariableStore):
        self.variables = variables
        self._pint_ureg = None

    def _get_ureg(self):
        if self._pint_ureg is None:
            import pint
            self._pint_ureg = pint.UnitRegistry()
        return self._pint_ureg

    def evaluate(self, raw_expr: str) -> str | None:
        """Evaluate an expression, return formatted result string or None."""
        expr = raw_expr.strip()
        if not expr:
            return None

        # Check for variable assignment: $name = expr
        assign_match = re.match(r'^\$([a-zA-Z_]\w*)\s*=\s*(.+)$', expr)
        if assign_match:
            var_name = f"${assign_match.group(1)}"
            value_expr = assign_match.group(2)
            result = self._eval_expression(value_expr)
            self.variables.set(var_name, result)
            return f"  {var_name} = {format_number(result)}"

        # Try unit conversion first, then math
        result = self._try_unit_conversion(expr)
        if result is not None:
            name = self.variables.add_result(result[0])
            return f"  {name} = {result[1]}"

        # Math evaluation
        value = self._eval_expression(expr)
        name = self.variables.add_result(value)
        return f"  {name} = {format_number(value)}"

    def _try_unit_conversion(self, expr: str) -> tuple[float, str] | None:
        """Try to parse as unit conversion. Returns (numeric_value, formatted_string) or None."""
        match = UNIT_CONVERSION_RE.match(expr)
        if not match:
            return None

        from_expr = match.group(1).strip()
        to_unit = match.group(2).strip()

        # Friendly aliases for temperature
        temp_aliases = {
            "fahrenheit": "degF", "farenheit": "degF", "f": "degF",
            "celsius": "degC", "centigrade": "degC", "c": "degC",
            "kelvin": "K",
        }

        to_unit_mapped = temp_aliases.get(to_unit.lower(), to_unit)

        try:
            ureg = self._get_ureg()

            # Try to split from_expr into value + unit
            num_match = re.match(r'^(-?\d+\.?\d*(?:e[+-]?\d+)?)\s*(.+)$', from_expr)
            if num_match:
                value = float(num_match.group(1))
                from_unit = num_match.group(2).strip()
                from_unit_mapped = temp_aliases.get(from_unit.lower(), from_unit)
                quantity = ureg.Quantity(value, from_unit_mapped)
            else:
                quantity = ureg.parse_expression(from_expr)

            converted = quantity.to(to_unit_mapped)
            magnitude = converted.magnitude
            # Use friendly unit display
            unit_str = f"{converted.units:~P}"
            return (float(magnitude), f"{format_number(magnitude)} {unit_str}")
        except Exception:
            return None

    def _eval_expression(self, expr: str) -> float:
        """Evaluate a math expression with variable substitution."""
        # Substitute variables
        expr = self.variables.substitute(expr)

        # Preprocess
        expr = _preprocess_factorial(expr)
        expr = _preprocess_implicit_multiplication(expr)

        # Build evaluator
        s = SimpleEval()
        s.functions = MATH_FUNCTIONS
        s.names = dict(MATH_CONSTANTS)

        # Remap ^ to power instead of XOR
        import ast
        s.operators[ast.BitXor] = lambda a, b: a ** b

        try:
            result = s.eval(expr)
        except NameNotDefined as e:
            raise ValueError(str(e))
        except FunctionNotDefined as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(str(e))

        if isinstance(result, str):
            return result
        return float(result)


def format_number(value) -> str:
    """Format a number for display."""
    if isinstance(value, str):
        return value
    if isinstance(value, float):
        if value == float('inf'):
            return "inf"
        if value == float('-inf'):
            return "-inf"
        if value != value:  # NaN
            return "NaN"
        if value == int(value) and abs(value) < 1e15:
            return f"{int(value):,}"
        # Use reasonable precision
        formatted = f"{value:,.10g}"
        return formatted
    return str(value)
