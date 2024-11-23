import streamlit as st
from .components import (
    cpu_value_container,
    psw_container,
    alu_container,
    memory_table,
)
from .styles import apply_global_styles


class UserInterface:
    def __init__(self) -> None:
        pass

    def render(self) -> None:
        st.set_page_config(layout="wide")
        apply_global_styles()  # Estilos globales

        # Contenedor principal
        with st.container():
            col1, col2, col3 = st.columns([1.5, 1, 1.5])

            # Columna izquierda (CPU y registros)
            with col1:
                self.display_cpu()

            # Columna central (Buses)
            with col2:
                self.display_system_buses()

                self.display_input_device()

            # Columna derecha (Memoria)
            with col3:
                self.display_memory()
                self.display_output_device()

    def display_memory(self):
        st.markdown("### Memoria")
        data_memory = [("0x0000", "0x1234"), ("0x0001", "0x5678")]
        program_memory = [("0x0000", "LOAD"), ("0x0001", "ADD")]
        memory_table("Memoria de Datos", data_memory)
        memory_table("Memoria de Programa", program_memory)

    def display_system_buses(self):
        st.markdown("### Bus del sistema")
        # Contenedores para los buses
        for bus_type in [
            "Bus de control",
            "Bus de direcciones",
            "Bus de datos",
        ]:
            st.markdown(
                f"""
                        <div style="
                            border: 2px solid #00FFFF;
                            padding: 10px;
                            margin: 16px 0;
                            border-radius: 5px;
                            color: white;
                            text-shadow: 0 0 5px #00FFFF;
                            box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
                        ">
                            {bus_type}
                        </div>
                        """,
                unsafe_allow_html=True,
            )

    def display_cpu(self):
        st.markdown("### CPU")

        # Primera fila de la columna izquierda
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            cpu_value_container("PC", "0x0000")
        with subcol2:
            cpu_value_container("UC", "FETCH")

        # Segunda fila
        subcol3, subcol4 = st.columns(2)
        with subcol3:
            cpu_value_container("IR", "0x0000")
        with subcol4:
            cpu_value_container("MAR", "0x0000")

        # Tercera fila
        subcol5, subcol6 = st.columns(2)
        with subcol5:
            psw_container(True, False, True)
        with subcol6:
            cpu_value_container("MBR", "0x0000")

        # Cuarta fila
        subcol7, subcol8 = st.columns(2)
        with subcol7:
            # alu_container("R1 + R2", "0x00FF")  # Ejemplo con suma de R1 y R2
            alu_container("R1", "R2", "AND", "FALSE")

        with subcol8:
            # Registros de usuario
            registers_data = [
                ("AL", "0x0000"),
                ("BL", "0x0000"),
                ("CL", "0x0000"),
                ("DL", "0x0000"),
            ]
            memory_table("Registros de Usuario", registers_data)

    def display_input_device(self):
        st.markdown("### Dispositivo de entrada")
        st.text_area(label="", placeholder="Escriba su programa aquí...", height=200)

    def display_output_device(self):
        st.markdown("### Dispositivo de salida")
        st.markdown(
            f"""
                        <div style="
                            border: 2px solid #00FFFF;
                            padding: 10px;
                            margin: 16px 0;
                            border-radius: 5px;
                            color: white;
                            text-shadow: 0 0 5px #00FFFF;
                            box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
                        ">
                            {">>"} Salida
                        </div>
                        """,
            unsafe_allow_html=True,
        )
