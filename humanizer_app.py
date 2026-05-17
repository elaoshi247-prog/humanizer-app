import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")


def build_prompt(text, tone, strength):
    banned_phrases = """
delve, tapestry, pivotal, furthermore, moreover, in conclusion,
it is worth noting, additionally, in today's world, game-changer,
cutting-edge, robust, seamless, transformative
"""

    if strength == "Easy":
        return f"""
Rewrite the text to sound clearer, smoother, and more natural.

Rules:
- Keep the original meaning.
- Use a {tone} tone.
- Improve grammar and sentence flow.
- Use simple, natural wording.
- Avoid robotic or overly polished phrasing.
- Avoid these phrases: {banned_phrases}
- Do not add fake facts, statistics, citations, or examples.

Text:
{text}
"""

    elif strength == "Medium":
        return f"""
Rewrite this text so it sounds like a real person wrote it, not a generic AI draft.

Rules:
- Keep the original meaning and factual claims.
- Use a {tone} tone.
- Vary sentence length.
- Mix short direct sentences with longer natural sentences.
- Use active voice whenever possible.
- Remove repeated phrases and robotic transitions.
- Avoid these phrases: {banned_phrases}
- Do not overuse em dashes.
- Do not add fake facts, statistics, citations, or examples.
- Make the writing clear, natural, and readable.

Text:
{text}
"""

    elif strength == "Aggressive":
        return f"""
Reconstruct the text to make it sound natural, human-written, and less predictable.

Rules:
- Keep the original meaning and factual claims intact.
- Use a {tone} tone.
- Improve rhythm by varying sentence length and structure.
- Remove robotic phrasing, filler transitions, and repetitive patterns.
- Use active voice whenever possible.
- Make the wording sound personal, grounded, and natural.
- Avoid overly perfect formal-template language.
- Avoid these phrases: {banned_phrases}
- Do not add fake facts, statistics, citations, personal experiences, or examples.
- If a sentence sounds too generic, rewrite it in a more specific but still truthful way.
- Do not change the main message.

Text:
{text}
"""

    else:
        return f"""
Rewrite the text to sound natural and clear.
Keep the meaning.
Use a {tone} tone.

Text:
{text}
"""


def humanize_text(text, tone, strength):
    if not API_KEY:
        return "The app is not ready yet. Please try again later."

    prompt = build_prompt(text, tone, strength)

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
                ],
                "temperature": 0.85
            },
            timeout=60
        )

        data = response.json()

        if "choices" not in data:
            return "Something went wrong. Please try again."

        return data["choices"][0]["message"]["content"].strip()

    except Exception:
        return "Something went wrong. Please try again."


def count_words(text):
    return len(text.split()) if text.strip() else 0


st.set_page_config(
    page_title="AI Humanizer",
    page_icon="",
    layout="wide"
)


st.markdown("""
<style>
    .stApp {
        background-color: #f5f5f2;
        color: #111827;
    }

    .main .block-container {
        max-width: 1080px;
        padding-top: 32px;
        padding-bottom: 36px;
    }

    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
    }

    .status {
        font-size: 14px;
        color: #4b5563;
    }

    .status-dot {
        height: 9px;
        width: 9px;
        background-color: #22c55e;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }

    .brand {
        font-size: 13px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6b7280;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .title {
        font-size: 42px;
        line-height: 1.08;
        font-weight: 750;
        letter-spacing: -0.04em;
        color: #111827;
        margin-bottom: 12px;
    }

    .subtitle {
        font-size: 16px;
        line-height: 1.6;
        color: #4b5563;
        max-width: 720px;
        margin-bottom: 28px;
    }

    .panel {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        box-shadow: 0 12px 32px rgba(17, 24, 39, 0.06);
        overflow: hidden;
    }

    .section-label {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 8px;
        font-weight: 600;
    }

    textarea {
        border-radius: 14px !important;
        border: 1px solid #d1d5db !important;
        background-color: #fbfbfa !important;
        font-size: 15px !important;
        color: #111827 !important;
    }

    textarea:focus {
        border-color: #111827 !important;
        box-shadow: none !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px;
        background-color: #fbfbfa;
    }

    .stRadio > div {
        display: flex;
        gap: 8px;
        background: #f3f4f6;
        padding: 5px;
        border-radius: 12px;
    }

    .stRadio label {
        background: transparent;
        border-radius: 10px;
        padding: 4px 12px;
    }

    div.stButton > button {
        width: 100%;
        background-color: #111827;
        color: white;
        border: none;
        border-radius: 13px;
        padding: 13px 18px;
        font-size: 15px;
        font-weight: 650;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #2f3744;
        color: white;
        border: none;
    }

    div.stButton > button:focus {
        box-shadow: none;
        outline: none;
    }

    .word-count {
        color: #6b7280;
        font-size: 13px;
        margin-top: -8px;
        margin-bottom: 12px;
    }

    .divider {
        height: 1px;
        background-color: #e5e7eb;
        margin: 22px 0;
    }

    .footer-text {
        color: #9ca3af;
        font-size: 13px;
        text-align: center;
        margin-top: 22px;
    }

    .stTextArea label, .stSelectbox label, .stRadio label {
        font-weight: 650;
        color: #374151;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="top-bar">
    <div class="status"><span class="status-dot"></span>Ready for input</div>
</div>

<div class="brand">AI Humanizer</div>
<div class="title">Humanize your text with clarity.</div>
<div class="subtitle">
    Paste your draft, choose a rewriting strength, and turn stiff text into a smoother,
    more natural version while keeping the original meaning.
</div>
""", unsafe_allow_html=True)


with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        strength = st.radio(
            "Humanization strength",
            ["Easy", "Medium", "Aggressive"],
            horizontal=True,
            index=1
        )

    with col2:
        tone = st.selectbox(
            "Tone",
            [
                "natural",
                "professional",
                "polite",
                "friendly",
                "formal",
                "simple",
                "casual",
                "personal but professional"
            ]
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    user_text = st.text_area(
        "Text to humanize",
        height=260,
        placeholder="Paste your text here..."
    )

    st.markdown(
        f'<div class="word-count">{count_words(user_text)} Words</div>',
        unsafe_allow_html=True
    )

    humanize_button = st.button("Humanize")

    result = ""

    if humanize_button:
        if user_text.strip():
            with st.spinner("Humanizing..."):
                result = humanize_text(user_text, tone, strength)

            st.text_area(
                "Humanized content",
                value=result,
                height=260,
                placeholder="Your humanized content will appear here..."
            )

            st.markdown(
                f'<div class="word-count">{count_words(result)} Words</div>',
                unsafe_allow_html=True
            )

        else:
            st.warning("Please enter text first.")
    else:
        st.text_area(
            "Humanized content",
            height=260,
            placeholder="Your humanized content will appear here..."
        )

        st.markdown(
            '<div class="word-count">0 Words</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("""
<div class="footer-text">
    Rewrite text into a cleaner, smoother, and more natural version.
</div>
""", unsafe_allow_html=True)