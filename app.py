from gemini_client import generate_code
from prompt_templates import (
    build_baseline_prompt,
    build_constraint_prompt,
    build_role_prompt,
)
from evaluator import evaluate_response


TASK = "Write a Python function that validates a password."


def run_strategy(name: str, prompt: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"STRATEGY: {name}")
    print(f"{'=' * 70}\n")

    result = generate_code(prompt)
    scores = evaluate_response(result)

    print("PROMPT:\n")
    print(prompt)
    print("\n" + "-" * 70 + "\n")

    print("MODEL OUTPUT:\n")
    print(result)
    print("\n" + "-" * 70 + "\n")

    print("RUBRIC SCORES:\n")
    print(scores)


if __name__ == "__main__":
    strategies = {
        "Baseline": build_baseline_prompt(TASK),
        "Constraint-Based": build_constraint_prompt(TASK),
        "Role-Based": build_role_prompt(TASK),
    }

    for name, prompt in strategies.items():
        run_strategy(name, prompt)