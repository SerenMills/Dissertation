"""Streamlit app for the Soteria Framework.

This file handles the main user interface, including:
- letting the user pick a task and prompting strategy
- sending prompts to the model
- displaying outputs and scores
- storing results so they can be compared or downloaded
"""
import streamlit as st
import pandas as pd

from gemini_client import generate_code, get_default_api_key
from prompt_templates import (
    build_baseline_prompt,
    build_constraint_prompt,
    build_role_prompt,
)
from evaluator import evaluate_response
from tasks import TASKS

# General guidance used for building this app:
# Streamlit docs (UI + layout): https://docs.streamlit.io/
# Pandas docs (data handling): https://pandas.pydata.org/docs/
# Python docs (general syntax & structures): https://docs.python.org/3/

# Set up the page layout before anything is rendered.
st.set_page_config(page_title="Soteria Framework", layout="wide")

# Based on Streamlit layout setup examples
# https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config

st.title("Soteria Framework")
st.subheader("Evaluating Prompt Engineering Strategies for Responsible AI-Generated Code")

# Explanation so users know what the tool is doing.
with st.expander("About this tool"):
    st.write(
        """
        This system evaluates prompt engineering strategies by:
        - generating code using different prompt structures
        - parsing structured outputs (code, explanation, assumptions, limitations, and tests)
        - scoring them using a predefined rubric across security, transparency, and test quality

        It is designed to support comparative analysis of responsible AI-generated code.
        """
    )

# Using Streamlit session state to persist data between reruns
# https://docs.streamlit.io/develop/api-reference/session-state

# Keep track of previous runs while the app is open
# users can compare results without saving anything to disk
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar pattern taken from Streamlit UI design patterns
# https://docs.streamlit.io/develop/api-reference/layout/st.sidebar

# Sidebar = where the user controls the experiment setup
st.sidebar.header("Configuration")

# Environment variable handling inspired by common Python practices
# https://docs.python.org/3/library/os.html#os.environ

# Demo mode uses fixed outputs, live mode actually calls the API
mode = st.sidebar.radio("Select mode", ["Demo mode", "Live mode"])

# Try to load an API key from env/secrets if one exists
default_api_key = get_default_api_key()
entered_api_key = None

if mode == "Live mode":
    # Let the user enter their own key instead of hardcoding one
    st.sidebar.markdown("### API Key")
    entered_api_key = st.sidebar.text_input(
        "Enter API key",
        type="password",
        help="Your key is used only for the current session.",
    )

# Dropdown UI element based on Streamlit selectbox component
# https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox

# User picks which coding task to run
selected_task_name = st.sidebar.selectbox("Select coding task", list(TASKS.keys()))

# User picks how the prompt is structured
selected_strategy = st.sidebar.selectbox(
    "Select prompting strategy",
    ["Baseline", "Constraint-Based", "Role-Based"],
)

# Button interaction pattern from Streamlit widgets documentation
# https://docs.streamlit.io/develop/api-reference/widgets/st.button

# Buttons for either running one strategy or comparing all of them
run_single = st.sidebar.button("Generate Single Response")
run_all = st.sidebar.button("Run All Strategies")

# Get the actual task text from the dictionary
task_text = TASKS[selected_task_name]

if mode == "Demo mode":
    st.info("Running in DEMO MODE — using fixed strategy-specific sample outputs and no API calls.")
else:
    if entered_api_key:
        st.success("Running in LIVE MODE — using manually entered API key.")
    elif default_api_key:
        st.success("Running in LIVE MODE — using default API key from .env or Streamlit secrets.")
    else:
        st.warning("Live mode selected, but no API key was found. The app will fall back to demo behaviour.")



# Simple strategy pattern for switching behaviour
# https://refactoring.guru/design-patterns/strategy
def build_prompt(strategy, task):
    """Return the correct prompt template depending on the strategy."""
    if strategy == "Baseline":
        return build_baseline_prompt(task)
    elif strategy == "Constraint-Based":
        return build_constraint_prompt(task)
    else:
        return build_role_prompt(task)


# Pipeline-style function combining multiple steps (prompt → model → evaluation)
# Inspired by typical data processing pipelines in Python
def run_generation(strategy):
    """Run the full pipeline for one strategy (prompt → model → evaluation)."""
    # Build the prompt depending on the chosen strategy
    prompt = build_prompt(strategy, task_text)

    if mode == "Demo mode":
        # In demo mode, skip API calls and return fixed outputs
        response = generate_code(prompt, strategy, api_key=None)
    else:
        # Use entered key if available, otherwise fall back to default
        active_key = entered_api_key if entered_api_key else default_api_key
        response = generate_code(prompt, strategy, api_key=active_key)

    # Score the output using the rubric (rule-based evaluation inspired by heuristic approaches)
    # https://en.wikipedia.org/wiki/Heuristic_(computer_science)
    results = evaluate_response(response)

    # Store everything needed for display + later comparison
    result = {
        "Strategy": strategy,
        "Task": selected_task_name,
        "Security": results["scores"]["security"]["total"],
        "Transparency": results["scores"]["transparency"]["total"],
        "Test Quality": results["scores"]["test_quality"]["total"],
        "Overall": results["scores"]["overall_total"],
        "parsed": results["parsed_sections"],
        "scores": results["scores"],
        "prompt": prompt,
    }

    return result



# Show results for one strategy
if run_single:
    result = run_generation(selected_strategy)

    # Save this run so it shows up in the dataset below
    st.session_state.history.append(result)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"## Model Output: {selected_strategy}")

        st.markdown("### Code")
        st.code(result["parsed"].get("CODE", ""), language="python")

        st.markdown("### Explanation")
        st.write(result["parsed"].get("EXPLANATION", ""))

        st.markdown("### Assumptions")
        st.write(result["parsed"].get("ASSUMPTIONS", ""))

        st.markdown("### Limitations")
        st.write(result["parsed"].get("LIMITATIONS", ""))

        st.markdown("### Tests")
        st.code(result["parsed"].get("TESTS", ""), language="python")

    with col2:
        st.markdown("## Evaluation Results")
        st.metric("Security", result["Security"])
        st.metric("Transparency", result["Transparency"])
        st.metric("Test Quality", result["Test Quality"])
        st.metric("Overall", result["Overall"])

        st.markdown("### Security Breakdown")
        st.json(result["scores"]["security"])

        st.markdown("### Transparency Breakdown")
        st.json(result["scores"]["transparency"])

        st.markdown("### Test Quality Breakdown")
        st.json(result["scores"]["test_quality"])

    with st.expander("Show Full Prompt"):
        st.text(result["prompt"])



# Run the same task across all strategies for comparison
if run_all:
    st.markdown("# Strategy Comparison")

    strategies = ["Baseline", "Constraint-Based", "Role-Based"]
    # Run each strategy on the same task
    results = [run_generation(s) for s in strategies]

    # Save all results so they can be downloaded later
    st.session_state.history.extend(results)

    # Using pandas DataFrame for structured comparison of results
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
    df = pd.DataFrame([
        {
            "Strategy": r["Strategy"],
            "Task": r["Task"],
            "Security": r["Security"],
            "Transparency": r["Transparency"],
            "Test Quality": r["Test Quality"],
            "Overall": r["Overall"],
        }
        for r in results
    ])

    st.markdown("## Key Insight")
    # Find which strategy performed best
    best = df.sort_values("Overall", ascending=False).iloc[0]
    st.success(
        f"Best performing strategy: **{best['Strategy']}** "
        f"(Overall score: {best['Overall']})"
    )

    st.markdown("## Score Comparison")
    st.dataframe(df, use_container_width=True)

    st.markdown("## Score Visualisation")
    # Format data so it works nicely in the chart
    chart_df = df.set_index("Strategy")[["Security", "Transparency", "Test Quality", "Overall"]]
    chart_df.columns = [
        "Security Score",
        "Transparency Score",
        "Test Quality Score",
        "Overall Score",
    ]
    # Simple built-in visualisation using Streamlit chart API
    # https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart
    st.bar_chart(chart_df)

    st.markdown("## Strategy Comparison Insights")
    st.write(
        """
        - Baseline prompting provides a useful reference point, but usually offers the weakest control over responsibility criteria.
        - Constraint-based prompting tends to improve compliance with explicit requirements such as validation and testing.
        - Role-based prompting often produces the strongest overall responses because it frames the model as a security-conscious agent rather than only imposing rules.
        """
    )

    st.markdown("## Detailed Outputs")
    for r in results:
        with st.expander(f"{r['Strategy']} Output"):
            st.markdown("### Code")
            st.code(r["parsed"].get("CODE", ""), language="python")

            st.markdown("### Explanation")
            st.write(r["parsed"].get("EXPLANATION", ""))

            st.markdown("### Assumptions")
            st.write(r["parsed"].get("ASSUMPTIONS", ""))

            st.markdown("### Limitations")
            st.write(r["parsed"].get("LIMITATIONS", ""))

            st.markdown("### Tests")
            st.code(r["parsed"].get("TESTS", ""), language="python")

            st.markdown("### Scores")
            st.json(r["scores"])

            with st.expander(f"Show {r['Strategy']} Prompt"):
                st.text(r["prompt"])


# 
# Show all previous runs and allow download
if st.session_state.history:
    st.markdown("# Experimental Dataset")

    # Build a clean table of results
    history_df = pd.DataFrame([
        {
            "Task": r["Task"],
            "Strategy": r["Strategy"],
            "Security": r["Security"],
            "Transparency": r["Transparency"],
            "Test Quality": r["Test Quality"],
            "Overall": r["Overall"],
        }
        for r in st.session_state.history
    ])

    st.dataframe(history_df, use_container_width=True)

    # Convert results to CSV for download (common data export pattern in pandas)
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
    csv = history_df.to_csv(index=False).encode("utf-8")

    col_download, col_clear = st.columns([1, 1])

    with col_download:
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="experiment_results.csv",
            mime="text/csv",
        )

    with col_clear:
        if st.button("Clear History"):
            # Clear stored results and refresh the app
            st.session_state.history = []
            st.rerun()



# Default message before anything is run
if not run_single and not run_all:
    st.info("Select a task and run a strategy or compare all.")