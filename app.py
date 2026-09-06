import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="CellSight AI", page_icon="🧬")
st.title("🧬 CellSight AI")
st.caption("Educational research prototype. Not a medical device. Does not diagnose any condition.")

@st.cache_resource
def load_models():
    m = {"pima": joblib.load("pima_model.joblib")}
    try:
        m["mtbls1"] = joblib.load("mtbls1_metabolomics_model.joblib")
    except Exception:
        m["mtbls1"] = None
    try:
        m["inflamed"] = joblib.load("cellsight_inflamed_model.joblib")
    except Exception:
        m["inflamed"] = None
    return m

models = load_models()

def cell_health_score(risk_proba):
    score = int(round(100 * (1 - risk_proba)))
    if score >= 80:   return score, "healthy", "🟢"
    elif score >= 60: return score, "stressed", "🟡"
    elif score >= 40: return score, "inflamed", "🟠"
    else:             return score, "pre-diabetic-risk", "🔴"

def show_result(p, note):
    score, cat, icon = cell_health_score(p)
    st.metric("Cell Health Score", f"{score}/100")
    st.subheader(f"{icon} Category: {cat}")
    st.progress(score / 100)
    st.info(note)

tab1, tab2, tab3 = st.tabs(["⚡ Quick demo", "🧪 Metabolomics file", "🔬 Multi-omics file"])

with tab1:
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
    if st.button("Compute Cell Health Score", key="b1"):
        row = pd.DataFrame([[preg, glucose, bp, skin, insulin, bmi, pedigree, age]],
                           columns=["preg","glucose","bp","skin","insulin","bmi","pedigree","age"])
        p = models["pima"].predict_proba(row)[0, 1]
        show_result(p, "Model: clinical biomarkers, trained on the public Pima diabetes dataset (768 people).")

with tab2:
    st.subheader("Upload a metabolomics sample")
    st.write("CSV with one row per sample and one column per NMR bin (MTBLS1 format, 220 columns).")
    up = st.file_uploader("Choose CSV", type="csv", key="u1")
    if up is not None and st.button("Score metabolomics sample", key="b2"):
        if models["mtbls1"] is None:
            st.error("mtbls1_metabolomics_model.joblib not found in this folder.")
        else:
            df = pd.read_csv(up)
            feats = list(models["mtbls1"].feature_names_in_)
            missing = [f for f in feats if f not in df.columns]
            if missing:
                st.error(f"{len(missing)} required columns missing, e.g. {missing[:5]}")
                st.stop()
            p = models["mtbls1"].predict_proba(df[feats])[:, 1]
            for i, pi in enumerate(p):
                st.write(f"Sample {i+1}:")
                show_result(float(pi), "Model: urine NMR metabolomics, trained on MTBLS1 (132 people).")

with tab3:
    st.subheader("Upload a fused multi-omics sample")
    st.write("CSV with one row per sample: gene-expression columns (log-CPM) + metabolite columns, matching the Part F feature names.")
    up2 = st.file_uploader("Choose CSV", type="csv", key="u2")
    if up2 is not None and st.button("Score multi-omics sample", key="b3"):
        if models["inflamed"] is None:
            st.error("cellsight_inflamed_model.joblib not found in this folder.")
        else:
            df = pd.read_csv(up2)
            obj = models["inflamed"]
            feats = obj["feature_names"]
            missing = [f for f in feats if f not in df.columns]
            if missing:
                st.error(f"{len(missing)} required features missing, e.g. {missing[:5]}")
            else:
                p = obj["pipeline"].predict_proba(df[feats])[:, 1]
                for i, pi in enumerate(p):
                    st.write(f"Sample {i+1}:")
                    show_result(float(pi), "Model: transcriptome + metabolome fusion, trained on IBDMDB/HMP2 (90 people).")
