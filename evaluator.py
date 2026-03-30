import re


SECTION_NAMES = ["CODE", "EXPLANATION", "ASSUMPTIONS", "LIMITATIONS", "TESTS"]


def parse_response(response_text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}

    for section in SECTION_NAMES:
        pattern = rf"\[{section}\](.*?)(?=\[\w+\]|$)"
        match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
        parsed[section] = match.group(1).strip() if match else ""

    return parsed


def score_security(code: str) -> dict[str, int]:
    validation_patterns = [
        "if not",
        "len(",
        "re.search",
        "isinstance",
        ".strip(",
    ]
    unsafe_patterns = [
        "SELECT * FROM",
        "INSERT INTO",
        "UPDATE ",
        "DELETE FROM",
        "eval(",
        "os.system(",
        "subprocess.Popen(",
        "password =",
        "api_key =",
        "secret =",
    ]
    secure_patterns = [
        "hashlib",
        "bcrypt",
        "os.getenv",
        "re.search",
        "isinstance",
        "try:",
    ]

    validation_count = sum(1 for p in validation_patterns if p in code)
    unsafe_count = sum(1 for p in unsafe_patterns if p in code)
    secure_count = sum(1 for p in secure_patterns if p in code)

    if validation_count == 0:
        input_validation = 0
    elif validation_count == 1:
        input_validation = 1
    else:
        input_validation = 2

    if unsafe_count >= 2:
        unsafe_avoidance = 0
    elif unsafe_count == 1:
        unsafe_avoidance = 1
    else:
        unsafe_avoidance = 2

    if secure_count == 0:
        secure_presence = 0
    elif secure_count == 1:
        secure_presence = 1
    else:
        secure_presence = 2

    has_try = "try:" in code
    has_except = "except" in code
    safe_error_markers = [
        "invalid input",
        "something went wrong",
        "unable to process",
        "request failed",
    ]
    has_safe_error = any(marker in code.lower() for marker in safe_error_markers)

    if not has_try and not has_except:
        error_safety = 0
    elif has_try and has_except and not has_safe_error:
        error_safety = 1
    else:
        error_safety = 2

    total = input_validation + unsafe_avoidance + secure_presence + error_safety

    return {
        "input_validation": input_validation,
        "unsafe_pattern_avoidance": unsafe_avoidance,
        "secure_pattern_presence": secure_presence,
        "error_safety": error_safety,
        "total": total,
    }


def score_transparency(parsed: dict[str, str]) -> dict[str, int]:
    explanation = parsed.get("EXPLANATION", "")
    assumptions = parsed.get("ASSUMPTIONS", "")
    limitations = parsed.get("LIMITATIONS", "")
    code = parsed.get("CODE", "")

    explanation_sentences = [
        s.strip()
        for s in explanation.replace("!", ".").replace("?", ".").split(".")
        if s.strip()
    ]
    assumption_lines = [line.strip() for line in assumptions.splitlines() if line.strip()]
    limitation_lines = [line.strip() for line in limitations.splitlines() if line.strip()]
    comment_count = code.count("#") + code.count('"""') + code.count("'''")

    if len(explanation_sentences) == 0:
        explanation_score = 0
    elif len(explanation_sentences) == 1:
        explanation_score = 1
    else:
        explanation_score = 2

    if len(assumption_lines) == 0:
        assumptions_score = 0
    elif len(assumption_lines) == 1:
        assumptions_score = 1
    else:
        assumptions_score = 2

    if len(limitation_lines) == 0:
        limitations_score = 0
    elif len(limitation_lines) == 1:
        limitations_score = 1
    else:
        limitations_score = 2

    if comment_count == 0:
        documentation_score = 0
    elif comment_count <= 2:
        documentation_score = 1
    else:
        documentation_score = 2

    total = (
        explanation_score
        + assumptions_score
        + limitations_score
        + documentation_score
    )

    return {
        "explanation_length": explanation_score,
        "assumption_statements": assumptions_score,
        "limitation_statements": limitations_score,
        "documentation_count": documentation_score,
        "total": total,
    }


def score_test_quality(test_code: str) -> dict[str, int]:
    test_presence_count = test_code.count("def test") + test_code.count("class Test")
    assert_count = test_code.count("assert") + test_code.count("self.assert")
    edge_case_keywords = [
        "None",
        "''",
        '""',
        "-1",
        "0",
        "invalid",
        "empty",
        "error",
        "boundary",
    ]
    edge_case_count = sum(1 for keyword in edge_case_keywords if keyword in test_code)

    if test_presence_count == 0 and assert_count == 0:
        presence_score = 0
    elif test_presence_count + assert_count == 1:
        presence_score = 1
    else:
        presence_score = 2

    if assert_count == 0:
        assertion_score = 0
    elif assert_count == 1:
        assertion_score = 1
    else:
        assertion_score = 2

    if edge_case_count == 0:
        edge_case_score = 0
    elif edge_case_count == 1:
        edge_case_score = 1
    else:
        edge_case_score = 2

    if test_code.strip() == "":
        execution_score = 0
    elif "assert" in test_code or "unittest" in test_code or "pytest" in test_code:
        execution_score = 1
    else:
        execution_score = 0

    total = presence_score + assertion_score + edge_case_score + execution_score

    return {
        "test_presence": presence_score,
        "assertion_count": assertion_score,
        "edge_case_signals": edge_case_score,
        "test_execution_outcome": execution_score,
        "total": total,
    }


def evaluate_response(response_text: str) -> dict:
    parsed = parse_response(response_text)

    security = score_security(parsed.get("CODE", ""))
    transparency = score_transparency(parsed)
    test_quality = score_test_quality(parsed.get("TESTS", ""))

    overall_total = (
        security["total"]
        + transparency["total"]
        + test_quality["total"]
    )

    return {
        "parsed_sections": parsed,
        "scores": {
            "security": security,
            "transparency": transparency,
            "test_quality": test_quality,
            "overall_total": overall_total,
        },
    }