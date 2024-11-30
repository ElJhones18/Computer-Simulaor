import streamlit as st


# Contenedor para valores de CPU
def cpu_value_container(label, value):
    base_style = """
        border: 2px solid #FF00FF;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
    """
    content = f"""
        <div style="{base_style}">
            <div style="color: white; font-size: 0.8em; text-shadow: 0 0 5px #fff;">{label}</div>
            <div style="color: white; font-size: 1.2em; font-family: monospace; text-shadow: 0 0 5px #fff;">{value}</div>
        </div>
    """
    st.markdown(content, unsafe_allow_html=True)


# Contenedor para el PSW
def psw_container(zero_flag, negative_flag, overflow_flag, interrupt_flag):
    flags_info = f"""
        Z:{'✓' if zero_flag else '✗'} |
        N:{'✓' if negative_flag else '✗'} |
        O:{'✓' if overflow_flag else '✗'} |
        I:{'✓' if interrupt_flag else '✗'}
    """
    cpu_value_container("PSW", flags_info)


# Contenedor para la ALU
def alu_container(operator1, operator2, operation, result):
    # operation = f"{operator1} {operation} {operator2}"
    base_style = """
        border: 2px solid #FF00FF;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
    """
    content = f"""
        <div style="{base_style}">
            <div style="color: white; font-size: 0.8em; text-shadow: 0 0 5px #fff;">ALU</div>
            <div style="color: white; font-size: 0.9em; font-family: monospace; margin-top: 5px;">{operator1} {operation} {operator2}</div>
            <div style="color: white; font-size: 1.2em; font-family: monospace; text-shadow: 0 0 5px #fff; margin-top: 5px;">{result}</div>
        </div>
    """
    st.markdown(content, unsafe_allow_html=True)


# Tabla genérica para memoria o registros
def memory_table(title, data):
    rows = "".join(
        [
            f'<tr><td style="padding: 5px; text-align: center; width:30%;">{addr}</td>'
            f'<td style="padding: 5px; text-align: center; width:70%;">{value}</td></tr>'
            for addr, value in data
        ]
    )
    table_style = """
        border: 2px solid #FF00FF;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    """
    content = f"""
        <div style="{table_style}">
            <h4 style="margin-bottom: 10px;">{title}</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tbody>{rows}</tbody>
            </table>
        </div>
    """
    st.markdown(content, unsafe_allow_html=True)


def display_bus(label, value):
    content = f"""
            <div style="
            border: 2px solid #00FFFF;
            padding: 10px;
            margin: 16px 0;
            border-radius: 5px;
            color: white;
            text-shadow: 0 0 5px #00FFFF;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
            ">
            {label}: {value}
            </div>
        """
    st.markdown(content, unsafe_allow_html=True)
