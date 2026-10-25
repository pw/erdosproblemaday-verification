# Referee report — seat "scores" (Section 5, PDF pp. 22–28, + brief item (v) first half)

Paper: OpenAI, "A power saving for planar unit distances", 23 Sep 2026, local copy
/tmp/oaimath/167/paper/paper.pdf. Every formula below was read off the rendered PDF pages 22–28
(and pp. 11–15, 16–22, 31–33 for the inputs and the downstream use), not off the mangled .txt.

## VERDICT FOR MY SCOPE: HOLDS AS READ

Section 5 (Lemma 5.1, the classes C/B/G and (5.3), the dominant-label paragraph, Lemma 5.2,
the history (5.7), templates (5.8)–(5.9), §5.2 and (5.10), Lemma 5.3, the score definition,
Lemma 5.4, Figure 1, Proposition 5.5, Proposition 5.6) was checked line by line. I found no
mathematical gap. Every inequality I re-derived has the direction and constant the paper states,
and the numerical checks (below) pass, while each of their deliberately broken controls fails.
The objections are exposition only: one ambiguity in the score display that matters, because the
other reading makes Prop 5.5 false, plus three cosmetic points.

This verdict is CONDITIONAL on the out-of-scope inputs that §5 consumes as black boxes:
Prop 2.4 ((2.3), (2.4)), Lemma 2.5, Lemma 2.6, Lemma 2.7 (D = o(log t)), Cor 3.3 / (3.17),
Lemma 4.1 (weighted product formula), Prop 4.4 (S → ∞), Lemma 4.5 (∫m = O(1) and the
label-match implications). I checked that each is APPLIED within its stated hypotheses. I did not
re-prove any of them; other seats own them.

## OBJECTIONS

**O1. Score display: the scope of "− 1{Y1≠Y2}" is ambiguous, and the wrong reading breaks Prop 5.5.**
Location: §5.2, PDF p. 25, the display defining `score`. Verbatim:
> "score = { 2I_x 1{Y1=Y2=r, N}, at a good rare level, / c(ρ)1{Y1=Y2, N}, at a common level, − 1{Y1≠Y2}. / 0, at a damaged level"

The "− 1{Y1≠Y2}" is typeset on the common-level row. Read literally, it charges bit differences
only at common levels, so damaged levels would score 0. The brief's own summary
("good rare 2I_x1{…}; damaged 0") reads it that way. Every later use needs the charge at
EVERY level:
- p. 26 (Prop 5.5): "All thresholds lie within the chosen level interval, so the integrated bit-difference charge at this place is exactly b′ − b."
- p. 28 (Prop 5.6), at good rare levels: "Hence the negative charge is at most I_{y1} + I_{y2} + M1 + M2."
- p. 28, at damaged levels: "On B there are no positives and the negative score is at least −1, whose total cost is W_b = o(S)."

Under the literal reading, the negative charge at place v is only |[b, b′) ∩ C_v| ≤ b′ − b. The
product-formula cancellation Σ*(b′ − b) = 2Σ*α_v then no longer controls the score, and the bound
D_i ≤ o(S) + 10δ²λC_i fails. Its only remaining input would be the positive-charge length 2T_v,
which is not small.
Severity: UNCLEAR, an EXPOSITION gap. The intended reading is forced by the three uses above, and
under it everything checks.
Fix: write "score = [positive part as displayed] − 1{Y1≠Y2}, at every level".

**O2. The symbol c_v means two different things.**
- Lemma 4.5 (p. 22): "c_v = 1 at nonarchimedean entries and c_v = √2 at archimedean entries", a multiplicative constant.
- Prop 5.5 (p. 26): "Let c_v = log 2 at archimedean entries and c_v = 0 otherwise", an additive constant in logarithms.

The derivation in Prop 5.5, "a matching label bounds it by the scale itself. If both bits are 1, a
positive charge requires s < b and a B1 match, which gives s ≥ b′ − α − c_v", is correct only with
the Prop 5.5 meaning: a B1 match gives s ≥ b′ − α − (1/2)log 2 ≥ b′ − α − log 2. With Lemma 4.5's
c_v = √2 subtracted from a logarithm it would be a different, though still valid, inequality.
Severity: COSMETIC.
Fix: rename one of the two (for example c′_v = log 2 in Prop 5.5).

**O3. Cross-references call lemmas and propositions "Theorem".**
§5 cites "Theorem 2.5", "Theorem 2.6", "Theorem 3.3", "Theorem 4.4", "Theorem 4.5", "Theorem 5.1",
"Theorem 5.3" and "Theorem 5.4" for Lemma 2.5, Lemma 2.6, Cor 3.3, Prop 4.4, Lemma 4.5, Lemma 5.1,
Lemma 5.3 and Lemma 5.4. I checked every occurrence in pp. 22–28: each points at the intended result.
Severity: COSMETIC.

**O4. The template sampling law is not written down.**
p. 24 verbatim: "a template is an ordered list θ = (h1, . . . , hk) obtained by sampling k independent neighbors of q and recording their histories."
The law of "a neighbor" is not stated; the natural reading is the conditional edge law ω(·|q),
uniform on neighbours by (2.11). Everything in §5 holds for ANY law of the k neighbours that
depends only on q: (5.9)'s conditional independence, Lemma 5.3, and M ≤ L^{2Kk}. §6 (ν̃_q = E_{p|q}ν_{H(p)},
Lemma 6.1 sampling) needs exactly ω(·|q). Flag for the §6 seat.
Severity: COSMETIC.

No FATAL objection and no GAP in scope.

## STATUS PER RESULT (the deliverable)

| Item | Status |
|---|---|
| Lemma 5.1 (parameters) and all stated consequences | VERIFIED LINE BY LINE |
| Classes C, B, G; (5.3); "C is an interval at each place" | VERIFIED LINE BY LINE |
| Minority bit uniqueness; dominant coordinate and label; I_x, h_P, h_Q, H_x* | VERIFIED LINE BY LINE |
| Lemma 5.2 ((5.4) both inequalities, (5.5), (5.6)) | VERIFIED LINE BY LINE |
| History (5.7) via (3.17) | VERIFIED (arithmetic redone; (3.17) itself taken as given) |
| Templates, (5.8), (5.9), conditional independence | VERIFIED LINE BY LINE |
| §5.2 three experiments, ρ, (5.10) | VERIFIED LINE BY LINE |
| Lemma 5.3 (marginals; M/d(p)) | VERIFIED LINE BY LINE |
| Score definition (N, c(ρ), δ, λ, three level cases) | VERIFIED (with O1) |
| Lemma 5.4 ((5.11) incl. b = b′; (5.12)) | VERIFIED LINE BY LINE + numerics |
| Figure 1 | VERIFIED (consistent with the proof of Lemma 5.4) |
| Proposition 5.5 | VERIFIED LINE BY LINE + numerics (toy in Q(i), abstract archimedean place, abstract per-place budget) |
| Proposition 5.6 | VERIFIED LINE BY LINE |

## LINE-BY-LINE NOTES

**Lemma 5.1.**
- Take K = ⌈√((D+1)log t)⌉ and log L ∼ √(log t/K). Then K log L ≍ (D+1)^{1/4}(log t)^{3/4} = o(log t), because D = o(log t) (Lemma 2.7).
- D/K ≤ √(D/log t) → 0.
- L → ∞ because K = o(log t).
- (D/K)^{1/4}, 1/L, 1/S and 1/d_{Q,min} all tend to 0. S → ∞ is Prop 4.4. For d_{Q,min}: (2.4) gives d(q) = |E|κ(q) ≥ γ|E|/|Q| = γ t^{a+o(a)}, and a log t → ∞.
- An integer k → ∞ with kK log L = o(log t) and k^{20}(…) → 0 exists. Choose it as in §3.4: k = min(⌊(log t/(K log L))^{1/2}⌋, ⌊(…)^{−1/40}⌋).

Consequences:
- k³/S ≤ k^{20}/S → 0.
- k^{3+1/16}e_t ≤ k^{20}e_t → 0.
- K log L → ∞, so k = o(log t), hence k = t^{o(1)}.

There is no circularity. k depends only on D, K, L, S and d_{Q,min}. Then ε = k^{−1/16}, then C, then H.

**Classes and (5.3).**
- W_c = ∫1_C ≤ ∫f/ε = S/ε.
- W_b ≤ k∫m (Markov on each level) = O(k) = o(S), because k³/S → 0.
- π(v,·) is nonincreasing. So {π ≥ ε} ∩ {π ≤ 1−ε} is an interval (ε ≤ 1/2).

**Minority bit and dominant label.**
- On G we have f < ε, and ε ≤ 1/2 once k ≥ 2^{16}. Then f ≠ 1/2, so the minority bit is unique, uniformly over G, for all large t.
- Majority bit 1−r. Consistency says: bit 0 ⇒ exactly B1 agrees; bit 1 ⇒ exactly A agrees. So the shared coordinate is B1 when r = 1 and A when r = 0, as stated.
- Its mismatch probability is ≤ P(Y = r) + P(inconsistent) ≤ f + m ≤ ε + 1/k, which is eventually ≤ s_0 uniformly on G.
- Lemma 2.5 applies. The labels form a common alphabet for P and Q (nonarchimedean classes named by their first vertex of P∪Q; integer cell indices at infinity), only finitely many are attained, and Lemma 2.5 holds "uniformly for every pair of label maps".

**Lemma 5.2.**
- (5.4), first inequality: this is Lemma 2.5.
- (5.4), second inequality, case r = 1 (dominant coordinate B1). If both ends carry ℓ, then B1 agrees. A consistent bit-1 edge needs B1 to disagree, so a consistent edge has bit 0, the majority. Hence every minority edge has an exceptional end or is inconsistent: f ≤ h_P + h_Q + m. The case r = 0 is identical with A.
- (5.5): ∫_G C(f+m) ≤ C(S + O(1)) = O(S).
- (5.6), edge term: use Lemma 2.6(ii) with δ_t = C(ε + 1/k), applied to F = {I_p = 1} and G = {I_q = 1}, whose marginals are ≤ δ_t on G.
- (5.6), wedge term: use Lemma 2.6(iii).
- The o(1) factors are uniform over these sets, so they come out of ∫_G, and then (5.5) applies. Correct.

**(5.7).** By (3.17) with T = C, W = W_c and m(τ) = m (consistency ⇒ strict cross):
∫_C E_E[1 − ν_{H(p)}(R_{y_q})] ≤ ∫_C m + W_c(4/L + 18(D/K)^{1/4}) ≤ O(1) + 18W_c e_t.
Multiply by k³ and use W_c ≤ k^{1/16}S:
O(k³) + 18 k^{3+1/16} e_t S = o(S),
by k³/S → 0 and k^{3+1/16}e_t → 0. Also |H(P)| ≤ (L²)^{K−1} ≤ L^{2K}. Correct.

**Templates.**
- M ≤ |H(P)|^k ≤ L^{2Kk}, and log M ≤ 2kK log L = o(log t).
- (5.9): θ is built from k fresh neighbours of q, so p ⫫ θ | q by construction.

**§5.2 and Lemma 5.3.**
- In all three experiments the two opposite endpoints are iid given the base, BY CONSTRUCTION. In Pθ the base is (p, θ). Given p alone, q and q′ are coupled through θ, but ρ, c(ρ), J_v and the use of (5.12) all condition on the full base (p, θ). The paper says so explicitly ("The base in the third experiment includes θ"), so the use is consistent.
- Slot marginals. In Pθ, (p,θ) ∼ Σ_q ω(p,q,θ) and q ∼ ω(q|p,θ), so (p,q,θ) ∼ ω. Then Σ_θ a(q,θ) = 1 gives the uniform edge law. Q and P are immediate.
- Collision bound. ω(q|p,θ) = 1{(p,q)∈E} a(q,θ)/(d(p)a_p(θ)), using µ(p) = d(p)/|E|. This is ≤ 1/(d(p)a_p(θ)). The collision probability is ≤ the max atom. Multiply by a_p(θ) and sum over ≤ M templates: ≤ M/d(p), pointwise in p.

**Lemma 5.4.**
- The left side of (5.11) is [2λ(a−T)]_+. Each intersection is ≤ T, so positivity needs both intersections of positive length. Then inf J < b ≤ b′ < sup J, so both thresholds are in int J, including when b = b′.
- a ≤ 2T and a ≤ |J|, so 2(a−T) ≤ a ≤ |J|.
- (5.12): for u < v in int J, P(u < X ≤ v) = P(X > u) − P(X > v) ≤ 2δ. Then exhaust int J (continuity from below).
- Correct. Note: the EQUAL flank length T is load-bearing (control B below fails without it). Prop 5.5 supplies equal flanks by enlarging both supports to length T_v.

**Prop 5.5.**
1. Distinct real endpoints give d ≠ d′. In Q, d − d′ = z_p − z_r. In P, d − d′ = z_{q′} − z_q. The w-difference is ±(1/d − 1/d′).
2. (5.14). Since 1/d − 1/d′ = (d′−d)/(dd′), we get −log|1/d − 1/d′|_v = u − n_e − n_e′ = u − b − b′. Adding u gives 2u − b − b′ = 2α − (b′−b). Checked exactly in Q(i) below.
3. The negative charge is 1{Y1≠Y2} = 1{s ∈ [b, b′)}. Both n_e(v) and n_e′(v) lie in I_v, so the integral is exactly b′ − b (needs O1's reading).
4. α = log max(|d|_v,|d′|_v) − log|d−d′|_v ≥ −log 2 (archimedean) or ≥ 0 (nonarchimedean). So T_v ≥ 0.
5. Both bits 1. B1 match ⇒ |1/d−1/d′|_v ≤ c·e^s with c ∈ {1, √2}, so s ≥ b+b′−u−log c = b′ − α − log c ≥ b′ − α − c_v ≥ b − T_v. Also s < b.
6. Both bits 0. A match ⇒ |d−d′|_v ≤ c·e^{−s}, so s ≤ u + log c ≤ b + α + c_v = b + T_v ≤ b′ + T_v. Also s ≥ b′. So (5.15) holds.
7. Rare positive with minority bit 1 at s₀:
   - s₀ < b, and π(v,s₀) = f(v,s₀) < ε.
   - Common levels have π ≥ ε > π(s₀). Minority-0 levels have π > 1/2 > π(s₀). Since π is nonincreasing, both kinds of level lie strictly below s₀ < b ≤ b′.
   - A positive in I_+ needs both bits 0, i.e. s ≥ b′. So no common positive and no minority-0 positive can sit in I_+.
   - A minority-1 rare positive needs both bits 1, so it sits in I_−. Damaged levels carry no positive.
   - Hence all positives lie in I_−, with coefficient ≤ max(2, 1+λ) = 2, total ≤ 2T_v.
8. Minority bit 0 (the symmetric case):
   - s₀ ≥ b′ and π(s₀) > 1−ε. Every common level and every minority-1 level has π smaller than π(s₀), so lies strictly above s₀ ≥ b′ ≥ b.
   - A positive in I_− needs s < b, so none sits there. All positives are in I_+.
   - Two rare positives with opposite minority bits cannot coexist.
   - A COMMON positive cannot coexist on the other flank. Checked.
9. No rare positive. Positive ≤ ∫_{I_−∪I_+}[(1−λ) + 2λ1_{J_v}] = (1−λ)2T_v + 2λa. J_v is an interval because C_v is one and ρ(v,·) is monotone. Lemma 5.4 (with T = T_v ≥ 0) then gives an excess over 2T_v of ≤ λ|J_v|1{b,b′ ∈ int J_v}.
10. Sum over places. Σ*[2T_v − (b′−b)] = Σ*[2α_v + 2c_v − (b′−b)] = 2Σ*c_v = 2 log 2, because Σ*(2α − (b′−b)) = Σ*(−log|(d−d′)(1/d−1/d′)|_v) = 0. Places of zero width have I_v = [0,0] ∋ all n_e(v), so b = b′ = 0 and score 0 ≤ 2T_v. The remark is correct.
11. Averaging. Restrict to distinct pairs, then drop the restriction in the nonnegative excess term. Given the base the endpoints are iid, so P(both in int J_v | base) = P(X ∈ int J_v)² ≤ 4δ² by (5.12), since |ρ(v,s) − 1/2| ≤ δ on J_v by definition.
    - On J_v, 2ρ(1−ρ) ≥ 2(1/4 − δ²), so E_base Σ*|J_v| ≤ C_i/(2(1/4−δ²)).
    - The constant is 4/(2(1/4−δ²)) = 8.0032 ≤ 10 (exact check below).
12. Equal endpoints. There is no negative charge. The positive part is ≤ (1+λ)W_c + 2H_x* ≤ 2(W_c + H_x*).
    - Collision probabilities: 1/d(q) (Q), 1/d(p) (P), and M/d(p) pointwise in p (Pθ, Lemma 5.3).
    - The bounds (2/d_{Q,min})(W_c + E_κH_q*), (2/d_{P,min})(W_c + E_µH_p*) and (2M/d_{P,min})(W_c + E_µH_p*) are o(S). This uses W_c ≤ k^{1/16}S together with k^{20}/d_{Q,min} → 0 (this is exactly why d_{Q,min} sits in (5.2)), E H* = O(S), M = t^{o(1)} and d_{P,min} = t^{1+o(a)}.
    - "Multiplication by an unbounded H_p* requires only its first moment" is right, because the collision bound is pointwise in p.

**Prop 5.6.**
- Pointwise positive bound. If I_x = 1, the y_j are normal and the edges are consistent, then the dominant labels of y1 and y2 are ℓ ≠ the base's. Consistency then forces each bit to be r: for r = 1 the B1 labels differ, so bit 1; for r = 0 the A labels differ, so bit 0. N holds because the y_j share ℓ in exactly the coordinate N tests (B1 for bits 1, A for bits 0). So 2I_x1{Y1=Y2=r, N} ≥ 2I_x(1 − I_{y1} − I_{y2} − M_1 − M_2) ≥ 2I_x − 2I_xI_{y1} − 2I_xI_{y2} − 2M_1 − 2M_2, using I_xM_j ≤ M_j.
- Negative bound. If both y_j are normal and both edges are consistent, the bits agree whether or not the base is exceptional. So 1{Y1≠Y2} ≤ I_{y1} + I_{y2} + M_1 + M_2.
- Slot marginals are uniform on E (Lemma 5.3), so E∫_G I_xI_{y_j} = ∫_G P_E(I_p = I_q = 1) = o(S) by (5.6), and E∫_G M_j ≤ ∫m = O(1).
- Damaged levels: score ≥ −1, total ≥ −W_b = −o(S).
- Result: 2EH_x* − 2EH_y* − o(S). Correct for all three experiments; the y-marginal is µ in Q and κ in P and Pθ.

**Hedge words in scope.**
Five instances, each checked: "follow directly" (L5.1), "immediate for ordinary stars" (L5.3),
"empty-interior case is immediate" (L5.4), "the analogous A match" (P5.5), and "The case of a
rare positive with minority bit 0 is symmetric" (P5.5). Each is genuinely routine and true as
written.

**Euclidean input inside §5 (brief item (i)).**
§5 uses the hyperbola zw = 1 at exactly two points:
- (a) through Lemma 4.5's consistency: exactly one coordinate is shared and the bit says which. This defines the dominant coordinate and the event N.
- (b) in (5.14): the second coordinate difference of two opposite endpoints is 1/d − 1/d′ = −(d−d′)/(dd′), so its valuation is determined by b, b′ and u.

For a metric whose w-jump is a different algebraic function g(d), the valuation of
g(d) − g(d′) is not determined by (b, b′, u). The product-formula identity Σ*(b′−b) = 2Σ*α,
which pays for every bit difference, then has no analogue. Lemmas 5.1–5.4 and Prop 5.6 are
metric-agnostic.

## FINITE CHECKS

All scripts are mine, in /tmp/oaimath/167/checks/. Nothing from the downloaded paper was executed.
Each check has at least one deliberately broken control, and every one of those controls FAILS.

### (a) Lemma 5.4 — (5.11) and (5.12)

The brief suggested "drop the indicator" as the failing control. That control cannot fail: the
indicator is ≤ 1, so dropping it only enlarges the right side. It is reported as such. Three
real failing controls replace it:
- A: halve the right side;
- B: unequal flank lengths, which are not allowed by the lemma and are avoided in Prop 5.5 by enlarging both flanks to T_v;
- C: count atoms at the CLOSED ends of J.

Output:
```
cases 100000 positive-excess cases 6664 of which b==b' 5621
paper (5.11) violations: 0
control: dropping the indicator (RHS grows) violations: 0 (expected 0: not a failing control)
control A: RHS halved violations: 2050 (expected >0)
control B: unequal flank lengths Tm!=Tp violations: 5442 (expected >0)
(5.12) checked 49589 violations (open interior): 0
control C: same with CLOSED J (endpoint atoms counted) violations: 49589 (expected >0)
```
Script `scores_lemma54.py`:
```python
# Check Lemma 5.4 (5.11) and (5.12) numerically, with failing controls.
import random, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)

def inter(a0,a1,b0,b1):
    return max(0.0, min(a1,b1)-max(a0,b0))

def lhs(b,bp,T,J,lam,Tm=None,Tp=None):
    # [(1-lam)(|I-|+|I+|) + 2 lam a - (|I-|+|I+|)]_+ ; Lemma uses Tm=Tp=T
    Tm = T if Tm is None else Tm; Tp = T if Tp is None else Tp
    j0,j1 = J
    a = inter(j0,j1,b-Tm,b) + inter(j0,j1,bp,bp+Tp)
    tot = Tm+Tp
    return max(0.0,(1-lam)*tot + 2*lam*a - tot), a

def rhs(b,bp,J,lam,ind):
    j0,j1 = J
    return lam*(j1-j0)*ind(b,bp,J)

def ind_paper(b,bp,J):   # 1{b,b' in int J}
    j0,j1=J
    return 1.0 if (j0<b<j1 and j0<bp<j1) else 0.0

def ind_one(b,bp,J):     # control: only b' in int J required (weaker indicator)
    j0,j1=J
    return 1.0 if (j0<bp<j1) else 0.0

def rnd():
    return random.choice([random.uniform(-3,3), float(random.randint(-3,3))])

N=100000
viol_paper=0; viol_halfcoef=0; viol_unequalT=0; viol_drop_ind=0; pos_cases=0; eqb_pos=0
for it in range(N):
    b=rnd(); bp=b+random.choice([0.0, abs(rnd())])
    T=abs(rnd())
    j0=rnd(); j1=j0+abs(rnd())
    lam=random.uniform(1e-6,0.999)
    L,a=lhs(b,bp,T,(j0,j1),lam)
    if L>0:
        pos_cases+=1
        if b==bp: eqb_pos+=1
    if L > rhs(b,bp,(j0,j1),lam,ind_paper)+1e-12: viol_paper+=1
    # control 1 (should FAIL): half the coefficient on the right
    if L > 0.5*rhs(b,bp,(j0,j1),lam,ind_paper)+1e-12: viol_halfcoef+=1
    # control 2 (should FAIL): unequal flank lengths with the paper's indicator
    Tm=abs(rnd()); Tp=abs(rnd())
    L2,_=lhs(b,bp,None,(j0,j1),lam,Tm,Tp)
    # natural analogue of the excess over (Tm+Tp):
    if L2 > rhs(b,bp,(j0,j1),lam,ind_paper)+1e-12: viol_unequalT+=1
    # 'drop the indicator' (brief's suggestion) cannot fail: RHS only grows
    if L > lam*(j1-j0)+1e-12: viol_drop_ind+=1
print("cases",N,"positive-excess cases",pos_cases,"of which b==b'",eqb_pos)
print("paper (5.11) violations:",viol_paper)
print("control: dropping the indicator (RHS grows) violations:",viol_drop_ind,"(expected 0: not a failing control)")
print("control A: RHS halved violations:",viol_halfcoef,"(expected >0)")
print("control B: unequal flank lengths Tm!=Tp violations:",viol_unequalT,"(expected >0)")

# (5.12): X arbitrary atomic law, J = maximal set where |P(X>s)-1/2|<=delta (exact, piecewise),
# check P(X in int J) <= 2 delta.  Control C: count atoms at the CLOSED ends of J (should fail).
viol512=0; viol512_closed=0; checked=0
for it in range(100000):
    k=random.randint(1,7)
    atoms=sorted(set(random.choice([round(random.uniform(-2,2),3), float(random.randint(-2,2))]) for _ in range(k)))
    k=len(atoms)
    w=[random.random()**3 for _ in range(k)]; Z=sum(w); w=[x/Z for x in w]
    delta=random.uniform(0.01,0.45)
    # piece m (m=0..k): m=0 is (-inf,a_0) value 1; m>=1 is [a_{m-1},a_m) value sum_{l>=m} w_l
    vals=[sum(w[m:]) for m in range(k+1)]
    good=[m for m in range(k+1) if abs(vals[m]-0.5)<=delta]
    if not good: continue
    assert good==list(range(good[0],good[-1]+1))  # monotone => contiguous
    if good[0]==0 or good[-1]==k: continue  # infinite J impossible for delta<1/2
    j0=atoms[good[0]-1]; j1=atoms[good[-1]] if good[-1]<k else None
    checked+=1
    pint=sum(wi for ai,wi in zip(atoms,w) if j0<ai<j1)
    pcl=sum(wi for ai,wi in zip(atoms,w) if j0<=ai<=j1)
    if pint>2*delta+1e-12: viol512+=1
    if pcl>2*delta+1e-12: viol512_closed+=1
print("(5.12) checked",checked,"violations (open interior):",viol512)
print("control C: same with CLOSED J (endpoint atoms counted) violations:",viol512_closed,"(expected >0)")
```

### (b) Explicit toy in Q(i): (5.14), the product-formula cancellation, and the supports (5.15) with the actual §4.4 states

Setup:
- d_N = 2. Archimedean entries are id and conj, weight 1/2 each.
- Split ℓ ≡ 1 (4): two places, one copy each. Ramified 2: two copies. Inert ℓ ≡ 3 (4): two copies. Every copy has weight 1/2, with |ℓ|_p = 1/ℓ.
- Logarithms are kept SYMBOLICALLY as Q-linear combinations of log ℓ, so (5.14) and Σ* = 0 are checked EXACTLY.
- Jumps: 15 Gaussian rationals of modulus 1 (real unit edges), all 210 ordered distinct pairs, in both orientations (Q: centre base, points q+d, q+d′; P: point base, centres p−d, p−d′). Real points satisfy w = z̄, and I assert the w-jump is 1/d.
- Nonarchimedean states: union-find classes of |z_x − z_x′|_v ≤ e^{−s} and |w_x − w_x′|_v ≤ e^{s} over the base, the two endpoints and three extra vertices. Labels are the first vertex in a fixed order. The script asserts that the relation is already transitive (ultrametric).
- Archimedean states: half-open grid cells with random fixed fractional shifts.

The script then scans s and records every level with (Y1=Y2=1 and B1 match) or (Y1=Y2=0 and A match), and checks that each lies in [b−T_v, b] ∪ [b′, b′+T_v]. As a sanity check it also tests Lemma 4.5's nonarchimedean consistency of both edges.

Per-place table for two pairs (the second pair has a diagonal difference, which makes the archimedean constant sharp):
```
d = (3/5+4/5i)  d' = (5/13+12/13i)  d-d' = (14/65+-8/65i)  1/d-1/d' = (14/65+8/65i)
  2|(1+1i)       wt=1  b=+0.0000 b'=+0.0000 u=+0.6931 alpha=+0.6931 T=+0.6931  (5.14) lhs==rhs: True  [2*log2]
  5|(1+2i)       wt=1/2  b=-1.6094 b'=+0.0000 u=-1.6094 alpha=+0.0000 T=+0.0000  (5.14) lhs==rhs: True  [-1*log5]
  5|(1+-2i)      wt=1/2  b=+0.0000 b'=+1.6094 u=+0.0000 alpha=+0.0000 T=+0.0000  (5.14) lhs==rhs: True  [-1*log5]
  13|(2+3i)      wt=1/2  b=-2.5649 b'=+0.0000 u=-2.5649 alpha=+0.0000 T=+0.0000  (5.14) lhs==rhs: True  [-1*log13]
  13|(2+-3i)     wt=1/2  b=+0.0000 b'=+2.5649 u=+0.0000 alpha=+0.0000 T=+0.0000  (5.14) lhs==rhs: True  [-1*log13]
  arch id        wt=1/2  b=+0.0000 b'=+0.0000 u=+1.3940 alpha=+1.3940 T=+2.0872  (5.14) lhs==rhs: True  [-2*log2 + 1*log5 + 1*log13]
  arch conj      wt=1/2  b=+0.0000 b'=+0.0000 u=+1.3940 alpha=+1.3940 T=+2.0872  (5.14) lhs==rhs: True  [-2*log2 + 1*log5 + 1*log13]
  Sum* of (5.14) lhs = 0 (product formula: must be 0)
  Sum*(b'-b) = 1*log5 + 1*log13  2 Sum* T_v - 2 log2 = 1*log5 + 1*log13  equal: True
d = (3/5+4/5i)  d' = (4/5+3/5i)  d-d' = (-1/5+1/5i)  1/d-1/d' = (-1/5+-1/5i)
  2|(1+1i)       wt=1  b=+0.0000 b'=+0.0000 u=+0.3466 alpha=+0.3466 T=+0.3466  (5.14) lhs==rhs: True  [1*log2]
  5|(1+2i)       wt=1/2  b=-1.6094 b'=+1.6094 u=-1.6094 alpha=+0.0000 T=+0.0000  (5.14) lhs==rhs: True  [-2*log5]
  5|(1+-2i)      wt=1/2  b=-1.6094 b'=+1.6094 u=-1.6094 alpha=+0.0000 T=+0.0000  (5.14) lhs==rhs: True  [-2*log5]
  arch id        wt=1/2  b=+0.0000 b'=+0.0000 u=+1.2629 alpha=+1.2629 T=+1.9560  (5.14) lhs==rhs: True  [-1*log2 + 2*log5]
  arch conj      wt=1/2  b=+0.0000 b'=+0.0000 u=+1.2629 alpha=+1.2629 T=+1.9560  (5.14) lhs==rhs: True  [-1*log2 + 2*log5]
  Sum* of (5.14) lhs = 0 (product formula: must be 0)
  Sum*(b'-b) = 2*log5  2 Sum* T_v - 2 log2 = 2*log5  equal: True
```
Full run (all 420 pair-experiments, seed 7, 200-point grid plus breakpoints, 4+2 shifts per archimedean entry):
```
MODE paper pairs 420 (5.14) exact failures 0 product-formula sum!=0: 0
positive-eligible (s,place,shift) samples 91313 outside (5.15): 0 max T_v 3.85
Lemma 4.5 nonarch consistency failures: 0
```
Controls (4 units = 24 pair-experiments):
- swapN: N defined on the SHARED coordinate. Should fail, and does.
- nolog2: c_v = 0 at infinity. Should fail, and does, at exactly the predicted level band s ∈ (α, log 5) for d − d′ = (−1+i)/5.
- halflog2: c_v = (1/2)log 2. Passes, which shows log √2 is the sharp label-match constant.
- wrongscale: B1 at side e^{−s}. Should fail, and does.
```
== control swapN (args: seed 7, grid 300, 6 shifts, 4 units)
  violation: Q (3/5+4/5i) (4/5+3/5i) na 2 s=-4.3176 b=0.0000 b'=0.0000 T=0.3466
  violation: Q (3/5+4/5i) (4/5+3/5i) na 2 s=-4.2886 b=0.0000 b'=0.0000 T=0.3466
MODE swapN pairs 24 (5.14) exact failures 0 product-formula sum!=0: 0
positive-eligible (s,place,shift) samples 444417 outside (5.15): 417570 max T_v 2.087
Lemma 4.5 nonarch consistency failures: 0
== control nolog2 (args: seed 7, grid 300, 6 shifts, 4 units)
  violation: Q (3/5+4/5i) (4/5+3/5i) arch id s=1.2982 b=0.0000 b'=0.0000 T=1.2629
  violation: Q (3/5+4/5i) (4/5+3/5i) arch id s=1.2631 b=0.0000 b'=0.0000 T=1.2629
MODE nolog2 pairs 24 (5.14) exact failures 0 product-formula sum!=0: 0
positive-eligible (s,place,shift) samples 10081 outside (5.15): 169 max T_v 1.946
Lemma 4.5 nonarch consistency failures: 0
== control halflog2 (args: seed 7, grid 300, 6 shifts, 4 units)
MODE halflog2 pairs 24 (5.14) exact failures 0 product-formula sum!=0: 0
positive-eligible (s,place,shift) samples 9670 outside (5.15): 0 max T_v 1.946
Lemma 4.5 nonarch consistency failures: 0
== control wrongscale (args: seed 7, grid 300, 6 shifts, 4 units)
  violation: Q (3/5+4/5i) (4/5+3/5i) na 2 s=-4.3466 b=0.0000 b'=0.0000 T=0.3466
  violation: Q (3/5+4/5i) (4/5+3/5i) na 2 s=-4.3176 b=0.0000 b'=0.0000 T=0.3466
  violation: Q (3/5+4/5i) (4/5+3/5i) na 2 s=-4.2886 b=0.0000 b'=0.0000 T=0.3466
MODE wrongscale pairs 24 (5.14) exact failures 0 product-formula sum!=0: 0
positive-eligible (s,place,shift) samples 224379 outside (5.15): 206270 max T_v 2.087
```
Scripts `scores_toy_qi.py` and `scores_toy_table.py`:
```python
# Toy check of (5.14), the product-formula cancellation, and the flank support (5.15)
# in N = Q(i), using the ACTUAL state definitions of Section 4.4:
#   nonarch entry v: A-class  = classes of |z_x - z_x'|_v <= e^{-s}  (labels = first vertex in fixed order)
#                    B1-class = classes of |w_x - w_x'|_v <= e^{s}
#   arch entry sigma: A = half-open grid cell of sigma(z_x), side e^{-s}; B1 = cell of sigma(w_x), side e^{s};
#                     one fixed fractional shift per grid, scaled with the side at every level.
# Weighted places of Q(i) (d_N = 2): 2 archimedean entries (id, conj), weight 1/2 each;
#   split l=1 mod 4: two places, 1 copy each; l=2 ramified (pi=1+i): 2 copies; l=3 mod 4 inert: 2 copies.
#   normalisation |l|_p = 1/l.
import sys, math, random, itertools
from fractions import Fraction as F
from sympy import factorint
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 7)
MODE = sys.argv[2] if len(sys.argv)>2 else "paper"   # paper | swapN | nolog2 | halflog2 | wrongscale

class G:
    __slots__=("a","b")
    def __init__(s,a,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): return G(s.a+o.a,s.b+o.b)
    def __sub__(s,o): return G(s.a-o.a,s.b-o.b)
    def __mul__(s,o): return G(s.a*o.a-s.b*o.b, s.a*o.b+s.b*o.a)
    def conj(s): return G(s.a,-s.b)
    def norm(s): return s.a*s.a+s.b*s.b
    def inv(s): n=s.norm(); return G(s.a/n,-s.b/n)
    def iszero(s): return s.a==0 and s.b==0
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def __repr__(s): return f"({s.a}+{s.b}i)"

def gauss_prime_over(l):
    if l==2: return [G(1,1)]
    if l%4==3: return [G(l,0)]
    for a in range(1,int(l**0.5)+1):
        b2=l-a*a; b=int(round(b2**0.5))
        if b*b==b2: return [G(a,b),G(a,-b)]
    raise ValueError(l)

def divides(pi,g):  # g Gaussian integer
    q=g*pi.conj(); n=pi.norm()
    return (q.a/n).denominator==1 and (q.b/n).denominator==1

def ord_int(pi,g):  # g nonzero Gaussian integer
    o=0
    while divides(pi,g):
        q=g*pi.conj(); g=G(q.a/pi.norm(),q.b/pi.norm()); o+=1
    return o

def ordpi(pi,x):
    n=math.lcm(x.a.denominator,x.b.denominator); g=G(x.a*n,x.b*n)
    return ord_int(pi,g)-ord_int(pi,G(n,0))

def primes_of(x):
    s=set()
    for num in (x.norm().numerator, x.norm().denominator):
        s|=set(factorint(num).keys())
    return s

def places_for(elts):
    ps=set()
    for x in elts: ps|=primes_of(x)
    out=[]
    for l in sorted(ps):
        for pi in gauss_prime_over(l):
            e=2 if l==2 else 1
            copies=2 if (l==2 or l%4==3) else 1
            out.append(("na",l,pi,e,copies))
    out.append(("arch","id",None,None,1)); out.append(("arch","conj",None,None,1))
    return out

def logabs_sym(x,pl):
    """log|x|_v as dict prime->Fraction coefficient of log(prime)"""
    if pl[0]=="na":
        _,l,pi,e,_=pl
        return {l: F(-ordpi(pi,x),e)}
    n=x.norm(); d={}
    for p,k in factorint(n.numerator).items(): d[p]=d.get(p,0)+F(k,2)
    for p,k in factorint(n.denominator).items(): d[p]=d.get(p,0)-F(k,2)
    return d
def sym_add(*ds):
    out={}
    for c,d in ds:
        for p,k in d.items(): out[p]=out.get(p,0)+c*k
    return {p:k for p,k in out.items() if k!=0}
def sym_val(d): return sum(float(k)*math.log(p) for p,k in d.items())

def emb(pl,x):
    return complex(float(x.a),float(x.b)) if pl[1]=="id" else complex(float(x.a),-float(x.b))

# --- unit Gaussian rationals (|d|=1): jumps of real unit edges
UNITS=[G(F(3,5),F(4,5)),G(F(4,5),F(3,5)),G(F(5,13),F(12,13)),G(F(12,13),F(5,13)),G(F(8,17),F(15,17)),
       G(F(-3,5),F(4,5)),G(F(3,5),F(-4,5)),G(0,1),G(-1,0),G(F(7,25),F(24,25)),G(F(20,29),F(21,29)),
       G(F(33,65),F(56,65)),G(F(63,65),F(16,65)),G(F(-5,13),F(12,13)),G(F(9,41),F(40,41))]
for u in UNITS: assert u.norm()==1

LOG2=math.log(2)
def cv_add(pl):
    if pl[0]=="na": return 0.0
    return {"paper":LOG2,"swapN":LOG2,"wrongscale":LOG2,"nolog2":0.0,"halflog2":0.5*LOG2}[MODE]

viol=0; checks=0; pf_fail=0; e514_fail=0; consist_fail=0; pairs=0; maxT=0
EXTRA=[G(F(5,3),F(2,7)),G(F(-2,9),F(5,4)),G(F(7,6),F(-1,10))]
NU=int(sys.argv[5]) if len(sys.argv)>5 else 6
PAIRS=list(itertools.permutations(UNITS[:NU],2))
for d,dp in PAIRS:
  for exper in ("Q","P"):
    pairs+=1
    if exper=="Q":
        base=G(F(1,3),F(2,7)); y1=base+d; y2=base+dp     # base centre q, points p=q+d, r=q+d'
    else:
        base=G(F(2,5),F(-1,11)); y1=base-d; y2=base-dp   # base point p, centres q=p-d, q'=p-d'
    Z={ 'x':base,'y1':y1,'y2':y2 }
    W={k:v.conj() for k,v in Z.items()}                   # real points: w = conj(z)
    # edge jump on edge (point,centre): d_e = z_point - z_centre ; w-jump = 1/d_e
    if exper=="Q": de1=Z['y1']-Z['x']; de2=Z['y2']-Z['x']
    else:          de1=Z['x']-Z['y1']; de2=Z['x']-Z['y2']
    assert de1==d and de2==dp
    assert (W['y1']-W['x'] if exper=="Q" else W['x']-W['y1'])==d.inv()
    verts=[('x',base),('y1',y1),('y2',y2)]+[(f"e{i}",z) for i,z in enumerate(EXTRA)]
    elts=[d,dp,d-dp,d.inv()-dp.inv()]+[a-b for (_,a),(_,b) in itertools.combinations(verts,2)]
    PL=places_for(elts)
    tot514=F(0); total={}
    for pl in PL:
        w=F(1,2)*pl[4]           # weight 1/d_N per copy
        n1=sym_add((-1,logabs_sym(d,pl))); n2=sym_add((-1,logabs_sym(dp,pl)))
        u=sym_add((-1,logabs_sym(d-dp,pl)))
        b,bp = (n1,n2) if sym_val(n1)<=sym_val(n2) else (n2,n1)
        alpha=sym_add((1,u),(-1,b))
        lhs=sym_add((-1,logabs_sym((d-dp)*(d.inv()-dp.inv()),pl)))
        rhs=sym_add((2,alpha),(-1,bp),(1,b))
        if lhs!=rhs: e514_fail+=1
        total=sym_add((1,total),(w,lhs))
        bv,bpv,av=sym_val(b),sym_val(bp),sym_val(alpha)
        cv=cv_add(pl); T=av+cv; maxT=max(maxT,T)
        if pl[0]=="arch": assert av>=-LOG2-1e-12
        # --- scan thresholds with the actual state definitions
        n1v,n2v=sym_val(n1),sym_val(n2)
        lo=min(bv-abs(T),bv)-4; hi=max(bpv+abs(T),bpv)+4
        NG=int(sys.argv[3]) if len(sys.argv)>3 else 600
        NS=int(sys.argv[4]) if len(sys.argv)>4 else 8
        grid=[lo+(hi-lo)*i/NG for i in range(NG+1)]
        breaks=[n1v,n2v]
        if pl[0]=="na":
            nv=len(verts); zc=[v for _,v in verts]; wc=[v.conj() for _,v in verts]
            LZ={(i,j):sym_val(logabs_sym(zc[i]-zc[j],pl)) for i,j in itertools.combinations(range(nv),2)}
            LW={(i,j):sym_val(logabs_sym(wc[i]-wc[j],pl)) for i,j in itertools.combinations(range(nv),2)}
            breaks+= [-x for x in LZ.values()]+list(LW.values())
            grid+= [t+e for t in breaks for e in (-1e-6,1e-6)]
            def cls(L,thr):
                par=list(range(nv))
                def f(i):
                    while par[i]!=i: i=par[i]
                    return i
                for (i,j),val in L.items():
                    if val<=thr+1e-12: par[f(j)]=f(i)
                # ultrametric => relation already transitive: verify
                for (i,j),val in L.items():
                    assert (f(i)==f(j))==(val<=thr+1e-12)
                return [min(k for k in range(nv) if f(k)==f(i)) for i in range(nv)]
            shifts=[None]
        else:
            zA=[emb(pl,v) for _,v in verts]; wB=[emb(pl,v.conj()) for _,v in verts]
            shifts=[((random.random(),random.random()),(random.random(),random.random())) for _ in range(NS)]+[((0.,0.),(0.,0.)),((.5,.5),(.5,.5))]
            def cell(c,side,shift): return (math.floor(c.real/side+shift[0]),math.floor(c.imag/side+shift[1]))
        for sh in shifts:
          for s in grid:
            if any(abs(s-t)<1e-9 for t in (n1v,n2v)): continue
            Y1=1 if n1v>s else 0; Y2=1 if n2v>s else 0
            if pl[0]=="na":
                Alab=cls(LZ,-s); Blab=cls(LW,-s if MODE=="wrongscale" else s)
                Am=Alab[1]==Alab[2]; Bm=Blab[1]==Blab[2]
                for j,Y in ((1,Y1),(2,Y2)):
                    Aj=Alab[0]==Alab[j]; Bj=Blab[0]==Blab[j]
                    ok=(Y==1 and Aj and not Bj) or (Y==0 and Bj and not Aj)
                    if MODE!="wrongscale" and not ok: consist_fail+=1
            else:
                sideA=math.exp(-s); sideB=math.exp(-s) if MODE=="wrongscale" else math.exp(s)
                Am=cell(zA[1],sideA,sh[0])==cell(zA[2],sideA,sh[0])
                Bm=cell(wB[1],sideB,sh[1])==cell(wB[2],sideB,sh[1])
            if MODE=="swapN": pos=(Y1==Y2==1 and Am) or (Y1==Y2==0 and Bm)
            else:             pos=(Y1==Y2==1 and Bm) or (Y1==Y2==0 and Am)
            if pos:
                checks+=1
                inside=(bv-T-1e-9<=s<=bv+1e-9) or (bpv-1e-9<=s<=bpv+T+1e-9)
                if not inside:
                    viol+=1
                    if viol<=3: print("  violation:",exper,d,dp,pl[0],pl[1],"s=%.4f b=%.4f b'=%.4f T=%.4f"%(s,bv,bpv,T))
    if total!={}: pf_fail+=1
print("MODE",MODE,"pairs",pairs,"(5.14) exact failures",e514_fail,"product-formula sum!=0:",pf_fail)
print("positive-eligible (s,place,shift) samples",checks,"outside (5.15):",viol,"max T_v",round(maxT,3))
if MODE in("paper","nolog2","halflog2","swapN"): print("Lemma 4.5 nonarch consistency failures:",consist_fail)
```
```python
# Print the per-place table (b, b', u, alpha, T_v, (5.14) both sides) for one explicit pair in Q(i).
import sys, math
sys.argv=['x','7','paper']
src=open('/tmp/oaimath/167/checks/scores_toy_qi.py').read().split('# --- unit Gaussian')[0]
exec(src)
def fmt(d): 
    return " + ".join(f"{k}*log{p}" for p,k in sorted(d.items())) or "0"
for (d,dp) in [(G(F(3,5),F(4,5)),G(F(5,13),F(12,13))),(G(F(3,5),F(4,5)),G(F(4,5),F(3,5)))]:
    print("d =",d," d' =",dp," d-d' =",d-dp," 1/d-1/d' =",d.inv()-dp.inv())
    PL=places_for([d,dp,d-dp,d.inv()-dp.inv()])
    sumb=F(0); tot={}; sumbb={}; sumT={}
    for pl in PL:
        w=F(1,2)*pl[4]
        n1=sym_add((-1,logabs_sym(d,pl))); n2=sym_add((-1,logabs_sym(dp,pl)))
        u=sym_add((-1,logabs_sym(d-dp,pl)))
        b,bp=(n1,n2) if sym_val(n1)<=sym_val(n2) else (n2,n1)
        al=sym_add((1,u),(-1,b))
        cv={} if pl[0]=="na" else {2:F(1)}
        T=sym_add((1,al),(1,cv))
        lhs=sym_add((-1,logabs_sym((d-dp)*(d.inv()-dp.inv()),pl)))
        rhs=sym_add((2,al),(-1,bp),(1,b))
        name=f"{pl[1]}|{pl[2]}" if pl[0]=="na" else f"arch {pl[1]}"
        print(f"  {name:14s} wt={w}  b={sym_val(b):+.4f} b'={sym_val(bp):+.4f} u={sym_val(u):+.4f} alpha={sym_val(al):+.4f} T={sym_val(T):+.4f}  (5.14) lhs==rhs: {lhs==rhs}  [{fmt(lhs)}]")
        tot=sym_add((1,tot),(w,lhs)); sumbb=sym_add((1,sumbb),(w,bp),(-w,b)); sumT=sym_add((1,sumT),(w,T))
    print("  Sum* of (5.14) lhs =",fmt(tot),"(product formula: must be 0)")
    print("  Sum*(b'-b) =",fmt(sumbb)," 2 Sum* T_v - 2 log2 =",fmt(sym_add((2,sumT),(-2,{2:F(1)}))),
          " equal:",sumbb==sym_add((2,sumT),(-2,{2:F(1)})))
```

### (b′) Abstract archimedean entry with non-unit jumps (b ≠ b′, α near −log 2)

At a non-identity embedding, z and w are unrelated except through w_y − w_x = 1/(z_y − z_x). With
random complex jumps of all sizes and random grid shifts, (5.15) holds with c_v = log 2 and FAILS
with c_v = 0. With c_v = (1/2)log 2 the supports are still contained in the flanks, but T_v < 0 in
632/3000 cases, which Lemma 5.4 (T ≥ 0) cannot accept. So log 2 is what the TRIANGLE INEQUALITY
step needs, and the paper's choice is the right one.
```
c_v=log2      positive-eligible samples=263853 outside flanks=0 (cases with T<0: 0)
c_v=halflog2  positive-eligible samples=276792 outside flanks=0 (cases with T<0: 632)
c_v=zero      positive-eligible samples=290056 outside flanks=301 (cases with T<0: 1353)
```
```python
# Abstract archimedean entry: at a non-identity embedding z and w are independent complex coordinates,
# only the edge relation w_y - w_x = 1/(z_y - z_x) holds. Random base (z0,w0), random jumps d1,d2 (any size),
# endpoints z=z0+d_j, w=w0+1/d_j. States: A = half-open grid cell of z at side e^{-s}, B1 = cell of w at side e^{s},
# one fixed fractional shift per grid. Check that every s with
#   (Y1=Y2=1 and B1 match) or (Y1=Y2=0 and A match)
# lies in [b-T,b] U [b',b'+T], T = alpha + c, alpha = u - b, u = -log|d1-d2|, for c = log 2 (paper),
# and that c = 0 (control) FAILS; c = (1/2) log 2 is reported (sharp constant).
import random, math, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 11)
def cell(c,side,sh): return (math.floor(c.real/side+sh[0]),math.floor(c.imag/side+sh[1]))
res={}
for cname,cval in (("log2",math.log(2)),("halflog2",0.5*math.log(2)),("zero",0.0)):
    viol=0; pos=0; negT=0
    random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 11)
    for it in range(3000):
        z0=complex(random.gauss(0,3),random.gauss(0,3)); w0=complex(random.gauss(0,3),random.gauss(0,3))
        def rj():
            r=math.exp(random.gauss(0,1.5)); th=random.uniform(0,2*math.pi); return r*complex(math.cos(th),math.sin(th))
        d1=rj()
        mode=random.random()
        if mode<0.3: d2=d1*complex(1+random.gauss(0,0.05),random.gauss(0,0.05))   # near-equal jumps
        elif mode<0.45: d2=-d1*(1+random.gauss(0,0.02))                             # near-opposite (alpha ~ -log 2)
        else: d2=rj()
        n1=-math.log(abs(d1)); n2=-math.log(abs(d2)); b,bp=min(n1,n2),max(n1,n2)
        u=-math.log(abs(d1-d2)); alpha=u-b
        assert alpha>=-math.log(2)-1e-9          # triangle inequality
        T=alpha+cval
        if T<0: negT+=1
        zs=[z0+d1,z0+d2]; ws=[w0+1/d1,w0+1/d2]
        shA=(random.random(),random.random()); shB=(random.random(),random.random())
        lo=b-abs(T)-4; hi=bp+abs(T)+4
        for i in range(1201):
            s=lo+(hi-lo)*i/1200
            Y1=n1>s; Y2=n2>s
            Am=cell(zs[0],math.exp(-s),shA)==cell(zs[1],math.exp(-s),shA)
            Bm=cell(ws[0],math.exp(s),shB)==cell(ws[1],math.exp(s),shB)
            if (Y1 and Y2 and Bm) or ((not Y1) and (not Y2) and Am):
                pos+=1
                if not ((b-T-1e-9<=s<=b+1e-9) or (bp-1e-9<=s<=bp+T+1e-9)): viol+=1
    res[cname]=(pos,viol,negT)
    print(f"c_v={cname:9s} positive-eligible samples={pos} outside flanks={viol} (cases with T<0: {negT})")
```

### (d) Abstract one-place check of Prop 5.5's per-place budget, including the one-sided rare-positive argument

The inequality checked is
score_v ≤ 2T_v + λ|J_v|·1{b,b′ ∈ int J_v} − (b′−b).

Setup:
- π is the true, monotone empirical profile of random edge values.
- Classes are assigned from f against random ε. Rare pieces are randomly good or damaged, with random I_x.
- The base law is a random conditional atom law.
- The worst case is taken: N holds on the whole flank.

Results:
- Paper mode: 0 violations, with the paper's constants and with stress constants (δ = 0.2, λ = 0.3, where the λ|J| excess is actually used).
- Control nonmono (π shuffled, which breaks the monotonicity the one-sided argument uses): FAILS.
- Control anybit (rare positives allowed regardless of the minority bit): FAILS.
```
MODE paper constants stress trials 40000 rare-positive trials 492 trials using the lam|J| excess 71 VIOLATIONS 0
MODE paper constants paper trials 40000 rare-positive trials 492 trials using the lam|J| excess 0 VIOLATIONS 0
MODE nonmono constants stress trials 40000 rare-positive trials 9698 trials using the lam|J| excess 2824 VIOLATIONS 2744
MODE nonmono constants paper trials 40000 rare-positive trials 9698 trials using the lam|J| excess 3124 VIOLATIONS 3123
MODE anybit constants stress trials 40000 rare-positive trials 17676 trials using the lam|J| excess 7555 VIOLATIONS 7476
MODE anybit constants paper trials 40000 rare-positive trials 17676 trials using the lam|J| excess 7806 VIOLATIONS 7806
```
```python
# Abstract single-place check of the per-place inequality used in Prop 5.5:
#   score_v  <=  2 T_v + lam |J_v| 1{b,b' in int J_v}  - (b'-b),
# where positives can only sit at s<b with both bits 1 inside I_- = [b-T,b], or at s>=b' with both
# bits 0 inside I_+ = [b',b'+T] (worst case: N true on the whole flank), the level classes come from a
# MONOTONE global profile pi(s)=P_E(n_e>s), common coefficient c(rho), good-rare coefficient 2 I_x(s)
# only when Y1=Y2=minority bit, damaged 0, negative charge 1{Y1!=Y2} at ALL levels.
# Controls (should FAIL): (A) non-monotone pi (pi values shuffled across pieces);
#                         (B) rare positives allowed regardless of the minority bit.
import random, sys, bisect
seed=int(sys.argv[1]) if len(sys.argv)>1 else 3
MODE=sys.argv[2] if len(sys.argv)>2 else "paper"
DL=sys.argv[3] if len(sys.argv)>3 else "stress"
random.seed(seed)
if DL=="paper": delta=0.01; lam=delta**2/2
else: delta=0.2; lam=0.3
def val(): return random.choice([round(random.uniform(-3,3),2), float(random.randint(-3,3))])
N=40000; viol=0; rarecases=0; excess_cases=0
for it in range(N):
    m=random.randint(2,9)
    ev=[val() for _ in range(m)]
    n1,n2=random.sample(ev,2) if m>=2 else (ev[0],ev[0])
    b,bp=min(n1,n2),max(n1,n2)
    lo=min(ev)-random.uniform(0,2); hi=max(ev)+random.uniform(0,2)
    T=abs(val())*random.random()
    eps=random.uniform(0.01,0.5)
    # conditional law of n_e given the base: random atoms (must include n1,n2 as possible values)
    ca=sorted(set([n1,n2]+[val() for _ in range(random.randint(0,4))]))
    cw=[random.random()**2 for _ in ca]; Z=sum(cw); cw=[x/Z for x in cw]
    # random piece structure for rare-level types and I_x
    cuts=sorted(set([round(random.uniform(lo,hi),2) for _ in range(random.randint(0,6))]))
    bps=sorted(set([lo,hi]+ev+ca+cuts+[b-T,b,bp,bp+T]))
    bps=[x for x in bps if lo<=x<=hi]
    piece_type={}; piece_I={}
    def ptype(s):
        k=bisect.bisect_right(cuts,s)
        if k not in piece_type: piece_type[k]=random.choice(["good","good","damaged"]); piece_I[k]=random.randint(0,1)
        return piece_type[k],piece_I[k]
    def pi_true(s): return sum(1 for x in ev if x>s)/len(ev)
    subs=[(bps[i],bps[i+1]) for i in range(len(bps)-1) if bps[i+1]>bps[i]]
    if MODE=="nonmono":
        pis=[pi_true((u+v)/2) for u,v in subs]; random.shuffle(pis)
        pimap={sv:p for sv,p in zip(subs,pis)}
    score=0.0; Jlen=0.0; Jpieces=[]; rare_pos=False
    for (u,v) in subs:
        s=(u+v)/2; L=v-u
        pi=pimap[(u,v)] if MODE=="nonmono" else pi_true(s)
        f=min(pi,1-pi)
        rho=sum(w for a,w in zip(ca,cw) if a>s)
        Y1=1 if n1>s else 0; Y2=1 if n2>s else 0
        common = f>=eps
        if common and abs(rho-0.5)<=delta: Jlen+=L; Jpieces.append((u,v))
        elig = (Y1==Y2==1 and b-T<=s<=b) or (Y1==Y2==0 and bp<=s<=bp+T)
        coef=0.0
        if common: coef = 1+lam if abs(rho-0.5)<=delta else 1-lam
        else:
            t,Ix=ptype(s)
            r = 1 if pi<0.5 else 0
            if t=="good" and Ix==1 and (Y1==Y2==r or MODE=="anybit"):
                coef=2.0
                if elig: rare_pos=True
        if elig: score+=coef*L
        if Y1!=Y2: score-=L
    if rare_pos: rarecases+=1
    if Jpieces:
        j0=min(u for u,v in Jpieces); j1=max(v for u,v in Jpieces)
        if MODE!="nonmono": assert abs((j1-j0)-Jlen)<1e-9, "J not an interval"
        ind = 1.0 if (j0<b<j1 and j0<bp<j1) else 0.0
    else: ind=0.0
    bound=2*T+lam*Jlen*ind-(bp-b)
    if score>bound+1e-9:
        viol+=1
        if viol<=2: print("  violation: b=%.2f b'=%.2f T=%.2f score=%.4f bound=%.4f rare=%s"%(b,bp,T,score,bound,rare_pos))
    if score>2*T-(bp-b)+1e-9: excess_cases+=1
print("MODE",MODE,"constants",DL,"trials",N,"rare-positive trials",rarecases,"trials using the lam|J| excess",excess_cases,"VIOLATIONS",viol)
```

### (c) Constants δ = 1/100, λ = δ²/2 (exact rationals)

Checked:
- (6.7): min = λ/2 exactly, attained at ρ = 1/2.
- 4δ² − λ > λ/2.
- 4/(2(1/4−δ²)) = 8.0032 ≤ 10.
- 10δ² < 1/4, i.e. λ/4 > 10δ²λ.

Controls: λ = 8δ² (should break (6.7)) and δ = 1/5 (should break 10δ² < 1/4). Both FAIL as expected.
```
[paper] delta=1/100 lam=1/20000
  (6.7) min over grid+edges = 2.5e-05  >= lam/2: True ; outside-edge infimum 4d^2-lam(1/2+2d^2) = 0.00037499
  4d^2 - lam > lam/2 : True
  Prop 5.5 constant 4/(2(1/4-d^2)) = 8.003201280512204  <= 10 : True
  10 d^2 < 1/4 : True   (sandwich lam/4 > 10 d^2 lam: True )
  on window 2rho(1-rho) >= 2(1/4-d^2): True
[control lam=8 d^2 (should FAIL (6.7))] delta=1/100 lam=1/1250
  (6.7) min over grid+edges = -1.59999920032e-07  >= lam/2: False ; outside-edge infimum 4d^2-lam(1/2+2d^2) = -1.6e-07
  4d^2 - lam > lam/2 : False
  Prop 5.5 constant 4/(2(1/4-d^2)) = 8.003201280512204  <= 10 : True
  10 d^2 < 1/4 : True   (sandwich lam/4 > 10 d^2 lam: True )
  on window 2rho(1-rho) >= 2(1/4-d^2): True
[control delta=1/5 (should FAIL 10d^2<1/4)] delta=1/5 lam=1/50
  (6.7) min over grid+edges = 0.01  >= lam/2: True ; outside-edge infimum 4d^2-lam(1/2+2d^2) = 0.1484
  4d^2 - lam > lam/2 : True
  Prop 5.5 constant 4/(2(1/4-d^2)) = 9.523809523809524  <= 10 : True
  10 d^2 < 1/4 : False   (sandwich lam/4 > 10 d^2 lam: False )
  on window 2rho(1-rho) >= 2(1/4-d^2): True
ALL PAPER CONSTANT CHECKS PASS: True | control1 passes? False | control2 passes? False
```
```python
# Constants of Sections 5-6: delta=1/100, lambda=delta^2/2 (exact rational arithmetic).
from fractions import Fraction as F
import sys
def run(delta,lam,label):
    ok=True
    half=F(1,2)
    def c(r): return 1+lam if abs(r-half)<=delta else 1-lam
    def g(r): return c(r)*(r*r+(1-r)**2)-2*r*(1-r)
    # identity in (6.7)
    for r in [F(i,1000) for i in range(1001)]+[half-delta,half+delta]:
        assert g(r)==(2*r-1)**2+(c(r)-1)*(r*r+(1-r)**2)
    # (6.7) >= lam/2: inside window min is at r=1/2 (value lam/2 exactly); outside, infimum at the window edge
    grid=[F(i,100000) for i in range(100001)]
    eps=F(1,10**12)
    pts=grid+[half-delta,half+delta,half-delta-eps,half+delta+eps]
    m=min(g(r) for r in pts)
    c67 = m>=lam/2
    inf_out = 4*delta**2 - lam*(half+2*delta**2)   # limit of g at the window edge from outside
    print(f"[{label}] delta={delta} lam={lam}")
    print("  (6.7) min over grid+edges =",float(m)," >= lam/2:",c67, "; outside-edge infimum 4d^2-lam(1/2+2d^2) =",float(inf_out))
    print("  4d^2 - lam > lam/2 :", 4*delta**2-lam > lam/2)
    k55 = 4/(2*(F(1,4)-delta**2))
    print("  Prop 5.5 constant 4/(2(1/4-d^2)) =",float(k55)," <= 10 :", k55<=10)
    print("  10 d^2 < 1/4 :", 10*delta**2 < F(1,4), "  (sandwich lam/4 > 10 d^2 lam:", lam/4 > 10*delta**2*lam,")")
    print("  on window 2rho(1-rho) >= 2(1/4-d^2):", min(2*r*(1-r) for r in [half-delta,half+delta,half])>=2*(F(1,4)-delta**2))
    return c67 and (4*delta**2-lam>lam/2) and k55<=10 and 10*delta**2<F(1,4)
a=run(F(1,100),F(1,100)**2/2,"paper")
b=run(F(1,100),8*F(1,100)**2,"control lam=8 d^2 (should FAIL (6.7))")
c=run(F(1,5),F(1,5)**2/2,"control delta=1/5 (should FAIL 10d^2<1/4)")
print("ALL PAPER CONSTANT CHECKS PASS:",a,"| control1 passes?",b,"| control2 passes?",c)
```

## CITATION TABLE (scope)

§5 cites NO external source. Every appeal is internal: Lemma 2.5, Lemma 2.6, Cor 3.3/(3.17),
Prop 4.4, Lemma 4.1 (the product formula, cited there to Milne [19] — outside my scope) and
Lemma 4.5. Each internal appeal was checked against the stated hypotheses of the result it uses:

| Use | Hypothesis | Status |
|---|---|---|
| Lemma 2.5 at each good rare level | common finite alphabet; mismatch ≤ f + m ≤ ε + 1/k ≤ s_0 eventually, uniform | MATCH |
| Lemma 2.6(ii),(iii) in (5.6) | marginals ≤ δ_t = C(ε + 1/k) → 0 on G | MATCH |
| (3.17) in (5.7) | tests = levels of C with the normalised measure, independent of the vertices; m bounds strict-cross failure (consistency ⇒ strict cross) | MATCH |
| Lemma 4.5 in (5.15) | label match ⇒ |·|_v ≤ c e^{∓s}, c ∈ {1, √2} | MATCH |
| Product formula in Prop 5.5 | (d−d′)(1/d−1/d′) ∈ N^× | MATCH |

## SUMMARY

§5 HOLDS AS READ, conditional on the out-of-scope inputs listed at the top. There is no FATAL
objection and no GAP. O1 (score display) is an exposition point that must be fixed, because the
literal typesetting makes Prop 5.5 false. O2–O4 are cosmetic.
