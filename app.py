import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd


def main():
    st.title("Pinturillo Diffusion")
    drawing_component()


def initialize_session_state():
    if "stroke_width" not in st.session_state:
        st.session_state.stroke_width = 3
    if "stroke_color" not in st.session_state:
        st.session_state.stroke_color = "#000000"
    if "background_color" not in st.session_state:
        st.session_state.background_color = "#ffffff"


def drawing_component():
    # Create a canvas component
    canvas_result = st_canvas(
        # Fixed fill color with some opacity
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


if __name__ == "__main__":
    initialize_session_state()
    main()
