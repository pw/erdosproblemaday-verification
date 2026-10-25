# Hostile referee brief — OpenAI preprint "The Euclidean plane is not five-colorable" (23 Sep 2026, 62 pp), family 158, Erdős problem #508

ONE paper, anonymous author ("OpenAI"), github.com/openai/math `preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/paper.pdf`
(sha256 607c2601…; byte-identical at the repo's first commit and at HEAD 1581d4c, 12 Oct). Local copies: /tmp/oaimath/158/paper/paper.pdf
(PDF page number = printed page number), /tmp/oaimath/158/paper/paper.txt (pdftotext -layout) and paper_plain.txt (pdftotext; line numbers
below refer to paper_plain.txt). Displayed math is MANGLED in both text files — absolute-value bars, overlines, subscripts, fraction bars and
set-builder braces are often lost; when a formula matters, Read the .pdf itself with `pages=` (it renders) and quote from the PDF.

A Lean 4 formalization EXISTS and is CATALOGUED (lean/formalization.yaml: declaration `OAI.EuclideanFiveColor.no_proper_five_coloring`,
file `OAI/Geometry/PlaneColoring/Five.lean`, comparator `ComparatorChallenges/EuclideanFiveColor.lean`, permitted axioms
propext/Quot.sound/Classical.choice). Sources, readable as text: /tmp/oai-math/oai-sparse/lean/OAI/Geometry/PlaneColoring/ (46 files; the
proof's import closure from Five.lean is 70 modules / 30,336 lines: 37 PlaneColoring + 19 OAI/Analysis/PlaneSpectrum + 14
OAI/MeasureTheory/CompactFactors; the import-ordered list is /tmp/oaimath/158/lean-build/order.txt). Comparator statement, verbatim:
    def ProperColoring (colorCount : ℕ) (coloring : ℂ → Fin colorCount) : Prop :=
      ∀ point otherPoint : ℂ, ‖point - otherPoint‖ = 1 → coloring point ≠ coloring otherPoint
    theorem no_proper_five_coloring : ¬ ∃ coloring : ℂ → Fin 5, ProperColoring 5 coloring
Five.lean's proof: `proper_to_borel_weak hc` (BorelTransfer.lean l.436: from ANY proper k-colouring, a Measurable d with `WeakColoring k d`)
then `no_measurable_weak_five_coloring`. `WeakColoring k c := AEMeasurable c volume ∧ ∀ᵐ p ∂(volume.prod angularMeasure), c p.1 ≠ c (p.1 + direction p.2)`
(Coloring.lean; angularMeasure = Haar probability on AddCircle (2π), direction = the unit vector e^{it}). Our kernel replay is RUNNING in
/tmp/oaimath/158/lean-build (steps.tsv, driver.log) — do NOT run lean/lake yourselves (memory guard on this box: live solvers); read the
Lean sources as text if your scope needs them. The kernel settles the THEOREM if it goes green with standard axioms; your job is the
human-readable PROOF in the PDF, and the STATEMENT (does the formal statement say what the paper and the problem page say).

THE CLAIM. Theorem 1.1 (p. 2): the Euclidean plane has no proper five-colouring, with arbitrary colour classes; hence 6 ≤ χ(ℝ²) ≤ 7.
Two parts. THEOREM 1.3 (transfer of colorability, for EVERY k, in ZFC): a proper k-colouring of ℝ² exists ⇔ a weak measurable k-colouring
exists, where (Definition 1.2) a weak measurable k-colouring is a Lebesgue-measurable c : ℝ² → {1..k} with
∑_i ∫_{B(0,R)} ∫_{S¹} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0 for every R (σ = normalized arc length) — i.e. monochromatic unit pairs have
product measure zero; EXCEPTIONAL unit pairs are permitted. THEOREM 1.4: no weak measurable FIVE-colouring exists.

WHY THIS MATTERS. erdosproblems.com/508 (saved: /tmp/oaimath/158/live/live_508.txt, live_508_claims.txt, live_508_forum.txt — fetched
14 Oct 2026 via our Hetzner box): the page says 5 ≤ χ ≤ 7 (lower bound de Grey 2018), 0 proof claims, 1 comment (Erdős 1975 quoting
Nelson's conjecture F(2)=4), last edited 22 Jan 2026. Nobody has posted this claim there. Bloom's 8 Oct blog lists #508 among the 25
problems the release touches ("This proof has been formalised. The PDF is 62 pages long.") and marks it "(partial)" on the FrontierMath
Erdős list (the problem asks the exact value; this would leave {6,7}). The FrontierMath/third-party repo github.com/M0-AR/openai-math-verify-2026
labels family 158 "L1 (plane as ℂ; 9-line question)" and states "No Lean rebuild performed here; kernel correctness assumed" — i.e. NOBODY
has publicly rebuilt the Lean or refereed the paper (our search 14 Oct 21:xxZ found no expert discussion at all). If this holds it is the
first improvement on the Hadwiger–Nelson lower bound since de Grey (2018; five), and a far bigger one: it would decide χ ∈ {6,7} AND prove
(Theorem 1.3) that the measurable and unrestricted chromatic numbers of the plane COINCIDE — a question that has been open since
Falconer proved χ_m ≥ 5 in 1981 (37 years before de Grey got χ ≥ 5 without measurability). The paper itself (p. 1) cites Payne: "the graph
on all of ℝ² whose edges have RATIONAL unit displacement vectors is two-colorable, while every measurable coloring requires at least five
colors. Thus measurable and unrestricted colorings cannot be identified merely because their distance constraints look the same." So a
transfer theorem MUST use something the rational-direction graph lacks. That is test (A) below and it is the single most important thing
in this referee round.

ARCHITECTURE (read §1.1 pp. 3–4 first whatever your scope; Figure 1 p. 4 is the dependency diagram).
Transfer (§2–4). F = real algebraic numbers, E = F(i) the countable "algebraic plane", K = {u ∈ E : |u| = 1} the countable group of
algebraic rotations (divisible, dense in the circle). Restrict a proper colouring to E; averaging its translates/rotations (amenable
averaging — an invariant MEAN, i.e. choice) gives a K- and E-invariant probability law on proper labelings of E. D = dual group of
E_discrete (compact, metrizable); C = j(ℝ²) ⊂ D the Borel subgroup of CONTINUOUS characters z ↦ exp(iξ·z); rotations act on D.
Definition 2.2: a K-invariant Borel probability ν on D is WILD if ν(C) = 0. THEOREM 2.3 (RIGIDITY): every wild ν is Haar measure m_D
(so its Fourier coefficients f_ν(z) = ∫ψ_z dν vanish at every nonzero z ∈ E). Proof: Lemma 2.4 (cosets of C are ν-null; the law of a
difference of two independent ν-samples is wild), Lemma 2.5 (vanishing line average), Lemma 2.6, Lemma 2.7 (RELATIVE SINGULARITY along a
Furstenberg–Zimmer compact tower: for an ergodic K-system, the difference of two characters sampled conditionally independently over the
terminal compact factor still gives C measure zero), §3: Lemma 3.1 (compact tower), 3.2 (conditional multiple averages), 3.3 (radial
identities: "two identities between sums of algebraic unit directions give a difference inequality" for the radial nonnegative Fourier
coefficient w(r) = −log m(r)), 3.4 (general position in a number field), 3.5 (addition under a cap) ⇒ a positive value at any nonzero
radius forces a uniform positive lower bound on an interval of algebraic radii, contradicting the vanishing line averages ⇒ ν = m_D.
§4: Lemma 4.1 (continuous vectors and positivity: the subspace of L² vectors on which the E-translation Koopman action is norm-continuous
is the L² of a probability FACTOR, so projection onto it is a conditional expectation — nonnegativity and ∑ label coordinates = 1 are
preserved; translations extend continuously to ℝ²). PROPOSITION 4.2 (proper ⇒ weak measurable): spectral theorem on the label indicators,
split off the part supported on C; the remainder's spectral measure is wild (Theorem 2.3) ⇒ its correlations at every nonzero algebraic
translation vanish ⇒ removing it keeps the zero unit correlations; jointly measurable versions of the translated coordinates; sample ω;
choose the least label with positive coordinate; exceptional null pairs. The converse (weak measurable ⇒ proper): Lemma 4.3 (density
points of a weak colour class contain no unit pair — Falconer/Payne adapted to product-a.e. exclusion), typical points, graph compactness.
Obstruction (§5–8), five labels, weak measurable c. §5: for a fixed centre x, weak-* limits of the typical angular samples e ↦ (1_{A_i}(y+re))_i
as y → x, r → 1 define circle TRACES; the PALETTE at (x,e) = labels with positive weight at e in some limit; Lemma 5.2 (palette transfer by
smooth transport of two unit directions), Cor 5.4 (sixty-degree exclusion), Lemma 5.5 (binary-centre separation, absolute δ* > 0),
PROPOSITION 5.6: at every centre, almost every palette has ≤ 2 labels. §6: transition graph Γ_x on the labels; Lemmas 6.2–6.4;
THEOREM 6.5: the centres where Γ_x contains a cycle form a CLOSED LOCALLY FINITE set; Lemmas 6.6–6.7. (The estimates use the decay of the
Fourier transform of circle measure; no finite perimeter or smoothness of boundaries is assumed.) §7: smooth the indicators by disk averages,
threshold + renormalize ⇒ probability vectors with ≤ 2 positive coordinates outside disks of vanishing total radius ⇒ a continuous map into
the complete graph K₅ (as a 1-complex); the forest structure away from cyclic centres fills the holes continuously (Lemma 7.4); a PLANAR
COVER OBSTRUCTION (Lemma 7.2 / Five.lean `PlanarCover.compact_open_cover_impossible`: a cover of the closed 5-disk by open sets, ≤ 2
overlapping at any point, each of diameter ≤ 2, is impossible) forces a nontrivial loop around a cyclic-centre disk (Lemma 7.6); a simple
cycle in the reduced edge path (Lemma 7.7); for each edge midpoint a connected component of its preimage crosses the annulus (Lemma 7.8);
limits give compact connected sets K_j with a common point x, each assigned its two endpoint labels, both absent a.e. from
Δ(K_j) = {z : min_q |z−q| < 1 < max_q |z−q|} — PROPOSITION 7.1 (a cycle of common exclusion continua; predecessor: Sokolov–Voronov Props 1–2).
§8: the cycle has length 3, 4 or 5 (simple cycle on five labels). Lemma 8.1 (one-sided strip restrictions); Prop 8.2 (length FIVE impossible:
six-position angular words, Lemma 8.3); Prop 8.5 (length FOUR impossible: two antipodal direction pairs + a parity rule, Lemma 8.6);
Prop 8.10 (length THREE impossible: six alternating sectors for the two outside labels ⇒ an open region using only the three cycle labels
a.e. ⇒ Lemma 8.8 polynomial three-label region ⇒ a RATIONAL PLACEMENT CERTIFICATE puts all seven Moser-spindle vertices in that region ⇒
contradiction). That completes Theorem 1.4.

THE TESTS THAT MATTER (every seat reads these; the seat whose scope they fall in must do them):
(A) PAYNE'S RATIONAL GRAPH. Replace E = F(i) by Q(i) and K by the rational unit circle {u ∈ Q(i) : |u| = 1} (countable, dense in S¹,
NOT divisible — (3+4i)/5 has no rational-coordinate square root). Run §2–4 verbatim. If the argument goes through unchanged it "proves"
that a proper 2-colouring of the rational-unit-distance graph yields a weak measurable 2-colouring of that graph — which Payne [22] (and
the paper's own p. 1) says is FALSE (measurable colourings of that graph need ≥ 5 colours). So name the EXACT step (lemma, line, quoted
sentence) that uses a property of F(i)/K the rational graph lacks: divisibility of K? density of algebraic radii (Lemma 3.4/3.5)? the
number-field general-position lemma? the decay of circle measure's Fourier transform? If no seat can name such a step, the transfer is
not proved. Conversely if the step is real, state what the method proves for the rational graph (presumably: nothing).
(B) PROVE-TOO-MUCH ON k. §2–4 never use k = 5; §5–8 do. For §5–8 name every place "five" enters (Prop 5.6's ≤ 2; cycle lengths 3/4/5;
Lemma 8.8; the Moser spindle). Would the same argument with SIX labels (cycle lengths 3–6; palettes ≤ 2?) also "prove" no weak measurable
6-colouring? That is NOT known to be false (6 is open) so it is not a refutation — but say precisely which step breaks at six, because if
nothing breaks the authors have left a bigger theorem on the table or the argument is wrong. With FOUR labels the conclusion is Falconer's.
(C) THE INVARIANT LAW. "Restricting a proper coloring to E and averaging its translates and rotations gives an invariant probability law on
proper labelings of E" — E ⋊ K is a countable amenable group acting on the compact space of proper labelings of E (compact: product of
finite sets, closed condition). Fine. But check the Lean's version: `PlaneFiveColor.LabelModel.Space k` and `measure k ω` in
OAI/Analysis/PlaneSpectrum/*.lean — is it a probability measure on labelings of E, invariant under translations (`trans_preserving`) and
rotations (`rotate_preserving`), with `ω` the actual colouring as a point? Does anything there assume more than ProperColoring?
(D) THE SPECTRAL STEP (Prop 4.2 / BorelTransfer.lean): label indicator → Hilbert vector; projection onto the "continuous vectors" subspace
(`space (representation k ω)` = vectors whose E-orbit map is continuous at 0); `residual_fourier` + `projection_coefficient` ⇒ the
projected vector keeps ⟪v, T_{u} v⟫ = 0 for every algebraic unit u (`projected_unit_correlation`); then by density/continuity for every
unit u on the circle (`circle_closed_induction`, `fieldVector_unit_correlation`); `projection_range` keeps values in [0,1] and
`projected_sum` keeps ∑ = 1 (so the projection is a conditional expectation, Lemma 4.1); `exists_measurable_field` builds a jointly
measurable version from a continuous L² path (approxIndex via a dense sequence; limsup of real/imag parts); `sample_field` (Fubini /
`Measure.ae_ae_comm`) picks ω. The RIGIDITY theorem enters through `residual_fourier` — find it (OAI/Analysis/PlaneSpectrum/Ergodicity.lean
and its imports) and check its hypotheses are exactly what BorelTransfer supplies.
(E) THE DENSITY-POINT CONVERSE is not needed for Theorem 1.1 (only proper ⇒ weak is used) — do not spend time there beyond noting it.
(F) §5–8 are the kind of continuum-geometry argument where "almost every", "limit", "connected component", "closed locally finite" and
"nontrivial loop" hide quantifier errors. For every lemma in your scope: what is the measure-zero exceptional set, is it independent of the
choices made before (centre x, direction e, the sequence y → x, r → 1), is every "limit" along a sequence that was fixed earlier, is
compactness invoked on a space that is actually compact, is "connected" used for sets that are connected (not merely preconnected / path
connected), does Lemma 7.2's planar cover obstruction have the hypotheses the application supplies (≤ 2-fold overlap EVERYWHERE,
diameters ≤ 2 of CONNECTED COMPONENTS of the positive regions, the disk of radius 5).
(G) THE RATIONAL PLACEMENT CERTIFICATE (Prop 8.10 / Lemma 8.8): recompute it exactly (Python fractions): the seven Moser-spindle vertices,
every edge of unit length (‖·‖² = 1 as a rational identity after the placement), every vertex inside the region the lemma gives
(0 < l < 4 and the polynomial inequalities of Lemma 8.8), with a control that FAILS (perturb a vertex, or use a non-unit edge).
(H) Corollary 1.5 and its citations ([12] Gwyn–Stavrianos Lemma 2.10/Thm 2.11; [2] Bourgeat et al. Thms 1–2) — the sources seat.

Classic holes to hunt: quantifier/parameter order; "clearly"/"it follows"/"similarly"/"the same argument"/"standard" at a hard step
(count them in your scope and check each — "This is a standard amenable averaging construction" on p. 3 is one); inequalities used in the
wrong direction; a limit taken before a sup; a "subsequence" that forgets a previously fixed subsequence; a lemma applied outside its
hypotheses (ergodicity assumed where the law is only invariant — ergodic decomposition? Lemma 2.7 and 3.1 say ERGODIC; where is the
general invariant law reduced to ergodic components?); a Borel/measurable claim about a set defined by an uncountable operation; a
"conditional expectation preserves positivity" step used for a projection that is NOT onto an L²(factor); invariant means (choice) used
where a limit is then taken as if along a sequence.

OUTPUT — write /tmp/oaimath/158/seats/referee_<YOURTAG>.md containing:
- Objections, numbered. Each: location (section / lemma / equation / PDF page), the quoted sentence(s) VERBATIM (from the PDF), what is
  wrong or unverifiable, severity FATAL / GAP / UNCLEAR / COSMETIC, what would fix it. For FATAL/GAP say whether it is a gap in the PROOF
  or in the EXPOSITION (the Lean, if it compiles, settles the theorem regardless — your job on the paper is the human-readable proof).
- For each lemma/proposition/equation in your scope: VERIFIED LINE BY LINE / SKIMMED / NOT READ. This distinction is the deliverable.
- Any finite check you ran: the script VERBATIM, its output, and a control that FAILS (a deliberately wrong input the check rejects).
  Python is fine; keep every run under a minute and under 1 GB (the box carries live solvers); never run lean/lake.
- Citation table for your scope (if any): cited result → what the paper claims it says → what the source actually says (quote) →
  MATCH / MISMATCH / COULD NOT FETCH. Fetch primary sources with curl/pdftotext (arXiv current version) or WebFetch.
- Verdict for your scope: HOLDS AS READ / GAP AT <location> / COULD NOT CHECK <what, why>.
Be concrete, quote, no "the authors should clarify". A machine wrote this; it will not be clarifying. Finish with a ≤400-word summary in
your final message (the file is the full report).
