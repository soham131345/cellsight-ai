"""CellSight AI - demo app. Run: streamlit run app.py"""
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="CellSight AI", page_icon="🧬")
st.title("🧬 CellSight AI — prototype")
st.caption("Educational prototype. Not a medical device. Does not diagnose anything.")

@st.cache_resource
def load_model():
    return joblib.load("pima_model.joblib")

model = load_model()

def cell_health_score(risk_proba):
    score = int(round(100 * (1 - risk_proba)))
    if score >= 80:   return score, "healthy", "🟢"
    elif score >= 60: return score, "stressed", "🟡"
    elif score >= 40: return score, "inflamed", "🟠"
    else:             return score, "pre-diabetic-risk", "🔴"

st.subheader("Enter biomarker values")
c1, c2 = st.columns(2)
with c1:
    glucose = st.slider("Glucose (mg/dL)", 50, 250, 110)
    bmi     = st.slider("BMI", 15.0, 50.0, 24.0, 0.1)
    age     = st.slider("Age", 18, 90, 25)
    bp      = st.slider("Blood pressure (mmHg)", 40, 140, 72)
with c2:
    insulin  = st.slider("Insulin (mu U/mL)", 0, 900, 80)
    preg     = st.slider("Pregnancies", 0, 17, 1)
    skin     = st.slider("Skin fold thickness (mm)", 5, 80, 25)
    pedigree = st.slider("Diabetes pedigree function", 0.05, 2.5, 0.35, 0.01)

if st.button("Compute Cell Health Score"):
    row = pd.DataFrame([[preg, glucose, bp, skin, insulin, bmi, pedigree, age]],
                       columns=["preg","glucose","bp","skin","insulin","bmi","pedigree","age"])
    p = model.predict_proba(row)[0, 1]
    score, cat, icon = cell_health_score(p)
    st.metric("Cell Health Score", f"{score}/100")
    st.subheader(f"{icon} Category: {cat}")
    st.progress(score / 100)
    st.info("Prototype model trained on the public Pima diabetes dataset (768 people).")
