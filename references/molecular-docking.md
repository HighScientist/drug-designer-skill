# Molecular docking — methods and validation

Docking predicts ligand poses in a receptor and ranks them with a fast
scoring function. It is a hypothesis-generation tool, not a binding-affinity
measurement. Treat every claim accordingly.

## Receptor preparation

- Pick a structure with: good resolution in the pocket, relevant ligand in
  the site (for holo runs), and no severe clashes or missing backbone near
  the binding region.
- Cap termini, add hydrogens, assign protonation states at the target pH
  using a defensible tool (e.g., PROPKA-style logic). Document residues with
  non-standard states (e.g., protonated histidines, deprotonated cysteines).
- Decide on waters deliberately: bulk water out; conserved, pocket-bridging,
  or catalytic waters retained (and documented).
- Resolve alternate locations (altlocs). Usually keep the highest-occupancy
  conformer, but justify the choice per residue when it matters.
- Handle cofactors, metals, covalent modifications explicitly — blanket
  removal of HETATMs is a common silent bug.

## Ligand preparation

- Canonicalize SMILES; strip salts; standardize tautomers and protonation at
  the target pH.
- Enumerate stereoisomers when stereochemistry is ambiguous. Flag any
  enumeration in the report.
- Generate 3D conformers appropriate for the docking tool (many modern
  dockers accept 2D input and conform internally; verify).

## Grid / search space

- Define the search box from a co-crystal ligand, a known site, or a
  pocket-detection tool. Document coordinates and dimensions.
- Box too small → artificially constrained poses. Box too large → random
  scatter and score inflation.
- For flexible-receptor or induced-fit workflows, document which side chains
  are flexible and why.

## Validation

### Redocking (self-docking)

- Dock the native ligand back into its structure. Pose RMSD < 2.0 Å to the
  crystal pose is a common (not universal) success threshold for medium-sized
  ligands; for small fragments use stricter cutoffs.
- Failure indicates a preparation or scoring problem — fix before running
  the production experiment.

### Cross-docking

- Dock the ligand of structure A into the prepared receptor from structure B
  (similar target, different conformation). Reveals sensitivity to
  conformational plasticity.

### Decoys

- For virtual-screening benchmarks, use property-matched decoys. DUD-E is
  widely used but has documented biases; when you use it, acknowledge them
  and consider DEKOIS, DUDE-Z, or custom matched decoys as sanity checks.
  See `literature-grounding.md`.

## Enrichment and classification metrics

- **ROC-AUC**: overall ranking quality; insensitive to class imbalance — can
  flatter a model on a screen-like (highly imbalanced) dataset.
- **PR-AUC**: more informative than ROC-AUC under strong class imbalance.
- **Enrichment Factor (EF)** at α (e.g., EF1%, EF5%): how much better than
  random among the top α fraction. Practical for triage.
- **BEDROC**: weights early recognition more strongly than AUC; pairs well
  with α near the screening threshold.

Report at least two of these, plus the operating point you care about.

## Consensus scoring

- Averaging or rank-fusing scores from multiple, diverse scoring functions
  can stabilize rankings, but only when the functions make independent
  errors. Report each component.
- Do not compare raw scores across scoring functions; compare ranks or
  z-scores.

## Pose analysis

- **Pose clustering** (e.g., by RMSD within the receptor frame) reveals
  score–geometry disagreements and highlights near-degenerate poses.
- **Interaction fingerprints** (PLIF / SPLIF / IChem-style) summarize
  contacts as a bit-vector for comparison and consensus.
- Visual inspection of the top poses remains essential — scripts alone miss
  steric clashes, bad geometries, and physically implausible contacts.

## Docking score caveats (state every time)

- Scores are force-field- or empirical-function biased. They correlate weakly
  and inconsistently with ΔG.
- Do not convert docking scores into Kd, Ki, IC50, or binding-affinity
  language.
- Absolute score numbers are often not comparable between runs if receptor,
  box, or protonation state differs.
- Ranking is only meaningful within a consistent protocol and a reasonable
  applicability domain.

## Tools (check the web for current versions, licenses, recommended
parameters)

Common choices include AutoDock Vina / AD4, Smina, Glide, GOLD, FlexX, rDock,
DOCK, Surflex, Gnina (ML-rescored), DiffDock and similar deep-learning
dockers. Each has different licensing, parameter defaults, and known failure
modes. Validate on your system before trusting any of them for ranking.
