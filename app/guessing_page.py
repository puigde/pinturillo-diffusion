import streamlit as st
from ui_utils import show_centered_title, exit_button


def guessing_page():
    st.session_state.current_page = "Guessing"
    show_centered_title("Guessing")
    exit_button()
