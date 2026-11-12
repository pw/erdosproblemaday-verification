# Hostile referee (Claude Opus 5.5 seat, 2026-11-12) — our K_{2,t} placement lemma (ours/LEMMA.md)

**VERDICT: HOLDS WITH FIXES** — no mathematical error; fixes are wording/labelling/priority (all applied to the page
and LEMMA.md).
Checked: CRT choice of k (C_q has q²−m ≥ q_u resp. ≥ 2q_v consecutive integers, contains q·s_q; offset 0 lies in the
window so q² ∤ q·s_q ⇒ s_q ≢ 0; k prime to every prime) · F2 at both ends (offsets −⌊m/2⌋ … ⌈m/2⌉−1, |b−u| ≤ ⌊m/2⌋ <
w₁w₂ ≤ pp′) · F3 (−kΠ ≡ q·s_q mod q²) · counting (disjoint charges by F2; w_i²-multiples irrelevant — 4 to 21 per
instance present, bound unaffected) · odd case (max A⁺ = m, demand t+1) · PNT step (1.584X²+1.32X ≤ 1.69X² iff
X ≥ 12.45) · equality (⌊m/q_u⌋ ≥ w_t ≥ t+1). (P2) is effectively strict since q_u ∤ w_t q_v.
Objections (applied): (1) Chen's literal hypothesis places M = Π; we place kΠ — say his proof goes through verbatim for
kΠ, not that his literal hypothesis is verified. (2) "(b) modulo PNT" mislabel — PNT is a theorem; rigorous.
(3) State q² > m (implied by P2). (4) Keep "(2−ε)n is stronger for large n" in any headline; Chen main.tex l.91 shows
the ES window is "positioned so that a single integer u, divisible exactly once by each p_i …" — same device; claim only
its use to clear the q²-multiples. Priority: repo has no proof for every t (sec_remains l.356, l.393–395); run37
referee_opus.md §C.3 ASSERTED "refuted for every θ < 1 and every constant C" without proof — credit it.
Independent recomputation (refsolve.py: DP over capped valuation types + an integer programme solved to proven
optimality by HiGHS; both agree with brute force on 600 small random instances, 0 mismatches): t=2: 5/6, t=3: 8/9,
t=4: 11/12, t=7: 20/21 (n=2t / 2t+1); the IP also gives 3t−1 / 3t for t = 5, 6, 8–14. Window scans: u = kΠ is the only
element divisible by two primes of D, v_p(u) = 1, no q_u²/q_v² multiples; x+1 = u−⌊m/2⌋ in every log line. Chen's
printed t = 2, 3 examples: 5 and 8. Red control: k2t.py's old t = 9 instance ((P2) fails) has a q_u² multiple in the
window and gives 25 < 26. Stress: 400 random instances of the lemma as written (t = 2–6, X 13–259, random valid s_q,
random lift of k): 0 failures. exact.py review: the specials + interchangeable singles split is exact; no path to a
too-large minimum.
