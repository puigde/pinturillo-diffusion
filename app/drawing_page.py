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
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=st.session_state.stroke_width,
        stroke_color=st.session_state.stroke_color,
        background_color=st.session_state.background_color,
        background_image=None,
        update_streamlit=True,
        height=500,
        width=2000,
        drawing_mode="freedraw",
        point_display_radius=0,
        display_toolbar=True,
        key="full_app",
    )

    # NOTE: updating the params here refreshes post interaction with canvas
    st.session_state.stroke_width = st.slider("Stroke width: ", 1, 25,
                                              st.session_state.stroke_width)
    st.session_state.stroke_color = st.color_picker(
        "Stroke color hex: ", value=st.session_state.stroke_color)
    st.session_state.background_color = st.color_picker(
        "Background color hex: ", value=st.session_state.background_color)

    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data)
    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.select_dtypes(include=["object"]).columns:
            objects[col] = objects[col].astype("str")
        st.dataframe(objects)
    run = st.button("Run")
    if run:
        if st.session_state.model_provider is None:
            out = [Image.open("sample_image.png")]

        else:
            out = run_model(canvas_result.image_data,
                            model_provider=st.session_state.model_provider)
        process_model_outputs(out)
