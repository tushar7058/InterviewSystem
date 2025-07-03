import os
import requests
from dotenv import load_dotenv

class GeminiLLM:
    def __init__(self, api_key=None, model="models/gemini-pro"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "AIzaSyDNQ96yuN3wOjj8HZLPLEBP0InRiYQWM4M")
        self.model = model
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:generateContent?key={self.api_key}"

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
            except Exception:
                return result
        else:
            return f"Error: {response.status_code} {response.text}"

# Example usage:
gemini = GeminiLLM(api_key="AIzaSyDNQ96yuN3wOjj8HZLPLEBP0InRiYQWM4M")
print(gemini.generate("Ask the first interview question."))
