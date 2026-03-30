from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

def generate_code(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )
    return response.text
    