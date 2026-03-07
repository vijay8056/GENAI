import streamlit as st
from processor import EchoProcessor
import os
import time

# Page Config
st.set_page_config(page_title="EchoNote AI", page_icon="🎤", layout="wide")

# Custom CSS for a modern look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #2e7bcf; color: white; }
    .status-box { padding: 10px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; }
    .recording-dot { height: 10px; width: 10px; background-color: #ff4b4b; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# Session State for tracking notes
if 'transcript' not in st.session_state:
    st.session_state.transcript = []
if 'processed_note' not in st.session_state:
    st.session_state.processed_note = ""
if 'listening' not in st.session_state:
    st.session_state.listening = False

processor = EchoProcessor()

# Sidebar: Note History
st.sidebar.title("📁 Previous Notes")
if os.path.exists("notes"):
    notes = sorted(os.listdir("notes"), reverse=True)
    for note in notes:
        if st.sidebar.button(f"📄 {note}"):
            with open(f"notes/{note}", "r", encoding="utf-8") as f:
                st.session_state.processed_note = f.read()

# Main Header
st.title("🎤 EchoNote AI")
st.caption("Your intelligent voice-to-notes assistant.")

# Layout: Two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Controls")
    
    # Toggle Listening Button
    if not st.session_state.listening:
        if st.button("🔴 Start Listening", key="start_btn"):
            st.session_state.listening = True
            st.rerun()
    else:
        if st.button("⏹️ Stop Listening", key="stop_btn"):
            st.session_state.listening = False
            st.rerun()

    # Listening Loop
    if st.session_state.listening:
        st.markdown('<div class="status-box"><span class="recording-dot"></span> Listening... (Speak now)</div>', unsafe_allow_html=True)
        text = processor.listen(timeout=2, phrase_time_limit=4)
        if text and not text.startswith("Error"):
            st.session_state.transcript.append(text)
            st.rerun() # Refresh to show text immediately
        elif text.startswith("Error"):
            st.error(text)
            st.session_state.listening = False
            st.rerun()
        else:
            # Re-run automatically to keep listening
            time.sleep(0.1)
            st.rerun()

    st.markdown("---")
    st.write("Current Session Transcript:")
    st.text_area("Live Feed", value="\n".join(st.session_state.transcript), height=300, disabled=True)

    if st.button("💾 Generate & Save AI Note"):
        if st.session_state.transcript:
            with st.spinner("Processing with AI..."):
                raw_text = " ".join(st.session_state.transcript)
                processed = processor.process_notes(raw_text)
                st.session_state.processed_note = processed
                filename = processor.save_note(processed)
                st.success(f"Saved to {filename}")
        else:
            st.warning("Nothing to process!")

with col2:
    st.subheader("✨ AI Enhanced Notes")
    if st.session_state.processed_note:
        st.markdown(st.session_state.processed_note)
    else:
        st.info("Your formatted notes will appear here after processing.")

# Clear Session
if st.sidebar.button("🗑️ Clear Session"):
    st.session_state.transcript = []
    st.session_state.processed_note = ""
    st.session_state.listening = False
    st.rerun()
