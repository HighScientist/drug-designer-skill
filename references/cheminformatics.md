# Cheminformatics — structures in, structures out, no surprises

Treat cheminformatics as data engineering. Most QSAR and docking disasters
start with sloppy molecule handling: unresolved tautomers, stealth
duplicates, mixed stereo definitions, salts confused for parents. This file
is the hygiene checklist.

## File formats

- **SMILES**: compact, line-based; canonicalization is toolkit-specific —
  canonicalize with *one* toolkit across the whole pipeline.
- **SDF / MOL**: 2D or 3D, explicit atom and bond blocks, supports
  properties per record; good for libraries.
- **MOL2**: carries atom types and partial charges; common in docking
  pipelines.
- **PDB** for ligands: lossy for bond orders; avoid as a ligand transit
  format.
- **InChI / InChIKey**: normalization and duplicate detection; InChIKey is
  strong for exact-structure identity.

## Standardization and curation

- Strip salts and solvents; keep the largest organic fragment when that is
  the intended molecule. Record removals.
- Normalize charges; pick a consistent tautomer policy (e.g., an explicit
  canonical-tautomer tool) and apply it uniformly.
- Set stereochemistry policy: preserve, enumerate, or drop — but never mix
  within a dataset.
- Kekulize or aromatize consistently.
- Canonicalize SMILES with the same toolkit and settings across the
  dataset.
- Run a duplicate pass on canonical SMILES *and* on InChIKeys. Resolve
  disagreements explicitly.

## Salts and mixtures

- Mixtures need a policy. Typical choices:
  - Keep the largest organic component.
  - Drop records with multiple drug-like components.
  - Preserve the entire record when the mixture is meaningful (co-crystals,
    cocrystal formers).
- Document and apply one policy consistently.

## Tautomer and stereochemistry caveats

- Tautomeric forms can differ in logP, pKa, H-bond donors, and predicted
  activity. The "right" tautomer depends on pH, binding-site environment,
  and experimental context.
- Stereochemistry flips can reverse activity. Ambiguous stereo should be
  *explicitly* flagged, not silently assigned.
- When enumerating, cap the enumeration count and record which parent each
  child came from.

## Similarity and substructure

- **Tanimoto on Morgan/ECFP fingerprints** is the de facto baseline
  similarity metric. Report radius and bit size.
- **MACCS-based Tanimoto** is more interpretable but weaker for
  structure-activity.
- **Substructure search (SMARTS)** for hard filters — PAINS, Brenk,
  reactive groups, inorganic atoms, undesired ring systems.
- **Scaffold analysis (Bemis–Murcko)** for dataset structure, split design,
  and scaffold-hopping analysis.

## Descriptors

- Physicochemical: MW, logP (method-specific; Crippen/clogP/XLogP differ),
  TPSA, HBD/HBA, rotatable bonds, ring counts, fraction sp3, formal charges.
- Topological, constitutional, electronic, and 3D descriptors are available
  in RDKit, Mordred, and others; document exactly which set you use.
- Beware descriptor redundancy — many descriptors are near-linear
  combinations of others.

## Library QC

Before running a virtual screen or training a model:

1. Parse all structures; record parse failures.
2. Standardize (salt strip, charge normalization, tautomer policy,
   canonicalization).
3. Deduplicate on canonical SMILES and InChIKey.
4. Flag PAINS / Brenk / reactive patterns as *alerts*, not truth. Many
   known drugs contain PAINS-like substructures.
5. Property-filter per the intended use (e.g., Lipinski, lead-likeness,
   fragment rules) — and document the chosen filter.
6. Inspect descriptor distributions for outliers, bimodality, or sudden
   cliffs suggesting mixed sources.
7. Report pass/fail counts at each stage.

## PAINS / Brenk / REOS etc.

- Treat alerts as hypotheses: "this substructure has historically been
  associated with assay interference". They are not proofs of activity or
  interference in a given assay.
- Do not auto-reject a compound solely on a PAINS hit; triage with context.

## Tools

- **RDKit** (Python, C++): the workhorse — standardization, fingerprints,
  descriptors, similarity, substructure, simple 3D, reaction handling.
- **Open Babel**: broad format coverage, 3D generation, protonation,
  conversion utilities.
- **ChemAxon, OEChem, Schrödinger**: commercial, capable, check licensing
  and version-specific behavior.
- **Mordred** (Python): extensive descriptor set built on RDKit.
- **rcdk / ChemmineR** (R): cheminformatics in R pipelines.

Check current docs and version behavior before relying on any specific API.

## Minimal RDKit hygiene snippet (conceptual)

```python
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors

smi = "CC(=O)Oc1ccccc1C(=O)O"  # aspirin
mol = Chem.MolFromSmiles(smi)
if mol is None:
    raise ValueError("parse failed")

mol = Chem.RemoveHs(mol)
canon_smi = Chem.MolToSmiles(mol)
fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
mw = Descriptors.MolWt(mol)
logp = Descriptors.MolLogP(mol)
tpsa = rdMolDescriptors.CalcTPSA(mol)
```

Use this pattern inside a pipeline that also handles: parse failures, salt
stripping, tautomer standardization, stereochemistry policy, and duplicate
detection. The bundled `scripts/compound_qc.py` covers the common cases.
