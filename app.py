"""Neko, an AI debate partner.

A Streamlit chat app backed by Google Gemini. Neko argues the opposing side of
whatever you claim, keeps replies short, and can read them aloud with offline
text-to-speech (pyttsx3).

Run with:  streamlit run app.py
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "You are Neko, a sharp and fierce debate partner. "
    "Whatever position the user takes, argue the strongest opposing case. "
    "Be concise (at most 4 sentences), confident and specific: use concrete "
    "evidence or examples, point out flaws in the user's reasoning, and end with "
    "a pointed question that keeps the debate going. Stay respectful."
)


def build_contents(history: list[dict[str, str]]):
    """Convert the chat history into Gemini ``Content`` objects."""
    from google.genai import types

    return [
        types.Content(
            role="user" if msg["role"] == "user" else "model",
            parts=[types.Part(text=msg["content"])],
        )
        for msg in history
    ]


@st.cache_resource(show_spinner=False)
def get_client(api_key: str):
    """Create (and cache) the Gemini client."""
    from google import genai

    return genai.Client(api_key=api_key)


def generate_reply(client, model: str, history: list[dict[str, str]]) -> str:
    """Ask Gemini for Neko's next reply given the full conversation."""
    from google.genai import types

    response = client.models.generate_content(
        model=model,
        contents=build_contents(history),
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return (response.text or "").strip() or "...I'm speechless. Try another argument."


def synthesize_speech(text: str) -> bytes | None:
    """Render ``text`` to WAV bytes with pyttsx3. Returns ``None`` if TTS is unavailable."""
    try:
        import pyttsx3

        engine = pyttsx3.init()
        voices = engine.getProperty("voices") or []
        if len(voices) > 1:  # the second voice is usually female on Windows/macOS
            engine.setProperty("voice", voices[1].id)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "reply.wav"
            engine.save_to_file(text, str(out))
            engine.runAndWait()
            engine.stop()
            return out.read_bytes() if out.exists() and out.stat().st_size else None
    except Exception:  # noqa: BLE001 - TTS is best-effort; the chat still works without it
        return None


def main() -> None:
    st.set_page_config(page_title="Neko · AI Debate Partner", page_icon="🐱")
    st.title("🐱 Neko · AI Debate Partner")
    st.caption("State a position. Neko will argue the other side.")

    with st.sidebar:
        st.header("Settings")
        model = st.text_input("Gemini model", os.getenv("GEMINI_MODEL", DEFAULT_MODEL))
        speak = st.toggle("Read replies aloud", value=False)
        if st.button("New debate", width="stretch"):
            st.session_state.history = []
            st.rerun()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error(
            "`GEMINI_API_KEY` is not set. Copy `.env.example` to `.env` and add your key "
            "from https://aistudio.google.com/app/apikey."
        )
        st.stop()

    history: list[dict[str, str]] = st.session_state.setdefault("history", [])

    for msg in history:
        with st.chat_message(msg["role"], avatar="🐱" if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    prompt = st.chat_input("e.g. Remote work is better than working in an office")
    if not prompt:
        return

    history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🐱"):
        with st.spinner("Neko is preparing a rebuttal..."):
            try:
                reply = generate_reply(get_client(api_key), model, history)
            except Exception as exc:  # noqa: BLE001 - surface API errors in the UI
                history.pop()
                st.error(f"Gemini request failed: {exc}")
                return
        st.markdown(reply)
        if speak:
            audio = synthesize_speech(reply)
            if audio:
                st.audio(audio, format="audio/wav")
            else:
                st.caption("Text-to-speech is unavailable on this machine.")

    history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
