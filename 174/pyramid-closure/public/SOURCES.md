# Source custody for Problem 174

Audit date: 2026-08-11 UTC.

This public package intentionally contains no third-party PDF. The private
source-custody bundle was checked against the official locations below. The
hashes identify the exact bytes used for the proof audit; they are not a grant
of redistribution rights.

## Moore

- Kenneth Moore, *A pyramid with a Ramsey base is Ramsey*.
- Official record: https://arxiv.org/abs/2608.09649
- Audited version: arXiv:2608.09649v1, submitted 2026-08-10 14:26:02 UTC.
- Locations: Theorem 1.2 on p. 2; supporting Theorems 2.1 and 2.2 and
  Lemma 2.3 on p. 2; proof on pp. 3--5.
- Observed PDF SHA-256:
  `2a1f866a06e5a8452f8b8425e6e244706a23eb039bb427eac5a51ade028fd45e`.
- License: CC BY 4.0,
  https://creativecommons.org/licenses/by/4.0/.
- No peer-reviewed version or journal reference was located at audit time.

## Ivan--Leader--Walters

- Maria-Romina Ivan, Imre Leader, and Mark Walters, *Generalised Prisms and
  Euclidean Ramsey Theory*.
- Official record: https://arxiv.org/abs/2606.13472
- Audited version: arXiv:2606.13472v1, submitted 2026-06-11 15:25:49 UTC.
- Locations used for context: Corollary 4 on p. 6 and Conjecture 8 on p. 9.
- Observed PDF SHA-256:
  `9e7a0da78ec6094bde530cf789c9ef58a680810ef2ac52feac49114c4c884f0e`.
- License: arXiv nonexclusive-distribution license; PDF omitted because no
  general downstream redistribution license was identified. License record:
  https://arxiv.org/licenses/nonexclusive-distrib/1.0/.

## Behague

- Natalie Behague, *Nearly all known Euclidean Ramsey sets are subsoluble*.
- Official record: https://arxiv.org/abs/2510.15677
- Audited version: arXiv:2510.15677v3, posted 2025-12-04 15:00:59 UTC.
- Location: Theorem 1.5 on p. 2. Background only; not a proof input.
- Observed PDF SHA-256:
  `f0ee8b166026281c106562102657a71a7be8a85db964e0b370244ddc4764fbfd`.
- License: CC BY-SA 4.0,
  https://creativecommons.org/licenses/by-sa/4.0/. PDF omitted by the
  package-wide policy.

## Classical inputs

- Erdos, Graham, Montgomery, Rothschild, Spencer, and Straus, *Euclidean
  Ramsey Theorems I*, Journal of Combinatorial Theory A 14 (1973), 341--363,
  DOI https://doi.org/10.1016/0097-3165(73)90011-3.
  Proposition 4 on journal p. 343 supplies finite compactness and Theorem 20
  on journal p. 357 supplies product closure. Observed PDF SHA-256:
  `ac59b75ae71753073a99d689e60a8d52caa7a47216dd21d7d57026b8d281682a`.
  The inspected copy reserved reproduction rights, so it is omitted.

- Peter Frankl and Vojtech Rodl, *A partition property of simplices in
  Euclidean space*, Journal of the AMS 3 (1990), 1--7,
  DOI https://doi.org/10.1090/S0894-0347-1990-1020148-2.
  Theorem 5.1 on journal p. 5 is the simplex theorem and the third imported
  proof input. Observed PDF SHA-256:
  `e82f0e24babe4751e695fd90da2f46363e127544f53598ea9a2ae805a6eaba72`.
  The inspected copy did not establish downstream redistribution permission,
  so it is omitted.

The independent hostile audit is preserved as `HOSTILE_AUDIT.md`. It records
the theorem-marker, quantifier, live-status, and source-identity checks made
against the private custody copies.
