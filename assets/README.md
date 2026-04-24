# `assets`

This directory contains reusable Markdown templates and checklists for reporting computational drug-discovery work in a consistent, reproducible way.

## Purpose

Use these files when the skill needs to deliver structured written outputs rather than only conversational answers.

## Files

- [`cadd-report-template.md`](./cadd-report-template.md): general-purpose report template for CADD analyses. Covers objective, inputs, assumptions, methods, QC, results, validation, interpretation, limitations, reproducibility, and next computational steps.
- [`docking-report-template.md`](./docking-report-template.md): specialized report template for docking and virtual screening. Includes receptor, binding site, ligand set, docking protocol, validation, pose analysis, and score caveats.
- [`md-report-template.md`](./md-report-template.md): specialized template for molecular dynamics analysis. Includes system definition, force fields, protocol, QC, core observables, convergence, and reproducibility.
- [`qsar-model-card-template.md`](./qsar-model-card-template.md): model card template for QSAR/QSPR systems. Documents intended use, training data, features, model type, validation, metrics, applicability domain, failure modes, and versioning.
- [`reproducibility-checklist.md`](./reproducibility-checklist.md): cross-cutting checklist for environment, inputs, preprocessing, parameters, validation, results, commands, and peer-ready packaging.

## When to use which template

- Use `cadd-report-template.md` for mixed or end-to-end computational studies.
- Use `docking-report-template.md` for docking campaigns or virtual screening summaries.
- Use `md-report-template.md` for trajectory-focused analyses.
- Use `qsar-model-card-template.md` when documenting predictive models.
- Use `reproducibility-checklist.md` alongside any of the above.

## Design principles

These assets reflect the same standards defined in `SKILL.md`:

- Reproducibility first
- Explicit assumptions and limitations
- Bounded interpretation
- No overclaiming from computational results alone
- No unsafe operational guidance
