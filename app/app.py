import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import yaml
import banana_dev as banana
from PIL import Image
import base64
from io import BytesIO


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
    run = st.button("Run")
    if run:
        run_model(canvas_result.image_data)


def run_model(image_data):
    model_inputs = get_model_inputs(image_data)
    out = banana.run(keys["banana-api"], keys["banana-model"], model_inputs)
    canny_image = base64.b64decode(out["modelOutputs"][0]["canny_base64"])
    st.image(Image.open(BytesIO(canny_image)))
    image = base64.b64decode(out["modelOutputs"][0]["image_base64"])
    st.image(Image.open(BytesIO(image)))


def get_model_inputs(image_data):
    model_inputs = {
        "prompt": "rihanna best quality, extremely detailed",
        "negative_prompt": "monochrome, lowres, bad anatomy, worst quality, low quality",
        "num_inference_steps": 20,
        "image_data":  png_export(image_data),
    }
    return model_inputs


def png_export(img_data):
    im = Image.fromarray(img_data.astype("uint8"), mode="RGBA")
    # im.save(file_path, "PNG")

    buffered = BytesIO()
    im.save(buffered, format="PNG")
    img_data = buffered.getvalue()
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(img_data.encode()).decode()
    except AttributeError:
        b64 = base64.b64encode(img_data).decode()
    return b64


def read_api_keys():
    global keys
    with open("api_keys.yaml", "r") as f:
        keys = yaml.load(f, Loader=yaml.FullLoader)


if __name__ == "__main__":
    read_api_keys()
    initialize_session_state()
    main()
