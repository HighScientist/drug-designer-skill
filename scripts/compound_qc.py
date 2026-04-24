#!/usr/bin/env python3
"""Compound-library QC: validate SMILES, canonicalize, deduplicate, flag.

Given a CSV/TSV with a SMILES column, this script:

- Parses each molecule with RDKit.
- Records parse failures.
- Canonicalizes SMILES and computes InChIKeys.
- Flags duplicates on canonical SMILES AND on InChIKey.
- Computes a small set of descriptors (MW, LogP, TPSA, HBD, HBA,
  rotatable bonds, ring count, fraction sp3).
- Flags PAINS-style hits via a small, explicitly-partial SMARTS set
  (as ALERTS — never treat as truth).

Read-only by default: prints a summary and, if --out is provided, writes
a new table with added columns. Never overwrites the input.

Requires RDKit. Exits gracefully if RDKit is missing.
"""

from __future__ import annotations

import argparse
import os
import sys


# A deliberately small, illustrative set of frequent-assay-interference
# SMARTS. This is NOT a full PAINS library. Treat hits as hypotheses and
# consult a current filter set for real library triage.
ALERT_SMARTS = {
    "quinone": "O=C1C=CC(=O)C=C1",
    "catechol": "c1cc(O)c(O)cc1",
    "rhodanine_core": "O=C1CSC(=S)N1",
    "thiourea": "NC(=S)N",
    "azo": "N=N",
    "aldehyde_generic": "[CX3H1](=O)[#6]",
    "michael_acceptor_enone": "C=CC(=O)[#6]",
}


def _import_rdkit():
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
        from rdkit.Chem.MolStandardize import rdMolStandardize
        from rdkit import RDLogger
        RDLogger.DisableLog("rdApp.*")
        return {
            "Chem": Chem,
            "AllChem": AllChem,
            "Descriptors": Descriptors,
            "rdMolDescriptors": rdMolDescriptors,
            "rdMolStandardize": rdMolStandardize,
        }
    except ImportError:
        print(
            "ERROR: RDKit is required for compound_qc.py.\n"
            "Install with:  conda install -c conda-forge rdkit\n",
            file=sys.stderr,
        )
        sys.exit(2)


def _import_pandas():
    try:
        import pandas as pd
        import numpy as np
        return pd, np
    except ImportError:
        print(
            "ERROR: pandas and numpy required.\n"
            "Install with:  pip install pandas numpy\n",
            file=sys.stderr,
        )
        sys.exit(2)


def standardize(mol, rd):
    try:
        lfc = rd["rdMolStandardize"].LargestFragmentChooser()
        mol = lfc.choose(mol)
        uncharger = rd["rdMolStandardize"].Uncharger()
        mol = uncharger.uncharge(mol)
    except Exception:
        pass
    return mol


def compute_row(smi, rd):
    Chem = rd["Chem"]
    Descriptors = rd["Descriptors"]
    rdMolDescriptors = rd["rdMolDescriptors"]

    out = {
        "parse_ok": False,
        "canonical_smiles": None,
        "inchikey": None,
        "mw": None, "logp": None, "tpsa": None,
        "hbd": None, "hba": None, "rot_bonds": None,
        "rings": None, "fraction_sp3": None,
        "alerts": "",
    }
    if not isinstance(smi, str) or not smi.strip():
        return out
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return out

    mol = standardize(mol, rd)
    if mol is None:
        return out

    try:
        canon = Chem.MolToSmiles(mol)
        ik = Chem.MolToInchiKey(mol) or None
    except Exception:
        return out

    out["parse_ok"] = True
    out["canonical_smiles"] = canon
    out["inchikey"] = ik

    try:
        out["mw"] = float(Descriptors.MolWt(mol))
        out["logp"] = float(Descriptors.MolLogP(mol))
        out["tpsa"] = float(rdMolDescriptors.CalcTPSA(mol))
        out["hbd"] = int(rdMolDescriptors.CalcNumHBD(mol))
        out["hba"] = int(rdMolDescriptors.CalcNumHBA(mol))
        out["rot_bonds"] = int(rdMolDescriptors.CalcNumRotatableBonds(mol))
        out["rings"] = int(rdMolDescriptors.CalcNumRings(mol))
        out["fraction_sp3"] = float(rdMolDescriptors.CalcFractionCSP3(mol))
    except Exception:
        pass

    alerts = []
    for name, smarts in ALERT_SMARTS.items():
        patt = Chem.MolFromSmarts(smarts)
        if patt is not None and mol.HasSubstructMatch(patt):
            alerts.append(name)
    out["alerts"] = ";".join(alerts)
    return out


def run(args, rd, pd, np):
    if not os.path.isfile(args.input):
        print(f"ERROR: file not found: {args.input}", file=sys.stderr)
        return 1

    ext = os.path.splitext(args.input)[1].lower()
    sep = "\t" if ext in (".tsv", ".tab") else ","
    df = pd.read_csv(args.input, sep=sep)

    if args.smiles_col not in df.columns:
        print(f"ERROR: column '{args.smiles_col}' not found.", file=sys.stderr)
        return 1

    rows = [compute_row(smi, rd) for smi in df[args.smiles_col].tolist()]
    qc_df = pd.DataFrame(rows)
    combined = pd.concat(
        [df.reset_index(drop=True), qc_df.reset_index(drop=True)], axis=1,
    )

    total = len(combined)
    ok = int(qc_df["parse_ok"].sum())
    bad = total - ok
    dup_smi = int(
        combined.loc[combined["parse_ok"], "canonical_smiles"]
        .duplicated(keep=False).sum()
    )
    dup_ik = int(
        combined.loc[combined["parse_ok"], "inchikey"]
        .dropna().duplicated(keep=False).sum()
    )
    n_alerts = int((qc_df["alerts"].fillna("") != "").sum())

    print(f"Input rows: {total}")
    print(f"Parsed OK:  {ok}")
    print(f"Parse failures: {bad}")
    print(f"Duplicates on canonical SMILES: {dup_smi}")
    print(f"Duplicates on InChIKey:         {dup_ik}")
    print(f"Rows with at least one alert flag: {n_alerts}")
    print()

    valid = qc_df.loc[qc_df["parse_ok"]]
    if not valid.empty:
        print("Descriptor summary (parsed rows only):")
        for col in ("mw", "logp", "tpsa", "hbd", "hba", "rot_bonds",
                    "rings", "fraction_sp3"):
            s = valid[col].dropna()
            if s.empty:
                continue
            print(f"  {col:13s} mean={s.mean():.3f}  median={s.median():.3f}  "
                  f"min={s.min():.3f}  max={s.max():.3f}")
    print()

    if args.out:
        if os.path.abspath(args.out) == os.path.abspath(args.input):
            print("ERROR: refusing to overwrite the input file. "
                  "Pass a different --out path.", file=sys.stderr)
            return 1
        out_ext = os.path.splitext(args.out)[1].lower()
        out_sep = "\t" if out_ext in (".tsv", ".tab") else ","
        combined.to_csv(args.out, sep=out_sep, index=False)
        print(f"Wrote QC table with added columns to: {args.out}")
        print()

    print("Caveats:")
    print("  - Alerts flag SUBSTRUCTURES historically associated with assay")
    print("    interference. They are hypotheses, not proofs; do not auto-reject.")
    print("  - The alert set here is a small illustrative subset; consult")
    print("    a current, maintained filter set for real library triage.")
    print("  - Standardization settings (tautomer/stereochemistry policy)")
    print("    should be pinned across a project for consistency.")
    print()
    print("Reproducibility:")
    cmd = (f"compound_qc.py {args.input} --smiles-col {args.smiles_col}"
           + (f" --out {args.out}" if args.out else ""))
    print(f"  command: {cmd}")
    return 0


def main() -> int:
    rd = _import_rdkit()
    pd, np = _import_pandas()

    parser = argparse.ArgumentParser(
        description="Compound-library QC: parse, canonicalize, deduplicate, flag.",
    )
    parser.add_argument("input", help="CSV/TSV input path.")
    parser.add_argument("--smiles-col", default="smiles")
    parser.add_argument("--out", default=None,
                        help="Optional output path with added QC columns. "
                             "Refuses to overwrite the input.")
    args = parser.parse_args()

    return run(args, rd, pd, np)


if __name__ == "__main__":
    sys.exit(main())
