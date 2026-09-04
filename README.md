# CellSight AI

Predicting cellular health status from **multi-omics** data (transcriptomics + metabolomics)
using machine learning - a step toward earlier, molecular-level preventive health screening.

*Current status: metabolomics layer implemented and validated on two independent public cohorts;
transcriptomics fusion is the next milestone.*

**Idea:** instead of yearly symptom-based checkups, use molecular data (metabolomics today,
multi-omics next) to classify a person's cellular health state - *healthy / pre-diabetic / diabetic* -
and output a simple **Cell Health Score (0–100)**.

> Educational research prototype. Not a medical device. Does not diagnose any condition.

## Results

| Experiment | Dataset | Model | Result |
|---|---|---|---|
| Baseline pipeline | Pima diabetes (768 people, 8 biomarkers) | Logistic regression (standardised, imputed) | Test AUROC 0.825 · 5-fold CV 0.83 |
| Metabolomics classifier | MTBLS1 - urine NMR, 132 people (T2D vs control) | Same pipeline | Test AUROC 0.937 · 5-fold CV 0.968 |
| **Independent replication** | MTBLS8644 - plasma LC-MS, 80 people, different lab/instrument/sample type | Same pipeline | Test AUROC 1.00 · 5-fold CV 0.988 |
| **3-class CellSight model** | MTBLS8644 (healthy / pre-diabetic / diabetic) | Multinomial logistic regression | Macro-AUROC 0.827 |

Notes:
- All evaluation uses stratified train/test splits + 5-fold cross-validation.
- In the 3-class model, misclassifications occur almost exclusively between adjacent
  categories (e.g. diabetic ↔ pre-diabetic), consistent with the biology of disease progression.
- The top predictive metabolites (e.g. sarcosine, carnitine species) have published
  associations with diabetes biology.

## Limitations (known and planned)

- Small, single cohorts; no cross-platform model transfer yet (batch effects remain an open problem).
- Internal validation only - external prospective validation is the next milestone.
- Binary/3-class proxies of "cellular health"; the full vision adds a transcriptomics layer
  (multi-omics fusion, e.g. the iHMP prediabetes cohort).

## Repository contents

| File | Description |
|---|---|
| `cellsight_starter_pipeline.ipynb` | Baseline pipeline (Pima) → real metabolomics (MTBLS1) → Cell Health Score |
| `cellsight_external_validation_v2.ipynb` | Independent replication + 3-class model (MTBLS8644) + driver metabolites |
| `app.py` | Streamlit demo app: biomarker sliders → Cell Health Score (uses `pima_model.joblib`) |

## Quick start

```bash
pip install pandas scikit-learn requests joblib streamlit
jupyter notebook          # run the notebooks top to bottom
streamlit run app.py      # launch the demo app (after running the starter notebook)
```

btw no GPU required

## Data sources (public)

- Pima Indians Diabetes dataset (UCI / NIDDK)
- MetaboLights MTBLS1 - Salek et al., urinary NMR metabolomics of type 2 diabetes
- MetaboLights MTBLS8644 - metabolomics of pre-diabetes to T2DM progression

## License

Soham Bhole, 2026. **All rights reserved.**
This repository is shared publicly for portfolio/review purposes. No permission is granted
to copy, modify, redistribute, or use this code or its derivatives without written consent.
