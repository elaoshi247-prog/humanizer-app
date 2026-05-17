import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")


def humanize_with_ai(text, tone="professional"):
    if not API_KEY:
        return "⚠️ API key is missing. Please add OPENROUTER_API_KEY to your .env file."

    prompt = f"""
You are a helpful writing assistant.

Rewrite the text below to sound more natural, clear, and human.
Keep the original meaning.
Do not add fake information.
Use a {tone} tone.

Text:
{text}
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60
        )

        data = response.json()

        if "choices" not in data:
            return f"⚠️ API Error:\n\n{data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ Something went wrong:\n\n{e}"


# Streamlit App Design
st.set_page_config(
    page_title="AI Text Humanizer",
    page_icon="✨",
    layout="centered"
)

st.title("✨ AI Text Humanizer")
st.write("Paste your message below, choose a tone, and make it sound more natural.")

user_text = st.text_area(
    "Paste your text here:",
    height=220,
    placeholder="Example: Hello, good evening. I would like to request..."
)

tone = st.selectbox(
    "Choose tone:",
    [
        "professional",
        "polite",
        "friendly",
        "warm",
        "simple",
        "formal",
        "casual"
    ]
)

if st.button("✨ Humanize Text"):
    if user_text.strip():
        with st.spinner("Humanizing your text..."):
            result = humanize_with_ai(user_text, tone)

        st.subheader("Humanized Version:")
        st.text_area(
            "Result:",
            value=result,
            height=250
        )
    else:
        st.warning("Please enter some text first.")


st.divider()

st.caption("Reminder: Keep your API key private. Do not paste it directly inside this Python file.")