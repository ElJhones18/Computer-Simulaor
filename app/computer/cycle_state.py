from enum import Enum


class CycleState(Enum):
    FETCH = "FETCH"
    DECODE = "DECODE"
    EXECUTE = "EXECUTE"
    STORE = "STORE"

    @classmethod
    def next_state(cls, current_state):
        states = list(cls)
        current_index = states.index(current_state)
        next_index = (current_index + 1) % len(states)
        return states[next_index]