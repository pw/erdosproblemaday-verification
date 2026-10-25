# Hostile referee brief — Erdős #203, the Quotient Lemma (lines / coarse tori)

You are refereeing a claimed result for erdosproblems.com/203 before it is published on a public scoreboard
(erdosproblemaday.com). Your job is to REFUTE it. Quote the exact sentence or line of code you object to. Do not
summarise; find what is wrong. If nothing is wrong, say HOLDS AS READ and list what you checked and how.

## The claim
Read `LEMMA.md` first (statement + proof of the Quotient Lemma; the two instances: lines and coarse tori; the coarsening
rule; what V_Λ(P) is and why V_Λ(pool(N)) < 1 excludes every covering system of period N). Then the computed claims
in `TABLE.md` (generated from the JSONL files by `table.py` — regenerate it yourself and diff):
  (A) For every period N ≤ 65,520 whose complete pool has density ≥ 1 (there are 26 of them; for the others the
      density condition already excludes), the line instance excludes N in EVERY direction tested (16 directions),
      with proven optimal values V well below 1 (worst case ≈ 0.93, best ≈ 0.53). This is a SECOND, independent
      route to the standing claim "no covering system has period ≤ 65,520" (the first used Theorem A's forced
      overlap of 5 and 7 plus the exact seven-prime block maxima of Theorem B).
  (B) For the open pools (110880 and possibly others — read TABLE.md for which): a direction whose PROVEN upper
      bound on the max–min is < 1 excludes the pool; a feasible choice with V ≥ 1 (witness re-counted) means that
      direction cannot exclude it. Check that no pool is called excluded on a FEASIBLE/time-limited run without a
      bound < 1, and that "bound" really is a proven bound (CP-SAT `BestObjectiveBound` for a maximisation).
  (C) Coarse-torus results, if any (`torus_*.jsonl`): INFEASIBLE in `--feas` mode = excluded; a bound ≥ 1 = undecided.

## What to attack (in order of damage)
1. THE LEMMA. Is the Quotient Lemma's proof correct? Specifically: (a) that a coset of L_p meets a cell y+Λ in a coset
   of L_p ∩ Λ (not merely a subset); (b) the index identity e_p = [G:S_p]·[Λ : Λ∩L_p]; (c) that "density of the union
   inside a cell ≤ sum of densities inside the cell" is the right inequality for a cell to be COVERED (a cell covered
   by ∪C_p has union-density 1 inside it); (d) the line instance's formulas i_p = gcd(a u_p + b v_p, e_p) and
   w_p = i_p/e_p — check them by direct enumeration on two primes of pool_720.json for a non-axis direction such as
   (2,-1); (e) the coarsening rule i_p ↦ gcd(i_p, M), w_p ↦ gcd(i_p,M)/e_p — check it by enumeration too; (f) the
   torus instance's lattice-image claim (torus.py --selftest enumerates it for T = 12, 10 — pick a different T).
   (g) Lemma 1 of the shipped entry (primes 2, 3 and the quadrant restriction change nothing) is ASSUMED here; say
   whether the reduction to coverings of ℤ² by cosets is sound as stated in LEMMA.md's first paragraph.
2. THE ENCODING. `linelemma.py::instance` and `::cpsat`: is the integer scaling exact (S = lcm of denominators; every
   weight integral)? Is `fix_one` (fixing the first lumpy prime's class to 0) a valid symmetry reduction — i.e. do
   translations τ ↦ τ+1 act transitively on the classes mod i_p of EVERY prime simultaneously, so that fixing one
   prime's class loses no generality? (The adversary chooses all t_p; shifting all t_p by c and τ by c is a bijection
   on configurations preserving min_τ W.) Is `recount_np` genuinely independent of the solver (it rebuilds W from
   E, the lumpy list and t)? Could the pool JSONs be wrong — recompute e_p, u_p, v_p for a few primes from scratch
   (u = discrete log of 2, v = of 3, in H_p ≅ ℤ/e_p; check 2 ↦ u by verifying that ord of u in ℤ/e_p equals ord_p 2).
3. THE VERDICT LOGIC. `excluded` is set when status OPTIMAL and V < 1, or when bound < 1. Confirm from the JSONL that
   every N listed as excluded in TABLE.md has at least one direction satisfying this, and that the claimed "every
   direction" statement for N ≤ 65,520 holds row by row (count directions, skipped ones included). Spot-check three
   rows by re-running `linelemma.py pool_N.json --dirs "a,b" --brute --milp` yourself (brute force only runs when
   ∏ i_p ≤ 3·10^6 — pick (0,1) at N = 5040 where it does).
4. THE CONTROLS. Run `linelemma.py --control` and `torus.py --selftest`. Then design one control of your own that
   the code must FAIL on: e.g. a pool where a covering EXISTS (two 'primes' with the same lattice and complementary
   cosets — construct one with e = 3 or 4) and confirm V = 1; and a mutation (halve one weight in the JSON) whose
   effect on V you predict before running.
5. THE SCOPE. The claim is about COVERING SYSTEMS of period N, i.e. finite sets of primes with e_p | N and one coset
   each. (i) Is "one coset per prime" right — could a prime p kill TWO cosets? (For fixed m, {(k,ℓ): p | 2^k3^ℓ m+1}
   is the preimage of ONE element −m^{-1} ∈ H_p, so one coset. Confirm.) (ii) Is pool(N) = all primes with e_p | N
   the right pool — are the pool JSONs complete (the shipped bundle certifies ∏ p^{v_p} = gcd(2^N−1, 3^N−1); the 13
   regenerated pools 7920 … 63360 were made by the same pool2.py — spot-check one by recomputing the gcd)? (iii) The
   perfect-power free sets (Theorem C of the shipped entry) are NOT handled by this lemma — is the page honest that
   the new exclusions are for the PURE covering mechanism only? (iv) Does excluding pool(N) exclude every DIVISOR of
   N (pool(d) ⊆ pool(N) and W only grows with the pool — confirm the monotonicity claim).
6. NOVELTY / WORLD. Has anyone stated this lemma for #203? Read the shipped entry's account of the 15 forum comments
   (bundle `verification/203/covering-forced-loss/`), AnimishSharma's density condition and veljjanoski's repository
   README; search for "line" / "projection" / "quotient" arguments on 2-D covering systems (Erdős–Graham p. 27 and
   the Sierpiński literature: a 1-D projection of a 2-D covering is a standard move — say so if it is, with a citation,
   and say whether the specific index/intensity formula is new or folklore).

## Files
`LEMMA.md`, `linelemma.py`, `torus.py`, `census_lines.py`, `table.py`, the `ll_*.jsonl` / `torus_*.jsonl` results,
the pool JSONs, the shipped bundle `~/ErdosProblemADay-main/verification/203/covering-forced-loss/` (README.md there
is the standing entry's receipts). Python 3 with ortools, scipy, numpy is installed (`python3`, also `~/.venv/bin/python`).
Work in `/tmp/ref203lines/` for anything you write; do not modify the originals. You may run solvers (nice 19, ≤ 2
workers, ≤ 10 minutes each) — the box is shared with long-running jobs.

## Output
A markdown report: VERDICT (HOLDS AS READ / HOLDS WITH FIXES / GAP AT …), then numbered findings each quoting the
offending text or code line, each tagged FATAL / FIX / NOTE, then the list of what you recomputed and what you got.
