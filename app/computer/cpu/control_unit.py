from computer.computer_state import ComputerState
from computer.cycle_state import CycleState
import streamlit as st


class ControlUnit:
    def __init__(self):
        self.fetch_signal: str = "1"
        self.write_signal: str = "0"

    def instruction_cycle(self, computer_state: ComputerState):
        if computer_state.cycle == CycleState.FETCH_INS:
            self.fetch_instruction(computer_state)
        elif computer_state.cycle == CycleState.DECODE:
            self.decode(computer_state)
        return computer_state

    def fetch_instruction(self, computer_state: ComputerState):
        match computer_state.actual_micro_operation:
            case 0:
                computer_state.system_registers.mar = computer_state.system_registers.pc
                computer_state.actual_micro_operation += 1
            case 1:
                # st.session_state.computer_state.system_bus.control_bus = self.fetch_signal
                computer_state.system_bus.control_bus = self.fetch_signal
                computer_state.actual_micro_operation += 1
            case 2:
                computer_state.system_bus.address_bus = (
                    computer_state.system_registers.mar
                )
                computer_state.actual_micro_operation += 1
            case 3:
                computer_state.system_bus.data_bus = computer_state.program_memory.read(
                    computer_state.system_registers.mar
                )
                computer_state.actual_micro_operation += 1
            case 4:
                computer_state.system_registers.mbr = computer_state.system_bus.data_bus
                computer_state.actual_micro_operation += 1
            case 5:
                computer_state.system_registers.ir = computer_state.system_registers.mbr
                computer_state.actual_micro_operation += 1
                computer_state.actual_micro_operation = 0
                computer_state.cycle = CycleState.DECODE

    def decode(self, computer_state: ComputerState):
        computer_state.user_registers.R1 = "xd"
