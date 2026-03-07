import os
import pyttsx3
import re
import datetime

class NoteReader:
    def __init__(self, notes_dir="../EchoNoteAI/notes"):
        self.notes_dir = notes_dir
        self.export_dir = "audio_exports"
        # Ensure export directory exists
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
            
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        self.engine.setProperty('volume', 1.0)

    def clean_markdown(self, text):
        """Removes Markdown symbols for natural speech."""
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'\*', '', text)
        text = text.replace("- ", "Next point, ")
        return text

    def list_notes(self):
        """Scans the notes directory and returns a list of files."""
        if not os.path.exists(self.notes_dir):
            # Try a local 'notes' folder if the relative one isn't found
            if os.path.exists("notes"):
                self.notes_dir = "notes"
            else:
                return []
        
        notes = [f for f in os.listdir(self.notes_dir) if f.endswith(".md")]
        return sorted(notes, reverse=True)

    def read_aloud(self, filename):
        """Plays the audio live through speakers."""
        filepath = os.path.join(self.notes_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = self.clean_markdown(f.read())
            print(f"\n🔊 Playing: {filename}...")
            self.engine.say(content)
            self.engine.runAndWait()

    def save_audio(self, filename):
        """Converts the note into an MP3 file."""
        filepath = os.path.join(self.notes_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = self.clean_markdown(f.read())
            
            # Create a unique filename for the export
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(filename)[0]
            export_filename = f"{base_name}_{timestamp}.mp3"
            export_path = os.path.join(self.export_dir, export_filename)
            
            print(f"\n💾 Exporting to: {export_path}...")
            self.engine.save_to_file(content, export_path)
            self.engine.runAndWait()
            print("✅ Export Complete!")
            return export_path

def main():
    reader = NoteReader()
    notes = reader.list_notes()

    if not notes:
        print("No notes found! Make sure EchoNoteAI has some saved notes.")
        return

    print("\n📜 NoteReaderAI: Voice & Export Menu")
    for i, note in enumerate(notes):
        print(f"{i+1}. {note}")

    choice = input("\nSelect note number (or 'q' to quit): ")
    if choice.isdigit() and 1 <= int(choice) <= len(notes):
        selected_note = notes[int(choice)-1]
        
        print("\nWhat would you like to do?")
        print("1. Listen Live (Speakers)")
        print("2. Save as MP3 Audio File")
        
        action = input("\nEnter choice (1 or 2): ")
        if action == "1":
            reader.read_aloud(selected_note)
        elif action == "2":
            reader.save_audio(selected_note)
        else:
            print("Invalid action.")
    elif choice.lower() == 'q':
        print("Goodbye!")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
