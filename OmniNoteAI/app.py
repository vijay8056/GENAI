import streamlit as st
from processor import OmniProcessor
import os
import time

# Page Config
st.set_page_config(page_title="OmniNote AI", page_icon="🌐", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #2e7bcf; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #1a5fb4; }
    .sidebar .sidebar-content { background-color: #262730; }
    .recording-dot { height: 12px; width: 12px; background-color: #ff4b4b; border-radius: 50%; display: inline-block; margin-right: 8px; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .card { padding: 20px; border-radius: 15px; background: #1e1e1e; border: 1px solid #333; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Session State
if 'transcript' not in st.session_state: st.session_state.transcript = []
if 'processed_note' not in st.session_state: st.session_state.processed_note = ""
if 'listening' not in st.session_state: st.session_state.listening = False

@st.cache_resource
def get_processor():
    return OmniProcessor()

processor = get_processor()

st.title("🌐 OmniNote AI")
st.caption("All-in-one Voice Intelligence Platform")

# Tabs
tab1, tab2 = st.tabs(["🎤 Create Notes", "📁 Audio Vault"])

# TAB 1: Transcription & AI
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Recording Controls")
        if not st.session_state.listening:
            if st.button("🔴 Start Listening"):
                st.session_state.listening = True
                st.rerun()
        else:
            if st.button("⏹️ Stop Listening"):
                st.session_state.listening = False
                st.rerun()

        if st.session_state.listening:
            st.markdown('<div class="recording-dot"></div> Listening...', unsafe_allow_html=True)
            text = processor.listen(timeout=2, phrase_time_limit=5)
            if text and not text.startswith("Error"):
                st.session_state.transcript.append(text)
                st.rerun()
            elif text.startswith("Error"):
                st.error(text)
                st.session_state.listening = False
                st.rerun()
            else:
                time.sleep(0.1)
                st.rerun()

        st.markdown("---")
        st.write("Current Session Feed:")
        st.text_area("Live Feed", value="\n".join(st.session_state.transcript), height=300, disabled=True)

        if st.button("💾 Generate & Save AI Note"):
            if st.session_state.transcript:
                with st.spinner("Gemini is processing..."):
                    raw_text = " ".join(st.session_state.transcript)
                    processed = processor.process_with_ai(raw_text)
                    st.session_state.processed_note = processed
                    fn = processor.save_markdown(processed)
                    st.success(f"Saved: {fn}")
            else:
                st.warning("Nothing to process!")

    with col2:
        st.subheader("✨ AI Enhanced Result")
        if st.session_state.processed_note:
            st.markdown(f'<div class="card">{st.session_state.processed_note}</div>', unsafe_allow_html=True)
        else:
            st.info("Your AI-enhanced notes will appear here.")

# TAB 2: Reader & Export
with tab2:
    st.subheader("Browse Your Notes")
    if os.path.exists("notes"):
        all_notes = sorted(os.listdir("notes"), reverse=True)
        if not all_notes:
            st.info("No notes found in the vault yet.")
        else:
            selected_fn = st.selectbox("Select a note to read:", all_notes)
            
            with open(f"notes/{selected_fn}", "r", encoding="utf-8") as f:
                note_content = f.read()

            st.markdown(f'<div class="card">{note_content}</div>', unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🔊 Play (British Female Voice)"):
                    with st.spinner("Speaking..."):
                        processor.speak(note_content)
            with c2:
                if st.button("💾 Export to MP3"):
                    with st.spinner("Exporting..."):
                        mp3_fn = processor.export_audio(note_content, base_name=selected_fn.split(".")[0])
                        st.success(f"Exported: {mp3_fn}")
            with c3:
                st.download_button("📥 Download MD File", data=note_content, file_name=selected_fn)
    else:
        st.info("Notes folder not found.")

# Sidebar Stats
st.sidebar.title("OmniStats")
st.sidebar.metric("Notes Captured", len(os.listdir("notes")) if os.path.exists("notes") else 0)
st.sidebar.metric("Audio Exports", len(os.listdir("audio_exports")) if os.path.exists("audio_exports") else 0)
if st.sidebar.button("🗑️ Clear Live Session"):
    st.session_state.transcript = []
    st.session_state.processed_note = ""
    st.rerun()
