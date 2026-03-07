import os
import datetime
import speech_recognition as sr
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class EchoProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use gemini-1.5-flash which is widely supported
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def listen(self, timeout=3, phrase_time_limit=5):
        """Captures audio from the microphone and transcribes it."""
        with sr.Microphone() as source:
            # Short ambient noise adjustment for faster start
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # Use shorter chunks for continuous feel
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = self.recognizer.recognize_google(audio)
                return text
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return ""
            except Exception as e:
                return f"Error: {str(e)}"

    def process_notes(self, raw_transcript):
        """Summarizes and formats the transcript using AI."""
        if not self.model:
            return f"Raw Transcript (No AI configured):\n{raw_transcript}"

        prompt = f"""
        Act as a professional note-taker. 
        Format and summarize the following raw speech transcript.
        Use Markdown headers, bullet points, and a 'TL;DR' summary at the end.
        
        Raw Transcript:
        {raw_transcript}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Error: {str(e)}\n\nOriginal Text: {raw_transcript}"

    def save_note(self, content):
        """Saves the note as a local Markdown file."""
        if not os.path.exists("notes"):
            os.makedirs("notes")
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"notes/note_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return filename
