import streamlit as st
import yaml
from landing_page import landing_page
from drawing_page import drawing_page
from guessing_page import pre_guessing_page, guessing_page
from postgame_page import postgame_page


def main():
    pages = {
        "Landing": landing_page,
        "Drawing": drawing_page,
        "Pre_guessing": pre_guessing_page,
        "Guessing": guessing_page,
        "Postgame": postgame_page,
    }
    pages[st.session_state.current_page]()


def initialize_session_state():
    if "stroke_width" not in st.session_state:
        st.session_state.stroke_width = 3
    if "stroke_color" not in st.session_state:
        st.session_state.stroke_color = "#000000"
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Landing"
    if "current_game_id" not in st.session_state:
        st.session_state.current_game_id = None
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""


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


def init_streamlit_page():
    st.set_page_config(page_icon="logo.png",
                       page_title="Pinturillo Diffusion", layout="wide")
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .block-container { padding-top: 1rem; padding-bottom: 0rem; padding-left: 5rem; padding-right: 5rem; }
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if __name__ == "__main__":
    init_streamlit_page()
    read_api_keys()
    define_provider()
    initialize_session_state()
    main()
