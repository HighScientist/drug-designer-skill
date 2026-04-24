# Reporting standards — reproducibility by default

A report is reproducible when a competent peer can, from the written record
alone, rebuild the analysis and expect the same result. These are the
non-negotiables.

## Environment and software

- Operating system, CPU/GPU summary when relevant.
- Language versions (Python, R).
- Package versions for *every* scientific dependency used (pin via
  `requirements.txt`, `environment.yml`, `renv.lock`, or equivalent).
- Docking/MD/QM software versions, license flavor, and any patches.
- Random seed(s) for anything stochastic.

## Input data

- Dataset name, source (URL, DOI, internal path), date of retrieval.
- Size (records, columns, atoms, trajectory length).
- File formats and how they were parsed.
- Exclusion/inclusion criteria.
- Hash or checksum when the data is expected to be immutable.

## Preprocessing

- Standardization (salt stripping, tautomer policy, stereochemistry
  policy, canonicalization toolkit).
- Protein preparation decisions (protonation, altlocs, missing-loop
  handling, water policy, cofactor/metal handling).
- Trajectory preparation (imaging, alignment selection, equilibration
  cutoff).
- Feature extraction (descriptors, fingerprint radius/bit size,
  normalization).

## Parameters

- Docking: box, scoring function, exhaustiveness/iterations, flexibility.
- MD: force field, water model, ensemble, thermostat/barostat, cutoffs,
  long-range electrostatics, timestep, constraints.
- ML: model family, hyperparameters, search range, selection criterion.

## Split strategy

- Scheme (random, scaffold, temporal, external, group-aware).
- Proportions, fold count, stratification.
- Whether a held-out external set was used.
- How leakage was prevented.

## Validation strategy

- Internal CV configuration (and whether nested).
- y-randomization result alongside the real model.
- Applicability-domain method and threshold.
- Calibration method if used.
- Metrics with uncertainty (mean ± std over folds/replicates; CIs when
  appropriate).

## Results

- Units and sample sizes on every number.
- Uncertainty on every reported metric.
- Negative or ambiguous results reported as honestly as positive ones.

## Assumptions and limitations

- Every assumption listed explicitly.
- Known failure modes of the methods used, in the context of this
  analysis.
- Boundaries of interpretation (what the results do *not* prove).

## Reproducibility commands

- Exact CLI invocations that produced the results.
- Paths relative to the project root, not absolute home-directory paths.
- If notebooks were used, export cleaned `.py`/`.R` scripts as the
  authoritative record.

## Interpretation boundaries

- Explicitly distinguish *computational* statements ("the model ranks X
  above Y with score Δ") from *biological* or *clinical* statements.
- Never promise binding affinity from docking scores or therapeutic
  outcomes from computational predictions.
- When recommending experiments, stay high-level; do not draft wet-lab
  protocols.

## Ship with

- Code.
- Environment file.
- README with the objective, inputs, and how to run.
- A populated `reproducibility-checklist.md` (see the asset).
- Where possible, a concrete example input and example output.

## Figures and tables

- Every axis labeled, every unit included, every legend complete.
- Replicate-aware visualization (e.g., replicate means with error bands
  rather than a single line).
- For docking/MD, include the receptor identifier and box/selection in
  captions.
- Do not use 3-D bar charts or rainbow colormaps for quantitative data.

## Where to use asset templates

- `assets/cadd-report-template.md` — general CADD report skeleton.
- `assets/docking-report-template.md` — docking / VS specific.
- `assets/md-report-template.md` — MD analysis.
- `assets/qsar-model-card-template.md` — QSAR/ML model card.
- `assets/reproducibility-checklist.md` — final sanity check before
  sharing.
