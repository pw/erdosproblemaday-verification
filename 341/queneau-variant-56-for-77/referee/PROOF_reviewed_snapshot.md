# Erdős #341, Queneau's variant (distinct summands): a seed with non-eventually-periodic gaps

**Setting.** Erdős Problem 341 (Erdős–Graham 1980, p. 53; "an old problem of Dickson"): extend a finite set A of positive
integers greedily by letting a_{n+1} be the least integer > a_n that is not of the form a_i + a_j with i, j ≤ n
(equal indices allowed — Dickson's rule, "rule D"). Is the gap sequence a_{m+1} − a_m always eventually periodic?
Zhiheng Li (Aug 2026, with GPT-5.6 Sol; Lean 4; refereed by us 2026-10-13) answered NO with the seed
A_Li = {1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,63,71,77,81,89,97}.
Ben Green's open-problems list (Problem 7, Jan 2026) poses, beside Dickson's rule, **Queneau's variant ("rule Q")**:
a_{n+1} is the least integer > a_n not of the form a_i + a_j with i < j ≤ n (distinct earlier terms), and says
"for both variants, the following question appears to be open: is u_{n+1} − u_n eventually periodic?"
Li's seed under rule Q is eventually periodic (membership period 5,733 = 49·117, certified by our finite
certificate on 2026-10-13), so his counterexample does not transfer.

Notation: ℕ_0 = {0,1,2,…}; [a,b] = {a,…,b}; for X ⊆ ℕ_0, X + X = {u+v : u,v ∈ X} and X ⊕ X = {u+v : u,v ∈ X, u ≠ v}.

## Theorem 1 (rule Q)
Let **A = {1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,56,63,71,81,89,97}** (Li's seed with 77 replaced by 56; 21 elements).
Under rule Q the greedy extension of A has a gap sequence that is not eventually periodic.

## Theorem 2 (rule D, same seed)
Under Dickson's rule the greedy extension of the same A also has a non-eventually-periodic gap sequence.

## Lemma 1 (exact recurrence ⇒ greedy; both rules)
Let S ⊆ ℕ be infinite, N ∈ S, A = S ∩ [1,N]. If for every t > N, t ∈ S ⟺ t ∉ S ⊕ S, then the increasing enumeration
of S is the rule-Q extension of A. (Same with S + S and rule D.)
Proof. Scan t > N in increasing order; before testing t the selected set is S ∩ [1,t−1]. Every representation
t = u + v with u ≠ v in S has u, v < t, so t ∈ (S∩[1,t−1]) ⊕ (S∩[1,t−1]) ⟺ t ∈ S ⊕ S, and the rule selects t exactly
when t ∈ S. (Li's Lemma 1.2 with ⊕ in place of +.) ∎

## The strict controller (Theorem 1)
    Y0 = {0,1} ∪ ⋃_{k≥0} [8^k + 1, 2·8^k]        (I_k := [8^k+1, 2·8^k]; I_0 = {2})
    Y1 = {1}   ∪ ⋃_{k≥0} [4·8^k, 8·8^k]           (J_k)
    Y2 = {0}   ∪ ⋃_{k≥0} [2·8^k, 4·8^k]           (K_k)

**Lemma 2 (strict sumsets).**
 (S0) Y0 ⊕ Y0 = {1,2,3} ∪ ⋃_{k≥1} [8^k + 1, 4·8^k − 1]
 (S1) Y1 ⊕ Y1 = ⋃_{k≥0} [4·8^k + 1, 16·8^k − 1]
 (S2) Y2 ⊕ Y2 = ⋃_{k≥0} [2·8^k, 8·8^k − 1]
Proof. Sums of distinct elements, grouped by the larger block involved.
(S0) {0,1} ⊕ {0,1} = {1}. {0,1} + I_k = [8^k+1, 2·8^k+1]. For k ≥ 1, I_k ⊕ I_k = [(8^k+1)+(8^k+2), (2·8^k−1)+2·8^k] =
[2·8^k+3, 4·8^k−1]; I_0 ⊕ I_0 = ∅. For j < k: I_j + I_k ⊆ [8^k+8^j+2, 2·8^k+2·8^j]; with j = 0 this is
[8^k+3, 2·8^k+2], which supplies 2·8^k+2; with 1 ≤ j < k it lies inside [8^k+1, 2·8^k + 2·8^{k−1}] ⊂ [8^k+1, 4·8^k−1].
So for k ≥ 1 the sums whose larger summand lies in I_k fill exactly [8^k+1, 4·8^k−1], and the sums from {0,1} ∪ I_0 are
{1,2,3}. Since 4·8^k − 1 < 8^{k+1} + 1 the pieces are disjoint. 
(S1) 1 + J_k = [4·8^k+1, 8·8^k+1]; J_k ⊕ J_k = [8·8^k+1, 16·8^k−1]; for j<k, J_j + J_k ⊆ [4·8^k+4, 8·8^k+8·8^{k−1}] ⊂
[4·8^k+1, 16·8^k−1]. Union [4·8^k+1, 16·8^k−1]; the element 1 alone contributes nothing; 16·8^k − 1 < 4·8^{k+1} + 1.
(S2) 0 + K_k = K_k; K_k ⊕ K_k = [4·8^k+1, 8·8^k−1]; for j<k, K_j + K_k ⊆ [2·8^k+2, 4·8^k+4·8^{k−1}] ⊂ [2·8^k, 8·8^k−1].
Union [2·8^k, 8·8^k−1]; 8·8^k − 1 < 2·8^{k+1}. ∎

**Lemma 3 (gate identities, strict).** For every q ≥ 2:
 (G1) q ∈ Y1 ⟺ q ∉ Y0 ⊕ Y0;  (G2) q ∈ Y2 ⟺ q ∉ Y1 ⊕ Y1;  (G3) q ∈ Y0 ⟺ q − 1 ∉ Y2 ⊕ Y2.
Proof. From (S0), ℕ_0 ∖ (Y0 ⊕ Y0) = {0} ∪ [4,8] ∪ ⋃_{k≥1}[4·8^k, 8^{k+1}] = {0} ∪ ⋃_{k≥0} J_k, which agrees with Y1 on
[2,∞). From (S1), ℕ_0 ∖ (Y1 ⊕ Y1) = [0,4] ∪ ⋃_{k≥0}[16·8^k, 32·8^k] = [0,4] ∪ ⋃_{k≥1} K_k, which agrees with Y2 on [2,∞)
(K_0 = [2,4]). From (S2), ℕ_0 ∖ (Y2 ⊕ Y2) = {0,1} ∪ ⋃_{k≥1}[8^k, 2·8^k − 1], so q − 1 lies in it, for q ≥ 2, iff
q ∈ {2} ∪ ⋃_{k≥1}[8^k+1, 2·8^k] = Y0 ∩ [2,∞). ∎
(The values at q = 0, 1 are prescribed by the seed and are not governed by the gates.)

## The shield (Li's Lemma 3.1, unchanged)
In ℤ/49: P = {7,14,28}, B = {3,22,32,40,48}, D = {1,2,5,13,27,36,47}, Q = P ∪ B.
 (cover)  (B+B) ∪ (P+B) ∪ (D+B) = ℤ/49 ∖ Q;
 (avoid)  Q ∩ ((B+B) ∪ (P+B) ∪ (D+B) ∪ (D+P)) = ∅;
 (PP)     (P+P) ∩ Q = P, and the only ordered pairs of P×P with sum in Q are 7+7=14, 14+14=28, 28+28≡7.
(Finite computation; recomputed from scratch in verify_closed_form.py.)

Define S = D ∪ {49q+b : q ≥ 0, b ∈ B} ∪ {49q+7 : q ∈ Y0} ∪ {49q+14 : q ∈ Y1} ∪ {49q+28 : q ∈ Y2}.
Then S ∩ [1,97] = D ∪ B ∪ (49+B) ∪ {7, 56} ∪ {63} ∪ {28} = A  (Y0 ∩ {0,1} = {0,1}, Y1 ∩ {0,1} = {1}, Y2 ∩ {0,1} = {0}).

**Theorem 3 (recurrence, rule Q).** For every t > 97: t ∈ S ⟺ t ∉ S ⊕ S.
Proof. Write t = 49q + r, 0 ≤ r < 49; t > 97 gives q ≥ 2.
Case r ∈ Q. Pair types D+D, D+B, D+P, B+B, B+P, P+P. A D+D sum is ≤ 94 < t. (avoid) excludes the next four types
from residues in Q, whether or not the summands are equal. Mixed P+P sums have residues 21, 35, 42 ∉ Q, so by (PP)
only the three diagonal pairs reach Q, and two distinct elements of one rail have distinct q:
 49q+14 ∈ S ⊕ S ⟺ q ∈ Y0 ⊕ Y0 ((49u+7)+(49v+7), u ≠ v);
 49q+28 ∈ S ⊕ S ⟺ q ∈ Y1 ⊕ Y1;
 49q+7  ∈ S ⊕ S ⟺ q − 1 ∈ Y2 ⊕ Y2 ((49u+28)+(49v+28) = 49(u+v+1)+7).
With Lemma 3 (q ≥ 2) every P-rail integer t > 97 is in S exactly when it is not in S ⊕ S. Every B-rail integer is in S,
and by (avoid) and (PP) it is not in S ⊕ S.
Case r ∉ Q. Then t ∉ S (its residue is on no rail; t > 97 > max D). By (cover) pick x ∈ B ∪ D ∪ P and b ∈ B with
x + b ≡ r (mod 49), and put e_x = x for x ∈ B ∪ D, e_7 = 7, e_14 = 63, e_28 = 28 — all elements of A ⊂ S. Write
e_x = 49u_x + x and x + b = 49c + r with u_x, c ∈ {0,1}. As q ≥ 2, the integer 49(q − u_x − c) + b is a positive element
of the b-rail, and t = e_x + (49(q−u_x−c)+b). The two summands are distinct: their residues are x and b, and
B, D, P are pairwise disjoint sets of residues, so equality forces x = b ∈ B, e_x = x ≤ 48, while the other summand is
≥ 49 + b > 48. Hence t ∈ S ⊕ S. ∎

By Lemma 1 (N = 97 ∈ S), the rule-Q extension of A is S.

**Lemma 4 (Li's Lemma 4.1).** If the gaps of an infinite T ⊆ ℕ are eventually periodic, the indicator of T is
ultimately periodic. (Proof in Li, §4: the period sum H is a membership period from t_K on.)

**Proof of Theorem 1.** 49q + 7 ∈ S ⟺ q ∈ Y0. Y0 contains the blocks I_k = [8^k+1, 2·8^k] (8^k consecutive members)
separated by [2·8^k + 1, 8^{k+1}] (6·8^k consecutive non-members). If the indicator of S were ultimately periodic
with period h, then 49h is also an ultimate period of it, and since 49(q+h)+7 = (49q+7) + 49h, h is an ultimate period
of the indicator of Y0; a run of ≥ h consecutive non-members inside the periodic tail forces that tail to be
identically 0, contradicting the later blocks. So the indicator of S
is not ultimately periodic, and by Lemma 4 the gap sequence is not eventually periodic. ∎

## The equal-rule controller (Theorem 2)
    Y0' = {0,1} ∪ ⋃_{k≥0} [2·8^k, 4·8^k − 1]      (I'_k; I'_0 = [2,3])
    Y1' = {1}   ∪ ⋃_{k≥1} [8^k − 1, 2·8^k − 1]     (J'_k)
    Y2' = {0}   ∪ ⋃_{k≥0} [4·8^k − 1, 8·8^k − 1]   (K'_k; K'_0 = [3,7])
Again Y0'∩{0,1} = {0,1}, Y1'∩{0,1} = {1}, Y2'∩{0,1} = {0}, so S' built from them has S' ∩ [1,97] = A.
**Lemma 2'.** (S0') Y0'+Y0' = [0,6] ∪ ⋃_{k≥1}[2·8^k, 8·8^k − 2];  (S1') Y1'+Y1' = {2} ∪ ⋃_{k≥1}[8^k, 4·8^k − 2];
(S2') Y2'+Y2' = {0} ∪ ⋃_{k≥0}[4·8^k − 1, 16·8^k − 2].
Proof. (S0') {0,1}+{0,1} = [0,2]; {0,1}+I'_k = [2·8^k, 4·8^k]; I'_k+I'_k = [4·8^k, 8·8^k−2]; I'_j+I'_k ⊆ [2·8^k+2, 4·8^k−1+4·8^{k−1}]
⊂ [2·8^k, 8·8^k−2] for j<k; the k = 0 pieces give [2,6]; 8·8^k − 2 < 2·8^{k+1}.
(S1') 1+1 = 2; 1+J'_k = [8^k, 2·8^k]; J'_k+J'_k = [2·8^k−2, 4·8^k−2]; J'_j+J'_k ⊆ [8^k+8^j−2, 2·8^k+2·8^j−2] ⊂ [8^k, 4·8^k−2]
(j ≥ 1); 4·8^k − 2 < 8^{k+1}.
(S2') 0+0 = 0; 0+K'_k = K'_k; K'_k+K'_k = [8·8^k−2, 16·8^k−2]; K'_j+K'_k ⊆ [4·8^k+4·8^j−2, 8·8^k+8·8^j−2] ⊂ [4·8^k−1, 16·8^k−2];
16·8^k − 2 < 4·8^{k+1} − 1. ∎
**Lemma 3' (gates, q ≥ 2).** ℕ_0∖(Y0'+Y0') = ⋃_{k≥1}[8^k−1, 2·8^k−1] = Y1'∩[2,∞); ℕ_0∖(Y1'+Y1') = {0,1} ∪ [3,7] ∪ ⋃_{k≥1}[4·8^k−1, 8·8^k−1],
which agrees with Y2' on [2,∞); ℕ_0∖(Y2'+Y2') = {1,2} ∪ ⋃_{k≥1}[2·8^k−1, 4·8^k−2], so q−1 lies in it (q ≥ 2) iff
q ∈ {2,3} ∪ ⋃_{k≥1}[2·8^k, 4·8^k−1] = Y0'∩[2,∞). ∎
Theorem 3' (t ∈ S' ⟺ t ∉ S'+S' for t > 97) is Li's proof verbatim (the distinctness remark is not needed), and
Theorem 2 follows as Theorem 1 did (Y0' has runs of 2·8^k members and 4·8^k non-members).

## Lemma 5 (the controller is forced by the seed; either rule)
Let R ⊆ {7, 56, 14, 63, 28, 77} contain at least one element of each rail, A_R = D ∪ B ∪ (49+B) ∪ R, and let S be the
greedy extension of A_R (rule Q, say). Then S = D ∪ {49q+b} ∪ {49q+7 : q ∈ Y0} ∪ {49q+14 : q ∈ Y1} ∪ {49q+28 : q ∈ Y2}
where Y_i ∩ {0,1} is read off R and, for q ≥ 2, Y1[q] = [q ∉ Y0 ⊕ Y0], Y2[q] = [q ∉ Y1 ⊕ Y1], Y0[q] = [q−1 ∉ Y2 ⊕ Y2]
(same with + for rule D).
Proof. Induction on t > 97: suppose S ∩ [1, t−1] has the stated shape. Write t = 49q + r, q ≥ 2. If r ∉ Q, (cover) gives
x ∈ B ∪ D ∪ P and b ∈ B with x + b ≡ r; R contains an element e_x = 49u_x + x of the x-rail with u_x ≤ 1 (for x ∈ B ∪ D take
e_x = x), so t = e_x + (49(q−u_x−c)+b) with both summands in S ∩ [1,t−1] and distinct (residue argument of Theorem 3): t is not
added. If r ∈ B, every pair summing to t is of a type excluded by (avoid)/(PP) or is a D+D sum ≤ 94: t is added. If r ∈ P,
the only pairs summing to t are the diagonal pairs on the previous rail, so t is added iff the gate condition holds.
Hence S ∩ [1, t] has the stated shape, with Y_i[q] given by the gates. ∎  (Theorem 3 is the special case where the gate
dynamics are the closed forms.)

## What the computer checked (all in ~/MathDyad/erdos341q/, logs in runs/)
1. verify_closed_form.py: from the closed forms alone, by FFT pair counts on [0, 8^7 = 2,097,152): the three gate
   identities hold for q ≥ 2 under the rule they are claimed for (0 violations each), FAIL under the other rule
   (7, 7, 6 violations), and FAIL when the start of the third block on any one rail is moved down by one (three mutations;
   the referee's own run moved every endpoint of every block k ≤ 3 by ±1 on both controllers — every non-vacuous mutation breaks a gate on [0, 8^5)); shield recomputed; S ∩ [1,97] = A;
   every t = 49q + r (r ∉ Q, 2 ≤ q < 60) has a cover pair of two distinct positive elements of S.
2. gates.py / census.c (two implementations of the forced rail dynamics, Python/numpy and C bitsets): from the seed's
   rail content for q ≤ 1 the dynamics reproduce the closed forms exactly (to 2^17 under both rules; to 2^20 under rule Q). Positive control
   (runs/control_li.log): Li's own rail content under rule D reproduces his Y0/Y1/Y2 with 0 mismatches to 32,768; under
   rule Q it is periodic with period 117 from q = 69.
3. greedy341.c (the 10-13 referee's independent bitset greedy on the integers, both rules) on A to 10^7:
   element-by-element equal to the closed-form S (rule Q) and S' (rule D) — see runs/gvc_*_1e7.log.
4. Census: of the 27 seeds D ∪ B ∪ (49+B) ∪ R with R ⊆ {7,56,14,63,28,77} hitting every rail at q ≤ 1 (the cover needs a
   representative on each rail), 18 show no period ≤ 8,192 on the quotient window [16,384, 32,768) under rule Q by the dynamics and 25 under rule D;
   Li's own R = {7,28,63,77} is periodic under rule Q (117). For all 27 the rail model agrees with greedy341 to 10^6 under
   rule Q (no such cross-check was run under rule D). ⚠ The window criterion is weak: on A itself the verdict hinges on a
   single quotient (16,385, the start of J_4, under rule Q; 32,767 under rule D) — a window missing a block boundary would
   read "period 1". The referee reproduced the counts with its own integer greedy, a different window ([10,204, 20,408),
   P ≤ 2,550) and both rules: the same 18 and 25 with the same per-seed periods. Only R = {7,28,56,63} is proved here; the
   others are computer observations with that bound.

## What is new, and what is not
- The shield mod 49, the three-rail scale-8 controller idea and Lemmas 1/4 are Li's. New: the strict-rule controller
  (Y0, Y1, Y2 above, with its proof), Lemma 5 (the controller is forced by the seed's rail content, so the greedy itself
  finds controllers), the seed A, and Theorem 2's second controller for rule D (a 21-element counterexample to #341 proper
  outside Li's family A_p, p ≥ 18, whose members have 7p − 20 ≥ 106 elements).
- Green (Jan 2026) lists the Queneau-variant periodicity question as open; van Berkel–Bosma (arXiv 2609.16843,
  2609.18522, Sep 2026) conjecture periodicity for strict 2-sumfree sequences with TWO-term starts S_{f,g} (and
  t-term starts for t-sumfree) — Theorem 1 does not touch those conjectures (our seed has 21 terms).
  Queneau 1972 and Finch 1992 concern two-term bases as described by van Berkel–Bosma (§2) and Green's references [119] (the
  primaries were not read here). Li's paper concerns rule D only. erdosproblems.com/341 shows only Li's claim (read
  2026-10-14 12:09Z via the Hetzner box; the HTML is in live/); #342 is Ulam's sequence (unique representation, i < j —
  Queneau's s = 1 sibling, cited by Green in the same paragraph), a different question.
