import streamlit as st
import google.generativeai as genai
import time
import streamlit.components.v1 as components

st.markdown("""
    <style>
    /* Light rounded and padded input */
    textarea, input[type="text"] {
        border-radius: 1rem !important;
        padding: 0.75rem !important;
        border: 1px solid #ccc !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        font-size: 1rem !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s ease-in-out;
    }

    /* On focus: a soft border color and slight glow */
    textarea:focus, input[type="text"]:focus {
        border: 1px solid #5b9bd5 !important;
        box-shadow: 0 0 8px rgba(91, 155, 213, 0.3) !important;
    }

    /* Optional: placeholder color */
    textarea::placeholder, input[type="text"]::placeholder {
        color: #888 !important;
    }
    </style>
""", unsafe_allow_html=True)


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


# Set page config
st.set_page_config(page_title="Alfred - Your AI Butler", page_icon="🦇")

# Configure API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Create the model
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

# Per-user session state
if "history" not in st.session_state:
    st.session_state.history = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=st.session_state.history)

# Title and intro
st.title("🦇 Alfred - Your Ai Butler")
st.markdown("_Designed To Assist My CatWoman(non)._")

# Voice output toggle
# Voice output toggle
enable_voice = st.checkbox("🔊 Enable Alfred's voice (British accent)")

# Chat reset button
if st.button("🗑️ Reset Chat"):
    st.session_state.history = []
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()


# JavaScript text-to-speech (browser-based)
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
        role = "Batman" if msg["role"] == "user" else "Alfred"
        st.markdown(f"**{role}:** {msg['parts'][0]}")

# Input form
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_area(height=40, key ="user_input" , placeholder="Ask Alfred something...")
    submitted = st.form_submit_button("Send")

# Handle message submission
if submitted and user_input.strip():
    try:
        st.session_state.history.append({'role': 'user', 'parts': [user_input]})
        response = st.session_state.chat_session.send_message(user_input)
        model_response = response.text

        # Typing animation
        with chat_container:
            st.markdown(f"**Batman:** {user_input}")
            display_text = ""
            response_container = st.empty()
            for char in model_response:
                display_text += char
                response_container.markdown(f"**Alfred:** {display_text}")
                time.sleep(0.015)

        # Speak using browser TTS
        if enable_voice:
            browser_tts(model_response)

        st.session_state.history.append({'role': 'model', 'parts': [model_response]})
        st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {e}")
