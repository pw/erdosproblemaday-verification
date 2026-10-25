# Erdős #128 — refereeing Amir Sarid's 131/5000 claim (erdos cron seat, 2026-10-12 18:00Z, Fable 5.1)

Live page read first (via Hetzner): $250 problem, OPEN; one proof claim on the tab — Amir Sarid, submitted
2026-08-07 (paper dated 4 Aug 2026, repo github.com/aimir/erdos-128-sparse-halves @ ba85f319):
β(G) ≤ 131/5000 = 0.0262 for every triangle-free G (Razborov 2021: 27/1024 = 0.026367), CONDITIONAL on
Balogh–Clemen–Lidický Thm 2(a) (D₂ ≤ n²/23.5, n large). Lean 4 (683 files) with BCL as a hypothesis.
Comments tab: Cormundus 26 Jul 2026 computational census (no counterexample ≤ 26 vertices; SRG table).

## Hand check of the argument (host seat, before any seat ran)
- L2.1 β ≤ β*: pair-shift concavity; odd n leaves one coordinate = 1/2, delete it. OK.
- L2.2 blow-up invariance: β*, ρ, t(C4) scale; D₂(G(k)) = k² D₂(G) by multilinearity on the cube. OK.
- L3.2 = Razborov Prop 1.1 (β ≤ ρ/8 − C4/(12ρ), C4 = 3t with-repetition sampling ⇒ ρ/8 − t/(4ρ)); (4) recomputed:
  (1−p)Q_u + pQ_v = p(1−p)[ρ/2 − e(N(u),N(v))/n²]; (5) hom(C4) = 2Σ_edges e(N(u),N(v)) incl. degenerate 4-cycles. OK.
- P3.3: ρ/8 − ρ²/4 + γ/4 decreasing for ρ > 1/4; at 7/22: 7/484 + 293/25000 = 79203/3025000 < 79255/3025000. OK.
  At ρ = 5/16 the same formula gives exactly 27/1024 — Razborov's bound is this method at the Clebsch density;
  Sarid's gain is entirely the ρ < 7/22 branch.
- L4.3: S_x = p³R_x²(U_x − 1/2); HM–AM; 2R³/(R²+1) ≥ 2R − 1 = (R−1)²/(R²+1); averaging gives σ > 2 − σ ≥ σ. Tight on
  every regular uniformly-weighted graph (checked K2, C5, general k-regular: S = k³/(2h³) = 4μ³). OK.
- L4.4: (10) −Σ w w φ φ = S_x; barycentric endpoints; the three t₊t₋ cases ≥ L(α). OK.
- §4.2: masses of 1_X + a1_Y and c1_Y are n/2; B1 = aρ/2 + cI − (1+a)μ/(4c), B2 = μ/4; saving L(a)μ³/c². OK.
- L4.5: ν(a) = 2cP; a* = I₀/(ρ₀/2 + I₀) = 88/417; envelope (16); derivative bounds (7/1000, 1/300, 256/2209 < 1);
  c* = 329/417, μ* = 18424/173889, baseline 4606/173889 < 2649/100000, saving > (4/15)(21/200)³ > 29/100000. OK.
  Max ≈ 0.02617 at a*. |Y|/|X| = 417/241 as stated.

## Own instruments
- c4probe.py: exact rational t(C4) − ρ³ + γρ ≥ 0 on ALL 14,651 triangle-free graphs on ≤ 10 vertices (nauty-geng -t),
  Clebsch = 6.25e-12 = ερ exactly, C5 blow-ups, K_{8,8}; mutation control γ − 1/1000 VIOLATES on Clebsch. Log c4probe_10.log.
- The author's verifier: 38 hosts, 34 squares, min slack 0 (host 0 = Clebsch-tight), ε needed 1.991e-11 < 2e-11 — rerun here, 14 s.
- Kernel replay: /tmp/erdos1800/lean-build/ (Mathlib v4.30.0 @ c5ea0035 = the claim's pin, hard-linked from
  ~/MathDyad/lean/boxcover; toolchain ~/.elan v4.30.0). steps.tsv there.
- Seats (Opus, hostile, tools): math · cert (independent certificate verifier) · sources+world · lean (source audit).
  Briefs /tmp/erdos1800/seats/*.md.

## CORRECTIONS (2026-10-13, 09:00Z seat, from the cert and sources referee seats and the blind page read)
- "host 0 = Clebsch-tight" above is WRONG: the zero-slack host is host 0 = the EMPTY six-vertex graph (target and every square
  coefficient vanish identically there; cert seat F4, HOSTS.tsv row 0). The Clebsch graph has 16 vertices and is not a host; at the
  Clebsch graphon the certificate leaves slack ≈ 6·10⁻¹². The author's README makes the same error; the paper's "tight at Clebsch"
  refers to the inequality, not to a host.
- "Sarid's gain is entirely the ρ < 7/22 branch" above is WRONG: Razborov's quadratic C₄ inequality fed through Lemma 3.2 gives
  exactly 27/1024 at EVERY density (sources seat F2, sympy), so the high branch also needs the new cubic certificate; the cubic is
  stronger than Razborov's for ρ > 5/16 and for ρ < 3/16 (difference ρ(16ρ−5)(16ρ−3)/256), only the first range being used.
- The brief's label "European J. Combin. 2024" for BCL's max-cut paper was OUR error (seats/COMMON.md); the comments tab cites that
  DOI for the sparse-halves literature, and it resolves to "10 problems for partitions of triangle-free graphs". No journal
  version of "Max cuts in triangle-free graphs" exists.
