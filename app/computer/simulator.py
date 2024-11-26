import time
from computer.cpu.control_unit import ControlUnit
from computer.memory.memory import Memory
from computer.assembly.parser import Parser
from computer.cpu.psw import PSW
from computer.computer_state import ComputerState
from computer.cycle_state import CycleState
import streamlit as st


class Simulator:

    def __init__(self) -> None:
        self.parser = Parser()
        self.uc = ControlUnit()

    def simulation(self):
        self.initialize_state()

    def step(self):
        computer_state: ComputerState = st.session_state.computer_state
        self.uc.instruction_cycle(computer_state)

    """
    input/output
    """

    def load_program(self, program: str):
        
        st.session_state.computer_state.data_memory.write("0011", "1100000000000011")
        """Carga un programa en memoria"""
        binary_instructions = self.parser.parse_program(program)

        # for i, inst in enumerate(binary_instructions):
        #     print(f"Instrucción {i} codificada: {inst}")
        #     # Decodificar para verificar
        #     print(f"Instrucción {i} decodificada: {self.parser.decode_instruction(inst)}\n")

        memory: Memory = st.session_state.computer_state.program_memory
        for i, binary in enumerate(binary_instructions):
            address = memory.memory[i][0]
            memory.write(address, binary)
        st.session_state.computer_state.cycle = CycleState.FETCH_INS

    """
    Simulator states
    """

    def initialize_state(self):
        """Inicializa el estado si no existe"""
        if "computer_state" not in st.session_state:
            computer_state = ComputerState()
            st.session_state.computer_state = computer_state

    def update_computer_state(self, computer_state: ComputerState):
        """Actualiza un componente específico del estado"""
        setattr(st.session_state, "compuder_state", computer_state)

    def restart(self):
        """Reinicia la simulación"""
        st.session_state.computer_state = ComputerState()
