import streamlit as st
import random
import json
import os
from drawing_page import create_game
from ui_utils import access_guessing_callback, drawing_page_callback
import json


def postgame_page():
    # read the game state.json as json
    with open(f"game_{st.session_state.current_game_id}/game_state.json", "r") as f:
        game_state = json.load(f)
    if game_state["drawing_player"] == st.session_state.player_name and game_state["status"] == "finished":
        # read the players
        with open(f"game_{st.session_state.current_game_id}/players.txt", "r") as f:
            players = f.read().split("\n")
            players = [player for player in players if player !=
                       st.session_state.player_name and player != ""]
            # pick a random player to be the next drawer
            print(players)
            next_drawer = random.choice(players)
            print(next_drawer)
            # update the game state
            game_state["next_drawing_player"] = next_drawer
            game_state["status"] = "loading_next"
            game_state["next_game_id"] = random.randint(1000, 9999)
            while os.path.exists(f"game_{game_state['next_game_id']}"):
                game_state["next_game_id"] = random.randint(1000, 9999)
            # write the game state
            with open(f"game_{st.session_state.current_game_id}/game_state.json", "w") as f:
                json.dump(game_state, f)
            # create the next game
            create_game(game_state["next_game_id"], next_drawer)
            st.title(game_state["next_game_id"])
            st.session_state.current_game_id = game_state["next_game_id"]
            st.session_state.current_page = "Guessing"
            st.session_state.generated_images = []
            st.experimental_rerun()
    elif "next_drawing_player" in game_state and (game_state["next_drawing_player"] == st.session_state.player_name) and (game_state["status"] == "loading_next"):
        st.session_state.current_game_id = game_state["next_game_id"]
        drawing_page_callback()
        st.experimental_rerun()
    else:
        access_guessing_callback()
        st.experimental_rerun()
