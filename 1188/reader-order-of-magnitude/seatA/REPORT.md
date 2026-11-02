# Referee A — Erdős #1188, submission 8gfcew (Pedro Martins)
(Opus seat, 2026-11-02 ~09:03–09:19Z. Saved by the host from the seat's final message; the harness blocked the seat from writing .md files.
Scripts/outputs: referee/A/scratch/ ; rendered pages referee/A/pages/.)

Scope (printed numbering): Sections 1, 2, 3, 5, 7 — Thm 1.3, Cor 1.4, Thm 1.5 + Prop 7.2, Cor 1.6, Lemmas 2.1–2.3, Construction 3.1 / Prop 3.2, Thm 1.2 + Prop 7.1.

## VERDICT: HOLDS WITH NOTES
No fatal defect, gap or slip in scope; three notes (wording / citation only). Every proof read line by line, formulas re-read from rendered pp. 4, 8–10, 21–22, 26–28. Scope establishes log F(x) ≤ (1−log2) x log x + 1.5x (all x ≥ 2) and log F(x) ≥ x/2 − 3x/log x (all x ≥ 40), hence log log F/log x → 1 elementarily. The x log x lower bound is Section 4 (seat B).

## Findings
N1 — exposition (abstract p.1): "for every prime p, the classes whose moduli are divisible by p project onto all residues modulo the largest power of p dividing a modulus" — vacuous-case wrong for p dividing no modulus (p^e = 1, empty family). Thm 1.3 (p.4) states it correctly ("let p be a prime dividing at least one of its moduli"). Cosmetic.
N2 — citation not verified (Section 7 p.26, R1–R5): Rosser–Schoenfeld [22] behind a bot wall; equation numbers unchecked (weak recollection θ bound is (3.16) not (3.14); not filed). Every inequality AS QUOTED with its range holds at extremal points for all t ≤ 10^8, 0 violations; negative controls fire (1.25506→1.2: 23 violations; 286→2: 32; 563→2: 65).
N3 — observation: the full data map is injective at small P (all 96 data at P=5, all 69,120 at P=7 give distinct systems), so ∏(p−1)! is conservative; no double counting.

## Line-by-line (no defect)
Lemmas 2.1–2.3 correct. Thm 1.3 correct, allows repeated moduli; Σp^{e−v} ≥ p^e, each term ≤ p^{e−1} ⇒ |A_p| ≥ p regardless of differing valuations. Cor 1.4 correct incl. boundary P+(n) = √x at x = p². Thm 1.5 injection into ∏(residues ∪ {∗}); formula (7) right. Prop 3.2: d* exists (<2P, | M(P), P∤d*), CRT coprimality, (top,cof) = (q,σ) / (P,τ(t)), moduli ≤ P(P+3), covering, minimality (i)(ii) correct. Thm 1.2 injectivity correct; asymptotic (3) correct. Prop 7.1 every step re-derived (1.3769 < 1.377; 17²/(2 log 17) = 51.004; 2.5+0.4+0.0117 < 3 at L=20; ranges fit). Prop 7.2: integer x suffices; (R5) at x and √x ≥ 286 gives log2 − 5/(2L²); final ≤ (1−log2)xL + 1.477x for L ≥ 11.312. Cor 1.6 correct. x ≥ 40 is the right threshold (P=3 fails: 6 ∤ M(3) = 2).

## What was run (nice 19, ulimit -v 8e6, timeout)
1. upper.py: Υ(x) for every integer 2 ≤ x ≤ 10^8 (paper: to 81,796). Max (Υ − (1−log2)x log x)/x = 0.541754 at x = 50 (matches paper 8.7(ii)); max 0.1774 over x ≥ 81,796; 0 violations. |S_x| vs (7) at 14 points; Table 2 reproduces 10^3..10^8; proof's intermediate inequalities 0 violations on [81796, 10^7] (min slack 0.056x).
2. lower.py: Λ ≥ X/2 − 3X/log X at every step endpoint X = P'(P'+3), primes to 10^8 (X ≈ 10^16; paper 4.85·10^8 certified, 2.2·10^14 float): 0 violations; max (X/2 − Λ) log X/X = 2.5874 at X = 928 (matches 8.7(i)); brute every integer 40 ≤ x ≤ 10^7: 0 violations, worst 2.5861 at 927.
3. brute_small.py: exact-integer factorial check for x ≤ 3000, identical; absolute margins ~48 / ~56, so float error irrelevant.
4. construction.py: literal Construction 3.1 + exact checker over Z/L. Controls: POS classical (True); NEG drop 7 mod 12 (not covering); NEG add 0 mod 8 (no private residue); NEG add 3 mod 6 (moduli not distinct); NEG modulus > xmax; NEG shift 1→3 mod 4 (not covering). Ex 3.3 reproduces. P=5: all 96 data valid, 96 distinct; P=7: all 69,120 valid and distinct; P=11 (d*=12 and 14): all 34,560 σ_p choices valid, distinct = ∏(p−1)!; P=11 300 random, P=13 60 random, P=17 6 random: 0 failures. Class counts = Σ(j(q)−1) + P.
5. localtest.py: 3,200 random certified-minimal coverings (3,088 with repeated moduli), 6,339 system–prime pairs: projection onto Z/p^e, Σp^{−v} ≥ 1, |A_p| ≥ p — 0 failures; NEG non-minimal {0 mod 2, 1 mod 2, 0 mod 3} fails at p=3.
Limits: [22] not obtained; double precision outside x ≤ 3000 (margins ~50); P=19 not run; Sections 4, 6, 8 (except 8.7) out of scope.
