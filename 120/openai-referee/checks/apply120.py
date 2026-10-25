#!/usr/bin/env python3
"""Insert the #120 entry + HEADLINES card + OAI_CLAIMS/LEAN_LABEL updates into <worktree>/src/index.js.
Usage: apply120.py <worktree> fills.json [--dry-run]. Every anchor asserted exactly once; refuses if any {PLACEHOLDER} survives."""
import sys, json, re, io
wt=sys.argv[1]; fills=json.load(open(sys.argv[2])); dry='--dry-run' in sys.argv
p=f"{wt}/src/index.js"; s=open(p,encoding='utf-8').read()
assert '120-openai-geometric-similarity-refereed' not in s, "entry already present"

ENTRY = r'''  {
    slug: "120-openai-geometric-similarity-refereed",
    problemNum: 120,
    title: "#120: OpenAI claims the geometric case of the Erdős similarity conjecture — for every ratio q a compact set of measure 1 − η with no affine copy of {qⁿ}; four hostile seats read the 13-page proof and found no gap, and the dyadic case (Green's Problem 94) is a Lean theorem that {LEAN_TITLE}",
    date: "2026-10-14",
    status: "in_progress",
    originatedByUs: false,
    summary:
      "Erdős asked whether every infinite set A ⊂ ℝ is avoided by some set of positive measure — no x + sA inside it, s ≠ 0. Finite sets are never avoided (Steinhaus); slowly decaying sequences are (Falconer, Eigen); the live page says the question is open for A = {1, 1/2, 1/4, …}, Problem 94 on Ben Green's list. OpenAI's 6 October release carries two anonymous preprints: a 16-page proof for the dyadic sequence (25 September, formalized in Lean) and a 13-page proof for every geometric sequence {qⁿ}, 0 < q < 1 (5 October, paper only). We read both. The construction routes every point of the line through a finite tree of random fair-bit tables and spends its measure budget exactly once at the leaf, so the number of independent chances to hit a translated point grows without the density growing; the scale count stays local to one block of the tree. Four tool-equipped seats with disjoint scopes, each briefed to refute, verified every lemma line by line and found only cosmetic items; exact-arithmetic simulations of the paper's own construction match its exact probability formula and the negative controls fail. {LEAN_SUMMARY} The general conjecture — every infinite set — stays open; what is settled, pending human review, is the family of geometric progressions, the special case the problem page names as open.",
    body: `
<p><strong>The problem</strong> (<a href="https://www.erdosproblems.com/120">erdosproblems.com/120</a>; Erdős 1974, <em>Mathematica
Balkanica</em> 4, Problem 4.33.7*; $100). Let <em>A</em> ⊆ ℝ be infinite. Must there be a set <em>E</em> ⊂ ℝ of positive measure containing
no set of the shape <em>aA</em> + <em>b</em>, <em>a</em> ≠ 0? Call <em>A</em> <em>measure universal</em> if the answer is no — if every
measurable set of positive measure contains an affine copy of <em>A</em>. Steinhaus's theorem makes every finite set universal (translate the
set by <em>s</em>·<em>a</em> for each of the finitely many <em>a</em>; for small <em>s</em> the intersection still has positive measure), so the
conjecture says exactly that no infinite set is. It is true when <em>A</em> is unbounded or dense in an interval, so the content is a sequence
<em>a</em>₁ &gt; <em>a</em>₂ &gt; … → 0. Falconer (1984) and Eigen (1985) settled every sequence with <em>a</em><sub><em>n</em>+1</sub>/<em>a</em><sub><em>n</em></sub>
→ 1; Kolountzakis (1997), Humke–Laczkovich (1998) and Chlebík (2015) gave finite-gap criteria that need the normalized minimum gap of large finite subsets to
decay subexponentially in their size; Bourgain (1987) handled sums of three infinite sets. Geometric sequences fail every one of those criteria
(the gap is at most <em>q</em><sup><em>m</em>−2</sup>/(1 − <em>q</em>) for <em>m</em> points), which is why the page can say the problem "is open when
<em>A</em> = {1, 1/2, 1/4, …}, which is Problem 94 on Green's open problems list" and Chlebík could write in 2015 that the status of every geometric or
faster sequence was unknown.</p>

<p><strong>The claim.</strong> OpenAI's 6 October 2026 release (github.com/openai/math, 372 claims) carries two unsigned preprints on this problem, both in
Bloom's 8 October list of 23 Erdős problems the release touches ("a special case of the Erdős similarity problem"). <em>The dyadic case of the Erdős
similarity conjecture</em> (25 September, 16 pp): for every η ∈ (0,1) there is a compact <em>E</em><sub>η</sub> ⊆ [0,1] with <em>m</em>(<em>E</em><sub>η</sub>)
&gt; 1 − η such that for every <em>x</em> ∈ ℝ and <em>s</em> ≠ 0 some <em>x</em> + <em>s</em>2<sup>−<em>n</em></sup>, <em>n</em> ≥ 1, lies outside <em>E</em><sub>η</sub>.
<em>The geometric case of the Erdős similarity conjecture</em> (5 October, 13 pp): the same for {<em>q</em><sup><em>n</em></sup> : <em>n</em> ≥ 1} and
every fixed <em>q</em> ∈ (0,1), the set depending on <em>q</em>. Both signs of the dilation are included; the paper is explicit that it says nothing
about arbitrary infinite sets. The release's Lean formalizes the dyadic statement only (<code>OAI.Problem310.dyadic_affine_avoidance</code>,
75 modules, 8,455 lines, Mathlib-only imports); the general-ratio theorem is paper only.</p>

<p><strong>Why it stayed open, and what gets past it.</strong> The natural attack is Kolountzakis's: a random union of grid cells at resolution
≈ <em>q</em><sup>−<em>n</em></sup> for each index <em>n</em>, so that for a fixed centre <em>x</em> and scale <em>t</em> the points <em>x</em> + <em>tq</em><sup><em>n</em></sup>
are tested independently. The obstruction is that the densities <em>p</em><sub><em>n</em></sub> must be summable — the open set has to be small — and then
∏(1 − <em>p</em><sub><em>n</em></sub>) is bounded below, so each (<em>x</em>, <em>t</em>) is missed with a fixed probability while there are uncountably
many of them; splitting a single budget <em>p</em> across <em>r</em> indices gives a miss probability like <em>e</em><sup>−<em>pr</em></sup> against
about <em>q</em><sup>−2<em>r</em></sup> distinct configurations as <em>t</em> sweeps [1,2], which loses. The two incomplete UBC summer reports the paper cites
(Solymosi 2011, Tom 2015) stopped there. The new idea is to spend the measure budget <em>once</em> and the resolution <em>freely</em>: every point of the line
is routed down a complete <em>M</em>-ary tree of height <em>d</em> by independent fair-bit tables indexed by nested dyadic grids (first child whose bit is 1,
else the default last child), and only the leaf carries a Bernoulli-<em>p</em> table deciding membership — so the random set <em>B</em> has density exactly
<em>p</em> however deep the tree (Lemma 4.1). Each edge owns a window of consecutive indices <em>n</em>, laid out in preorder with gaps; a centre is
<em>stable</em> if translations from a window never move it across a boundary of any earlier grid (Lemma 3.2: all but density 4<em>Kcq</em><sup><em>g</em>+1</sup>
of centres), while at the window's own resolution the centre and its <em>r</em> translated points have distinct keys (Lemma 3.3, because the cell width is
below (1 − <em>q</em>)<em>q</em><sup><em>b</em></sup>). At a stable centre whose route first takes a default at vertex <em>U</em> — which happens unless an
event of probability (1 − 2<sup>1−<em>M</em></sup>)<sup><em>d</em></sup> — the translated points of the windows on <em>U</em>'s non-default edges inherit the centre's
earlier decisions, reach <em>U</em>, and read fresh bits (Lemma 4.2); conditional on the centre's exposed entries, the (<em>M</em> − 1)<em>r</em> local tests fail
together with probability exactly (1 − <em>p</em>/2)<sup>(<em>M</em>−1)<em>r</em></sup> at any fixed scale (Lemma 4.3). The step that makes the scale count
affordable is the window-length rule <em>r</em><sub><em>h</em></sub> ≥ <em>g</em> + σ<sub><em>h</em>−1</sub> (Lemma 3.1): a test at the first default consults no
grid finer than 2<em>r</em> indices past its window's start, so as <em>t</em> sweeps [1,2] the vector of local tests changes at most
<em>D</em><sub><em>M</em>,<em>q</em></sub>(<em>r</em>) = 4 + 2(<em>M</em> − 1)<em>r</em>(1 + 2<em>cq</em><sup>−2<em>r</em></sup>) times (Lemma 5.1), a count that does
not depend on <em>M</em> — and choosing <em>M</em> with <em>p</em>(<em>M</em> − 1)/2 &gt; 2 log(1/<em>q</em>) makes the exponential win. Missed centres form a closed
periodic set of density ≤ 3<em>p</em>, covered by an open set that repairs them because <em>tq</em><sup><em>n</em></sup> → 0; the resulting open periodic
<em>H</em> of density ≤ 6<em>p</em> hits <em>x</em> + <em>tG</em><sub><em>q</em></sub> for every centre and every <em>t</em> ∈ [1,2] (Proposition 2.1), and a summable union of
dyadic dilations and reflections of such sets, <em>p</em><sub><em>k</em></sub> = η4<sup>−|<em>k</em>|</sup>/64, removes measure exactly 7η/16 from [0,1] while meeting
every nontrivial affine copy (§2).</p>

<p><strong>What we did.</strong> Four hostile seats (Opus, tool-equipped, disjoint scopes, each briefed with the paper's architecture and told to quote the sentence
it objects to): <em>grids</em> (§3), <em>routing</em> (§4), <em>scales</em> (§5 and §2), and a <em>whole</em>-paper seat aimed at the question above — why fifty years,
and where would it break. All four: <strong>HOLDS AS READ</strong>, every lemma in both papers verified line by line, no FATAL, no GAP. The objections are cosmetic
and listed in the reports: the nesting identity and the monotonicity of window endpoints are asserted rather than proved (the dyadic paper writes them out);
Lemma 4.3 carries a "stable centre" hypothesis it never uses; the step 1 − <em>u</em> ≤ <em>e</em><sup>−<em>u</em></sup> in Lemma 5.1 is implicit; the
measurability of <em>x</em> ↦ ℙ(<em>x</em> ∈ <em>R</em>) is unstated (trivial on a finite probability space); the Chlebík repair citation is looser than in the
dyadic version; the notation 𝒜 clashes with <em>A</em><sub><em>i</em>,<em>n</em></sub>. The "prove too much" tests all came back the right way: the argument uses
the infinitude of the pattern in exactly two places — the index sets must grow as <em>p</em> → 0 (from (5.5), (<em>M</em> − 1)<em>r</em><sub>*</sub> &gt;
2 log(4/<em>p</em>)/<em>p</em>) and the repair step needs <em>tq</em><sup><em>n</em></sup> → 0 — so for a finite pattern it proves only the true "most centres"
statement, consistent with Steinhaus; the geometric ratio enters at Lemmas 3.2 and 3.3 and in the count (5.3), which depends only on the index difference, so a
super-geometric sequence breaks (5.3) and the method does not reach the full conjecture; for <em>q</em> → 1 every constant stays finite for each fixed <em>q</em>
(the paper never claims uniformity). Three seats ran the paper's own construction in exact rational arithmetic as an instrument that can fail: the routing seat
measured the conditional failure probability in 48 cells (two centres including a grid-boundary point, <em>U</em> at heights 1 and 2, generic and boundary
scales, <em>p</em> ∈ {0.3, 0.5}) against (1 − <em>p</em>/2)<sup>(<em>M</em>−1)<em>r</em></sup> — max |<em>z</em>| 2.14 over 98 <em>z</em>-scores, success counts binomial —
with 0 violations of Lemma 4.2 in 26.9 million translated-point routings, while an unstable centre broke Lemma 4.2, a 64× coarser grid broke the formula (<em>z</em>
= +135) and a mutated membership rule broke the density (<em>z</em> = +362); the whole seat repeated it on six configurations at <em>q</em> ∈ {1/2, 3/5, 1/3} to depth
3 with the same pattern; the grids seat laid out the windows of 36 trees and found Lemma 3.1 sharp (equality at every height ≥ 2), 0 key collisions in Lemma 3.3,
0 violations of (3.3) in 250,000 comparisons at stable centres. Our own script (<code>checks/checks120.py</code>, written from the definitions): the measure sum
(2.3) is 7/16 exactly in rationals; (3.1), monotonicity and the separation inequality hold for <em>q</em> from 0.03 to 0.999 with margin ≥ 4; Lemma 3.1 on the
36 trees; (4.3) by Monte Carlo; the finite <em>r</em><sub>*</sub> of (5.5) exists at five (<em>q</em>, <em>p</em>) pairs (<em>r</em><sub>*</sub> = 93 at
<em>q</em> = 1/2, <em>p</em> = 1/2; 7,030 at <em>q</em> = 1/3, <em>p</em> = 0.05, where the slack over 2 log(1/<em>q</em>) is 0.003){MC_SENTENCE} One thing the brief
got wrong and the seats caught: a toy with gap <em>g</em> = 1 admits <em>no</em> stable centre at all — the paper's choice of <em>g</em> rules exactly that out, and
the simulations used the paper's <em>g</em>.</p>

<p><strong>The Lean, and what it certifies.</strong> The comparator (<code>ComparatorChallenges/DyadicAvoidance.lean</code>) states, with a <code>sorry</code>:
for every η ∈ (0,1) there is <em>E</em> ⊆ [0,1], compact, of volume &gt; 1 − η, such that for all <em>x</em>, <em>s</em> with <em>s</em> ≠ 0 some
<em>x</em> + <em>s</em>·(1/2)<sup><em>n</em></sup>, <em>n</em> ≥ 1, is outside <em>E</em>. That is the page's special case verbatim up to one line: a compact set is
measurable, and an affine copy of {1, 1/2, 1/4, …} contains an affine copy of {1/2, 1/4, …}, so avoiding the latter avoids the former (Formal Conjectures'
<code>green_94</code> quantifies <em>n</em> from 0; same remark). {LEAN_PARA} <strong>A provenance point all four seats raised independently:</strong> the Lean
proves the <em>dyadic paper's</em> construction, which at <em>q</em> = 1/2 is not the geometric paper's specialization — its grids are
2<sup><em>b</em>+2</sup> against the geometric <em>N</em><sub><em>b</em></sub> = 2<sup><em>b</em>+3</sup>, its branching condition is <em>p</em>(<em>M</em> − 1)/2 ≥ 10
against &gt; 2 log 2, and its final deduction uses only shrinking dilations together with 2<sup>−<em>m</em></sup><em>D</em> ⊆ <em>D</em>, which is special to
<em>q</em> = 1/2, where the geometric §2 uses every <em>k</em> ∈ ℤ. Each version is internally correct and their scale-count constants agree where they overlap;
but the kernel certifies the dyadic <em>theorem</em>, not a line of the geometric <em>proof</em>. The general-ratio bookkeeping rests on the seats' hand
checks above. Independently of us, Harald Schilly's <em>math-distance-set-similarity</em> (Zenodo, October 2026) reports rebuilding OpenAI's whole 2,459-file
Lean tree at commit adc7f12 under <code>leanchecker --fresh</code> and uses the dyadic theorem as an explicit hypothesis; the module is byte-identical between that
commit and today's main.</p>

<p><strong>The world, 14 October.</strong> The problem page (last edited 23 January 2026) still says the dyadic case is open; the proof-claims tab is empty; of the
three comments, two (14 March 2026) concern a <em>different</em> statement — Formal Conjectures had once omitted measurability, a DeepMind prover found that the
ℤ-span of a Hamel basis has positive <em>outer</em> measure and avoids every affine copy of {1, 1/2, 1/4, …}, and a reader notes de Reyna (1983) proved that
outer-measure variant for every |<em>A</em>| ≥ 3 — and one (November 2025) points to Gao–Mooroogen–Yip on a Kolountzakis–Papageorgiou analogue. Green's list
(30 January 2026 version) still asks Problem 94 ("Let <em>A</em> ⊂ ℝ be a set of positive measure. Does <em>A</em> contain an affine copy of {1, 1/2, 1/4, …}?")
with no update. The teorth database says open (statement formalized, last updated 31 August 2025 — refreshed today). <strong>Formal Conjectures has moved:</strong> PR
#6898, merged 11 October, marks <code>green_94</code> research solved, <code>answer(False)</code>, citing OpenAI's <code>Main.lean#L103</code>; <code>erdos_120</code>
— the general conjecture — stays open, which is the right pair. Bloom's 8 October post lists #120 among the 23 with his standing caveat that he has not read the
proofs or checked that the Lean compiles. {SOURCES_PARA}</p>

<p><strong>Labels.</strong> The dyadic case, Green's Problem 94, answered NO: {LEAN_LABEL_SENTENCE} The geometric case for every ratio (Theorem 1.1 of the 5
October paper): <strong>(c) plausible/unverified by a human</strong> — four tool-equipped machine seats with disjoint scopes read it line by line, each briefed
to refute, and found no gap; the probabilistic core was reproduced by simulation with controls that fail. The §2 reduction from the periodic hitting set to the
theorem, the 7η/16 budget, and the one-line bridge to the problem page's statement: <strong>(a) elementary</strong>, checked here. Scoreboard: #120 stays
<strong>OPEN</strong> — the conjecture is about every infinite set, and nothing here touches that; the family {<em>q</em><sup><em>n</em></sup>}, which the page names as the
open special case, is now claimed for every <em>q</em> and formally proved for <em>q</em> = 1/2. Not ours.</p>

`,
    links: [
      { label: "OpenAI, \"The geometric case of the Erdős similarity conjecture\" (5 Oct 2026, 13 pp — the claim for every ratio, paper only)", url: "https://github.com/openai/math/blob/main/preprints/The-geometric-case-of-the-Erdos-similarity-conjecture-October-5-2026/geometric-erdos-similarity.pdf" },
      { label: "OpenAI, \"The dyadic case of the Erdős similarity conjecture\" (25 Sept 2026, 16 pp — the formalized theorem)", url: "https://github.com/openai/math/blob/main/preprints/The-dyadic-case-of-the-Erdos-similarity-conjecture-September-25-2026/paper.pdf" },
      { label: "The Comparator challenge statement — ComparatorChallenges/DyadicAvoidance.lean", url: "https://github.com/openai/math/blob/main/lean/ComparatorChallenges/DyadicAvoidance.lean" },
      { label: "The Lean proof — OAI/MeasureTheory/DyadicAvoidance/Main.lean (theorem dyadic_affine_avoidance at line 103)", url: "https://github.com/openai/math/blob/main/lean/OAI/MeasureTheory/DyadicAvoidance/Main.lean" },
      { label: "OpenAI's scope note for the formalization — lean/docs/084.md", url: "https://github.com/openai/math/blob/main/lean/docs/084.md" },
      { label: "Formal Conjectures, Green's Problem 94 — research solved, answer(False), citing the Lean proof (PR #6898, 11 Oct)", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/GreensOpenProblems/94.lean" },
      { label: "Ben Green, 100 open problems — Problem 94 (version of 30 Jan 2026)", url: "https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf" },
      { label: "Chlebík, On the Erdős similarity problem (arXiv:1512.05607) — Theorem 15 and the remark on geometric sequences", url: "https://arxiv.org/abs/1512.05607" },
      { label: "Kolountzakis–Papageorgiou, Large sets containing no copies of a given infinite sequence (Analysis & PDE 18, 2025; arXiv:2208.02637)", url: "https://arxiv.org/abs/2208.02637" },
      { label: "Jung, Lai, Mooroogen — the 2024 survey the problem page recommends (arXiv:2406.17213)", url: "https://arxiv.org/abs/2406.17213" },
      { label: "Schilly, Erdős similarity for distance sets — the independent leanchecker --fresh replay of OpenAI's tree (Zenodo)", url: "https://github.com/haraldschilly/math-distance-set-similarity" },
      { label: "Our audit bundle — brief, four referee reports, the replay (driver, module logs, axioms, statement match, controls), our checks, world captures", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/120/openai-referee" },
      { label: "erdosproblems.com/120", url: "https://www.erdosproblems.com/120" },
    ],
  },
'''
CARD = r'''  {
    n: 120, kind: "bound", tag: "REFEREED 14 OCT · OPENAI'S CLAIM · EVERY GEOMETRIC RATIO · FOUR SEATS, NO GAP · DYADIC CASE {CARD_LEAN} · NOT OURS · PROBLEM STAYS OPEN · UNREVIEWED BY HUMANS",
    title: "The Erdős similarity conjecture for geometric sequences: OpenAI's 13-page proof holds as read, and the dyadic case — Green's Problem 94 — is a Lean theorem {CARD_LEAN_TITLE}",
    line: "Is every infinite set avoided by some set of positive measure? Open for {qⁿ} since 1974; the page lists {1, 1/2, 1/4, …} as the open case. " +
      "OpenAI's 5 October paper constructs, for every ratio, a compact subset of [0,1] of measure 1 − η that meets every nontrivial affine copy of the sequence, by routing the line through a finite tree of random tables that spends its measure budget once while the number of independent tests grows. " +
      "Four hostile seats verified every lemma; exact-arithmetic simulations of the construction match its exact probability formula with controls that fail. {CARD_LINE_LEAN} The general conjecture stays open.",
    href: "/day/120-openai-geometric-similarity-refereed",
  },
'''
# fills
for k,v in fills.items():
    ENTRY=ENTRY.replace('{'+k+'}',v); CARD=CARD.replace('{'+k+'}',v)
left=re.findall(r"\{[A-Z_]{4,}\}", ENTRY+CARD)
assert not left, f"unfilled placeholders: {left}"
# 1) entry at top of entries
a="const entries = [\n"; assert s.count(a)==1; s=s.replace(a,a+ENTRY)
# 2) headline card at top
a="const HEADLINES = [\n"; assert s.count(a)==1; s=s.replace(a,a+CARD)
# 3) OAI_CLAIMS[120]
old='  120:  { fam: 84,  claim: "the similarity conjecture for the sequences {qⁿ} (Lean only for q = ½)", lean: "partial" },'
assert s.count(old)==1
s=s.replace(old,'  120:  { fam: 84,  claim: "the similarity conjecture for every geometric sequence {qⁿ}, 0 < q < 1 (5 Oct paper, paper only); the dyadic case q = ½ = Green\'s Problem 94 (25 Sept paper, formalized)", lean: "own120" },')
# 4) LEAN_LABEL own120
a='own1150: "'; assert s.count(a)==1
s=s.replace(a,'own120: "'+fills['LEAN_LABEL_OWN120'].replace('"','\\"')+'", own1150: "')
if dry: print("DRY RUN OK — all anchors matched; entry", len(ENTRY), "chars"); sys.exit(0)
open(p,'w',encoding='utf-8').write(s); print("applied")
