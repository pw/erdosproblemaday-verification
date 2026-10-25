# Seat I report: printed §7 (Prop 7.1) and printed §8 (Lemma 8.1, proof of Theorem 1.2)

Paper: OpenAI, "Bounded-Step Walks on Gaussian Primes" (26 Sep 2026). Sources read: `src/build/information.tex`
(printed §7–§8), plus all of main, periodicity, preliminaries, geometry, coverage-transfer and schedule, so I could
check what §7–§8 consume. Printed numbering is used throughout. Scripts and outputs are in `seats/I_work/`.

## 0. Bottom line

I went through §7 and §8 line by line, trying to refute them. I found no fatal error and no gap inside these two
sections. Every inequality checks, including the constants. The five targets in the brief come out as follows:

- (a) The normalisation matches.
- (b) The conditioning variables are the same objects.
- (c) The o(1) in (8.1) is uniform in the number of batches, by a margin of about exp(−7·X_M).
- (d) The quantifiers are in the right order.
- (e) Neither section needs the walk to be generic.

The divergence arithmetic is correct. Numerically, S(M) = Σ_T 1/log T equals (#windows)·log(1.05)/log B to 8 digits
(§5.1).

**The result is conditional.** §7–§8 are only as good as five statements imported from §6, which belong to other
seats: (6.2), (6.4), (6.5), (6.9) at i = 0, and Prop 6.2 at i = 0. §1 lists the exact form and quantifiers §7
needs from each. If any of them fails, the failure is in §6, not here.

## 1. What §7–§8 import from §6

| Imported | Exact form used in §7–§8 | Where used |
|---|---|---|
| (6.4) | At the checkpoint A_0(T), under the schedule law from time 0: f_{z_{A_0}}(q_T) ≥ (1−e_0) q_T L_*, and q_T L_* ≥ c_0 T. Here f is the average over uniform signed q_T-subsets of B_T, the same law as C_T. | (7.2) |
| (6.5) | Σ_{T'<T} k_{T'} log(2T') ≤ e_0 c_0 T for every used batch T, with the sum over used batches (all with log T' ≥ X_{⌈M/2⌉}). | (7.2), via H(O) |
| (6.9), i = 0 | H(z_{t_*} − z_{A_0}) ≤ C_D T^{1/4}. This is unconditional, from time 0; t_* counts as a checkpoint ("or the terminal stage"). | (7.3), (7.9) |
| Prop 6.2, i = 0 | For every exact start a at A_0(T), at most a fraction η_0 = 1/100 of the 2k_T signed primes fail (τ_0, β_0) = (1/4, 1/200) coverage of the terminal law b_{0,a,π}. This must hold for every batch at once, with an M-threshold uniform over walks. | (7.6), favorable coordinates |
| (6.2) | TV(L(t_*), L(t_*+a)) ≤ T_+^{−9} for 0 ≤ a ≤ T_+, both from an exact start at A_0(T) and from time 0. | §7 hit floor; §8 block comparison |

These are consistent with zero avoidance and smuggle in no contradiction. For a walk in A(P_M), residue 0 is an
exceptional residue of b_{0,a,π} at every start, which coverage's "fewer than p^{1−β}" allowance permits. In (7.7)
this shows up as the true residue always lying in the u_x < 1/4 class.

## 2. Printed §7, Proposition 7.1: step-by-step audit

The objects match: X'_T = F_{C_T}(z_{t_*}) and O'_T = (F_{C_{T'}}(z_{t_*}))_{T'<T}. C is independent of the
schedule, and entropies are taken at fixed C, as stated in §7, paragraph 2.

**(7.2).** E_C H(X) = f_{z_{A_0}}(q_T), because C_T is a uniform q_T-subset with fair signs. That is exactly the law
in f's definition (printed §4.3), and it is independent of A_0. H(O) is at most the log of O's alphabet, which is
Σ_{T'<T} Σ_{π∈C_{T'}} log p ≤ e_0 c_0 T ≤ e_0 q L_*. Holds.

**(7.3).** A_0 sits at scale V ≤ T^{1/4}. Lemma 6.1 gives log(1+S_0) ≤ 2g_1 V, so H(s) ≤ log|D_0| ≤ 4g_1 T^{1/4}
+ O_D(1). The offset length N = T_+^{10} is inside S_0, but log N = 10.5·100^M ≪ g_1 V ≥ exp(0.23·100^{M/2} − M^3).
Holds.

**(7.4).** Every package's positions z_{t_*+l}, l < L, lie on the walk, so they are nonzero mod every selected π. The
true residue therefore passes every package, and supp(X | O, P) is contained in Π_π L_π(P). Holds; no independence is
used.

**(7.5), posterior kernel.** This needs the schedule to be Markov in walk time. It is: the operation sequence is
deterministic, and each transition uses n = ⌊e^{gU}⌋ and fresh randomness that depend only on the current time.
(O, X) are functions of A_0 for fixed C. Holds.

**(7.6).**

> E_C E_{O,X} #unfavorable ≤ 2 E_C E_{O,X} Σ_π E[χ(A_0,π) | O,X,C] = 2 E_{A_0} E_C Σ_π χ(A_0,π) ≤ 2η_0 q

- The first step is Markov's inequality on the posterior.
- The equality is the tower property, using independence of the prior law of A_0 from C. It holds for every fixed
  C_{<T} as well.
- The last step uses P[(p,σ) ∈ C_T] = q/(2k): the bad count is at most η_0·2k, times q/(2k), giving η_0 q.

Holds.

**u_x averaging.** Σ_x (μ(G) − u_x) = ∫_G #{x : Pr < τ_0/p} dμ < p^{1−β_0} μ(G) ≤ p^{1−β_0}. If u_x < 1/4 the summand
exceeds 1/4, because μ(G) ≥ 1/2. Holds.

**Disjoint chances.**
- Smoothing applies to the time function g(t) = 1[z_t − z_a ≡ −x]: event l is {g(t_*+l) = 1}, so the TV bound (6.2)
  transfers the floor to every l < L ≤ T_+.
- T_+^{−9} ≤ τ_0/(2p) is trivial.
- Self-avoidance plus D·L ≤ D·T^{2/5} < √T ≤ √p (since T ≥ exp(100^{M/2}) ≫ D^{10}) makes the L hit events
  pairwise disjoint within one package.
- Mixing over the posterior gives a hit floor u_x·τ_0/(2p) ≥ τ_0/(8p).
- So a package rejects x with probability at least L·τ_0/(8p).

Holds.

**(7.7).** Packages are i.i.d. given (O, X), so P(x survives) ≤ exp(−c L m_T/p) with c = 1/32, and
L m_T/p ≥ (K_0/2) log T. The step p·exp(−c L m_T/p) ≤ p^{1−β_0} needs only K_0/64 > β_0 + log2/log T. **Any
K_0 ≥ 1 works** (EXPOSITION E1), so K_0 is absolute. Holds.

**H(X | O, P) bound and (7.8).**
- The bound needs 2η_0β_0 log(2T) + log 5 ≤ (β_0/2) L_*, i.e. 10^{−4} log(2T) + 1.61 ≤ 0.0025 log T, true once
  log T ≥ about 671.
- (7.2) minus that bound leaves (β_0/2 − 2e_0) = 0.0023 ≥ β_0/3 = 0.00167.

Holds.

**Transport and (7.9).**
- Conditional i.i.d. gives I(X;P|O) ≤ Σ_a I(X;P_a|O) = m_T I(X; s, W | O).
- Then I(X; s, W | O) = I(X; s | O) + I(X; W | O, s), and I(X; s | O) ≤ H(s).
- Given s, (O, X) ↔ (O', X') is a bijection, and σ(O, s) = σ(O', s). So I(X; W | O, s) = I(X'; W | O', s).
- The identity I(A;B|C,S) − I(A;B|C) = I(A;S|B,C) − I(A;S|C) ≤ H(S) is correct.

All verified, including on random finite laws (§5.3). There is a negative control: if conditional independence of
the packages is dropped (P_2 = P_1 ⊕ X), the transport inequality fails, 0.693 > 0. So the i.i.d.-given-(O, X)
construction is load-bearing, and it is provided.

**Final constant.**

> E_C I(X'; W | O') ≥ β_0 c_0 L/(6K_0 log T) − 2C_D T^{1/4}

T^{1/4} = o(T^{2/5}/log T), with a threshold depending on D only through c_0 and C_D. So
c_1 = β_0 c_0/(12K_0) (= c_0/2400 with K_0 = 1).

c_1 depends on D only through c_0 = c_0(a_0, g_0, l_0):
- a_0 < 1/2 is absolute.
- l_0 = 15 is absolute (from 2^{−l_0} < e_0/3).
- g_0 depends on D through the O_D(g) in Lemma 4.3.

**c_1 does not depend on B or M.** This matters: B is chosen after c_0, so c_1 depending on B would be circular, and
it does not.

## 3. Printed §8: Lemma 8.1 and the proof of Theorem 1.2

**Telescope.**
- Q_{j−1}(t_*) is exactly O'_{T_j}, since "smaller batches" means T_1, …, T_{j−1} across all windows.
- The charge a_j − b_j = I(X'_{T_j}; W_{L_j}(t_*) | O'_{T_j})/L_j is exactly the quantity in (7.1).
- L_T = 2^{⌊log_2 T^{2/5}⌋} is non-decreasing in T, so L_j divides L_{j+1}.
- Chain rule: Q_j(t_*+a) is a function of Q_j(t_*) and the preceding a increments. So
  H(block_a | Q_j(t_*), earlier blocks) ≤ H(W_{L_j}(t_*+a) | Q_j(t_*+a)).
- Smoothing applies with a < L_{j+1} ≤ T_+^{2/5}.
- Lemma 3.2 applies with ε = T_+^{−9} ≤ 1/2 and log(alphabet) ≤ L_j log K_D + Σ_T k_T log(2T) = O_D(T_+), giving
  2h(ε) + 2ε·O(T_+) = O(T_+^{−8}). Lemma 3.2's proof (a coupling, then |ΔH| ≤ h(ε) + ε log a, applied jointly and to
  the marginal with h increasing on [0, 1/2]) is correct.
- The telescoping identity Σ_{j=1}^{n}(a_j − b_j) = a_1 − b_n + Σ_{j<n}(a_{j+1} − b_j) is correct; a_1 ≤ log K_D and
  b_n ≥ 0.

Holds. Lemma 8.1 uses neither self-avoidance nor zero avoidance; it holds for every walk and every base time law with
a uniform offset.

**(c), uniformity of o(1).** The error is at most (n_B − 1)·O_D(T_+^{−7}), with n_B ≈ 0.05·X_M/log B·(1 + 1/100 + …)
= O(log T_+). For M = 10 and log B = 233, log_10(n_B·T_+^{−7}) ≈ −3.2·10^{20}. The error is explicit, uniform in C
and the walk, and n_B's growth is irrelevant.

**Final assembly.**
- Averaging (8.1) over C (Lemma 8.1 holds for each fixed C) and inserting (7.1) gives (8.2):
  c_1 Σ_T 1/log T ≤ log K_D + o(1).
- Window m contributes Σ_{j: X_m ≤ j log B ≤ 1.05X_m} 1/(j log B) → log(1.05)/log B.
- The paper's bound "at least cX_m/log B batches, contribution ≥ c/(1.05 log B)" holds once 0.05·X_{⌈M/2⌉} ≥ 2 log B,
  which is automatic since B is fixed before M.
- Windows are disjoint because 1.05X_m < X_{m+1}. There are ⌊M/2⌋ + 1 of them, so S(M) → ∞ linearly in M.

**(d), quantifier order.** Fix D, then β_0, e_0, l_0, g_0, a_0, c_0, K_0, c_1, then B, then M. Every
"sufficiently large M" used in §7–§8 depends only on D (through C_D, c_0, B, K_D) or is absolute, never on the walk.

The logical form is: ∃M_0(D) ∀M ≥ M_0 ∀ infinite self-avoiding D-walks w ⊂ A(P_M), c_1 S(M) ≤ log K_D + η(M), with
η(M) → 0 independent of w. Pick M with c_1 S(M) > log K_D + η(M). P_D := P_M is the union of the full batches B_T,
with both factors imposed. It is independent of C and of any walk. The assumption "walk lies in A(P_M)" is the
whole walk from time 0, which is exactly the negation of Theorem 1.2's conclusion for that P_M.

(The sets P_M are not nested in M, because the window range ⌈M/2⌉..M slides. That is harmless: one M is chosen.)

**(e), genericity.** §7–§8 never assume genericity. All randomness is in sampled times on the fixed walk, plus C.
The only walk properties used are:
- self-avoidance, for disjoint hits;
- zero avoidance, for the true residue always passing;
- the step bound, for D·L < √p and the K_D-letter alphabet.

Uniformity over adversarial walks is entirely inherited from the §6 imports in §1.

## 4. Objections (classified)

- **E1 (EXPOSITION), (7.7).** The text says *"Choose the fixed K_0 large enough for the second inequality."* Any
  K_0 ≥ 1 suffices: the condition is K_0 > 64β_0 + o(1) ≈ 0.32. So c_1 = β_0 c_0/12 can be stated explicitly in terms
  of c_0.
- **E2 (EXPOSITION), proof of Thm 1.2.** The text says *"contains at least cX_m/log B of the numbers log T = j log B,
  for an absolute c > 0 and all sufficiently large M."*
  - This needs X_{⌈M/2⌉} ≥ 40 log B, which is legitimate because B precedes M.
  - The exact per-window limit is log(1.05)/log B ≈ 0.0488/log B, against the paper's c/(1.05 log B) ≈ 0.0476/log B.
  - Smaller windows exceed the limit because of floor effects.
- **E3 (EXPOSITION), constants.** §7's opening says the constant "depends only on D"; Prop 7.1 says "depending only on
  the fixed schedule parameters". These agree, because those parameters depend only on D. It would help to state
  that c_1 is independent of B. It is, and the order B-after-c_0 requires it.
- **E4 (EXPOSITION), lemma usage.** Lemma 3.3 (short lists) is not used in §7. §7 uses the cruder support bound
  (7.4), which is correct. Lemma 3.2 is used only in §8. Lemma 6.1 is used for (6.2) in both §7 and §8, and through
  (6.8)/(6.9) for H(s).
- **E5 (EXPOSITION), (8.1).** The o(1) could be stated explicitly as (n_B − 1)·O_D(T_+^{−7}). Leaving it as "o(1)"
  hides how large the margin is.
- **N1 (note, not an objection), citation.** The Tao entropy-decrement reference [12, §3, eq. (40), Lemma 17] is cited
  only as methodological context. Nothing in §8 depends on it, and §8 is self-contained. I did not check the cited
  equation and lemma numbers.

No GAP-level or FATAL objection in §7–§8.

## 5. Numerical checks (all in `seats/I_work/`, run under `ulimit -v 4e6; timeout 900`)

### 5.1 Divergence arithmetic (`divergence.py`, mpmath at 120 digits)

Setup: T = B^j, X_m = 100^m, window condition X_m ≤ j log B ≤ 1.05X_m, window sums computed exactly via digamma.

| B | per-window contribution, m ≥ 4 | S(10) | S(20) | S(40) | S(80) |
|---|---|---|---|---|---|
| 3 | 0.0444107 = log1.05/logB | 0.26646 | 0.48852 | 0.93263 | 1.82084 |
| e^10 | 0.0048790 | 0.029274 | 0.053669 | 0.10246 | 0.20004 |
| e^50 | 0.00097580 | 0.0058548 | 0.010734 | 0.020492 | 0.040008 |
| 10^30 | 0.00070631 | 0.0042379 | 0.0077694 | 0.014833 | 0.028959 |
| e^233 (~10^101) | 0.00020940 | 0.0012564 | 0.0023034 | 0.0043974 | 0.0085854 |

S(M) = (⌊M/2⌋ + 1)·log(1.05)/log B to 8 digits. It is linear in M and unbounded. Windows are pairwise disjoint;
the first non-empty window is m = 1 or 2.

Scale illustration only (the constants are nonexplicit):
- With g_0 = 10^{−3}, l_0 = 15 and a_0 = 1/4: c_0 ≈ 6·10^{−98}, c_1 ≈ 2.6·10^{−101}, log B ≈ 234.
- The required M is then about 6·10^{104}. It is finite and depends only on D.
- P_D's largest prime is near exp(1.05·100^M). Finite, but not computable in any practical sense.

### 5.2 Lemma 8.1 on a toy walk, with a negative control (`telescope_toy.py`)

Setup:
- Walk: a self-avoiding walk with steps in {+1, +i, −i} and no immediate vertical reversal (D = 1, K_D = 5). N = 20000.
- Time law: uniform time on [0, N), standing in for t_*; TV of a shift by a is a/N.
- Residues: one random-signed factor per prime.
- Lengths: L = 1, 2, 4, 8 (and 1, 2, 4, 4, 8).

Results:

| Regime | Nested sum Σ(a_j − b_j) | Bound log 5 + Σε | Every step a_{j+1} ≤ b_j + ε_j | Un-nested Σ_j I(X_j; W_{L_j})/L_j |
|---|---|---|---|---|
| A, p ≈ 400–3200 | 1.0549 | 1.6306 | holds | 3.786 > log 5 |
| B, p ≈ 10^{12} (one residue pins the time) | 1.0778 | 1.6306 | holds | 3.861 > log 5 |
| C, intermediate | 0.8106 | 1.6366 | holds; strictly in two steps (−0.107, −0.160) | 0.865 ≤ log 5 |

The negative control fires in A and B: dropping the nesting breaks the bound. So conditioning on O'_T = Q_{j−1}(t_*)
is load-bearing, and §7 proves its bound for that same conditioning (target b).

### 5.3 Information identities (`identities.py`)

On 300 random conditionally-i.i.d. laws:
- max[I(X;P|O) − Σ_a I(X;P_a|O)] = −7·10^{−4}, i.e. ≤ 0 as required.
- Negative control (P_2 = P_1 ⊕ X): 0.693 > 0, so the inequality fails as it should without conditional independence.
- The identity before (7.9) holds to 1·10^{−15}.
- (7.9) holds on random laws mod 5.

## 6. Cross-reference to the Lean (read, not compiled; the coordinator is running the kernel replay)

`InformationTelescope.lean: common_law_information_telescope` is Lemma 8.1 almost verbatim:
- nested factor sets F j ⊆ F (j+1);
- L j ∣ L (j+1);
- an arbitrary base law joined with a uniform offset Fin (N+1);
- a continuity error that is a slightly sharper form, 2h(ε) + ε(L_j log K_D + 2R), than Lemma 3.2's
  2h(ε) + 2ε log a.

`BatchCertificate`'s fields (`short`: (DL)^2 < p; `smooth_error`; `list`: log(4u_i + p·e^{−nLτ/(8p)}) ≤ log p − A;
`rate`: n(L r + 2·H(s)-bound) ≤ b(A(1−2η) − δ·meanLog) − E) correspond line for line to §7's (7.2)–(7.9).

The Lean reparametrises the batches. It uses dyadic batches [2^j, 2^{j+1}], spaced K apart, in windows
100^w·e^m, w < W, with W fixed before m. It also picks one good selection per batch existentially instead of
averaging over C. Neither change affects the paper's argument, but the Lean does not literally use the printed §6.1
parameters (B, X_m = 100^m, ⌈M/2⌉..M).

Scope of the verdict: printed §7–§8, given (6.2), (6.4), (6.5), (6.9) and Prop 6.2 at i = 0 as listed in §1.

VERDICT: HOLDS AS READ
