import streamlit as st
from ui_utils import show_centered_title, exit_button
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from model_utils import run_model, process_model_outputs
import random
import os
import yaml
from ui_utils import display_generated_images


def drawing_page():
    st.session_state.current_page = "Drawing"
    if st.session_state.current_game_id is None:
        create_game()
    show_centered_title(f"Drawing on game {st.session_state.current_game_id}: {st.session_state.word.upper()}")
    drawing_component()
    exit_button()


def create_game():
    """A game is defined by a random four digit game id. Each game has a directory in the server"""
    game_id = random.randint(1000, 9999)
    st.session_state.current_game_id = game_id
    if not os.path.exists(f"game_{game_id}"):
        os.makedirs(f"game_{game_id}")
    
    with open("games.yaml") as f:
        themes = yaml.load(f, Loader=yaml.FullLoader)

    # Select a random country
    random_country = random.choice(themes)
    # country_name = list(random_country.keys())[0]

    # Select a random word from that country
    random_word = random.choice(random_country[list(random_country.keys())[0]])

    st.session_state.word, st.session_state.prompt = random_word['word'], random_word['prompt']
    with open(f"game_{game_id}/word.txt", "a") as f:
        f.write(st.session_state.word + "\n")

    with open(f"game_{game_id}/players.txt", "a") as f:
        f.write(st.session_state.player_name + "\n")


def drawing_component():
    """The main drawing component."""
    c0, c1 = st.columns(2)
    with c0:
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=st.session_state.stroke_width,
            stroke_color=st.session_state.stroke_color,
            background_color="#ffffff",
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
        with c01:
            stroke_width = st.slider("Stroke width: ", 1, 25,
                                     key="stroke_width")
        with c02:
            stroke_color = st.color_picker(
                "Stroke color hex: ", key="stroke_color")
        with c03:
            run = st.button(
                "Run model", type="primary")

    with c1:
        if run:
            if st.session_state.model_provider is None:
                out = [Image.open("sample_image.png")]

            else:
                out = run_model(canvas_result.image_data,
                                st.session_state.prompt,
                                model_provider=st.session_state.model_provider,
                                )
            process_model_outputs(out)
        else:
            display_generated_images()
