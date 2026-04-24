# drug-designer

[![Claude Skill](https://img.shields.io/badge/source-Claude%20Skill-0B5FFF)](./SKILL.md)
[![Codex Adapter](https://img.shields.io/badge/adapter-AGENTS.md-111111)](./AGENTS.md)
[![Focus](https://img.shields.io/badge/focus-CADD%20%26%20Cheminformatics-1B7F5A)](./references/cadd-methods.md)

`drug-designer` is an expert AI skill for computational drug discovery. It is authored as a Claude skill in [`SKILL.md`](./SKILL.md) and adapted for Codex through [`AGENTS.md`](./AGENTS.md).

## Purpose

The skill helps with:

- Computational drug-discovery analysis
- Workflow design and reproducible execution
- Scientific interpretation and methodology critique
- Report drafting and structured analytical outputs
- Code generation for cheminformatics, docking, MD, and QSAR tasks

## Canonical files

- [`SKILL.md`](./SKILL.md): source of truth for behavior, safety rules, triage, execution workflow, output structure, and quality rules.
- [`AGENTS.md`](./AGENTS.md): thin Codex adapter that instructs Codex to load and follow `SKILL.md`.

## Supported domains

- CADD, SBDD, and LBDD
- Molecular docking and virtual screening
- Molecular dynamics analysis
- QSAR / QSPR / machine learning baselines
- Cheminformatics and compound QC
- Protein structure and protein-ligand interpretation
- Literature-grounded methodology review
- Reproducible scientific reporting

## Safety model

The skill explicitly separates requests into:

- Allowed computational and educational analysis
- High-level caution-only dual-use or optimization-adjacent requests
- Refused or redirected requests such as synthesis, wet-lab protocols, toxin design, safety evasion, and clinical decision-making

See [`references/safety-and-ethics.md`](./references/safety-and-ethics.md) and the safety gate in [`SKILL.md`](./SKILL.md).

## Directory structure

```text
drug-designer/
├── AGENTS.md
├── README.md
├── SKILL.md
├── assets/
│   ├── README.md
│   ├── cadd-report-template.md
│   ├── docking-report-template.md
│   ├── md-report-template.md
│   ├── qsar-model-card-template.md
│   └── reproducibility-checklist.md
├── references/
│   ├── README.md
│   ├── cadd-methods.md
│   ├── cheminformatics.md
│   ├── literature-grounding.md
│   ├── molecular-docking.md
│   ├── molecular-dynamics.md
│   ├── python-r-tooling.md
│   ├── qsar-ml-statistics.md
│   ├── reporting-standards.md
│   ├── safety-and-ethics.md
│   └── structural-biology.md
└── scripts/
    ├── README.md
    ├── analyze_md.py
    ├── compound_qc.py
    ├── inspect_structure.py
    ├── qsar_baseline.py
    └── summarize_docking.py
```

## How the skill works

1. Start from the scientific question.
2. Classify the request through the safety gate.
3. Identify inputs, provenance, units, and limitations.
4. Load only the relevant reference modules.
5. Use bundled scripts where they improve reproducibility.
6. Return results with methods, QC, limitations, and next computational steps.

## Subdirectories

- [`assets/`](./assets/README.md): report templates and reproducibility checklists.
- [`references/`](./references/README.md): domain guidance loaded on demand according to task type.
- [`scripts/`](./scripts/README.md): reproducible utilities for structural analysis, docking summaries, MD, QSAR, and compound QC.

## Relationship between Claude and Codex

This directory is intentionally organized so the same skill can serve both ecosystems:

- Claude reads `SKILL.md` directly.
- Codex reads `AGENTS.md`, which points back to `SKILL.md` instead of duplicating the instructions.

That design keeps one canonical instruction set while still making the skill usable in Codex-compatible environments.
