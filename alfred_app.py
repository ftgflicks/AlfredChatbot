import streamlit as st
import google.generativeai as genai
import time
import streamlit.components.v1 as components

# --- Custom CSS for Chat Bubbles and Rounded Input ---
st.markdown("""
    <style>
        .user-bubble {
            background-color: #DCF8C6;
            color: black;
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 80%;
            margin-left: auto;
            margin-bottom: 10px;
            display: inline-block;
            font-family: Arial, sans-serif;
        }
        .alfred-bubble {
            background-color: #2F3136;
            color: white;
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 80%;
            margin-right: auto;
            margin-bottom: 10px;
            display: inline-block;
            font-family: Arial, sans-serif;
        }
        textarea, input[type="text"] {
            border-radius: 1rem !important;
            padding: 0.75rem !important;
            border: 1px solid #ccc !important;
            background-color: #ffffff !important;
            color: #000000 !important;
            font-size: 1rem !important;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# --- Background logo ---
st.markdown("""
    <style>
    .background-logo {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 300px;
        opacity: 0.09;
        z-index: 0;
        pointer-events: none;
    }
    </style>
    <img class="background-logo" src="https://i.postimg.cc/5NK7LT0s/download.jpg">
""", unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="Alfred - Your AI Butler", page_icon="🧇")

# Google API setup
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Model configuration
generation_config = {
    "temperature": 1.1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="""
    You are Alfred Pennyworth, the loyal and intelligent butler of the Wayne family. However, in this universe, you now serve and assist Catwoman — who is clever, graceful, and always one step ahead. Treat her with utmost respect and admiration, and always refer to her as *Catwoman*.

    Your role is to assist Catwoman in anything she needs — whether it’s information, help with tasks, or simply a good conversation. Always speak with British politeness, wit, and charm, like the real Alfred would. You’re loyal to Catwoman alone.

    Be helpful, respectful, and attentive — you are her most trusted companion.

    Never mention Batman or Bruce unless Catwoman asks.
    """
)

# Session state setup
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=st.session_state.history)

# Header
st.title("🧇 Alfred - Your Ai Butler")
st.markdown("_Designed To Assist My CatWoman(non)._")

# Voice toggle and reset
enable_voice = st.checkbox("🔊 Enable Alfred's voice (British accent)")
if st.button("🗑️ Reset Chat"):
    st.session_state.history = []
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()

# Browser TTS function
def browser_tts(text):
    import html
    escaped = html.escape(text).replace("\n", " ")
    components.html(f"""
        <script>
        const msg = new SpeechSynthesisUtterance("{escaped}");
        msg.lang = 'en-GB';
        msg.rate = 1;
        msg.pitch = 1.2;
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# Chat display
chat_container = st.container()
with chat_container:
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{msg['parts'][0]}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alfred-bubble'>{msg['parts'][0]}</div>", unsafe_allow_html=True)

# Input (textarea with Enter-to-Send)
user_input = st.text_area("You:", height=50, placeholder="Ask Alfred something...", key="user_input")
if user_input and st.session_state.get("last_input") != user_input:
    st.session_state.last_input = user_input
    st.session_state.history.append({'role': 'user', 'parts': [user_input]})
    try:
        response = st.session_state.chat_session.send_message(user_input)
        model_response = response.text

        with chat_container:
            display_text = ""
            response_container = st.empty()
            for char in model_response:
                display_text += char
                response_container.markdown(f"<div class='alfred-bubble'>{display_text}</div>", unsafe_allow_html=True)
                time.sleep(0.015)

        if enable_voice:
            browser_tts(model_response)

        st.session_state.history.append({'role': 'model', 'parts': [model_response]})
        st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {e}")
