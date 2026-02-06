"""Variable store, substitution, auto-naming."""

import re


class VariableStore:
    def __init__(self):
        self._vars: dict[str, float] = {}
        self._counter = 0
        self._last: float | None = None

    @property
    def count(self) -> int:
        return len(self._vars)

    @property
    def last(self) -> float | None:
        return self._last

    def add_result(self, value: float) -> str:
        """Store a result with an auto-generated name. Returns the name."""
        self._counter += 1
        name = f"${self._counter}"
        self._vars[name] = value
        self._last = value
        self._vars["$_"] = value
        return name

    def set(self, name: str, value: float):
        """Set a named variable."""
        if not name.startswith("$"):
            name = f"${name}"
        self._vars[name] = value
        self._last = value
        self._vars["$_"] = value

    def get(self, name: str) -> float | None:
        return self._vars.get(name)

    def delete(self, name: str) -> bool:
        if name in self._vars and name != "$_":
            del self._vars[name]
            return True
        return False

    def clear(self):
        self._vars.clear()
        self._counter = 0
        self._last = None

    def items(self) -> list[tuple[str, float]]:
        """Return variables sorted, excluding $_."""
        return sorted(
            [(k, v) for k, v in self._vars.items() if k != "$_"],
            key=lambda x: x[0],
        )

    def substitute(self, expr: str) -> str:
        """Replace $var references with their values. Detects circular refs."""
        seen: set[str] = set()
        return self._substitute(expr, seen, depth=0)

    def _substitute(self, expr: str, seen: set[str], depth: int) -> str:
        if depth > 100:
            raise ValueError("circular reference detected")

        def replacer(match):
            name = match.group(0)
            if name in seen:
                raise ValueError(f"circular reference: {name}")
            val = self._vars.get(name)
            if val is None:
                raise ValueError(f"undefined variable: {name}")
            seen.add(name)
            return str(val)

        result = re.sub(r'\$[a-zA-Z_]\w*|\$\d+', replacer, expr)
        # Check if more substitutions needed
        if re.search(r'\$[a-zA-Z_]\w*|\$\d+', result):
            return self._substitute(result, seen, depth + 1)
        return result

    def to_dict(self) -> dict:
        """Serialize for persistence."""
        return {"vars": dict(self._vars), "counter": self._counter}

    def from_dict(self, data: dict):
        """Restore from persistence."""
        self._vars = data.get("vars", {})
        self._counter = data.get("counter", 0)
        if "$_" in self._vars:
            self._last = self._vars["$_"]
