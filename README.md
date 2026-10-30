# Sentinel Password Intelligence

A professional, privacy-first password-strength analyzer built with **Python, Streamlit, security heuristics, entropy estimation, and a Random Forest ML classifier**.

## Features
- Password strength score (0–100) and five strength levels
- Entropy estimate and character-class analysis
- Detection of common passwords, repeated characters, and predictable sequences
- Random Forest ML classification with confidence
- Explainable recommendations and score breakdown
- Password input is masked by default; the app does not intentionally save or transmit submitted passwords

## Important ML limitation
The included model is bootstrapped using **synthetic educational data** whose labels are generated from transparent heuristics. This demonstrates a complete ML workflow (feature engineering, training, inference, probability output), but it is not a model trained on a representative real-world password dataset and must not be treated as a production security verdict. For research-grade evaluation, replace the synthetic training generator with a legally obtained, ethically handled, properly labeled dataset and report precision, recall, F1, confusion matrix, and dataset limitations.

## Run locally
Python 3.10+ recommended.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the application
streamlit run app.py
```

The app trains and saves `password_model.joblib` automatically on first run. To train it separately:

```bash
python train_model.py
```

## Project structure
```text
password_strength_analyzer/
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
├── password_model.joblib   # generated on first run
└── src/
    ├── __init__.py
    └── analyzer.py
```

## Architecture
1. **Input layer:** masked password entry in Streamlit.
2. **Feature engineering:** length, character classes, uniqueness ratio, repeated runs, sequences, common-password match, estimated entropy.
3. **Security engine:** deterministic scoring and risk checks.
4. **ML engine:** Random Forest predicts a strength class and confidence.
5. **Guidance layer:** creates recommendations from detected weaknesses.
6. **Presentation:** dashboard with score, analysis, recommendations, and chart.

## Security and privacy notes
- Use only sample/test passwords when demonstrating this academic project.
- Do not add password logging, analytics capture, or cloud transmission.
- Do not store plaintext passwords.
- This is an educational estimator, not a guarantee against cracking or a replacement for MFA and a password manager.
