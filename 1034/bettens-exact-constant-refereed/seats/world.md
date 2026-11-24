# World seat (Claude instance, Opus 5.5), 2026-11-24 — the record as far as we could read it

erdosproblems.com was not read (its robots.txt excludes AI agents; our wall since 2026-11-19). Items the seat found
only in a third-party retelling of that site's forum are omitted from this copy and were not used on the page.

## Status of #1034 and of the exact-constant question

- **Community database** (github.com/teorth/erdosproblems, data/problems.yaml at cfd0fdb, 2026-11-23 21:07Z):
  status "disproved (Lean)", last_update 2025-12-04, formalized yes (2026-08-05), tags graph theory; no comments
  field. History: "open" from the 2025-09-13 sync; set to "disproved" on 2025-10-28 (commits ca6649f, c2a7dab);
  "disproved (Lean)" by the 2025-12-05 snapshot. No change since Bettens's deposit (expected: the status tracks the
  main yes/no question).
- **Formal Conjectures** (FormalConjectures/ErdosProblems/1034.lean, main 86a2f58, read 2026-11-24): four
  statements — `erdos_1034` (the negation of the (1/2 − ε)n statement, research solved, with a formal_proof link
  to plby/lean-proofs), `variants.lower_bound` ((1/6 − ε)n), `variants.upper_bound` ((2 − √(5/2) + ε)n),
  `variants.k4_free`. The exact constant is not posed as a variant; no answer is recorded. Added 2026-08-05 by
  PR #4551 (closing issue #1085). Issue/PR searches for 1034, Ma Tang, Faudree etc. found nothing on an exact
  constant.
- **Ma–Tang note** (J. Ma and Q. Tang, http://staff.ustc.edu.cn/~jiema/Erdos-1034.pdf, PDF created 2025-10-21,
  unchanged since at least the 2025-11-06 Wayback capture): Theorem 2.1 gives graphs with more than n²/4 edges in
  which every triangle has at most (2 − √(5/2) + ε)n vertices adjacent to two of its vertices. Section 3 quotes
  Erdős [Quaestiones Math. 16 (1993), p. 344] asking to determine the largest h(n), states
  (1/6 − o(1))n ≤ h(n) ≤ (2 − √(5/2) + o(1))n (the lower bound from the classical book theorem), and ends:
  "Determining the exact asymptotic constant c∗ := lim h(n)/n remains open." No value proposed; no arXiv version.
- **Later work:** nothing found improving 0.418861 or the n/6 lower bound (arXiv title/abstract searches;
  related 2026 papers 2605.02652, 2607.16746, 2607.15071, 2611.13608, 2610.37739, 2607.09474 grepped; OpenAlex).
  facebookresearch/atlas-lean (2026-11-23) has an elementary Lean refutation with the weaker constant 1/2 − 1/46.

## Prior and parallel claims

No other claim of an exact value, or of (36 − 5√3)/66 ≈ 0.41424, anywhere searched: Zenodo API, DataCite,
OpenAlex, GitHub code search (numeric forms of the constant; Erdos1034/erdos_1034 across ~15 repos), the OpenAI
catalogue (github.com/openai/math CONTENTS.md, no 1034 entry), MathOverflow (StackExchange API, with a positive
control), Tao's blog (WordPress API, posts and comments) and his Mathstodon posts. The submitter's "as Tao noted"
was not found in any source we may read.

The deposit: Zenodo 23223509 (DOI 10.5281/zenodo.23223509), created 2026-10-07, preprint, CC-BY-4.0, the only
version (concept 23223508 resolves to it). MD5s of all five files match our local copy.

## What is new, as far as the record shows

1. The upper bound is a parameter choice inside Ma and Tang's family (six equal cliques, α₆ = (6 + √3)/11, no
   leftover block). A numerical optimisation of their full family (q equal blocks plus one leftover, all α) lands
   at q = 6 with the leftover going to zero, within grid resolution of c₆. Other values: c₅ = (25 − 2√10)/45 =
   0.41501, 2 − √(5/2) = 0.418861.
2. The lower bound is the substantive new claim: from n/6 to 0.4142n. If the certificate verifies, the bounds
   meet, the limit exists, and the question Ma and Tang left open is answered.
3. Formal Conjectures has no exact-constant variant; one would be a natural follow-up.
4. Our site had no July working report on #1034; /problem/1034 showed only the database status.
5. Bodnár's toolbox paper (arXiv:2601.06590) does not mention this problem.

Not searched: MathSciNet, zbMATH, Google Scholar, Semantic Scholar, X/Twitter. arXiv searched in title/abstract/
comment fields only (full text for the papers named above).
