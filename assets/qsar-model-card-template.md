# QSAR / QSPR Model Card — {{model_name}}

## Intended use

- Task (regression / classification):
- Endpoint (e.g., pIC50 against target X):
- Intended downstream decision:
- **Out-of-scope uses** (must include):
  - Not a medical-device or diagnostic model.
  - Not a replacement for experimental validation.
  - Not for prescribing, diagnosis, or treatment.

## Training data

- Source(s), version(s), retrieval date:
- Size (records, classes or value range):
- Curation steps (salt stripping, tautomer policy, stereochemistry,
  canonicalization toolkit):
- Duplicate / near-duplicate handling:
- Class balance (for classification):

## Features

- Representation (fingerprint type and params, descriptor set, learned
  encoder + version):
- Scaling / normalization (fit on training only):
- Feature count and any selection procedure:

## Model

- Family and version:
- Hyperparameters (final set + search range):
- Random seed(s):

## Validation

- Split strategy (random / scaffold / temporal / external / group):
- CV scheme (folds, stratification, group-awareness, nested or not):
- External test set (source, size, provenance):
- y-randomization results:
- Applicability-domain method and threshold:
- Calibration method (if used):

## Metrics

- Regression: RMSE, MAE, R², Spearman ρ — with mean ± std across folds.
- Classification: AUROC, AUPRC, MCC, precision/recall at the decision
  threshold.
- Uncertainty estimates (CIs, ensemble std, conformal intervals).
- Calibration summary (Brier, ECE, reliability curve reference).

## Applicability domain

- Definition (Tanimoto NN, leverage, conformal, ensemble variance):
- Coverage on validation and external sets:
- How predictions outside the AD will be surfaced to users:

## Known failure modes

- Chemotype gaps:
- Activity cliffs:
- Assay heterogeneity:
- Structural edge cases (macrocycles, organometallics, etc.):

## Ethical and safety considerations

- Dual-use notes:
- No deployment for medical, prescribing, or diagnostic purposes.
- Training-data bias considerations.

## Reproducibility

- Environment file:
- Training command:
- Evaluation command:
- Data access policy / hashes:

## Contact and versioning

- Model version:
- Release date:
- Contact:
