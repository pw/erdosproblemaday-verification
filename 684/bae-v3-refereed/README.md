# Erdős #684 — Ji Ho Bae, arXiv:2604.23784v3, refereed and Lean-replayed (2026-10-31)

Page: https://erdosproblemaday.com/day/684-bae-unbounded-log-limsup-refereed

## The claim
f(n) = min{1 ≤ k ≤ n : u(n,k) > n²}, u(n,k) = ∏_{p≤k} p^{ν_p C(n,k)}. Bae v3 (3 Sep 2026), Theorem 1.2:
limsup f(n)/log n · (log log log n)/(log log n) ≥ 1/2; hence f(n)/log n is unbounded.
Source: arXiv e-print v3 sha256 8ce5187566651fdbadb2f4143e9026baac6442dd17feaadd5bf7bb34ba3d9abe
(tex ERDOS684_FINAL_PAPER_formal.tex 0edd5c72…be0; PDF a83b9254f2d7…b85f). Not copied here (CC BY 4.0 on arXiv).

## Chain
1. **Replay (`replay/`).** github.com/jidodat/erdos684-lean, tag `v3-arxiv` = 49ee38cdb954634477d175f0b91fd9f56a1aec16,
   Lean v4.32.2, Mathlib 905b958 (from the Mathlib cache), PrimeNumberTheoremAnd a5154676 (built from source).
   `run.sh`: scrubbed env, scratch HOME, nice 19, LEAN_NUM_THREADS=4, each step gated on the previous rc.
   `steps.tsv`: cache_get rc 0 (116 s) · build rc 0 (391 s, 8,696 jobs) · audit rc 0 · eval rc 0.
   `logs/audit.log`: `#print axioms` = [propext, Classical.choice, Quot.sound] for main_theorem_unconditional,
   unbounded_unconditional, main_theorem_limsup, main_theorem, pntHyp; statements and definitions printed;
   **negative control** `audit_ctl_sorry` prints [sorryAx].
   `fresh.sh`: `leanchecker --fresh Erdos684Lean` over the whole import closure (re-checks the cached Mathlib oleans);
   its negative control (non-existent module) exits 1 (`fresh_negctl` row). **The pass exited 0** (`fresh` row,
   2026-10-31T10:17:43Z, 3,706 s wall, peak RSS 8.2 GB, `logs/fresh.log`): the kernel re-checked the whole import
   closure, cached Mathlib oleans included.
2. **Literal values (`replay/Eval2.lean`, `numerics/`).** The formal f(n) (Lean's `uPart`, evaluated) for n ≤ 73 equals
   all 73 terms of OEIS A392019 (`b392019.txt`) and our trial-division table from the integer C(n,k) (`ftable.py`, n ≤ 60).
   Control: a mutant with primes < k (`mutation.py`) disagrees with OEIS at n = 28, 50, 51, 54.
3. **Bridge (ours, `bridge/Bridge684.lean`).** FC's `smallPrimePart` and `erdos_684.upper_bound` statement copied verbatim
   from FormalConjectures/ErdosProblems/684.lean @ d9f6ffa8dd7fc2b8b597dd1f7a824d27b12b88af (`check_verbatim.py`, log `check_verbatim.log`; a mutated copy
   fails). Proves: `smallPrimePart_eq_uPart` (rfl); `erdos_684_unbounded_fc` and `erdos_684_rate_fc` (Bae's theorem with no f
   and no ⊤: infinitely many n with smallPrimePart n k ≤ n² for all 1 ≤ k ≤ min(n, C log n), resp. the 1/2 rate);
   `fThr_ne_top_eventually` and `unbounded_finite` (ASSUMING FC's upper-bound statement as a hypothesis — its proof is AItoBit's,
   not built here). All standard axioms (`bridge.log`). Mutants: M1 (conclusion ≤ n) and M2 (FC hypothesis weakened to n <)
   both fail to compile — sensitivity of the proofs, not falsity of the mutant statements.
4. **Readings (`seats/`).** Three separately briefed AI seats (Claude Opus 5.5, same model as the main seat — correlated readers):
   S statement/definitions — HOLDS WITH NOTES (Note A: the final statements are also met by any n with f(n) = ⊤; the bridge
   closes this given FC's upper bound); P the paper as written — HOLDS AS READ (fixes: §9 overclaims; Lemma 4.1 statement lacks
   "for all sufficiently large M"); W the world — Palomar PALOMAR-2026-09-03-000006 v1 replayed commit 4543ff7 (Lean 4.32.0,
   Mathlib 81a5d257; proof files identical to v3-arxiv — `git diff v3-arxiv 4543ff7 -- Erdos684Lean` is empty, re-checked by the
   main seat) through Comparator + Lean's kernel + nanoda on 3 Sep; no other public replay or audit found.
   Seat reports were written to disk by the main seat from the seats' final messages. A fourth, blind
   cold-read seat read the rendered page against this bundle (SHIP AFTER FIXES; 18 fixes applied before deploy, incl. withdrawing
   seat S's Note B — the 'axioms' it found are inside a docstring).
   The Erdős 1979 quote was checked against the scan (combinatorica.hu/~p_erdos/1979-23.pdf, sha256 a4703a10…dfd, pp. 76–77).
5. **Roy (Zenodo 23183198, 6 Oct).** `numerics/roy_check.py`: APSSV's n = M_K − 1 has u(n,k) = 1 for every k ≤ K
   (K = 30, 100, 300), contradicting that note's Theorem "for every n ≥ 3 and k ≥ 1 with k ≤ n/2, log u ≥ k/4 + O(k/log k)".

## Reproduce
Clone the repo at the tag into /tmp/e684/lean/repo, then `replay/run.sh`; `bridge/run_lean.sh $PWD/bridge/Bridge684.lean`;
`python3 numerics/ftable.py 60`, `python3 numerics/mutation.py`, `python3 numerics/roy_check.py` (needs sympy).
