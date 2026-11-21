# Hostile referee (Opus 5.5 seat, briefed to refute, own solvers written before reading ours) — 21 Nov 2026

Verdict: the reader's bound holds. C = 61487/77376 ≈ 0.794652 is a valid upper bound, and a conservative one. The fixes are
to his exposition, not his numbers: the submission states no framework, and one side remark has wrong arithmetic. Our side
checks out: bound.py computes a valid lower bound on W, and our profiles match the referee's at every point where both exist.

1. Partition lemma, density of S, block inclusion (closed interval [1, N/m]), asymptotic (h = Σ_{d∈J}[t ≥ d], finite J,
   tail term h(M)/M included), refinement F_{pM}(t) ≤ F_M(t) + F_M(t/p) for p ∤ M, δ_{pM} = δ_M/(1+1/p): correct.
   "Distinct" forces k ≥ 2; all programs implement it.
2. Its programs: ihs.py (implicit hitting set; masters RC2 MaxSAT / SCIP / Minicard; exact big-int subset-sum separation;
   every set re-checked by a second separator) and c/refdfs.c (include/exclude search, same family as our prof.c, written
   separately). Positive control: A390394 n = 1..22 with all three masters. Negative control: BUG=1 changes it. Limit:
   BUG=2 (off-by-one at the mask's top bit) is invisible to the n ≤ 22 control, which is why every set is re-checked.
   F values: 5040 all 60 divisors (refdfs; ihs agrees to t = 140); 55440 to t = 144 (refdfs; ihs agrees to 84);
   720720 to t = 70 (ihs; refdfs agrees to 66). Profiles in profiles/.
3. Reader's claims: W_5040 = 3907/5040 exactly. 55440 excess: +1 on [36,42), 0 on [42,55), +1 on [55,56), +2 on [56,60),
   +1 on [60,77), +2 on [77,80), +1 on [80,84), +2 on [84,88), +3 on [88,112), +2 on [112,126] — all six intervals hold,
   each an understatement (integral over [1,126) is 103/4620 vs his 257/18480). 720720: +1 on [60,70); his [65,66) holds.
   All stated fractions exact. Objection 1: "improves … by 121717/77376000" — true difference 365/232128 ≈ 0.0015724.
   Objection 2: "certified … via exact branch-and-bound / MILP" — no certificate, code or framework given.
   From its own profiles: C ≤ 61267/77376 ≈ 0.791809 (55440 level 0.792425); its mybound.py and our bound.py agree.
4. Ours: zero disagreements across 12 files on the overlap. bound.py valid at every step (exact h = (i+1) − F; missing data
   = 0; child bound lbc(d) + lbc(d/p) with exact Fractions at non-integer t/p; step functions constant between divisors of
   pM; running max legitimate (h nondecreasing); integral Σ lb(d)(1/d − 1/next) + tail). Sanity: no data ⇒ C = 1; only
   5040 data ⇒ 0.798025 at every level. Objection 3: our "+3 on [88,110)" is +3 on [88,112) (at 110: 23 − 19 − 1).
   Objection 4 (process): profile3.py re-checks cuts only after the loop, and no CP-SAT log reached that line; it re-checked
   every saved cut set: 11 files, 0 non-solutions. Caveat: values beyond its overlap (55440 past 144, 720720 past 70,
   all of 110880 and 1441440) are single-source for the referee.
5. Other failure modes (definition, block subset, t = N/m exactly, tail, o(1), p ∤ M, h at non-integer t/p): none found.

Main seat's responses: objection 3 fixed on the page; objection 4 answered by scip_recheck.py, which re-checks every cut of
each frozen dump in Fractions before re-solving (all genuine), and by the per-step dumps; the caveat is why the headline
uses only values confirmed by two programs or by a published constant (see analysis/final2.py, version A).
