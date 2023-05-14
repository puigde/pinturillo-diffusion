from pathlib import Path
import base64
from PIL import Image
from io import BytesIO
import streamlit as st


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path, height=400):
    img_html = f"<img height='{height}' src='data:image/png;base64,{{}}' class='img-fluid'>".format(
        img_to_bytes(img_path)
    )
    return img_html


def prepare_input_image(image_data):
    """Prepares the image data for the model."""
    image_file = BytesIO()
    Image.fromarray(image_data.astype("uint8"), mode="RGBA").save(
        image_file, format="PNG")
    image_file.seek(0)
    return image_file
