# Molecular Dynamics Report — {{project_name}}

## Objective

- Scientific question:
- Observables of interest:

## System

- Starting structure (PDB ID / predicted model):
- Mutations, constructs, biological assembly:
- Ligand / cofactor / metal inclusion:
- Protonation / altloc / water decisions:
- Box type, size, ionization, net charge:

## Force field and parameters

- Protein force field:
- Ligand parameters (source, charge method):
- Water model:
- Ion parameters:
- Timestep, constraints:
- Thermostat / barostat:
- Cutoffs and long-range electrostatics:

## Protocol

- Minimization:
- Equilibration (stages, restraints, durations):
- Production:
  - Replicate count:
  - Simulated time per replicate:
  - Seeds:
- Hardware / runtime notes:

## Trajectory QC

- Imaging / unwrapping:
- Alignment selection:
- Equilibration cutoff (per replicate):
- Energy / temperature / pressure stability:
- Gross visual QC notes (no dissociated ligand, no exploded system, etc.):

## Core observables

- RMSD (selection, reference, per-replicate plot):
- RMSF (selection, per-residue, per-replicate):
- Radius of gyration:
- SASA (total / hydrophobic):
- Hydrogen bonds / salt bridges (criteria, occupancy):
- Distances / contact maps (selections and cutoffs):

## Higher-order analyses (if used)

- PCA / tICA:
- Clustering (method, parameters, cluster populations):
- MSM (states, lag time, CK test) — only with full validation:

## Convergence

- Per-observable convergence evidence:
- Agreement across replicates:
- Block-averaging summary:
- Statement: what is converged, what is not.

## Free-energy-adjacent analyses (if any)

- MM/PBSA / MM/GBSA (protocol, dielectric, entropy handling) — *relative*
  ranking only.
- FEP / TI (cycle closure, hysteresis, phase-space overlap).

## Results

- Findings with units and uncertainty.

## Interpretation

- Supported claims:
- Unsupported claims (explicitly):

## Limitations

- Force-field bias:
- Sampling scope:
- Starting-structure dependence:
- Single protonation/tautomer assumptions:

## Reproducibility

- Commands:
- Input files and hashes:
- Seeds.

## Recommended next computational steps

-
-
-

## Safety and scope

- MD does not prove therapeutic or clinical effect.
- Kinetic / thermodynamic claims require full validation, not one metric.
