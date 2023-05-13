import streamlit as st
from ui_utils import show_centered_title, exit_button
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
from model_utils import run_model, process_model_outputs


def drawing_page():
    st.session_state.current_page = "Drawing"
    show_centered_title("Drawing")
    drawing_component()
    exit_button()


def drawing_component():
    """The main drawing component."""
    c0, c1 = st.columns(2)
    with c0:
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=st.session_state.stroke_width,
            stroke_color=st.session_state.stroke_color,
            background_color=st.session_state.background_color,
            background_image=None,
            update_streamlit=True,
            height=500,
            width=600,
            drawing_mode="freedraw",
            point_display_radius=0,
            display_toolbar=True,
            key="full_app",
        )
        c01, c02, c03 = st.columns(3)
        # TODO: make this components refresh after modification using callbacks
        with c01:
            st.session_state.stroke_width = st.slider("Stroke width: ", 1, 25,
                                                      st.session_state.stroke_width)
        with c02:
            st.session_state.stroke_color = st.color_picker(
                "Stroke color hex: ", value=st.session_state.stroke_color)

        with c03:
            st.session_state.background_color = st.color_picker(
                "Background color hex: ", value=st.session_state.background_color)
        run = st.button("Run")
    with c1:
        if run:
            if st.session_state.model_provider is None:
                out = [Image.open("sample_image.png")]

            else:
                out = run_model(canvas_result.image_data,
                                model_provider=st.session_state.model_provider)
            process_model_outputs(out)
