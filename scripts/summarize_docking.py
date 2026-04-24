#!/usr/bin/env python3
"""Summarize a docking or virtual-screening results table.

Expects a CSV or TSV with at least an identifier column and a score
column. Produces: record count, missing-score count, duplicate count,
score distribution summary, and the top-N compounds by score.

Notes:
- Lower docking scores are better for most scoring functions
  (AutoDock/Vina/Smina conventions). Use --higher-is-better to flip.
- This script does NOT convert scores to binding affinity.
- Read-only, no network access.

Requires: pandas (and numpy). Exits with a clear install hint if missing.
"""

from __future__ import annotations

import argparse
import os
import sys


def _import_pandas():
    try:
        import pandas as pd
        import numpy as np
        return pd, np
    except ImportError:
        print(
            "ERROR: pandas and numpy are required for summarize_docking.py.\n"
            "Install with:  pip install pandas numpy\n",
            file=sys.stderr,
        )
        sys.exit(2)


def load_table(path: str, pd):
    ext = os.path.splitext(path)[1].lower()
    sep = "\t" if ext in (".tsv", ".tab") else ","
    df = pd.read_csv(path, sep=sep)
    return df


def summarize(df, id_col: str, score_col: str, higher_is_better: bool,
              top_n: int, pd, np) -> None:
    n = len(df)
    print(f"Records loaded: {n}")
    print(f"Columns: {list(df.columns)}")
    print()

    if id_col not in df.columns:
        print(f"ERROR: ID column '{id_col}' not found.", file=sys.stderr)
        sys.exit(1)
    if score_col not in df.columns:
        print(f"ERROR: Score column '{score_col}' not found.", file=sys.stderr)
        sys.exit(1)

    missing = df[score_col].isna().sum()
    print(f"Missing scores: {missing}")

    dup_ids = df[id_col].duplicated(keep=False)
    print(f"Duplicate IDs: {int(dup_ids.sum())}")

    finite = df[score_col].dropna()
    if finite.empty:
        print("All scores missing. Nothing to rank.")
        return

    print()
    print(f"Score column: '{score_col}'  "
          f"(higher is better: {higher_is_better})")
    print(f"  count: {finite.size}")
    print(f"  mean:  {finite.mean():.4f}")
    print(f"  std:   {finite.std(ddof=1):.4f}" if finite.size > 1 else
          "  std:   n/a")
    print(f"  min:   {finite.min():.4f}")
    print(f"  p05:   {finite.quantile(0.05):.4f}")
    print(f"  p25:   {finite.quantile(0.25):.4f}")
    print(f"  p50:   {finite.median():.4f}")
    print(f"  p75:   {finite.quantile(0.75):.4f}")
    print(f"  p95:   {finite.quantile(0.95):.4f}")
    print(f"  max:   {finite.max():.4f}")

    # detect suspicious bunching (many identical scores)
    mode_val = finite.mode().iloc[0] if not finite.mode().empty else None
    mode_freq = int((finite == mode_val).sum()) if mode_val is not None else 0
    if mode_val is not None and mode_freq > max(5, 0.05 * finite.size):
        print(
            f"  note: {mode_freq} records share the score {mode_val:.4f} "
            f"({100 * mode_freq / finite.size:.1f}%); check for parsing or "
            "scoring-saturation issues."
        )
    print()

    ascending = not higher_is_better
    ranked = df.dropna(subset=[score_col]).sort_values(
        score_col, ascending=ascending
    )
    print(f"Top {top_n} by score:")
    top = ranked.head(top_n)
    for _, row in top.iterrows():
        print(f"  {row[id_col]}\t{row[score_col]:.4f}")
    print()

    print("Caveats:")
    print("  - Docking scores are not binding affinities.")
    print("  - Ranking is only valid within a consistent protocol.")
    print("  - Always validate with redocking/cross-docking and visual inspection.")
    print()
    print("Reproducibility:")
    print(f"  command: summarize_docking.py --id-col {id_col} "
          f"--score-col {score_col} "
          f"{'--higher-is-better ' if higher_is_better else ''}"
          f"--top {top_n} {os.path.basename(sys.argv[-1])}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize docking / virtual-screening results.",
    )
    parser.add_argument("input", help="CSV or TSV path.")
    parser.add_argument(
        "--id-col", default="id",
        help="Column with compound identifiers (default: 'id').",
    )
    parser.add_argument(
        "--score-col", default="score",
        help="Column with docking scores (default: 'score').",
    )
    parser.add_argument(
        "--higher-is-better", action="store_true",
        help="Flip ranking direction (for scoring functions where higher "
             "scores are better).",
    )
    parser.add_argument(
        "--top", type=int, default=20,
        help="How many top-ranked records to list (default: 20).",
    )
    args = parser.parse_args()

    pd, np = _import_pandas()

    if not os.path.isfile(args.input):
        print(f"ERROR: file not found: {args.input}", file=sys.stderr)
        return 1

    df = load_table(args.input, pd)
    summarize(
        df,
        id_col=args.id_col,
        score_col=args.score_col,
        higher_is_better=args.higher_is_better,
        top_n=max(1, args.top),
        pd=pd,
        np=np,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
