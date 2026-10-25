# Erdős #432: exact two-row coprime-grid thresholds through 40 columns

Date: 2026-08-12 UTC

This is a finite exact extension of the two-row auxiliary problem introduced
in `runs/erdos432_wave9i.md`.  It does **not** improve the asymptotic bounds in
the original problem.

## Live collision gate

Bright Data captures made on 2026-08-12 showed:

- <https://www.erdosproblems.com/432>: `OPEN`, `0 claimed proofs for this
  problem`, `Currently working on this problem None`;
- <https://www.erdosproblems.com/forum/discuss/432>: one comment, Sungchul
  Lee's 2026-06-23 partial-results announcement.  It does not claim to settle
  the problem.

The collision gate therefore passed.  The raw captures are frozen as
`live_problem_20260812.txt` and `live_forum_20260812.txt`.

## Definition and reduction

Let `T2(x)` be the largest `n` for which two positive rows and `n` positive
columns have `2n` distinct sums, all at most `x`, that are pairwise coprime.
For arbitrary positive rows `{a,a+d}` and positive columns `B`, put
`V=a+B`. Then `V` lies in `[2,x-d]` and the sums are exactly

```text
{v,v+d : v in V}.
```

Conversely, such a set `V` gives rows `{1,1+d}` and columns `V-1`. Thus
`T2(x)>=n` if and only if some `d>0` admits `n` starts `v` for which all `2n`
integers `v,v+d` are distinct and pairwise coprime. Put

```text
L_n = min{x : T2(x) >= n}.
```

The coprime-grid terminology and CRT finite-grid extension framework already
appear in Sungchul Lee's public June 2026 manuscript. The earlier project
report independently checked that framework and established

```text
(L_2,...,L_10) = (11,17,23,31,41,47,67,79,83)
```

and only the weaker boundary `L_11>100`.

## New exact table

The two independent exhaustive audits prove the following new exact finite
table in this project; no absolute novelty claim is made:

| n | L_n | gap d | starts V |
|---:|---:|---:|:---|
| 11 | 101 | 12 | 11,13,17,31,37,41,47,61,67,71,89 |
| 12 | 107 | 6 | 11,23,31,41,43,53,61,65,73,83,97,101 |
| 13 | 127 | 6 | 13,23,25,37,41,53,61,73,83,101,103,113,121 |
| 14 | 131 | 18 | 5,13,19,29,41,43,49,53,79,83,89,103,109,113 |
| 15 | 149 | 10 | 13,17,19,31,37,43,49,61,73,79,97,103,121,127,139 |
| 16 | 167 | 10 | 13,19,31,37,43,49,61,73,79,97,103,121,127,139,153,157 |
| 17 | 173 | 10 | 13,17,19,31,37,43,49,61,73,79,97,103,121,127,139,157,163 |
| 18 | 191 | 10 | 17,19,31,37,43,61,73,79,97,103,121,127,139,151,157,163,169,181 |
| 19 | 197 | 18 | 5,19,29,41,43,53,79,83,89,103,109,113,119,139,149,151,163,173,179 |
| 20 | 211 | 18 | 5,19,29,41,43,53,79,83,89,103,109,113,119,139,149,151,173,179,181,193 |
| 21 | 241 | 12 | 17,25,31,41,47,61,67,71,97,101,127,137,151,157,161,179,181,197,211,227,229 |
| 22 | 251 | 18 | 19,29,41,43,49,53,79,83,89,103,109,113,137,139,149,173,179,181,211,221,223,233 |
| 23 | 257 | 18 | 5,19,29,41,43,53,79,83,89,103,109,113,119,139,149,151,173,179,181,211,223,233,239 |
| 24 | 271 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,173,181,193,199,227,233,239,241 |
| 25 | 281 | 30 | 17,23,31,41,59,67,73,83,101,107,109,121,127,149,167,173,181,193,199,227,233,239,241,247,251 |
| 26 | 307 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,203,227,239,241,251,263,277 |
| 27 | 313 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,203,227,239,241,263,277,281,283 |
| 28 | 347 | 30 | 17,23,31,41,59,67,73,83,101,107,109,121,127,149,167,181,193,199,227,239,241,247,263,281,283,301,307,317 |
| 29 | 361 | 30 | 7,17,23,31,41,59,67,73,79,83,101,107,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,319,331 |
| 30 | 367 | 30 | 7,17,23,31,41,59,67,73,79,83,101,107,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,319,331,337 |
| 31 | 379 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,331,337,343,349 |
| 32 | 383 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,331,337,343,349,353 |
| 33 | 389 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,331,337,343,349,353,359 |
| 34 | 431 | 30 | 17,23,31,41,59,67,73,79,83,101,107,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,319,331,343,353,367,379,389,401 |
| 35 | 439 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,367,389,401,409 |
| 36 | 449 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,359,367,401,409,419 |
| 37 | 463 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,359,367,409,419,431,433 |
| 38 | 487 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,367,389,409,431,433,449,457 |
| 39 | 491 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,367,389,401,409,433,449,457,461 |
| 40 | 509 | 30 | 17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,359,367,401,409,419,433,457,461,479 |

For each row, direct integer gcd checks prove the witness at `L_n`.  The two
audits independently prove that no `n`-column witness exists at `L_n-1`.
Monotonicity then makes `L_n` exact.

## Exhaustive engines

### A. From-scratch C++ gcd graph

For every `d=1,...,L_n-3`, the audit creates one vertex for every internally
coprime pair `(v,v+d)`.  It joins two vertices precisely when the four integers
are pairwise coprime.  A valid grid is exactly a clique.  The decision search
branches over every candidate vertex; a greedy proper coloring supplies only a
safe upper bound for pruning.  The full table passed in about 12 seconds at
`-O3`, with 4.1 MiB peak RSS.

### B. Independent prime-support CP-SAT

The Python audit factors all integers by trial division.  For fixed `d`, each
candidate pair is represented by the union of its two prime supports.  It then
creates one Boolean variable per pair and an at-most-one constraint for every
prime.  It asserts that at least `n` pairs are selected.  Every gap at every
lower boundary is independently reported `INFEASIBLE` by OR-Tools CP-SAT with
one worker and fixed seed.  This audit does not construct the gcd graph or call
the C++ search. It used OR-Tools 9.15.6755 and passed all 30 rows in about 24
seconds. CP-SAT does not provide proof certificates here. The transcript
digest was

```text
4b0ceb2770292580f2cebd639fb2dcdc98291e2e72105b7b2187eb21866ee5b4
```

As a memory-safety check, the hardest displayed C++ row (`n=40`) also passed
under AddressSanitizer and UndefinedBehaviorSanitizer.

## Scope

This is **computational-only exact finite progress**.  It concerns a stronger
injective two-row subclass of #432.  The elementary finite-to-infinite CRT
extension lemma from the earlier report embeds every displayed finite witness
in some infinite coprime grid, but says nothing useful about the growth scale.
The asymptotic problem therefore remains open.
