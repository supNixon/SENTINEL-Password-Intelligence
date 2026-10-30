import streamlit as st
import pandas as pd
from pathlib import Path
from src.analyzer import analyze_password, load_or_train_model

st.set_page_config(page_title="Sentinel | Password Intelligence", page_icon="🛡️", layout="wide")
st.markdown("""
<style>
:root { --ink:#172033; --muted:#64748b; }
.block-container { padding-top: 2rem; max-width: 1180px; }
.hero { padding: 1.7rem 1.9rem; border-radius: 18px; background: linear-gradient(120deg,#101c36,#233f69); color:white; margin-bottom:1.2rem; }
.hero h1 { color:white; margin:0; font-size:2.1rem; }
.hero p { color:#dbeafe; margin:.45rem 0 0; }
.metric-card { padding:1rem; border:1px solid #e2e8f0; border-radius:14px; background:#fff; }
.small-muted { color:#64748b; font-size:.88rem; }
.stProgress > div > div > div > div { background-color:#2563eb; }
</style>
""", unsafe_allow_html=True)

model, model_status = load_or_train_model()
st.markdown('<div class="hero"><h1>🛡️ Sentinel Password Intelligence</h1><p>Hybrid password-strength assessment using explainable security rules, entropy analysis, and a machine-learning classifier.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("About this project")
    st.write("A privacy-first educational security tool. Password analysis happens locally in this app process.")
    st.caption("Model: Random Forest • Feature engineering • Rule-based guidance")
    st.divider()
    st.write("**Model status**")
    st.success(model_status)
    st.caption("Do not enter a password you actively use. Use a sample or test password.")

st.warning("Privacy notice: This demo does not intentionally save or transmit the password. For maximum safety, test with a sample password—not a real account password.")
password = st.text_input("Enter a test password", type="password", placeholder="Type a sample password…")
show = st.checkbox("Show password while testing", value=False)
if show and password:
    st.code(password)

if password:
    result = analyze_password(password, model)
    score = result["score"]
    label = result["strength"]
    colors = {"Very Weak":"#dc2626","Weak":"#ea580c","Moderate":"#ca8a04","Strong":"#16a34a","Very Strong":"#047857"}
    color = colors[label]
    c1,c2,c3 = st.columns([1.2,1,1])
    with c1:
        st.markdown(f'<div class="metric-card"><div class="small-muted">Overall strength</div><h2 style="color:{color};margin:.3rem 0">{label}</h2><div style="font-size:2rem;font-weight:700">{score}/100</div></div>', unsafe_allow_html=True)
        st.progress(score/100)
    with c2:
        st.metric("Estimated entropy", f'{result["entropy"]:.1f} bits')
        st.caption("Higher entropy generally means more search effort.")
    with c3:
        st.metric("ML prediction", result["ml_strength"])
        st.caption(f'Model confidence: {result["ml_confidence"]:.0%}')

    st.subheader("Security analysis")
    left,right = st.columns(2)
    with left:
        st.markdown("**Detected characteristics**")
        for item, ok in result["checks"].items():
            st.write(("✅ " if ok else "⚠️ ") + item)
    with right:
        st.markdown("**Risk indicators**")
        if result["risks"]:
            for risk in result["risks"]:
                st.write("• " + risk)
        else:
            st.success("No obvious high-risk patterns detected by this demo.")

    st.subheader("AI-style improvement recommendations")
    for rec in result["recommendations"]:
        st.write("💡 " + rec)

    st.subheader("Score breakdown")
    chart = pd.DataFrame({"Component":["Length","Character variety","Pattern resistance","Entropy"],"Points":result["breakdown"]})
    st.bar_chart(chart.set_index("Component"))
    st.caption("The overall score combines deterministic security checks and entropy. The ML model provides a separate learned classification; it is not a guarantee of safety.")

else:
    st.subheader("What the analyzer evaluates")
    a,b,c = st.columns(3)
    a.info("**Length & variety**\\n\\nChecks password length and character classes.")
    b.info("**Pattern detection**\\n\\nFlags common sequences, repetition, keyboard-like patterns and predictable words.")
    c.info("**Machine learning**\\n\\nA Random Forest model classifies engineered password features.")
    st.markdown("### Example test passwords")
    st.code("hello123\\nSummer2026!\\nViolet-River-Compass-72")
    st.caption("These examples are illustrative. Avoid reusing them.")

st.divider()
st.caption("Sentinel Password Intelligence • Academic cybersecurity project • Not a substitute for a password manager or a breach-monitoring service.")
