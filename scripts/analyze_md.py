#!/usr/bin/env python3
"""Basic MD trajectory analysis using MDAnalysis.

Computes: frame count, total simulated time (from dt), RMSD (Cα),
RMSF (Cα), radius of gyration, and optional distance time series
between two atom selections.

Read-only. No network access. Optional dependency: MDAnalysis.

Example:
  analyze_md.py --topology system.pdb --trajectory traj.xtc
  analyze_md.py --topology system.psf --trajectory traj.dcd \\
      --selection-a "resid 42 and name CA" \\
      --selection-b "resid 77 and name CA"
"""

from __future__ import annotations

import argparse
import os
import sys


def _import_mda():
    try:
        import MDAnalysis as mda
        from MDAnalysis.analysis import rms
        import numpy as np
        return mda, rms, np
    except ImportError:
        print(
            "ERROR: MDAnalysis (and numpy) are required for analyze_md.py.\n"
            "Install with:  pip install MDAnalysis numpy\n",
            file=sys.stderr,
        )
        sys.exit(2)


def describe_universe(u, np) -> None:
    print(f"Atoms: {u.atoms.n_atoms}")
    print(f"Residues: {u.residues.n_residues}")
    print(f"Segments: {u.segments.n_segments}")
    n_frames = len(u.trajectory)
    print(f"Frames: {n_frames}")
    try:
        dt = float(u.trajectory.dt)
        total = dt * n_frames
        print(f"dt per frame (ps): {dt:.3f}")
        print(f"Total simulated time covered (ps): {total:.3f}")
    except Exception:
        print("dt / total time: not available from trajectory metadata")


def compute_rmsd_rmsf(u, rms, np) -> None:
    ca = u.select_atoms("protein and name CA")
    if ca.n_atoms == 0:
        print("No protein Cα atoms found; skipping RMSD/RMSF.")
        return

    # RMSD trajectory against first frame
    u.trajectory[0]
    ref_positions = ca.positions.copy()

    rmsd_values = []
    for ts in u.trajectory:
        # Align on Cα with translation + rotation
        from MDAnalysis.analysis.align import alignto
        alignto(u, u, select="protein and name CA", in_memory=False)
        diff = ca.positions - ref_positions
        rmsd_val = float(np.sqrt((diff ** 2).sum() / ca.n_atoms))
        rmsd_values.append(rmsd_val)

    arr = np.array(rmsd_values)
    print()
    print("RMSD (Cα vs. first frame, Å):")
    print(f"  frames: {arr.size}")
    print(f"  mean:   {arr.mean():.3f}")
    print(f"  std:    {arr.std(ddof=1):.3f}" if arr.size > 1 else
          "  std:    n/a")
    print(f"  min:    {arr.min():.3f}")
    print(f"  max:    {arr.max():.3f}")

    # RMSF per Cα residue (simple pass)
    positions_stack = []
    for ts in u.trajectory:
        positions_stack.append(ca.positions.copy())
    stack = np.array(positions_stack)  # (frames, atoms, 3)
    mean_pos = stack.mean(axis=0)
    fluct = stack - mean_pos
    rmsf = np.sqrt((fluct ** 2).sum(axis=2).mean(axis=0))
    print()
    print("RMSF (Cα, Å) summary:")
    print(f"  residues: {rmsf.size}")
    print(f"  mean: {rmsf.mean():.3f}")
    print(f"  max:  {rmsf.max():.3f} at residue index {int(rmsf.argmax())}")


def compute_rg(u, np) -> None:
    protein = u.select_atoms("protein")
    if protein.n_atoms == 0:
        print("No protein atoms; skipping Rg.")
        return
    rg_values = []
    for ts in u.trajectory:
        rg_values.append(float(protein.radius_of_gyration()))
    arr = np.array(rg_values)
    print()
    print("Radius of gyration (protein, Å):")
    print(f"  mean: {arr.mean():.3f}")
    print(f"  std:  {arr.std(ddof=1):.3f}" if arr.size > 1 else "  std: n/a")
    print(f"  min:  {arr.min():.3f}")
    print(f"  max:  {arr.max():.3f}")


def compute_distance(u, sel_a: str, sel_b: str, np) -> None:
    a = u.select_atoms(sel_a)
    b = u.select_atoms(sel_b)
    if a.n_atoms == 0 or b.n_atoms == 0:
        print(f"WARNING: empty selection; A='{sel_a}' has {a.n_atoms} atoms, "
              f"B='{sel_b}' has {b.n_atoms} atoms. Skipping distance.")
        return
    values = []
    for ts in u.trajectory:
        ca = a.center_of_geometry()
        cb = b.center_of_geometry()
        values.append(float(np.linalg.norm(ca - cb)))
    arr = np.array(values)
    print()
    print(f"Distance (center-of-geometry) between '{sel_a}' and '{sel_b}' (Å):")
    print(f"  frames: {arr.size}")
    print(f"  mean: {arr.mean():.3f}")
    print(f"  std:  {arr.std(ddof=1):.3f}" if arr.size > 1 else "  std: n/a")
    print(f"  min:  {arr.min():.3f}")
    print(f"  max:  {arr.max():.3f}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Basic MD trajectory QC and observables via MDAnalysis.",
    )
    parser.add_argument("--topology", required=True,
                        help="Topology/structure file (PDB/PSF/PRMTOP/GRO).")
    parser.add_argument("--trajectory", required=True,
                        help="Trajectory file (XTC/DCD/TRR/NC).")
    parser.add_argument("--selection-a", default=None,
                        help="Optional first selection for distance analysis.")
    parser.add_argument("--selection-b", default=None,
                        help="Optional second selection for distance analysis.")
    args = parser.parse_args()

    mda, rms, np = _import_mda()

    for p in (args.topology, args.trajectory):
        if not os.path.isfile(p):
            print(f"ERROR: file not found: {p}", file=sys.stderr)
            return 1

    u = mda.Universe(args.topology, args.trajectory)

    print(f"Topology:   {args.topology}")
    print(f"Trajectory: {args.trajectory}")
    print()
    describe_universe(u, np)

    compute_rmsd_rmsf(u, rms, np)
    compute_rg(u, np)

    if args.selection_a and args.selection_b:
        compute_distance(u, args.selection_a, args.selection_b, np)
    elif bool(args.selection_a) ^ bool(args.selection_b):
        print("WARNING: --selection-a and --selection-b must be provided "
              "together; skipping distance analysis.")

    print()
    print("Caveats:")
    print("  - Single-metric and single-trajectory results do not prove")
    print("    convergence; replicate simulations and inspect multiple")
    print("    observables.")
    print("  - RMSF here is a per-Cα estimate on the raw trajectory;")
    print("    prefer aligned + equilibrated-only trajectories for claims.")
    print()
    print("Reproducibility:")
    print(f"  command: analyze_md.py --topology {args.topology} "
          f"--trajectory {args.trajectory}"
          + (f" --selection-a \"{args.selection_a}\"" if args.selection_a else "")
          + (f" --selection-b \"{args.selection_b}\"" if args.selection_b else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
