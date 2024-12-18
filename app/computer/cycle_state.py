from enum import Enum


class CycleState(Enum):
    WAITING = "WAITING"
    FETCH_INS = "FETCH INSTRUCTION"
    DECODE = "DECODE"
    FETCH_OP = "FETCH OPERAND"
    EXECUTE = "EXECUTE"
    WRITE = "WRITE"

    @classmethod
    def next_state(cls, current_state):
        states = list(cls)
        current_index = states.index(current_state)
        next_index = (current_index + 1) % len(states)
        return states[next_index]