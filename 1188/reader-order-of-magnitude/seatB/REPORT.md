# Referee B — Erdős #1188, submission 8gfcew (Pedro Martins): Sections 4, 6 + lower-bound assembly
(Opus seat, 2026-11-02 ~09:03–09:54Z. Saved by the host from the seat's final message; harness blocked .md writes.
Code/outputs: referee/B/scratch/ — cover.py, split.py, random_split.py, neg_tau.py, lemma410_synth.py, large.py, table4.py, constants.py + *.out.)

## VERDICT: HOLDS WITH NOTES — no fatal finding, no gap. Every proof read line by line (pp. 11–25 vs rendered images).

## Findings
N1 (exposition): headline lower bound has no explicit x₀. Thm 4.8 uses K = ⌈4/ρ(1/g)⌉, P = largest prime ≤ √(x/K) (p.15),
   limits g → 0, ε → 0, de Bruijn with unspecified error ⇒ c1 = 0.0672 is a limit constant; only explicit lower bound is
   x/2 − 3x/log x (Thm 1.2). §8.4 admits Λ(x) is larger for x ≤ 10^16; the abstract does not say so.
N2 (exposition / numerics): classes reach far outside their fibres (A_λ fixes only its own valuation; B_t contains almost every
   point of a high fibre) ⇒ minimality rests on valuation-maximal private integers + labels τ(ι(q)) = q; random-point covering
   tests at large x are nearly blind (leaf deleted: 4000 random fibre points found nothing uncovered at X = 10^6, 10^7). The seat's
   own first "exhaustive" sampler had this flaw — caught by its leaf-deletion control (0 of 17 / 0 of 323 where 1 expected);
   corrected sampler (private-integer neighbourhood z ≡ ι(q) mod P, z ≡ 0 mod r^{E_r}) reports exactly 1/17 and 1/323.
   Paper's §8.2 large-instance checks test private integers + moduli, not covering — fine because covering is proved.
N3 (slip in wording): Construction 4.2 data need not exist for a given (P, I) (P = 13, I = {5,7,11}: M_F(13) = 72 has 12
   divisors, (T3) impossible). Prop 4.3 is correctly conditional; existence Lemmas 4.6, 4.9 check out.
N4 (exposition): Table 5 C1(0.3) printed "0.0459…", true 0.0459890 (truncated, others rounded).
N5: Remark 4.14(a) fine: max C1 = 0.06722014 at h = 0.2245; C1(0.225) = 0.06721936.

## Checked
Prop 4.3 (modulus → (q,e,σ); covering via Lemma 4.1 + tree walk; minimality: levels by valuations, fibres by digit u, siblings by
last common node label, every B_t). Prop 4.7 (all inequalities, some tight: N ≥ 0.063y ≥ y/20; log 20 + 1 = 3.996 ≤ 4; injectivity).
Lemma 4.10 (telescoping N₁ = Σ_e L_e/e; successor structure; N₁ < p − 1). Thm 4.8 (pool sizes, (6), m ↦ (d,s) injective; Rankin
step Lemma 4.12 via −log(1−t) ≤ t + t² on [0,2/3], Σp^{−4/3} ≈ 1.13 < 2; Lemma 4.11 within hypotheses; substitution β = 1−α−τ
gives C1, C2). Source of x log x: disjoint groups (p,d), independent padding assignments, L_p(d) ≈ x^β classes with β > h ⇒
β log x freedom per class; moduli p·d·s·r, density C2(h); nothing double counted.
Constants: two independent ρ (dilog closed form; delay-ODE integration) vs mpmath; controls ρ(2) = 1 − log 2, ρ(3) = 0.0486083883,
ρ(4) = 0.00491093. κ1 = 0.012679471691, κ2 = 0.038682047714; C1(0.225) = 0.067219355825, C2(0.2175) = 0.212875840462 (paper
0.0672193558 / 0.2128758404); all 9 rows of Table 5 agree. Own lower-Riemann certificate (high-precision floats, not interval):
n = 2000 control 0.0671803703 / 0.2126765337 (correctly fails); n = 10000 0.0672115579 / 0.2128359667 (certifies); paper
0.0672112649 / 0.2128349949. Remark 4.14(b) densities 0.0011/0.0488/0.2129/0.0441; C* = 0.124330; c1/3 = 0.0224 > 1/45.
Machine checks: checker controls (classical +; drop 7(12) −; add 0(8) −; {0(2),1(2)} −). Examples 4.4 (all 6720) and 4.5 (all 120 +
3000 random I-part-7) valid and distinct. 48/48 random Construction 4.2 instances exhaustive over periods ≤ 12,252,240 (depth 3, any
label order); 720 permutations of a 6-leaf group → 720 distinct valid systems. Negative controls: drop leaf / duplicate padding /
padding ∤ M_F(q) fail; τ with v₂ ≤ 1 (violating τ(ι(16)) = 16) fails minimality (8 mod 16 loses private integer); a "swap two τ"
control was vacuous (relabels t) — kept in random_split.out, replaced by the v₂ control. Lemma 4.10 bookkeeping: 200 synthetic
trials to depth 6 pass. Large: Prop 4.7 parameters X = 10^6 (P = 701, I = {17,19,23,29,31}, |G| = 30): 46,984 classes, 7,192 split,
109,702 covering points 0 uncovered; Lemma 4.10 trees X = 10^7 (P = 997, I = {11,13,17,19}, depth 2): 78,654 classes, 2,661 split,
709,981 points incl. 539,393 exhaustive hard-mode over 33 split fibres, 0 uncovered; distinct moduli ≤ X, every private integer in
exactly its own class; leaf-deletion + duplicate-padding controls fail as they should. Table 4 reproduced to every digit 10^8..10^14,
capacity at every p.
Section 6: Lemma 6.1 (three prime-power-top ranges ≤ 2x^{3/4} each), Lemma 6.2 anchor (tried anchor in a p-divisible class, p²
moduli — holds), Prop 6.4 (data determine system; t_p ≤ min(p, S/p + γ_p); 12x^{3/4} + 3b; split at √S), Thm 1.8, Cor 1.9, Thm 1.7
assembly — correct.
