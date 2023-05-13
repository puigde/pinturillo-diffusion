import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh
from ui_utils import show_centered_title, exit_button, chat_callback

seed = 0  # TODO
hint_interval = 3  # seconds

def guessing_page():
    st.session_state.current_page = "Guessing"
    show_centered_title("Guessing")
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


def chat_component():
    username = "salcc"
    usercolor = "red"
    """The chat component."""
    if not hasattr(st.session_state, "chat"):
        st.session_state.chat = []
    st.markdown(f"""
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
    {"".join([f"<p><span style='color: {usercolor};'>{username}</span>: {message}</p>" for message in st.session_state.chat])}
    </div>
    """, unsafe_allow_html=True)
    st.text_input("", on_change=chat_callback, key="add_message", label_visibility="collapsed")
