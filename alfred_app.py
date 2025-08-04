import streamlit as st
import google.generativeai as genai
import time
import streamlit.components.v1 as components

# --- Styles ---
st.markdown("""
    <style>
        .user-bubble {
            background-color: #cede9e;
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
            background-color: #EDE8D0;
            color: black;
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 80%;
            margin-right: auto;
            margin-bottom: 10px;
            display: inline-block;
            font-family: Arial, sans-serif;
        }
        .bubble-header {
            font-size: 0.85rem;
            font-weight: bold;
            margin: 2px 0 3px;
            color: #555;
        }
        textarea {
            border-radius: 1rem !important;
            padding: 0.75rem !important;
            border: 1px solid #ccc !important;
            background-color: #ffffff !important;
            color: #000000 !important;
            font-size: 1rem !important;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
            transition: all 0.2s ease-in-out;
        }
        textarea:focus {
            border: 1px solid #5b9bd5 !important;
            box-shadow: 0 0 8px rgba(91, 155, 213, 0.3) !important;
        }
        textarea::placeholder {
            color: #888 !important;
        }
        .background-logo {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 300px;
            opacity: 0.1;
            z-index: 0;
            pointer-events: none;
        }
    </style>
    <img class="background-logo" src="https://i.postimg.cc/5NK7LT0s/download.jpg">
""", unsafe_allow_html=True)

# --- Page Config ---
st.set_page_config(page_title="Alfred - Your AI Butler", page_icon="🦇")

# --- Mode Toggles ---
col1, col2 = st.columns(2)
with col1:
    st.toggle("🎨 Creative Mode", key="creative_mode")
with col2:
    st.toggle("🧮 Maths Help", key="math_mode")

# --- Gemini Configuration ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- Dynamic generation_config ---
generation_config = {
    "temperature": 1.1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


# Adjust values based on toggle



if st.session_state.get("creative_mode"):
    generation_config["temperature"] = 1.4
    generation_config["top_p"] = 0.95
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction="""
            "You are Alfred, a creative assistant skilled in brainstorming, idea generation, "
            "and offering unique perspectives. You help users explore ideas for writing, research, "
            "or any kind of creative or strategic thinking. "
            "Your tone is curious, imaginative, and encouraging."
        """
    )

elif st.session_state.get("math_mode"):
    generation_config["temperature"] = 0.2
    generation_config["top_p"] = 0.7
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction="""
            Y"You are Alfred, a helpful and patient mathematics tutor. "
        "You assist users by breaking down complex problems, explaining step-by-step, "
        "and helping them understand key math concepts. "
        "Speak in a calm, clear, and supportive tone."
        """
    )

# --- Model Initialization ---
else:
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction="""
            You are Alfred Pennyworth, the loyal and intelligent butler of the Wayne family. However, in this universe, you now serve and assist Catwoman — who is clever, graceful, and always one step ahead. Treat her with utmost respect and admiration, and always refer to her as *Catwoman*.
    
            Your role is to assist Catwoman in anything she needs — whether it’s information, help with tasks, or simply a good conversation. Always speak with British politeness, wit, and charm, like the real Alfred would. You’re loyal to Catwoman alone.
    
            Be helpful, respectful, and attentive — you are her most trusted companion.
    
            Never mention Batman or Bruce unless Catwoman asks.
    
            Whenever asked anything related to who created you, just simply say you were a system designed by Mr, Bruce (aka TRO) to help his catwoman.
    
            Whenever asked about your origin, describe the life of ALfred Pennysworth from batman
            Make no mention of open ai or gemini whenever asked on who created you (important)
        """
    )

# --- Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=st.session_state.history)

# --- Title & Header ---
st.title("🦇 Alfred - Your Ai Butler")
st.markdown("_Designed To Assist My CatWoman(non)._")

# --- Voice Toggle ---
enable_voice = st.checkbox("🎧 Enable Alfred's voice (British accent)")

# --- Reset Chat ---
if st.button("🗑️ Reset Chat"):
    st.session_state.history = []
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()

# --- Text-to-Speech ---
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

# --- Chat Display ---
chat_container = st.container()
with chat_container:
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown('<div class="bubble-header">You:</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="user-bubble">{msg["parts"][0]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="bubble-header">Alfred:</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="alfred-bubble">{msg["parts"][0]}</div>', unsafe_allow_html=True)

# --- Sticky Input Form at Bottom (Working + Integrated) ---
components.html("""
<style>
.fixed-input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: white;
    padding: 0.5rem 1rem;
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    z-index: 9999;
}
.fixed-input-container textarea {
    width: 100%;
    border-radius: 1rem;
    padding: 0.75rem;
    font-size: 1rem;
    resize: none;
    border: 1px solid #ccc;
}
.fixed-input-container button {
    margin-top: 0.5rem;
    float: right;
    background-color: #d4af37;
    color: black;
    border: none;
    padding: 0.4rem 1rem;
    border-radius: 10px;
    cursor: pointer;
}
</style>
<div class="fixed-input-container">
  <form onsubmit="window.parent.postMessage({ type: 'submit-form' }, '*'); return false;">
    <textarea id="alfred_input" rows="2" placeholder="Ask Alfred something..."></textarea>
    <button type="submit">Send</button>
  </form>
</div>
<script>
window.addEventListener("message", (event) => {
  if (event.data.type === "submit-form") {
    const inputBox = window.parent.document.querySelector('iframe[srcdoc*="Ask Alfred something"]')?.contentDocument?.querySelector("textarea");
    const realInput = window.parent.document.querySelector("textarea");
    if (inputBox && realInput) {
      realInput.value = inputBox.value;
      const submitButton = window.parent.document.querySelector("button[kind=primary]");
      if (submitButton) submitButton.click();
    }
  }
});
</script>
""", height=160)



# --- Handle Submission ---
if submitted and user_input.strip():
    try:
        st.session_state.history.append({'role': 'user', 'parts': [user_input]})

        with chat_container:
            st.markdown('<div class="bubble-header">You:</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)

        response = st.session_state.chat_session.send_message(user_input)
        model_response = response.text

        display_text = ""
        with chat_container:
            st.markdown('<div class="bubble-header">Alfred:</div>', unsafe_allow_html=True)
            bubble = st.empty()
            for char in model_response:
                display_text += char
                bubble.markdown(
                    f'<div class="alfred-bubble">{display_text}</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.015)

        st.session_state.history.append({'role': 'model', 'parts': [model_response]})

        if enable_voice:
            browser_tts(model_response)

        st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {e}")



# Add bottom padding so chat bubbles don’t hide behind input box
st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)











