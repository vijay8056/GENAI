# EchoNote AI: Real-Time Audio Transcription & Summarization

EchoNote AI is an intelligent meeting assistant that listens to your conversations, generates accurate transcripts, and provides AI-powered summaries and formatting.

## Features
- **Live Listening**: Real-time microphone capture and speech-to-text.
- **AI Processing**: Automatic formatting (headers, lists) and summarization using LLMs (OpenAI/Gemini).
- **Persistent Storage**: Save notes locally in Markdown format with a searchable history.
- **Clean UI**: A modern Streamlit-based web interface.

## Quick Start
1.  **Clone the Repo**:
    ```bash
    git clone <your-repo-url>
    cd EchoNoteAI
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Keys**:
    - Rename `.env.example` to `.env`.
    - Add your API keys (OpenAI or Gemini).
4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## Project Structure
- `app.py`: Main Streamlit application and UI logic.
- `processor.py`: Speech processing and AI summarization engine.
- `notes/`: Directory where all generated notes are stored.
- `.env`: (Ignored) Your private API credentials.
