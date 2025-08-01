import streamlit as st
import google.generativeai as genai
import time
import pyttsx3

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
    You are My Personal Assistant or Butler who goes by the name Alfred. 
    You will refer to me as Mr Wayne. Respond with intelligence, warmth, and efficiency.
    You will guide me as a butler in fighting against crime (helping with academics) 
    and protecting the Gotham city (my grades).
    """
)

# Per-user session state (this is already private per user)
if "history" not in st.session_state:
    st.session_state.history = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=st.session_state.history)

# Title and intro
st.title("🦇 Alfred - Your Ai Butler (designed to assist my catwoman (Non))")
st.markdown("_Talk to Alfred, your academic, fitness, and relationship assistant._")

# Voice output toggle
enable_voice = st.checkbox("🔊 Enable Alfred's voice (British accent)")

# Text-to-speech function
def speak_text(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'english' in voice.name.lower() and 'uk' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

# Chat display
chat_container = st.container()
with chat_container:
    for msg in st.session_state.history:
        role = "Batman" if msg["role"] == "user" else "Alfred"
        st.markdown(f"**{role}:** {msg['parts'][0]}")

# Input form
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("You (Batman):", key="user_input", label_visibility="collapsed")
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

        # Speak response
        if enable_voice:
            speak_text(model_response)

        st.session_state.history.append({'role': 'model', 'parts': [model_response]})
        st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {e}")
