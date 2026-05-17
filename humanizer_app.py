import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env for local use
load_dotenv()

# Supports both local .env and Streamlit Cloud Secrets
API_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")


def humanize_with_ai(text, tone="professional"):
    if not API_KEY:
        return "⚠️ API key is missing. Please add OPENROUTER_API_KEY to your .env file or Streamlit Secrets."

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
                    {"role": "user", "content": prompt}
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


st.set_page_config(
    page_title="AI Text Humanizer",
    page_icon="✨",
    layout="centered"
)

# Custom CSS design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 45%, #fff8fb 100%);
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 45px;
        padding-bottom: 45px;
    }

    .hero-card {
        background: rgba(255, 255, 255, 0.85);
        padding: 35px;
        border-radius: 28px;
        box-shadow: 0 20px 50px rgba(30, 41, 59, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.7);
        margin-bottom: 25px;
    }

    .title {
        font-size: 44px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 8px;
        letter-spacing: -1px;
    }

    .subtitle {
        font-size: 17px;
        color: #6b7280;
        line-height: 1.6;
        margin-bottom: 0;
    }

    .badge {
        display: inline-block;
        background: #eef2ff;
        color: #4f46e5;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #6366f1, #ec4899);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 13px 22px;
        font-size: 16px;
        font-weight: 700;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 30px rgba(99, 102, 241, 0.38);
        color: white;
    }

    textarea {
        border-radius: 18px !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        border-radius: 16px;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        margin-top: 35px;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero-card">
    <div class="badge">✨ AI Writing Assistant</div>
    <div class="title">AI Text Humanizer</div>
    <p class="subtitle">
        Paste your message, choose a tone, and turn stiff writing into something clear,
        natural, and easy to understand.
    </p>
</div>
""", unsafe_allow_html=True)


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

        st.subheader("Humanized Version")
        st.text_area(
            "Result:",
            value=result,
            height=260
        )
    else:
        st.warning("Please enter some text first.")


st.markdown("""
<div class="footer">
    Built with Streamlit · Keep your API key private 🔐
</div>
""", unsafe_allow_html=True)