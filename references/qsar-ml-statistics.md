# QSAR / QSPR / ML / statistics — validation that holds up

QSAR/QSPR and related ML models are easy to build and easy to fool. This file
is the validation backbone; follow it whenever you model molecular
properties.

## Workflow

1. **Problem framing.** Regression vs. classification, threshold choice,
   assay relevance, known activity range, intended decision use.
2. **Data curation.** Source, assay type, unit harmonization
   (e.g., IC50 → pIC50), standardized structures, mixture handling, salt
   stripping, stereochemistry policy, duplicate policy.
3. **Split strategy** *before* any featurization or leakage-sensitive step.
4. **Featurization.** Descriptors, fingerprints, physicochemical features,
   3D where justified.
5. **Model selection and tuning** using only training folds (no test leakage
   into hyperparameter search).
6. **Validation.** Internal CV + external test + y-randomization +
   applicability-domain analysis + calibration.
7. **Report.** Model card (see `assets/qsar-model-card-template.md`),
   limitations, intended domain, not-for-medical-use disclaimer.

## Descriptor and fingerprint design

- **Morgan / ECFP-like fingerprints**: strong baseline for similarity and
  SAR modeling. Report radius and bit length.
- **MACCS keys**: small, fast, interpretable, weaker than ECFP for
  structure-activity.
- **Physicochemical descriptors** (MW, logP, TPSA, HBD/HBA, rotatable
  bonds): useful, low-dimensional, interpretable.
- **Learned representations** (graph neural nets, transformers,
  pretrained molecular encoders): often competitive, frequently hard to
  interpret, and sensitive to pretraining corpus. Evaluate against a strong
  fingerprint + gradient-boosted-tree baseline.

## Splits — the single most important decision

- **Random split**: easiest, usually optimistic. Acceptable only for an
  in-distribution, non-proprietary baseline.
- **Scaffold split (Bemis–Murcko)**: harder and closer to prospective use;
  required for chemical-series generalization claims.
- **Temporal split**: when publication/assay dates exist, mirrors the real
  prospective setting.
- **External split**: an independent dataset, preferably from a different
  lab/assay, is the strongest test.
- **Cluster-based splits**: stratify by structural or property clusters to
  probe out-of-distribution performance.

Matching the split to the decision is more important than the model choice.

## Leakage prevention

Leakage is the default failure mode. Check, at minimum:

- Duplicates (exact and canonical-SMILES).
- Near-duplicates (tautomers, salts, stereoisomers, protonation states).
- Target leakage (features computed using the label or using the full
  dataset including test).
- Group leakage (same compound or close analog in train and test).
- Temporal leakage (future data informing past predictions).
- Preprocessing leakage (scalers/imputers fit on the full dataset).

Build preprocessing inside a `Pipeline` or equivalent and fit it only on
training folds.

## Cross-validation

- **k-fold** for reasonably sized, independent datasets.
- **Nested CV** when hyperparameters are tuned: outer loop estimates
  generalization, inner loop tunes. Reporting a single-CV best score as
  "generalization" is a common overstatement.
- **Leave-one-group-out** (scaffold, series, assay, lab) when
  group-structured.
- Report mean ± std across folds, not just the mean.

## y-randomization

- Permute labels and refit. The resulting "null" model should perform near
  chance. If it doesn't, you have leakage or severe information imbalance.
- Report y-rand metrics alongside real metrics.

## Applicability domain (AD)

- Define how far a new molecule is from the training distribution: Tanimoto
  to nearest training neighbor, descriptor-space distance, leverage,
  conformal-prediction non-conformity, ensemble disagreement.
- Predictions outside the AD are extrapolations. Flag them, do not trust
  their numeric value.

## Calibration

- For classifiers, check reliability curves, Brier score, expected
  calibration error, and consider Platt/isotonic/sigmoid calibration.
- For regressors, report prediction intervals (quantile regression,
  ensembles, conformal prediction).

## Uncertainty quantification

- Deep ensembles, MC dropout, Gaussian-process models, or conformal
  prediction. Report not just point predictions.
- Distinguish *aleatoric* (data noise) from *epistemic* (model ignorance) —
  they carry different decision implications.

## Metrics

### Regression

- RMSE, MAE (report with units).
- R², but be skeptical — it's sensitive to target variance and can hide
  flat predictions on narrow ranges.
- Spearman / Kendall ρ for ranking-focused tasks.

### Classification

- AUROC, AUPRC (report AUPRC under imbalance).
- Matthews correlation coefficient for imbalanced binary tasks.
- Precision/recall at a clinically or operationally relevant threshold,
  not only at 0.5.
- Confusion matrix on the external test set.

## Class imbalance

- Report class prevalence.
- Avoid accuracy as the headline metric when prevalence is skewed.
- Consider class weights, stratified sampling, threshold tuning, calibrated
  probabilities; avoid oversampling that leaks into CV folds.

## Model interpretability

- **SHAP** / **permutation importance** / **feature importance from trees**:
  useful but fragile under correlated features and group structure. Report
  carefully.
- Substructure-based attribution (e.g., per-atom contributions from
  gradient-boosted models on fingerprints) can help generate chemist-friendly
  hypotheses but is not mechanistic proof.

## Model cards

Document: intended use; training data provenance, size, and distribution;
features; hyperparameters; validation protocol; metrics with uncertainty;
applicability domain; known failure modes; ethical and safety
considerations. Template in `assets/qsar-model-card-template.md`.
