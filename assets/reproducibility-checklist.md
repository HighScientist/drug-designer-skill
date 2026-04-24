# Reproducibility Checklist

Before sharing any report or model output, walk this list. Every item
should be either "done" with a pointer, or explicitly marked N/A with a
reason.

## Environment

- [ ] OS, CPU/GPU noted.
- [ ] Language versions (Python / R) recorded.
- [ ] Package versions pinned (`requirements.txt` / `environment.yml` /
      `renv.lock`).
- [ ] Scientific software versions recorded (docking, MD, QM, cheminfo).
- [ ] Random seed(s) recorded.

## Inputs

- [ ] Data source (URL / DOI / internal path) documented.
- [ ] Retrieval date captured.
- [ ] Input file hashes or checksums recorded where applicable.
- [ ] Inclusion / exclusion criteria written down.

## Preprocessing

- [ ] Molecule standardization policy described (salt, tautomer, stereo,
      canonicalization).
- [ ] Protein preparation decisions recorded (protonation, altlocs,
      missing loops, waters, cofactors/metals).
- [ ] Trajectory preparation recorded (imaging, alignment, equilibration
      cutoff).
- [ ] Feature extraction settings recorded.

## Parameters

- [ ] Docking: box, scoring function, exhaustiveness, flexibility.
- [ ] MD: force field, water model, ensemble, thermostat/barostat,
      cutoffs, electrostatics, timestep, constraints, replicates.
- [ ] ML: model family, hyperparameters, selection criterion, search
      range.

## Validation

- [ ] Split strategy stated (random / scaffold / temporal / external /
      group).
- [ ] Nested CV used when hyperparameters were tuned (or explained why
      not).
- [ ] y-randomization reported (if QSAR/ML).
- [ ] Applicability-domain analysis reported (if QSAR/ML).
- [ ] Calibration reported (if classification with decision thresholds).
- [ ] Metrics reported with mean ± std or CI.

## Results

- [ ] Units and sample sizes on every number.
- [ ] Uncertainty reported where applicable.
- [ ] Negative / ambiguous results reported honestly.

## Reproducibility commands

- [ ] Exact CLI commands included.
- [ ] Paths relative to project root.
- [ ] Notebooks exported to scripts (or scripts are the source of truth).

## Safety and scope

- [ ] Computational vs. biological/clinical statements separated.
- [ ] No wet-lab procedural guidance issued.
- [ ] No diagnostic or prescribing claims.
- [ ] Dual-use considerations addressed where relevant.

## Peer-ready bundle

- [ ] README with objective, inputs, run instructions.
- [ ] Example input and example output.
- [ ] This checklist populated.
