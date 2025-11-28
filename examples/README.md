# Example DFA Files

This folder contains example DFA definitions for testing and demonstration purposes.

## How to Use

1. Open the application: `python main.py`
2. Copy the JSON content (excluding `name`, `description`, and `test_strings` fields) into the Definition tab
3. Click "Load DFA" to visualize
4. Use the test strings provided in each file for demonstration

## Examples Overview

| File | Description | States | Key Concept |
|------|-------------|--------|-------------|
| `01_binary_ends_with_00.json` | Strings ending with "00" | 3 | Basic DFA structure |
| `02_even_number_of_ones.json` | Even count of 1s | 2 | Parity checking |
| `03_contains_substring_ab.json` | Contains "ab" | 3 | Pattern matching |
| `04_divisible_by_3.json` | Binary divisible by 3 | 3 | Modular arithmetic |
| `05_starts_and_ends_same.json` | Same start/end symbol | 5 | Branching paths |
| `06_exactly_two_ones.json` | Exactly two 1s | 4 | Counting with dead state |
| `07_no_consecutive_ones.json` | No "11" substring | 3 | Rejection patterns |
| `08_minimization_demo.json` | Redundant states | 5→3 | **Minimization demo** |
| `09_self_loop_demo.json` | Self-loops | 2 | Self-loop visualization |
| `10_single_state.json` | Accept all strings | 1 | Edge case |
| `11_length_mod_3.json` | Length divisible by 3 | 3 | Length-based acceptance |
| `12_complex_5_states.json` | Contains "101" | 4 | Complex pattern |

## Presentation Order

For a comprehensive presentation, demonstrate in this order:

1. **01** - Basic introduction to DFA
2. **02** - Simple 2-state parity example
3. **10** - Edge case: single state
4. **09** - Show self-loop rendering
5. **06** - Counting with dead state concept
6. **04** - Mathematical application (divisibility)
7. **12** - Complex pattern matching
8. **08** - **Minimization feature demo** (highlight before/after)

## Test Strings

Each JSON file includes `test_strings` with `accept` and `reject` arrays. Use these in the Bulk Test tab to verify correctness.
