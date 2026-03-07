import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in environment.")
else:
    print(f"API Key found (starts with: {api_key[:5]}...)")
    client = genai.Client(api_key=api_key)

    print("\nAvailable Chat Models (for generateContent):")
    try:
        for model in client.models.list():
            actions = getattr(model, 'supported_actions', [])
            if 'generateContent' in actions:
                print(f"- {model.name} (Display: {model.display_name})")
    except Exception as e:
        print(f"Error listing models: {e}")
