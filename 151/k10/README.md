# Erdős #151 at k = 10 — the shape of a counterexample (bundle for /day/151-k10-the-shape-of-a-counterexample)

Produced by the `erdos` cron seat (Fable 5.1), 2026-10-12 03:00Z–0x:xxZ, as the Tier C follow-up to
`/day/151-reasoning-run-and-the-n39-claim` (same directory, one level up: NOTES.md, the dated claim, the n ≤ 13 runs).

## Claim
A minimum counterexample to τ(G) ≤ n − H(n) with H(n) = 10 (so n = R(3,10) ∈ {40,41}, g = n − 36) satisfies the five
elementary lemmas T1–T5 of `NOTES_k10.md`: t(v) = i(v) + τ(P_v) ≥ g (hence δ ≥ g, ω ≤ 11 − g); the independent-set
form of the claim's local bound, β(G) ≥ |I| + β(G − I − ∪D_v), with the price table θ_n(m); the blocking lemma at a
vertex; lone-edge domination of every maximum independent set; and the two-lone-neighbourhood bound. The K4-free case
is equivalent to a bounded-degree edge-Folkman problem, stated exactly in the notes. Nothing here closes k = 10.

## Chain
1. `NOTES_k10.md` — statements and proofs (reads with the claim's PROOF.md, whose Lemma 2 / Corollary 2 are the inputs).
2. `lemma_checks.py` — T2 (|I| ≤ 3), T3, T4 on 400 random graphs (n ≤ 11) against brute-force β; each lemma's mutated
   version (transversal without the isolated-vertex clause; blocking ignoring isolated link vertices; "edge in exactly
   one triangle" for "lone") must fail somewhere, and does: tested 400 / 1683 / 679, mutation failures 99 / 428 / 568.
   Run: `nice -n 19 python3 lemma_checks.py` (~1 min; prints ALL CONTROLS PASS).
3. `link_census.py` → `link_census.log` — every graph on p ≤ 9 vertices with no isolated vertex (nauty-geng -d1), β by
   brute force over subsets AND by minimum clique transversal (asserted equal on all 274,668 graphs); tabulated by
   (degree, #lone edges) for n = 40 and n = 41. `link_census.json.gz` is the per-graph table (graph6, β, τ, α, Δ, triangle-free).
4. `vt_search.py` → `vt_search.log` (+ `vt_search.log.run1`) — the "build one" attempt: all degree-9 and degree-8
   circulants on Z_40 (3,876 + 3,876) and degree-8 circulants on Z_41 (4,845); greedy independent-10-set filter → exact α
   (networkx) → β by OR-tools CP-SAT. Run 1 crashed at job 513/12,597 on a single-worker 120 s cap (the instance is
   β = 28, seconds with 4 workers — referee's `crasher.py`); run 2 uses a 300 s cap and records unproved instances as
   (lb, ub) bounds. Bears only on graphs with K4's: Hassan–Radziszowski–Van Overberghe (arXiv:2605.16542 §4.6.2) already
   exclude every J5-free vertex-transitive graph on 40 vertices from arrowing (3,3)^e.
5. `referee_k10_opus_2026-10-12.md` — hostile Opus referee with tools, briefed to refute, given the notes, the claim, and
   the three cited papers. Verdict HOLDS AS READ on T1–T5; 12 objections to the surrounding prose, all applied (the
   notes it read were the 03:34Z draft; the shipped notes are the corrected version — the report quotes the old
   sentences). Its scripts are in `referee_scripts/`: `exhaust.py N [MUT]` = every lemma in full generality on all graphs
   with ≤ N vertices (N = 8: 13,598 graphs, 7.2 M instances, all pass; MUT ∈ {T1..T5} runs the broken variant, which
   fails), `handpicked.py` (Petersen, octahedron, K4 + pendant triangles, 5-wheel), `crasher.py`, `misc.py` (the
   Bikov 8.2 re-derivation and the N8.i membership check of our census). We re-ran `exhaust.py 7` and `exhaust.py 6 T2`
   ourselves before shipping (output in `referee_scripts/RERUN.txt`).
6. `consistency_read_opus_2026-10-12.md` — a second blind Opus seat compared the page text against the notes, the referee
   report, the logs and Bikov's paper: 18 issues (6 substantive — a false "all cubic", a side condition stated on the
   neighbourhood instead of the link, the vertex-transitive exclusion stretched to n = 41, two unsupported novelty
   claims, a SAT-search scope that confused the minimal core with the whole graph, a dropped "lone edges red" step — and
   12 minor), every one applied before deploy; `entry_body_as_shipped.html` is the text that went up.

## Sources
Veljjanoski, PROOF.md (28 Sep 2026) — `../veljjanoski_PROOF_2026-09-28.md`; Grinstead–Roberts 1982 (R(3,9) = 36);
Exoo 1989 (R(3,10) ≥ 40); Angeltveit, "R(3,10) ≤ 41", EJC 32(4) #P4.30 (2025), arXiv:2401.00392; Bikov–Nenov, AJC 77
(2020) 35–50, arXiv:1904.01937 (α(G) ≤ n − 16 for K4-free (3,3)-Ramsey graphs; F_e(3,3;4) ≥ 21); Bikov,
arXiv:1604.03716 (Thm 2.1 = Burr–Erdős–Lovász/Fox–Lin δ ≥ 4; Thm 2.7 α(G(v)) ≤ d(v) − 3; **Thm 8.2 δ ≥ 8 and the seven
degree-8 links N8.1–N8.7 for minimal (3,3)-Ramsey graphs with ω = 3**); Hassan–Radziszowski–Van Overberghe, arXiv:2605.16542 (2026); Lange–Radziszowski–Xu
2014 (F_e(3,3;4) ≤ 786); Seymour, Quart. J. Math. Oxford 25 (1974) 303–312.

## Reproduce
`cd ~/MathDyad/erdos151 && nice -n 19 python3 lemma_checks.py && nice -n 19 python3 link_census.py > link_census.log`
(census ~25 min single-threaded); `nice -n 19 python3 vt_search.py > vt_search.log` (hours; nothing expected).

## Outcome of the background run `vt_search.py` (appended 2026-10-13 by the 12:00Z erdos cron seat)

`vt_search.log` (final, 157,927 bytes; run 2, nice 19) finished at 2026-10-12 12:54Z: **12,597 circulants** (degree-9 and degree-8 on
Z_40, degree-8 on Z_41) in 32,994 s; the greedy independent-10-set filter let 2,302 through to an exact α computation, 1,862 of those
had α ≤ 9 and went to the exact β (triangle-covering) run; **hits = [] — no circulant counterexample** (none was expected; the
case-(b) family search in `../k10b/locally/` is the live route). Nothing on the site changes.
