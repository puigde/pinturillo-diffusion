from dataclasses import dataclass
import streamlit as st
from ui_utils import show_centered_title, exit_button, access_guessing_callback
import os
import random
import os
from streamlit_autorefresh import st_autorefresh
from ui_utils import show_centered_title, exit_button, winner_update_game_state, check_game_state
import time
import json

seed = time.time_ns() % 100
hint_interval = 40  # seconds


def pre_guessing_page():
    st.session_state.current_page = "Pre_guessing"
    show_centered_title("Enter a game:")
    current_game_id = st.text_input("Game id")
    if not os.path.exists(f"game_{current_game_id}"):
        prev_enter = st.button("Access game")
        if prev_enter:
            st.warning("Game id does not exist")
    else:
        access = st.button(
            "Access game", on_click=access_guessing_callback, args=(current_game_id,))
        if access:
            st.warning("Username taken for this game")
    exit_button()


def guessing_page():
    check_game_state()
    show_centered_title(f"Guessing in game {st.session_state.current_game_id}")
    with open(f"game_{st.session_state.current_game_id}/game_state.json", "r") as f:
        game_state = json.load(f)
    st.session_state.word = game_state["word"]
    st.session_state.count = st_autorefresh(interval=1000, key="counter")
    st.session_state.mask_count += 1
    c01, c02 = st.columns([1.2, 2])
    c0, c1 = st.columns(2)
    with c01:
        counter_component()
    with c02:
        hint_component()
    with c0:
        try:
            st.image(
                f"game_{st.session_state.current_game_id}/last_image.png", width=500)
        except:
            pass
    with c1:
        chat_component()
    exit_button()


def counter_component():
    """The counter component."""
    st.markdown(
        f"Time until next hint: {(hint_interval - st.session_state.mask_count) % (hint_interval + 1)}")


def mask_word(word, mask):
    """Masks a word with a list of indices."""
    return " ".join([word[i].upper() if i not in mask else "_" for i in range(len(word))])


def hint_component():
    """The prompt component."""
    mask = [i for i in range(len(st.session_state.word))]
    if not hasattr(st.session_state, "solved"):
        for i in range(st.session_state.mask_count // hint_interval):
            if len(mask) > 0:
                random.seed(i + seed)
                del mask[random.randint(0, len(mask) - 1)]
    else:
        mask = []
    st.markdown(
        f"<span style='font-family: monospace; font-size: 2em; font-weight: bold;'>{mask_word(st.session_state.word, mask)}</span>", unsafe_allow_html=True)


@dataclass
class Message:
    """A message."""
    player_name: str
    text: str


def read_chat_file(filename):
    """Reads a chat file.

    The chat file is a text file where each line is a message.
    The format of a message is:
    <player_name> <message>
    """
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as f:
        return [Message(*line.split(" ", 1)) for line in f.readlines()]


def usercolor(player_name):
    """Returns the color of a user."""
    return f"#{hash(player_name) % 0xffffff:06x}"


def chat_component():
    """The chat component."""
    st.session_state.chat = read_chat_file(
        f"game_{st.session_state.current_game_id}/chat.txt")
    m = f"""
    <style>
    #chat {{
        height: 470px;
        overflow-y: scroll;
        border: 1px solid #ccc;
    }}

    #chat p {{
        margin: 0;
    }}
    </style>

    <div id="chat">
    {"".join([f"<p><span style='color: {usercolor(message.player_name)};'>{message.player_name}</span>: {message.text.strip()}</p>" for message in st.session_state.chat])}
    </div>

    <script>
    // I think this does not work inside st.markdown...
    let chat = document.getElementById("chat");
    console.log(chat.scrollHeight);
    chat.scrollTop = chat.scrollHeight;
    </script>
    """
    st.markdown(m, unsafe_allow_html=True)
    st.text_input("Type here", on_change=chat_callback, key="add_message",
                  label_visibility="collapsed")


def chat_callback():
    with open(f"game_{st.session_state.current_game_id}/chat.txt", "a") as f:
        f.write(f"{st.session_state.player_name} {st.session_state.add_message}\n")
    if st.session_state.add_message.upper() == st.session_state.word.upper():
        st.balloons()
        st.session_state.mask_count = 0
        st.session_state.solved = True
        winner_update_game_state()
    else:
        st.session_state.chat.append(st.session_state.add_message)
    st.session_state.add_message = ""
