# Molecular dynamics — analysis and caveats

MD generates a sample from a (finite, biased) trajectory of a force-field
model of your system. Analysis is about turning that sample into defensible
statements about equilibrium ensembles or kinetic hypotheses. Both are easy
to overclaim.

## Trajectory QC first — always

Before any science:

- Unwrap PBC consistently; re-image around the solute.
- Remove or align rigid-body motion by superposing on a stable reference
  selection (often backbone C-alpha of structured regions).
- Check timestep, output stride, and total simulated time.
- Visualize the first/middle/last frames in PyMOL or VMD to spot exploded
  systems, dissociated ligands, or cofactor drift.
- Confirm temperature, pressure, and energy are stable in the production
  region.

## Equilibration vs. production

- Discard the equilibration portion explicitly. Do not assume a fixed
  10 ns/20 ns cutoff — inspect observables and keep only the statistically
  stationary region.
- If the observable you care about is still drifting at the end, your run is
  not converged for *that* observable, regardless of energy plateaus.

## Core observables

- **RMSD** (backbone or C-alpha, after superposition): global stability. A
  plateau is necessary but not sufficient for convergence.
- **RMSF** per residue: local flexibility. Useful for highlighting hinges,
  flexible loops, and allosteric movement.
- **Radius of gyration (Rg)**: compactness. Useful for folding/unfolding
  trends and for multi-domain rearrangements.
- **SASA** (total, hydrophobic, residue-wise): exposure changes; binding
  pocket opening/closing.
- **Hydrogen bonds / salt bridges**: occupancy over the trajectory for
  specific interactions. Report donor–acceptor criteria explicitly.
- **Contact maps and distance timeseries**: good for ligand pose stability
  and specific residue–ligand interactions.

## Higher-order analyses

- **PCA / essential dynamics**: project onto principal modes of backbone
  motion to summarize dominant conformational directions.
- **tICA**: for slow processes and kinetic distances, commonly used with
  Markov state models.
- **Clustering** (e.g., RMSD-based, density-based): summarize conformational
  ensembles; report cluster populations with uncertainty.
- **Markov state models**: require careful lag-time selection, implied
  timescale checks, and validation (CK tests). Do not assert kinetics from a
  single model without these.

## Uncertainty, replicates, and convergence

- Run **independent replicates** with different initial velocities (and
  ideally different starting conformations). Report observables as mean ±
  stddev over replicates.
- Use **block averaging** within a single trajectory for autocorrelated
  observables. Report block size and whether blocks are statistically
  independent.
- **Convergence is per-observable.** An RMSD plateau does not imply a
  converged binding affinity estimate or a converged loop-state population.
- Check agreement across replicates before claiming convergence.

## Free-energy-adjacent caveats

- MM/PBSA and MM/GBSA are endpoint methods with strong assumptions. They may
  rank a congeneric series acceptably; absolute numbers are rarely
  meaningful.
- FEP/TI needs cycle closure, hysteresis checks, and phase-space overlap
  diagnostics. A converged ΔΔG requires demonstrated convergence, not just
  a completed run.

## Common software

- **MDAnalysis** (Python): general trajectory analysis, selection language,
  RMSD/RMSF/contacts, SASA (via external tools).
- **MDTraj** (Python): fast RMSD/contacts/secondary structure.
- **CPPTRAJ** (AmberTools): robust trajectory processing, RMSD/RMSF, H-bonds,
  clustering.
- **GROMACS tools** (`gmx rms`, `gmx rmsf`, `gmx gyrate`, `gmx sasa`,
  `gmx hbond`, `gmx cluster`, `gmx covar`/`gmx anaeig`).
- **VMD / PyMOL**: visual QC and per-frame inspection.
- **Bio3D** (R): trajectory analysis, PCA, cross-correlation analysis.

Check current docs for APIs and flags — they drift across versions.

## Reporting MD — checklist

- Force field + water model + ion parameters.
- Box type, box size, ionization, net charge.
- Minimization, equilibration, production protocols with timings.
- Timestep, constraints, thermostat/barostat, cutoffs, long-range
  electrostatics.
- Replicate count, total simulated time, production window used.
- Analysis selections, definitions (H-bond criteria, contact cutoffs),
  alignment selection.
- Convergence evidence per observable.
- Limitations: force-field bias, sampling scope, single-protonation
  assumptions, starting-structure dependence.
