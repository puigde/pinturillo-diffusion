import streamlit as st
from image_utils import img_to_html
import os
from PIL import Image
from io import BytesIO
import json


def exit_button():
    st.button("Exit", on_click=exit_button_callback)


def exit_button_callback():
    st.session_state.current_page = "Landing"
    st.session_state.generated_images = []


def drawing_page_callback():
    if st.session_state.player_name == "" or " " in st.session_state.player_name:
        return
    st.session_state.current_page = "Drawing"
    st.session_state.generated_images = []


def pre_guessing_page_callback():
    if st.session_state.player_name == "" or " " in st.session_state.player_name:
        return
    st.session_state.current_page = "Pre_guessing"
    st.session_state.generated_images = []


def postgame_page_callback():
    if st.session_state.player_name == "" or " " in st.session_state.player_name:
        return
    st.session_state.current_page = "Postgame"
    st.session_state.generated_images = []


def winner_update_game_state():
    st.session_state.mask_count = 0
    # Loads the game state
    with open(f"game_{st.session_state.current_game_id}/game_state.json", "r") as f:
        game_state = json.load(f)
    game_state["status"] = "finished"
    game_state["winner"] = st.session_state.player_name
    # Saves the game state
    with open(f"game_{st.session_state.current_game_id}/game_state.json", "w") as f:
        json.dump(game_state, f)


def check_game_state(postgame_status="loading_next"):
    with open(f"game_{st.session_state.current_game_id}/game_state.json", "r") as f:
        game_state = json.load(f)
    if game_state["status"] == postgame_status:
        # postgame_page_callback()
        if st.session_state.player_name == "" or " " in st.session_state.player_name:
            return
        st.session_state.current_page = "Postgame"
        st.session_state.generated_images = []


def access_guessing_callback(game_id):
    # register the current user as players in the game txt file if not already otherise return
    if os.path.exists(f"game_{game_id}"):
        with open(f"game_{game_id}/players.txt", "r") as f:
            players = f.read().split("\n")
        if st.session_state.player_name in players:
            return
        else:
            with open(f"game_{game_id}/players.txt", "a") as f:
                f.write(f"{st.session_state.player_name}\n")
    st.session_state.current_game_id = game_id
    st.session_state.current_page = "Guessing"
    st.session_state.generated_images = []


def show_centered_title(title, show_logo=True):
    if show_logo:
        st.markdown(f"<h1 style='text-align: center; color: black;'>{img_to_html('logo.png', height=40)} {title}</h1>",
                    unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='text-align: center; color: black;'>{title}</h1>",
                    unsafe_allow_html=True)


def display_generated_images():
    for image in reversed(st.session_state.generated_images):
        try:
            st.image(image, width=500)
        except:
            st.image(Image.open(BytesIO(image)))
