import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load local .env file
load_dotenv()

# Works for both local .env and Streamlit Cloud Secrets
API_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")


def build_prompt(text, tone, prompt_mode, audience, use_case, constraints):
    banned_phrases = """
delve, tapestry, pivotal, furthermore, moreover, in conclusion,
it is worth noting, additionally, in today's world, game-changer
"""

    if prompt_mode == "Core humanizer":
        return f"""
Rewrite this text so it sounds like a knowledgeable person wrote it, not an AI assistant.

Apply these rules:
- Keep the original meaning and factual claims intact.
- Use a {tone} tone.
- Vary sentence length. Mix short sentences with longer ones.
- Never make every sentence follow the same rhythm.
- Use active voice whenever possible.
- Remove robotic, generic, or overused AI phrases.
- Avoid these phrases: {banned_phrases}
- Do not overuse em dashes.
- Do not add fake facts, statistics, citations, or examples.
- Make the writing clear, natural, and readable.

Text:
{text}
"""

    elif prompt_mode == "First-person rewrite":
        return f"""
Please rewrite the following content from a first-person perspective, transforming it from a neutral summary into a natural personal version.

Content to rewrite:
{text}

Tone:
{tone}

Constraints:
- Keep all factual claims the same.
- Use "I" naturally where appropriate.
- Make it sound personal but still clear.
- If you add an example, make it clearly labeled hypothetical.
- Remove buzzwords and repeated phrases.
- Avoid these phrases: {banned_phrases}
- Do not invent statistics, credentials, citations, or real case studies.
- Make it sound like a real person wrote it, not a perfect formal template.
"""

    elif prompt_mode == "Natural reconstruction":
        return f"""
Reconstruct the provided text to improve flow and reduce robotic or predictable phrasing.

Text to reconstruct:
{text}

Tone:
{tone}

Rules:
- Vary sentence length.
- Improve paragraph flow.
- Use active voice.
- Remove repetitive structure.
- Remove robotic transitions and filler phrases.
- Avoid these phrases: {banned_phrases}
- Make the writing smoother without changing the meaning.

Do not:
- Add an H1.
- Use filler intros like "In today's world."
- Keep the same paragraph count if it hurts the flow.
- Add fake details or unsupported claims.
"""

    elif prompt_mode == "Context-enhanced rewrite":
        return f"""
Enhance the text by grounding it in clear, real-world context and nuanced vocabulary that fits the audience and purpose.

Draft:
{text}

Context to include:
- Audience: {audience}
- Use case: {use_case}
- Constraints: {constraints}

Tone:
{tone}

Rules:
- Keep the original meaning.
- Use active voice whenever possible.
- Vary sentence and paragraph length.
- Avoid generic AI-style phrasing.
- Avoid these phrases: {banned_phrases}
- Do not invent statistics, credentials, citations, or real case studies.
- If more detail is needed but not provided, write [ADD SPECIFIC EXAMPLE].
"""

    elif prompt_mode == "Academic humanizer":
        return f"""
Rewrite this academic text so it reads as if a fluent human scholar wrote it, not an AI assistant.

Text:
{text}

Tone:
{tone}

Apply these rules carefully:
- Maintain a formal academic register.
- Do not make the writing casual or conversational.
- Vary sentence length. Mix shorter analytical sentences with longer sentences that include embedded clauses.
- Remove passive voice where the agent is identifiable.
- Keep passive voice only where academic convention requires it.
- Replace AI transition phrases with precise academic alternatives.
- Avoid these phrases: {banned_phrases}
- Preserve all citations, statistics, and technical terminology exactly.
- Do not invent sources, statistics, studies, or credentials.
- If an example is needed but not provided, write [ADD EXAMPLE] instead of inventing one.
"""

    elif prompt_mode == "Blog or marketing rewrite":
        return f"""
Rewrite this blog or marketing draft so it reads like a knowledgeable writer with a clear point of view, not an AI assistant.

Draft:
{text}

Tone:
{tone}

Apply these rules:
- Open with a direct sentence that states the point clearly.
- Vary paragraph length.
- Mix short, punchy sentences with longer explanatory ones.
- Use active voice.
- Write naturally for the reader.
- Avoid these phrases: {banned_phrases}
- Replace generic transitions with more specific, natural connections.
- Keep all facts, statistics, and links exactly as they are.
- Do not invent claims, numbers, or examples.
"""

    elif prompt_mode == "Social media rewrite":
        return f"""
Rewrite this social media post so it sounds like a real person wrote it, not a content brief or AI draft.

Post:
{text}

Tone:
{tone}

Rules:
- Write naturally and directly.
- Use contractions when appropriate.
- No markdown.
- No headers.
- No bullet points.
- Avoid these phrases: {banned_phrases}
- Keep the message clear and human.
- End with either a direct question or one clear call to action, not both.
- Do not add fake details.
"""

    elif prompt_mode == "Professional message":
        return f"""
Rewrite this message so it sounds professional, natural, and respectful.

Message:
{text}

Tone:
{tone}

Rules:
- Keep the message clear and direct.
- Make it sound polite but not overly formal.
- Use simple professional wording.
- Remove repeated phrases.
- Avoid these phrases: {banned_phrases}
- Do not add fake information.
- Keep the original request or message intact.
"""

    else:
        return f"""
Rewrite the text below to sound natural, clear, and human-written.
Keep the original meaning.
Use a {tone} tone.
Avoid robotic phrasing.
Do not add fake information.

Text:
{text}
"""


def humanize_with_ai(text, tone, prompt_mode, audience, use_case, constraints):
    if not API_KEY:
        return "API key is missing."

    prompt = build_prompt(text, tone, prompt_mode, audience, use_case, constraints)

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


# Page setup
st.set_page_config(
    page_title="Humanize AI Text",
    page_icon="",
    layout="centered"
)


# Minimalist professional design
st.markdown("""
<style>
    .stApp {
        background-color: #f6f6f3;
        color: #111827;
    }

    .main .block-container {
        max-width: 920px;
        padding-top: 56px;
        padding-bottom: 48px;
    }

    .header {
        margin-bottom: 34px;
    }

    .label {
        font-size: 12px;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        color: #6b7280;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .title {
        font-size: 44px;
        line-height: 1.08;
        font-weight: 750;
        letter-spacing: -0.04em;
        color: #111827;
        margin-bottom: 14px;
    }

    .subtitle {
        font-size: 17px;
        line-height: 1.65;
        color: #4b5563;
        max-width: 710px;
    }

    .content-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 30px;
        box-shadow: 0 12px 34px rgba(17, 24, 39, 0.055);
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
        border-radius: 14px;
        background-color: #fbfbfa;
    }

    .stTextInput input {
        border-radius: 14px;
        background-color: #fbfbfa;
    }

    div.stButton > button {
        width: 100%;
        background-color: #111827;
        color: white;
        border: none;
        border-radius: 14px;
        padding: 14px 18px;
        font-size: 15px;
        font-weight: 650;
        transition: 0.2s ease;
        margin-top: 6px;
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

    h3 {
        color: #111827;
        letter-spacing: -0.02em;
        margin-top: 24px;
    }

    .stTextArea label, .stSelectbox label, .stTextInput label {
        font-weight: 650;
        color: #374151;
        font-size: 14px;
    }

    .small-note {
        color: #6b7280;
        font-size: 13px;
        line-height: 1.5;
        margin-top: -4px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


# Header
st.markdown("""
<div class="header">
    <div class="label">AI Text Humanizer</div>
    <div class="title">Make your writing sound natural.</div>
    <div class="subtitle">
        Rewrite text into a clearer, smoother, and more natural version while keeping the original meaning.
    </div>
</div>
""", unsafe_allow_html=True)


# Main content card
st.markdown('<div class="content-card">', unsafe_allow_html=True)

user_text = st.text_area(
    "Original text",
    height=220,
    placeholder="Paste your text here..."
)

prompt_mode = st.selectbox(
    "Rewrite style",
    [
        "Core humanizer",
        "Professional message",
        "First-person rewrite",
        "Natural reconstruction",
        "Context-enhanced rewrite",
        "Academic humanizer",
        "Blog or marketing rewrite",
        "Social media rewrite"
    ]
)

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

audience = ""
use_case = ""
constraints = ""

if prompt_mode == "Context-enhanced rewrite":
    audience = st.text_input(
        "Audience",
        placeholder="Example: teacher, professor, client, parent, student..."
    )

    use_case = st.text_input(
        "Use case",
        placeholder="Example: school submission, email, report, message..."
    )

    constraints = st.text_input(
        "Constraints",
        placeholder="Example: 150 words, formal tone, no added facts..."
    )

if st.button("Humanize Text"):
    if user_text.strip():
        with st.spinner("Rewriting..."):
            result = humanize_with_ai(
                user_text,
                tone,
                prompt_mode,
                audience,
                use_case,
                constraints
            )

        st.subheader("Humanized text")
        st.text_area(
            "Result",
            value=result,
            height=280
        )
    else:
        st.warning("Please enter text first.")

st.markdown('</div>', unsafe_allow_html=True)