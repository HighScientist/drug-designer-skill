# CADD methods — a concise map

A compressed tour of the CADD pipeline. Use as a checklist when scoping a
project, not as a textbook. Search the web for *current* tool versions,
benchmarks, and recent method papers — those change. Fundamentals below are
stable.

## Target selection

- Start from a clear biological hypothesis (pathway, disease link, genetics,
  chemical validation).
- Evaluate druggability: pocket geometry, conservation, precedented
  chemotypes, assay tractability.
- Map target ↔ structure ↔ sequence: UniProt → PDB entries → isoforms, splice
  variants, species, and any relevant mutants.
- Flag reasons **not** to proceed: housekeeping role, paralog redundancy,
  essential off-target, or known toxicity association.

## Protein preparation

- Choose structure by resolution, completeness of binding site, ligand
  relevance, B-factors, and holo vs. apo. Prefer holo structures co-crystalised
  with a chemically similar ligand when available.
- Standardize: fix missing atoms, cap termini, model missing loops (short
  loops only; flag longer gaps), assign protonation states at target pH,
  resolve alternate conformations, handle cofactors/metals explicitly.
- Waters: keep conserved, mechanistically important waters; remove bulk.
- Document every manual decision — protein prep is where reproducibility
  silently dies.

## Ligand preparation

- Enumerate reasonable tautomers and protomers at the target pH.
- Assign stereochemistry explicitly; do not let the toolchain guess.
- Generate a small, diverse set of 3D conformers when the downstream method
  needs them.
- Standardize salts, strip counterions unless chemically relevant, and
  canonicalize SMILES.

## Structure-Based Drug Design (SBDD)

- Requires a reliable structure of the target (experimental or high-confidence
  predicted) with a defined binding site.
- Methods: docking, pharmacophore on receptor, fragment-based design,
  structure-guided SAR, free-energy perturbation.
- Failure modes: wrong protonation, wrong tautomer, flexible loops, induced
  fit, cryptic pockets, water networks, protein–protein interfaces.

## Ligand-Based Drug Design (LBDD)

- Uses known actives to guide design without a reliable structure.
- Methods: QSAR/QSPR, similarity search, pharmacophores, shape matching,
  matched molecular pairs, scaffold hopping.
- Failure modes: limited chemotype diversity, activity cliffs, assay
  heterogeneity, poor applicability domain.

## Docking

- Fast, approximate pose prediction and relative ranking.
- Always validate via redocking of the native ligand and, where possible,
  cross-docking to related structures.
- Scores are not ΔG. See `molecular-docking.md`.

## Virtual screening

- Filter → dock → post-process → triage. Apply property and structural
  filters *before* docking to save compute and to reduce false positives.
- Benchmark against decoys you trust (DUD-E has known biases — see
  `literature-grounding.md`).
- Report enrichment metrics (ROC-AUC, PR-AUC, EF, BEDROC) rather than raw
  hit counts.

## MD refinement and analysis

- Use MD to probe stability, flexibility, water networks, induced fit, and
  residence-time hypotheses.
- Always replicate. One trajectory is an anecdote, not evidence.
- See `molecular-dynamics.md`.

## Free-energy methods (conceptual)

- MM/PBSA, MM/GBSA: cheap, often wrong on absolute values, sometimes useful
  for *relative* ranking within a congeneric series. Report the full
  protocol.
- FEP / TI: more rigorous *relative* ΔΔG between close analogs when the
  perturbation is small and convergence is demonstrated. Validation by
  hysteresis, cycle closure, and replicate runs is expected.
- Absolute binding free energy: demanding; do not promise it from short
  alchemical runs.

## QSAR / ML

- Workflow in `qsar-ml-statistics.md`. Core lesson: leakage is the default
  failure mode.

## ADMET prediction caveats

- Public ADMET models are trained on noisy, biased, small datasets.
- Use predictions as *flags*, not ground truth.
- Never communicate ADMET predictions as medical or safety guidance.

## Reproducibility and validation

- Record software versions, input hashes, seeds, parameters.
- Script every step that changes inputs.
- Validate every model at the boundary of its training data before trusting
  its extrapolations.
