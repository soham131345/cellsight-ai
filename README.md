# CellSight AI

Predicting cellular health status from **multi-omics** data (transcriptomics + metabolomics)
using machine learning — a step toward earlier, molecular-level preventive health screening.

*Current status: metabolomics + transcriptomics layers implemented; fusion validated on
three independent public cohorts.*

**Idea:** instead of yearly symptom-based checkups, use molecular data to classify a person's
cellular health state — *- / stressed / inflamed / pre-diabetic* — and output a simple
**Cell Health Score (0–100)**.

> Educational research prototype. Not a medical device. Does not diagnose any condition.

## Results

| Experiment | Dataset | Model | Result |
|---|---|---|---|
| Baseline pipeline | Pima diabetes (768 people, 8 biomarkers) | Logistic regression (standardised, imputed) | Test AUROC 0.825 · 5-fold CV 0.83 |
| Metabolomics classifier | MTBLS1 — urine NMR, 132 people (T2D vs control) | Same pipeline | Test AUROC 0.937 · 5-fold CV 0.968 |
| **Independent replication** | MTBLS8644 — plasma LC-MS, 80 people, different lab/instrument/sample type | Same pipeline | Test AUROC 1.00 · 5-fold CV 0.988 |
| **3-class CellSight model** | MTBLS8644 (- / pre-diabetic / diabetic) | Multinomial logistic regression | Macro-AUROC 0.827 |
| LC-MS dual-mode fusion | MTBLS8644 (POS + NEG ion modes) | Early fusion + leakage-safe feature selection | CV AUROC 0.991 |
| Metabolome + microbiome fusion | iHMP prediabetes cohort (107 subjects, longitudinal) | Early fusion, **subject-level GroupKFold** | CV AUROC 0.78 (honest) vs 0.997 (naive split — see finding below) |
| **Transcriptome + metabolome fusion** | IBDMDB/HMP2 (90 subjects, biopsy RNA-seq + stool LC-MS; inflamed vs -) | Early fusion + feature selection | TX alone 0.942 · MBX alone 0.969 · **fused 0.988** |

### Key methodological finding

On longitudinal multi-omics data, the commonly used **sample-level split leaks information**
(the same person's repeated samples land in both train and test). A published benchmark reports
0.997 AUROC with that split; under honest subject-level cross-validation the same data yields
~0.70–0.78. All CellSight models use subject-aware validation.

Notes:
- In the 3-class model, misclassifications occur almost exclusively between adjacent
  categories (e.g. diabetic ↔ pre-diabetic), consistent with the biology of disease progression.
- Fusion outperforms either omics layer alone in every cohort tested (2/2 independent datasets).
- Top predictive metabolites (e.g. sarcosine, carnitine species) have published
  associations with diabetes biology.
- If any errors are faced, these will not be due to the code because the code has been tested across three different environments. Should there be any errors, feel free to click the ask chatgpt/google button below the error when it appears.

## Limitations (known and planned)

- Small, single cohorts; no cross-platform model transfer yet (batch effects remain an open problem).
- Internal validation only — external prospective validation is the next milestone.
- Categories are proxies of "cellular health" derived from disease labels.

## Repository contents

| File | Description |
|---|---|
| `cellsight_starter_pipeline.ipynb` | Baseline pipeline (Pima) → real metabolomics (MTBLS1) → Cell Health Score |
| `cellsight_external_validation_v2.ipynb` | Independent replication + 3-class model (MTBLS8644) + driver metabolites |
| `cellsight_fusion.ipynb` | LC-MS POS+NEG fusion (MTBLS8644) |
| `cellsight_multiomics_fusion.ipynb` | Metabolome + microbiome fusion + the leakage finding (iHMP) |
| `cellsight_transcriptomics_fusion.ipynb` | Transcriptome + metabolome fusion (IBDMDB) — the "inflamed" branch |
| `app.py` | Streamlit demo app: biomarker sliders → Cell Health Score (uses `pima_model.joblib`) |
| `*.joblib` | Trained models saved by the notebooks |

## Quick start

```bash
pip install pandas scikit-learn requests joblib streamlit numpy
jupyter notebook          # run the notebooks top to bottom
streamlit run app.py      # launch the demo app
```

## no gpu required to run

## Data sources (public)

- Pima Indians Diabetes dataset (UCI / NIDDK)
- MetaboLights MTBLS1 — Salek et al., urinary NMR metabolomics of type 2 diabetes
- MetaboLights MTBLS8644 — metabolomics of pre-diabetes to T2DM progression
- iHMP / HMP2 — Integrative Human Microbiome Project prediabetes cohort (via public mirrors)
- IBDMDB / HMP2 — Lloyd-Price et al., Nature 2019 (host transcriptome + metabolome;
  metabolomics mirror: Metabolomics Workbench ST000923)

## License

Soham Bhole, 2026. **All rights reserved.**
This repository is shared publicly for portfolio/review purposes. No permission is granted
to copy, modify, redistribute, or use this code or its derivatives without written consent.
