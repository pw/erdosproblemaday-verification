# Seat F — finite stage (§9.1–9.6, Appendix A, the two checkers)

VERDICT: HOLDS AS READ (§9.1–9.6 + Appendix A; two EXPOSITION notes, no GAP, nothing FATAL)

Summary: every §9 inference rule re-derived from §2/§5/§6 and found exactly as strong as proved (none stronger); my own
brute-force enumerator + generating function reproduce all 42 pairs / 3099 patterns / Table 1 (as SETS, matching both
programs and the trace); both checkers implement the rules line-for-line (special cases req[0]={0}, k−ℓ incl. d=0, round-start
matrix all correct); a third validator written from the paper re-derives every initial matrix by explicit construction
(3099/3099 identical) and re-checks every round witness and final packing (0 bad, negative controls fire); mutation tests show
every rule does work except the top endpoint of (9.7) and the batch convention; one UNSOUND mutation (no degree test) leaves
the printed table byte-identical, so stdout agreement alone is weak evidence — the trace/explicit-construction match is what
certifies the code. Lean route: same patterns, different (witness-certificate) encoding, independent of the Python.

Printed numbering used throughout (from paper.txt): Prop 9.1 (finite verification), Lemma 9.2 (pattern coverage),
Lemma 9.3 (labels), Lemma 9.4 (extension rule, interval (9.7)), Lemma 9.5 (required-path rule), Lemma 9.6 (inheritance),
Lemma 9.7 (ball bounds, (9.8)–(9.11)), Lemma 9.8 (packing test, compatibility (9.12)), Lemma 9.9 (eliminating a path
hypothesis), Prop 9.10 (procedure soundness), Table 1 (pattern counts), Table 2 (results). From §6: Lemma 6.1 (closing),
Lemma 6.2 (optimality criterion (6.4)), Lemma 6.4 (separation), Cor 6.5 (singleton/ball compatibility). Lemma 5.3 (size test),
Lemma 2.2 (expansion), Theorem 3.x clq:bound (max{3,⌊k/2⌋} ≤ t ≤ k).

## 0. What §6 actually establishes for the optimal system (the hypotheses §9 may use)

Quoted from §6.1: "Choose a path system P of maximum total amount L subject to L<h. Among systems with this amount, choose one with
the minimum number e of assigned paths." Lemma 6.1: "No path system on Q, of total amount q and with v incident clique vertices,
satisfies h ≤ q ≤ k+1−v." Lemma 6.2: "L + 1_{e'≥e} ≤ A ≤ k+1−v' is impossible." Lemma 6.4(2): "if no such path has parameter
1 ≤ d ≤ r, then y has no neighbor in B_{r−1}(x;X)". Lemma 6.4(1): balls B_r(x), B_s(y) disjoint+anticomplete if parameters
1..r+s+2 forbidden. Cor 6.5: singleton–singleton needs xy ∉ E(G); singleton(−1)–ball(s) needs 1..s+1 forbidden.
Lemma 2.2 (expansion |N[I]| ≥ k|I|+1), δ ≥ k, α ≤ k, ω = t, no C_{k+1}; Lemma 5.3 (|Y| > max{k,2t} ⇒ α(Y) ≥ 3, needs k ≥ 5).
§9 uses nothing from §7–§8 (those assume t ≥ 9). I checked each §9 rule against exactly these.

## 2. Completeness of the enumeration (§9.1, Lemma 9.2, Table 1) — CONFIRMED

* Domain re-derived from first principles: k ≥ 5 (k = 3,4 are §4), t ≤ 8 (t ≥ 9 is Prop 8.4, which holds for every k with
  k ≤ 2t+1), and max{3,⌊k/2⌋} ≤ t ≤ k (Theorem clq:bound). For t ≤ 8 the lower bound ⌊k/2⌋ ≤ 8 forces k ≤ 17. Scanning
  k = 5..39 × t = 3..8 with only these constraints gives exactly the 42 pairs of (9.1). Nothing between "t ≤ 8" and "t ≥ 9"
  or between "k ≤ 4" and "k ≥ 5" is lost; for k ≥ 18 every admissible t is ≥ 9.
* Own enumerator (F_work/enum_own.py), deliberately dumb: generate ALL ordered lists of ORIENTED chains (tuples of positive
  amounts, Σ(len+1)=t, Σamount ≤ B=k−t), then canonicalise afterwards (each chain → min(c, reverse c), sort). This shares no
  recursion with either checker's generator. Separately, my own polynomial-arithmetic evaluation of the generating function
  (9.4)–(9.5). Result: for all 42 pairs, brute = gf = summary.json "patterns" = Table 1, and the per-amount histogram equals
  summary.json "by_amount". Total 3099; per k: 7,14,26,34,63,75,142,164,311,315,601,468,879 — every row of Table 1.
* Set equality, not just counts (F_work/cmp_sets2.py): for every (k,t), my canonical set = set(original `forests(t,k−t)`) =
  set(independent `patterns(t,k−t)`) = the set of patterns appearing in certificates.jsonl; `forests` emits no duplicates.
* The invariant is right: a weighted linear forest's isomorphism class is the multiset of its weighted-path classes, and a
  weighted path's class is its amount sequence up to reversal. Including L < k−t (unused budget) is correct and necessary,
  since optimality does not force L = h−1.
* The printed program in Appendix A equals verification/code/original_checker.py (diffed against pdftotext; only form feeds differ).
* Main seat's unmodified verify.py run (finite/run1): both checkers reproduce expected-output.txt, 3099 / 42 / 0 unresolved,
  trace sha a5646def… equals the supplied certificates.jsonl.

## 1. Soundness of every inference rule in §9 (re-derived from §2/§5/§6 only)

**Extension rule, Lemma 9.4 / (9.7) — SOUND.** Re-derivation: an outside x–y path (d ≥ 1 internal vertices, all outside S),
extended along the old path(s) through x and y to z ∈ T(x), w ∈ T(y), is a simple z–w path whose interior avoids Q
(disjointness: same supporting path ⇒ x<y and z<w force z=a, w=b and the segments {a..x},{y..b} are disjoint; different
supporting paths share at most a clique endpoint, excluded by z≠w; the outside interior is outside S). Old paths with x or y
internal are discarded; any subset E of the rest has interiors disjoint from the new path. E + zw is a linear forest iff
deg_E(z),deg_E(w) ≤ 1 and z,w in different components (this also excludes zw ∈ E). Amount A = q + d with q exactly as
defined (|x−z| counts the extension vertices other than z, including x). Lemma 6.2 forbids L+1_{e'≥e} ≤ A ≤ k+1−v', which is
(9.7). Note the rule only ever asserts d ≥ 1; I checked that requiring z < w loses no valid choice (for x<y every valid
endpoint pair has z<w; the swapped same-path choice has overlapping segments). The rule is exactly as strong as Lemma 6.2.

**Required-path rule, Lemma 9.5 — SOUND.** J-path (length ℓ ≤ k, inside X) + outside path with k−ℓ internal vertices (outside X)
= cycle of k+1 vertices; for d=0 the J-path has length k ≥ 5 so the chord xy is not on it. Requires only that J-edges are real
edges, which holds for the initial J (clique edges + expanded path steps) and for trial edges by hypothesis.

**Inheritance, Lemma 9.6 — SOUND** (outside paths relative to X' are outside paths relative to X ⊆ X'; includes d = 0).

**Ball bounds, Lemma 9.7 — SOUND.** b_0: i has ≥ k neighbours and at most n_X−1−|{j:0∈M_ij}| of them in X. u_0=2 when b_0 ≥ t:
a t-clique in N(i)∖X plus i is a (t+1)-clique. Step r: j ∈ A_r(i) has no neighbour in B_{r−1}(i;X) by Lemma 6.4(2) ("if no
such path has parameter 1 ≤ d ≤ r, then y has no neighbor in B_{r−1}(x;X)"); an independent I ⊆ B_{r−1} with |I| = u_{r−1}
has N[I]∖X ⊆ B_r and N[I]∩X ⊆ X∖A_r(i), so expansion (Lemma 2.2) gives (9.9). (9.10): b_r > t ⇒ not a clique (ω = t);
b_r > max(k,2t) ⇒ α ≥ 3 by Lemma 5.3 (needs k ≥ 5, no C_{k+1}, ω ≤ t — all hypotheses of Prop 9.1). Exception (9.11):
if B_r were a clique C then |C| = t = |B_{r−1}| forces B_{r−1} = B_r = C; each v ∈ C has ≤ t−1 neighbours outside X and
misses A_r(i), so k ≤ deg v ≤ (t−1) + (n_X − T_r) ≤ (t−1) + (k+1−t) = k forces N(v)∩X = X∖A_r(i) ∋ i, giving a (t+1)-clique.
(Remark: the exception can only fire at r = 2, since û_1 = 1 forces b_0 < t; harmless.)

**Packing / compatibility, Lemma 9.8 and (9.12) — SOUND.** Exactly Lemma 6.4(1) for two balls (1..r+s+2), Cor 6.5 for
singleton–ball (1..s+1) and singleton–singleton (0 ∈ M_ij means the edge is absent). Distinct bases are required. Sum of
certified independence numbers of pairwise disjoint, anticomplete sets ≤ α(G) ≤ k. Radius pruning ("Removing redundant
radii") is correct: an omitted radius r has u_r = u_q for the last retained q ≥ 0 and strictly weaker compatibility needs;
q+s+2 ≥ 1 so the singleton–singleton case is never invoked. The inclusion/exclusion search is an exact max-weight-clique test.

**Strengthening, Lemma 9.9 — SOUND.** d=0: the hypothesised edge is a real edge of G[S]; d=1: its actual middle vertex
z ∉ S is a real vertex, X = S∪{z}, J' = J + iz + zj is realised. Old entries stay valid (9.6), new entries by 9.5, and either
contradiction (required edge with 0 forbidden, or packing on X with n_X = |S|+1) refutes the hypothesis; the conclusion is
relative to S because z was arbitrary. Batch-adding (Step 3/4) is sound because every trial in a batch uses only prohibitions
already proved; but note that sequential (in-place) addition would ALSO be sound — the "old matrix" convention is a
reproducibility convention, not a soundness requirement (tested as mutation V1 below).

**Procedure, Prop 9.10 — SOUND**; termination by monotone growth of a finite set.

**Nothing in §9 is stronger than §6 proves.** §9 uses only: Lemma 6.1/6.2 (via 9.4), Lemma 6.4/Cor 6.5 (via 9.7/9.8),
Lemma 5.3, Lemma 2.2, ω = t, α ≤ k, no C_{k+1}. It does not use §7–§8 (which need t ≥ 9). Prop 9.1 is stated for any graph
with these properties (not only the minimal counterexample); its proof uses nothing more, so the stronger statement is fine.

## 3. Code vs paper (line-level reading of both checkers)

**original_checker.py** — implements §9 exactly; I found no rule stronger than proved and no missing case.
* `forests` = Lemma 9.2 recursion (keeps extending rejected prefixes; empty tuple consumes a vertex).
* `data` = Lemma 9.3 labels; `tips` = T(x) (9.6).
* `forbidden(k, L=n−t, …)`: subsets E of old edges not having x or y internal (`rest`), degree ≤ 1 tests on z and w,
  forward-reachability `reach` (correct connectivity test for z < w by Lemma 9.3's monotone-route property), `z>=w` skipped,
  `low = L+(e>=len(edges))-q`, `high = k+1-v-q`, `range(max(1,low), high+1)` — exactly (9.7) with d ≥ 1. L is the pattern's
  actual amount n−t, not the budget k−t (correct: unused budget allowed).
* `exact`: state (visited bitmask, endpoint) per start, ℓ = 1..k, records k−ℓ — Lemma 9.5 incl. ℓ = k (d = 0). Copies M,
  so the old matrix is never mutated; for an augmented H the new row/column starts empty (Lemma 9.6 remark).
* `pack`: b_0, u_0 = 1+[b_0 ≥ t], T_r with `req[r]` = {1..r}, b_r, û_r, exception `val==1 and b==c==t and k+1-n+T>=t`
  — exactly (9.8)–(9.11) (b is b_{r−1}, c is b_r at that line). Retains radius r only if u_r > u_{r−1} (paper's pruning).
  `req[0]={0}` is assigned only AFTER the weights are computed (weights only use req[1], req[2]); afterwards
  `req[r+s+2]` gives {0} for two singletons and {1..r+s+2} otherwise — exactly (9.12). Adjacency requires i ≠ j (distinct
  bases). `find` = the inclusion/exclusion search (success iff a clique of weight > k).
* `check`: Step 1 → 1; Step 2 (`exact`, then `bad`) → 2; Step 3 trials skip d ∈ M_ij and d = 0 on required edges, each trial
  `bad(H, exact(H, M))` with the round-start M; additions applied after the loop — the "old matrix" convention holds.
  Outer loops are exactly (9.1).

**independent_checker.py** — imports nothing from the original; implements the same rules by different means: patterns via
partitions/compositions/multisets; initial constraints by building the candidate new system explicitly (segment lists,
explicit disjointness test, union-find linear-forest test) and testing "improves" (A<h and (A>L or A=L with fewer paths)) OR
"closes" (h ≤ A ≤ k+1−v'). I checked this union equals the original's single interval [L+1_{e'≥e}, k+1−v'] (because v' ≤ t
⇒ k+1−v' ≥ h). Packing: per-base branching, all radii kept, witness re-asserted. Required paths: frozenset states.

**Shared (non-independent) elements.** (i) the labelling convention, deliberately identical; (ii) the ball-bound arithmetic —
`ball_options` is a line-for-line transliteration of (9.8)–(9.11) incl. the exception test; (iii) the procedure skeleton and the
(visited, end) state-merging idea for required paths; (iv) verify.py's "trace equals supplied data" is a self-consistency check
of the independent program against its own earlier output, not a third opinion. So the two programs independently cross-check
IMPLEMENTATION, not the RULES: an unsound rule would be replicated in both. That is why §1 re-derives every rule by hand; I found
none unsound.

**Third check (mine, F_work/validate_certs.py).** Written from the paper text, not from either program: initial constraints
re-derived by explicit construction of every candidate new system (subset E × endpoint choice × d) and the Lemma 6.2 interval;
required paths by plain DFS (no state merging); each round's additions re-justified by re-running its recorded trial witness on
MY trial data (fresh vertex, my required-path closure); every packing witness checked against MY ball bounds (weight ≤ my u_r,
b_0 > 0 for balls, distinct bases, (9.12), total > k). Negative controls (F_work/neg.jsonl): bumped weight, spurious initial
flag, deleted rounds, enlarged radius, duplicated base — all 5 rejected; the unmodified record passes. Full run: see §5.

## 4. Lean finite stage (read only, not built)

Same patterns, same labelling, DIFFERENT rule encoding.
* Patterns: `patternChoices t B lower` (CertificateModel.lean) is the same recursion as `forests` (chainChoices = compositions
  with ≤ t−1 parts, `A ≤ A.reverse ∧ lower ≤ A`); per (k,t) the explicit list is pinned by
  `patterns_k_t_coverage : patternChoices t (k-t) [] = patterns_k_t := by decide +kernel`, and completeness for the real system
  is a PROOF (`mem_patternChoices` + `PathSystem.canonical_realization`, which reorients/permutes chains to the canonical form
  and keeps amount and edge count, hence optimality via `optimal_of_same`). 3099 `certificate_N_valid` theorems; FiniteRange.lean
  case-splits exactly the 42 pairs (k ≤ 17 derived by omega from k/2 ≤ t ≤ 8) and `reduced_counterexample_impossible` (same file) routes k ≤ 4 and ω ≥ 9 to the other stages.
* Rules: there are no interval formulas. A certificate is a tree `forbid i j d R N` where the reason R is checked on the
  augmented label graph with d FRESH vertices (`augmentedEdges n E i j d`, realised by `exists_extension` from an actual outside
  path) and is one of: `.system C` (an explicit improved path system, checked against `Improvement` = Lemma 6.2's two cases),
  `.cycle C` (an explicit (k+1)-cycle = Lemma 9.5), `.packing P`, `.edge i j`, or a nested forbid. Ball weights are
  `BallCertificate`s with explicit excluded sets Z (rules `zero`/`succ` mirror (9.8)–(9.11); the stagnation case is stated
  slightly more generally — t ≤ b_{r−1} and n+t ≤ k+1+|Z| — which is still sound by the same argument). Compatibility uses
  radiusCode = radius+1 (singleton 0), giving {0} or {1..code_a+code_b} — identical to (9.12).
* `FiniteCertificate.sound` proves each constructor against Lean's own `PathSystem.Optimal` (amount < k+1−|Q|, maximal amount,
  then minimal edge count — matches §6.1), `OutsidePath`, `outsideBall` (matches (6.5)), `FiniteHyp` (k ≥ 5, 3 ≤ t ≤ k, no
  C_{k+1}, ω ≤ t, α ≤ k, expansion). So the Lean route does NOT rely on the paper's Lemma 9.4 arithmetic or on either Python
  program; it re-checks explicit witnesses in the kernel. Spot check: certificate_0 (k=5,t=3, three singletons) forbids
  0–1 at d=1..4 by explicit systems [[0,3,1],[2]], …, [[0,3,4,5,6,1],[2]] and packs two radius-1 balls of weight 3 — the same
  deductions as the Python trace's initial flags 30 = {1,2,3,4} and witness [[0,1,3],[1,1,3]] (Lean's ball uses Z = ∅, b = 8,
  Python's T_1 = 2, b = 10; both certify weight 3). If the main seat's kernel replay of these 3099 certificates succeeds, the
  finite stage has a third, machine-checked confirmation whose trusted base is the Lean definitions above.

## 5. Third-validator result (F_work/validate_certs.py, full certificates.jsonl)

`records 3099 bad 0 initial mismatches 0` (6 min, one core). I.e. for every one of the 3099 instances: my explicit-construction
initial matrix (Lemma 9.4 via Lemma 6.2, built independently) is IDENTICAL to the trace's `initial` flags; every recorded
round addition (all d ∈ {0,1}) is re-justified by its witness on my own trial data; every final packing (all 3099 finals are
packings) is valid under my own ball bounds. The negative controls in §3 show the validator can fail.

## 6. Mutation tests on COPIES of original_checker.py (F_work/mutate.py; each replacement asserted to match exactly once)

Control (unmodified copy): output byte-identical to expected-output.txt (0 / 3049 / 50). Weakening = a rule deleted or
weakened (still sound, should FAIL to exclude something if the rule does work). "rc 124" = per-mutation wall timeout
(900 s for W1, 300 s for the rest); counts are over the k values completed, which is enough because out0 > 0 is decisive.

| mutation | k done | out0 (NOT excluded) | out1 | out2 | verdict |
|---|---|---|---|---|---|
| W1 no extension rule (Lemma 9.4) | 5–14 | 304 | 0 | 847 | load-bearing |
| W2 extension lower bound ignores min-e tie-break (always L+1) | all | 8 | 3028 | 63 | tie-break load-bearing (8 patterns) |
| W3 extension upper bound k−v'−q (one short) | all | 0 | 2907 | 192 | top endpoint not needed for exclusion (only shifts 1→2) |
| W4 E = ∅ only (no retained old paths) | 5–13 | 190 | 38 | 608 | subsets E load-bearing |
| W5 E = all eligible old paths only | all | 8 | 950 | 2141 | proper subsets needed for 8 |
| W6 no required-path rule (Lemma 9.5) | all | 50 | 3049 | 0 | every output-2 case needs it |
| W7 no strengthening (stop after Step 2) | all | 46 | 3049 | 4 | Step 3 needed for 46; 4 close at Step 2 (= the 4 traces with 0 rounds) |
| W8 no d=0 trials | all | 18 | 3049 | 32 | load-bearing |
| W9 no d=1 trials (fresh vertex) | all | 17 | 3049 | 33 | load-bearing |
| W10 no exception (9.11) | all | 4 | 3042 | 53 | the exception IS load-bearing (4 patterns) |
| W11 no size-test triple (Lemma 5.3) | 5–13 | 103 | 570 | 163 | load-bearing |
| W12 u_0 without the clique-pair rule | all | 14 | 3046 | 39 | load-bearing |
| W13 T_r = 0 (no excluded neighbours, Lemma 6.4(2)) | 5–12 | 499 | 26 | 0 | load-bearing (massively) |
| W14 no singleton options | all | 5 | 3048 | 46 | load-bearing (5 patterns) |
| W15 no radius-2 balls | 5–13 | 77 | 587 | 172 | load-bearing |
| W16 no radius-1/2 balls | 5–12 | 521 | 4 | 0 | load-bearing |
| W17 ball growth term removed (b_r = b_{r−1}) | 5–12 | 521 | 4 | 0 | load-bearing (expansion step) |
| W18 no "b_r > t ⇒ pair" in balls | 5–12 | 517 | 8 | 0 | load-bearing |
| W19 no size test and no exception | 5–13 | 107 | 560 | 169 | load-bearing |
| W20 singleton–singleton never compatible | all | 1 | 3049 | 49 | the req[0]={0} case is load-bearing (1 pattern) |
| V1 in-round updates applied immediately (still sound) | all | 0 | 3049 | 50 | output IDENTICAL: the "old matrix" convention is reproducibility, not soundness |

Exception (9.11) — which patterns need it: exactly the four all-singleton patterns with t = k (k = 5,6,7,8). Hand check for
k = t = 5, S = Q: the extension rule forbids d = 1..4 between clique vertices; b_0 = 1, u_0 = 1; b_1 = 5·1+1−5+4 = 5 = t,
u_1 = 1; b_2 = 5 = t with k+1−n+T_2 = 5 ≥ t, so (9.11) gives α(B_2(q)) ≥ 2 (genuinely: if B_2(q) were a clique it equals
B_1(q), has 5 vertices each missing the other 4 clique vertices, so each is adjacent to q ⇒ K_6). Packing B_2(q) (2) + B_0(q')
for the other four (1 each; ball–ball needs 1..4 and 1..2, both proved) = 6 > 5. Correct.

**Strengthenings (unsound or wrong rules) — what the output can and cannot see:**

| mutation | out0 | out1 | out2 | visible in Table 2? |
|---|---|---|---|---|
| S1 extension lower bound drops the indicator (forbids A = L even when e' ≥ e) | 0 | 3087 | 12 | yes (split changes) |
| S2 extension upper bound k+2−v'−q | 0 | 3083 | 16 | yes |
| S3 compatibility needs only 1..r+s+1 | 0 | 3070 | 29 | yes |
| S4 size test with ≥ instead of > | 0 | 3051 | 48 | yes |
| S5 no connectivity (reach) test in Lemma 9.4 | 0 | 3067 | 32 | yes |
| **S6 no degree ≤ 1 test on z,w in Lemma 9.4** | 0 | 3049 | 50 | **NO — byte-identical output** |
| S7 required-path rule records k−ℓ+1 instead of k−ℓ (wrong, not merely stronger) | 3 | 3049 | 47 | yes (now fails) |
| S8 u_0 = 2 already when b_0 ≥ t−1 | 0 | 3052 | 47 | yes |
| S9 req[0] left empty (two singletons always compatible) | 0 | 3063 | 36 | yes |

S6 is the instructive one: dropping the degree test adds UNPROVED forbidden parameters to the initial matrix of 2471 of the
3099 patterns (e.g. k=6, t=4, P=((),(1,1)): d=1 between labels 0 and 3, which no valid system justifies — I checked by hand
that 0–o–3 yields neither an improvement nor a C_7), yet the printed table is identical. So "both programs reproduce every row
of Table 2" (§9.6, App. A) cannot by itself certify that the rules are implemented as proved. What does certify it here:
(a) line reading (the degree test IS in both programs); (b) the original's `initial()` matrices equal the trace's `initial`
flags for all 3099 records (checked); (c) those flags equal my explicit-construction derivation for all 3099 (§5). Recommendation
(EXPOSITION, not a gap): verify.py should check the initial matrices / trace against an explicit-construction derivation, not
only stdout rows.

## 7. Objections (all EXPOSITION; no GAP, nothing FATAL)

E1. Lemma 9.4: "Let E ⊆ ℰ(P) consist of old endpoint edges whose represented paths do not contain x or y in their
interiors." Read literally this fixes E as THE set of all such edges; the rule (and both programs, and the later sentence
"over all allowed choices of z,w,E") uses every SUBSET. Mutation W5 (E = the full set only) leaves 8 patterns unexcluded, so
the subset reading is load-bearing. Fix: "Let E be any subset of the old endpoint edges whose …". EXPOSITION.

E2. §9.6 / Appendix A: "Two implementations … give the same results in Table 2" and "Both complete runs give every row of
Table 2." Row agreement is an insensitive witness of rule fidelity: removing the degree test from Lemma 9.4 (an unsound
strengthening that adds unproved entries to 2471 of 3099 initial matrices) reproduces expected-output.txt byte for byte. The
code is in fact correct (read; and initial matrices = trace = explicit construction for all 3099), so this is not a gap, but
verify.py should compare matrices/traces against an explicit-construction derivation rather than rely on stdout rows, and
the two programs share the ball-bound arithmetic verbatim, so their agreement does not independently test (9.8)–(9.11).
EXPOSITION / methodology.

Minor: (9.11) can only fire at r = 2 (û_1 = 1 forces b_0 < t); it is needed for exactly the four t = k all-singleton
patterns (k = 5..8), which I hand-checked for k = 5.

## 8. Artefacts (all under /tmp/oaimath/189/seats/F_work/)
enum_own.py (own enumerator + gf), cmp_sets2.py (set equality vs both programs + trace), validate_certs.py (+ neg.jsonl,
negctl.py; validate.log = `records 3099 bad 0 initial mismatches 0`), mutate.py (+ mut/*.py copies, mutate_part1.log [W1],
mutate2.log [rest]), s6lib.py/w10lib.py (pattern-level diagnosis of S6 and W10). Nothing outside seats/ was modified.
