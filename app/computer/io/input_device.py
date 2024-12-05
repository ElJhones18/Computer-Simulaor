import streamlit as st
from streamlit_ace import st_ace

from computer.simulator import Simulator


def display_input_device(simulator: Simulator):
    st.markdown("### Dispositivo de entrada")
    program_input = st_ace(
        language="assembly_x86", theme="monokai", height=160, auto_update=True
    )

    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        if st.button(
            "Cargar",
            disabled=st.session_state.computer_state.cycle.value != "WAITING",
        ):
            with col2:
                try:
                    simulator.load_program(program_input)
                    st.success("Programa cargado correctamente")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
