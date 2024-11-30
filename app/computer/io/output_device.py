import streamlit as st


def display_output_device():
    st.markdown("### Dispositivo de salida")
    data = int(st.session_state.computer_state.data_memory.get_all()[-1][1], 2)
    address = len(st.session_state.computer_state.data_memory.get_all()) - 1
    # memory_addres =
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
                        >> {data}
                    </div>
                    """,
        unsafe_allow_html=True,
    )
    st.write(
        f"La salida está conectada a la ultima dirección de la memoria de datos. Escriba en la dirección **#{address}** para ver el resultado."
    )
