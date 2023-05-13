import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import yaml
import banana_dev as banana
from PIL import Image
import base64
from io import BytesIO
import replicate


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
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []


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
        out = run_model(canvas_result.image_data,
                        model_provider=MODEL_PROVIDER)
        process_model_outputs(out)


def run_model(image_data, model_provider="replicate"):
    """Runs the model on the painted image."""
    model_inputs = get_model_inputs(image_data, model_provider=model_provider)
    if model_provider == "banana":
        out = banana.run(KEYS["banana-api"],
                         KEYS["banana-model"], model_inputs)
    elif model_provider == "replicate":
        out = replicate.run(
            KEYS["replicate-model"],
            input=model_inputs,
        )
    return out


def process_model_outputs(out, model_provider="replicate"):
    """Adds generated images to session state. Displays images."""
    if model_provider == "banana":
        image = base64.b64decode(out["modelOutputs"][0]["image_base64"])
        st.session_state.generated_images.append(image)
    elif model_provider == "replicate":
        for image in out:
            st.session_state.generated_images.append(image)
    for image in st.session_state.generated_images:
        try:
            st.image(image, width=500)
        except:
            print(image)
            st.image(Image.open(BytesIO(image)))


def get_model_inputs(image_data, model_provider="replicate"):
    """Gets a json serializable object of model inputs. Key components are prompt and image."""
    assert model_provider in ["banana", "replicate"]
    if model_provider == "banana":
        image_file = prepare_input_image(image_data)
        model_inputs = {
            "prompt": "rihanna best quality, extremely detailed",
            "negative_prompt": "monochrome, lowres, bad anatomy, worst quality, low quality",
            "num_inference_steps": 20,
            "image_data":  image_file,
        }
    elif model_provider == "replicate":
        image_file = prepare_input_image(image_data)
        model_inputs = {
            "prompt": "rihanna best quality, extremely detailed",
            "structure": "scribble",
            "image":  image_file,
        }
    return model_inputs


def prepare_input_image(image_data):
    """Prepares the image data for the model."""
    image_file = BytesIO()
    Image.fromarray(image_data.astype("uint8"), mode="RGBA").save(
        image_file, format="PNG")
    image_file.seek(0)
    return image_file


def read_api_keys():
    """Reads the api keys from the api_keys.yaml file."""
    global KEYS
    with open("api_keys.yaml", "r") as f:
        KEYS = yaml.load(f, Loader=yaml.FullLoader)


def define_provider():
    """Defines the model provider. Current version is validated on replicate."""
    global MODEL_PROVIDER
    default_provider = "replicate"
    MODEL_PROVIDER = default_provider


if __name__ == "__main__":
    read_api_keys()
    define_provider()
    initialize_session_state()
    main()
