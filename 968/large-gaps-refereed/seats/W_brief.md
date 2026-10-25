# Seat W — the world and the sources.
Read COMMON.md first. You may use the web (WebSearch / WebFetch / curl). Scope:
1. Novelty. Was Theorem 1.1 (positive proportion of gaps > C log p for EVERY C) or Corollary 1.2 (Erdős–Prachar) known before
   25 Sep 2026, unconditionally? Check Bazzanella–Languasco–Zaccagnini 2010 (Theorems 3 and 5 — confirm the 2/3.454 = 0.579038… number
   and whether it counts prime starts), Banks–Freiberg–Maynard 2016, Merikoski, Pintz, Goldston–Pintz–Yıldırım, Ford–Maynard–Tao,
   Tao's 2019 blog/paper "empty interval" argument the paper cites, Jha 2026, Gallagher 1976. Search arXiv (math.NT, 2025–Oct 2026)
   for any independent or competing proof, and for any public criticism of this OpenAI paper. Report dates and exact theorem numbers.
2. The problem as Erdős posed it: Erdős–Prachar, Abh. Math. Sem. Univ. Hamburg 25 (1961/62) 251–256, p. 256 — what exactly did they ask
   (density vs lower density)? Er65b. erdosproblems.com/968 (saved copy in /tmp/oaimath/026/live/, comments by Tao and others — read
   both comments in full and report what they claim), OEIS A387591.
3. Formal Conjectures: FormalConjectures/ErdosProblems/968.lean at google-deepmind/formal-conjectures@90d18f666eb98adec4eee4d12f1d37e30b4eb204
   marks erdos_968 'research solved' and links OpenAI's RatioCorollary.lean#L30 as formal_proof. Note that FC's statement uses a
   0-based u n = nth Prime n/(n+1) and FC's own Set.lowerDensity (liminf), not OpenAI's statement — confirm by reading both.
   When did FC add the 'solved' tag (commit/PR)? Any FC issue/PR about it?
4. Lean context: before this release, was there any public Lean 4 formalization of the Bombieri–Vinogradov theorem or of
   Siegel–Walfisz (e.g. in PrimeNumberTheoremAnd, Mathlib PRs, Arend Mellendijk's sieve work, other projects)? Report what exists
   with links and dates, or say you found none and how you searched.
5. Spot-check 3–4 of the paper's citations for accuracy (e.g. GY2005 "p. 6, equation (2.14)", BFI1986 "p. 206, equation (1.4)",
   Gallagher1976 "p. 5, equation (3)", Maynard2015 "Section 6, p. 404") — does the cited place say what the paper says it says?
Report as COMMON.md says (first line HOLDS AS READ / GAP / REFUTED applies to the paper's literature claims and novelty framing).
