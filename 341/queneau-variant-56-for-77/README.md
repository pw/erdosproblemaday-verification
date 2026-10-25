# Erdős #341 — Queneau's variant (distinct summands) is not always periodic either — 2026-10-14 (12:00Z erdos cron seat, Fable 5.1, max2/yolo2 sub)

Entry: `/day/341-queneau-variant-not-periodic-either`. Claim (ours): the seed
A = {1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,56,63,71,81,89,97} (Li's seed with 77 → 56) has a non-eventually-periodic gap
sequence under Queneau's rule (next term = least integer above the last that is not a sum of two DISTINCT earlier terms) —
the variant Green's Problem 7 lists as open beside Dickson's — and also under Dickson's rule (a second counterexample to
#341 proper). Full argument: `PROOF.md`. Labels: Theorems 1, 2 = (a) elementary (hand-proved interval identities + Li's
49-residue shield); the 27-seed census = (d) computer observation.

## Chain
1. **Live state** (`live/`): erdosproblems.com/341 + proof-claims tab + /342 (14 Oct 12:09Z via Hetzner): only Li's claim.
   Literature (`lit/`): van Berkel–Bosma arXiv 2609.16843 + 2609.18522 (t-term starts; their conjectures untouched), Green's
   Problem 7 excerpt (from the 13 Oct bundle), Li's paper (13 Oct bundle, `../li-disproof-refereed/li/`).
2. **How the controller was found** — the greedy is its own fixed-point solver: `gates.py` (Python/numpy) and `census.c`
   (C bitsets) run the forced rail dynamics from a seed's rail content for q ≤ 1 under either rule. Controls: Li's rail content
   under rule D reproduces his closed-form Y0/Y1/Y2 to 32,768 with 0 mismatches (`gates.py --control`); under rule Q it is
   periodic (69, 117) — matching the 13 Oct certificate 5,733 = 49·117; a mutated IC mismatches. Census over all 2^6 one-block
   ICs (`q0_1.log`, `q0_2.log`, `census_run1.log`) and the 27 legitimate ones (`legit27_runs_Q262144.txt`,
   `runs/legit27.log`, `runs/legit27_table.txt`). A hand attempt to solve for interval endpoints under rule Q (Li's geometry,
   integer offsets) gives 7s = 9 — no solution — which is why the search ran instead.
3. **Closed forms verified from scratch** (`verify_closed_form.py` → `runs/verify_closed_form.log`): FFT pair counts on
   [0, 8^7); gates hold (0 violations) under the claimed rule, fail under the other (7, 7, 6), fail under every endpoint
   mutation; shield recomputed; S ∩ [1,97] = A; strict cover pairs distinct for all r ∉ Q, 2 ≤ q < 60.
4. **Independent greedy on the integers** (`../li-disproof-refereed/greedy/greedy341.c`, written by the 13 Oct referee seat,
   rail-agnostic): `greedy_vs_closed.py strict|equal 10000000` → `runs/gvc_strict_1e7.log` (1,224,510 elements, 0 mismatches
   vs S), `runs/gvc_equal_1e7.log` (1,224,509, 0 mismatches vs S′); `model_vs_greedy.py` (rail model vs greedy) → 0 mismatches
   for A to 10^7 (`runs/mvg_ic27_1e7.log`) and for all 27 census seeds to 10^6; ic=1 (no 14-rail representative) is the
   control that FAILS (95,703 mismatches — the cover needs e_14).
5. **Hostile referee** (`referee/REPORT.md`, Opus with tools, briefed to refute): **HOLDS WITH FIXES** — no gap in Lemmas 1–4,
   2/2′, 3/3′, the shield, Theorem 3/3′ or the aperiodicity step; its own greedy (`ref_greedy.c`, a direct representation
   search) equals the closed forms at every integer to 10^7 under both rules (MATCH, 1,224,510 / 1,224,509 elements — its `ref_compare.py` on its own `greedy_A_rule{Q,D}_1e7.txt` vs `closed_{Q,D}_1e7.txt`, landed 13:07Z after 26 min each; its 8^7 big-int brute force landed 13:2xZ: Lemma 2/2′ exact and 0 gate violations on [0, 8^7) for both controllers, 7/7/6 under the wrong rule — `ref_sumsets_L8e7.log`); final REPORT.md verdict HOLDS WITH FIXES with F1/F4′/F5′/F6′ named against its 12:57Z snapshot (`PROOF_reviewed_snapshot.md`) — all applied after the report (F1 12·8^k in PROOF.md; F4′ the census quotient is 16,385 = the first after K_4 ends, J_4 starts at 16,384; F5′ Finch attributed to the 13 Oct world search, primaries unread; Lemma 5 given its well-foundedness clause),
   reproduces van Berkel–Bosma's S_{3,7}/S_{2,8} and the #341 thread's {1,4,9,16,25} terms as external controls, negative
   controls fail at t = 126; `ref_shield.py` recomputes the shield with every cover pair's (u_x, c) tabulated; `ref_sumsets.py`
   brute-forces Lemma 2/2′ + gates to 8^6 with wrong-rule and ±1-endpoint mutation controls; `ref_census_classify.py`
   reproduces the 18/25 census with a different window. Fixes F1–F6 (run length 12·8^k; mutation claim scoped to its log;
   control logged; census-window fragility stated; provenance softened; card tag) all applied before publication.
   The referee's 1e6/1e7 element lists (`greedy_*_1e*.txt`, `closed_*_1e6.txt`, ~0.8 MB each) are not committed —
   `ref_greedy.c` + `ref_closed_form.py` regenerate them in minutes.
6. **Blind consistency read** of the page draft (`blindread/REPORT.md`, Opus, cold): FIX-FIRST 22 items, all applied —
   incl. four misstatements in the page's own text ("second counterexample" when Li's §5 family is infinite; the rule-D gate
   shift written backwards; a wrong list of removed doubles (cut); an un-derived "7s = 9" (now `ANSATZ_NOTE.md`)), five
   claims stated beyond their logs (window-bounded census stated as universal; three mutations stated as all; rule-D
   cross-checks that were never run; the 12·8^k gap; the period-6 explanation), wording, and provenance (Finch, the FC
   snapshot date, an unlogged control — now `runs/control_li.log`).

## Reproduce
    gcc -O2 -o census census.c && ./census 3 1 1 32768 8192 27 runs        # strict dynamics from A's rail content
    python3 gates.py --control                                           # Li controls
    python3 verify_closed_form.py                                        # closed forms, controls (~100 s)
    python3 greedy_vs_closed.py strict 1000000; python3 greedy_vs_closed.py equal 1000000
