from gemini_client import generate_code
from prompt_templates import build_constraint_prompt

task = "Write a Python function that validates a password."
prompt = build_constraint_prompt(task)

result = generate_code(prompt)

print("FINAL PROMPT:\n")
print(prompt)
print("\n" + "=" * 50 + "\n")
print("GEMINI OUTPUT:\n")
print(result)