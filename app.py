import json
import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

st.set_page_config(page_title="Simple AI Chatbot", page_icon="💬")
st.title("💬 Simple AI Chatbot")
st.caption("Ask questions using the information in knowledge.json.")

# Keep the conversation in memory for this browser session.
if "messages" not in st.session_state:
    st.session_state.messages = []

def load_knowledge():
    """Read the local JSON knowledge file."""
    try:
        with open("knowledge.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Could not load knowledge.json: {error}")
        return {}

knowledge = load_knowledge()

# Groq is used here, so the key must be GROQ_API_KEY (not GEMINI_API_KEY).
api_key = os.getenv("GROQ_API_KEY", "").strip()

with st.sidebar:
    st.header("Settings")
    st.write("Model: `openai/gpt-oss-20b`")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.caption("Conversation history lasts for this session only.")

# Show existing messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept a new message from the user.
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key or api_key == "your_groq_api_key_here":
        answer = (
            "Please add your Groq API key to the `GROQ_API_KEY` value in your "
            "`.env` file, then restart the app."
        )
        with st.chat_message("assistant"):
            st.warning(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        # Tell the model to prioritize the information in the JSON file.
        system_message = {
            "role": "system",
            "content": (
                "You are a helpful assistant. Use the following JSON knowledge "
                "as the primary source for answering questions. If the answer "
                "is not present in the JSON, say that the provided knowledge "
                "does not contain the answer; you may then offer general help "
                "but clearly distinguish it from the JSON information.\n\n"
                "JSON knowledge:\n"
                + json.dumps(knowledge, ensure_ascii=False, indent=2)
            ),
        }

        # Send the system prompt and the session's conversation history to Groq.
        api_messages = [system_message] + [
            {"role": item["role"], "content": item["content"]}
            for item in st.session_state.messages
        ]

        try:
            client = Groq(api_key=api_key)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=api_messages,
                        temperature=0.2,
                    )
                    answer = response.choices[0].message.content or "I couldn't generate a response."
                    st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
        except Exception as error:
            # Show a useful message without exposing secret credentials.
            st.error(
                "The request to Groq failed. Check your internet connection and "
                "API key, then try again. Details: "
                f"{type(error).__name__}: {error}"
            )
