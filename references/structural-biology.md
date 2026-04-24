# Structural biology — reading protein structures correctly

You cannot do SBDD faster than you can read structures carefully. This file
is the checklist for opening a PDB/mmCIF, a predicted model, or an
experimental ensemble and not tripping over its silent details.

## File formats

- **PDB**: legacy fixed-column ASCII format; de facto standard for small
  proteins; has limits (chain IDs, serial numbers, very large assemblies).
- **mmCIF / PDBx**: preferred modern format; handles large assemblies,
  richer metadata.
- **PDB IDs** correspond to deposited entries; check the header for
  resolution, method (X-ray, cryo-EM, NMR), R-factors, ligand validation
  flags, and known errata.

## Structural elements to inventory

Before analyzing anything, enumerate:

- **Chains**: A, B, C ...; annotate by sequence identity and biological
  assembly definition.
- **Residues**: by chain; flag nonstandard residues, modifications, gaps.
- **Hetero atoms (HETATM)**: ligands, cofactors, metals, buffers, cryo
  additives — many HETATMs are crystallographic crud, some are essential.
- **Waters**: volume vs. site; conserved waters near the binding pocket
  matter.
- **Alternate locations (altlocs)**: keep track; one residue may have
  multiple conformers with occupancies adding to 1.0.
- **Insertion codes**: numbering can have insertion letters; don't assume
  sequential integers.

Use `scripts/inspect_structure.py` as a first pass.

## Chains, assemblies, and symmetry

- The asymmetric unit in a PDB entry may not match the biological
  assembly. Generate the biological assembly (BIOMT / assembly records)
  when relevant.
- Interface analyses must use the biological assembly, not only the
  asymmetric unit.

## Missing loops and residues

- Short gaps (a few residues) can often be modeled with loop modelers; long
  gaps (tens of residues) usually cannot and should be flagged.
- Loops near the binding site are especially consequential — state the gap
  explicitly in the methods.

## Cofactors and metals

- Metals (Zn, Mg, Ca, Fe, Mn, Ni...) have specific geometric and charge
  requirements. Do not treat metal coordination with a generic force field
  without checking.
- Essential cofactors (NAD(P)H, FAD, heme, ATP/ADP, GTP/GDP analogs) shape
  the pocket — keeping them is often mandatory for docking.
- Lipids in membrane-protein structures: keep or remove deliberately per
  the biological question.

## Waters

- Crystallographic waters are context-dependent. In many kinase and
  nuclear-receptor pockets, specific waters mediate key H-bonds — keep
  them.
- Without evidence for a bridging role, remove pocket waters to avoid
  artificial templating of docking poses.

## Sequence ↔ structure ↔ UniProt mapping

- Match PDB residue numbering to UniProt numbering; they often differ (tag
  cleavage, construct truncations, engineered mutations).
- Use SIFTS-style mapping resources when precision matters.
- Record the construct's mutations explicitly.

## Predicted models (AlphaFold / ESMFold / RoseTTAFold / colabfold)

Predicted structures are hypotheses. Read them with their confidence
metrics.

- **pLDDT** (per-residue): AlphaFold2/3 confidence. Roughly: >90 very
  high; 70–90 confident; 50–70 low; <50 disordered/unreliable.
- **PAE** (pairwise aligned error): the relative positioning of two
  residues is only trustworthy where PAE is low between them. Use for
  inter-domain orientations.
- Loops, termini, and disordered regions are often low-confidence. Binding
  pockets built from low-confidence regions are unreliable.
- Predicted models may lack cofactors, metals, and waters — add them
  explicitly if you need them for docking.
- For ligand-binding predictions specifically, consult current
  literature/benchmarks for which tools and versions handle holo prediction
  acceptably.

## Binding site interpretation

- Define the binding site: residues within a cutoff of a reference ligand,
  or via pocket-detection (e.g., fpocket-style tools), or via
  sequence/structure conservation.
- Inventory key interactions: H-bonds, salt bridges, hydrophobic contacts,
  pi-stacking, halogen bonds, metal coordination, water bridges.
- Map hotspots: residues with highest contact frequency across known
  ligands, or with conservation among orthologs.

## Tools

- **Biopython** (Python): parse PDB/mmCIF, iterate residues/atoms, handle
  SeqRecord alignment, simple structure manipulation.
- **Bio3D** (R): sequence-structure analysis, ensemble analysis, PCA/NMA,
  trajectory analysis.
- **PyMOL / ChimeraX / VMD**: visualization, preparation, image generation
  for reports.
- **OpenMM**, **Rosetta**, **Modeller**: preparation, loop modeling,
  relaxation.

Refer to current docs for exact APIs; they change across versions.

## Reporting structural inputs — checklist

- PDB ID, chain(s), biological assembly.
- Resolution, method, R/Rfree for X-ray; EMDB ID and resolution for cryo-EM;
  ensemble choice for NMR.
- Residue range used, mutations, truncations.
- Ligand/cofactor/metal decisions.
- Water decisions.
- Protonation and altloc decisions.
- Source of any predicted model, version, confidence summary (mean pLDDT,
  PAE comments), and reason for choosing it.
