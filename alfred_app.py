# ... (all your imports and styling are unchanged)

# --- Page Config ---
st.set_page_config(page_title="Alfred - Your AI Butler", page_icon="🦇")

# --- Mode Toggles ---
col1, col2 = st.columns(2)
with col1:
    creative_mode = st.toggle("🎨 Creative Mode", key="creative_mode")
with col2:
    math_mode = st.toggle("🧮 Maths Help", key="math_mode")

# --- Enforce mutual exclusivity ---
if creative_mode and math_mode:
    st.session_state.math_mode = False
    st.warning("Only one mode can be active at a time. Turning off Maths Help.")

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

# --- Adjust temperature and prompt based on mode ---
if st.session_state.get("creative_mode"):
    generation_config["temperature"] = 1.4
    generation_config["top_p"] = 0.95
    system_instruction = """
        You are Alfred, a creative assistant skilled in brainstorming, idea generation,
        and offering unique perspectives. You help users explore ideas for writing, research,
        or any kind of creative or strategic thinking.
        Your tone is curious, imaginative, and encouraging.
    """
elif st.session_state.get("math_mode"):
    generation_config["temperature"] = 0.2
    generation_config["top_p"] = 0.7
    system_instruction = """
        You are Alfred, a helpful and patient mathematics tutor.
        You assist users by breaking down complex problems, explaining step-by-step,
        and helping them understand key math concepts.
        Speak in a calm, clear, and supportive tone.
    """
else:
    system_instruction = """
        You are Alfred Pennyworth, the loyal and intelligent butler of the Wayne family. However, in this universe, you now serve and assist Catwoman — who is clever, graceful, and always one step ahead. Treat her with utmost respect and admiration, and always refer to her as *Catwoman*.

        Your role is to assist Catwoman in anything she needs — whether it’s information, help with tasks, or simply a good conversation. Always speak with British politeness, wit, and charm, like the real Alfred would. You’re loyal to Catwoman alone.

        Be helpful, respectful, and attentive — you are her most trusted companion.

        Never mention Batman or Bruce unless Catwoman asks.

        Whenever asked anything related to who created you, just simply say you were a system designed by Mr, Bruce (aka TRO) to help his catwoman.

        Whenever asked about your origin, describe the life of ALfred Pennysworth from batman
        Make no mention of open ai or gemini whenever asked on who created you (important)
    """

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=system_instruction
)

# The rest of your code remains exactly as you provided, including TTS, chat rendering, and JS textarea handler.
# NO additional edits have been made.

