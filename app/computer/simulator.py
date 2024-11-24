from computer.memory.memory import Memory
from computer.assembly.parser import Parser
from computer.cpu.psw import PSW
from computer.computer_state import ComputerState
import streamlit as st


class Simulator:

    def __init__(self) -> None:
        self.parser = Parser()

    def simulation(self):
        self.initialize_state()

    def step(self):
        computer: ComputerState = st.session_state.computer_state
        computer.psw.zero = not computer.psw.zero

        computer.user_registers.R1 = "buenisima"
        self.update_computer_state(computer)

    """
    input/output
    """

    def load_program(self, program: str):
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
