# Erdős #757: reader submission 7bkzb8 — c* ≤ 5/9 (VERIFIED)

Reviewed 2026-10-19. The submission (anonymous, consent to publish given; verbatim in `SUBMISSION.md`)
claims c* ≤ 5/9 for the Sidon constant of (4,5)-sets, below Ma–Tang's 4/7 (arXiv:2602.23282 v2, the best
published upper bound; also Tao's optimization-constants entry 5b). We verified it, for every K, with a
complete proof (`PROOF.md`) that reduces it to finite exact computations, two independent solvers, and a
hostile referee seat (`referee/REPORT.md`: HOLDS WITH GAPS, four gaps, all fixed here).

## The statement verified

O = {0,49,75,83,98,101,117,119,121,159,269}, φ(x) = 101 + 18x/269, S_K = O ∪ φ(O) ∪ … ∪ φ^K(O).
For every K ≥ 0: |S_K| = 11 + 9K, S_K is a (4,5)-set, and its largest Sidon subset has exactly 7 + 5K
points. Hence c* ≤ (7+5K)/(11+9K) for every K, so **c* ≤ 5/9 ≈ 0.5556** (published: 9/17 ≤ c* ≤ 4/7).
Already K = 6 — 65 points, largest Sidon subset 37 — gives 37/65 ≈ 0.5692 < 4/7 ≈ 0.5714 by a single
finite set. Integer form: multiply S_K by 269^K.

Why it works: O's only additive structure is nine 3-term progressions (9 = |O| − 2, the most Ma–Tang's
Lemma 2.4 allows), and the copies φ^j(O) form a chain, consecutive copies sharing exactly two points, with
no additive relation crossing copies at any depth. A Sidon set is then exactly a chain of per-copy choices,
and a 4-state max-plus transfer matrix gives 7 + 5K exactly.

## Files

| file | what | instrument |
| --- | --- | --- |
| `build.py` | S_K with exact rationals, scaled to integers | — |
| `check45.py` | literal \|B−B\| ≥ 11 on every 4-subset, K ≤ 12 (119 points); controls | exhaustive |
| `relations.py` | every a+b=c+d (a=b allowed) in S_K; tests each lies inside one copy; copy overlaps; injected-point control | exhaustive, K = 0,1,3,6,10,12 |
| `transfer.py` | max-plus chain DP; v_K = [6+5K, 7+5K, 7+5K, 7+5K] for all K | exact |
| `sidon_cpsat.py` | max Sidon subset, OR-tools CP-SAT, K ≤ 8 | solver 1 |
| `indep/indep_check.py` | separately written integer construction, distance-collision encoding, CaDiCaL 1.5.3 + cardinality: ≥ 7+5K SAT, ≥ 8+5K UNSAT, K ≤ 8 | solver 2 |
| `PROOF.md` | the all-K proof: canonical levels, a 269-adic/size span lemma (any relation spans ≤ 10 levels), shift argument, (4,5) and h for all K | proof |
| `referee/` | hostile seat's report and its own scripts (independent brute force to K = 150) | referee |
| `out_*.txt` | frozen outputs of the runs above | — |

## Reproduce

```
python3 check45.py 12
for K in 0 1 3 6 10 12; do python3 relations.py $K; done
python3 transfer.py
python3 sidon_cpsat.py 0 8          # needs ortools
cd indep && python3 -I indep_check.py 8   # needs python-sat
sha256sum -c SHA256SUMS              # from this directory
```

## Labels

(a) elementary: P2–P3, P5 and the DP once the finite facts are in. (d) computer-assisted: O's relation list
and (4,5)-property, the S_12 relation census (which the span lemma turns into an all-K statement), and the
transfer matrix entries. Nothing rests on (c).

## Credit

The construction, the claim and the +5-per-level sketch are the submitter's. Ours: the all-K proof write-up
(the span lemma that makes the finite check cover every K), the checks, and the referee pass.
