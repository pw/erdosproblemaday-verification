  {
    slug: "181-openai-hypercube-ramsey-refereed",
    problemNum: 181,
    title: "#181: OpenAI's proof that R(Q_n) = O(2ⁿ) — 172 pages read by nine hostile seats, sources checked, and a third-party Lean 4 kernel check we are replaying",
    date: "2026-10-11",
    status: "in_progress",
    originatedByUs: false,
    summary:
      "Burr and Erdős asked in 1975 whether the Ramsey number of the n-dimensional cube is bounded by a constant times its " +
      "number of vertices. Fifty years of upper bounds got the exponent from 2n+o(n) down to (2−c)n; OpenAI's 23 September " +
      "2026 paper claims the whole conjecture, R(Q_n) ≤ C·2^n, in 172 machine-written pages with no Lean. We read it in nine " +
      "sectioned hostile seats briefed to refute, checked every cited theorem against its source, found that the same third " +
      "party who formalized OpenAI's Hindman proof has published a 752-file Lean 4 proof of exactly the Formal Conjectures " +
      "statement — and our own kernel replay of it is running as this goes live. Verdict on the paper as written: holds as read, nine seats out of nine — no mathematical gap, one exposition gap (Lemma 18.1), one step taken on trust (§9.1), and no hidden rate on N/2^n anywhere.",
    body: `
<p><strong>The problem</strong> (<a href="https://www.erdosproblems.com/181">erdosproblems.com/181</a>; community
database status OPEN as of our 11 October refresh). <em>Let Q<sub>n</sub> be the n-dimensional hypercube graph (2<sup>n</sup>
vertices, n2<sup>n−1</sup> edges). Prove that R(Q<sub>n</sub>) ≪ 2<sup>n</sup>.</em> Burr and Erdős raised it in 1975 as
the sharpest test of their conjecture that bounded-arboricity families have linear Ramsey numbers: the cube has
n/2 = ½log<sub>2</sub>|V| edges per vertex, the largest density their own first-moment bound permits a linear family to have.
The lower bound is 3·2<sup>n−1</sup> − 1 (two red blocks, blue between). Upper bounds: Graham–Rödl–Ruciński 2001 gave
8(16n)<sup>n</sup>; Shi (2001, 2007) made it polynomial in 2<sup>n</sup>; Fox–Sudakov n·2<sup>2n+5</sup>; Conlon–Fox–Sudakov
2<sup>2n+6</sup>; Lee's degenerate-graphs theorem (Annals 2017) (1+o(1))2<sup>2n</sup>; and Tikhomirov (2022, EJC 2024)
2<sup>2n−cn+1</sup> + 2 with c ≈ 0.0366 — the first exponent below 2. Our own <a href="/report/181">July working report</a>
audited that literature and re-verified a finite case; it did not touch the asymptotic question.</p>

<p><strong>What OpenAI claims.</strong> <em>The hypercube Ramsey number has linear order</em> (23 September 2026, family 171
of the 6 October release, 172 pages, no Lean in the release). Theorem 1.1: there is an absolute constant C with
R(Q<sub>n</sub>) ≤ C·2<sup>n</sup> for every n ≥ 0 — the conjecture exactly, with no numerical value for C and, the paper says
plainly, no information about whether R(Q<sub>n</sub>)/2<sup>n</sup> converges.</p>

<p><strong>How the proof is built</strong> (plain version). It is a proof by contradiction along a sequence. If the ratio
R(Q<sub>n</sub>)/2<sup>n</sup> is unbounded, Lemma 2.1 produces dimensions n → ∞ and two-colourings between two disjoint host
sides of size N each, with no monochromatic cube across the sides, N ≤ n2<sup>n</sup> and C<sub>n</sub> = N/2<sup>n</sup> → ∞
<em>at no prescribed rate</em>. Everything after that is "eventually along this sequence". Lemma 3.2 is the compactness
engine: for any countable list of patch properties, pass to a subsequence and throw away o(N) labels so that each property
is either eventually absent or <em>available</em> — survives every removal of a fixed fraction κN of labels. The first twelve
sections prove <em>discrepancy</em>: every pair of probability laws on the two sides, within the width budgets in play
(width = log of N times the largest atom), sees edge density within a vanishing error of ½ in both colours — because any
available bias, purity, polynomial density cap, small-grid purity, asymmetric purity, intermediate bias exponent, full-dimensional
cluster or "linear-budget jump" is shown to yield a monochromatic cube directly (Sections 4–11), each construction paying its
local repetitions and predictive tests out of the density surplus it assumes. Section 13 then extracts disjoint host patches of
one colour, one orientation and one of finitely many modes, and allocates the cube to them as subcubes fixed by initial
coordinates with dyadic weights rounded from the patch masses (Kraft equality makes the prefix code exact; the retained patches
carry more than half the mass; each role has ℓ<sub>i</sub> "crossing" edges into other patches, with ℓ<sub>i</sub> and
log(N/M<sub>i</sub>) both charged to the patch's gain budget s<sub>i</sub>/(1000u)). The gain is the (M/N)(1+2δ)<sup>n</sup>
story from §1.3: n independent restrictions that each keep a label with probability ½+δ leave M(½+δ)<sup>n</sup> labels, so a
density surplus can pay for a smaller support. When the surplus is large (Section 15) the odd roles are assigned injectively
and the even roles get weights supported on their common neighbourhoods whose column sums are O(1/C<sub>n</sub>); Hall's
theorem does the rest. When the surplus is small or zero (Sections 16–18, including the bounded case of one patch of size
≍ N with no gain at all) a fixed linear map on cube words sorts the odd roles into syndrome classes — the coordinate IDs are
distinct, so an even role has at most one neighbour in each class — and O(log n) late classes get provisional labels that are
replaced one class at a time from reserved host sets; each even role ends with two random candidates adjacent to all its
assigned neighbours, and Hall fails only when the multigraph on labels with one edge per even role has a connected component
with more edges than vertices. That is where the "no rate" promise is cashed: the expected number of such components is
bounded by e<sup>O(r)</sup>·M·(K/C<sub>n</sub>)<sup>ηn</sup> plus a convergent small-set sum, and
n·log 2 + ηn·log(K/C<sub>n</sub>) → −∞ "however slowly C<sub>n</sub> → ∞" once C<sub>n</sub> exceeds a fixed constant.</p>

<p><strong>What we checked ourselves</strong> before the seats reported: Lemma 3.2's dichotomy with its quantifiers written
out (the negation of "available" is an infinitely-often statement, and the proof applies the dichotomy member by member, which
is what makes "an available finite union has an available member" sound); Lemma 3.7, the gated posterior comparison, which is
a two-line Bayes bound once the selection event is inside the likelihood; the dyadic allocation of §13.2 (the first segment of
decreasing dyadic weights to reach 1 reaches it exactly, and Σ<sub>J</sub> M<sub>i</sub> &gt; S/2 because each weight is below
twice its mass); the endpoint-multigraph count of §18.5 (a connected Hall-violating p-set needs two mergers beyond its spanning
tree; integrating leaves at K/M each and the two surplus edges at M<sup>−2</sup>e<sup>.01n</sup> gives K<sup>p</sup>M<sup>−p−1</sup>e<sup>.02n</sup>,
as printed); the §15 union bound N·(K′/C<sub>n</sub>)<sup>n</sup> = o(1), which uses N ≤ n2<sup>n</sup> and nothing about the rate
of C<sub>n</sub>; and Lemma 16.1's syndrome classes. None of this is a check of the 150 pages in between — that is what the
seats were for.</p>

<!-- PAPER_AS_WRITTEN:BEGIN -->
<p><strong>The paper as written — a nine-seat hostile read.</strong> We refereed the 172-page preprint the way we refereed
OpenAI's Hindman paper for <a href="/day/172-openai-hindman-sums-products-refereed">#172</a>, scaled to its length: seven
tool-equipped Opus seats with disjoint scopes over the mathematics (§2–3 the probabilistic framework; §4–5; §6–7 through the
first discrepancy milestone (7.2); §8–9; §10–12; §13–15; §16–18 and the final matching), one over the bibliography and the live
world, and one over the Lean source — each briefed that the base rate for a machine-written 172-page proof of a famous
conjecture being correct is low, that its job was to find the sentence where it fails, to fetch every cited theorem from its
current source rather than from memory, to track every constant's dependencies, to hunt for any hidden rate on
N/2<sup>n</sup> → ∞, and to say which steps it verified line by line and which it only skimmed. Every objection below carries its
quote in the bundle; the seats' own lists of what they skimmed are the honest edge of this read.</p>

<p><strong>§2–3, the framework (seat: framework) — HOLDS AS READ.</strong> Lemma 2.1 loses nothing (no later section uses an
edge inside a host side; N ≤ n2<sup>n</sup> is used only for unions over e<sup>O(n)</sup> labels). Lemma 3.2's dichotomy is exact:
"not available" is precisely liminf τ<sub>n</sub>/N = 0, i.e. eliminable by o(N) removals along a subsequence; the diagonal choice
keeps total removals ≤ N/j; the finite-union clause is correct when read as "available along no subsequence" (the seat wrote a
cleaner pigeonhole proof); every later invocation runs over countably many rational parameters. Lemma 3.3's K = 4/κ depends on
the counterexample sequence, not on nothing — and at every use checked it only multiplies negative powers of n or terms beaten by
C<sub>n</sub> → ∞, so no circularity. Lemmas 3.5–3.10 re-derived; 35+ later invocations spot-checked against their hypotheses,
the §4 uses of 3.6–3.9 line by line including the recomputation of selection inside the likelihood. One lead was run to ground:
the formalizers' design note records that their first decomposition of Lemma 3.9 (calibrated near-product injections) was
<em>false</em> — it claimed every completed atom is at most 10/d, when only the dummy atoms are O(1/d), and it took an existential
"some injection law has additive singleton error" that cyclic shifts satisfy while breaking (3.2). The paper's text avoids both
traps: it says only the dummy rows' atoms are O(1/d), proves the joint bound for one specific sequential sampler conditioned on
its tracking event, and gets exact marginals by separation inside the set of laws satisfying the joint bounds. Exposition notes:
Lemma 3.8 is stated in n but §14 applies it to an internal dimension h that may stay bounded (valid — the thresholds depend only on
fixed parameters and Q<sub>0</sub> is chosen after them — but unsaid). Fetched and matching: Erdős–Lovász §2, Lu–Székely Lemma 3,
Lipschitz percolation, dependent rounding (P1)–(P3), Hoeffding, Azuma, Freedman. Not fully checked: the ball-intersection exponent
in Lemma 3.8 Step 3, the branching domination in Lemma 3.10 Step 5, the mesh-limit argument's constants.</p>

<p><strong>§4–5 (seat: initial_a) — HOLDS AS READ, no gap of either kind.</strong> Lemma 4.1 re-derived from the rendered pages:
plateau and trimming, the coordinate-key gadget, validity of tuple sets with the Azuma dip count, marking and height choices, the
posterior bound |S| ≥ N·e<sup>−(log 2 − c₂a*/2)n</sup>, mask balancing via Kakutani, the Hall step. Selection is recomputed as the
tuple varies (the gate reads only preparatory data; the reference law deletes the whole tuple). Lemma 5.1 checked through every
displayed estimate — the parent/stream construction with a₀ = 1/3, prefix-deletion and block-reconstruction tests, the odd-row
comparison P ≤ e<sup>a₃k</sup>Q<sub>c</sub>, the minimax common high-row law, the selection correction for low rows,
F<sub>z</sub> ≤ e<sup>a₆kn</sup>Q, the posterior density e<sup>τ₀kn</sup>, the even-row cap O(e<sup>τ₁n</sup>), three-level odd column
sums, the clock-lemma interface, Hall. Two corrections to our own brief: §5.4 is not a Kakutani application but Markov plus the
local lemma in five stages; and τ₁ &lt; log 2 is not the operative condition — what is needed is τ₁ &lt; log 2 − H<sub>bin</sub>(2ρ)
acting on the repeat term of the scattered-moment bound, with ρ chosen after τ₁, no cycle. Constant order q₀ → a<sub>i</sub>, δ → K<sub>h</sub>,
η → K₁ → K₂ → K₀ → K<sub>D</sub> → K<sub>s</sub> → K<sub>B</sub> → α → height exponents; none depends on n, the witness or the removed sets.
Minor: Lemma 4.1 uses "bad sequence" and "current sets" without defining them; log q ≥ −log 2 + .7a<sub>i</sub> stated without proof
(true for a<sub>i</sub> ≤ ½); §5.4 Stage 4 justifies a product over J → ∞ variables by "(1+o(1)) per variable", which is not enough as
written though the product is e<sup>o(s)</sup> — the one place where the stated reason is not the real one; the observation-record
counts on p. 39 asserted, not derived. No rate on C<sub>n</sub>: it enters only through |A|/N, |B|/N → 0.</p>

<p><strong>§6–7 and the first milestone (seat: initial_b) — HOLDS AS READ.</strong> (7.2) is reached by stabilizing three fixed
properties in order: a violation of (7.1) would, by Lemma 3.3 and Lemma 6.1 with the sides swapped (γ = ¼, p₀ = c/2), give a cube,
so it is eventually absent; purity at widths 2n<sup>d/4</sup> with defect ≤ e<sup>−n<sup>h</sup></sup> would, by Lemma 7.1 with p = h/2,
contradict (7.1); with purity absent, Lemma 4.1 excludes bias at widths n<sup>d/4</sup>. So η₀ = h = d/(4·10⁹), an absolute constant:
D* → D₀ → d → (b, c, h) → η₀ with no cycle, D* genuinely universal (it enters only through η ≤ n<sup>2D*</sup>Λ with 2D* &lt; d₀, and d₀
depends on nothing in the inputs). Re-derived: e<sup>.4kn</sup>, O(e<sup>.55n</sup>), n<sup>d/2</sup> + 2cn<sup>d</sup> log n, .04n<sup>4d</sup>;
Lemma 7.1 Steps 1–6; Lemma 6.1 Steps 1–3 with the three-stage conditioning, the marking/maximality argument and both load
cancellations; the selection bias handled three different ways for even rows, low odd rows and high odd rows. Lemma 3.2 is applied
here to a list of three fixed properties, so countability never arises. Cosmetic: the swapped Lemma 6.1 is never stated; two O(1)
caps are really O(K); no tie-break in the marking rule; Lemma 3.9 applied "with d = N" when the retained side is smaller (pad with
zero-mass labels); d not declared rational. Unclear only by dependency: the §6.2 descriptor counts rest on §5.3's state geometry.</p>

<p><strong>§8–9, asymmetric widths and the intermediate bias exponents (seat: asymmetric) — HOLDS AS READ, with one step the
seat could not check line by line.</strong> All twelve steps of Lemma 8.1, Corollary 8.2, Definition 9.1, the parameter selection
of Proposition 9.2, §9.2 (core erasure, the covariance tail, the Finner/Hoeffding concentration) and §9.3 re-derived. "No relation
p &gt; τ is required" is correct — every use of p needs only e<sup>−n<sup>p/2</sup></sup>·poly(n) → 0. Corollary 8.2's list of width
pairs is countable (rational pairs, the exponent a function of the pair), so Lemma 3.2 applies, and the one downstream use needs one
pair. H<sup>†</sup> and H<sub>L</sub><sup>†</sup> are well-defined monotone limits in [0, ∞]; the case split is exhaustive, with
H<sup>†</sup> = 1, H<sub>L</sub><sup>†</sup> = 1, H<sup>†</sup> = ∞ and H<sup>†</sup> = 0 all covered and nothing concluded at an
infimum. Separate dependency graphs for the two cases of Proposition 9.2 — the appendix warns they use different parameter orders —
have no cycle and no constant depending on n. Selection is recomputed where the hidden tuple varies (§8 Steps 6–7); in §9 the
center map is fixed in advance, so there is nothing to recompute. Finner's inequality fetched from Project Euclid and matching
(its §3 allows Σ1/p<sub>j</sub> ≤ 1 on probability spaces, the form used). No rate on C<sub>n</sub>. <strong>The unchecked step,
§9.1 (pp. 81–82), UNCLEAR:</strong> the map assigning each cube position to a nearby center is built by "adapting Steps 2–4 of
Lemma 3.8", but Lemma 3.8's stated hypotheses do not cover this case — the radius n<sup>σ</sup> is not one the lemma allows (fitting
it to the small-radius option would need b &gt; 2.97 where the lemma requires b &lt; 1), the paths cross slices and the crowd tests
are replaced by three new ones, and the Lipschitz step (Step 5) is used but not mentioned. Every exponent condition the sketch
states was checked and none fails (base case, overlap estimate, the ratio χ/2 &gt; a + 4σ<sub>h</sub>, configuration count, the union
over 2<sup>n</sup> sites); the induction itself is two paragraphs of sketch, and the construction is genuinely needed — simpler
coverings give too many centers for the width budget. An exposition gap rather than a known mathematical one; it is the one place
in the proof where a referee has to take "the same argument" on trust. Minor: "we call these the base gates" in §8 can be read as
excluding the η<sub>g</sub>, Z<sub>g</sub> bounds Step 4 needs; §9.3 reuses one constant c for two roles where the charge constant must be
strictly smaller; Lemma 3.10 applied without stating B (B ≥ 2 is needed; §8 uses 3); ρ and σ clash with Lemma 3.8's symbols.</p>

<p><strong>§10–12, cluster exclusion, the linear-budget jump and deep discrepancy (seat: cluster) — HOLDS AS READ.</strong>
Every displayed inequality on pp. 89–111 re-derived, the borderline arithmetic checked numerically: Proposition 10.1's list test
(10.1), eligibility rule, tilt tails, the e<sup>.1m</sup> mean cap and the likelihood bound (10.2), the posterior and "light part" step,
column-sum concentration, and the clock-lemma and Lemma 3.6 hypotheses; Corollary 10.2 including its second use in Lemma 13.2
(a valid rational δ exists because a<sub>C</sub> &lt; min(η₀,1)/10⁶); the §11 slice experiment, Lemmas 11.2 (Kakutani's closed graph
checked) and 11.3, §11.3, Corollaries 11.4 and 12.1; Lemmas 12.2–12.6 in full; Appendix A's rows and Figure 1 agree with the text
and the dependency order has no cycle. The reverse-orientation discrepancy n<sup>−.95</sup> that Proposition 11.1 needs comes from
neither Corollary 8.2 nor 12.1 but from the case hypothesis H<sup>†</sup> ≥ 1 in the reversed orientation via Definition 9.1 — not
circular. The sharpest budgets hold with margin: n·b<sub>*</sub> = n<sup>.05</sup> ≪ gh = n<sup>.09</sup>, and the deep error
n<sup>−.96</sup> needs b<sub>*</sub> = o(n<sup>−.94</sup>) and b<sub>*</sub> &lt; n<sup>−.905</sup>. Selection is recomputed when the hidden
tuple varies, in L<sub>w</sub> (p. 94) and F<sub>w</sub> (p. 98). No rate on C<sub>n</sub>. Thirteen exposition objections, two of which
matter: on p. 93 the supremum defining w<sub>ℓ,c</sub> must be read as over eligibility sets of size ≥ .99λ — under Lemma 3.8's
generic ≥ λ/3 reading the per-slice sum becomes 3 and the claimed bound N·max p̂<sub>b</sub> ≤ e<sup>.1m</sup> fails; the text supports
the .99λ reading, so the claim holds as intended, but a reader who takes the lemma's own constant will think it broken. And on
pp. 92 and 96 the independence of well-separated roles rests on a "primitive domain" locality claim whose distance arithmetic
checks but whose measurability is asserted rather than proved — the one structural point in this scope worth confirming against the
Lean. Hamming 1950 §3 (archive.org scan) and Azuma's Remark 1 fetched and matching.</p>

<p><strong>§13–15, allocation and the high modes (seat: allocation) — HOLDS AS READ.</strong> All of §13 checked: the cluster
witness Lemma 13.2 builds really is a Corollary 10.2 witness; fixing one colour and one orientation is a pigeonhole over twenty types
at each n — and necessary, since the host is bipartite and every patch must send odd roles to the same side; the dyadic rounding is
as we read it; crossing edges go to distinct leaves and are crossings from both ends, matching Conlon–Fox–Lee–Sudakov's
Proposition 2.2(ii) (fetched); labels in different patches are distinct because the patches are; the N/3 reserve is set aside
before extraction and used only in §16; the budget ℓ<sub>i</sub>, log(N/M<sub>i</sub>) ≤ s<sub>i</sub>/(1000u) holds for every
retained patch, with the size constant c independent of Q₀, which it needs to be; Lemma 13.4's three degree windows, clique
exclusion and mesh stability check. §14: (14.1), the likelihood bound, the cap N·max σ<sub>v</sub> ≤ 2<sup>h</sup>e<sup>−500s</sup>, the mean
bound Eσ<sub>v</sub> ≤ K/M<sub>i</sub>, Kakutani's hypotheses in Proposition 14.2 and max π<sub>i</sub> ≤ 11/M<sub>i</sub> at the fixed
point all re-derived; fixed low-mode scales are fine inside §14 because the estimates only need scales above Q₀. §15: Lemma 15.1 in
full including the clock lemma with B = 5 and the union bound N(K′/C<sub>n</sub>)<sup>n</sup> → 0; both cluster-history alarms; Lemma
15.2; the small/large-bin scale relations; and the Hall step — odd labels injective across patches, even rows supported on common
neighbours of <em>all</em> odd neighbours including crossings, normalization preserving column sums ≤ 1. Two UNCLEAR, both exposition:
in Proposition 15.4 the order of comparisons and reverse integration for small-bin repeats is asserted rather than derived (every
cost exponent checks); in Proposition 15.3 the seat did not confirm that the certificate events' dependency graph is exactly the one
Lemma 3.5 requires. No rate on C<sub>n</sub>: the high modes need C<sub>n</sub> above an absolute constant and N ≤ n2<sup>n</sup>.</p>

<p><strong>§16–18, the low modes and the final matching (seat: lowmodes) — HOLDS AS READ, with one exposition gap.</strong>
Lemma 16.1 by hand: the syndrome map, class sizes 2<sup>n−1</sup>/H<sub>*</sub>, at most one neighbour per class, at least ⌊j/2⌋
neighbours in the last j classes, at most one late internal neighbour. Lemmas 17.1–17.3 and Proposition 17.4 hold; the polynomial
slack of the bounded regime comes from deferring the p(v) ≥ A₀log n/2 late hits (Lemma 17.1). Injectivity: early labels sit in
disjoint cells and patches outside the reserve, late labels come from disjoint late pools, injective within each class. Adjacency:
each even role's two candidates hit every odd neighbour — internal, bulk, crossing, and late after replacement. Lemma 18.6 as we read
it: tree diagrams give p+1 classes, a violator needs two further merges with two edges at the maximum weight, both sums vanish. Every
occurrence of C<sub>n</sub> in §16–18 traced: the facts used are C<sub>n</sub> → ∞, N ≥ 2<sup>n</sup>, N ≤ n2<sup>n</sup> — no rate.
<strong>The gap, Lemma 18.1 (p. 149):</strong> the proof says <em>"For a target sketch, its empirical hit fraction H(y) … has mean
.5 + O(b<sub>*</sub>). In its second moment, nonconflicting pairs contribute .25 + O(b<sub>*</sub>) by (18.2)"</em> — but (18.2) covers
only labels in D<sub>v</sub><sup>0</sup> and nonconflicting pairs there, and the lemma's hypotheses never say the sketch entries lie in
D<sub>w</sub><sup>0</sup>. As worded for arbitrary side data the implication is false: the formalizers built a finite model satisfying
both requirements with zero retained mass, and the seat checked it. The missing premise — every sketch entry lies in
D<sub>w</sub><sup>0</sup> — holds automatically on the paper's own gate (the sketch is drawn from τ<sub>w</sub><sup>j</sup>, supported in
D<sub>w</sub><sup>0</sup> unless the fallback point mass is used, which the gate rules out; a fallback sketch would also break
Requirement 1 by itself), and the paper states the support condition explicitly in the parallel spot in Lemma 18.2. Two seats
reached this independently — the Lean source audit found the formalizers' record of it, and the §18 seat confirmed it from the
text. The conclusion is true; the wording is incomplete. That is the only gap of any kind in the proof that this read found.
Cosmetic: Proposition 18.4 applies the clock lemma with its dimension parameter replaced by e<sup>n<sup>δ′</sup></sup> without the
lemma saying its parameter is arbitrary; Proposition 16.3 imports §15.2's capacity certificates at target .2 without redoing the
constants (not fully checked). Moser–Tardos, Haeupler–Saha–Srinivasan Theorem 2.2, Harris–Srinivasan, Lu–Székely all fetched and
matching.</p>

<p><strong>The bibliography and the live world (seat: citations) — ACCURATE.</strong> All 34 references exist; all 31 DOIs
resolve and Crossref or zbMATH matches every author list, title, venue, volume, issue and page range; both renyi.hu links serve the
right Erdős scans; the LaTeX source carries the same 34 entries in the same order. Every theorem-number citation in §1.1–1.2 was
read in its source and quoted beside the paper's paraphrase: Burr–Erdős's L-set definition in §1, Lemma 3.3, Lemma 4.3 and the §7
cube question; Graham–Rödl–Ruciński's Theorem 1 with its strict inequality; Fox–Sudakov Corollary 1.3 and Lemmas 2.1–2.2;
Conlon–Fox–Sudakov Corollary 4.2 and §4; Lee's Theorem 1.3 and the paragraph after it giving 2<sup>2n</sup> + n²2<sup>n</sup>;
Tikhomirov's Theorem 1.1 and Corollary 1.2; Gowers §4 Lemma 11; Sudakov §2; Kostochka–Rödl Lemma 1; the main theorems of
Conlon–Fox–Lee–Sudakov, both Fiz Pontiveros–Griffiths–Morris–Saxton–Skokan papers and Mota–Sárközy–Schacht–Taraz. Chvátal–Rödl–
Szemerédi–Trotter, Beck and Shi 2007 could be checked only through secondary sources, which agree. The paper's own small arguments
are right: the 3·2<sup>n−1</sup> − 1 two-block lower bound, the reflected Gray code (checked by script for d ≤ 8 with a negative
control), the F<sup>□k</sup> ⊆ Q<sub>dk</sub> embedding. Known exact values are R(Q₂) = 6 and R(Q₃) = 13 (Lidický–Pfender 2021); no
published bound on R(Q₄). Four cosmetic notes: "[3, Section 3]" needs §1 as well; Tikhomirov's Corollary 1.2 exists only from arXiv
v3 (2 March 2024) on; "Sudakov explicitly drew on Gowers" overstates Sudakov's "was influenced by"; an orphan source file
<code>01-regime-guide.tex</code> never reaches the PDF. No fabricated bibliographic detail anywhere.</p>

<p><strong>Novelty.</strong> No human proof of R(Q<sub>n</sub>) = O(2<sup>n</sup>) and no improvement on Tikhomirov anywhere we could
look (arXiv sweeps, the Erdős-problems site and forum, Tao's post, MathOverflow, Hacker News, Mathstodon, press). The preprint is not
on arXiv; it was never revised after its 6 October commit; openai/math has issues and discussions turned off, so no public correction
can be filed there. OpenAI's own Lean library proves 2<sup>n</sup> ≤ R(Q<sub>n</sub>) ≤ 4<sup>2<sup>n</sup></sup> and the Lemma 2.1
reduction, nothing more. erdosproblems.com/181 shows no status and does not mention OpenAI; Bloom's 8 October post lists the claim as
"not formalised" under his blanket disclaimer; the teorth database still says OPEN and unformalized; no comment from Tao, Conlon, Fox,
Sudakov, Tikhomirov or Lee.</p>

<p><strong>Verdict on the paper as written: HOLDS AS READ, nine seats out of nine; no mathematical gap found.</strong> What the
read did find, in order of weight: one <em>exposition</em> gap (Lemma 18.1's second-moment step needs a support premise the lemma's
wording omits and the gate supplies — found independently by the §18 seat and, through the formalizers' own notes, by the Lean seat);
one step taken on trust (§9.1's center map, "adapting Steps 2–4 of Lemma 3.8" outside that lemma's stated hypotheses — every exponent
condition checks, the induction is a sketch); one reading that is load-bearing (p. 93's supremum must be over ≥ .99λ eligibility sets,
which the text supports and Lemma 3.8's own constant would not); one asserted measurability (pp. 92, 96); two compressed orderings in
§15; a "(1+o(1)) per variable" in §5.4 that is not the real reason the product is small; and a few dozen cosmetic notes — undefined
terms in Lemma 4.1, reused symbols, lemmas applied to parameters they were not stated for (Lemma 3.8 on an internal dimension h, the
clock lemma with an exponential dimension), unstated tie-breaks and B values. Every one of these has its quote in the bundle, and
every one, where the seat could decide, resolved in the paper's favour. The one place every seat was told to hunt — a hidden rate on
N/2<sup>n</sup> → ∞ — came back empty nine times: the only facts used are C<sub>n</sub> → ∞, N ≥ 2<sup>n</sup> and N ≤ n2<sup>n</sup>,
and every threshold on C<sub>n</sub> is a fixed constant. What this is not: a human expert's reading, or a check of every constant —
the seats' skimmed lists (Lemma 3.8 Step 3's exponent, Lemma 3.10 Step 5's branching domination, the exact record counts on pp. 38–39
and 42–44, the exact exponents of Lemma 18.2's block protocol, the §14.2 eligibility logic, Proposition 16.3's imported certificates)
are the edge of this read — and a referee that finds nothing is weaker evidence than a kernel that accepts a proof, which is why the
formal object below carries the label and this section carries the register.</p>
<!-- PAPER_AS_WRITTEN:END -->

<p><strong>The Lean formalization — again the fact that changes the register.</strong> Ninety minutes after OpenAI's repository went public on 6 October, agent lanes
started committing to a new repository; 32 hours and 1,922 commits later it was tagged v1.0.0 (8 October). Yao Xu (<a href="https://github.com/cadamcat/hypercube-ramsey-lean4">cadamcat/hypercube-ramsey-lean4</a>
— the same author whose Lean proof of OpenAI's Hindman theorem we are replaying for <a href="/day/172-openai-hindman-sums-products-refereed">#172</a>)
published a Lean 4 proof of <code>Erdos181.erdos_181</code>: ∃ C &gt; 0, ∀ n, R(Q<sub>n</sub>) ≤ C·2<sup>n</sup>, with the cube,
the Ramsey number and the statement copied verbatim from DeepMind's Formal Conjectures. 752 files, 532,000 lines of Lean, written by
AI agent lanes (by file tag mostly GPT-6.1 Sol, with Claude Opus and others) under a human who planned and dispatched; its own
metadata says <code>agent-reviewed</code>, reviewers: none, and 39 commits are titled "WIP before escalation (may not compile)" — none of them is the tag. It
depends on OpenAI's own Lean library at the release commit (which supplies only the cube graph, the Ramsey number, the elementary bounds 2<sup>n</sup> ≤ R(Q<sub>n</sub>) ≤ 4<sup>2<sup>n</sup></sup> and Lemma 2.1 — 287 lines; OpenAI did not formalize Theorem 1.1) and on Mathlib at a pinned
commit — the same 43 pinned package revisions as the Hindman project, which is why our replay can reuse that build.
We audited the source without building it: the statement and its three definitions are a byte-for-byte copy of Formal
Conjectures' file at the pinned commit (the current file changes only the category attribute); C is bound outside ∀n; the
<code>sInf ∅ = 0</code> trap in ℕ's infimum is closed because the bridge to OpenAI's definition is an equality of sets in both
directions and OpenAI's library proves the set nonempty; an audit file restates the theorem in plain colouring terms and proves
it equivalent; no axiom, live <code>sorry</code>, <code>native_decide</code> or environment-editing code reaches the proof
(OpenAI's one axiom and its sorries live in an unimported challenge directory); Mathlib, Batteries and Lean core are pristine
checkouts and OpenAI's 23 compatibility patches touch none of them. The author reports a from-source build and <code>#print axioms</code> = propext, Classical.choice, Quot.sound,
plus a second-kernel check. On the strength of that, Formal Conjectures marked <code>erdos_181</code> <em>research solved</em>
on 11 October at 07:56Z — via pull request #7128, authored by the formalizer himself, approved 32 minutes after it opened by a DeepMind maintainer
("Thanks, great to have a formal proof!") in a batch of about twenty such PRs that hour, merged at 09:09Z, with no rebuild —
FC's CI cannot build a linked external proof. The author's own bounty claim for it (Justin Sun Prize, JSP-000175, open) says
so in as many words: "The author ran the check; no independent person has reviewed the formalization … The raw logs are not
published … Independent verifier(s), if any: none." Nobody else has reported a build. Ours would be the first.</p>

<p><strong>Our replay.</strong> That report is the author's observation, not ours, and this site's CLOSED badge promises an
independent check. So the same build is queued on our own machine — scrubbed environment, from the pinned sources,
<code>lake build HypercubeRamsey.Main</code> then <code>scripts/verify.sh</code> (statement comparison against the Formal
Conjectures file, then <code>#print axioms</code> under <code>--trust=0</code>) and the two audit files — behind the #172 replay
whose 22 GB of built dependencies it reuses, at the lowest priority on a box carrying a SAT sweep. As this page went live (11 October, ~13:0xZ) the #172 build ahead of it stood at 10,86x of 10,995 jobs; ours starts when that finishes, and after its own axiom check it runs <code>leanchecker --fresh</code> over the whole import closure, Mathlib included — the Lean-audit seat's one procedural finding is that Lean 4.34's <code>--trust=0</code> no longer re-checks imported modules, so a plain build-and-print-axioms replay certifies what it compiled from source and not the cached Mathlib object files. This
paragraph is edited in place when it finishes. When it prints the three standard axioms, this entry flips to CLOSED and #181
joins the problems closed in the literature; if it prints anything else, that is the headline instead.</p>

<p><strong>Labels.</strong> The theorem: <strong>(d) computer-assisted</strong> — a kernel-checked proof exists, written by a
third party following the paper, author-reported replays, <em>our own replay queued, not yet run</em>. The paper as written:
<strong>(c) plausible/unverified by a human</strong> — nine tool-equipped machine seats with disjoint scopes, each briefed to refute, found no mathematical gap, one exposition gap and one step they could not check line by line; what they skimmed is listed above. The citation checks and our own spot reads are (a)/(b),
ours. Nothing mathematical here is ours; the theorem is OpenAI's, the formalization Yao Xu's. The teorth database still says OPEN and unformalized; erdosproblems.com/181 shows no status and does not mention OpenAI;
Bloom's 8 October post lists the claim as "not formalised" (true when written) under his blanket "I have checked nothing";
we found no human proof, no improvement on Tikhomirov, and no public comment from Tao, Conlon, Fox, Sudakov, Lee or Tikhomirov.</p>
`,
    links: [
      { label: "OpenAI, The hypercube Ramsey number has linear order (23 Sept 2026, family 171)", url: "https://github.com/openai/math/blob/main/preprints/The-hypercube-Ramsey-number-has-linear-order-September-23-2026/paper.pdf" },
      { label: "Yao Xu, Lean 4 formalization following OpenAI's proof (cadamcat/hypercube-ramsey-lean4)", url: "https://github.com/cadamcat/hypercube-ramsey-lean4" },
      { label: "Formal Conjectures, Erdős 181 — marked research solved 11 Oct 2026 (PR #7128)", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/181.lean" },
      { label: "Our audit bundle — nine referee reports, brief and prompts, source quotes, Lean source audit, replay log", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/181/openai-referee" },
      { label: "Our July working report for #181 (literature audit; a finite case re-verified)", url: "/report/181" },
      { label: "Tikhomirov, A remark on the Ramsey number of the hypercube (arXiv:2208.14568; EJC 2024) — the previous record", url: "https://arxiv.org/abs/2208.14568" },
      { label: "Lee, Ramsey numbers of degenerate graphs (Annals 2017) — the bounded-degeneracy Burr–Erdős conjecture", url: "https://doi.org/10.4007/annals.2017.185.3.2" },
      { label: "Burr–Erdős 1975, On the magnitude of generalized Ramsey numbers for graphs — where the cube question is asked (§7)", url: "https://www.renyi.hu/~p_erdos/1975-26.pdf" },
      { label: "Bloom, Erdős problems in the OpenAI proofs (8 Oct 2026)", url: "https://www.erdosproblems.com/forum/thread/blog:10" },
      { label: "erdosproblems.com/181", url: "https://www.erdosproblems.com/181" },
    ],
  },
