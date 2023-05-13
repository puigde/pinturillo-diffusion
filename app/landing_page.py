import streamlit as st
from ui_utils import show_centered_title, drawing_page_callback, pre_guessing_page_callback
from image_utils import img_to_html


def landing_page():
    st.session_state.current_game_id = None
    st.session_state.current_page = "Landing"
    show_centered_title("Pinturillo Diffusion", show_logo=False)
    st.markdown(f"<h1 style='text-align: center; color: grey;'>{img_to_html('logo.png')}</h1>",
                unsafe_allow_html=True)
    _, c_username, _ = st.columns([1.25, 2, 1])
    with c_username:
        st.session_state.player_name = st.text_input("Enter your name")
    cs = st.columns([2.5, 1, 1, 1.5])
    with cs[1]:
        a = st.button("Drawing", on_click=drawing_page_callback)
    with cs[2]:
        b = st.button("Guessing", on_click=pre_guessing_page_callback)
    if (a or b):
        _, c_usernamecp, _ = st.columns([1.25, 2, 1])
        with c_usernamecp:
            if st.session_state.player_name == "":
                st.warning("Please enter your username")
            elif " " in st.session_state.player_name:
                st.warning("Username cannot contain spaces")
