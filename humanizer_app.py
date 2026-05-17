import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")


def humanize_with_ai(text, tone="professional"):
    if not API_KEY:
        return "API key is missing."

    prompt = f"""
Rewrite the text below to sound natural, clear, and human.
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
            return "Something went wrong. Please try again."

        return data["choices"][0]["message"]["content"]

    except Exception:
        return "Something went wrong. Please try again."


st.set_page_config(
    page_title="Humanize AI Text",
    page_icon="",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #f7f7f5;
        color: #1f2933;
    }

    .main .block-container {
        max-width: 880px;
        padding-top: 55px;
        padding-bottom: 40px;
    }

    .header {
        margin-bottom: 34px;
    }

    .label {
        font-size: 13px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #6b7280;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .title {
        font-size: 44px;
        line-height: 1.1;
        font-weight: 700;
        letter-spacing: -0.04em;
        color: #111827;
        margin-bottom: 14px;
    }

    .subtitle {
        font-size: 17px;
        line-height: 1.65;
        color: #4b5563;
        max-width: 680px;
    }

    .content-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0 12px 35px rgba(17, 24, 39, 0.06);
    }

    textarea {
        border-radius: 14px !important;
        border: 1px solid #d1d5db !important;
        background-color: #fafafa !important;
        font-size: 15px !important;
        color: #111827 !important;
    }

    textarea:focus {
        border-color: #111827 !important;
        box-shadow: none !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        border-radius: 14px;
        background-color: #fafafa;
    }

    div.stButton > button {
        width: 100%;
        background-color: #111827;
        color: white;
        border: none;
        border-radius: 14px;
        padding: 14px 18px;
        font-size: 15px;
        font-weight: 600;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #374151;
        color: white;
        border: none;
    }

    div.stButton > button:focus {
        box-shadow: none;
        outline: none;
    }

    h3 {
        color: #111827;
        letter-spacing: -0.02em;
    }

    .stTextArea label, .stSelectbox label {
        font-weight: 600;
        color: #374151;
        font-size: 14px;
    }

    .footer {
        margin-top: 28px;
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="header">
    <div class="label">AI Text Humanizer</div>
    <div class="title">Make your writing sound natural.</div>
    <div class="subtitle">
        Rewrite text into a clearer, smoother, and more human-sounding version while keeping the original meaning.
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="content-card">', unsafe_allow_html=True)

user_text = st.text_area(
    "Original text",
    height=220,
    placeholder="Paste your text here..."
)

tone = st.selectbox(
    "Tone",
    [
        "professional",
        "natural",
        "polite",
        "friendly",
        "formal",
        "simple",
        "casual"
    ]
)

if st.button("Humanize Text"):
    if user_text.strip():
        with st.spinner("Rewriting..."):
            result = humanize_with_ai(user_text, tone)

        st.subheader("Humanized text")
        st.text_area(
            "Result",
            value=result,
            height=260
        )
    else:
        st.warning("Please enter text first.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Clean rewriting for clearer communication.
</div>
""", unsafe_allow_html=True)