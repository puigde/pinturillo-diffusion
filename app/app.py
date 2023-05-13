import streamlit as st
import yaml
from landing_page import landing_page
from drawing_page import drawing_page
from guessing_page import guessing_page


def main():
    st.set_page_config(page_icon="logo.png",
                       page_title="Pinturillo Diffusion", layout="wide")
    pages = {
        "Landing": landing_page,
        "Drawing": drawing_page,
        "Guessing": guessing_page,
    }
    pages[st.session_state.current_page]()


def initialize_session_state():
    if "stroke_width" not in st.session_state:
        st.session_state.stroke_width = 3
    if "stroke_color" not in st.session_state:
        st.session_state.stroke_color = "#000000"
    if "background_color" not in st.session_state:
        st.session_state.background_color = "#ffffff"
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Landing"


def read_api_keys():
    """Reads the api keys from the api_keys.yaml file."""
    with open("api_keys.yaml", "r") as f:
        api_keys = yaml.load(f, Loader=yaml.FullLoader)
    st.session_state.api_keys = api_keys


def define_provider():
    """Defines the model provider. Current version is validated on replicate."""
    default_provider = "replicate"
    model_provider = default_provider
    # model_provider = None  # avoid replicate calls in test mode and display saved image
    st.session_state.model_provider = model_provider


if __name__ == "__main__":
    read_api_keys()
    define_provider()
    initialize_session_state()
    main()
