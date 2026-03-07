import os
import datetime
import speech_recognition as sr
from dotenv import load_dotenv
import google.generativeai as genai
import pyttsx3
import re

# Load environment variables
load_dotenv()

class OmniProcessor:
    def __init__(self):
        # 1. Speech-to-Text Setup
        self.recognizer = sr.Recognizer()
        
        # 2. Gemini AI Setup
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            
        # Paths
        self.notes_dir = "notes"
        self.export_dir = "audio_exports"
        for d in [self.notes_dir, self.export_dir]:
            if not os.path.exists(d): os.makedirs(d)

    def _get_engine(self):
        """Initializes and returns a fresh TTS engine with the correct voice."""
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
        
        voices = engine.getProperty('voices')
        # Try to find a British Female voice
        found_voice = False
        for voice in voices:
            name = voice.name.lower()
            if ('female' in name or 'zira' in name or 'hazel' in name) and ('uk' in name or 'british' in name or 'en-gb' in name):
                engine.setProperty('voice', voice.id)
                found_voice = True
                break
        
        if not found_voice:
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        return engine

    def listen(self, timeout=3, phrase_time_limit=5):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                return self.recognizer.recognize_google(audio)
            except (sr.WaitTimeoutError, sr.UnknownValueError): return ""
            except Exception as e: return f"Error: {str(e)}"

    def process_with_ai(self, raw_transcript):
        if not self.model: return f"Raw Transcript (No AI):\n{raw_transcript}"
        prompt = f"Act as a professional note-taker. Format and summarize this transcript with Markdown headers and bullet points. Include a 'TL;DR' summary.\nTranscript:\n{raw_transcript}"
        try: return self.model.generate_content(prompt).text
        except Exception as e: return f"AI Error: {str(e)}"

    def save_markdown(self, content):
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fn = f"{self.notes_dir}/note_{ts}.md"
        with open(fn, "w", encoding="utf-8") as f: f.write(content)
        return fn

    def clean_text(self, text):
        # Remove headers and stars
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'\*+', '', text)
        return text.replace("- ", "Next point, ")

    def speak(self, text):
        clean = self.clean_text(text)
        engine = self._get_engine()
        engine.say(clean)
        engine.runAndWait()
        # Explicitly stop the engine to release the COM object
        engine.stop()

    def export_audio(self, text, base_name="note"):
        clean = self.clean_text(text)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        export_fn = f"{self.export_dir}/{base_name}_{ts}.mp3"
        engine = self._get_engine()
        engine.save_to_file(clean, export_fn)
        engine.runAndWait()
        engine.stop()
        return export_fn
