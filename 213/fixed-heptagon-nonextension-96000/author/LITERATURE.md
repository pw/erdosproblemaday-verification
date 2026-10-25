# Literature and public-frontier audit

Access/search date: 2026-08-11 UTC.

## Current scope

- The live page for [Erdos problem 213](https://www.erdosproblems.com/213)
  says the best construction has seven points.
- Avdeev, Zvolinskiy, and Momot,
  [Particular Examples of Planar Integral Point Sets and Their
  Classification](https://doi.org/10.46698/q7071-3025-8385-h), Vladikavkaz
  Mathematical Journal 28(1) (2026), 28-36, says in its abstract that the
  largest known general-position set has seven points and no eight-point
  example is known. Its 2021 arXiv precursor is archived in
  `sources/avdeev_momot_zvolinskiy_2021_arxiv.pdf`.
- OEIS [A096873](https://oeis.org/A096873), checked on 2026-08-11, lists the
  minimum general-position diameters only through seven points:
  `1,1,1,8,73,174,22270`. It does not list an eighth term.
- Searches also checked 2024-2026 work on characteristic and diameter,
  including Avdeev-Lushina (arXiv:2407.08121) and Solymosi
  (arXiv:2606.26311). Those papers concern diameter bounds or short distances
  in semi-general/arbitrary planar integral point sets and do not supply an
  eight-point general-position example or this bounded extension result.

This negative search is not a theorem of absence. It supports the deliberately
narrow novelty comparison below.

## Primary metric and public cutoff

Kreisel and Kurz,
[There are integral heptagons, no three points on a line, no four on a
circle](https://d-nb.info/994732597/34), give the exact 7-by-7 distance matrix
archived in `heptagon_matrix.json`. Their exhaustive search proves
`d_dot(2,7) = 22270`, and they state that this heptagon has characteristic
`2002 = 2*7*11*13`.

The same paper states that they then exhaustively constructed all
general-position planar integral point sets of diameter at most `70000` whose
characteristic divides

`6469693230 = 2*3*5*7*11*13*17*19*23*29`.

Thus characteristic 2002 is inside their documented search class. They report
a second heptagon of diameter 66810. The primary PDF is frozen at
`sources/kreisel_kurz_2008_heptagons.pdf`.

## Exact comparison and its boundary

This bundle directly certifies that the published diameter-22270 heptagon has
no eighth point at positive integral distance at most `96000` from every one
of its seven vertices. Numerically, `96000 > 70000`, so it advances the
explicit cutoff for this fixed-heptagon, characteristic-2002 extension slice
by 26000.

This is not an extension of the paper's entire restricted-characteristic
catalogue from 70000 to 96000. It is a stronger point-extension test for one
fixed heptagon and a narrower configuration class. In particular, it proves
none of the following:

- that an arbitrary eight-point set has diameter greater than 96000;
- that no eight-point general-position integral set exists;
- that either known heptagon is globally inclusion-maximal;
- that the second diameter-66810 heptagon has the same extension bound;
- that problem 213 is solved for `n = 8`, let alone for every `n`.
