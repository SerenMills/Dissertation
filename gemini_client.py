"""
Handles model access for the Soteria Framework.

This file is responsible for:
- loading an API key if one is available
- returning demo outputs when no key is present
- sending prompts to the Gemini API in live mode
"""
import os

from dotenv import load_dotenv
import streamlit as st
from google import genai
from streamlit.errors import StreamlitSecretNotFoundError

# Main guidance used cited here instead of throughout: 
# python-dotenv docs: https://pypi.org/project/python-dotenv/
# Streamlit secrets docs: https://docs.streamlit.io/develop/concepts/connections/secrets-management
# Google Gen AI Python SDK docs: https://googleapis.github.io/python-genai/

# Load local environment variables so the app can pick up an API key during development.
load_dotenv()


def get_default_api_key() -> str | None:
    """Try Streamlit secrets first, then fall back to a local .env value."""
    # Streamlit secrets are useful when the app is deployed online.
    try:
        if "API_KEY" in st.secrets:
            return st.secrets["API_KEY"]
    except StreamlitSecretNotFoundError:
        pass

    # If no Streamlit secret exists, use the local environment variable instead.
    return os.getenv("API_KEY")


def demo_response_for_strategy(strategy: str) -> str:
    """Return a fixed demo response so the system still works without live API access."""
    # These fixed outputs make the UI and rubric testable even without external model calls.
    if strategy == "Baseline":
        return """
[CODE]
def validate_password(password):
    return len(password) >= 6

[EXPLANATION]
This implementation provides only a minimal password check.
It accepts any password with a length of at least six characters.

[ASSUMPTIONS]
- The input is always a string.
- A short password length check is sufficient.

[LIMITATIONS]
- No type validation is included.
- No uppercase, lowercase, or numeric checks are performed.

[TESTS]
def test_valid_length():
    assert validate_password("abcdef") is True

def test_short_password():
    assert validate_password("abc") is False
""".strip()

    elif strategy == "Constraint-Based":
        return """
[CODE]
import re

def validate_password(password):
    if not isinstance(password, str):
        return False

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    return True

[EXPLANATION]
This version adds explicit constraints to improve password validation.
It checks input type, minimum length, uppercase presence, and numeric characters.

[ASSUMPTIONS]
- Passwords are provided as Python strings.
- Only uppercase and numeric checks are required for this task.

[LIMITATIONS]
- It does not require lowercase or special characters.
- It does not check for breached or reused passwords.

[TESTS]
def test_valid_password():
    assert validate_password("Password1") is True

def test_missing_number():
    assert validate_password("Password") is False

def test_invalid_type():
    assert validate_password(None) is False
""".strip()

    else:  # Role-based version
        return """
[CODE]
import re

def validate_password(password: str) -> bool:
    \"\"\"Validate a password against basic security rules.\"\"\"
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
This implementation follows a more security-conscious approach to password validation.
It first verifies that the input is a string, strips surrounding whitespace, and then checks length, uppercase, lowercase, and numeric requirements.

[ASSUMPTIONS]
- The password is provided as a plain Python string.
- Basic character-class validation is sufficient for this stage of the system.

[LIMITATIONS]
- It does not check against breached-password databases.
- It does not require special characters or prevent common password reuse.

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


# simple wrapper keeps API handling separate from the UI code.
# makes the project easier to test and change later.
def generate_code(prompt: str, strategy: str, api_key: str | None = None) -> str:
    """Generate a live response when possible, otherwise fall back to demo mode."""
    # Prefer a manually supplied key, but fall back to the default loader if needed.
    active_key = api_key or get_default_api_key()

    # If no key is available at all, return a fixed demo response instead of failing.
    if not active_key:
        return demo_response_for_strategy(strategy)

    # Create the Gemini client only when live generation is actually possible.
    client = genai.Client(api_key=active_key)

    # Send the built prompt to the model and return the text output.
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    return response.text