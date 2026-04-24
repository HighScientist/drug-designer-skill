#!/usr/bin/env python3
"""Inspect a PDB or mmCIF structure and summarize its contents.

Reports chains, residue counts, ligands (HETATMs), waters, metals,
alternate locations, insertion codes, and common structural flags
(missing backbone atoms, non-standard residues, unusual B-factors).

Requires Biopython. If Biopython is not installed, the script prints a
clear install suggestion and exits with a non-zero status.

This script is read-only and does not access the network.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import Counter, defaultdict

STANDARD_AA = {
    "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS",
    "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP",
    "TYR", "VAL",
    "MSE",  # often treated as methionine
}

STANDARD_NT = {"DA", "DC", "DG", "DT", "DU", "A", "C", "G", "T", "U"}

COMMON_METALS = {
    "ZN", "MG", "CA", "FE", "MN", "NI", "CU", "NA", "K", "CO", "CD",
    "HG", "PT", "AU", "PB", "AL",
}

WATER_NAMES = {"HOH", "WAT", "H2O", "DOD"}


def _import_biopython():
    try:
        from Bio.PDB import PDBParser, MMCIFParser
        return PDBParser, MMCIFParser
    except ImportError:
        print(
            "ERROR: Biopython is required for inspect_structure.py.\n"
            "Install it with:  pip install biopython\n",
            file=sys.stderr,
        )
        sys.exit(2)


def parse_structure(path: str):
    PDBParser, MMCIFParser = _import_biopython()
    ext = os.path.splitext(path)[1].lower()
    if ext in (".cif", ".mmcif"):
        parser = MMCIFParser(QUIET=True)
    else:
        parser = PDBParser(QUIET=True)
    structure_id = os.path.basename(path)
    return parser.get_structure(structure_id, path)


def summarize(structure, path: str) -> dict:
    summary = {
        "path": path,
        "models": 0,
        "chains": [],
        "residue_counts": {},
        "nonstandard_residues": Counter(),
        "ligands": Counter(),
        "metals": Counter(),
        "waters": 0,
        "altlocs": 0,
        "insertion_codes": 0,
        "missing_backbone": [],
        "high_b_factor_residues": [],
    }

    for model in structure:
        summary["models"] += 1
        for chain in model:
            chain_id = chain.id or "_"
            residues = list(chain)
            protein_res = 0
            nt_res = 0
            for res in residues:
                hetflag, resseq, icode = res.id
                resname = res.get_resname().strip()

                if icode.strip():
                    summary["insertion_codes"] += 1

                # altlocs
                for atom in res:
                    if atom.get_altloc().strip():
                        summary["altlocs"] += 1
                        break

                if resname in WATER_NAMES:
                    summary["waters"] += 1
                    continue

                if resname in COMMON_METALS and hetflag.strip():
                    summary["metals"][resname] += 1
                    continue

                if hetflag.strip():  # any other HETATM
                    summary["ligands"][resname] += 1
                    continue

                if resname in STANDARD_AA:
                    protein_res += 1
                    needed = {"N", "CA", "C", "O"}
                    present = {a.get_name() for a in res}
                    if not needed.issubset(present):
                        summary["missing_backbone"].append(
                            f"{chain_id}:{resname}{resseq}"
                        )
                    # crude B-factor flag
                    bvals = [a.get_bfactor() for a in res]
                    if bvals and max(bvals) > 100.0:
                        summary["high_b_factor_residues"].append(
                            f"{chain_id}:{resname}{resseq} (maxB={max(bvals):.1f})"
                        )
                elif resname in STANDARD_NT:
                    nt_res += 1
                else:
                    summary["nonstandard_residues"][resname] += 1

            summary["chains"].append({
                "chain_id": chain_id,
                "protein_residues": protein_res,
                "nucleotide_residues": nt_res,
                "total_items": len(residues),
            })
        break  # only first model for this summary; note count above

    return summary


def print_summary(summary: dict) -> None:
    path = summary["path"]
    print(f"=== Structure inspection: {path} ===")
    print(f"Models in file: {summary['models']}")
    print()
    print("Chains (first model):")
    for ch in summary["chains"]:
        print(
            f"  chain {ch['chain_id']}: "
            f"{ch['protein_residues']} protein, "
            f"{ch['nucleotide_residues']} nt, "
            f"{ch['total_items']} total residue records"
        )
    print()

    if summary["ligands"]:
        print("Ligands / non-standard HETATMs:")
        for name, count in summary["ligands"].most_common():
            print(f"  {name}: {count}")
    else:
        print("Ligands / non-standard HETATMs: none")
    print()

    if summary["metals"]:
        print("Metal ions:")
        for name, count in summary["metals"].most_common():
            print(f"  {name}: {count}")
    else:
        print("Metal ions: none")
    print()

    print(f"Waters: {summary['waters']}")
    print(f"Alternate-location residues: {summary['altlocs']}")
    print(f"Insertion-code residues: {summary['insertion_codes']}")
    print()

    if summary["nonstandard_residues"]:
        print("Non-standard (polymer) residues:")
        for name, count in summary["nonstandard_residues"].most_common():
            print(f"  {name}: {count}")
        print()

    if summary["missing_backbone"]:
        print("Residues with missing backbone atoms (N/CA/C/O):")
        for r in summary["missing_backbone"][:50]:
            print(f"  {r}")
        if len(summary["missing_backbone"]) > 50:
            print(f"  ... and {len(summary['missing_backbone']) - 50} more")
        print()

    if summary["high_b_factor_residues"]:
        print("Residues with very high B-factor (max > 100):")
        for r in summary["high_b_factor_residues"][:25]:
            print(f"  {r}")
        if len(summary["high_b_factor_residues"]) > 25:
            print(f"  ... and {len(summary['high_b_factor_residues']) - 25} more")
        print()

    print("Reproducibility:")
    print(f"  command: inspect_structure.py {path}")
    print("  tool: Biopython PDB/MMCIF parser")
    print()
    print("Caveats:")
    print("  - This is a syntactic inspection, not a biological validation.")
    print("  - Ligand/water/metal classification is heuristic; verify manually.")
    print("  - Computational inspection does not prove structural correctness.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect a PDB/mmCIF file and summarize its contents.",
    )
    parser.add_argument(
        "input",
        help="Path to a .pdb or .cif/.mmcif file.",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"ERROR: file not found: {args.input}", file=sys.stderr)
        return 1

    structure = parse_structure(args.input)
    summary = summarize(structure, args.input)
    print_summary(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
