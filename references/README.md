# `references`

This directory contains the domain knowledge modules that power the `drug-designer` skill. These files are meant to be loaded lazily according to the task branch instead of being preloaded all at once.

## Purpose

Each reference file acts as a focused guidance module for one part of the computational drug-discovery workflow.

## Files

- [`cadd-methods.md`](./cadd-methods.md): high-level map of target selection, protein and ligand preparation, SBDD, LBDD, docking, virtual screening, MD refinement, free-energy concepts, QSAR/ML, ADMET caveats, and reproducibility.
- [`structural-biology.md`](./structural-biology.md): guidance for reading protein structures correctly, including file formats, assemblies, missing residues, cofactors, waters, predicted structures, and binding-site interpretation.
- [`molecular-docking.md`](./molecular-docking.md): docking and virtual-screening methodology, including receptor/ligand preparation, search-space setup, validation, enrichment metrics, consensus scoring, and score caveats.
- [`molecular-dynamics.md`](./molecular-dynamics.md): MD analysis principles, trajectory QC, equilibration vs. production, core observables, higher-order analyses, convergence, and reporting expectations.
- [`qsar-ml-statistics.md`](./qsar-ml-statistics.md): leakage-aware QSAR/QSPR and ML validation guidance, including splits, cross-validation, y-randomization, applicability domain, calibration, uncertainty, metrics, and model cards.
- [`cheminformatics.md`](./cheminformatics.md): structure formats, standardization, salts, tautomer and stereochemistry caveats, similarity, descriptors, library QC, and screening-alert context.
- [`python-r-tooling.md`](./python-r-tooling.md): orientation to the Python and R scientific stacks commonly used by this skill, plus notes on when online documentation should be checked.
- [`literature-grounding.md`](./literature-grounding.md): methodology map connecting common computational drug-discovery topics to classic concepts and areas where literature grounding matters.
- [`reporting-standards.md`](./reporting-standards.md): reproducibility expectations for environments, inputs, preprocessing, parameters, validation, interpretation boundaries, and report packaging.
- [`safety-and-ethics.md`](./safety-and-ethics.md): the safety boundary document for allowed, cautionary, and refused request classes.

## Loading strategy

The intended workflow is:

- Start with the primary branch for the task.
- Pull adjacent references only when they are necessary.
- Consult `safety-and-ethics.md` first for borderline or dual-use contexts.

Examples:

- Structure-based work: `cadd-methods.md` + `structural-biology.md`
- Docking: `molecular-docking.md`
- MD: `molecular-dynamics.md`
- QSAR/ML: `qsar-ml-statistics.md`
- Compound handling and descriptors: `cheminformatics.md`
- Report writing: `reporting-standards.md`

## Why this directory matters

This directory is what keeps the skill specific and disciplined. Instead of relying on vague general knowledge, the skill can route into the exact guidance needed for the current scientific task.
