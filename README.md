# Dissertation
# Soteria Framework

Soteria is a Streamlit-based research artefact designed to evaluate how different prompt engineering strategies influence the generation of responsible AI-produced code.

The system compares three prompting strategies:

- Baseline prompting
- Constraint-based prompting
- Role-based prompting

It then evaluates the generated outputs using the **Soteria rubric**, which scores responsibility across three dimensions:

- Security
- Transparency
- Test Quality

---

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

 Use **Demo mode** if you don’t have an API key.

---

## What This Project Does

This project was developed as part of a dissertation exploring whether prompt engineering can be used to improve the responsibility of AI-generated code.

The system allows you to:

- select a coding task
- choose a prompting strategy
- generate code
- automatically evaluate the output
- compare strategies side by side
- export results as CSV

---

## Project Structure

```
Artefact/
├── app.py
├── gemini_client.py
├── prompt_templates.py
├── evaluator.py
├── tasks.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Installation

### 1. Download the project

Either clone the repo:

```bash
git clone https://github.com/SerenMills/Dissertation
cd Dissertation
```

Or download as a ZIP and extract.

---

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
streamlit run app.py
```

---

## API Key Setup (Optional)

You only need this for **Live mode**.
Register for free google gemini account : https://ai.google.dev/gemini-api/docs
Click API keys on the side bar when loaded into dashboard, then create/view api keys. 
You will be able to create an API key for free without needing to attatch a card. Do not share this key with anyone. 

### Option 1 – Demo Mode (Recommended for marking)

No API key needed. The app uses fixed outputs.

### Option 2 – `.env` file

Create a file called `.env` in the project folder:

```env
API_KEY=your_api_key_here
```

### Option 3 – Enter in app

You can paste your key directly into the sidebar when using Live mode.

---

## How to Use

1. Open the app
2. Select Demo or Live mode
3. Choose a task
4. Choose a prompting strategy
5. Click:
   - **Generate Single Response**, or
   - **Run All Strategies**
6. View:
   - generated code
   - explanations
   - scores
   - comparison chart

---

## Evaluation (Soteria Rubric)

The system evaluates outputs across three dimensions:

- Security (max 8)
- Transparency (max 8)
- Test Quality (max 7)

Total possible score: **23**

The evaluator uses a rule-based approach, looking for patterns such as:

- input validation
- unsafe coding practices
- explanations and assumptions
- presence of tests

This makes scoring consistent and reproducible, but does not capture full semantic correctness.

---

## Notes for Markers

- The system is fully usable in Demo mode (no API required)
- Live mode is optional and requires an API key
- All tasks, prompts, and scoring are predefined for consistency

---

## Troubleshooting

### Streamlit not found

```bash
python -m streamlit run app.py
```

### Missing modules

```bash
pip install -r requirements.txt
```

### No API key

Use Demo mode or add a `.env` file

---

## Limitations

- Evaluation is heuristic (pattern-based)
- Does not fully understand code semantics
- Limited task set
- API usage may be rate-limited

---

## Author

Seren Mills  
Dissertation Artefact – Soteria Framework

---

## Licence

This project is intended for academic submission and evaluation. 
This REPO will be removed once the submission is graded and marked