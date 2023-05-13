import streamlit as st
from ui_utils import show_centered_title, drawing_page_callback, guessing_page_callback
from image_utils import img_to_html


def landing_page():
    st.session_state.current_page = "Landing"
    show_centered_title("Pinturillo Diffusion")
    st.markdown(f"<h1 style='text-align: center; color: grey;'>{img_to_html('logo.png')}</h1>",
                unsafe_allow_html=True)
    c0, c1 = st.columns(2)
    with c0:
        st.button("Drawing", on_click=drawing_page_callback)
    with c1:
        st.button("Guessing", on_click=guessing_page_callback)
