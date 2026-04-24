# Python and R tooling — orient quickly, verify online

This is a *map*, not a reference manual. APIs drift; when a specific call
matters, check the official documentation online.

## Python — data and science stack

### pandas

- Use for tabular data wrangling; keep dtypes explicit.
- Prefer `pd.read_csv(..., dtype=...)` to let-pandas-guess.
- For chemistry CSVs, watch out for SMILES columns getting autoparsed or
  quoted inconsistently.

### numpy

- Core numerical arrays; broadcast carefully, especially across time/atom
  axes in MD analysis.
- Be explicit about dtypes (float32 vs. float64) in long trajectories to
  manage memory.

### scipy

- `scipy.stats` for hypothesis tests, distributions, correlation.
- `scipy.spatial` for distance metrics and KD-trees (neighbor searches in
  3D).
- `scipy.cluster` for hierarchical clustering.

### statsmodels

- Linear/GLM models with rich diagnostics; preferable to scikit-learn when
  inference and coefficient interpretation matter.

### scikit-learn

- Standard ML toolbox. Use `Pipeline` for all preprocessing — it is the
  simplest way to avoid fit-on-test leakage.
- `StratifiedKFold`, `GroupKFold`, and custom CV splitters for scaffold,
  temporal, or group splits.
- `cross_validate` for multiple metrics in one call.
- Prefer gradient boosting (XGBoost / LightGBM / HistGradientBoosting) as
  a strong baseline before complex neural models.

### RDKit

- `rdkit.Chem` for molecules, `rdkit.Chem.AllChem` for 3D and fingerprints,
  `rdkit.Chem.Descriptors` / `rdMolDescriptors` for physicochemical
  properties.
- Import patterns:
  ```python
  from rdkit import Chem
  from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
  from rdkit.Chem import Draw  # optional
  ```
- Pitfalls: `MolFromSmiles` returns `None` on failure — always check.
  Tautomer handling is not automatic — apply a standardizer explicitly.

### MDAnalysis

- Selection language (VMD-like) plus Python iteration over trajectories.
- Useful primitives: `Universe`, `AtomGroup`, `analysis.rms.RMSD`,
  `analysis.rms.RMSF`, `analysis.distances.distance_array`.
- Pitfall: selection strings silently match empty sets — verify
  non-empty before using.

### MDTraj

- Alternative MD analysis library; often faster for RMSD/contacts; slightly
  different API and selection DSL.

### Biopython

- `Bio.PDB.PDBParser`, `MMCIFParser` for structures.
- Iteration order: `structure → model → chain → residue → atom`.
- Pitfall: alternate locations and insertion codes need explicit handling.

### matplotlib

- Long the default plotting library. Keep plots simple, include units,
  include replicate indicators, and always label axes.

### networkx

- Useful for interaction networks, reaction networks, and residue contact
  graphs.

### xgboost / lightgbm

- Strong tabular baselines. Respect class imbalance (class weights /
  scale_pos_weight); log validation curves; use early stopping only on
  inner CV folds.

## R — scientific stack

### Bio3D

- Structure parsing, alignment, sequence conservation, PCA/NMA, MD
  trajectory analysis in R.

### tidyverse / data.table

- `tidyverse` for legible pipelines on moderate data; `data.table` for
  speed on large tables.

### caret / tidymodels

- ML workflows; `tidymodels` is the newer, more modular ecosystem with
  tighter separation of data → recipe → model → resamples.

### randomForest / e1071 / glmnet

- Baseline classifiers and regressors. `glmnet` for elastic-net regression
  with strong numerical behavior.

### pROC

- ROC analyses with confidence intervals and DeLong comparison.

### ggplot2

- Grammar of graphics plotting; preferred for publication figures.

### rcdk / ChemmineR

- R cheminformatics when staying inside R — fingerprints, descriptors,
  similarity. Less feature-rich than RDKit; interop with RDKit via
  reticulate is common.

## Common pitfalls (language-agnostic)

- **Silent type coercion** on chemical identifiers (e.g., Excel turning
  "1E6" SMILES fragments into numbers).
- **Fit-on-test leakage** via scalers or imputers.
- **Group-structure ignored** in CV (scaffolds, assays, labs).
- **Package updates breaking analyses**: pin versions in an environment
  file and record them in the report.
- **GPU nondeterminism** for neural models: set seeds, but understand that
  cuDNN may still be nondeterministic.

## When to check docs online

Check the web rather than relying on memory when:

- You need current function signatures or keyword arguments.
- You're checking whether a package supports a feature in its current
  version.
- You're looking for recommended parameters or benchmark settings.
- You're recommending a package that may have been deprecated or
  refactored.
- You need license/distribution details before recommending an install.

Cite sources when the user will act on the answer.
