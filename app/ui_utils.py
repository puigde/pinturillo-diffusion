import streamlit as st


def exit_button():
    st.button("Exit", on_click=exit_button_callback)


def exit_button_callback():
    st.session_state.current_page = "Landing"
    st.session_state.generated_images = []


def drawing_page_callback():
    st.session_state.current_page = "Drawing"
    st.session_state.generated_images = []


def pre_guessing_page_callback():
    st.session_state.current_page = "Pre_guessing"
    st.session_state.generated_images = []


def access_guessing_callback(game_id):
    st.session_state.current_game_id = game_id
    st.session_state.current_page = "Guessing"
    st.session_state.generated_images = []


def show_centered_title(title):
    st.markdown(f"<h1 style='text-align: center; color: black;'>{title}</h1>",
                unsafe_allow_html=True)
