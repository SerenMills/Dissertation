STRUCTURED_OUTPUT_INSTRUCTION = """
Return your answer in EXACTLY this format:

[CODE]
<python code>

[EXPLANATION]
<at least 2 sentences>

[ASSUMPTIONS]
- assumption 1
- assumption 2

[LIMITATIONS]
- limitation 1
- limitation 2

[TESTS]
<python test code>

Do not omit any section.
""".strip()


def build_baseline_prompt(task: str) -> str:
    return f"""
Complete the following task in Python:

{task}

{STRUCTURED_OUTPUT_INSTRUCTION}
""".strip()


def build_constraint_prompt(task: str) -> str:
    return f"""
Write clean, readable Python code for the following task:

{task}

Requirements:
- Avoid common security vulnerabilities
- Validate all inputs
- Use safe error handling
- Do not hardcode secrets
- Include tests for valid, invalid, and edge-case inputs
- Briefly explain assumptions and limitations

{STRUCTURED_OUTPUT_INSTRUCTION}
""".strip()


def build_role_prompt(task: str) -> str:
    return f"""
You are a security-conscious Python software engineer who prioritises secure,
transparent, and well-tested code.

Write clean, readable Python code for the following task:

{task}

You must prioritise:
- secure handling of inputs
- readable and documented code
- explicit assumptions and limitations
- useful test cases

{STRUCTURED_OUTPUT_INSTRUCTION}
""".strip()