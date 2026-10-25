# Erdős #160 — the two upper-bound claims on the proof-claims tab, refereed (13 October 2026)

**Problem.** h(N) = least number of colours on {1,…,N} such that every nontrivial four-term arithmetic progression
sees at least three distinct colours (erdosproblems.com/160; Erdős 1989, with Freud). Page (last edited 2 Dec 2025):
h(N) ≪ N^{2/3} (LeechLattice, MO 410808, 2021), h(N) ≪ N^{log 3/log 22 + o(1)} (Hunter, 18 Oct 2025, from DTZ's ℤ/22ℤ
3-colouring), h(N) ≫ exp(c (log N)^{1/9}) (Bloom–Sisask via the elementary reduction).

**Claims refereed (both live on the tab on 13 Oct 2026, captures in `live/`).**
1. Rio Itabe, *A candidate N^{1/3+o(1)} upper bound for Erdős Problem 160*, 14 Jul 2026, GitHub
   `ritabe-dev/ErdosProblem160-OneThirdUpper` tag `v0.2.1-review-candidate` (commit fd426c9003c2acbae3e668c462b8fed73c41fb1c;
   PDF sha256 acac7779…ee65a), with a Lean 4 development. Claim: ∀ ε > 0, eventually h(N) ≤ N^{1/3+ε}.
2. Ruizhe Shi, Yiqi Dong, *An improved upper bound for colorings without symmetrically colored k-term APs*, arXiv:2607.20752
   (v1 22 Jul, v2 28 Jul 2026). Claim: a (k−1)^{k²/4−1}·p-colouring of ℤ/p^{k²/4}ℤ with no nontrivial symmetrically coloured
   k-AP (even k ≥ 4, prime p > k); for k = 4 a 27p-colouring of ℤ/p⁴ℤ; h(N) ≤ N^{1/4+o(1)}; ρ₄(α) = O_ε(α^{5−ε});
   Gowers's Conjecture 4.2 (GAFA 2001) false for every even k ≥ 6.

**Verdicts.** Shi–Dong §§2–5 (seat A): HOLDS AS READ — Theorem 1.1, Cor 1.2, Cor 4.3, Cor 1.3 follow; two minor GAPs in the written
proofs, each closing in one line (Lemma 2.2 iterates Lemma 2.1 on a step-exactly-p case outside its range — carries still constant;
Lemma 5.3's "opposite sides of M/2 ⇒ τ differs" is false at x = M/2 but the one boundary carry lands on 0), seven EXPOSITION notes.
Shi–Dong §6 + world (seat B): HOLDS AS READ — (1)/(2) match DTZ Thm 1.8 / Prop 2.4+Thm 2.8 exactly; exponent arithmetic correct;
Conj 1.10 refuted with DTZ's quantifier order; "first counterexample for even k ≥ 6" holds up (DTZ's local-lemma N^{2/k} and the k = 4
colouring both fall short; nothing else found); FT24's all-layer colouring is NOT symmetric-free (explicit counterexample), Shi–Dong not a
corollary of it; priority: Itabe public 8 days before v1. Itabe Lean (seat C): STATEMENT MATCHES — siteH = Formal Conjectures
erdos_160.h ∀n (IsFourTermAP ↔ IsAPOfLength 4, provable, not proved in the repo = E1); hypotheses discharged; prime from Mathlib's
Bertrand. Itabe prose (seat D): HOLDS AS READ, 12 EXPOSITION. Host: both constructions read lemma by lemma; brute-force and replay
instruments below. Overall: both claims hold as read; the problem stays OPEN; nothing in the bounds is ours.

**Also ours: exact values.** h(N) = 3 for 4 ≤ N ≤ 12, 4 for 13 ≤ N ≤ 22, 5 for 23 ≤ N ≤ 35, 6 for 36 ≤ N ≤ 51; h(52) undecided (900 s cap)
(`exact-table/`). Not in OEIS (terms search 13 Oct 2026 via oeis.org: no match — `exact-table/oeis_search_2026-10-13.txt`). Blind consistency read of the rendered page before deploy: `seats/E_blind_read.md` (33 findings, all applied via `fix160.py`).

## Chain and controls

### Shi–Dong (`shidong/`)
- `check_shidong_k4.py` — Python: irreducible cubic by brute force (first found), norm as z^{1+p+p²} in F_p[T]/(f), anisotropy
  checked by enumeration, colouring c(n) = (τ(x₀),τ(x₁),τ(x₂), x₀ + N(x₁,x₂,x₃)) with τ(x)=⌊3x/p⌋ on ℤ/p⁴ℤ, EVERY (a,d),
  d ≠ 0 tested for c(a)=c(a+3d) ∧ c(a+d)=c(a+2d). Controls (must each find violations): drop the norm coordinate;
  replace the norm by the isotropic cubic x₁³; drop τ on digit 1. Logs `check_shidong_k4_py_p5_7.log`, `check_shidong_k4_py_p11.log`: p = 5, 7, 11 → 0 violations,
  palettes 125, 187, 297 (≤ 27p; which colours are attained depends on the cubic), all controls fire.
- `check_shidong_k4.c` — C, decorrelated: a different irreducible cubic (search from the top of the coefficient range), norm as
  the determinant of the 3×3 multiplication-by-z matrix, unsigned modular enumeration. Logs `check_shidong_k4_c_p5_7_11.log`,
  `check_shidong_k4_c_p13.log`: p = 5, 7, 11, 13 → 0 violations over 625·624, 2401·2400, 14641·14640, 28561·28560 pairs;
  palette 123, 189, 297, 351 (= 27p for p ≥ 7); all three controls fire at every p.
- `sample_shidong_k6.c` — Theorem 1.1 at k = 6, p = 7 (ℤ/7⁹ℤ, 5⁸·7 colours, layers P₁ + P₃ + P₅, irreducibles T³+2 and
  T⁵+T+3 found by brute force, norms as determinants, anisotropy enumerated): 10⁸ random 6-APs + every d from 3 random starts
  (121,060,818 more) → 0 symmetric; no-Q control → 13 symmetric in 10⁸. Sampling, NOT a proof. Log `sample_shidong_k6_p7.log`.
- Reading: host seat (every lemma, boundary cases named in the entry) + seats A (math §§2–5 and the #160 reduction) and
  B (§6 transference/Gowers, priority, literature) in `seats/`.

### Itabe (`itabe/`)
- `check_itabe.py` + `check_itabe.log` — his three labels rebuilt from the manuscript: cubic factor ν_p on [0,p³) and on
  ℤ/p³ℤ for p = 5, 7, 11 with a RANDOM irreducible cubic each (basis-independence tested): 0 proper-ABBA, palettes 35/55/91
  ≤ 9p, controls (no norm / isotropic) fire; mod-24 label λ_{P,L} for (P,L) = (25,1),(25,2),(49,1): 0 three-equal, 0 ABAB,
  control (digits dropped) finds ABAB on every horizon and three-equal at L = 2 (the L = 1 horizons have too few digits for
  the square norm alone to admit a three-equal pattern — the control's silence there is about the control, not the claim;
  exit code 2 = "cannot see" on that account, recorded honestly); dyadic label μ_{B,L} for (B,L) = (4,2),(8,2),(16,2),(8,3):
  0 AABB, control (buckets dropped) fires. Seat C's independent rebuild (`seats/c_itabe_check/`) agrees, p up to 13.
- `replay/` — kernel replay on this box: `run.sh` (driver; its first `lake build -j2` failed instantly — Lake 5 has no `-j` —
  so its three audit steps ran on an unbuilt tree and are superseded), `run2.sh` (re-ran the audits after the author's own
  `scripts/check_release.sh` built the project), `steps.tsv` (every step, rc, seconds), `check_release.log` (21 modules
  built, "All checks passed."), `their_axioms.log` (9 endpoints, each `[propext, Classical.choice, Quot.sound]`, the
  threshold identity `[propext, Quot.sound]`), `axioms.log` (our `Axioms160.lean`: pp.all statements of the two headline
  theorems + `siteH` + `IsFourTermAP`, then axioms of 5 declarations incl. `natCubicColour_abba_free` and the +1 bridge),
  `negcontrol.log` (a sorry'd theorem → `sorryAx` reported), `source_scan.log` (empty: no sorry/admit/axiom/native_decide/
  implemented_by/extern/unsafe/partial/opaque in first-party sources). Toolchain Lean v4.30.0, Mathlib v4.30.0 (tag), cache
  get 183 s, build 174 s. `leanchecker --fresh ErdosProblems.E160.RealAsymptotics` over the Mathlib closure: exit 0 after 3,125 s (started 2026-10-13 18:17:37Z; `itabe/steps.tsv` row `leanchecker_fresh`, log `itabe/leanchecker_fresh.log`); controls in `itabe/leanchecker_controls.log` (non-existent module rc 1, non-fresh `Problem` rc 0). Landed 19:09Z, recorded by the 21:00Z seat.
- Statement match: `siteH` (Problem.lean) = the Formal Conjectures `erdos_160.h` with `IsFourTermAP` in place of
  `Set.IsAPOfLength 4`; seat C proves the two predicates equivalent on every set of naturals (both exclude d = 0; sets ignore
  orientation), so `siteH n = erdos_160.h n` for every n — an equality the repo does not itself prove (seat C's E1).
- Seats C (Lean sources + statement) and D (prose) in `seats/`.

### Exact table (`exact-table/`)
- `exact_h.py` — per (N,k) CNF: one-hot colours; y_{n,{c,c'}} ↔ (x_{n,c} ∨ x_{n,c'}); for every 4-AP and colour pair the clause
  ¬y₁∨¬y₂∨¬y₃∨¬y₄; symmetry break colour(1)=0; CaDiCaL; monotone search k ↑; every SAT witness re-verified by an independent
  Python check of all 4-APs. `exact_h.tsv` (N, h(N), solver seconds, witness) + `#UNSAT` rows; `exact_h.log`.
- `verify_unsat.py` — SECOND encoding (equality indicators e_ij ↔ ∨_c (x_ic ∧ x_jc) per progression; the seven forbidden
  two-colour equality patterns) on a SECOND solver (pysat Glucose 4): `verify_unsat_glucose4.log` re-proves UNSAT at (13,3)
  and (23,4) and SAT (with verified witnesses) at (12,3), (22,4); `verify_unsat_h6.log`: (35,5) SAT with verified witness and **(36,5) UNSAT** (3,072 vars, 11,905 clauses) — landed 18:44Z after the ship, so all three thresholds are now re-proved on the second solver/encoding. The table search itself stopped at (52,6) on its 900 s cap (`exact_h.log`), so h(52) ∈ {6,7} is undecided.

### Live captures (`live/`)
erdosproblems.com/160, its proof-claims tab, MathOverflow 410808 — fetched 13 Oct 2026 18:0xZ through our Hetzner box.

## Reproduce
```
cd shidong && gcc -O2 -o check_shidong_k4 check_shidong_k4.c && ./check_shidong_k4 7      # 0.05 s; 13 → ~1 min
python3 check_shidong_k4.py 5 7                                                            # ~1 s
gcc -O2 -o sample_shidong_k6 sample_shidong_k6.c && ./sample_shidong_k6 100000000           # ~20 s, 160 MB
cd ../itabe && python3 check_itabe.py                                                      # ~25 s
git clone https://github.com/ritabe-dev/ErdosProblem160-OneThirdUpper && cd ErdosProblem160-OneThirdUpper && git checkout v0.2.1-review-candidate
lake exe cache get && bash scripts/check_release.sh && lake env lean --trust=0 ../Axioms160.lean   # Lean v4.30.0; ~6 min
cd ../exact-table && python3 exact_h.py 50 900 && python3 verify_unsat.py 36 5             # cadical on PATH; pysat
```
