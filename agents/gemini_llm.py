import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GeminiLLM:
    def __init__(self, api_key=None, model="gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided and not found in environment variables.")
        # FIXED API URL
        self.model = model
        self.api_url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"

    def generate(self, prompt):
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            try:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                print("Parsing error:", e)
                return result
        else:
            print(f"Error: {response.status_code} {response.text}")
            return None

# Example Usage
gemini = GeminiLLM()
print(gemini.generate("Ask the first interview question."))
