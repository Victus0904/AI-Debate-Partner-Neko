# 🐱 Neko · AI Debate Partner

[![CI](https://github.com/Victus0904/AI-Debate-Partner-Neko/actions/workflows/ci.yml/badge.svg)](https://github.com/Victus0904/AI-Debate-Partner-Neko/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-4285F4)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Streamlit chatbot that **argues the other side**. State a position and Neko, a
sharp, concise debate partner powered by Google Gemini, replies with the strongest
counter-argument and a question that keeps the debate going. Replies can be read
aloud with offline text-to-speech.

## Features

- **Multi-turn debates.** The full conversation is sent to Gemini, so Neko remembers your earlier arguments.
- **Opinionated persona.** The system prompt makes Neko take the opposing stance, cite concrete evidence and stay under four sentences.
- **Voice output.** Optional offline TTS with `pyttsx3`, rendered to an in-browser audio player.
- **Configurable model.** Choose any Gemini model from the sidebar or with `GEMINI_MODEL`.
- **Graceful failures.** Missing keys and API errors are shown in the UI instead of crashing the app.

## Quick start

```bash
git clone https://github.com/Victus0904/AI-Debate-Partner-Neko.git
cd AI-Debate-Partner-Neko
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env        # then paste your key into .env
streamlit run app.py
```

Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | yes | none | Google Gemini API key |
| `GEMINI_MODEL` | no | `gemini-2.5-flash` | Model used for replies |

> **Text-to-speech on Linux** needs eSpeak: `sudo apt-get install espeak-ng`. Windows and macOS use their built-in voices.

## Project structure

```text
.
├── app.py              # Streamlit UI, Gemini calls, TTS
├── tests/test_app.py   # Headless Streamlit smoke tests (no API calls)
├── requirements.txt
└── .env.example
```

## Running the tests

```bash
pip install pytest
pytest -q
```

## Tech stack

Python · Streamlit · Google Gemini (`google-genai`) · pyttsx3

## License

[MIT](LICENSE)
