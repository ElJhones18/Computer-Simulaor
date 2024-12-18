import streamlit as st
from streamlit_ace import st_ace
from .components import (
    cpu_value_container,
    display_bus,
    psw_container,
    alu_container,
    memory_table,
)
from .styles import apply_global_styles
from computer.simulator import Simulator
from computer.io.input_device import display_input_device
from computer.io.output_device import display_output_device


class UserInterface:
    def __init__(self) -> None:
        self.simulator = Simulator()

    def render(self) -> None:

        self.simulator.simulation()

        st.set_page_config(layout="wide")
        apply_global_styles()  # Estilos globales

        # Contenedor principal
        with st.container():
            col1, col2, col3 = st.columns([1.8, 1.5, 2])

            # Columna izquierda (CPU y registros)
            with col1:
                self.display_cpu()

            # Columna central (Buses)
            with col2:
                self.display_system_buses()
                self.display_input_device()

            # Columna derecha (Memoria)
            with col3:
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    self.display_data_memory()
                with subcol2:
                    self.display_program_memory()
                # _, subcol, _ = st.columns([1, 20, 1])
                # with subcol:
                #     pass

            col4, col5, col6 = st.columns([1.8, 1.5, 2])
            with col4:
                self.display_simulation_controls(self.simulator)
            with col5:
                self.display_output_device()
            with col6:
                self.simulation_info()

    """Simulation components"""

    def simulation_info(self):
        st.markdown("### Información del simulador")
        # st.write(f" **Señal de control 1** = *Pedir a memoria*")
        # st.write(f" **Señal de control 0** = *Escribir en memoria*")
        st.write(
            "El simulador solo soporta ingreso de números enteros positivos de hasta 4 bits de manera inmediata. Internamente se pueden manejar números de hasta 16 bits."
        )
        st.write("La ALU devuelve cero si el resultado es negativo.")
        st.write(
            "Si ocurre sobreflujo o division por cero, el programa cargado terminará su ejecución."
        )

    def display_simulation_controls(self, simulator: Simulator):
        st.write("### Controles de la simulación")
        col_controls = st.columns([1, 1])

        with col_controls[0]:
            if st.button(
                "Paso",
                disabled=st.session_state.computer_state.cycle.value == "WAITING",
            ):
                simulator.step()
                st.rerun()

        with col_controls[1]:
            if st.button("Reset"):
                simulator.restart()
                st.rerun()

        size = len(st.session_state.computer_state.program_memory.get_all()) - 1
        actual_line = int(st.session_state.computer_state.system_registers.pc, 2) - size
        if st.session_state.computer_state.cycle.value == "WAITING":
            actual_line = ""
        st.write(f"##### **Línea actual** >>  *{actual_line}*")
        st.write(
            f"##### **Instrucción decodificada** >>  *{st.session_state.computer_state.actual_insstruction}*"
        )

    """Computer components"""

    def display_data_memory(self):
        st.markdown("### Memoria")
        memory_table(
            "Memoria de Datos", st.session_state.computer_state.data_memory.get_all()
        )

    def display_program_memory(self):
        st.markdown("### ")
        memory_table(
            "Memoria de Programa",
            st.session_state.computer_state.program_memory.get_all(),
        )

    def display_system_buses(self):
        st.markdown("### Bus del sistema")
        # Contenedores para los buses
        display_bus(
            "Bus de control", st.session_state.computer_state.system_bus.control_bus
        )
        display_bus(
            "Bus de direcciones", st.session_state.computer_state.system_bus.address_bus
        )
        display_bus("Bus de datos", st.session_state.computer_state.system_bus.data_bus)

    def display_cpu(self):
        st.markdown("### CPU")

        # Primera fila de la columna izquierda
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            cpu_value_container(
                "PC", st.session_state.computer_state.system_registers.pc
            )
        with subcol2:
            cpu_value_container("UC", st.session_state.computer_state.cycle.value)

        # Segunda fila
        subcol3, subcol4 = st.columns(2)
        with subcol3:
            cpu_value_container(
                "IR", st.session_state.computer_state.system_registers.ir
            )
        with subcol4:
            cpu_value_container(
                "MAR", st.session_state.computer_state.system_registers.mar
            )

        # Tercera fila
        subcol5, subcol6 = st.columns(2)
        with subcol5:
            psw_container(
                st.session_state.computer_state.psw.zero,
                st.session_state.computer_state.psw.negative,
                st.session_state.computer_state.psw.overflow,
                st.session_state.computer_state.psw.interrupt,
            )
        with subcol6:
            cpu_value_container(
                "MBR", st.session_state.computer_state.system_registers.mbr
            )

        # Cuarta fila
        subcol7, subcol8 = st.columns(2)
        with subcol7:
            alu_container(
                st.session_state.computer_state.alu.operator1,
                st.session_state.computer_state.alu.operator2,
                st.session_state.computer_state.alu.operation,
                st.session_state.computer_state.alu.result,
            )

        with subcol8:
            registers_data = [
                ("R1", st.session_state.computer_state.user_registers.R1),
                ("R2", st.session_state.computer_state.user_registers.R2),
                ("R3", st.session_state.computer_state.user_registers.R3),
                ("R4", st.session_state.computer_state.user_registers.R4),
            ]
            memory_table("Registros de Usuario", registers_data)

    """I/O devices"""

    def display_input_device(self):
        display_input_device(self.simulator)

    def display_output_device(self):
        display_output_device()
