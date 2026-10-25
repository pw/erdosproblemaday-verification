# The seven seat prompts (verbatim scopes), each preceded by "Read /tmp/oaimath/076/REFEREE_BRIEF.md first and follow it exactly. YOURTAG = <tag>."
All seats: Opus, tool-equipped, launched 2026-10-12 ~09:2xZ by the erdos cron seat (09:00Z tick, Fable 5.1); each writes
/tmp/oaimath/076/seats/referee_<tag>.md (copied into the bundle). Page numbers are the paper's printed pages (= PDF pages).

## reduce — sib1 §1–§2 (pp. 1–4), §7 (p. 21), Appendix A (pp. 23–24), and the three contrary preprints
Theorem 1.1 as stated vs the comparator Lean statement (quantifiers, "length N" vs "degree n", √N vs √(N−1), both endpoints);
Prop 2.1's exact constants K_δ and 1−7δ as printed vs as used in the proof of Theorem 1.1 (the step 1−8δ ⇒ µ ≤ 4δN; monotonicity of
u log(80N/u) on 0<u≤N/2; the order "N→∞ with δ fixed, then δ↓0"); Lemma 2.2's statement incl. µ=0; Cor 7.1 and its proof (does
L^p-flatness really follow from a one-sided sup bound + Parseval? for which p?); Appendix A line by line AGAINST THE PREPRINTS
THEMSELVES: refs/2504.21499 (Theorem 1, Equation (27), the concentration constant and Bonami–Révész refs/0707.3023 Definitions 1–2,
Theorem 7, Proposition 9), refs/2509.04212 (Theorem 1 hypothesis (46), Corollary 3's identity), refs/1609.03435v2 (Theorem 3.3,
Equation (2.1) endpoint convention). Is OpenAI's diagnosis of each contrary argument correct, and does it matter for Theorem 1.1
(they say Appendix A is independent of the proof — confirm)? Also §1.1's prior-work sentences (Rudin–Shapiro √(2N), Balister
√(6N−2−1), Erdélyi N+(N−1)^{1/3}/38 — check refs/2608.00744 Theorem 2.1 verbatim) and the live-thread quantifier objection by Bloom.

## construct — sib1 §3 (pp. 5–9) + §4 (pp. 9–14)
Lemma 3.1 (signed interval packing) every inequality: the finite-field hypergraph, degrees/codegrees, the Pippenger–Spencer
hypotheses as quantified in Alon–Yuster Lemma 2.1 (fetch Alon–Yuster, Graphs & Combinatorics 21 (2005) 377–384, or say COULD NOT
FETCH; the paper quotes "(1−β)t < d(v) < (1+β)t" and a codegree bound — check the quoted form matches the source), the passage from a
near-perfect matching/colouring to disjoint intervals of the right widths, "pairwise nonparallel" vs linear relations among ≥3 forms,
the role of H and whether H is fixed before N; §4 Prop 4.1 (auxiliary polynomial with controlled widths), Lemma 4.2 (uniform
quadratic integration — uniform in what, and is the error term's dependence on g, β honest), the spreading of coefficients over extra
torus variables and the bookkeeping of |F| ≤ 1 and mean-square ≥ 1−O(δ) after spreading; constant cycles among δ, m, r, H, the
primes, and the widths.

## sample — sib1 §5 (pp. 14–18)
Lemma 5.1 and §5.1 (uniform estimate for quadratic sums: uniform in the block centre, the angle t, and the compact parameter set
J?), §5.2 (fixed blocks, separated stationary contributions): the claim that at each angle at most one stationary contribution
survives — is it a consequence of the packing in §3 for ALL t including interval endpoints and the ±a pairs of a real F; the Poisson
summation step and the integer-frequency shifts; the non-stationary blocks' contribution (integration by parts — how many
derivatives, is the smooth cutoff's support strictly inside the block, boundary terms); the orthogonality/mean-square recovery giving
(2) with the constant 1−7δ; the delivery of Prop 2.1's (1) with K_δ exactly; every "O(·)" — whose constants, uniform in N?; the
dependence of N₀ on the fixed data only. Also check: does the construction give a vector for EVERY integer N ≥ 1 as Prop 2.1 claims
(block boundaries, rounding of N/H)?

## round — sib1 §6 (pp. 18–21) + §8 (pp. 21–23)
Lemma 6.1 (discrepancy bound for real matrices) against Lovett–Meka refs/1203.5747 — quote their Theorem 4 (the paper says it cites
v2), check hypotheses (row norms, the number of constraints vs dimension, the partial-colouring guarantee that half the coordinates
reach ±1) and that the constant C₀ is absolute; §6.2 dyadic rounding: how the defect mass µ is kept from increasing across rounds,
the Fourier error per round and its sum, the log(80N/µ) form, the case µ = 0 and tiny µ (does the bound degrade gracefully, is the
"≤ N/2" monotonicity actually used), and that Lemma 2.2 as stated (absolute C, every N ≥ 1, every X) is what §6 proves. §8: the
merit-factor normalization F(A) = N²/(2ΣC_u²) vs Downarowicz–Lacroix refs/downarowicz_lacroix (Definition 2, Lemma 0, Theorem 2);
does unbounded max merit factor through all N follow from Theorem 1.1 (L⁴ norm ⇒ merit factor; Parseval for the ‖P‖₄⁴ identity);
Corollary 8.2's spectral statement vs their Theorem 2 (what exactly is "simple spectrum" there, what is asserted about absolute
continuity, and the companion-manuscript remark).

## lean — the formal object
Read /tmp/oaimath/076/lean/AsymptoticallyMinimalLittlewood.lean (+ .json) and the solution tree
/tmp/oaimath/166/lean-build/repo/.lake/packages/OAI/lean/OAI/Analysis/Littlewood/ (Model.lean, Main.lean and the modules in
/tmp/oaimath/076/lean/cone.txt). (1) Is `MainStatement` in Model.lean textually identical to the comparator's, and is `main` in
Main.lean a proof of THAT constant (not a renamed or weakened one)? (2) Does the Lean statement say what erdosproblems.com/1150
negates — write out the correspondence (length N vs degree n; the N₀ ≥ 1 clause; ‖z‖=1 over ℂ; Real.sqrt N; coefficients as reals
equal to ±1)? (3) What route does the Lean proof take — map the 24 modules to the paper's sections (does it follow §3–§6, or a
different/simpler argument; which external Mathlib results carry the discrepancy step, the stationary phase, the hypergraph
colouring — is Pippenger–Spencer in Mathlib? if not, how is Lemma 3.1 done formally? is any heavy analytic input replaced by
something cheaper?). (4) Look for anything that would make the theorem vacuous or mis-stated: a `MainStatement` that is trivially
true, an `IsRealSigning` that admits 0, an `N` cast issue, a `Real.sqrt` of a negative, a theorem proved for a DIFFERENT
`littlewoodValue`. (5) Check Formal Conjectures (github.com/google-deepmind/formal-conjectures) for an `erdos_1150` statement and
compare it to the comparator; check openai/math issues for anything on family 076. Do NOT run lake/lean. Report `grep -c sorry`
etc. only as what you saw in source (our scan: 0 forbidden constructs; the control fired).

## ultra — the two-sided claim: /tmp/oaimath/076/paper/paper.pdf (16 pp) whole, + sib2's Lemmas 3.1 and 6.2 (the inherited inputs)
Theorem 1 (both bounds, both endpoints z=±1); §2 Lemmas 2.1–2.3 (uniform stationary phase: uniformity claims and error terms);
§3 Lemmas 3.1–3.2 (complex rounding with prescribed phases — the defect-sensitive complex version); §4 Prop 4.1 + Lemma 4.2
(two-sided comparison 1 ≤ |c_a|/√w_a ≤ 1+Cδ — the rounding of spreading factors to EQUAL magnitudes); §5 Prop 5.1 (the joined waves:
endpoint curvature increase, phase matching, the summable exterior Fourier tail — this is the new part; is the lower bound (1−ε)√N
really uniform across the gaps between waves?); §6 projection and rounding. Quote sib2's Lemma 3.1 and Lemma 6.2 verbatim and
check they are applied with their hypotheses. This paper is NOT needed for #1150; say so in your report's first line and keep the
verdict about ITS theorem.

## world — citations, numerics, and the world
(1) Every bibliography entry of sib1 (pp. 25–26) exists and the cited locator says what is claimed: Erdős 1957 Problem 22 (vs the
live thread's remark that Problem 22 reads like erdosproblems #230 — settle which problem is which), Hayman–Lingham Problems 4.13
and 4.31 (refs/1809.07200v2 — quote them), Erdélyi refs/2608.00744 Thm 2.1, Balister refs/1909.08777 Thm 1, BBMST refs/1907.09464
Thm 1.1 (and whether the Annals version differs), Jedwab–Katz–Schmidt Thm 1.1/Cor 3.2 (6.342061…), Georgiev et al refs/2511.02864
§6.13 Problem 6.28 (what did AlphaEvolve find at degree ≤ 100 — quote the numbers), Bombieri–Bourgain, Kahane, Littlewood 1966,
Rudin 1959 Thm I, Spencer 1985, Beck 1981, Frankl–Rödl, Alon–Yuster, Pippenger–Spencer, Downarowicz–Lacroix, the OpenAI companion
[20]. (2) Numerics (nice -n 19 python3, seconds): brute-force m_N for N ≤ 20 and compare with any printed table you can find
(Odlyzko / Georgiev et al); check Erdélyi's bound N+(N−1)^{1/3}/38 against them; verify Appendix A's three computations (Dirichlet
kernel concentration B_α(E)=1 for E ⊃ (−d,d); the a_j=2^j example with K=2; the failed identity for P=1+z at z=1, z'=i). (3) The
world: any human expert reaction to OpenAI's Littlewood claims (Tao, Bloom, Erdélyi, Balister, Sahasrabudhe, el Abdalaoui — blogs,
X/Bluesky, MathOverflow, arXiv comments since 23 Sept 2026); whether erdosproblems.com or Formal Conjectures changed #1150's status;
openai/math issues on 076; any independent build of the Lean. Quote, date, link; "no reaction found" must say where you looked.
