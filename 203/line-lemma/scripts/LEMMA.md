# Erdős #203 — the Quotient Lemma on lines, and the 5–7 cut (Theorem D) — statements, proofs, scope, attribution

Setting (as in the shipped entry /day/203-no-covering-system-with-period-up-to-30000). For a prime p ≥ 5 let
H_p = ⟨2,3⟩ ≤ (ℤ/p)^×, e_p = |H_p|, and L_p = ker(φ_p : ℤ² → H_p, (k,ℓ) ↦ 2^k 3^ℓ), a sublattice of index e_p.
Writing H_p ≅ ℤ/e_p with 2 ↦ u_p, 3 ↦ v_p (gcd(u_p, v_p, e_p) = 1 since φ_p is onto), L_p = {u_p k + v_p ℓ ≡ 0 (mod e_p)}.
A #203 covering system is a finite set P of primes ≥ 5 and one coset C_p of L_p for each p ∈ P with ∪ C_p = ℤ²
(Lemma 1 of the entry: the primes 2 and 3 and the quadrant restriction change nothing; for fixed m the set of (k,ℓ) with
p | 2^k3^ℓm+1 is the preimage of the single element −m^{−1} ∈ H_p, so ONE coset per prime). Every assignment of cosets
arises from some m (CRT), independently over p.

**SCOPE.** Everything below concerns PURE covering systems. The perfect-power free sets of Theorem C (qℤ² for odd primes
q | N₀ and (2,0)+4ℤ²) are a separate mechanism; `linelemma.py --pp 1` credits them as fixed-class lumps (see the entry),
but the exclusions stated here do not cover that variant unless the pp run says so.

## Quotient Lemma (elementary; a standard fact about coset covers — see Attribution)

Let Λ ≤ ℤ² be any subgroup, G = ℤ²/Λ, π : ℤ² → G, and for p ∈ P let S_p = (L_p + Λ)/Λ ≤ G. Then

(i) C_p meets a cell y + Λ either not at all, or in a single coset of L_p ∩ Λ; so the density of C_p inside every cell
    it meets is the same number  w_p(Λ) := 1/[Λ : L_p ∩ Λ] = [G : S_p] / e_p,  and the cells it meets form one coset of
    S_p in G.

(ii) If ∪_{p∈P} C_p = ℤ², then for EVERY cell g ∈ G:   W(g) := Σ_{p : g ∈ π(C_p)} w_p(Λ) ≥ 1.          (★)
    (A covered cell has density 1 inside it covered by the C_p meeting it; the density of their union inside the cell is
    at most the sum of their densities inside it.)

Proof of (i). C_p = x + L_p. If y + Λ meets C_p at z then (y + Λ) ∩ C_p = z + (Λ ∩ L_p), a full coset of Λ ∩ L_p inside
z + Λ = y + Λ, of relative density 1/[Λ : Λ ∩ L_p]. The second isomorphism theorem gives [Λ : Λ ∩ L_p] = [L_p + Λ : L_p],
and e_p = [ℤ² : L_p] = [ℤ² : L_p + Λ]·[L_p + Λ : L_p] = [G : S_p]·[Λ : Λ ∩ L_p]. π(C_p) = π(x) + S_p. ∎

Averaging (★) over G (finite G, or a fundamental domain) gives back Σ 1/e_p ≥ 1 (the density condition).

Define V_Λ(P) := max over coset choices of min over g ∈ G of W(g). Then
  * V_Λ(P) < 1 ⇒ no #203 covering system uses a subset of P (W only grows with P), so for P = pool(N) = {p : e_p | N}
    (the complete pool; every prime usable at period N lies in it) none has period N, nor any divisor of N
    (pool(d) ⊆ pool(N));
  * monotone in Λ: if Λ' ≤ Λ then V_{Λ'} ≤ V_Λ — because W_Λ on a cell of ℤ²/Λ is the AVERAGE of W_{Λ'} over the cells of
    ℤ²/Λ' inside it (each C_p contributes w_p(Λ) on the coarse cell and w_p(Λ') on the fine cells it meets, which are a
    fraction w_p(Λ)/w_p(Λ') of them), and a minimum is at most an average;
  * exact at the bottom: for Λ = ∩_{p∈P} L_p every w_p = 1 and V ≥ 1 iff a covering exists; at the top (Λ = ℤ²) it is the
    density condition.

## Instance 1 — lines.  Λ = ℤd, d = (a,b) primitive, G ≅ ℤ via the transverse coordinate τ = bk − aℓ.
Let g_p = 2^a 3^b ∈ H_p, with discrete logarithm s_p = a u_p + b v_p (mod e_p). Then S_p = i_p ℤ with
    i_p = [H_p : ⟨g_p⟩] = gcd(s_p, e_p),      w_p = i_p / e_p = 1 / ord_p(2^a 3^b).
(Proof: L_p ∩ ℤd = ord_p(g_p)·ℤd, so [Λ : L_p ∩ Λ] = ord_p(g_p) = e_p/gcd(s_p,e_p), and S_p ≤ ℤ has that index.)
In words: C_p meets one residue class of lines modulo i_p, and on each of those lines it is one residue class modulo
ord_p(2^a 3^b). Primes with i_p = 1 ("everywhere" primes: 2^a 3^b generates H_p) contribute the constant E = Σ 1/e_p;
the others are lumps the adversary must place (one class each).

Coarsening. For any M ≥ 1, averaging W over a progression τ ≡ c (mod M) gives the same shape with i_p ↦ gcd(i_p, M),
w_p ↦ gcd(i_p, M)/e_p: it is (★) for the rank-2 lattice Λ' = {x : π(x) ≡ 0 (mod M)} ⊇ ℤd (G ≅ ℤ/M; S_p = gcd(i_p,M)ℤ/M by
the general formula) — necessary as well, and exact when lcm(i_p) | M.

## Instance 2 — coarse tori.  Λ = Tℤ², G = (ℤ/T)².
S_p = {u_p k + v_p ℓ ≡ 0 (mod gcd(T, e_p))} (Tℤ² maps onto gcd(T,e_p)·ℤ/e_p), so i_p = [G : S_p] = gcd(T, e_p) and
w_p = gcd(T,e_p)/e_p; C_p projects onto one of the i_p cosets {u_p k + v_p ℓ ≡ c (mod i_p)}. For T = lcm of the e_p of a
block the block's primes have w_p = 1 (the exact union problem of Theorem B) while every other prime stays at its coarse
intensity; if Theorem B's inequality fails for the block then V_{Tℤ²} < 1. Projecting (ℤ/T)² → ℤ/T (forget k) is the
line instance in direction (1,0) coarsened to M = T, so V_{Tℤ²} ≤ that value (asserted by `torus.py --selftest`).
Recorded for the hierarchy; the solver could not decide the T = 60 instance with all 99 primes of 720720 (UNKNOWN),
although Theorem D below shows it is infeasible.

## Theorem D — the 5–7 cut on the (1,1) lines (elementary; no solver)
Direction d = (1,1): g_p = 6. Since 6 ≡ 1 (mod 5), i_5 = e_5 = 4 and w_5 = 1: the prime 5 covers ENTIRELY the lines
τ ≡ t_5 (mod 4) and nothing else. Since 6 has order 2 mod 7 and e_7 = 6, i_7 = 3 and w_7 = 1/2. Coarsen to M = 60 and
let S be the 30 classes τ (mod 60) with τ ≢ t_5 (mod 4) and τ ≢ t_7 (mod 3) (with t_5 = 0 after a translation, the three
choices of t_7 give three sets S that are translates of one another mod 12, so what follows does not depend on them). On S the primes 5 and 7 contribute nothing,
so   min_τ W(τ) ≤ avg_{τ∈S} W(τ) ≤ B(P) := Σ_{p∈P, p≠5,7} (gcd(i_p,60)/e_p) · max_c |{τ ∈ S : τ ≡ c (mod gcd(i_p,60))}| / 30.
B(P) is a finite sum a reader can recompute from the pool (`fivesevencut.py`, 40 lines). Values: every one of the 26
periods ≤ 65,520 with density ≥ 1 has B ≤ 3965/4752 = 0.8344 (at 55440); 110880: 35303/41580 = 0.8490; 166320: 0.8682;
221760: 10823/12672 = 0.8541; 332640: 0.8835; 720720: 11255/12012 = 0.9370. All < 1. Hence NO covering system uses a
subset of any of these pools — in particular none has period N for any N ≤ 65,520, nor for any divisor of 110880, 166320,
221760, 332640 or 720720. (Recomputed independently by the hostile referee and by us; on the five open pools the referee's exact
M = 60 optimum in direction (1,1) never exceeds B, as it must not.) This is Theorem A's forced overlap of 5 and 7 (e_35 = 24 = e_5 e_7)
seen line by line: along (1,1) the two primes' lumps cannot be made to share lines with the rest of the pool.

## What `linelemma.py` computes beyond Theorem D
V_Λ(P) exactly (a rational with denominator dividing lcm e_p) as a max–min integer program: one-hot coset variables for
the lumpy primes, one linear constraint per cell, objective max z; and a FEASIBILITY model (every cell ≥ 1 as hard
constraints) whose INFEASIBLE answer is a proof. Solvers: OR-tools CP-SAT (an OPTIMAL value is exact; a proven
BestObjectiveBound < 1 is a proof even when the optimum did not close; INFEASIBLE is a proof) and HiGHS (scipy.milp) on
the same formulation. Every witness a solver returns is re-counted on every cell by a loop that uses only the (i_p, w_p)
instance (independent of the solvers, not of the formulas — which the referee verified by direct enumeration, 448 tests).
The reported value of a time-limited solution may sit below its re-count (z is only bounded above by every W), so the
re-count check is rc ≥ V there and rc = V at OPTIMAL. `fix_one` fixes the first lumpy prime's class: translations τ ↦ τ+c
shift every class simultaneously and preserve min W, so this loses nothing. Brute force (`--brute`) ran only on the controls
and the 720 pool — every published row has ∏ i_p above its limit.

## Controls (`controls.log`, `selftest_torus.log`)
Classical covering 0(2) 0(3) 1(4) 3(8) 7(12) 23(24) as full-weight classes ⇒ V = 1 (CP-SAT, brute force, HiGHS agree);
{2,3,4,8} leaves a point bare ⇒ V = 0; shifting E by 1/7 shifts V by exactly 1/7; the 4 cosets of L_5 as four 'primes'
⇒ V = 1 in all 17 directions (1 < i < e, fractional weights exercised), plus the 6 cosets of L_7 ⇒ V = 2; dropping one
L_7 coset in direction (0,1) ⇒ exactly 11/6. Torus: lattice image by enumeration (T = 10, 12), synthetic cover/non-cover,
brute = CP-SAT on 7 primes at T = 12, torus ≤ line projection. The referee's own end-to-end check: a 2-D brute force on
(ℤ/60)² with real primes, sharing no code with these formulas, against CP-SAT — 31 direction instances, 0 mismatches.

## Attribution (novelty, as found by the hostile referee)
The Quotient Lemma is the standard restriction of a coset cover to the cosets of a subgroup (B. H. Neumann 1954;
Tomkinson; Z.-W. Sun, arXiv:math/0501451) — not new as a lemma. On the #203 thread, AnimishSharma (21 Jun 2026) noted that
setting ℓ = 0 makes m a classical Sierpiński number (★ on one line, unweighted), and veljjanoski (15 Sep 2026) used the
shear k' = k + Jℓ and a "strip" family (primes aligned with one direction; not a necessary condition on the full pool).
What is ours: the weighted condition on EVERY line (intensity 1/ord_p(2^a3^b) on one class mod i_p), its max–min and
feasibility forms over the whole pool, Theorem D, and the exclusions.
