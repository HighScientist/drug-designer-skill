# Docking / Virtual Screening Report — {{project_name}}

## Objective

- Task (pose prediction / binding-site characterization / virtual screen /
  triage):
- Intended downstream decision:

## Target and receptor

- PDB ID(s) / predicted model source:
- Chain(s), biological assembly:
- Resolution / confidence summary:
- Mutations, constructs, truncations:
- Cofactors, metals, conserved waters retained:
- Protonation / altloc / tautomer decisions:

## Binding site

- Site definition (reference ligand, residues, coordinates, detection tool):
- Grid / search box (coordinates and dimensions):
- Flexibility (rigid receptor, flexible side chains, induced fit):

## Ligand set

- Source and size:
- Preparation (salt stripping, tautomer policy, stereochemistry policy,
  canonicalization toolkit):
- Property filters applied:
- Any duplicates / near-duplicates removed:

## Docking protocol

- Tool + version:
- Scoring function:
- Exhaustiveness / iterations / seeds:
- Poses retained per ligand:

## Validation

- Redocking RMSD of native ligand:
- Cross-docking results (if applicable):
- Decoy set used (and known biases):
- Enrichment metrics (ROC-AUC, PR-AUC, EF@α, BEDROC@α):

## Pose analysis

- Pose clustering summary:
- Interaction fingerprint / key contacts:
- Visual inspection notes (implausible geometries? clashes? solvent
  exposure?):

## Results

- Top-ranked compounds / poses (with caveats about score vs. affinity):
- Distribution of scores and flags for outliers:

## Statistical / uncertainty notes

- Replicate seeds (if multiple runs):
- Score distribution caveats:

## Interpretation

- What can be concluded about binding *poses* vs. about binding *affinity*:
- What can be concluded about relative ranking within this protocol:

## Limitations

- Scoring-function limitations:
- Receptor conformation limitations (single snapshot vs. ensemble):
- Applicability of the docking protocol to the library diversity:

## Reproducibility

- Commands:
- Environment:
- Input hashes:

## Recommended next computational steps

- Rescoring with an independent scorer:
- MD refinement / MM/PBSA on top hits (relative only):
- Applicability-domain checks before any decision:

## Safety and scope

- Docking scores are not binding affinities.
- Recommendations for experimental validation are high-level only.
