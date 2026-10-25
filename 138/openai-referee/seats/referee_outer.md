# Referee report — seat `outer` — §4 "An outer coloring of the labels" (04-outer.tex)

Paper: OpenAI, "Quantitative Superexponential Bounds for van der Waerden Numbers" (23 Sep 2026), sha256 042acea3…
Source read: `build/sections/04-outer.tex` (188 lines, read in full, every line), plus for the interface
`03-counting.tex` (Lemma count:global, Def. count:eligible, Lemma count:local), `02-setup.tex` (parameters, meshes)
and the two places §5 consumes the proposition (05-dichotomy.tex l.188–194 and l.295–307).
Printed numbering (PDF): §4 starts p. 9; **Lemma 4.1** = `outer:lll` (p. 10); **Proposition 4.2** = `outer:coloring` (p. 10,
proof pp. 10–12); equations (4.1) `outer:lll-condition`, (4.2) `outer:conditional`, (4.3) `outer:row-size`, (4.4) `outer:tail`,
(4.5) `outer:first-weight`, (4.6) `outer:second-weight`, (4.7) `outer:incident-weight`, (4.8) `outer:criterion` (p. 12),
(4.9) `outer:pullback` (p. 12).

## Verdict for scope

**HOLDS AS READ.** Lemma 4.1 and Proposition 4.2 are correct as written, conditional only on the two inputs from §3
(Lemma 3.2 `count:global`, Lemma 3.4 `count:local`), which are outside this seat and which I did not re-prove.
No FATAL, no GAP. Every inequality in the chain was re-derived by hand and the numerical ones were checked by
script with exact arithmetic or 60-digit arithmetic, each with a control that fails. The objections below are
COSMETIC / UNCLEAR (exposition only). Two informational findings matter to other seats: (a) §4 is robust to the exact
form of the §3 counts and states precisely what it needs from them (section "Interface"), and (b) the Lean does NOT
formalize the paper's (CDh)^{6D} / 9(3k²F+1)² counts; it uses (16005Dh)^{14D} / 16(3k²F+1)^6 from a different
(Sauer–Shelah) arrangement bound. §4's argument works with either, so this does not affect §4, but it means the Lean
certifies the theorem without certifying the paper's sharper §3 constants.

## Verification status (the deliverable)

| Item (TeX label / printed) | Status |
|---|---|
| Lemma `outer:lll` / Lemma 4.1 statement, hypotheses | VERIFIED LINE BY LINE |
| (4.1) `outer:lll-condition` | VERIFIED |
| Proof: induction (4.2) `outer:conditional`, positivity step, T1/T2 split, chain rule for P(A_{T1}∣A_{T2}), "independence from T_2 in the numerator", final inequality | VERIFIED LINE BY LINE (+ exhaustive brute force on 226 random instances, every subset T) |
| Prop `outer:coloring` / Prop 4.2 statement (i),(ii), "threshold absolute" | VERIFIED LINE BY LINE |
| First family: word-indexed events, grouping, cyclic dealing into w_max rows, "a label occurs at most once in each row" | VERIFIED LINE BY LINE (+ brute force, 3898 words) |
| (4.3) `outer:row-size` ⌊L_0/w_max⌋ ≥ δM − 1 | VERIFIED |
| Count of first-family events ≤ kT_glob | VERIFIED |
| Events are functions of the ξ_β only (word fixes light/heavy and the rows) | VERIFIED |
| Second family: one event per (eligible pattern, h, t), l(E) = #regular positions ≥ h/2, finiteness | VERIFIED |
| cosh moment identity, cosh t ≤ e^{t²/2} via (2j)! ≥ 2^j j!, Markov | VERIFIED LINE BY LINE (+ exact) |
| (4.4) `outer:tail` and the strict/weak remark | VERIFIED (+ exact binomial tails l ≤ 600) |
| Weights z_E = e^{−l(E)/32} | VERIFIED |
| (4.5) `outer:first-weight` | VERIFIED given Lemma 3.2 (threshold computed from the paper's displayed bounds: k ≥ 10^23) |
| (4.6) `outer:second-weight`, decreasing claim, sup ≤ 6 log(CD³)/D, "each summand ≤ e^{−h/128}", tail | VERIFIED given Lemma 3.4 (threshold of the text's route: D ≥ 29,210, k ≳ 10^44.7) |
| (4.7) `outer:incident-weight`, uniformity in β | VERIFIED |
| Dependency graph and its compatibility with Lemma 4.1's hypothesis | VERIFIED |
| Σ_{F∈Γ(E)} z_F ≤ l(E)/500 (double counting direction) | VERIFIED (+ brute force) |
| l(E) ≥ 100 eventually; z_E < 1/2; log(1 − z) ≥ −2z on [0,1/2] | VERIFIED |
| (4.8) `outer:criterion`; "1/8 − 1/32 − 2/500 multiplied by 100 exceeds log 2" | VERIFIED (exact rational certificate) |
| Conclusion (i) by summing rows; (ii) | VERIFIED |
| (4.9) `outer:pullback` | definition; nothing to verify |
| Lemma 3.2 `count:global`, Def. 3.3 `count:eligible`, Lemma 3.4 `count:local` (inputs) | SKIMMED (read in full for the interface; not re-proved — other seats) |

## Objections

**O1 — COSMETIC (exposition). Cross-references print the wrong theorem-environment name throughout.**
Location: Prop 4.2 (ii) and the proof, pp. 10–12 (also §5 and §6). TeX: "`\item In every eligible recorded pattern of \Cref{count:eligible},`"
prints as "(ii) In every eligible recorded pattern of **Theorem 3.3**", but 3.3 is **Definition** 3.3 (p. 8 heading:
"Definition 3.3 (Eligible local patterns)"). Likewise "`where $T_{\mathrm{glob}}$ is the number in \Cref{count:global}`" prints
"Theorem 3.2" (it is Lemma 3.2); "`\Cref{count:local} bounds the second-family weight`" prints "Theorem 3.4" (Lemma 3.4);
"`a dependency graph of the kind required in \Cref{outer:lll}`" prints "Theorem 4.1" (Lemma 4.1); §5 cites "Theorem 4.2(i)" for
Proposition 4.2. Every \Cref in the paper renders as "Theorem" (shared-counter cleveref misconfiguration). Mathematically
harmless; a reader hunting "Theorem 3.3" will not find it. Fix: `\crefname{lemma}{Lemma}{Lemmas}` etc. for each environment.

**O2 — UNCLEAR (exposition, not proof). The event family is an indexed family with repeated events; "distinct" must mean distinct indices.**
TeX: "`take one event for each eligible recorded pattern and its discrete parameters $h,t$`" and "`Join two distinct events
whenever their supports share a label variable.`" The second-family event depends only on the recorded word (its regular
positions are its non-`*` entries), so one word eligible for several t yields several identical events; similarly one row
of labels can arise from several words in the first family. If "two distinct events" were read as "two distinct subsets
of the sample space", identical copies would be declared non-adjacent although they are obviously dependent, and the
hypothesis of Lemma 4.1 ("each $E$ is independent of the sigma-algebra generated by the events outside $\{E\}\cup\Gamma(E)$")
would fail. The intended reading — distinct *members* of the indexed family — is correct, and all event counts used
(≤ kT_glob; ≤ (CDh)^{6D} per label and h) are upper bounds under either convention (merging duplicates only lowers them).
The Lean takes the index reading (`outerNeighbors … filter fun j => j ≠ i ∧ ¬ Disjoint (support i) (support j)`,
OuterColoring.lean). Fix: "two distinct members of the family".

**O3 — COSMETIC. "Its tail tends to zero as $D\to\infty$."** (p. 11, after (4.6).) The antecedent of "Its" is
"the infinite sum in (4.6)"; what is meant is the bound Σ_{h>D²} e^{−h/128} ≤ e^{−(D²+1)/128}/(1−e^{−1/128}) → 0, a
tail whose starting index moves with D. Correct; the phrase is loose. Also implicit (correct): the passage from
"sup ≤ 6 log(CD³)/D = o(1)" to "each summand … at most e^{−h/128}" is exactly the requirement 6 log(CD³)/D ≤ 1/128.

**O4 — COSMETIC / informational. Size of the thresholds hidden in "for all sufficiently large $k$".**
Not an error — the paper only ever claims "an absolute integer $K_0$" and never a value. Measured from the paper's own
displayed bounds (scripts below): (4.5) ≤ 1/1000 from k = 10^23 on (log T_glob ≤ 2D[log 9 + 2 log(3k²F+1)],
log λ ≤ D² log 2M); the text's route for (4.6) ("each summand ≤ e^{−h/128}", i.e. 6 log(CD³)/D ≤ 1/128) needs
D ≥ 29,210, i.e. k ≳ 10^44.7, with C = (9·16005²)^{1/3} ≈ 1321 extracted from the proof of Lemma 3.4
(C_0 = 9·16005² since 9(16004Dh+1)² ≤ 9·16005²(Dh)²; C_0^{2D}D^{4D}h^{5D+1} ≤ (C_0^{1/3}Dh)^{6D}); summing the series
directly instead lowers this to D ≥ 13,736, k ≳ 10^41.4. So the proof's K_0 is at least of order 10^41 from §4 alone.
Nobody should quote a "reasonable" K_0 for Theorem 1.1 on the strength of this proof.

No other objections. I specifically looked for, and did not find: a reversed inequality, a probability treated as exact
that is approximate, an o(1) depending on β or on the progression, a threshold depending on r, q, λ or β, a lemma used
outside its hypotheses, or a strict/weak boundary mishandled.

## Line-by-line notes (what I checked and how)

**Lemma 4.1 (`outer:lll`).** Hypothesis "each $E$ is independent of the sigma-algebra generated by the events outside
$\{E\}\cup\Gamma(E)$" is the standard mutual-independence hypothesis. Induction claim (4.2): P(A_T) > 0 and
P(E∣A_T) ≤ z_E for E ∉ T. Base T = ∅: A_∅ = Ω, P(E) ≤ z_E∏(1−z_F) ≤ z_E since 1 − z_F ∈ (0,1). Positivity step:
"$\Pp(A_T)=\Pp(A_{T\setminus\{F\}})\bigl(1-\Pp(F\mid A_{T\setminus\{F\}})\bigr)>0$" — uses the IH at T∖{F} (size |T|−1,
F ∉ T∖{F}) and z_F < 1; needs T ≠ ∅ (it is, in the inductive step). Conditional step, T_1 = T ∩ Γ(E), T_2 = T∖T_1:
if T_1 = ∅ then T ⊆ ℰ∖({E}∪Γ(E)) (because E ∉ T), A_T lies in the generated sigma-algebra, and P(A_T) > 0 was just
shown, so P(E∣A_T) = P(E). Otherwise P(A_{T_1}∣A_{T_2}) = ∏_i (1 − P(F_i ∣ A_{T_2 ∪ {F_1..F_{i−1}}})) with each
conditioning set of size ≤ |T|−1 and not containing F_i, so the IH gives ≥ ∏_{T_1}(1−z_F); positivity of every
A_{T_2 ∪ …} also comes from the IH. Then P(E∣A_T) = P(E∩A_{T_1}∩A_{T_2})/P(A_T) ≤ P(E∩A_{T_2})/P(A_T)
= P(E∣A_{T_2})/P(A_{T_1}∣A_{T_2}). **"Using independence from $T_2$ in the numerator"**: T_2 = T∖Γ(E) and E ∉ T, so
T_2 ⊆ ℰ∖({E}∪Γ(E)) and A_{T_2} belongs to exactly the sigma-algebra in the hypothesis; P(E∣A_{T_2}) = P(E). This is the
right sigma-algebra statement. Last step: P(E)/∏_{T_1}(1−z_F) ≤ z_E∏_{Γ(E)∖T_1}(1−z_F) ≤ z_E. Correct. (The Lean,
FiniteLocalLemma.lean `positive_and_conditional_bound`, proves the same induction under the weaker hypothesis
P(bad i ∩ avoid T) = P(bad i)P(avoid T) for T disjoint from neighbors(i) ∪ {i}; the paper's hypothesis implies it.)

**First family.** Words are fixed (they come from L and the progressions, before any randomness); light/heavy is the
multiplicity in the word; "`with all choices fixed as functions of the word`" makes each row a deterministic label set,
so each row event is a function of (ξ_β)_{β in the row} only. A group of equal light labels has ≤ w_max members and is
contiguous in the ordered list; dealing the list cyclically into w_max rows (index p ↦ row p mod w_max) sends a run of
length ≤ w_max to distinct rows — "a label occurs at most once in each row" holds. Row sizes are ⌊L_0/w_max⌋ or
⌈L_0/w_max⌉, and L_0/w_max ≥ δk/(k/M) = δM, so the minimum is ≥ ⌊δM⌋ ≥ δM − 1 ((4.3); true for every k, no largeness).
Rows partition the light positions; positions ↔ labels bijectively inside a row, so l(E) = row size. Number of rows per
word is w_max ≤ k/M < k and the number of words is T_glob (same population: words of progressions with d ≠ 0), so ≤ kT_glob
events. Brute force (rows.py) confirms all four properties on 3898 random words, and that dealing into w_max − 1 rows or
skipping the grouping produces repeats (controls).

**Second family.** Index set = {(h, t, w) : h_0 < h ≤ 2M, t ∈ {0..h−1}^D, w ∈ (𝓛∪{*})^h eligible for h,t}: finite.
Regular positions = non-`*` entries of w; by Def. 3.3(i) their labels are pairwise distinct and there are ≥ h/2 of them,
so l(E) ≥ h/2 > D²/2 and the event is a function of the ξ_β at those labels. "Uses ξ_β" ⟺ β occurs in w ⟺ "eligible
pattern … containing β" in Lemma 3.4 — the counted object matches.

**Tail (4.4).** X − l/2 = Σ(ξ_i − 1/2) with ξ_i − 1/2 = ±1/2, so E e^{±(X−l/2)} = cosh(1/2)^l exactly; cosh t =
Σ t^{2j}/(2j)! ≤ Σ t^{2j}/(2^j j!) = e^{t²/2} termwise since (2j)! = ∏_{i≤2j} i ≥ ∏_{i≤j}(2i) = 2^j j!. Markov:
P(X − l/2 ≥ l/4) ≤ e^{−l/4}cosh(1/2)^l ≤ e^{−l/8}, same for the lower tail. Bad event = {X < l/4} ∪ {l − X < l/4}
⊆ {X − l/2 ≤ −l/4} ∪ {X − l/2 ≥ l/4}: "`The weak tail inequalities also cover the strict inequalities`" is right
(and the weak event is strictly larger exactly when 4 | l — tail.py lists l = 4, 8, …, 40). Exact tails for l ≤ 600:
max ratio (weak tail)/(2e^{−l/8}) = 0.5666 at l = 1, never > 1.

**Weights and (4.5).** z_E = e^{−l/32} is decreasing in l, so every first-family event has z_E ≤ e^{−(δM−1)/32} and the
total is ≤ kT_glob e^{−(δM−1)/32}. log of it = log k + O(k^{3/10} log k) − k^{1/2}/320 + O(1) → −∞. Using the paper's
displayed bound it is ≤ log(1/1000) from k = 10^23 and stays so through 10^259 (first_weight.py). Control: rows of size
δk^{1/4} (or D = k^{1/5}) never reach the budget — the comparison k^{3/10} log k ≪ k^{1/2} is load-bearing and holds.

**(4.6).** Per event weight ≤ e^{−h/64} (l ≥ h/2); per (β, h) at most (CDh)^{6D} events (Lemma 3.4, uniform in β, q, λ, D).
Extending to all h > D² only adds nonnegative terms (the infinite series converges for each D). "`take $C\ge1$`" is
harmless (the bound is monotone in C). f(h) = log(CDh)/h has f′ = (1 − log(CDh))/h² ≤ 0 iff CDh ≥ e; for h ≥ D², C ≥ 1
this holds once D ≥ 2 (D³ ≥ 8 > e) — "decreasing for h ≥ D² once D is large" is correct. Hence sup_{h>D²} 6D log(CDh)/h
≤ 6D log(CD·D²)/D² = 6 log(CD³)/D → 0. Each summand = exp(h[6D log(CDh)/h − 1/64]) ≤ exp(−h/128) once
6 log(CD³)/D ≤ 1/128; then Σ_{h>D²} ≤ e^{−(D²+1)/128}/(1 − e^{−1/128}) → 0. All verified (decreasing.py), with controls
(C = 1, D = 1 and C = 0.1, D = 2 are not decreasing from h = D²; at D = 1000 the summand bound fails by e^{1.6·10^5};
replacing h > D² by h > D the sup bound fails — the D² separation from Lemma 2.1 is load-bearing).

**(4.7), graph, double counting.** Σ_{E uses ξ_β} z_E ≤ (total first-family weight) + (per-β second-family weight)
→ 0 uniformly in β, so ≤ 1/500 eventually. Events outside {E}∪Γ(E) have supports disjoint from S(E), hence generate a
sub-sigma-algebra of σ(ξ_β : β ∉ S(E)), independent of σ(ξ_β : β ∈ S(E)) ∋ E: Lemma 4.1's hypothesis holds.
Σ_{F∈Γ(E)} z_F ≤ Σ_{β∈S(E)} Σ_{F∋β} z_F ≤ l(E)/500 — every neighbor is counted at least once on the right (overcounting,
and including E itself, only increases the right side): correct direction (brute-forced in lll_bruteforce.py; the reverse
inequality fails on a 2-label example — control).

**l(E) ≥ 100, (4.8).** δM − 1 ≥ 100 for k > 1009² and h/2 ≥ (D²+1)/2 ≥ 100 for D ≥ 15. z_E ≤ e^{−100/32} ≈ 0.0439 < 1/2.
log(1−z) + 2z is 0 at 0 with derivative 2 − 1/(1−z) ≥ 0 on [0,1/2]: log(1−z) ≥ −2z there. So
z_E∏(1−z_F) ≥ exp(−l/32 − 2Σz_F) ≥ exp(−(1/32 + 2/500)l). 1/8 − 1/32 − 2/500 = 359/4000 exactly; ×100 = 359/40 = 8.975;
e^{359/40} ≥ 1 + 359/40 = 399/40 > 2 (rational certificate), so exp(−(1/32+2/500)l) ≥ 2e^{−l/8} for l ≥ 100 (in fact
for l ≥ 8). At l = 100 the margin is a factor 3951.5. (4.8) is exactly what Lemma 4.1 needs.

**Conclusion.** (i): for a progression with ≥ δk light positions its word is in the first family; each row has each bit on
≥ 1/4 of its positions; rows partition the light positions; summing gives each bit on ≥ L_0/4 light positions (§5 uses
L_0/4 ≥ δk/4 = k/40 ≥ γk). (ii): directly from the second family. "Threshold absolute": every threshold above is a
condition on k alone with absolute constants (list below). No r anywhere in §4.

## "Sufficiently large k" inventory for §4 (brief item (e))

Finite list; each is a condition on k alone with absolute constants; each holds for all large k with the stated parameters
(no reversed inequality):

| # | Where | Inequality needed | Holds? |
|---|---|---|---|
| S1 | (4.3) | ⌊L_0/w_max⌋ ≥ δM − 1 | every k (no largeness needed) given L_0 ≥ δk, w_max ≤ k/M |
| S2 | rows nonempty | δM ≥ 1 | k ≥ 100 |
| S3 | "l(E) ≥ 100 eventually" | δM − 1 ≥ 100 and (D²+1)/2 ≥ 100 | k > 1009², and D ≥ 15 (k > 14^10 ≈ 2.9·10^11) |
| S4 | (4.5) | k T_glob e^{−(δM−1)/32} ≤ 1/1000 | log T_glob = O(D(log k + D² log 2M)) = O(k^{3/10} log k) = o(k^{1/2}); from the displayed bounds, k ≥ 10^23 |
| S5 | decreasing claim | log(CD³) ≥ 1 with C ≥ 1 | D ≥ 2 |
| S6 | "each summand ≤ e^{−h/128}" | 6 log(CD³)/D ≤ 1/128 | D ≥ 29,210 for C ≈ 1321 (k ≳ 10^44.7); D ≥ 23,156 for C = 1 |
| S7 | tail | e^{−(D²+1)/128}/(1−e^{−1/128}) ≤ 1/1000 | D ≥ 39 |
| S8 | (4.7) | S4 + S6/S7 total ≤ 1/500 | yes, from the larger of S4, S6 |
| S9 | (4.8) | (359/4000)·l ≥ log 2 | every l ≥ 8, in particular l ≥ 100 (no k-dependence) |

## Interface: what §4 actually needs from §3 (robustness; relevant to brief item (a))

§4 uses Lemma 3.2 and Lemma 3.4 only through:
1. **Global:** log T_glob ≤ (δM − 1)/32 − log k − log 1000, i.e. log T_glob ≤ k^{1/2}/320 − O(log k).
2. **Local:** with N_h(β) = #{(t, eligible pattern for h,t containing β)}, Σ_{D² < h ≤ 2M} N_h(β) e^{−h/64} ≤ 1/1000
   uniformly in β. Sufficient: log N_h(β) ≤ h/128 for all h > D² (uniformly in β); because h > D², it is also enough
   that log N_h(β) ≤ D²/65 uniformly in h and β (then the sum is ≤ e^{D²/65}·e^{−(D²+1)/64}/(1−e^{−1/64}) ≤ 65·e^{−D²/4160} → 0).

Consequences: (a) any bound of the shape (CDh)^{aD} works for any fixed a (the Lean's 14D does); (b) count:local could
even lose a factor exp(o(D²)) — e.g. |V|^{O(D)} = exp(O(k^{1/10} log k)) — without harming §4; (c) but a factor
λ^{Ω(D)} (log λ ≥ θ(D²) ~ D² because every prime ℓ ≤ D² < 2M divides λ, so log λ^{D} ≳ D³ ≫ D²) or a factor
depending on the anchor width such as |I|/α for even one coordinate (|I|/α ≤ 2Hq^{D+1}, log ≈ (D+1) log q ≈ c k log k ≫ 2M)
would break (4.6). So the brief's point (a) is confirmed from the §4 side: the
weights sum to o(1) **only because** Lemma 3.4's bound is independent of q, λ and the anchor width (up to exp(o(D²))).
Whether Lemma 3.4 really delivers that is the counting seat's question; §4 uses it correctly.

## Prove-too-much / role of c (brief item (j)) and quantifiers (item (i))

§4 imposes on the parameters only D³ log M = o(M) (i.e. D ≪ k^{1/6}/polylog) and D log(CD³) = o(D²) (D → ∞).
The exponent c enters §4 only through q, hence through log|V| = log(2m) = O(log k + log log q): §4 would be unaffected
by c = 1 or larger. §4 does not cap c; the cap must come from §6 (2c − γ/80 < 0), not here. No quantity in §4
depends on r; K_0's §4 part is uniform in r, q, λ, β and in the choice of the prime P. §4 claims nothing beyond
Prop 4.2 — nothing is overclaimed.

## Lean cross-reference (read as text only; nothing run)

- `FiniteLocalLemma.lean`: `positive_and_conditional_bound` / `finite_asymmetric_local_lemma` — same induction, same
  S = T∖Γ(i), U = T∩Γ(i) split; independence hypothesis stated only for "avoid" events (weaker than the paper's, implied by it).
- `OuterColoring.lean`: `outer_log_one_sub_lower` (log(1−z) ≥ −2z on [0,1/2]), `outer_local_criterion` (hypotheses
  100 ≤ l, z ≤ 1/2, Σz ≤ l/500 ⇒ 2e^{−l/8} ≤ e^{−l/32}∏(1−z)) = (4.8) verbatim; `outer_neighbor_weight_bound` = the
  double counting; `outerNeighbors` indexes by `j ≠ i` (cf. O2). `FairBitTail.lean` `balancing_tail` ≤ 2exp(−|S|/8) = (4.4).
- `OuterBudget.lean` / `UniformBudget.lean`: the incident budget is proved with row envelope exp(…k^{3/10}log k −
  k^{1/2}/320) — i.e. rows of size cutoff/10 − 1 = δM − 1, matching (4.3)/(4.5) — and with local term
  `(16005 * D * h) ^ (14 * D)` (EligiblePatternTests.lean:171, LabelIncidences.lean:84), global base
  `(16 * (3 * k ^ 2 * F + 1) ^ 6) ^ (2 * D)`, coming from `Arrangement.lean:225-227`
  `(realizedSigns forms D).card ≤ (e + 2) ^ 2 * (s + 1) ^ (2 * (e + 1))` (Sauer–Shelah), **not** the paper's
  (e+1)²(s+1)^e / 9(3k²F+1)² / (CDh)^{6D}. Comment in UniformBudget.lean: "Any fixed polynomial exponent is allowed;
  in particular this includes the proved `14D` pattern bound." **Flag for the counting seat:** the Lean does not certify
  Lemma 3.1's bound (e+1)²(s+1)^e or Lemma 3.4's exponent 6D as stated; it certifies weaker ones that suffice. For §4
  this is immaterial (Interface (a)).

## Finite checks (all under /tmp/oaimath/160/seats/outer_checks/; each < 10 s, < 35 MB RSS)

Run as `python3 <script>.py` (mpmath 1.3.0, Python 3.12.3). Every check prints its controls; each control FAILS as required.

### lll_bruteforce.py

Lemma 4.1 exhaustively on random small product spaces (exact Fractions): for every instance satisfying (4.1) with the share-a-variable graph, the invariant (4.2) is checked for EVERY subset T and every E ∉ T; plus the double-counting step. Controls: same verifier with the edgeless (wrong) dependency graph; the two-point example; reverse double counting.

```python
# Exhaustive check of Lemma outer:lll (finite asymmetric LLL) on random small
# product spaces of fair bits, exact Fraction arithmetic. For every instance whose
# z-weights satisfy (outer:lll-condition) for the "share a variable" dependency graph,
# verify the induction invariant (outer:conditional) for EVERY T subset of the family and
# every E not in T (this exercises the T1/T2 split and "independence from T_2"), hence
# P(intersection of complements) > 0.  Also checks the double-counting step
#   sum_{F in Gamma(E)} z_F <= |S(E)| * max_beta sum_{F uses beta} z_F.
# CONTROLS run through the SAME verifier with a mutant (too sparse) dependency graph.
import random, itertools, sys
from fractions import Fraction as Fr

def build(n, m, rng):
    outcomes = list(itertools.product((0,1), repeat=n))
    events = []
    for _ in range(m):
        s = sorted(rng.sample(range(n), rng.randint(1, min(4, n))))
        pats = list(itertools.product((0,1), repeat=len(s)))
        bad = set(rng.sample(pats, rng.randint(1, max(1, len(pats)//3))))
        events.append((s, frozenset(i for i,w in enumerate(outcomes) if tuple(w[j] for j in s) in bad)))
    return len(outcomes), events

def share_graph(events):
    m = len(events)
    return [[f for f in range(m) if f != e and set(events[e][0]) & set(events[f][0])] for e in range(m)]

def criterion(N, events, nb, z):
    for e in range(len(events)):
        prod = Fr(1)
        for f in nb[e]: prod *= (1 - z[f])
        if not Fr(len(events[e][1]), N) <= z[e]*prod: return False
    return True

def invariant(N, events, z):
    """returns None if (outer:conditional) holds for all T, else a witness"""
    m = len(events); allw = frozenset(range(N))
    for r in range(m+1):
        for T in itertools.combinations(range(m), r):
            A = allw
            for f in T: A = A - events[f][1]
            if not len(A) > 0: return ('P(A_T)=0', T)
            for e in range(m):
                if e in T: continue
                if not Fr(len(events[e][1] & A), len(A)) <= z[e]: return ('P(E|A_T)>z_E', T, e)
    return None

def choose_z(N, events, nb):
    for mult in (Fr(3,2), Fr(2), Fr(3)):
        z = [min(Fr(9,10), mult*Fr(len(ev[1]), N) + Fr(1,1000)) for ev in events]
        if criterion(N, events, nb, z): return z
    return None

def main():
    rng = random.Random(1)
    held = nocrit = 0
    for it in range(1500):
        N, events = build(rng.randint(3, 8), rng.randint(2, 6), rng)
        nb = share_graph(events)
        z = choose_z(N, events, nb)
        if z is None: nocrit += 1; continue
        w = invariant(N, events, z)
        if w is not None: print('LEMMA VIOLATION', w); return 1
        n = 1 + max(max(ev[0]) for ev in events)
        B = max(sum((z[f] for f in range(len(events)) if b in events[f][0]), Fr(0)) for b in range(n))
        for e in range(len(events)):
            if not sum((z[f] for f in nb[e]), Fr(0)) <= len(events[e][0])*B:
                print('DOUBLE-COUNT VIOLATION', e); return 1
        held += 1
    print(f'correct graph: {held} instances satisfied the criterion, invariant held in all; {nocrit} had no admissible z')
    # CONTROL A (must FAIL): same verifier, MUTANT graph with all edges deleted
    # (independence hypothesis of outer:lll is then false).
    rng = random.Random(2); fails = tried = 0; first = None
    for it in range(3000):
        N, events = build(rng.randint(2, 5), rng.randint(2, 6), rng)
        nb0 = [[] for _ in events]
        z = choose_z(N, events, nb0)
        if z is None: continue
        tried += 1
        w = invariant(N, events, z)
        if w is not None:
            fails += 1
            if first is None: first = (w, [(ev[0], sorted(ev[1])) for ev in events])
    print(f'CONTROL A (edgeless mutant graph): criterion held in {tried} instances, invariant/conclusion FAILED in {fails}')
    print('  first failing instance:', first)
    # CONTROL B (must FAIL): the textbook two-point example through the same verifier.
    events = [([0], frozenset([0])), ([0], frozenset([1]))]   # Omega={0,1}: E={0}, F={1}
    z = [Fr(3,5), Fr(3,5)]
    print('CONTROL B: mutant graph criterion', criterion(2, events, [[],[]], z),
          '| invariant witness', invariant(2, events, z),
          '| true graph criterion', criterion(2, events, share_graph(events), z))
    return 0
sys.exit(main())
```

Output:

```
correct graph: 226 instances satisfied the criterion, invariant held in all; 1274 had no admissible z
CONTROL A (edgeless mutant graph): criterion held in 3000 instances, invariant/conclusion FAILED in 1945
  first failing instance: (('P(E|A_T)>z_E', (1,), 3), [([2, 3, 4], [0, 6, 8, 14, 16, 22, 24, 30]), ([2], [4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31]), ([0, 1, 2, 3], [0, 1, 14, 15]), ([1, 2], [8, 9, 10, 11, 24, 25, 26, 27]), ([3, 4], [2, 6, 10, 14, 18, 22, 26, 30]), ([1, 3, 4], [3, 7, 11, 15, 19, 23, 27, 31])])
CONTROL B: mutant graph criterion True | invariant witness ('P(E|A_T)>z_E', (0,), 1) | true graph criterion False
[wall 1.01 s, maxrss 12740 KB, exit 0]
```

### tail.py

(4.4): exact binomial tails vs 2e^{-l/8} for l = 1..600; moment identity; cosh(1/2) ≤ e^{1/8}; (2j)! ≥ 2^j j!; strict vs weak remark. Controls: 2e^{-l/7}, e^{1/9}, 3^j j!, reversed remark.

```python
# Check (outer:tail): for X ~ Bin(l,1/2), the bad event "some bit on strictly fewer than
# l/4 of l positions" = {X < l/4} U {l-X < l/4}; paper bounds it by the WEAK tails
# P(X-l/2 <= -l/4) + P(X-l/2 >= l/4) <= 2 e^{-l/8}.  Exact binomial tails (Fraction),
# exp via mpmath at 60 digits. Also checks E e^{+-(X-l/2)} = cosh(1/2)^l, cosh(1/2)<=e^{1/8},
# and (2j)! >= 2^j j!.
import sys, math
from fractions import Fraction as Fr
import mpmath as mp
mp.mp.dps = 60

def tails(l):
    tot = 2**l
    weak = sum(math.comb(l, j) for j in range(l+1) if 4*j <= l or 4*j >= 3*l)     # X<=l/4 or X>=3l/4
    strict = sum(math.comb(l, j) for j in range(l+1) if 4*j < l or 4*(l-j) < l)   # X<l/4 or l-X<l/4
    return Fr(strict, tot), Fr(weak, tot)

def check(bound_exp_den, L=600):
    worst = (0, None); first_fail = None
    for l in range(1, L+1):
        s, w = tails(l)
        assert s <= w
        b = 2*mp.e**(-mp.mpf(l)/bound_exp_den)
        r = mp.mpf(w.numerator)/w.denominator/b
        if r > worst[0]: worst = (r, l)
        if r > 1 and first_fail is None: first_fail = l
    return worst, first_fail

def main():
    worst, ff = check(8)
    print('claim  P <= 2e^{-l/8}, l=1..600: max ratio weak_tail/bound = %s at l=%d; first failure: %s'
          % (mp.nstr(worst[0], 8), worst[1], ff))
    # moment identity and cosh bound
    for l in (1, 2, 5, 17, 40):
        lhs = mp.fsum(mp.binomial(l, j)*mp.mpf(2)**(-l)*mp.e**(j - mp.mpf(l)/2) for j in range(l+1))
        lhs2 = mp.fsum(mp.binomial(l, j)*mp.mpf(2)**(-l)*mp.e**(-(j - mp.mpf(l)/2)) for j in range(l+1))
        assert abs(lhs - mp.cosh(0.5)**l) < mp.mpf(10)**-50 and abs(lhs2 - mp.cosh(0.5)**l) < mp.mpf(10)**-50
    print('E e^{+-(X-l/2)} = cosh(1/2)^l verified for l in (1,2,5,17,40) to 1e-50')
    print('cosh(1/2) =', mp.nstr(mp.cosh(0.5), 15), '<= e^{1/8} =', mp.nstr(mp.e**(mp.mpf(1)/8), 15), ':', mp.cosh(0.5) <= mp.e**(mp.mpf(1)/8))
    assert all(math.factorial(2*j) >= 2**j*math.factorial(j) for j in range(0, 300))
    print('(2j)! >= 2^j j! for j = 0..299: True')
    # strict vs weak: weak strictly larger exactly when some j hits l/4 or 3l/4 (4 | l)
    diff = [l for l in range(1, 41) if tails(l)[0] != tails(l)[1]]
    print('l in 1..40 where weak tail != strict tail:', diff)
    print('--- CONTROLS (each must FAIL) ---')
    worst7, ff7 = check(7)
    print('CONTROL claim P <= 2e^{-l/7}: first l where exact weak tail exceeds it =', ff7, '(max ratio %s at l=%d)' % (mp.nstr(worst7[0], 6), worst7[1]))
    print('CONTROL cosh(1/2) <= e^{1/9}:', mp.cosh(0.5) <= mp.e**(mp.mpf(1)/9))
    print('CONTROL (2j)! >= 3^j j! at j=1:', math.factorial(2) >= 3*math.factorial(1))
    print('CONTROL "weak tail <= strict tail" (reverse of the paper remark) at l=4:', tails(4)[1] <= tails(4)[0])
    kl = 0.75*math.log(1.5) + 0.25*math.log(0.5)
    print('true large-deviation rate KL(3/4||1/2) = %.6f  (> 1/8 = 0.125, < 1/7 = %.6f)' % (kl, 1/7))
    return 0
sys.exit(main())
```

Output:

```
claim  P <= 2e^{-l/8}, l=1..600: max ratio weak_tail/bound = 0.56657423 at l=1; first failure: None
E e^{+-(X-l/2)} = cosh(1/2)^l verified for l in (1,2,5,17,40) to 1e-50
cosh(1/2) = 1.12762596520638 <= e^{1/8} = 1.13314845306683 : True
(2j)! >= 2^j j! for j = 0..299: True
l in 1..40 where weak tail != strict tail: [4, 8, 12, 16, 20, 24, 28, 32, 36, 40]
--- CONTROLS (each must FAIL) ---
CONTROL claim P <= 2e^{-l/7}: first l where exact weak tail exceeds it = 196 (max ratio 77.3421 at l=600)
CONTROL cosh(1/2) <= e^{1/9}: False
CONTROL (2j)! >= 3^j j! at j=1: False
CONTROL "weak tail <= strict tail" (reverse of the paper remark) at l=4: False
true large-deviation rate KL(3/4||1/2) = 0.130812  (> 1/8 = 0.125, < 1/7 = 0.142857)
[wall 1.28 s, maxrss 15792 KB, exit 0]
```

### criterion.py

(4.8) with exact rational arithmetic (359/4000; certificate e^{359/40} ≥ 399/40 > 2) and 60-digit checks; log(1−z) ≥ −2z; worst-case product. Controls: l = 7, incident weight 1/20, z = 0.8.

```python
# Check (outer:criterion): for l >= 100, given sum_{F in Gamma(E)} z_F <= l/500 and every z_F <= 1/2,
#   z_E prod (1-z_F) >= exp(-(1/32+2/500) l) >= 2 e^{-l/8},   z_E = e^{-l/32}.
# Exact rational part with Fraction; transcendental part with a rational certificate
# (e^x >= 1+x) and with mpmath at 60 digits.
import sys
from fractions import Fraction as Fr
import mpmath as mp
mp.mp.dps = 60

def margin(a_inc):
    # positive difference 1/8 - 1/32 - 2*a_inc  (a_inc = per-label incident weight bound)
    return Fr(1,8) - Fr(1,32) - 2*a_inc

def crit_holds(l, a_inc):
    # exp(-(1/32+2a)l) >= 2 e^{-l/8}  <=>  margin*l >= log 2
    return mp.mpf(margin(a_inc).numerator)/margin(a_inc).denominator*l >= mp.log(2)

def main():
    d = margin(Fr(1,500))
    print('1/8 - 1/32 - 2/500 =', d, '=', float(d), '; times 100 =', d*100)
    # rational certificate: e^{359/40} >= 1 + 359/40 > 2  => log 2 < 359/40
    cert = 1 + d*100
    print('certificate 1 + 100*margin =', cert, '> 2 :', cert > 2, '  (e^x >= 1+x)')
    l = 100
    lhs = mp.e**(-(mp.mpf(1)/32 + mp.mpf(2)/500)*l)
    rhs = 2*mp.e**(-mp.mpf(l)/8)
    print('l=100: exp(-(1/32+2/500)l) = %s ; 2e^{-l/8} = %s ; ratio = %s' % (mp.nstr(lhs,12), mp.nstr(rhs,12), mp.nstr(lhs/rhs,12)))
    assert lhs >= rhs
    assert all(crit_holds(L, Fr(1,500)) for L in range(100, 20001))
    print('criterion holds for every integer l in [100, 20000] (monotone in l)')
    lmin = next(L for L in range(1, 1000) if crit_holds(L, Fr(1,500)))
    print('smallest l at which the second inequality holds:', lmin)
    # log(1-z) >= -2z on [0,1/2]
    grid = [mp.mpf(i)/20000 for i in range(0, 10001)]
    assert all(mp.log(1-z) >= -2*z for z in grid)
    print('log(1-z) >= -2z on 10001-point grid of [0,1/2] incl. endpoints: True; at z=1/2:',
          mp.nstr(mp.log(0.5),10), '>= -1')
    zE = mp.e**(-mp.mpf(100)/32)
    print('z_E at l=100 = e^{-100/32} =', mp.nstr(zE, 10), '< 1/2:', zE < 0.5)
    # sharper worst case for the product given sum z_F = l/500 and each z_F <= zmax:
    # log(1-z)/z is decreasing, so the product is smallest when mass sits on z_F = zmax.
    for L in (100, 101, 150, 1000):
        S = mp.mpf(L)/500
        worst_prod = (1 - zE)**(S/zE)
        val = mp.e**(-mp.mpf(L)/32)*worst_prod
        print('  l=%d: worst-case z_E*prod = %s  vs  paper lower bound %s  vs  2e^{-l/8} = %s' %
              (L, mp.nstr(val,8), mp.nstr(mp.e**(-(mp.mpf(1)/32+mp.mpf(2)/500)*L),8), mp.nstr(2*mp.e**(-mp.mpf(L)/8),8)))
    print('--- CONTROLS (each must FAIL) ---')
    print('CONTROL l=7 (below lmin):', crit_holds(7, Fr(1,500)))
    print('CONTROL per-label incident weight 1/20 instead of 1/500: margin =', margin(Fr(1,20)),
          '; criterion at l=100:', crit_holds(100, Fr(1,20)), '; at l=10^6:', crit_holds(10**6, Fr(1,20)))
    print('CONTROL log(1-z) >= -2z at z=0.8:', mp.log(1-mp.mpf('0.8')) >= -2*mp.mpf('0.8'))
    return 0
sys.exit(main())
```

Output:

```
1/8 - 1/32 - 2/500 = 359/4000 = 0.08975 ; times 100 = 359/40
certificate 1 + 100*margin = 399/40 > 2 : True   (e^x >= 1+x)
l=100: exp(-(1/32+2/500)l) = 0.0294518073691 ; 2e^{-l/8} = 7.45330634416e-6 ; ratio = 3951.50903628
criterion holds for every integer l in [100, 20000] (monotone in l)
smallest l at which the second inequality holds: 8
log(1-z) >= -2z on 10001-point grid of [0,1/2] incl. endpoints: True; at z=1/2: -0.6931471806 >= -1
z_E at l=100 = e^{-100/32} = 0.04393693362 < 1/2: True
  l=100: worst-case z_E*prod = 0.035810047  vs  paper lower bound 0.029451807  vs  2e^{-l/8} = 7.4533063e-6
  l=101: worst-case z_E*prod = 0.034637372  vs  paper lower bound 0.028431716  vs  2e^{-l/8} = 6.5775198e-6
  l=150: worst-case z_E*prod = 0.0067765295  vs  paper lower bound 0.0050543804  vs  2e^{-l/8} = 1.4388266e-8
  l=1000: worst-case z_E*prod = 3.4677589e-15  vs  paper lower bound 4.9104299e-16  vs  2e^{-l/8} = 1.0332841e-54
--- CONTROLS (each must FAIL) ---
CONTROL l=7 (below lmin): False
CONTROL per-label incident weight 1/20 instead of 1/500: margin = -1/160 ; criterion at l=100: False ; at l=10^6: False
CONTROL log(1-z) >= -2z at z=0.8: False
[wall 0.85 s, maxrss 18528 KB, exit 0]
```

### decreasing.py

(4.6) analysis: log(CDh)/h decreasing from h = D², sup bound, summand bound and its threshold D*, tail. Controls: (C,D) = (1,1), (0.1,2); D = 1000; h > D instead of h > D².

```python
# Check the (outer:second-weight) analysis:
#  (a) f(h) = log(CDh)/h is decreasing for h >= D^2 once D is large (C >= 1);
#  (b) sup_{h > D^2} 6D log(CDh)/h <= 6 log(C D^3)/D;
#  (c) threshold D* with 6 log(C D^3)/D <= 1/128, after which every summand
#      (CDh)^{6D} e^{-h/64} <= e^{-h/128}, and the tail sum_{h>D^2} e^{-h/128} is tiny;
#  explicit C from the proof of count:local: C0 = 9*16005^2 (9(16004Dh+1)^2 <= C0 (Dh)^2), C = C0^{1/3}.
import math, sys

def step_decreasing(C, D, h):
    # sign of f(h) - f(h+1) = [log(CDh) - h*log1p(1/h)] / (h(h+1))
    return math.log(C*D*h) - h*math.log1p(1.0/h) > 0

def check_decreasing(C, D, steps=20000):
    h0 = D*D
    hs = list(range(h0, h0+steps)) + [int(h0*1.37**i) for i in range(1, 120)]
    return all(step_decreasing(C, D, h) for h in hs)

def check_sup(C, D, a=6):
    h0 = D*D
    bound = a*math.log(C*D**3)/D
    hs = [h0+1+i for i in range(5000)] + [int(h0*1.21**i) for i in range(1, 200)]
    return max(a*D*math.log(C*D*h)/h for h in hs) <= bound*(1+1e-12)

def threshold(C, a=6):
    D = 2
    while a*math.log(C*D**3)/D > 1/128: D += 1
    return D

def summand_ok(C, D, a=6):
    # log[(CDh)^{aD} e^{-h/64}] <= -h/128 at h = D^2+1 .. and geometric samples
    h0 = D*D
    hs = [h0+1+i for i in range(2000)] + [int(h0*1.11**i) for i in range(1, 400)]
    worst = max(a*D*math.log(C*D*h) - h/64 + h/128 for h in hs)
    return worst <= 0, worst

def main():
    C0 = 9*16005**2
    Cpf = C0**(1/3)
    print('C0 = 9*16005^2 =', C0, ' C = C0^(1/3) = %.3f  (count:local proof constant)' % Cpf)
    for C in (1, 2, Cpf, 1e6, float(C0)):
        for D in (2, 3, 5, 10, 100, 1000, 30000):
            assert math.log(C*D**3) >= 1, (C, D)
            assert check_decreasing(C, D), (C, D)
            assert check_sup(C, D), (C, D)
    print('(a),(b) verified for C in {1,2,%.1f,1e6,%d}, D in {2,3,5,10,100,1000,30000}' % (Cpf, C0))
    for C, a, name in ((1, 6, 'C=1, (CDh)^{6D}'), (Cpf, 6, 'paper C, (CDh)^{6D}'), (16005, 14, 'Lean (16005Dh)^{14D}')):
        Ds = threshold(C, a)
        ok, worst = summand_ok(C, Ds, a)
        logtail = -(Ds*Ds+1)/128 - math.log(1-math.exp(-1/128))
        print('%-24s D* = %6d (k > (D*-1)^10 ~ 10^%.1f); summand<=e^{-h/128} at D*: %s (max log-excess %.3g); log10(tail sum) <= %.4g'
              % (name, Ds, 10*math.log10(Ds-1), ok, worst, logtail/math.log(10)))
    print('--- CONTROLS (each must FAIL) ---')
    print('CONTROL C=1, D=1 decreasing from h=D^2:', check_decreasing(1, 1), ' f(1)=%.4f f(2)=%.4f' % (math.log(1)/1, math.log(2)/2))
    print('CONTROL C=0.1, D=2 decreasing from h=D^2:', check_decreasing(0.1, 2))
    ok, worst = summand_ok(Cpf, 1000)
    print('CONTROL summand bound at D=1000 (k~10^30), paper C: %s (log-excess %.4g at worst sampled h)' % (ok, worst))
    print('CONTROL sup bound with D^2 replaced by D (h > D) at D=100, C=1: ',
          max(6*100*math.log(100*h)/h for h in range(101, 20000)) <= 1/128)
    return 0
sys.exit(main())
```

Output:

```
C0 = 9*16005^2 = 2305440225  C = C0^(1/3) = 1321.046  (count:local proof constant)
(a),(b) verified for C in {1,2,1321.0,1e6,2305440225}, D in {2,3,5,10,100,1000,30000}
C=1, (CDh)^{6D}          D* =  23156 (k > (D*-1)^10 ~ 10^43.6); summand<=e^{-h/128} at D*: True (max log-excess -141); log10(tail sum) <= -1.819e+06
paper C, (CDh)^{6D}      D* =  29210 (k > (D*-1)^10 ~ 10^44.7); summand<=e^{-h/128} at D*: True (max log-excess -154); log10(tail sum) <= -2.895e+06
Lean (16005Dh)^{14D}     D* =  77899 (k > (D*-1)^10 ~ 10^48.9); summand<=e^{-h/128} at D*: True (max log-excess -286); log10(tail sum) <= -2.059e+07
--- CONTROLS (each must FAIL) ---
CONTROL C=1, D=1 decreasing from h=D^2: False  f(1)=0.0000 f(2)=0.3466
CONTROL C=0.1, D=2 decreasing from h=D^2: False
CONTROL summand bound at D=1000 (k~10^30), paper C: False (log-excess 1.596e+05 at worst sampled h)
CONTROL sup bound with D^2 replaced by D (h > D) at D=100, C=1:  False
[wall 0.42 s, maxrss 11940 KB, exit 0]
```

### second_sum_threshold.py

Informational: where the per-label second-family sum itself drops below 1/1000 (vs the text's summand route). Control: D = 5000.

```python
# Informational: smallest D at which the per-label second-family weight bound
#   S(D) = sum_{h > D^2} (C D h)^{6D} e^{-h/64}
# is <= 1/1000, with C = (9*16005^2)^{1/3} from the proof of count:local, versus the paper's
# sufficient route (each summand <= e^{-h/128}, needing 6 log(C D^3)/D <= 1/128).
# For D > 384, g(h) = 6D log(CDh) - h/64 is decreasing on h > D^2 with slope <= 6D/D^2 - 1/64,
# so S(D) <= exp(g(D^2+1)) / (1 - exp(6/D - 1/64)).
import math
C = (9*16005**2)**(1/3)
def logS_upper(D, a=6, C=C):
    slope = a/D - 1/64
    assert slope < 0
    return a*D*math.log(C*D*(D*D+1)) - (D*D+1)/64 - math.log(1 - math.exp(slope))
D = 400
while logS_upper(D) > math.log(1/1000): D += 1
print('true-sum route (paper C, 6D): S(D) <= 1/1000 from D =', D, '(k > (D-1)^10 ~ 10^%.1f)' % (10*math.log10(D-1)))
D = 2000
while logS_upper(D, a=14, C=16005) > math.log(1/1000): D += 1
print('true-sum route (Lean 16005, 14D): from D =', D, '(k ~ 10^%.1f)' % (10*math.log10(D-1)))
# CONTROL (must FAIL): at D = 5000 the per-label weight is astronomically large
print('CONTROL D=5000: log S(D) upper bound = %.4g (> log(1/1000) = %.3f)' % (logS_upper(5000), math.log(1/1000)))
```

Output:

```
true-sum route (paper C, 6D): S(D) <= 1/1000 from D = 13736 (k > (D-1)^10 ~ 10^41.4)
true-sum route (Lean 16005, 14D): from D = 36945 (k ~ 10^45.7)
CONTROL D=5000: log S(D) upper bound = 5.915e+05 (> log(1/1000) = -6.908)
[wall 0.09 s, maxrss 10972 KB, exit 0]
```

### first_weight.py

(4.5) from the paper's displayed bounds (count:global, setup:dilation, setup:q-bounds), k = 10^e. Controls: rows of size δk^{1/4}; D = k^{1/5}.

```python
# Check (outer:first-weight): k*T_glob*exp(-(delta*M-1)/32) = o(1), using exactly the bounds the
# paper displays: T_glob <= [9(3k^2F+1)^2]^{2D} (count:global), F = k^2*lambda + 2m,
# log lambda <= h0*log(2M) (setup:dilation), m = ceil(k^2 R) <= k^2 R + 1,
# R = log(1+1/(2alpha)) <= (D+1) log q, log q <= c k log k / D + log(2k^2) (setup:q-bounds).
# Reports the first k = 10^e at which the first-family total weight is <= 1/1000
# (half of the 1/500 incident budget). Everything in log space; D, M exact integers.
import math, sys

def iroot_ceil(n, r):
    # exact ceil(n^(1/r)) by binary search on integers
    lo, hi = 0, 1 << (n.bit_length()//r + 2)
    while lo < hi:
        mid = (lo + hi)//2
        if mid**r >= n: hi = mid
        else: lo = mid + 1
    return lo

def logaddexp(a, b):
    m = max(a, b); return m + math.log(math.exp(a-m) + math.exp(b-m))

def log_first_weight(e, Dpow=10, rowfun=None, lean=False):
    k = 10**e; L = e*math.log(10)
    D = iroot_ceil(k, Dpow); M = iroot_ceil(k, 2)
    c = 1e-5; delta = 0.1
    logM2 = math.log(2*M)
    log_lambda = D*D*logM2                       # paper's bound log(lambda) <= h0 log(2M)
    log_q = c*math.exp(L)*L/D + math.log(2) + 2*L
    R = (D+1)*log_q
    log_2m = math.log(2) + logaddexp(2*L + math.log(R), 0.0)
    logF = logaddexp(2*L + log_lambda, log_2m)
    log_inner = logaddexp(math.log(3) + 2*L + logF, 0.0)          # log(3k^2F+1)
    if lean: logT = 2*D*(math.log(16) + 6*log_inner)
    else:    logT = 2*D*(math.log(9) + 2*log_inner)
    rows = (delta*M - 1) if rowfun is None else rowfun(k)
    return L + logT - rows/32, logT, D, M

def first_ok(**kw):
    target = math.log(1/1000)
    hist = []
    for e in range(4, 260):
        v = log_first_weight(e, **kw)[0]
        hist.append((e, v))
    ok = [e for e, v in hist if v <= target]
    first = ok[0] if ok else None
    stays = first is not None and all(v <= target for e, v in hist if e >= first)
    return first, stays, hist

def main():
    first, stays, hist = first_ok()
    print('paper bounds: first k=10^e with first-family weight <= 1/1000: e =', first, '; stays below through e=259:', stays)
    for e in (20, 22, 23, 24, 26, 30, 45, 60):
        v, logT, D, M = log_first_weight(e)
        print('  e=%3d  D=%-8d  log T_glob <= %.4g   (deltaM-1)/32 = %.4g   log(k T e^{-(dM-1)/32}) = %.4g' % (e, D, logT, (0.1*M-1)/32, v))
    f2, s2, _ = first_ok(lean=True)
    print('Lean global-count base 16(3k^2F+1)^6: first e =', f2, '; stays:', s2)
    print('--- CONTROLS (each must FAIL) ---')
    f3, s3, h3 = first_ok(rowfun=lambda k: 0.1*iroot_ceil(k, 4) - 1)
    print('CONTROL rows of size delta*k^{1/4} instead of delta*M: first e =', f3, '; value at e=259: %.4g' % h3[-1][1])
    f4, s4, h4 = first_ok(Dpow=5)
    print('CONTROL D = k^{1/5} instead of k^{1/10} (log T_glob ~ D^3 log M vs M): first e =', f4, '; value at e=259: %.4g' % h4[-1][1])
    return 0
sys.exit(main())
```

Output:

```
paper bounds: first k=10^e with first-family weight <= 1/1000: e = 23 ; stays below through e=259: True
  e= 20  D=100       log T_glob <= 9.495e+07   (deltaM-1)/32 = 3.125e+07   log(k T e^{-(dM-1)/32}) = 6.37e+07
  e= 22  D=159       log T_glob <= 4.185e+08   (deltaM-1)/32 = 3.125e+08   log(k T e^{-(dM-1)/32}) = 1.06e+08
  e= 23  D=200       log T_glob <= 8.697e+08   (deltaM-1)/32 = 9.882e+08   log(k T e^{-(dM-1)/32}) = -1.185e+08
  e= 24  D=252       log T_glob <= 1.813e+09   (deltaM-1)/32 = 3.125e+09   log(k T e^{-(dM-1)/32}) = -1.312e+09
  e= 26  D=399       log T_glob <= 7.782e+09   (deltaM-1)/32 = 3.125e+10   log(k T e^{-(dM-1)/32}) = -2.347e+10
  e= 30  D=1000      log T_glob <= 1.409e+11   (deltaM-1)/32 = 3.125e+12   log(k T e^{-(dM-1)/32}) = -2.984e+12
  e= 45  D=31623     log T_glob <= 6.641e+15   (deltaM-1)/32 = 9.882e+19   log(k T e^{-(dM-1)/32}) = -9.881e+19
  e= 60  D=1000000   log T_glob <= 2.791e+20   (deltaM-1)/32 = 3.125e+27   log(k T e^{-(dM-1)/32}) = -3.125e+27
Lean global-count base 16(3k^2F+1)^6: first e = 26 ; stays: True
--- CONTROLS (each must FAIL) ---
CONTROL rows of size delta*k^{1/4} instead of delta*M: first e = None ; value at e=259: 5.992e+80
CONTROL D = k^{1/5} instead of k^{1/10} (log T_glob ~ D^3 log M vs M): first e = None ; value at e=259: 3.003e+158
[wall 0.19 s, maxrss 10980 KB, exit 0]
```

### rows.py

First-family row construction by brute force (≤1 occurrence per row, min row size, partition, summing balanced rows). Controls: w_max − 1 rows; ungrouped order.

```python
# Brute-force check of the first-family row construction in Prop outer:coloring:
# light labels = multiplicity <= k/M in the word; if L0 >= delta*k light positions,
# order light positions grouping equal labels, deal cyclically into w_max rows.
# Claims: (1) a label occurs at most once per row; (2) every row has >= floor(L0/w_max)
# >= delta*M - 1 positions; (3) rows partition the light positions; (4) if every row has
# each bit on >= 1/4 of its positions then each bit is on >= 1/4 of the light positions.
import random, sys
from fractions import Fraction as Fr
from collections import Counter

def make_rows(word, k, M, nrows=None, grouped=True, rng=None):
    mult = Counter(word)
    light = [j for j in range(k) if mult[word[j]]*M <= k]      # multiplicity <= k/M
    if not light: return None
    wmax = max(mult[word[j]] for j in light)
    if grouped: order = sorted(light, key=lambda j: (word[j], j))
    else: order = light[:]; rng.shuffle(order)
    R = wmax if nrows is None else nrows
    rows = [order[i::R] for i in range(R)]
    return light, wmax, rows

def check(word, k, M, delta, **kw):
    out = make_rows(word, k, M, **kw)
    if out is None: return 'nolight'
    light, wmax, rows = out
    L0 = len(light)
    if L0 < delta*k: return 'few'
    if any(len({word[j] for j in r}) != len(r) for r in rows): return 'REPEAT'
    if min(len(r) for r in rows) < L0 // wmax: return 'SHORT'
    if not (L0 // wmax >= delta*M - 1): return 'ROWSIZE'
    if sorted(j for r in rows for j in r) != sorted(light): return 'PARTITION'
    return 'ok'

def main():
    rng = random.Random(7)
    delta = Fr(1, 10)
    stats = Counter()
    for it in range(4000):
        k = rng.randint(100, 900); M = max(2, int(k**0.5) + rng.randint(0, 3))
        nl = rng.randint(2, k)
        word = [rng.randint(0, nl) if rng.random() < 0.7 else rng.randint(0, 5) for _ in range(k)]
        stats[check(word, k, M, delta)] += 1
    print('correct construction:', dict(stats))
    assert all(s in ('ok', 'few', 'nolight') for s in stats)
    # (4) summing balanced rows: random bits, keep only colorings where every row balanced
    good = bad = 0
    for it in range(3000):
        k = 200; M = 15
        word = [rng.randint(0, 120) for _ in range(k)]
        out = make_rows(word, k, M)
        light, wmax, rows = out
        if len(light) < k/10: continue
        bits = {b: rng.randint(0, 1) for b in set(word)}
        if all(4*sum(bits[word[j]] == v for j in r) >= len(r) for r in rows for v in (0, 1)):
            for v in (0, 1):
                if 4*sum(bits[word[j]] == v for j in light) < len(light): bad += 1
            good += 1
    print('row-balanced colorings tested:', good, '; overall-unbalanced among them:', bad)
    assert bad == 0
    print('--- CONTROLS (each must FAIL) ---')
    stats = Counter()
    for it in range(2000):
        k = rng.randint(100, 900); M = max(2, int(k**0.5))
        word = [rng.randint(0, k//3) for _ in range(k)]
        out = make_rows(word, k, M)
        if out is None or out[1] < 2: continue
        stats[check(word, k, M, delta, nrows=out[1]-1)] += 1
    print('CONTROL deal into w_max-1 rows:', dict(stats))
    stats = Counter()
    for it in range(2000):
        k = rng.randint(100, 900); M = max(2, int(k**0.5))
        word = [rng.randint(0, k//3) for _ in range(k)]
        stats[check(word, k, M, delta, grouped=False, rng=rng)] += 1
    print('CONTROL ungrouped (random) order:', dict(stats))
    return 0
sys.exit(main())
```

Output:

```
correct construction: {'ok': 3898, 'nolight': 55, 'few': 47}
row-balanced colorings tested: 2950 ; overall-unbalanced among them: 0
--- CONTROLS (each must FAIL) ---
CONTROL deal into w_max-1 rows: {'REPEAT': 2000}
CONTROL ungrouped (random) order: {'REPEAT': 2000}
[wall 8.50 s, maxrss 12308 KB, exit 0]
```

## Citation table (scope: §4 has one citation)

| Cited | Paper's claim | Source says | Verdict |
|---|---|---|---|
| Erdős–Lovász 1975, "Problems and results on 3-chromatic hypergraphs and some related questions", Colloq. Math. Soc. J. Bolyai 10, 609–627 (`erdosLovasz1975`) | "For the origins of the local lemma, see Erdős and Lovász~\cite{erdosLovasz1975}; the proof of the form used here is included." | p. 616 (local copy /tmp/oaimath/160/refs/erdos_1975-34.pdf, PDF p. 8, rendered and read): "**Lemma.** Let G be a (finite) graph with maximum degree d and vertices v_1, …, v_n. Let us associate an event A_i with v_i (i = 1, …, n) and suppose that A_i is independent of the set {A_j : (v_i, v_j) ∈ E(G)}. Also suppose (3) P(A_i) ≤ 1/(4d). Then (4) P(Ā_1 … Ā_n) > 0." (symmetric form; the printed "∈ E(G)" is evidently a misprint in the source for non-adjacency) | **MATCH** — the paper cites it only for the origin of the local lemma and proves its own asymmetric version (Lemma 4.1) in full; it does not attribute the asymmetric form to this source. |

## Summary

Scope 04-outer.tex: **HOLDS AS READ.** Lemma 4.1 (finite asymmetric LLL) is correct line by line; the "independence from
T_2 in the numerator" uses exactly the sigma-algebra in the hypothesis (T_2 ⊆ ℰ∖({E}∪Γ(E)) because E ∉ T). Prop 4.2:
first-family rows are deterministic functions of the word, each label at most once per row, rows of size ≥ δM − 1,
≤ kT_glob events; second family indexed by (pattern, h, t), finite, l(E) ≥ h/2; tail (4.4) correct including the strict
inequalities; (4.5) holds since log T_glob = O(k^{3/10} log k) = o(k^{1/2}); (4.6)'s decreasing claim, sup bound,
summand bound and tail are correct; (4.7) uniform in β; dependency graph valid; double counting in the right direction;
(4.8) holds with margin (359/4000)·100 = 8.975 > log 2. No FATAL, no GAP. Objections: O1 cross-references print
"Theorem" for Lemma/Definition/Proposition (cosmetic); O2 "distinct events" must mean distinct indices (unclear,
exposition); O3 loose "its tail" (cosmetic); O4 the proof's thresholds are k ≳ 10^23 for (4.5) and k ≳ 10^41–10^44.7
for (4.6) (informational; no K_0 is claimed). Informational for other seats: §4 needs only log T_glob ≤ k^{1/2}/320 −
O(log k) and a per-label local count exp(o(D²)) uniform in q, λ, β; the Lean formalizes weaker counts
((16005Dh)^{14D}, Sauer–Shelah arrangement bound) than the paper's 6D / (e+1)²(s+1)^e, which suffices for §4 but leaves
the paper's sharper §3 constants uncertified by Lean.
