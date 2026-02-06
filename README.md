# figya

A modern terminal calculator with unit conversions, variables, and session persistence.

## Install

```bash
pipx install .
```

Or with pip in a virtual environment:

```bash
pip install .
```

## Usage

```bash
figya              # interactive REPL
figya -e "2+2"     # evaluate and exit
echo "5+5" | figya # piped input
```

### Math

```
figya> 2 + 2
  $1 = 4
figya> sin(pi/4)
  $2 = 0.7071067812
figya> 2^10
  $3 = 1,024
figya> 5!
  $4 = 120
figya> 2pi
  $5 = 6.283185307
```

### Unit Conversions

```
figya> 5 feet in meters
  $1 = 1.524 m
figya> 100 kg to pounds
  $2 = 220.4622622 lb
figya> 72 fahrenheit in celsius
  $3 = 22.22222222 °C
```

### Variables

```
figya> $radius = 5
  $radius = 5
figya> $radius * 2
  $1 = 10
figya> $_ + 1
  $2 = 11
```

### Commands

| Command | Description |
|---------|-------------|
| `help` | Show help |
| `list` | Show all variables |
| `save <name>` | Save workspace |
| `restore <name>` | Restore workspace |
| `delete $var` | Delete a variable |
| `clear` | Clear all variables |
| `quit` / `exit` | Quit |

### Functions

`sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sqrt`, `log`, `log2`, `ln`, `exp`, `abs`, `round`, `floor`, `ceil`, `factorial`, `degrees`, `radians`, `gcd`, `lcm`, `min`, `max`, `hex`, `oct`, `bin`

### Constants

`pi`, `e`, `tau`, `inf`

## Data

Session data is stored in `~/.local/share/figya/`.
