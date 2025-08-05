import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}

# You can change this model if you want better results
HF_MODEL = "google/flan-ul2"

def get_hf_answer(user_prompt: str) -> str:
    if not HF_API_KEY:
        return "⚠️ Hugging Face API key missing. Please set it in your .env file."

    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    payload = {
        "inputs": user_prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        if resp.status_code == 503:
            return "Model is loading, please try again in a few seconds."
        if resp.status_code != 200:
            return f"Hugging Face API error {resp.status_code}: {resp.text}"
        data = resp.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        return str(data)
    except Exception as e:
        return f"Exception calling Hugging Face: {e}"
