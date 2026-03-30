def build_baseline_prompt(task: str) -> str:
    return task

def build_constraint_prompt(task: str) -> str:
    return f"""
Write clean, readable Python code for the following task:

{task}

Avoid common security vulnerabilities.
Validate all inputs.
Use safe error handling.
Do not hardcode secrets.
Include tests for valid, invalid, and edge-case inputs.
Briefly explain any assumptions.
""".strip()

def build_role_prompt(task: str) -> str:
    return f"""
You are a security-conscious Python software engineer who prioritises secure, transparent, and well-tested code.

Write clean, readable Python code for the following task:

{task}
""".strip()