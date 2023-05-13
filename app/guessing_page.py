from dataclasses import dataclass
import streamlit as st
import random
import os
from streamlit_autorefresh import st_autorefresh
from ui_utils import show_centered_title, exit_button
import time

seed = time.time_ns() % 100  # TODO
hint_interval = 3  # seconds

def guessing_page():
    st.session_state.current_page = "Guessing"
    show_centered_title("Guessing")
    st.session_state.username = "salcc" + str(seed)
    st.session_state.word = "turtle"
    st.session_state.count = st_autorefresh(interval=1000, limit=hint_interval * 60, key="counter")
    c0, c1 = st.columns(2)
    with c0:
        counter_component()
        hint_component()
    with c1:
        chat_component()
    exit_button()

def counter_component():
    """The counter component."""
    st.text(f"Time until next hint: {(hint_interval - st.session_state.count) % (hint_interval + 1)}")

def mask_word(word, mask):
    """Masks a word with a list of indices."""
    return " ".join([word[i].upper() if i not in mask else "_" for i in range(len(word))])

def hint_component():
    """The prompt component."""
    mask = [i for i in range(len(st.session_state.word))]
    if not hasattr(st.session_state, "solved"):
        for i in range(st.session_state.count // hint_interval):
            if len(mask) > 0:
                random.seed(i + seed)
                del mask[random.randint(0, len(mask) - 1)]
    else:
        mask = []
    st.text(mask_word(st.session_state.word, mask))


@dataclass
class Message:
    """A message."""
    username: str
    text: str

def read_chat_file(filename):
    """Reads a chat file.
    
    The chat file is a text file where each line is a message.
    The format of a message is:
    <username> <message>
    """
    if not os.path.exists(filename):
        return []
    
    with open(filename, "r") as f:
        return [Message(*line.split(" ", 1)) for line in f.readlines()]

def usercolor(username):
    """Returns the color of a user."""
    return f"#{hash(username) % 0xffffff:06x}"

def chat_component():
    """The chat component."""
    st.session_state.chat = read_chat_file("chat.txt")
    m = f"""
    <style>
    .chat {{
        height: 300px;
        overflow-y: scroll;
        border: 1px solid #ccc;
    }}

    .chat p {{
        margin: 0;
    }}
    </style>

    <div class="chat">
    {"".join([f"<p><span style='color: {usercolor(message.username)};'>{message.username}</span>: {message.text.strip()}</p>" for message in st.session_state.chat])}
    </div>
    """
    print(m)
    st.markdown(m, unsafe_allow_html=True)
    st.text_input("", on_change=chat_callback, key="add_message", label_visibility="collapsed")

def chat_callback():
    st.session_state.chat.append(st.session_state.add_message)
    with open("chat.txt", "a") as f:
        f.write(f"{st.session_state.username} {st.session_state.add_message}\n")
    if st.session_state.add_message.upper() == st.session_state.word.upper():
        st.balloons()
        st.session_state.solved = True
    st.session_state.add_message = ""