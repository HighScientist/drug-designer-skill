# AGENTS.md — Codex adapter for `drug-designer`

This file is a **thin adapter**, not a duplicate of the skill. The full skill
lives in `drug-designer/SKILL.md` and its `references/`, `scripts/`, and
`assets/` subdirectories.

## When to load the skill

Before responding, read `drug-designer/SKILL.md` and follow it whenever the
task touches any of:

- Computer-Aided Drug Design (CADD)
- Structure-Based Drug Design (SBDD) or Ligand-Based Drug Design (LBDD)
- Molecular docking or virtual screening
- Molecular dynamics (MD) simulation analysis
- QSAR / QSPR / machine learning for molecular property prediction
- Cheminformatics (SMILES/SDF/MOL2, RDKit, Open Babel, fingerprints,
  descriptors, library QC)
- Protein structure analysis (PDB/mmCIF, AlphaFold outputs)
- Protein–ligand interaction analysis
- Statistical validation for drug-discovery models
- Drug-discovery data science, pipelines, or reports

If the task is adjacent but unclear (for example, "a bioinformatics question
that mentions a protein"), skim `drug-designer/SKILL.md` §4 (triage) and
decide whether the skill branches apply.

## How to use the skill

1. Read `drug-designer/SKILL.md` first. It is the source of truth.
2. Classify the request via §2 (Safety gate). Apply the caution/refuse
   behavior before doing technical work.
3. Follow §4 (Triage) to load only the relevant `references/*.md` — do not
   preload everything.
4. Follow §5 (Execution workflow) for order of operations.
5. Use scripts in `drug-designer/scripts/` when they make the analysis more
   reproducible. Run `--help` first.
6. For reports, use the matching template in `drug-designer/assets/` and the
   reproducibility checklist.
7. Apply §8 (Quality rules) to every answer — especially docking-score vs.
   binding-affinity, leakage, applicability domain, and MD convergence
   caveats.

## What not to do

- Do not duplicate skill content into this file. If guidance drifts, update
  `drug-designer/SKILL.md`, not this adapter.
- Do not bypass the safety gate in §2, even when the user frames the request
  as "just a thought experiment".
- Do not invent citations, package APIs, or benchmark numbers. Follow the
  freshness policy in §3.

## Merge guidance

If this repository already has an `AGENTS.md`, merge the sections above into
it rather than overwriting unrelated project instructions. Keep the two
anchors intact: *when to load the skill* and *how to use the skill*.
