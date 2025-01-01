import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import tempfile

# Configure generative AI API
genai.configure(api_key=st.secrets["api_key"])

def ai(txt):
    """
    Generates AI response based on the input.

    Parameters:
    - txt: The user's latest input.

    Returns:
    - AI response text.
    """
    # Use the configured generative AI model
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("give detailed information " + txt)
    return response.text

def speak_gtts(text):
    """
    Converts text to speech using gTTS and plays it using Streamlit.

    Parameters:
    - text: The text to be spoken.
    """
    tts = gTTS(text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# Streamlit app structure
st.title("QuantWeb.AI")
st.header("Developed by Codidioter")
st.write("\n" * 20)
st.markdown("---")
st.write("This AI can make mistakes, so check important info", align="bottom")
st.markdown("---")

# Initialize session state for storing chat messages if not already initialized
if "message" not in st.session_state:
    st.session_state.message = []

# Input from the user
input = st.chat_input("Ask QuantWeb")

# Display previous chat messages
for chat in st.session_state.message:
    with st.chat_message(chat["role"]):
        st.write(chat["message"])

# Button to display the full conversation history
if st.button("Show Conversation History"):
    history_text = "\n".join(
        f"{msg['role'].capitalize()}: {msg['message']}" for msg in st.session_state.message
    )
    st.text_area("Conversation History", value=history_text, height=300)

# Button to speak the last bot message
if st.button("Read aloud"):
    # Get the last bot message from the chat interface
    last_bot_message = next(
        (msg["message"] for msg in reversed(st.session_state.message) if msg["role"] == "bot"),
        None,
    )
    if last_bot_message:
        speak_gtts(last_bot_message)
        st.success("Speaking the message!")
    else:
        st.warning("No messages available to speak.")

# Process new input
if input:
    with st.chat_message("user"):
        st.write(input)
        # Append user's message to session state
        st.session_state.message.append({"role": "user", "message": input})

    if "Hello" in input or "hi" in input  or "hello" in input:
        with st.chat_message("bot"):
            bot_reply = "How can I help you 🙂!"
            st.write(bot_reply)
            # Append bot's message to session state
            st.session_state.message.append({"role": "bot", "message": bot_reply})
    elif "Who are you" in input or "who are you" in input:
        with st.chat_message("bot"):
            bot_reply = "I'm an updated version of CI-GPT. I've been fed with a lot of information and details!"
            st.write(bot_reply)
            # Append bot's message to session state
            st.session_state.message.append({"role": "bot", "message": bot_reply})
    elif "How many lines code does QuantWeb have?" in input:
        with st.chat_message("bot"):
            bot_reply = "My work is to assist you. Asking about personal information would be inappropriate!"
            st.write(bot_reply)
            # Append bot's message to session state
            st.session_state.message.append({"role": "bot", "message": bot_reply})
    elif "Tell about Logesh" in input or "tell about Logesh" in input:
        with st.chat_message("bot"):
            bot_reply = (
                "Logesh is the founder of Codidiot. He developed the QuantWeb background remover and QuantWeb.AI. "
                "He continues to work on developing more Python web apps!"
            )
            st.write(bot_reply)
            # Append bot's message to session state
            st.session_state.message.append({"role": "bot", "message": bot_reply})
    elif "Do you like Logesh" in input or "you like Logesh" in input:
        with st.chat_message("bot"):
            bot_reply = (
                "Yes, I like Logesh! He is the founder of Codidiot and has developed QuantWeb.AI and other tools."
            )
            st.write(bot_reply)
            # Append bot's message to session state
            st.session_state.message.append({"role": "bot", "message": bot_reply})
    else:
        # Generate AI response
        with st.chat_message("bot"):
            data = ai(input)
            st.write(data)
            # Append bot's message to session state
            st.session_state.message.append({"role": "bot", "message": data})

# Print conversation history for debugging
print(st.session_state.message)
