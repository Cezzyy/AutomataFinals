"""
DFA Logic Module (Model) - Pure DFA operations with no UI dependencies
"""


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = set(states)
        self.alphabet = list(alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = set(final_states)

    @classmethod
    def from_dict(cls, data):
        """Create DFA from dictionary representation."""
        required = ["states", "alphabet", "transitions", "start_state", "final_states"]
        for key in required:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")
        return cls(
            states=data["states"],
            alphabet=data["alphabet"],
            transitions=data["transitions"],
            start_state=data["start_state"],
            final_states=data["final_states"]
        )

    def to_dict(self):
        """Convert DFA to dictionary representation."""
        return {
            "states": list(self.states),
            "alphabet": self.alphabet,
            "transitions": self.transitions,
            "start_state": self.start_state,
            "final_states": list(self.final_states)
        }

    def get_transition(self, state, symbol):
        """Get the next state for a given state and input symbol."""
        if state in self.transitions and symbol in self.transitions[state]:
            return self.transitions[state][symbol]
        return None

    def test_string(self, test_str):
        """Test if a string is accepted by the DFA. Returns (accepted, final_state, steps)."""
        state = self.start_state
        steps = [(state, None)]  # (state, symbol_consumed)
        
        for char in test_str:
            next_state = self.get_transition(state, char)
            if next_state is None:
                return False, state, steps  # Stuck - no valid transition
            state = next_state
            steps.append((state, char))
        
        return state in self.final_states, state, steps

    def minimize(self):
        """Minimize the DFA using table-filling algorithm. Returns a new minimized DFA."""
        # Step 1: Remove unreachable states
        reachable = set()
        queue = [self.start_state]
        while queue:
            state = queue.pop(0)
            if state in reachable:
                continue
            reachable.add(state)
            if state in self.transitions:
                for symbol in self.transitions[state]:
                    next_state = self.transitions[state][symbol]
                    if next_state not in reachable:
                        queue.append(next_state)

        states = reachable
        final_states = self.final_states & reachable
        transitions = {s: t for s, t in self.transitions.items() if s in reachable}

        # Step 2: Table-filling algorithm for equivalent states
        distinguishable = set()
        for s1 in states:
            for s2 in states:
                if s1 < s2:
                    if (s1 in final_states) != (s2 in final_states):
                        distinguishable.add((s1, s2))

        changed = True
        while changed:
            changed = False
            for s1 in states:
                for s2 in states:
                    if s1 < s2 and (s1, s2) not in distinguishable:
                        for symbol in self.alphabet:
                            t1 = transitions.get(s1, {}).get(symbol)
                            t2 = transitions.get(s2, {}).get(symbol)
                            if t1 and t2:
                                pair = (min(t1, t2), max(t1, t2))
                                if pair in distinguishable:
                                    distinguishable.add((s1, s2))
                                    changed = True
                                    break

        # Find equivalent state groups
        equivalent_groups = {}
        state_to_group = {}
        for state in sorted(states):
            found_group = None
            for rep in equivalent_groups:
                pair = (min(state, rep), max(state, rep))
                if pair not in distinguishable:
                    found_group = rep
                    break
            if found_group:
                equivalent_groups[found_group].append(state)
                state_to_group[state] = found_group
            else:
                equivalent_groups[state] = [state]
                state_to_group[state] = state

        # Build minimized DFA
        new_states = list(equivalent_groups.keys())
        new_transitions = {}
        for rep in new_states:
            new_transitions[rep] = {}
            old_state = equivalent_groups[rep][0]
            if old_state in transitions:
                for symbol, target in transitions[old_state].items():
                    new_transitions[rep][symbol] = state_to_group.get(target, target)

        new_final = [s for s in new_states if s in final_states]
        new_start = state_to_group.get(self.start_state, self.start_state)

        return DFA(new_states, self.alphabet, new_transitions, new_start, new_final)


SAMPLE_DFA_DATA = {
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
