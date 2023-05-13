import banana_dev as banana
import replicate
from PIL import Image
import base64
from io import BytesIO
import streamlit as st
from image_utils import prepare_input_image
import requests


def run_model(image_data, model_provider="replicate"):
    """Runs the model on the painted image."""
    model_inputs = get_model_inputs(image_data, model_provider=model_provider)
    if model_provider == "banana":
        out = banana.run(st.session_state.api_keys["banana-api"],
                         st.session_state.api_keys["banana-model"], model_inputs)
    elif model_provider == "replicate":
        out = replicate.run(
            st.session_state.api_keys["replicate-model"],
            input=model_inputs,
        )
    return out


def process_model_outputs(out, model_provider="replicate"):
    """Adds generated images to session state. Displays images."""
    if model_provider == "banana":
        image = base64.b64decode(out["modelOutputs"][0]["image_base64"])
        st.session_state.generated_images.append(image)
    elif model_provider == "replicate" or model_provider is None:
        for image in out:
            st.session_state.generated_images.append(image)
    for image in st.session_state.generated_images:
        try:
            st.image(image, width=500)
        except:
            st.image(Image.open(BytesIO(image)))
    if st.session_state.current_game_id is not None:
        with open(f"game_{st.session_state.current_game_id}/last_image.png", "wb") as f:
            last_image = st.session_state.generated_images[-1]
            if isinstance(last_image, str):
                if last_image.startswith("http"):
                    response = requests.get(last_image)
                    response.raise_for_status()
                    image_bytes = response.content
                else:
                    image_bytes = last_image.encode()
                with Image.open(BytesIO(image_bytes)) as img:
                    img.save(
                        f"game_{st.session_state.current_game_id}/last_image.png")
            else:
                last_image.save(
                    f"game_{st.session_state.current_game_id}/last_image.png")


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
