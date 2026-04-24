# `scripts`

This directory contains bundled command-line utilities that make `drug-designer` more reproducible. All scripts are read-oriented analytical helpers built for local execution with explicit caveats and failure messages.

## Shared behavior

Across the directory, the scripts are designed to:

- Use `argparse` and support `--help`
- Avoid internet access
- Fail clearly when optional dependencies are missing
- Avoid destructive writes
- Print caveats and reproducibility-oriented command summaries
- Avoid overstating computational outputs as biological proof

## Scripts

### [`inspect_structure.py`](./inspect_structure.py)

Inspects PDB or mmCIF files using Biopython and reports:

- Model and chain counts
- Protein and nucleotide residue counts
- Ligands, waters, metals, and non-standard residues
- Alternate locations and insertion codes
- Missing backbone atoms and unusually high B-factors

Primary use case: quick structural inventory and syntax-level QC for protein structures before downstream analysis.

### [`summarize_docking.py`](./summarize_docking.py)

Summarizes docking or virtual-screening tables in CSV/TSV format and reports:

- Record counts and column names
- Missing-score counts
- Duplicate identifier counts
- Score distribution statistics
- Top-ranked compounds
- Score bunching warnings

Primary use case: fast QC and ranking summaries for docking outputs. It explicitly warns that docking scores are not binding affinities.

### [`analyze_md.py`](./analyze_md.py)

Performs basic trajectory analysis with MDAnalysis and reports:

- Atom, residue, segment, and frame counts
- Trajectory timestep and covered simulation time when available
- C-alpha RMSD
- C-alpha RMSF summary
- Protein radius of gyration
- Optional inter-selection distance statistics

Primary use case: first-pass MD QC and descriptive analysis, with clear warnings against claiming convergence from a single metric or single trajectory.

### [`qsar_baseline.py`](./qsar_baseline.py)

Builds a leakage-aware baseline QSAR/QSPR model using scikit-learn and:

- Loads a CSV/TSV with SMILES and target columns
- Detects duplicated SMILES
- Featurizes molecules with RDKit Morgan fingerprints when available
- Falls back to a clearly labeled hash-based featurizer when RDKit is absent
- Runs cross-validation for regression or classification
- Reports fold-aggregated metrics with uncertainty

Primary use case: creating a didactic, reproducible baseline rather than a production-ready predictive system.

### [`compound_qc.py`](./compound_qc.py)

Performs compound-library QC with RDKit and:

- Validates SMILES parsing
- Standardizes structures
- Produces canonical SMILES and InChIKeys
- Flags duplicates
- Computes basic descriptors
- Applies a deliberately partial alert SMARTS panel
- Optionally writes an enriched output table without overwriting the input

Primary use case: molecule-table hygiene before modeling, docking, or screening analysis.

## Suggested usage pattern

1. Run a script with `--help`.
2. Verify that the required dependency stack is available.
3. Use the script output as analytical support, not as final scientific proof.
4. Carry the caveats into the report or final answer.
