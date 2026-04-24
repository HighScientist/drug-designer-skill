# Literature grounding — methodology map

A decision aid for choosing and critiquing methods, plus guidance on when to
refresh via the web. **Do not fabricate references.** When unsure of a
citation, say so and mark it as needing verification.

Each entry covers: *what it is for*, *when to use it*, *common failure
modes*, *validation expectations*, and *whether web search is recommended*.

## Classic CADD concepts

- **What**: the conceptual backbone — pharmacophore theory, shape theory,
  scaffolds, SAR, matched pairs, free-energy decomposition.
- **When**: grounding any drug-discovery conversation.
- **Failure modes**: over-literal application to novel chemotypes;
  ignoring assay context.
- **Validation**: compare hypotheses against known actives/inactives.
- **Web search**: rarely needed — these concepts are stable.

## Lipinski and drug-likeness heuristics

- **What**: Lipinski Ro5, Veber, Ghose, lead-likeness, fragment rules.
- **When**: library design and hit triage.
- **Failure modes**: treating heuristics as prohibitions; oral-drug rules
  applied to non-oral contexts; beyond-Ro5 chemotypes (PROTACs, macrocycles,
  peptidomimetics) often violate Ro5 and still succeed.
- **Validation**: benchmark against your therapeutic area.
- **Web search**: recommended for beyond-Ro5 space, since literature is
  active.

## Docking validation

- **What**: redocking, cross-docking, decoy-based enrichment, pose-level
  RMSD.
- **When**: before trusting any docking result for decisions.
- **Failure modes**: relying on raw score, ignoring cross-docking, using a
  biased decoy set.
- **Validation**: redock RMSD < 2.0 Å (case-dependent), cross-dock to a
  second holo structure, report EF/BEDROC on a chemically balanced set.
- **Web search**: recommended for current docking-tool benchmarks.

## Virtual screening benchmarking

- **What**: prospective-style evaluation of ranking quality on a set of
  actives and decoys/inactives.
- **When**: before deploying a VS pipeline.
- **Failure modes**: DUD-E-style biases (property-matched decoys may still
  be distinguishable by topological features), single-target
  overfitting.
- **Validation**: multiple targets, multiple decoy sources (e.g., DUD-E,
  DEKOIS, DUDE-Z, ChEMBL-derived), report EF/BEDROC not only AUC.
- **Web search**: recommended — benchmarks evolve.

## QSAR validation

- **What**: OECD principles, rigorous splits, external validation, AD,
  y-randomization.
- **When**: any model meant to inform decisions.
- **Failure modes**: random split only, internal CV only, leakage, no AD.
- **Validation**: scaffold/temporal split + external test + y-randomization
  + AD analysis + calibration.
- **Web search**: rarely needed for principles; recommended for recent
  benchmarks (e.g., MoleculeNet-like datasets, Therapeutics Data Commons)
  and current best practices.

## MD convergence and uncertainty

- **What**: replicate simulations, block averaging, autocorrelation, MSM
  validation.
- **When**: any time you interpret MD observables quantitatively.
- **Failure modes**: single trajectory, unreported equilibration, cherry-
  picked observables.
- **Validation**: independent replicates, per-observable convergence
  checks, reported uncertainty.
- **Web search**: occasionally — for force-field updates and simulation
  best-practices updates.

## MM/PBSA and MM/GBSA

- **What**: endpoint free-energy estimators.
- **When**: *relative* ranking of close analogs, with eyes open.
- **Failure modes**: absolute ΔG claims; inconsistent receptor preparation
  across compounds; ignoring entropy estimates; ignoring dielectric
  choices.
- **Validation**: known series with experimental ΔG; sensitivity analysis
  across dielectric and sampling parameters.
- **Web search**: recommended for current protocol recommendations.

## FEP / TI (alchemical free energy)

- **What**: rigorous relative free-energy methods between close analogs.
- **When**: small perturbations on a congeneric series with good structural
  data and adequate sampling resources.
- **Failure modes**: poor phase-space overlap; insufficient sampling;
  under-reported hysteresis; cycle closure failures.
- **Validation**: demonstrated convergence, cycle closure, hysteresis
  checks, replicate runs.
- **Web search**: recommended — methods and protocols evolve quickly.

## Pharmacophores

- **What**: 3D arrangement of pharmacophore features (H-bond donors/
  acceptors, hydrophobes, aromatics, charges).
- **When**: LBDD with known actives; scaffold hopping; virtual screening
  pre-filter.
- **Failure modes**: overfit to a single active; too-permissive features;
  ignoring stereochemistry.
- **Validation**: enrichment against decoys; scaffold diversity of hits.
- **Web search**: occasionally, for current tools.

## Matched molecular pairs (MMP)

- **What**: systematic analysis of single structural changes and their
  effects on properties.
- **When**: SAR analysis, design suggestions, property prediction by
  analogy.
- **Failure modes**: assuming transferability beyond the dataset; rare
  transformations with high variance.
- **Validation**: prospective hold-out predictions on MMP transformations.
- **Web search**: occasionally, for MMP tools and datasets.

## Scaffold splits

- **What**: train/test partitions by Bemis–Murcko scaffold.
- **When**: evaluating generalization across chemotypes.
- **Failure modes**: small dataset → scaffold imbalance; ring-opening or
  aromatic-shift edge cases.
- **Validation**: compare scaffold vs. random split metrics; report the
  gap.
- **Web search**: rarely.

## Deep learning for molecular property prediction

- **What**: GNNs, transformers, pretrained molecular encoders.
- **When**: large datasets; when beating gradient-boosted baselines matters
  and is demonstrated on your split strategy.
- **Failure modes**: overfitting on small datasets; leakage via pretraining
  data; nondeterminism without seeds; single-split overconfidence.
- **Validation**: compare against strong fingerprint + GBT baseline;
  scaffold/temporal split; report with replicates.
- **Web search**: highly recommended — this field moves quickly.

## Graph neural networks

- **What**: GCN, GAT, MPNN, graph transformers for molecules.
- **When**: structured data where graph topology matters.
- **Failure modes**: over-smoothing in deep GNNs; data hunger; sensitivity
  to hyperparameters; limited interpretability.
- **Validation**: as for deep learning above.
- **Web search**: recommended for current architectures.

## Protein language models

- **What**: large transformers trained on protein sequences (ESM family and
  others).
- **When**: sequence-based predictions, structure prediction assistance,
  representation learning for downstream tasks.
- **Failure modes**: domain shift; hallucinated features; test-set
  contamination with pretraining corpus.
- **Validation**: careful out-of-distribution tests; compare with simpler
  baselines.
- **Web search**: highly recommended — landscape changes rapidly.

## Active learning

- **What**: iterative label acquisition to maximize model improvement per
  experiment.
- **When**: small labeled sets, costly experiments, a real iteration budget.
- **Failure modes**: exploitation collapse; acquisition-function bias;
  unrealistic offline evaluation.
- **Validation**: retrospective simulation with held-out acquisition
  pools.
- **Web search**: recommended for current acquisition strategies and
  benchmarks.

## Generative molecular design — safety caveats

- **What**: models that propose novel molecular structures (SMILES/graph/3D
  generative models, reinforcement learning with scoring).
- **When**: exploratory design under supervised computational scoring
  functions with explicit applicability domain and safety review.
- **Failure modes**: producing synthetically inaccessible molecules;
  producing dual-use hazards; reward hacking; mode collapse; unvalidated
  property predictions being reinforced.
- **Validation**: synthetic accessibility scoring, retro-synthesis
  checks at a conceptual level (no procedural routes in this skill),
  property-prediction confidence, diversity of proposals.
- **Safety**: do not optimize toward toxicity, evasion, weaponization, or
  controlled-substance targets. See `safety-and-ethics.md`.
- **Web search**: recommended — this field is active and safety norms
  evolve.

## When to cite — and when not to

- Cite primary literature, reviews, or authoritative documentation when a
  claim is specific and consequential.
- Do not cite from memory if you are uncertain of authorship, year, or
  journal — retrieve it online or flag the claim as needing verification.
- Placeholders (e.g., `[Author et al., Journal, Year — verify]`) are
  acceptable in drafts as long as they are replaced or removed before
  delivery.
