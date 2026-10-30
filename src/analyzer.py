import math
import re
import string
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = Path(__file__).resolve().parent.parent / "password_model.joblib"
LABELS = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]

COMMON = {
    "password","password1","123456","12345678","qwerty","admin","letmein",
    "welcome","iloveyou","abc123","monkey","dragon","football"," sunshine"
}
SEQUENCES = ["1234","abcd","qwerty","asdf","zxcv","9876","1111","0000"]

def features(password: str):
    p = password or ""
    n = len(p)
    lower = any(c.islower() for c in p)
    upper = any(c.isupper() for c in p)
    digit = any(c.isdigit() for c in p)
    special = any(not c.isalnum() for c in p)
    unique_ratio = len(set(p))/max(n,1)
    repeats = bool(re.search(r"(.)\1{2,}", p))
    sequence = any(s in p.lower() for s in SEQUENCES)
    common = p.lower() in COMMON
    classes = sum([lower,upper,digit,special])
    pool = (26 if lower else 0)+(26 if upper else 0)+(10 if digit else 0)+(33 if special else 0)
    entropy = n * math.log2(pool) if pool else 0
    return np.array([n, classes, int(lower), int(upper), int(digit), int(special),
                     unique_ratio, int(repeats), int(sequence), int(common), entropy], dtype=float)

def _synthetic_training_data():
    # Educational bootstrap data only. Labels are generated from transparent heuristics,
    # not from real leaked-password corpora.
    rng = np.random.default_rng(42)
    X, y = [], []
    for _ in range(7000):
        n = int(rng.integers(3, 31))
        classes = int(rng.integers(1,5))
        lower, upper, digit, special = [int(i < classes) for i in range(4)]
        rng.shuffle([lower, upper, digit, special])
        pool = (26*lower)+(26*upper)+(10*digit)+(33*special)
        ent = n * math.log2(max(pool,1))
        unique = float(rng.uniform(.35,1))
        repeat = int(rng.random() < .12)
        seq = int(rng.random() < .12)
        common = int(rng.random() < .035)
        row = [n,classes,lower,upper,digit,special,unique,repeat,seq,common,ent]
        score = min(100, max(0, n*2.1 + classes*9 + ent*.35 + unique*9 - repeat*18 - seq*20 - common*55))
        label = 0 if score < 25 else 1 if score < 42 else 2 if score < 62 else 3 if score < 82 else 4
        X.append(row); y.append(label)
    return np.asarray(X), np.asarray(y)

def load_or_train_model():
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH), "Loaded trained Random Forest model"
        except Exception:
            pass
    X,y = _synthetic_training_data()
    model = RandomForestClassifier(n_estimators=180, max_depth=12, random_state=42, class_weight="balanced")
    model.fit(X,y)
    joblib.dump(model, MODEL_PATH)
    return model, "Trained demo Random Forest model (synthetic educational data)"

def analyze_password(password, model):
    p = password or ""
    f = features(p)
    n, classes, lower, upper, digit, special, unique, repeats, sequence, common, entropy = f
    risks = []
    if common: risks.append("Matches a common-password entry.")
    if sequence: risks.append("Contains a predictable sequence.")
    if repeats: risks.append("Contains a character repeated three or more times.")
    if n < 12: risks.append("Shorter than the recommended 12-character minimum.")
    if classes < 3: risks.append("Uses fewer than three character categories.")
    if p.lower() in {"password","admin","qwerty","letmein"}: risks.append("Extremely predictable password choice.")

    checks = {
        f"At least 12 characters ({int(n)}/12)": n >= 12,
        "Lowercase letters": bool(lower),
        "Uppercase letters": bool(upper),
        "Numbers": bool(digit),
        "Special characters": bool(special),
        "No obvious repeated-character run": not bool(repeats),
        "No common sequence detected": not bool(sequence),
        "Not an exact common-password match": not bool(common),
    }
    # Deterministic score: length, diversity, entropy and pattern penalties.
    length_pts = min(30, n*2.5)
    variety_pts = classes*8
    pattern_pts = 20 - (18 if repeats else 0) - (16 if sequence else 0) - (25 if common else 0)
    entropy_pts = min(22, entropy/3)
    score = int(max(0,min(100,length_pts+variety_pts+pattern_pts+entropy_pts)))
    strength = "Very Weak" if score < 25 else "Weak" if score < 42 else "Moderate" if score < 62 else "Strong" if score < 82 else "Very Strong"
    probs = model.predict_proba(f.reshape(1,-1))[0]
    pred = int(model.predict(f.reshape(1,-1))[0])
    ml_strength = LABELS[pred]
    confidence = float(probs[pred])
    recommendations = []
    if n < 12: recommendations.append("Increase the length to at least 12–16 characters; a longer passphrase is often easier to remember.")
    if classes < 3: recommendations.append("Mix character categories where practical, but prioritize length and unpredictability.")
    if common or sequence: recommendations.append("Avoid dictionary words, famous phrases, dates, names, and keyboard or numeric sequences.")
    if repeats: recommendations.append("Replace long repeated-character runs with unrelated characters or words.")
    recommendations.append("Use a unique password for every account and store it in a reputable password manager.")
    recommendations.append("Enable multi-factor authentication (MFA), especially for email, banking, and administrator accounts.")
    if not recommendations: recommendations.append("Keep it unique, never share it, and enable MFA.")
    return {"score":score,"strength":strength,"entropy":entropy,"ml_strength":ml_strength,
            "ml_confidence":confidence,"checks":checks,"risks":risks,
            "recommendations":recommendations,
            "breakdown":[round(length_pts,1),round(variety_pts,1),round(max(0,pattern_pts),1),round(entropy_pts,1)]}
