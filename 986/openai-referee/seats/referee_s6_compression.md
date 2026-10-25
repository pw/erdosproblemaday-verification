# Referee report — Paper B (s ≥ 6), "Sharp Logarithmic Exponents for Fixed Off-Diagonal Ramsey Numbers", §§4–6 (marking, compression, conclusion)
Seat: s6_compression. Started 2026-10-20. Written incrementally; verdict line filled at the end.

VERDICT: HOLDS AS READ for §4 (marking), §5 (compression), §6 (iteration, transfer, upper bound) and the §1 entropy
lower bound — conditional on geom:description, geom:validation and geom:produced-test exactly as stated (§§2–3 internals
are another seat's; COULD NOT CHECK them here). No FATAL or GAP found. One UNCLEAR scope discrepancy with the Lean
(Objection 1: the formal library proves Theorem 1.2 for EVERY d ≥ 3, the paper claims only d ≥ 5, and the d ≥ 5
hypothesis is never used in the text), plus expository fixes (Objections 2–7).

## Working notes (appended as read)

### Pass 1 notes (§1 entropy lower bound, §4 marking) — 2026-10-20
- base:selection-entropy (01-foundations.tex): max-atom bound P(F=f) ≤ 2C_0·C(N,ℓ)·(Q_dQ_{d-1})^{-ℓ}; arithmetic checked:
  ℓ[(2d-1)σ − (d−1)σ + η log σ − O(1)] = dσℓ + ηℓ log σ − O(ℓ). Holds for ANY selector, any auxiliary randomness, because it is a
  max-atom bound on an event containment. Conditioning on an event of prob ≥ c multiplies the domination constant by 1/c. Holds.
  Conditioning on a public-table VALUE τ when the restricting event involves τ: per-τ loss is log(1/P(E|τ)); averaged over τ|E the
  loss is ≤ 1/(e·c) (x log x ≥ −1/e), so "after averaging" is fine provided the stream is independent of the table before the event.
- mark:marking: popular count 32q^l, poor-cheap count Cq^{d+1}/|Z_l| via variance identity, |Z_r| ≤ |Z_l|, expensive count
  O(qσ) per scan via |U_l| ≤ (l+1)|Z_l| and multiplicative shrink 1−1/(16(d+1)q) from ≤Q_d. All checked; holds.
  Deficit bound (mark:subset-deficit) = Λ + O(k) + ΔE h − ηℓ log σ, the last term DROPPED. Holds.
  NOTE: (mark:entropy-upper) H(F) ≤ dσℓ + Λ + O(k) + O(Δqσ) means the contradiction needs, at the final stage,
  Λ = o(k log σ) and Δ = o(σ^η log σ). Initial stage has Λ=0, Δ=(d−1)σ (whole flag space vs q^d) — Δqσ = Θ(qσ²) ≫ k log σ.
- mark:representatives (exposure): TC-drop identity re-derived; selected-absorption identity correct (M_i of a rep is a function of
  other blocks' draws); telescoping holds. T_1/m = o(1) in all three cases checked against (mark:windows).
- mark:endpoint-mass, mark:core-dimension, mark:collision (open band: dims r and d+2−r contradict containment; integer band:
  forced U=V^⊥, both flags in R(V_i(a)), ≤ C_dσ per i by simultaneous occupancy) — all checked; holds.
- mark:good-indices: three proportions O(σ^{−2β}), O(σ^{−1001β}), O(σ^{2000β−η/2}) re-derived; holds.

### Pass 2 notes (§5 compression, §6 conclusion) — first read
- comp:step accounting re-derived: per node cost CqP(d_A+d_B+P) (description) + CqP(d_A+d_B+1) (validation); potential
  G=log(|U_A||U_B|/q^{d+1}); d_A+d_B ≤ G+CK_* uses n_An_B ≥ .81|A||B| ≥ q^{d+1}e^{-CK_*} POINTWISE (deterministic);
  children G_left ≤ d_B+C, G_right ≤ d_A+C from the validated cap sizes, which are part of the ACCEPTANCE predicate,
  hence deterministic on success. Level sums ≤ C(σ+wK_*); total CqP·log(w+2)·(σ+wP)+Cwσ. Holds as a max-length bound.
- end:entropy-contraction arithmetic re-derived: qPσ/k ≤ CDσ^{9β−η}, qP²w/k ≤ CDσ^{18β−η/2}, wσ/k ≤ Cσ/q. D_new ≤ σ^β +
  Dσ^{β−η/3} + CDσ^{7β−η} ≤ σ^{2β}+Dσ^{−η/4}; T=⌈8/η⌉ rounds → D_T ≤ 2σ^{2β}; final Λ_*/k ≤ 2σ^{2β−η/3},
  Δ_*qσ/k ≤ Cσ^{8β−η}. Then mark:entropy-upper gives dσℓ_* + O(k). Contradiction with dσℓ_*+ηℓ_* log σ − O(k). Holds.
  The O(k) excess in the upper bound is J_0−dσ = O(1) per cheap slot plus O(1)/slot masks; the surplus is ηℓ log σ. OK.
- Conditionings per round: (a) θ_0-determined class event, prob ≥ 1/#classes; (b) after FIXING a table family τ chosen
  so that P(success|τ) ≥ c (tables independent of stream ⇒ fixing τ leaves the stream law unchanged), the success event.
  Plus the initial occupancy event (≥1/2). Total 2(T+1)+1 = O(1/η) conditionings, independent of q. Lower bound's
  domination constant becomes 2·∏(1/c_i): fixed. Holds.
- comp:rich-union: Schwartz–Zippel + box-partition rank bound; re-derived; holds (proof self-contained, citation not load-bearing).
- comp:high-rank: coverage (variance estimate, span growth .3/q per sample, conflict union bound 2h·σ^{−2000β}/q =
  O(σ^{−1999β}), excess-span bound Ce^K/q), size (rich-union dyads, binomial tail, sum bounded uniformly in t). Holds.
- comp:supports, comp:average-incidence, comp:target-incidence, comp:order, open-band deletion count: re-derived; hold.
- comp:tree-loss: chronology of ancestor tests (left child: first points vs pivot's LATE second support; right: second
  points vs pivot's EARLY first support) matches the time direction of consistency. Holds.
- §6 transfer: q ∈ [c_0x,x], x=t/(log t)^{1+η}; k ≤ q(log q)^{1+η} < t; r(s,t) > ⌊q^d log q⌋ ≥ c t^{s−1}/(log t)^{s−2+(s−1)η};
  η=min{1/20, ε/(2d)}. Holds. Prime-interval lemma (Chebyshev) holds. Upper bound (Alon-style triangle-free lemma +
  sampling/deletion induction) re-derived; holds.

### Pass 3 notes — citations, Lean cross-check, numerical test
- Nie–Wang (arXiv 1402.3018v2, fetched): Thm 5.6 is HF(F_q^n,d)·|cl_d(Y)| ≤ q^n|Y| (Thm 4.1 its engine). With d=cδq,
  HF ≈ (cδq)^n/n!, and rich subspaces lie in cl_d(X̃) by Schwartz–Zippel ⇒ comp:rich-union. Citation accurate; the
  paper's own proof is self-contained; Lean `rich_union_projective` (Marking/CardVectorLifts.lean:112) proves it with the
  explicit constant (5n/δ)^n. Holds.
- Bradač v3 (fetched): §2.5 digraph D* edge (a,b)→(a',b') iff a⊥b' and a'⊥̸b = Paper B's edge rule. Claim 2.13 uses the
  same popular (|Z_l|/(16q), ≤32q^l) and poor (|Z_l|/(8q)) thresholds, BUT Bradač's W(y) spans ALL earlier b_i with
  a_i⊥y, while Paper B's V(y) spans only EXPENSIVE ones. Checked the three facts used survive this (consistency gives
  a⊥V(b) for any sub-collection; rank increments only at expensive steps; domain counts relative to current state).
- Numerical: s6c_scripts/marking_sim.py runs both scans on greedy-consistent tuples in PG(3,5), PG(3,7), PG(2,11):
  0 violations of a⊥V(b); popular-set size ≤ 32q^l asserted and held; max cheap joint domain / q^d ∈ [0.38, 1.74].
  (Small q only — confirms the bookkeeping, not asymptotics.)
- Lean ContextOutput (Execution/ContextOutput.lean:12): `domains : Γ → Fin m → Finset F` is a function of the MESSAGE
  ALONE, `dominated : (μ.map source) ≤ L·p`, `cost : entropy (μ.map msg) ≤ C`, `chosen : Fin m ↪o Fin ℓ`. This
  formally enforces "the new decoder reads only the new message" and encodes every conditioning as a domination factor.
  Lean final contradiction `eventually_no_small_context` (Parameters/NoContext.lean:20): no ContextOutput with
  m ≥ cqσ^{1+η}, B = P q^d exp(48σ^{8β}), C = k, L = (4·classCount)^T. Matches end:final-budgets (Λ_* ≤ k, Δ_* = O(σ^{8β})).
  Lean iteration `eventually_iterated_context` uses T = ⌈8/η⌉+1 stages, retained fraction (1/2)/(256·classCount)^T:
  matches §6 (T+1 compressions).
- !! Lean `actual_prime_construction (i : ℕ) : PrimeConstruction (i+3)` — EVERY d ≥ 3, no restriction on i anywhere
  (grepped). Paper restricts to d ≥ 5 and never uses it. See Objection 1.

## Objections

**1. UNCLEAR (scope / paper-vs-Lean; the most consequential item from this seat).**
Quoted: 01-foundations.tex l.4 "Fix an integer $d\ge5$ and $0<\eta<1/10$"; 00-introduction.tex, Theorem
`intro:prime-construction` "Fix an integer $d\ge5$ …".
Why: grep shows `d\ge5` appears ONLY where it is fixed (01 l.4, 06 l.16, intro l.115); no step of §§1, 4, 5, 6 uses
d ≥ 5 (nothing in marking, high-rank coverage (r+r' > d+1), integer/open bands, rich-union, tree, or iteration depends on
d beyond d ≥ 2–3). The Lean agrees and goes further: `Construction/PrimeConstruction.lean:14`
`theorem actual_prime_construction (i : ℕ) : PrimeConstruction (i+3)` with NO hypothesis on i (grepped the whole
SharpRamsey tree for any lower bound on i: none; `eventually_graph_witness` takes only `0<η`, `η≤1`). With
`Bounds/Lower.lean:166 all_epsilon_lower (d) (hd : 1≤d)` and `Upper.ramsey_upper (3 ≤ s)`, the hypothesis `hs : 6 ≤ s` of
`main_of_primeConstruction` is used only via `omega` for 3 ≤ s, s−1+1 = s, s−1−1 = s−2. So, conditional on the kernel
replay, the SAME library proves `MainBounds 4 ∧ MainLimit 4`, i.e. r(4,t) = t³/(log t)^{2+o(1)} (improving
Mattheus–Verstraete's t³/(log t)⁴, which the paper itself cites at intro l.65 as the state of the art for s = 4), and
`MainBounds 5` (Paper A's theorem) — results neither preprint claims. Either the d ≥ 5 restriction is gratuitous (then
the paper understates its own result and Paper A is a special case) or there is a d-dependent defect visible in neither
the text nor the Lean. A hostile reader should treat an unclaimed improvement of the best-known r(4,t) bound as a red
flag demanding an explicit statement.
Fix: authors state whether Theorem 1.2 holds for d = 3, 4 and why it is restricted; after the replay, the kernel seat
should compile the 5-line corollary `example : SharpLogRamsey.MainBounds 4 ∧ SharpLogRamsey.MainLimit 4` (copy of
`main_of_primeConstruction` with `hs : 4 ≤ s`, using `LowerTransfer.actual_prime_construction 0`).

**2. EXPOSITION (marking is a genuine modification of Bradač Claim 2.13, not a transcription).**
Quoted: 04-marking.tex §"The marking message": "This marking procedure adapts the counting argument in
\cite[Claim~2.13]{Bradac2026}" and "Whenever a position is declared expensive, adjoin its second endpoint $b$ to $V(y)$
… No other position changes the state."
Why: in Bradač v3 (fetched, arXiv 2605.28793v3 p.11) W(y) is the span of ALL earlier b_i with a_i ⊥ y. Paper B updates
only at expensive positions — necessary so the decoder can rebuild the state from transmitted values. I checked that all
three facts used survive (a ⊥ V(b) by consistency for any sub-collection of earlier flags; rank increase of ≥|Z_l|/(16q)
points only at expensive steps; popular ≤ 32q^l and poor ≤ Cq^{d+1}/|Z_l| counts relative to the current state), and
simulated both scans (s6c_scripts/marking_sim.py: PG(3,5), PG(3,7), PG(2,11): 0 violations of a ⊥ V(b), popular count
assertion holds, cheap joint domain/q^d ≤ 1.74). Holds; but say "modifies" and note the change.

**3. EXPOSITION (the lower bound is far more robust than stated; state it so the reader can audit conditionings).**
Quoted: 00-introduction.tex "This bound survives any fixed number of restrictions to events of probability bounded
below"; 01-foundations.tex `base:selection-entropy` "The implicit constant may depend on $C_0$".
Why: the max-atom proof gives H(F) ≥ ℓ[dσ + η log σ − O(1) − log(k/ℓ)] − log(2C_0): the domination constant enters only
ADDITIVELY as log(2C_0) (Lean `Entropy/SelectedEntropy.lean:13 selected_map_entropy`: ℓ((d)log q + η log σ + log c − 1)
− log(2C), needing only N ≤ q^dσ and ℓ ≥ cqσ^{1+η}). It therefore survives conditioning on events of probability as
small as e^{−o(k log σ)}; the paper's actual conditionings are 2(T+1)+1 = O(1/η) events (occupancy ≥ 1/2; per stage a
θ_0-determined class event ≥ 1/#classes; per stage the success event after FIXING a good table family τ — tables are
independent of the stream, so fixing τ leaves the stream law unchanged). Lean: Lstar = (4·classCount)^T. Holds with
huge margin. Also make explicit that "after averaging" means: choose τ with P(success | τ) ≥ c, then condition (05
proof of comp:step does this; 00 l.218–221 is vaguer).

**4. EXPOSITION (high-rank proof notation; and comp:order's scope).**
Quoted: 05-compression.tex proof of `comp:high-rank`: "Fixing both auxiliary rows leaves the actual target law equal to
its original conditional law \(p_i\)". Here i is the target, while in the same proof the source is "the early
representative" (elsewhere also indexed i). Rename. Quoted: `comp:order` "For good representatives \(i<j\) in distinct
blocks, \(u_j\le u_i+CK\)": this holds for ALL such pairs, not only consecutive ones (the deletion count uses only the
consecutive case). The all-pairs form is what makes an ancestor's cap |U_A'| ≈ q^{d+1}/|B_pivot| size-compatible with a
descendant's earlier support A_{W'} (u_pivot ≤ u_{W'} + CK); the loss argument doesn't need it explicitly (it goes
through incidence density), but a sentence would pre-empt the obvious "the caps are the wrong size for descendants"
objection.

**5. EXPOSITION (units).** 02-geometry.tex l.30 "Integers $m\geq 0$ are encoded with $O(1+\log(m+1))$ bits" and all
description lengths are in bits, while 01-foundations.tex says "Entropies use natural units" and Λ = H(C). Constant
factor only; say so once.

**6. COSMETIC (paper vs Lean, different-but-stronger forms).** (a) Lean `Bounds/Lower.lean:19 prime_interval` uses
Mathlib Bertrand (prime in [x/4, x]) instead of the paper's Chebyshev Lemma `end:prime-interval` (which is correct as
written). (b) Lean `eventually_graph_witness` (Construction/GraphWitness.lean:21) proves the construction for EVERY
N ≤ q^dσ and every k ∈ [qσ^{1+η}/2, qσ^{1+η}], stronger than Theorem 1.2's single N, k. (c) Lean's final budget is
entropy ≤ k (not o(k)) with domain factor P·exp(48σ^{8β}) — consistent with `end:final-budgets`.

**7. COSMETIC.** `end:parameter-contraction`: σ^β + Dσ^{β−η/3} + CDσ^{7β−η} ≤ σ^{2β} + Dσ^{−η/4} — the σ^β → σ^{2β}
weakening is unnecessary (harmless). `mark:collision` calls c_ij "symmetric" but defines it only for i<j via G_ij;
say "extended symmetrically".

## Counting every log σ (priority 3) — explicit ledger
Final upper bound H(F_*) ≤ Λ_* + [masks: O(log d) per slot ⇒ O(k)] + [cheap slots: (ℓ_*−h)·J_0, J_0 = dσ + O_d(1) ⇒
dσℓ_* + O(k)] + [expensive: h ≤ Cqσ deterministic, each dσ + Δ_* + O(1) ⇒ the dσ part is inside dσℓ_*, Δ_*·Cqσ =
O(σ^{8β−η})k = o(k), O(1)·qσ = o(k)]. Λ_* ≤ 2σ^{2β−η/3}k. Exposure positions, old contexts, supports, rows: NOT in the
final message (discarded each stage; the lower bound is re-applied to the new subtuple). Per-stage cost is per NODE
(≤ w nodes, O(log w) levels), never per position: qPσ log w + qP²w log w + O(wσ). No per-position log σ term exists.
Surplus ηℓ_* log σ ≥ ηc^{T+1}k log σ. Comparison holds for large q.

## Lemmas checked and holding
base:selection-entropy (arithmetic and conditioning robustness), base:incidence (last assertion), base:rectangles,
base:event-transfer, base:scale-comparisons; mark:marking (popular 32q^l; poor Cq^{d+1}/|Z_l|; |Z_r| ≤ |Z_l|; expensive
O(qσ) via |U_l| ≤ (l+1)|Z_l| and shrink factor; message cost; subset deficit; entropy-upper); marginal caps
(mark:reciprocal-caps incl. clamping, mark:high-caps), band partition, class pigeonhole; mark:windows and T_1/m = o(1)
in all three cases; mark:representatives (TC-drop identity re-derived, selected-absorption identity, telescoping);
mark:endpoint-mass; mark:core-capture, mark:core-dimension; mark:collision (open band dim r + (d+2−r) contradiction;
integer band U = V^⊥ forcing both flags into R(V_i(a)); ≤ C_dσ charged slots per i pointwise); mark:good-indices (the
three proportions σ^{−2β}, σ^{−1001β}, σ^{2000β−η/2}); comp:rich-union (and the Nie–Wang citation); comp:high-rank
(coverage, excess-span bound, size via dyads); comp:supports; comp:average-incidence; comp:target-incidence;
comp:order; open-band deletion count; comp:product; comp:tree-loss (chronology of ancestor tests, per-depth trim
failure Cjε, Markov density rejection, CεH²); decoder reconstruction; comp:new-domain; comp:gap-potential,
comp:potential-branch, comp:tree-cost; proof of comp:step (table fixing, success conditioning, max-length ⇒ entropy);
§6 iteration (end:entropy-contraction, end:parameter-contraction, T = ⌈8/η⌉, end:final-budgets, uniform constants);
end:prime-interval; transfer to all t (k < t, η = min{1/20, ε/(2d)}); end:triangle-free; end:upper-bound induction;
proof of intro:main. Lean statement fidelity: ComparatorChallenges/SharpLogRamsey.lean `MainBounds`/`MainLimit` match
Theorem 1.1 (C independent of ε; `ramsey` = sInf of N with every graph on Fin N having an s-clique or independent
t-set = classical r(s,t)).
