# Automata Visualizer Pro

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/PyQt5-5.15+-green.svg" alt="PyQt5">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

A powerful PyQt5-based application for visualizing, debugging, and minimizing Deterministic Finite Automata (DFA). Built with a clean MVC architecture for maintainability and extensibility.

## Screenshots

![Automata Visualizer Pro](<img width="1919" height="1079" alt="Screenshot 2025-11-29 062553" src="https://github.com/user-attachments/assets/dbd5bc59-18c0-4d31-93a4-a9371b5e4aab" />)

## Features

- **Interactive DFA Visualization**: Load DFA definitions from JSON and visualize them as beautiful, interactive state diagrams
- **Step-by-Step Debugger**: Walk through string acceptance one character at a time with visual state highlighting
- **Bulk Testing**: Test multiple input strings simultaneously and view results
- **DFA Minimization**: Automatically minimize DFAs using the table-filling algorithm
- **Draggable States**: Rearrange state positions by dragging nodes
- **Zoom & Pan**: Navigate large automata with mouse scroll and drag
- **Dark Theme**: Modern dark UI for comfortable viewing

## Table of Contents

- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [DFA JSON Format](#dfa-json-format)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
automata-visualizer-pro/
├── main.py          # GUI application (View/Controller)
├── dfa_logic.py     # DFA logic module (Model)
├── README.md        # Documentation
└── LICENSE          # MIT License
```

## Architecture

This project follows the **MVC (Model-View-Controller)** design pattern:

| Layer | File | Responsibility |
|-------|------|----------------|
| **Model** | `dfa_logic.py` | Pure DFA logic, validation, string testing, minimization algorithm. No UI dependencies. |
| **View/Controller** | `main.py` | PyQt5 GUI components, user interaction handling, visualization rendering. |

### Why MVC?

- **Separation of Concerns**: Logic is decoupled from presentation
- **Testability**: The model can be unit tested without GUI dependencies
- **Maintainability**: Changes to UI don't affect core logic and vice versa
- **Reusability**: The DFA model can be reused in other applications

## Requirements

- Python 3.7 or higher
- PyQt5 5.15 or higher

## Installation

### Option 1: Clone and Run

```bash
# Clone the repository
git clone https://github.com/yourusername/automata-visualizer-pro.git
cd automata-visualizer-pro

# Install dependencies
pip install PyQt5

# Run the application
python main.py
```

### Option 2: Virtual Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/automata-visualizer-pro.git
cd automata-visualizer-pro

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install PyQt5

# Run the application
python main.py
```

## Usage

### Starting the Application

```bash
python main.py
```

### Workflow

1. **Define DFA**: Edit the JSON in the Definition tab or use the sample DFA
2. **Load DFA**: Click "Load DFA" to parse and visualize
3. **Test Strings**: Use the Debugger tab to step through or run strings
4. **Bulk Test**: Use the Bulk Test tab to test multiple strings at once
5. **Minimize**: Click "Minimize" to reduce the DFA to its minimal form

### Tabs Overview

| Tab | Purpose |
|-----|---------|
| **Definition** | Edit DFA as JSON, load and minimize |
| **Debugger** | Step-by-step string testing with visual feedback |
| **Bulk Test** | Test multiple strings simultaneously |

### Controls

| Action | Control |
|--------|---------|
| Pan canvas | Click and drag on empty space |
| Zoom | Mouse scroll wheel |
| Move state | Drag individual state nodes |

## DFA JSON Format

### Schema

```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["0", "1"],
  "transitions": {
    "q0": {"0": "q1", "1": "q0"},
    "q1": {"0": "q2", "1": "q0"},
    "q2": {"0": "q2", "1": "q2"}
  },
  "start_state": "q0",
  "final_states": ["q2"]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `states` | `string[]` | Yes | List of all state names |
| `alphabet` | `string[]` | Yes | List of input symbols |
| `transitions` | `object` | Yes | Nested object: `state → symbol → next_state` |
| `start_state` | `string` | Yes | Name of the initial state |
| `final_states` | `string[]` | Yes | List of accepting/final states |

## API Reference

### DFA Class (`dfa_logic.py`)

```python
from dfa_logic import DFA, SAMPLE_DFA_DATA

# Create from dictionary
dfa = DFA.from_dict(data)

# Test a string
accepted, final_state, steps = dfa.test_string("001")

# Get transition
next_state = dfa.get_transition("q0", "0")

# Minimize DFA
minimized_dfa = dfa.minimize()

# Export to dictionary
data = dfa.to_dict()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `from_dict(data)` | `dict` | `DFA` | Class method to create DFA from dictionary |
| `to_dict()` | - | `dict` | Export DFA to dictionary format |
| `get_transition(state, symbol)` | `str, str` | `str \| None` | Get next state for given state and symbol |
| `test_string(test_str)` | `str` | `tuple(bool, str, list)` | Test if string is accepted. Returns (accepted, final_state, steps) |
| `minimize()` | - | `DFA` | Return a new minimized DFA |

## Examples

### Example 1: Binary strings ending with "00"

```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["0", "1"],
  "transitions": {
    "q0": {"0": "q1", "1": "q0"},
    "q1": {"0": "q2", "1": "q0"},
    "q2": {"0": "q2", "1": "q0"}
  },
  "start_state": "q0",
  "final_states": ["q2"]
}
```

**Accepts**: `00`, `100`, `1100`, `0100`  
**Rejects**: `0`, `01`, `10`, `11`

### Example 2: Binary strings with even number of 1s

```json
{
  "states": ["even", "odd"],
  "alphabet": ["0", "1"],
  "transitions": {
    "even": {"0": "even", "1": "odd"},
    "odd": {"0": "odd", "1": "even"}
  },
  "start_state": "even",
  "final_states": ["even"]
}
```

**Accepts**: `0`, `11`, `0110`, `1001`  
**Rejects**: `1`, `10`, `01`, `111`

### Example 3: Strings containing "ab"

```json
{
  "states": ["start", "saw_a", "accept"],
  "alphabet": ["a", "b"],
  "transitions": {
    "start": {"a": "saw_a", "b": "start"},
    "saw_a": {"a": "saw_a", "b": "accept"},
    "accept": {"a": "accept", "b": "accept"}
  },
  "start_state": "start",
  "final_states": ["accept"]
}
```

**Accepts**: `ab`, `aab`, `bab`, `abab`  
**Rejects**: `a`, `b`, `ba`, `aa`

## Algorithms

### DFA Minimization

The minimization uses the **Table-Filling Algorithm** (also known as the Myhill-Nerode theorem approach):

1. **Remove unreachable states**: BFS from start state to find all reachable states
2. **Mark distinguishable pairs**: Initially mark pairs where one is final and one is not
3. **Iterate**: For each unmarked pair, check if any input symbol leads to a marked pair
4. **Merge equivalent states**: States in unmarked pairs are equivalent and can be merged

**Time Complexity**: O(n²k) where n = number of states, k = alphabet size

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Keep model logic in `dfa_logic.py`
- Keep UI code in `main.py`
- Add docstrings to new functions
- Test changes before submitting PR

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'PyQt5'` | Run `pip install PyQt5` |
| Application doesn't start | Ensure Python 3.7+ is installed |
| DFA not loading | Check JSON syntax and required fields |
| States overlapping | Drag states to rearrange them |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Inspired by automata theory coursework
- Thanks to all contributors

---

<p align="center">
  Made with ❤️ for automata theory enthusiasts
</p>
