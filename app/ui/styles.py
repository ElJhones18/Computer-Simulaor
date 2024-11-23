import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
        }
        h3 {
            color: white;
            text-shadow: 0 0 5px #00FFFF;
        }
        #MainMenu, footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
