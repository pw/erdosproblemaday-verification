# Erdos Problem 174: pyramid closure, source and proof audit

Audit date: 2026-08-11 UTC

Status: **PARTIAL, independently audited**.

## 1. Narrow result

The live problem asks for a characterization of the finite Euclidean Ramsey
sets. Kenneth Moore's preprint, posted on 2026-08-10, proves the following
closure theorem (Theorem 1.2 of arXiv:2608.09649v1):

> Let `B` be a finite Ramsey set in a Euclidean space. If `z` is outside the
> affine hull of `B`, then `B union {z}` is Ramsey.

This is exactly Conjecture 8 of Ivan--Leader--Walters,
arXiv:2606.13472v1. Their Corollary 4 already proves the conclusion for a
subsoluble base; Moore removes that structural assumption and handles every
finite Ramsey base. It is a genuine partial result toward Problem 174, not a
characterization. The source is arXiv v1, and no peer-reviewed version or
journal reference was located. For site purposes it is treated as an
unrefereed preprint. The audited conclusion is therefore: **the preprint claim
is correct modulo three named classical theorems, and an independent
reconstruction found no gap**.

An immediate iterated corollary is useful for stating the scope precisely. If
`B` is Ramsey and points `z_1,...,z_t` can be ordered so that

```
z_i not in aff(B union {z_1,...,z_(i-1)})
```

for every `i`, then `B union {z_1,...,z_t}` is Ramsey. This follows by `t`
applications of Moore's theorem; no extra geometric assumption is hidden.

This bundle does **not** claim that every spherical or every subtransitive set
is Ramsey, does not handle an added point inside the affine hull, and gives no
effective dimension bound.

## 2. Strict gate

The rendered live page and discussion thread were opened through Bright Data
on 2026-08-11. `LIVE_GATE.txt` preserves the relevant transcription. They
showed:

- status `OPEN`;
- `0 claimed proofs for this problem`;
- `Currently working on this problem: None`;
- `I am working on formalising the results on this problem: None`;
- four comments, the newest dated 2026-02-15;
- page last edited 2025-10-16.

The newest comment mentions Behague's 2025 subsolubility paper. None of the
four comments mentions Moore or arXiv:2608.09649. `LIVE_GATE.txt` preserves a
plain-text transcription of the relevant rendered markers and comments.

Problem number 174 is absent as a target from both current site data files.
The defining phrases `euclidean ramsey`, `ramsey set`, `subtransitive`,
`subsoluble`, `spherical set`, and `rotations act transitively` have no
case-insensitive hit in either file. At the gate time the files had hashes:

```
08e988d080d5317adf768ba827b4f21397699b30d28cc749807616b6753a3b76  src/index.js
9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052  src/ledger_data.js
```

The live page lists no related OEIS sequence, and the upstream metadata has
`oeis: [N/A]`. Current OEIS searches for the exact Euclidean-Ramsey phrases
returned unrelated Euclidean-geometry and graph-Ramsey sequences. This
qualitative closure theorem has no integer sequence to update.

## 3. Primary-source chronology

1. Erdos--Graham--Montgomery--Rothschild--Spencer--Straus (EGMRSS),
   *Euclidean Ramsey Theorems I*, JCTA 14 (1973), 341--363,
   DOI 10.1016/0097-3165(73)90011-3. Proposition 4 is the finite compactness
   witness; Theorem 20 says the Cartesian product of two Ramsey
   configurations is Ramsey.
2. Frankl--Rodl, *A partition property of simplices in Euclidean space*,
   JAMS 3 (1990), 1--7, DOI 10.1090/S0894-0347-1990-1020148-2. Its main result
   says every finite nondegenerate simplex, equivalently every finite
   affinely independent Euclidean set, is Ramsey.
3. Behague, *Nearly all known Euclidean Ramsey sets are subsoluble*,
   arXiv:2510.15677v3 (2025). This is already mentioned in the live thread and
   is background only.
4. Ivan--Leader--Walters, *Generalised Prisms and Euclidean Ramsey Theory*,
   arXiv:2606.13472v1 (2026-06-11). Its Conjecture 8 asks exactly whether a
   Ramsey base stays Ramsey after one out-of-affine-hull point is added.
5. Moore, *A pyramid with a Ramsey base is Ramsey*, arXiv:2608.09649v1,
   posted 2026-08-10 14:26:02 UTC. Theorem 1.2 proves Conjecture 8.

No third-party PDF is distributed in this public package. `SOURCES.md`
preserves the official URLs, theorem locations, observed SHA-256 identities,
and license notes from the private source-custody audit.

## 4. Independent proof reconstruction

Write `R^n ->_r T` when every `r`-colouring of `R^n` contains a
monochromatic congruent copy of `T`. Let `X = B union {z}`. Induct on the
number `r >= 1` of colours.

The standard convention takes a finite configuration to be nonempty. If the
empty set is admitted, the exceptional base `B = empty` is immediate because
`B union {z}` is a singleton and hence Ramsey. Assume below that `B` is
nonempty.

The case `r=1` is immediate. For `r>=2`, the induction hypothesis gives some
`d_2` with `R^(d_2) ->_(r-1) X`. EGMRSS Proposition 4 gives a finite
configuration

```
C = {c_1,...,c_m} subset R^(d_2),   C ->_(r-1) X.
```

After restricting to `aff(B union {z})` and applying an isometry, write
`B subset R^(d_1)` and `z=(u,h)` with `u in R^(d_1)` and `h>0`. Let
`e_1,...,e_m` be the standard orthonormal basis of `R^m`, and put

```
s_i = (c_i, h e_i),        S = {s_1,...,s_m},
P   = B x S,
a_i = (u, c_i, 0),         A = {a_1,...,a_m},
P_i = B x {s_i}.
```

The `h e_i` block proves `S` is affinely independent: if
`sum lambda_i s_i=0` and `sum lambda_i=0`, its last block is
`h sum lambda_i e_i=0`, hence every `lambda_i=0`. Frankl--Rodl therefore
makes `S` Ramsey. Since `B` is Ramsey, EGMRSS Theorem 20 makes `P=B x S`
Ramsey.

The set `A` is congruent to `C`, and every fibre `P_i` is congruent to `B`.
For every `b in B`,

```
||(b,c_i,h e_i) - (u,c_i,0)||^2 = ||b-u||^2 + h^2
                                      = ||(b,0)-(u,h)||^2.
```

Thus `P_i union {a_i}` is congruent to `X` for every `i`.

Choose a dimension large enough both to contain `P union A` and to force a
monochromatic copy `P'` of `P` in every `r`-colouring. (Dimension
monotonicity follows by restricting a colouring to a lower-dimensional
affine subspace.) Call the colour of `P'` red. A congruence `P -> P'` extends
to an ambient Euclidean isometry, so it also transports all the `a_i`.

- If some transported `a_i` is red, its red fibre produces a red `X`.
- Otherwise the transported copy of `A congruent C` uses at most the other
  `r-1` colours, and `C ->_(r-1) X` produces a monochromatic `X`.

This closes the induction with all colour and dimension quantifiers in the
required order.

For completeness, the isometry-extension step does not assume that `P`
affinely spans the ambient space. Translate one chosen point to the origin.
Equality of pairwise distances gives equality of the two Gram matrices, so
the congruence extends linearly to an isometry between the two affine-direction
subspaces. Extend orthonormal bases of those subspaces to orthonormal bases of
the common ambient `R^N`; mapping the completed bases gives the required
global orthogonal map, followed by the translation.

## 5. Audit of imported quantifiers

- EGMRSS Proposition 4 applies because every target copy is finite. It gives
  a finite set of points, not merely finitely many transformations.
- EGMRSS Theorem 20 quantifies over every finite number of colours and loses
  only dimension, exactly matching the definition used here.
- Frankl--Rodl proves more than needed: for each nondegenerate simplex it
  permits exponentially many colours as the ambient dimension grows. A fixed
  finite `r` is therefore covered.
- Moore needs no transitivity, subtransitivity, solubility, measurability, or
  regularity assumption on the colouring.
- `z outside aff(B)` is essential to get `h>0`; the proof does not establish
  same-affine-span closure.

The independent reconstruction found no circular use of the desired theorem.
The only non-elementary inputs are the three named results above.

## 6. Reproduction

Run from the bundle directory:

```bash
./reproduce.sh
```

The checker uses only the Python standard library. It checks manifest closure,
source-custody metadata, publication wording, and exact rational fixtures for
the affine-independence, Cartesian-product, apex-distance, and colour-dichotomy
parts of the construction. The reproducer runs it under normal Python,
`python3 -O`, and `python3 -OO`, then corrupts a tracked narrative, source
metadata file, and geometric fixture and requires every mode to reject each
mutation. It also requires every mode to reject untracked files, a nested
manifest, duplicate entries, a PDF extension, and PDF magic hidden under a
different extension. These finite checks audit the algebraic gadget; they do
not replace the general proof or the three classical theorems.

## 7. Publication-safe conclusion

**PARTIAL (rigorous modulo named primary theorems; arXiv v1):** Moore's
arXiv:2608.09649v1, posted 2026-08-10, proves that the class sought in Erdos
Problem 174 is closed under adjoining a point outside the current affine hull,
resolving Conjecture 8 of Ivan--Leader--Walters. The proof has been
independently reconstructed and its geometric gadget exactly checked. The
general characterization remains open. No peer-reviewed version or journal
reference was located as of the audit date.
