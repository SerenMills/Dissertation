import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("API_KEY")


DEMO_RESPONSE = """
[CODE]
import re

def validate_password(password: str) -> bool:
    \"\"\"Validate a password against simple security rules.\"\"\"
    if not isinstance(password, str):
        return False

    password = password.strip()

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    return True

[EXPLANATION]
This solution checks that the input is a string before applying validation rules.
It then verifies length and basic character requirements using regular expressions.

[ASSUMPTIONS]
- The password is provided as a plain Python string.
- Special character requirements are not mandatory for this version.

[LIMITATIONS]
- This function does not check against breached-password lists.
- It does not enforce special characters or prevent repeated characters.

[TESTS]
def test_valid_password():
    assert validate_password("Secure123") is True

def test_short_password():
    assert validate_password("Abc12") is False

def test_missing_number():
    assert validate_password("Password") is False

def test_invalid_type():
    assert validate_password(None) is False
""".strip()


def generate_code(prompt: str) -> str:
    """
    Generate code from Gemini if an API key is available.
    Otherwise, return a deterministic demo response.
    """
    if not API_KEY:
        return DEMO_RESPONSE

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    return response.text