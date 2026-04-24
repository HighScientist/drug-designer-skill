#!/usr/bin/env python3
"""Baseline QSAR / QSPR modeling with leakage-aware defaults.

Loads a CSV/TSV with a SMILES column and a target column, builds Morgan
fingerprints (via RDKit when available), and fits a simple scikit-learn
baseline with cross-validation.

Goals:
- Teach the correct shape of a validated baseline.
- Warn loudly about leakage risks (duplicates, near-duplicates, small data,
  single random split).
- Report metrics with fold-level uncertainty.

Limitations:
- Not a production modeling workflow.
- Does not compute applicability domain, calibration, or y-randomization
  (recommended as next steps, documented in the output).
- Read-only. No network access.

Example:
  qsar_baseline.py data.csv --smiles-col smiles --target-col pIC50 \\
      --task regression --cv 5 --seed 0
"""

from __future__ import annotations

import argparse
import os
import sys


def _import_core():
    try:
        import numpy as np
        import pandas as pd
        return np, pd
    except ImportError:
        print(
            "ERROR: numpy and pandas required.\n"
            "Install with:  pip install numpy pandas\n",
            file=sys.stderr,
        )
        sys.exit(2)


def _import_sklearn():
    try:
        import sklearn  # noqa: F401
        from sklearn.model_selection import cross_validate, KFold, StratifiedKFold
        from sklearn.ensemble import (
            RandomForestRegressor, RandomForestClassifier,
        )
        return {
            "cross_validate": cross_validate,
            "KFold": KFold,
            "StratifiedKFold": StratifiedKFold,
            "RandomForestRegressor": RandomForestRegressor,
            "RandomForestClassifier": RandomForestClassifier,
        }
    except ImportError:
        print(
            "ERROR: scikit-learn is required for qsar_baseline.py.\n"
            "Install with:  pip install scikit-learn\n",
            file=sys.stderr,
        )
        sys.exit(2)


def _import_rdkit_optional():
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
        return Chem, AllChem
    except ImportError:
        return None, None


def featurize(smiles_list, np, Chem, AllChem, radius: int, n_bits: int):
    """Return (features, valid_mask). Uses Morgan when RDKit is available.

    Falls back to a crude, reproducible hashing featurizer if RDKit is not
    installed, so the script can still demonstrate the workflow shape.
    """
    n = len(smiles_list)
    valid = np.zeros(n, dtype=bool)

    if Chem is not None and AllChem is not None:
        features = np.zeros((n, n_bits), dtype=np.uint8)
        for i, smi in enumerate(smiles_list):
            if not isinstance(smi, str) or not smi:
                continue
            mol = Chem.MolFromSmiles(smi)
            if mol is None:
                continue
            bv = AllChem.GetMorganFingerprintAsBitVect(
                mol, radius=radius, nBits=n_bits,
            )
            on_bits = list(bv.GetOnBits())
            features[i, on_bits] = 1
            valid[i] = True
        return features, valid, "morgan"

    # Fallback: hash-based multi-hot on SMILES substrings. Not a real
    # chemical descriptor — clearly labeled in the output.
    features = np.zeros((n, n_bits), dtype=np.uint8)
    for i, smi in enumerate(smiles_list):
        if not isinstance(smi, str) or not smi:
            continue
        for k in range(len(smi) - 2):
            tok = smi[k:k + 3]
            features[i, hash(tok) % n_bits] = 1
        valid[i] = True
    return features, valid, "hash-fallback"


def run(args, np, pd, sk):
    if not os.path.isfile(args.input):
        print(f"ERROR: file not found: {args.input}", file=sys.stderr)
        return 1

    ext = os.path.splitext(args.input)[1].lower()
    sep = "\t" if ext in (".tsv", ".tab") else ","
    df = pd.read_csv(args.input, sep=sep)

    for col in (args.smiles_col, args.target_col):
        if col not in df.columns:
            print(f"ERROR: column '{col}' not found.", file=sys.stderr)
            return 1

    print(f"Records loaded: {len(df)}")

    # Duplicate-check on SMILES string as a first pass (does not
    # canonicalize; see compound_qc.py for a stronger check).
    n_dupes = int(df[args.smiles_col].duplicated().sum())
    if n_dupes:
        print(f"WARNING: {n_dupes} duplicated SMILES rows detected. "
              "Deduplicate or justify retention before modeling; duplicates "
              "leak information across CV folds.")

    # Drop rows with missing target
    before = len(df)
    df = df.dropna(subset=[args.smiles_col, args.target_col]).reset_index(drop=True)
    print(f"After dropping rows with missing SMILES/target: {len(df)} "
          f"(removed {before - len(df)})")

    Chem, AllChem = _import_rdkit_optional()
    if Chem is None:
        print("WARNING: RDKit not available; using a hash-based fallback "
              "featurizer. Install RDKit for real Morgan fingerprints:  "
              "conda install -c conda-forge rdkit")

    X, valid, feat_name = featurize(
        df[args.smiles_col].tolist(), np, Chem, AllChem,
        radius=args.radius, n_bits=args.bits,
    )
    y = df[args.target_col].to_numpy()
    X = X[valid]
    y = y[valid]
    print(f"Featurizer: {feat_name}  shape: {X.shape}")

    if X.shape[0] < 20:
        print("WARNING: fewer than 20 valid rows; results will be unreliable.")

    if args.task == "regression":
        model = sk["RandomForestRegressor"](
            n_estimators=200, random_state=args.seed, n_jobs=-1,
        )
        splitter = sk["KFold"](
            n_splits=args.cv, shuffle=True, random_state=args.seed,
        )
        scoring = ["neg_root_mean_squared_error", "neg_mean_absolute_error", "r2"]
    else:
        model = sk["RandomForestClassifier"](
            n_estimators=300, random_state=args.seed, n_jobs=-1,
            class_weight="balanced",
        )
        splitter = sk["StratifiedKFold"](
            n_splits=args.cv, shuffle=True, random_state=args.seed,
        )
        scoring = ["roc_auc", "average_precision", "matthews_corrcoef"]

    print(f"Task: {args.task}")
    print(f"CV: {args.cv}-fold "
          f"({'stratified' if args.task == 'classification' else 'KFold'}), "
          f"seed={args.seed}")
    print("Model: sklearn RandomForest (baseline).")
    print()

    res = sk["cross_validate"](
        model, X, y, cv=splitter, scoring=scoring,
        return_train_score=False, n_jobs=-1,
    )

    print("Cross-validated metrics (mean ± std over folds):")
    for key in scoring:
        values = res[f"test_{key}"]
        label = key.replace("neg_", "").replace("_", "-")
        sign = -1.0 if key.startswith("neg_") else 1.0
        adj = sign * values
        print(f"  {label:28s} {adj.mean():.4f} ± {adj.std(ddof=1):.4f}"
              if len(adj) > 1 else
              f"  {label:28s} {adj.mean():.4f}")

    print()
    print("Caveats:")
    print("  - This is a RANDOM-split CV baseline. It typically OVERESTIMATES")
    print("    prospective performance. Re-run with scaffold or temporal")
    print("    splits before trusting any number for decision-making.")
    print("  - Duplicates / near-duplicates / stereo-isomer twins leak")
    print("    information across folds; see compound_qc.py for a cleaner pass.")
    print("  - Recommended next steps: scaffold split, external test set,")
    print("    y-randomization, applicability-domain analysis, calibration,")
    print("    uncertainty estimates.")
    print("  - Predicted activity is NOT experimental potency.")
    print()
    print("Reproducibility:")
    print(f"  command: qsar_baseline.py {args.input} "
          f"--smiles-col {args.smiles_col} "
          f"--target-col {args.target_col} --task {args.task} "
          f"--cv {args.cv} --seed {args.seed} "
          f"--radius {args.radius} --bits {args.bits}")
    return 0


def main() -> int:
    np, pd = _import_core()
    sk = _import_sklearn()

    parser = argparse.ArgumentParser(
        description="Baseline QSAR/QSPR modeling with leakage-aware defaults.",
    )
    parser.add_argument("input", help="CSV/TSV with SMILES and target columns.")
    parser.add_argument("--smiles-col", default="smiles")
    parser.add_argument("--target-col", default="target")
    parser.add_argument("--task", choices=("regression", "classification"),
                        default="regression")
    parser.add_argument("--cv", type=int, default=5)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--radius", type=int, default=2,
                        help="Morgan fingerprint radius (default 2).")
    parser.add_argument("--bits", type=int, default=2048,
                        help="Morgan fingerprint bit length (default 2048).")
    args = parser.parse_args()

    return run(args, np, pd, sk)


if __name__ == "__main__":
    sys.exit(main())
