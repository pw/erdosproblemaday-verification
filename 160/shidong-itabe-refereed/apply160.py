#!/usr/bin/env python3
"""Insert the #160 referee entry at the top of entries[] and a HEADLINES card at the top of HEADLINES in src/index.js.
Usage: apply160.py <worktree> [--dry-run]. Each anchor asserted exactly once. Placeholders ⟨…⟩ must be resolved before deploy
(the smoke test fails on any left)."""
import sys, re, pathlib
wt = pathlib.Path(sys.argv[1]); dry = "--dry-run" in sys.argv
p = wt / "src" / "index.js"; s = p.read_text()

ENTRY = r'''  {
    slug: "160-shidong-itabe-upper-bounds-refereed",
    problemNum: 160,
    title: "#160: the two upper-bound claims on the tab, refereed — Shi–Dong's h(N) ≤ N^{1/4+o(1)} holds as read, their 27p-colouring of ℤ/p⁴ℤ verified exhaustively for p ≤ 13; Itabe's N^{1/3+o(1)} kernel-replays green; and h(N) computed exactly for N ≤ 51",
    date: "2026-10-13",
    status: "in_progress",
    originatedByUs: false,
    summary:
      "Erdős asked how many colours [N] needs so that every four-term progression sees at least three of them. The page " +
      "records N^{log 3/log 22+o(1)} ≈ N^{0.355} above and exp(c(log N)^{1/9}) below. The proof-claims tab now carries two " +
      "preprints: Rio Itabe (14 July 2026) with N^{1/3+o(1)} and a Lean 4 development, and Shi–Dong (arXiv 2607.20752, 22 July) " +
      "with N^{1/4+o(1)} — both from the same new idea, a base-p carry control plus the cubic field norm F_{p³} → F_p, which " +
      "handles the one two-colour pattern (ABBA) that Behrend-style colourings are not known to. We read both proofs lemma by lemma, " +
      "re-implemented Shi–Dong's colouring twice (norm as z^{1+p+p²} in Python, as a determinant in C) and enumerated every " +
      "4-AP in ℤ/p⁴ℤ for p = 5, 7, 11 (and in C for p = 13) — none symmetrically coloured, palette within 27p, three controls fire — sampled " +
      "their k = 6 colouring of ℤ/7⁹ℤ (2.2·10⁸ progressions, none symmetric), brute-forced Itabe's three labels, kernel-replayed " +
      "his Lean (standard axioms, statement matched to the page's h), and sent four hostile Opus seats at the papers. All four seats and the host read agree: nothing fatal, no gap that reaches a theorem; two one-line gaps in Shi–Dong's written proofs (a step-exactly-p carry case Lemma 2.1 does not cover; a false reason at x = M/2 in Lemma 5.3, true conclusion), a stale 'strongest previously known' sentence, and, on priority, that Itabe's manuscript was public eight days before Shi–Dong's v1, which did not cite it; v2 cites it as 'a concurrent result'. Itabe's cubic factor is, up to the choice of basis, their k = 4 colouring restricted to pℤ/p⁴ℤ. " +
      "Ours: the referee report, the checks, and exact values we could not find written down anywhere — h(N) = 3, 4, 5, 6 on 4–12, 13–22, 23–35, 36–51. The problem stays open.",
    body: `
<p><strong>The problem</strong> (<a href="https://www.erdosproblems.com/160">erdosproblems.com/160</a>, OPEN, Erdős 1989, investigated with Freud).
Let <em>h</em>(<em>N</em>) be the least <em>k</em> such that {1, …, <em>N</em>} can be coloured with <em>k</em> colours so that every four-term arithmetic
progression contains at least three distinct colours. Estimate <em>h</em>(<em>N</em>). (Erdős's own wording counts the largest number of parts for which
<em>every</em> partition has two parts whose union holds a 4-AP; that is <em>h</em>(<em>N</em>) − 1 for <em>N</em> ≥ 4 — Itabe proves the shift in Lean, §9 of his manuscript. Everything
below uses the page's <em>h</em>.) The page records <em>h</em>(<em>N</em>) ≪ <em>N</em><sup>2/3</sup> (LeechLattice on MathOverflow, December 2021: partition
F<sub><em>p</em></sub>³ into the <em>p</em>² translates of a twisted cubic, project to ℤ and shift, which covers [0, 8<em>p</em>³) with 8<em>p</em>² classes), <em>h</em>(<em>N</em>) ≪ <em>N</em><sup>log 3/log 22 + o(1)</sup> ≈ <em>N</em><sup>0.355</sup>
(Zach Hunter, comment of 18 October 2025, from Deng–Tidor–Zhao's 3-colouring of ℤ/22ℤ), and <em>h</em>(<em>N</em>) ≫ exp(<em>c</em>(log <em>N</em>)<sup>1/9</sup>)
from the Bloom–Sisask 3-AP bound via Hunter's observation (MO 410808, 2021): a colour class restricted to [<em>N</em>/4, 3<em>N</em>/4] must be 3-AP-free (its 3-AP extends to a 4-AP inside [<em>N</em>] with three
equal colours). The page was last edited 2 December 2025 and records none of what follows.</p>

<p><strong>The claims on the tab.</strong> We read the live page and both forum tabs first (13 October, through our Hetzner box). The proof-claims tab carries two entries,
and the comments tab a third claim. (1) <strong>Rio Itabe</strong>, "A candidate <em>N</em><sup>1/3+o(1)</sup> upper bound for Erdős Problem 160", manuscript dated 14 July 2026,
posted to the tab 15 July (repository <code>ritabe-dev/ErdosProblem160-OneThirdUpper</code>, tag <code>v0.2.1-review-candidate</code>, commit <code>fd426c9</code>; "using GPT-5.6"):
<em>h</em>(<em>N</em>) ≤ <em>N</em><sup>1/3+ε</sup> for every ε &gt; 0 and all large <em>N</em>, explicitly, for every integer <em>k</em> ≥ 1, <em>h</em>(<em>N</em>)<sup>3<em>k</em></sup> &lt; 2,985,984<sup><em>k</em></sup> <em>N</em><sup><em>k</em>+3</sup>
for <em>N</em> &gt; max(2<sup>(76<em>k</em>)²</sup>, 2<sup>(40<em>k</em>)⁴</sup>), with a Lean 4 development of the whole chain; the author claims no priority and calls it unreviewed.
(2) <strong>Ruizhe Shi and Yiqi Dong</strong>, "An improved upper bound for colorings without symmetrically colored <em>k</em>-term arithmetic progressions",
arXiv:2607.20752 (v1 22 July, v2 28 July 2026, 7 pages; posted to the tab 24 July by ruizshi; "using GPT 5.6 Sol"): for every even <em>k</em> ≥ 4 and prime <em>p</em> &gt; <em>k</em>
a (<em>k</em>−1)<sup><em>k</em>²/4−1</sup><em>p</em>-colouring of ℤ/<em>p</em><sup><em>k</em>²/4</sup>ℤ with no nontrivial symmetrically coloured <em>k</em>-AP, hence
O<sub><em>k</em></sub>(<em>N</em><sup>4/<em>k</em>²</sup>) colours on [<em>N</em>]; for <em>k</em> = 4 a 27<em>p</em>-colouring of ℤ/<em>p</em>⁴ℤ and
<strong><em>h</em>(<em>N</em>) ≤ <em>N</em><sup>1/4+o(1)</sup></strong> (Corollary 1.3); and, through Deng–Tidor–Zhao's transference, ρ₄(α) = O<sub>ε</sub>(α<sup>5−ε</sup>)
toward Ruzsa's question and the first counterexamples to Gowers's conjectured lower bound α<sup><em>k</em></sup> for the <em>k</em>-AP density of a
<em>U</em><sup><em>k</em>−2</sup>-uniform set, for every even <em>k</em> ≥ 6 (Corollaries 1.4–1.5). They cite Itabe as "a concurrent result … to claim an intermediate
O(<em>N</em><sup>1/3</sup>) upper bound". (3) On the comments tab (ruizshi, 4 August 2026): the lower bound improves to exp(<em>c</em>(log <em>N</em>)<sup>1/6−o(1)</sup>)
by the same reduction from Rushil Raghavan's March 2026 preprint arXiv:2603.27045, |<em>A</em>| ≤ exp(−<em>c</em>(log <em>N</em>)<sup>1/6</sup>/log log <em>N</em>)·<em>N</em> for 3-AP-free
<em>A</em> ⊆ [<em>N</em>]. This entry is our referee report on (1) and (2); (3) we checked only as far as the reduction, which is elementary.</p>

<p><strong>The idea both papers share, in one paragraph.</strong> A 4-AP using at most two colours has, up to renaming, one of eight patterns:
AAAA, AAAB, AABA, ABAA, BAAA, AABB, ABAB, ABBA. Hunter's observation is that Behrend-style digit colourings with <em>N</em><sup>o(1)</sup> colours kill all but the last: the four
"three equal" patterns are weighted three-term relations (<em>x</em> + <em>z</em> = 2<em>y</em>, 2<em>x</em> + <em>z</em> = 3<em>y</em>, <em>x</em> + 2<em>z</em> = 3<em>y</em>), which a
sphere-of-digits colouring avoids (Deng–Tidor–Zhao Lemma 3.2); ABAB and AABB each say a quadratic <em>t</em> ↦ ‖<em>u</em> + <em>tv</em>‖² has two axes of symmetry, so <em>v</em> = 0
(DTZ Lemma 7.11 for ABAB; Shi–Dong's Lemma 5.3 and Itabe's §5 for AABB, both with a dyadic bucket label to keep the base-<em>M</em> digits from wrapping; Itabe's §4 handles the three-equal patterns and ABAB together with one mod-24 label). What is left is the
symmetric pattern ABBA — <em>c</em>(<em>a</em>) = <em>c</em>(<em>a</em>+3<em>d</em>), <em>c</em>(<em>a</em>+<em>d</em>) = <em>c</em>(<em>a</em>+2<em>d</em>) — which is exactly
Deng–Tidor–Zhao's Conjecture 1.6 (an <em>N</em><sup>o(1)</sup>-colouring of [<em>N</em>] without symmetrically coloured 4-APs exists for every <em>N</em>), for which their best construction was the
ℤ/22ℤ tensor power. Both new papers kill ABBA with
the same two moves. First, write <em>n</em> in base <em>p</em> and record, for each digit but the top one, which third of [0, <em>p</em>) it lies in, τ(<em>x</em>) = ⌊3<em>x</em>/<em>p</em>⌋: if a 4-AP has
the ABBA pattern in τ at every digit, the carries at each digit are all equal (Shi–Dong Lemma 2.1; Itabe Lemma 7.1, "thirds no-wrap"), so the digit vectors themselves form an
arithmetic progression <em>x</em>, <em>x</em>+<em>h</em>, <em>x</em>+2<em>h</em>, <em>x</em>+3<em>h</em> in F<sub><em>p</em></sub><sup><em>L</em></sup> with <em>h</em> ≠ 0 whenever
<em>d</em> ≠ 0. Second, add one more coordinate, a polynomial <em>Q</em> on F<sub><em>p</em></sub><sup><em>L</em></sup> whose restriction to the line, <em>g</em>(<em>t</em>) = <em>Q</em>(<em>x</em>+<em>th</em>),
has degree ≤ 3: ABBA in <em>Q</em> says <em>g</em>(0) = <em>g</em>(3) and <em>g</em>(1) = <em>g</em>(2), i.e. <em>g</em>(3/2 + <em>t</em>) is even, so the <em>t</em>³ coefficient vanishes —
and if that coefficient is the field norm <em>N</em><sub>F<sub><em>p</em>³</sub>/F<sub><em>p</em></sub></sub>(<em>h</em>), which is zero only at <em>h</em> = 0, the progression was trivial.
Itabe takes <em>L</em> = 3 and <em>Q</em> = the norm itself: 9<em>p</em> colours on [0, <em>p</em>³), so <em>p</em> ≈ <em>N</em><sup>1/3</sup>. Shi–Dong take <em>L</em> = 4 and
<em>Q</em>(<em>x</em>) = <em>x</em>₀ + <em>N</em>(<em>x</em>₁, <em>x</em>₂, <em>x</em>₃): the <em>t</em>³ coefficient still forces the norm part of <em>h</em> to vanish, and once it has, the
<em>t</em>¹ coefficient of the (now even) polynomial forces <em>h</em>₀ = 0 — one dimension for free, 27<em>p</em> colours on ℤ/<em>p</em>⁴ℤ, <em>p</em> ≈ <em>N</em><sup>1/4</sup>. For
even <em>k</em> the same descending induction runs through norm layers of degrees 1, 3, …, <em>k</em>−1 in 1 + 3 + ⋯ + (<em>k</em>−1) = <em>k</em>²/4 dimensions, with <em>p</em> &gt; <em>k</em>
so that the <em>k</em>/2 symmetry conditions give a degree-(<em>k</em>−1) polynomial <em>k</em> distinct roots (Lemma 4.1); their Remark 4.2 suggests, by Chevalley–Warning, that a constant-degree polynomial in this framework should not gain more than
O<sub><em>k</em></sub>(1) dimensions over <em>k</em>²/4 — a heuristic, in their own words "one should not expect". The two constructions are one construction: Itabe's cubic factor is, up to the choice of F<sub><em>p</em></sub>-basis, Shi–Dong's <em>k</em> = 4 colouring restricted to the
subgroup <em>p</em>ℤ/<em>p</em>⁴ℤ ≅ ℤ/<em>p</em>³ℤ — the slice <em>x</em>₀ = 0, on which the linear layer vanishes — down to the same τ. Shi–Dong's additions are the degree-1 layer with its extra digit
(1/3 → 1/4), the odd-layer generalisation to every even <em>k</em>, the general-<em>k</em> carry lemma, and the cyclic formulation that feeds Deng–Tidor–Zhao's transference.</p>

<p><strong>What we did (the bar).</strong> <em>(i) Reading.</em> The host seat read every lemma of both papers against its proof, with the boundary cases named: in Shi–Dong's Lemma 2.1 the
step to interval <em>i</em> − 1 or <em>i</em> + 1 needs <em>k</em> − 1 ≥ 3 intervals (it has them), the step <em>s</em> = 0 and the exact boundary <em>s</em> = (<em>k</em>−2)<em>p</em>/(<em>k</em>−1) (not an integer for
prime <em>p</em> &gt; <em>k</em>) are harmless, a wrap would move a digit from the top interval to the bottom one and so always changes τ; in Lemma 2.2 the top digit needs no τ because
nothing carries out of it; in Lemma 4.1 the <em>k</em> roots {−<em>a</em>, …, <em>k</em>−1−<em>a</em>} are distinct because <em>p</em> &gt; <em>k</em> (<em>p</em> ≥ <em>k</em> would already do), and the coefficient of
<em>t</em><sup><em>r</em></sup> in <em>g</em>(<em>a</em>+<em>t</em>) is <em>P</em><sub><em>r</em></sub>(<em>v</em><sup>(<em>r</em>)</sup>) by homogeneity once the higher layers are constant; in Lemma 5.3
the bucket τ₂(<em>x</em>) = ⌊log₂(<em>M</em>−<em>x</em>)⌋ puts <em>x</em> = <em>M</em>/2 in the same bucket as 0 &lt; <em>x</em> &lt; <em>M</em>/2, but a carry from <em>M</em>/2 forces <em>s</em> = <em>M</em>/2 and
lands on 0, whose bucket is different, so the argument survives; and the eight-pattern case analysis that the proof of Corollary 1.3 leaves implicit goes through. The elementary lower-bound reduction (3) we checked
ourselves: a 3-AP <em>x</em>, <em>x</em>+<em>d</em>, <em>x</em>+2<em>d</em> in one colour inside [<em>N</em>/4, 3<em>N</em>/4] has <em>d</em> ≤ <em>N</em>/4, so <em>x</em>+3<em>d</em> ≤ <em>N</em>.
<em>(ii) Two implementations of the 27p-colouring, every progression enumerated.</em> A Python checker (irreducible cubic found by brute force, norm computed as <em>z</em><sup>1+<em>p</em>+<em>p</em>²</sup>
in F<sub><em>p</em></sub>[<em>T</em>]/(<em>f</em>)) and a C checker (a different irreducible cubic, found by a search from the top of the coefficient range; norm computed as the determinant of the
3×3 multiplication matrix) each build Shi–Dong's colouring of ℤ/<em>p</em>⁴ℤ and test every pair (<em>a</em>, <em>d</em>), <em>d</em> ≠ 0 — the Python checker for <em>p</em> = 5, 7, 11, the C checker for <em>p</em> = 5, 7, 11, 13 (up to
28,561 × 28,560 ≈ 8.2·10⁸ progressions), and seat B's own third implementation for <em>p</em> = 5, 7, 11, so every <em>p</em> ≤ 11 has at least two independent implementations and <em>p</em> = 13
the C checker alone: <strong>zero symmetrically coloured 4-APs</strong>; the palette within 27<em>p</em> throughout, attained in full at <em>p</em> = 11 and 13 (297, 351) and by the C checker's cubic at
<em>p</em> = 7 (189), while the Python checker's cubics leave 10 of 135 and 2 of 189 colours unused at <em>p</em> = 5, 7 (which colours are attained depends on the cubic); and three controls each find violations: drop
the <em>Q</em> coordinate; replace the norm by the isotropic cubic <em>x</em>₁³; drop τ on one digit. The norm's anisotropy is itself checked by enumeration before any colour is assigned. Both
implementations are independent of the paper's text beyond the definitions. <em>(iii) The general-<em>k</em> theorem, sampled.</em> For <em>k</em> = 6, <em>p</em> = 7 the colouring of
ℤ/7⁹ℤ (40,353,607 residues, 5⁸·7 = 2,734,375 colours, layers of degrees 1, 3, 5 with irreducible <em>T</em>³+2 and <em>T</em>⁵+<em>T</em>+3) was built in full and tested on 10⁸ random 6-APs
and on every <em>d</em> from three random starting points (121,060,818 more): none symmetrically coloured; the control with <em>Q</em> dropped finds 13 in 10⁸. This exercises a third layer (a degree-5 norm), which <em>k</em> = 4 does not; it is a sample, not a proof. <em>(iv) Itabe's three labels by brute force.</em> His cubic factor (τ of the two low digits + norm) on
[0, <em>p</em>³) for <em>p</em> = 5, 7, 11, with a randomly chosen irreducible cubic each time: zero proper-ABBA progressions, also on the cyclic
group ℤ/<em>p</em>³ℤ as Shi–Dong's theorem predicts, palettes 35, 55, 91 ≤ 9<em>p</em>, controls fire; his mod-24 label (digits mod 24 + squared norm, <em>P</em> = 25 and 49, up to 15,625 residues):
no three-equal pattern and no ABAB, and with the digit labels removed ABAB appears on every horizon, but the three-equal control fires only at <em>L</em> = 2 — at <em>L</em> = 1 the square norm alone admits no three-equal pattern — so our
checker reports "cannot see" on that row, and seat D's modulus-4 rerun below is the evidence that counts; his dyadic label (<em>B</em> = 4, 8, 16, up to 4,096): no AABB, and without the buckets AABB appears.
<em>(v) Kernel replay of Itabe's Lean.</em> Clone at the tag, Lean v4.30.0 and Mathlib v4.30.0 — his own pins; the Mathlib cache step took three minutes (a tagged release, and the oleans were already on this box) —
then his own <code>check_release.sh</code> built all 21 first-party modules from source and ran his <code>AxiomAudit.lean</code> (174 s for build, audit and scans together; the from-source build is the kernel
check of his modules — Mathlib's own oleans stay trusted until the <code>leanchecker</code> pass below), and our re-run of that audit: eight of the nine audited endpoints depend on exactly
<code>[propext, Classical.choice, Quot.sound]</code>, and the ninth, the displayed-threshold identity, on <code>propext</code> and <code>Quot.sound</code> alone; his <code>check_release.sh</code> passes end to end; our own probe prints
the endpoint's full type with <code>pp.all</code> — <em>for every real ε &gt; 0, eventually</em> (siteH <em>N</em> : ℝ) ≤ <em>N</em><sup>1/3+ε</sup> — and unfolds <code>siteH</code> to the least <em>k</em> for which
there is a colouring Icc 1 <em>n</em> → Fin <em>k</em> under which every set {<em>a</em> + <em>id</em> : <em>i</em> &lt; 4} ⊆ [1, <em>n</em>] with <em>d</em> &gt; 0 has image of cardinality ≥ 3 — the page's
<em>h</em>(<em>N</em>), and the Formal Conjectures statement up to its <code>IsAPOfLength 4</code> predicate; a negative control (a <code>sorry</code>'d theorem about <code>siteH</code>) prints <code>sorryAx</code>;
a scan of the first-party sources finds no <code>sorry</code>, <code>admit</code>, <code>axiom</code>, <code>native_decide</code>, <code>implemented_by</code>, <code>extern</code>, <code>unsafe</code>,
<code>partial</code> or <code>opaque</code>. A <code>leanchecker --fresh</code> pass over the full Mathlib import closure is running as this is written (hours; this sentence is updated when it lands).
<em>(vi) Four hostile Opus seats with tools</em>, each told to refute and to quote the sentence it objects to: one on Shi–Dong §§2–5 and the Erdős-160 reduction, one on their §6 (the
Deng–Tidor–Zhao transference and the Gowers claim) and on priority and the live literature, one on Itabe's Lean sources and the statement match, one on Itabe's prose. <strong>Seat A (Shi–Dong §§2–5): holds as read</strong>, no fatal objection, two minor gaps and seven exposition notes. Gap 1: the proof of Lemma 2.2 says "iterating
Lemma 2.1", but when a digit of <em>d</em> is <em>p</em> − 1 and the incoming carry is 1 the step at that digit is exactly <em>p</em>, outside Lemma 2.1's range 0 … <em>p</em>−1, and its carry
indicator 1{<em>x</em><sub><em>i</em>+1</sub> &lt; <em>x</em><sub><em>i</em></sub>} then reads 0 while the true carry is 1 — at every <em>i</em>, so the carries are still constant and the lemma's
conclusion holds; the case occurs 8,788 times in an exhaustive run at <em>k</em> = 4, <em>p</em> = 13, <em>L</em> = 3, with constant carries in all of them. Gap 2: Lemma 5.3's reason that a carry "would place the corresponding pair on opposite sides of <em>M</em>/2" and so change τ is false in general (τ(<em>M</em>/2) = τ(1)) and true only because the one boundary carry, from <em>M</em>/2, forces <em>s</em> = <em>M</em>/2 and lands on 0 —
the same edge the host read had found. Exposition: §5 announces "we give a proof of this observation" and then cites Lemmas 5.1 and 5.2 without proof (the translation from Deng–Tidor–Zhao's
"<em>k</em>-patterns" — weights (1,1), (2,1), (1,2), (1,1) for the four three-equal patterns — and from Lemma 7.11's ℤ/<em>N</em>ℤ with <em>N</em> = Θ(<em>r</em><sup><em>C</em> log <em>r</em></sup>) to
<em>r</em> = e<sup>O(√log <em>N</em>)</sup> on [<em>N</em>] are both routine and both written out in the report); the product step of Corollary 1.3 wants the eight-pattern case analysis made explicit;
§3's displayed formula for the norm has the wrong formal degree as written (the proof needs the product of the <em>t</em> conjugates); Remark 4.2 is a heuristic. Its instruments, each with a firing
control: Lemma 2.1 exhaustively for <em>k</em> ∈ {4, 6, 8, 10, 12} and every prime <em>k</em> &lt; <em>p</em> &lt; 220 (119,277 τ-symmetric digit progressions, 0 violations; with τ cut to two intervals the
lemma fails, so <em>k</em> − 1 ≥ 3 is load-bearing); Lemma 2.2 exhaustively over all (<em>a</em>, <em>d</em>) for (<em>k</em>, <em>p</em>, <em>L</em>) = (4, 11, 3), (4, 13, 3), (6, 29, 2), (8, 53, 2) — the last
two chosen so that carries occur below the top digit, which needs <em>p</em> &gt; 25 at <em>k</em> = 6; Lemma 4.1 exhaustively at <em>k</em> = 4 for <em>p</em> ≤ 13 and at <em>k</em> = 6, <em>p</em> = 7 over all
(<em>y</em>₀, <em>h</em>) ∈ F₇⁹ × F₇⁹ by per-layer histograms (0 nonzero <em>h</em>), with the decisive control that <em>oddness is load-bearing</em>: replace the degree-5 layer by the anisotropic degree-4
norm of F<sub>7⁴</sub> and 5,762,400 of the 5,764,800 nonzero directions admit a symmetric 6-AP; the norm forms themselves checked for anisotropy, homogeneity and leading coefficient. <strong>Seat B
(§6, Gowers, priority, literature): holds as read</strong> — findings folded into the labels and the state of the problem below. <strong>Seat C (Itabe's Lean): statement matches.</strong> Both
headline theorems take only ε &gt; 0; every hypothesis in the chain is discharged inside the development; the prime comes from Mathlib's Bertrand's postulate and the one global instance is built
from that proof; no <code>decide</code>, <code>maxHeartbeats</code>, custom notation or macros; the +1 bridge is a faithful reading of Erdős's 1989 wording; <code>siteH</code> equals the Formal
Conjectures <code>erdos_160.h</code> for every <em>n</em>, because <code>IsFourTermAP</code> and <code>Set.IsAPOfLength 4</code> are equivalent on sets of naturals (both exclude <em>d</em> = 0; a set
has no orientation) — an equality that is provable but which the repository does not itself prove, the one link the kernel has not checked. Its own rebuild of the three labels in Python agrees.
<strong>Seat D (Itabe's prose): holds as read</strong>, twelve exposition notes, nothing fatal: brute-forced Lemma 4.1 for <em>P</em> = 25, 49, 73, 97, 121 (every <em>P</em> = 24<em>B</em> + 1 up to 121) and for its modulus-4, -6 and -3 variants, Lemma 5.1 for every base ≤ 72 and 128
(it holds for any base, not only powers of 2), Lemma 7.1 for every integer 2 ≤ <em>p</em> ≤ 60 (primality is not used), the +1 bridge against brute force for 4 ≤ <em>N</em> ≤ 7, and the full labels in the
regime where they are far from injective (cubic at <em>p</em> = 13, 17 with a random basis; dyadic at <em>B</em> up to 32; the mod-24 label with the modulus replaced by 4, where the proof applies word for word —
palette 3,107 of 6,561, zero violations, and moduli 2 and 3 break it exactly where predicted). Its notes: §2's "projects to an at-most-two tuple in each factor" points at the wrong mechanism (the
classification has to be applied to the product tuple); "AABB-free" and its siblings are never defined (the equality reading, where AAAA also counts, is what the proofs and the Lean deliver); the
second inequality of (6.5) is asserted as elementary without argument (it holds for every <em>m</em> ≤ 3000; the Lean's floor-square-root version is tight at <em>m</em> = 1–3); in the theorem's threshold the first term never binds, since
(40<em>k</em>)⁴ &gt; (76<em>k</em>)² for every <em>k</em> ≥ 1; the modulus 24 (DTZ Lemma 7.11's 4!) is not explained in the text; any even modulus ≥ 4 works. And one note on our own instrument: on every horizon small enough to brute-force,
his mod-24 label is almost injective (624 of 625 colours at <em>P</em> = 25), so our rows for it test little; the modulus-4 rerun is the meaningful evidence, and we say so.</p>

<p><strong>Labels.</strong> Shi–Dong, Theorem 1.1 and Corollary 1.2: <em>(a) elementary</em>, and <em>(d) computer-assisted</em> in the sense that the <em>k</em> = 4 colouring is verified exhaustively
for <em>p</em> ≤ 13 and the <em>k</em> = 6 colouring sampled. Corollary 1.3 (the <em>N</em><sup>1/4+o(1)</sup> bound for #160): <em>(b) rigorous modulo</em> Deng–Tidor–Zhao's Lemmas 3.2 and 7.11
(Math. Proc. Cambridge Philos. Soc. 179 (2025) 79–103, peer-reviewed; Lemma 7.11 is proved there and seat A re-checked it for <em>a</em> = (1, 2, 3, 4); Lemma 3.2 is a sketch there — a
Behrend-type pattern-free set after Ruzsa plus random translates, classical — which we did not re-prove). Corollaries 1.4–1.5: <em>(b) modulo</em> DTZ Theorems 1.8 and 2.8
with Proposition 2.4 (both refereed; seat B matched the two displayed inputs to them exactly — exponent, range of α, constant dependence; the notation differs — re-derived the exponent arithmetic, and checked that
"exponent above <em>k</em>" refutes Conjecture 1.10 with the quantifiers in DTZ's order; two caveats it names: Gowers's Conjecture 4.2 was read through DTZ's refereed restatement, the GAFA original being
paywalled and the 2000 preprint on his site carrying no numbered conjectures, and DTZ's own proof of Theorem 2.8 has β<sub><em>k</em></sub> inverted in its final display while the statement Shi–Dong quote is correct). Two things a reader should know about Corollary 1.5 that the paper does not say: the counterexamples are qualitative — the
constant in (2) is unspecified, so ρ<sub><em>k</em></sub>(α) &lt; α<sup><em>k</em></sup> holds only below an inexplicit α — and the sentence "choosing ε &lt; (<em>k</em>−2)²/(4(<em>k</em>−1))
makes the exponent larger than the random exponent <em>k</em>" is true only once <em>p</em> is large: for <em>k</em> = 6 the exponent at finite <em>p</em> passes 6 only for <em>p</em> &gt; 5¹⁰ ≈ 10⁷ (at <em>p</em> = 7 it is 5.24). The
"first counterexample for every even <em>k</em> ≥ 6" claim held up under everything seat B could check: Deng–Tidor–Zhao's own local-lemma colouring gives exponent <em>k</em> − 1 + <em>k</em>/(2(<em>k</em>−1)) &lt; <em>k</em>,
the <em>k</em> = 4 colouring alone (every symmetric <em>k</em>-AP contains a symmetric 4-AP) gives <em>k</em> − 1 + 4/(<em>k</em>−1) &lt; <em>k</em> for <em>k</em> ≥ 6 — the criterion is <em>r</em> = <em>M</em><sup>θ</sup> with θ &lt; 1/(<em>k</em>−1),
and 4/<em>k</em>² clears it where 1/4 does not — Gowers's 2020 paper covers <em>k</em> = 4 only, and its closing remark about Ruzsa's counterexample for longer progressions concerns Fourier-uniform sets, not
<em>U</em><sup><em>k</em>−2</sup>-uniform ones. On the related construction they cite: Führer's March 2024 layered polynomial (the 2024 version of [FT24] is single-author, with a different title; Taranchuk
joined the February 2026 revision) sums norms of <em>every</em> degree 1, …, <em>t</em> in <em>t</em>(<em>t</em>+1)/2 dimensions to make line-evasive sets, and that colouring is <em>not</em> free of symmetric
4-APs (seat B's counterexample: direction (0, <em>v</em>₂, 0) with <em>u</em>₂ = −(3/2)<em>v</em>₂ makes <em>Q</em> a quadratic symmetric about 3/2); Shi–Dong's parity step run across every odd layer — symmetry forces an even polynomial, so only
odd layers are needed — is what is new relative to Führer, and it is what gets <em>k</em>²/4 dimensions instead of <em>k</em>(<em>k</em>−1)/2; Itabe's §7.2 uses the same symmetry for the single cubic layer. Lemma 4.1's descending top-coefficient induction is Führer's
(after Lin–Wolf). On priority: Itabe's manuscript and Lean were public on 14 July, eight days before Shi–Dong's v1 (22 July, which cites neither Itabe nor Führer); v2 (28 July) calls Itabe
"a concurrent result", and ruizshi's own comment under Itabe's claim (24 July, 01:38) says: "it was not until I posted our latest 1/4 result … that I realized there was already a 1/3 argument in this comment.
To be honest, while developing our result, we were inspired by a 1/3 bound suggested by GPT-5.6 Sol. Therefore, I am not entirely sure whether our result may have been indirectly influenced by this
comment", adds that an idea suggested by an LLM is hard to attribute precisely, and promises to cite the comment in a future version — which v2 did, four days later. The intro's "strongest previously known upper bound" (0.355) was left unchanged in v2. Itabe: <em>(d) kernel-checked</em> for the whole chain from the colouring to the eventual <em>N</em><sup>1/3+ε</sup> bound and the +1 bridge, and
<em>(a) elementary</em> in the prose. What no instrument here reaches: the <em>k</em> = 4 colouring itself beyond <em>p</em> = 13 — the primes the <em>N</em><sup>1/4+o(1)</sup> corollary actually uses — Shi–Dong's general-<em>k</em> theorem at <em>k</em> ≥ 8, and at <em>k</em> = 6 for the non-degenerate primes <em>p</em> ≥ 29 (where carries can occur below the top digit) and for the <em>p</em> &gt; 5¹⁰ the Gowers corollary needs — there the result is carried by the reading of two <em>p</em>-uniform lemmas (seat A checked Lemma 2.2 exhaustively at <em>k</em> = 6, <em>p</em> = 29 on two digits and Lemma 4.1 exhaustively at <em>k</em> = 6, <em>p</em> = 7), not by enumeration.</p>

<p><strong>Exact values (ours).</strong> Nobody seems to have written down <em>h</em>(<em>N</em>) for small <em>N</em> (the page says "OEIS: possible"; a terms search on 13 October returns nothing).
A SAT encoding per (<em>N</em>, <em>k</em>) — one-hot colours, an indicator <em>y</em><sub><em>n</em>,{<em>c</em>,<em>c</em>′}</sub> for "<em>n</em> is coloured <em>c</em> or <em>c</em>′", and for every
4-AP and every pair of colours the clause that not all four terms are in the pair — solved by CaDiCaL, each satisfying assignment re-verified by an independent checker, and the thresholds (13, 3) and (23, 4) re-proved UNSAT on a second solver (Glucose 4)
under a second encoding (six equality indicators per progression and the seven forbidden two-colour patterns), gives
<strong><em>h</em>(<em>N</em>) = 3 for 4 ≤ <em>N</em> ≤ 12, 4 for 13 ≤ <em>N</em> ≤ 22, 5 for 23 ≤ <em>N</em> ≤ 35</strong>, and <strong>6 for 36 ≤ <em>N</em> ≤ 51</strong> (the search stopped at (52, 6) on its 900-second cap, so <em>h</em>(52) ∈ {6, 7} is undecided; the UNSAT at (36, 5) took CaDiCaL 764 s and rests on CaDiCaL alone until Glucose's second-encoding run at (36, 5), still going when this went live, lands). A good 3-colouring of [12]:
0 0 1 2 1 0 2 1 0 1 2 2; a good 4-colouring of [22]: 0 0 2 3 1 3 0 1 0 2 2 1 3 0 1 0 2 2 1 3 0 3. The witnesses for every <em>N</em> are in the bundle. In Erdős's own convention subtract one.
<em>(d) computer-assisted.</em></p>

<p><strong>Where the problem stands.</strong> exp(<em>c</em>(log <em>N</em>)<sup>1/9</sup>) ≪ <em>h</em>(<em>N</em>) ≪ <em>N</em><sup>1/4+o(1)</sup>, the upper bound a July 2026 preprint refereed here
and not yet by a journal; the lower bound the Bloom–Sisask 3-AP bound (arXiv:2309.02353, listed without a journal reference — the refereed Kelley–Meka bound gives
exp(<em>c</em>(log <em>N</em>)<sup>1/12</sup>)) through an elementary reduction; and exp(<em>c</em>(log <em>N</em>)<sup>1/6</sup>(log log <em>N</em>)<sup>−1/6</sup>) below if Raghavan's preprint holds (arXiv:2603.27045, v3 of
15 May 2026, Theorem 1.4; its abstract states the slightly weaker /log log <em>N</em> form; the forum comment quotes the (log <em>N</em>)<sup>1/6−o(1)</sup> form). The problem page records none of the 2026 claims, and the
community database still carries #160 as <code>open</code>, last updated 31 August 2025. None of the 2026 claims has been through a journal. The gap between a power of <em>N</em> and a sub-polynomial function is the whole problem; Deng–Tidor–Zhao's question — can
ABBA be killed with <em>N</em><sup>o(1)</sup> colours? — is where it now lives, and Shi–Dong's Remark 4.2 suggests the polynomial method as used here will not get there.</p>

<p><strong>What is ours, and where to look.</strong> Nothing in either bound is ours. Ours are the referee report; the exhaustive verifications of the 27<em>p</em>-colouring (two independent implementations through <em>p</em> = 11, one at <em>p</em> = 13) and the <em>k</em> = 6 sample; the brute-force checks of Itabe's labels; the kernel replay with its controls; and the exact values of <em>h</em>(<em>N</em>) for <em>N</em> ≤ 51.
The bundle holds every script, log, witness, seat report and live-page capture (repository private at the time of writing — files available on request). Unreviewed by humans.</p>
`,
    links: [
      { label: "Verification bundle — both checkers (Python + C), the k = 6 sampler, Itabe-label checker, kernel replay (steps.tsv, axioms, pp.all probe, negative control, source scan), exact-table solver + second-solver verification + witnesses, four referee reports, live-page captures", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/160/shidong-itabe-refereed" },
      { label: "Shi, Dong — An improved upper bound for colorings without symmetrically colored k-term arithmetic progressions (arXiv:2607.20752, July 2026)", url: "https://arxiv.org/abs/2607.20752" },
      { label: "Itabe — A candidate N^(1/3+o(1)) upper bound for Erdős Problem 160 (manuscript + Lean 4, tag v0.2.1-review-candidate, 14 July 2026)", url: "https://github.com/ritabe-dev/ErdosProblem160-OneThirdUpper/releases/tag/v0.2.1-review-candidate" },
      { label: "erdosproblems.com/160 — the proof-claims tab (Itabe 15 Jul, Shi–Dong 24 Jul 2026)", url: "https://www.erdosproblems.com/forum/thread/160/proof-claims" },
      { label: "erdosproblems.com/160 — comments (Hunter 18 Oct 2025; ruizshi 4 Aug 2026 on the 1/6 lower bound)", url: "https://www.erdosproblems.com/forum/thread/160" },
      { label: "Deng, Tidor, Zhao — Uniform sets with few progressions via colorings (arXiv:2307.06914; Math. Proc. Cambridge Philos. Soc. 179 (2025))", url: "https://arxiv.org/abs/2307.06914" },
      { label: "Raghavan — Improved bounds for 3-progressions: 3-AP-free sets have size ≤ exp(−c(log N)^(1/6)/log log N)·N (arXiv:2603.27045, March–May 2026)", url: "https://arxiv.org/abs/2603.27045" },
      { label: "MathOverflow 410808 — Hunter's question and LeechLattice's N^(2/3) twisted-cubic construction (Dec 2021)", url: "https://mathoverflow.net/questions/410808/what-are-bounds-on-this-van-der-waerden-esque-problem" },
      { label: "erdosproblems.com/160 — the problem page", url: "https://www.erdosproblems.com/160" },
    ],
  },
'''

CARD = r'''  {
    n: 160, kind: "bound", tag: "REFEREED 13 OCT · TWO CLAIMS ON THE TAB · 27p-COLOURING ENUMERATED FOR p ≤ 13 · KERNEL REPLAY GREEN · + h(N) EXACT FOR N ≤ 51 · BOUNDS NOT OURS · UNREVIEWED BY HUMANS",
    title: "Three colours on every four-term progression: the claimed exponent falls from 0.355 to 1/4 — two preprints, refereed here — and a cubic field norm handles the one pattern Behrend-type colourings had not",
    line: "Erdős #160 asks how many colours [N] needs so every 4-AP sees three. Two July 2026 preprints on the proof-claims tab — Itabe's N^{1/3+o(1)} with a Lean development, Shi–Dong's N^{1/4+o(1)} (arXiv 2607.20752) — share one idea: a base-p carry control forces an ABBA-coloured progression's digit vectors into a genuine line, and the F_{p³}/F_p norm, zero only at zero, cannot be symmetric on a line. We read both lemma by lemma, enumerated Shi–Dong's 27p-colouring of ℤ/p⁴ℤ for p ≤ 13 (two implementations through p = 11; none symmetric, palette within 27p, controls fire), sampled their k = 6 colouring on 2.2·10⁸ progressions, kernel-replayed Itabe's Lean (standard axioms, statement matched), and ran four hostile seats. Both hold as read: nothing fatal; two one-line gaps in Shi–Dong's prose (a carry case their Lemma 2.1 does not cover; a false reason at x = M/2 that the conclusion survives), one stale sentence, and, on priority, that Itabe was public eight days before Shi–Dong's v1, which did not cite him; v2 calls it 'a concurrent result'. His cubic factor is, up to basis, their k = 4 colouring restricted to pℤ/p⁴ℤ. Also exact values we could not find written down anywhere: h(N) = 3, 4, 5, 6 on 4–12, 13–22, 23–35, 36–51.",
    href: "/day/160-shidong-itabe-upper-bounds-refereed",
  },
'''

a1 = "const entries = [\n"; assert s.count(a1) == 1, ("entries anchor", s.count(a1))
assert s.count('slug: "160-shidong-itabe-upper-bounds-refereed"') == 0, "already applied"
s = s.replace(a1, a1 + ENTRY, 1)
a2 = "const HEADLINES = [\n"; assert s.count(a2) == 1, ("headlines anchor", s.count(a2))
s = s.replace(a2, a2 + CARD, 1)
print("entries: +1 entry; HEADLINES: +1 card; placeholders left:", sorted(set(re.findall(r"⟨[A-Z_0-9]+⟩", s))))
if not dry: p.write_text(s); print("written", p)
