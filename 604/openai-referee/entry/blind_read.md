# Blind consistency read — /day/604-openai-weak-pinned-distances-refereed (14 Oct 2026)

Read: body604.html (paragraphs cited as ¶Problem, ¶Claim, ¶Architecture, ¶Lean, ¶Seats, ¶World, ¶Labels), entry604.js
(title/summary/links), headline_card.js, oai_claim_line.txt, closed_comment.txt, the own604 LEAN_LABEL in apply604.py, and
rendered_604.txt (the page chrome that renders with the entry). Checked against: paper.pdf/paper.txt, all eight seat reports,
lean-build/ (steps.tsv, modules.tsv, statement_match*, logs/, probe/, driver.log, build.sh), the Lean sources, the world
captures, FC 604.lean, Bloom's post, formalization.yaml, docs_167.md, dewar.txt.

Independently re-verified and correct (no finding): 48/48 modules rc=0 errors=0, build 508 s; axioms of main/pins/
pinsStatement/exists_pin_eventually = [propext, Classical.choice, Quot.sound]; **I re-split the pp.all blocks at declaration
heads myself, and main + F/pairFraction/richPairs/k/distanceFiber are raw byte-equal to the comparator's (488/679/830/3985/255/5075
bytes)**, so "byte for byte" holds; comparator main shows sorryAx; wrongshape type mismatch; negcontrol sorryAx; cert-machine
exit 0, 567 s, both kernel strings; plasma-ai's "prose proof (Sections 2 through 7) is unreviewed"; FC erdos_604 is tagged
`research open` and its docstring notes the zero distance; Bloom: 25 problems, "This proof has been formalised. The PDF is 27
pages long."; problem page: last edited 23 March 2026, Comments (1) (Hunter, 12:59 on 08 Feb 2026), Proof claims (0),
c = 0.864137…, Harborth sentence present; teorth 604 open, lu 2025-08-31; Dewar Conj. 4.7 wording and Thm 4.10 (arXiv v1,
10 May 2025); Erdős 1957 Problem 16 quote is in referee_sources.md (row [4]); "unchanged since the first commit", "not among the
three withdrawn / fourteen revised", "no human has publicly reviewed" all in referee_sources.md §5–§6; 200,000 instances;
KS p = 0.40–0.82 and < 1e−93 for the three controls; κ = −1.4572; 21 pairs on 7 points of ℚ(i); 397 instances; 2,478 trees,
288×, δ³/512 vs δ²; 1.32 → 4.5·10⁻⁴ vs 1.48; 2.1359 / 0.1359 / 0.272; 79 s (78,705 ms); paper sha256 6350959d…; 27 pages;
F₃/F₄ and the rhombus; axisLaw.prod axisLaw (RandomGrids.lean:342), signedCell_formula (Variance.lean:304),
arithmetic_sequence_impossible (ArithmeticContradiction.lean), no sorry/admit/axiom/native_decide in the 48 files, Pins imported
by OAI.lean:478, only `import Mathlib` from outside. Dates 23 Sept 2026 (paper), 6 Oct (release), 2 Oct (FC PR opened),
8 Oct (FC merge, Bloom post), 31 Aug 2025 (teorth), 23 Mar 2026 (page), Feb 2026 (Hunter), 14 Oct — all consistent.

---

## Findings

**1. WRONG — the right-shape probe is five tactic lines, not four.**
- Summary: "the page's question, written from scratch, closes from the Lean in four lines"; ¶Lean: "compiles from
  exists_pin_eventually in four tactic lines".
- Evidence: lean-build/probe/RightShape.lean lines 7–11: `intro ε hε` / `filter_upwards [...] with n h P hP` /
  `obtain ⟨x, hx, hle⟩ := h P hP` / `subst hP` / `exact ⟨x, hx, hle⟩` — five.
- Fix: "five tactic lines" / "in five lines" (also in the bundle README §2.5).

**2. UNSUPPORTED — "14,207 lines" is the non-blank count; `wc -l` says 15,879.**
- ¶Lean: "The formalization is 48 files and 14,207 lines under OAI/Geometry/PinnedDistances/".
- Evidence: `cat OAI/Geometry/PinnedDistances/*.lean | wc -l` = 15,879; `grep -vc '^\s*$'` = 14,207. File count 48 is right.
- Fix: "48 files, 15,879 lines (14,207 non-blank)".

**3. WRONG — the headline card says the Lean states Theorem G.**
- headline_card.js: "noticed the argument proves a more general Theorem G (two injective coordinates over a number field) that
  the Lean states at exactly that generality."
- Evidence: what the Lean states at that generality is the core contradiction `arithmetic_sequence_impossible`
  (ArithmeticContradiction.lean ~l.37–45: no sequence of `PreparedGraph`s with injective Z₁, Z₂ into number fields), not
  Theorem G. The Lean's §2 (the extraction that produces a `PreparedGraph`) is proved only for real planar configurations:
  referee_extremal.md:267 "The subset estimates are proved on the ORIGINAL real configuration before specialising". The body
  itself is careful ("the Lean's core contradiction arithmetic_sequence_impossible is stated at exactly that generality").
- Fix: "…a more general Theorem G (two injective coordinates over a number field), whose core contradiction the Lean states at
  that generality."

**4. MISLEADING — "a counterexample to Theorem G would contradict a kernel-checked theorem."**
- ¶Seats (Fourth).
- Evidence: referee_whole.md:175 "A counterexample to Theorem G **of the PreparedGraph form** would therefore contradict a
  kernel-checked theorem." Getting from a Theorem G counterexample (e.g. Minkowski) to a `PreparedGraph` sequence needs §2's
  extraction in that setting — field-agnostic on paper (referee_extremal.md verdict) but not formalised in that generality (#3).
- Fix: "…so a counterexample to Theorem G, once put through §2's extraction (field-agnostic on paper, formalised only for the
  plane), would contradict a kernel-checked theorem."

**5. WRONG — a cosmetic note misreports both the paper and the transport seat.**
- ¶Seats cosmetic list: "Lemma 6.1's hypothesis is met only because w vanishes below δ/2, which is said on p. 19 but not where
  the tree is built."
- Evidence: the paper does say it, at the point of use — paper.txt:1174 (p. 22): "In the tree for Dj, every positive edge has
  both side masses greater than δ/2, by the support condition on w. Apply Lemma 6.1…". The seat's actual objection
  (referee_transport.md:116–121, obj. 2) is different: singleton-leaf edges have finite (zero) length only because
  w(α({x})) = w(1/n) = 0, i.e. n ≥ 2/δ — "stated once, on p.19 … but not where the tree is built".
- Fix: "the singleton-leaf edges have zero length only because w(1/n) = 0 once n ≥ 2/δ, which is said on p. 19 but not where
  the tree is built."

**6. WRONG — "fetched at the cited versions".**
- ¶World: "Twelve of the fourteen references were fetched at the cited versions and say what the paper says they say".
- Evidence: referee_sources.md:59–61 "[6] FRT was checked against the JCSS 2004 journal version …, not the cited STOC 2003
  proceedings. [5] Evans–Matsen was checked in arXiv 1005.1699v3 …; the cited JRSS-B 2012 version could not be fetched"; :334
  "fetched at the cited (or matching) versions". (Guth–Katz, Lund–Petridis, Katz–Tardos, Tardos were also read as arXiv/author
  copies.)
- Fix: "Twelve of the fourteen references were fetched (some as arXiv or author copies; FRT as its journal version, Evans–Matsen
  as its arXiv preprint) and say what the paper says they say".

**7. WRONG — the problem page does not "say open".**
- ¶Labels: "the problem page, the teorth database and Formal Conjectures all still say open".
- Evidence: referee_sources.md:248 "No status label is displayed (statuses hidden site-wide)"; live_604.html text has no status,
  only "The best known bound is … due to Katz and Tardos". The page's own ¶World says exactly that and no more.
- Fix: "the problem page still gives Katz–Tardos as the best known bound, and the teorth database and Formal Conjectures still
  say open".

**8. WRONG (count) + UNSUPPORTED (bundle) — "seven referee reports".**
- Links: "Our audit bundle — paper text, brief, seven referee reports with their check scripts, …".
- Evidence: there are eight reports (referee_{extremal,arithmetic,smallcells,variance,transport,limits,whole,sources}.md); the
  body itself says seven seats "plus a sources-and-world seat". seats/PROMPTS.md:1 says "The seven seat prompts" and lists eight —
  the miscount's origin. And as of this read the bundle (verification/604/openai-referee/) has `seats/` = PROMPTS.md +
  REFEREE_BRIEF.md only, `checks/` empty: no reports, no scripts; README still has the placeholder `LEANCHECKER_SENTENCE` and says
  `SHA256SUMS` exists (it does not).
- Fix: "eight referee reports (seven on the proof, one on sources)"; copy the eight reports and every `*_checks|*_scripts|*_work`
  dir into the bundle before deploy (the link is a claim about it).

**9. MISLEADING — "Three findings" then four; run-on.**
- ¶Seats: "Three findings are worth more than cosmetics. First, … Second, … Third, … So the kernel certifies …, which is more than
  either alone.Fourth, and the whole seat's own finding: …".
- Evidence: four items; rendered text "alone.Fourth" (no space — body604.html has no separator).
- Fix: "Four findings…"; put "So the kernel certifies…" after the Fourth item, or start Fourth as a new sentence with a space.

**10. MISLEADING — "the human-readable proof is certified by the seats' hand reading — two different arguments for one
statement".**
- ¶Seats (end of Third).
- Evidence: (a) the page's own ¶Labels grades the prose (c) "plausible/unverified by a human" — machine seats reading it is not
  certification. (b) The Lean is not a different argument end to end: referee_limits.md:113 "`BoundedContradiction.lean` … follows
  the paper's §7 route"; referee_transport.md:140 steps that "match one-for-one" (`arch_cross_defect`, `arch_fiber_cut`,
  `iid_transfer`); §3–§5 (product formula, nested grids, (3.6), Lemma 5.1 = `signedCell_formula`) are shared. It diverges in §2,
  the tree lemma, the §7 obstruction (and the §6 weight/duality).
- Fix: "So the kernel certifies the theorem; the seats' reading supports the prose, which the Lean follows in architecture but
  replaces in §2, Lemma 6.1 and Lemma 7.1."

**11. MISLEADING — ¶Labels: "found no gap; the cosmetic list above is the whole yield".**
- Contradicts ¶Seats, which lists four findings "worth more than cosmetics" (KT for s > 0.1359, Hunter, Lean route, Theorem G).
- Fix: "found no gap; the yield is the cosmetic list and the four framing findings above".

**12. MISLEADING — the CLOSED badge and the OAI-claims boilerplate.**
- Rendered header: "CLOSED OCT 14, 2026"; status `proof_claimed` (→ badge "CLOSED"), HEADLINES `kind: "solved"`, 604 added to
  CLOSED_BY_LITERATURE. The site legend defines CLOSED as "The problem is closed — a real proof exists".
- Evidence: the body supports exactly "First question answered yes; n/√log n stays open" (summary), "anything about n/√log n (the
  second question …) stay open" (¶World); the problem as posed has two questions ("…? Or even ≫ n/√log n?", live_604.html);
  plasma-ai records `scope: partial`. A reader seeing a bare CLOSED will read "#604 solved". The card tag ("#604'S FIRST QUESTION
  ANSWERED YES") and closed_comment.txt are properly qualified; the badge and the title are not.
- Also: the OAI-claims box rendered on this page ends "anything on this page that says the question is open was written before
  that release and has not re-checked it" — false here: this entry was written after the release and deliberately says the second
  question is open.
- Fix: qualify the badge on /day/604 and /problem/604 ("CLOSED — first question; n/√log n open") or use `partial`; suppress the
  boilerplate's last clause on the entry that referees the claim.

**13. MISLEADING (attribution/overclaim) — summary.**
- "Seven tool-equipped seats … found no gap — only that the s > 0.1359 half was already Katz–Tardos, that the Lean takes a
  different route through §2 and §7, and that the argument proves a more general Theorem G nobody has stated."
- Evidence: the Katz–Tardos reduction (and the Hunter point) is the sources seat's (S2, S3) — the eighth seat, not one of the
  seven. "Nobody has stated": referee_whole.md says "I found no prior statement of either" — a coverage claim. The Lean also
  departs in §6 (tent weight, δ³ tree bound, KR duality; transport obj. 5).
- Fix: "Eight seats (seven on the proof, one on sources) … through §2, §6 and §7 … a more general Theorem G that no source the seats
  searched states."

**14. MISLEADING — "The Euclidean plane enters in exactly three places".**
- ¶Architecture: "— the two coordinate maps are injective on real points, distinct points have nonzero distance, and §7 needs an
  archimedean place".
- Evidence: nonzero distance is a consequence of injectivity (referee_whole.md:123, R2: "injectivity … ⇒ t(x,y) ≠ 0 … In the
  Euclidean case this is the only use of reality"); the archimedean place is a characteristic-zero/number-field input, present for
  Minkowski and ℂ² alike (Theorem G), not a Euclidean one; and the essential Euclidean input — the factorization (3.1) of a rank-2
  form — is missing from the list, though ¶Seats later calls it "load-bearing" (ℓ∞ grid).
- Fix: "The Euclidean structure enters through the factorization (3.1) into two coordinates that are injective on real points (so
  distinct points have nonzero product); the characteristic-zero input is §7's archimedean place."

**15. WORDING — product formula "at every place".**
- ¶Architecture: "applies the product formula of K at every place: on a fiber the two logarithmic depths sum to a constant".
- Evidence: (3.3) i₁ + i₂ = h_e holds place by place from the factorization; the product formula is the sum over places
  (⟨i₁+i₂⟩ = 0, p. 12). A number theorist will stumble on "product formula … at every place".
- Fix: "…factors ‖y−x‖², so at every place the two logarithmic depths on a fiber sum to a constant, and the product formula over
  all places makes their weighted sum vanish on every pair: …".

**16. WORDING — "the complex weight 2/[K:ℚ] is Milne's |σa|²".**
- A weight is not an absolute value. Evidence: referee_arithmetic.md (3.2) normalization: Milne's complex normalized value is
  |σa|², so log‖a‖_v = 2 log|σa|, and dividing by [K:ℚ] gives σ_v = 2/[K:ℚ].
- Fix: "(the factor 2 in the complex weight 2/[K:ℚ] is Milne's squared modulus |σa|², …)".

**17. UNSUPPORTED (count) — "on thousands of random instances".**
- ¶Seats: "the §5 seat verified the signed identity and the exact cell-probability formula (5.4) term for term … on thousands of
  random instances".
- Evidence: referee_variance.md:24 "(5.4) … exact check (400 random instances)"; :115 block A = 400 instances (signed identity,
  zero mass/marginals, (5.4)); block B = 150 hierarchies for the integrated identity. The thousands (5,000 / 3,000) are the min
  inequality and (6.2).
- Fix: "on 400 random instances (and the integrated form on 150 hierarchies)".

**18. WORDING (count) — "121 small configurations".**
- ¶Seats: "checked exactly on 121 small configurations with a failing control".
- Evidence: sources_checks/iso_reduction.py (referee_sources.md:98–108): 11 configurations (4 grids, 6 random, circle+centre) ×
  11 thresholds T = 2..12 = 121 cases ("0/121 cases violate", :121). The seat's own prose has the same slip.
- Fix: "on 121 (configuration, threshold) cases from 11 small configurations".

**19. WORDING — "The driver fetched the Mathlib cache (79 s)".**
- Evidence: logs/cache_get.log:59–61 "No files to download … Decompressed 8907 already-cached file(s) … Completed successfully in
  78705 ms"; it ran as a separate process before the driver (build.sh waits on cache_get.pid; steps.tsv has no cache_get row;
  driver.log: "mathlib oleans present: 8529").
- Fix: "The Mathlib cache was unpacked beforehand (`lake exe cache get`, nothing to download, 79 s); the driver then compiled…".

**20. WORDING — statement-match history.**
- ¶Lean: "Our first statement-match script printed MISMATCH twice — its block splitter cut at blank lines …, then mis-keyed the
  declaration heads; the third version … matches, and all three are in the bundle".
- Evidence: two scripts (v1, v2) each printed MISMATCH once (statement_match.txt, _v2.txt; steps.tsv). Only the three verdict files
  are in the bundle; the v1 code is in build.sh, the v2 and v3 scripts are nowhere in /tmp/oaimath/604 or the bundle.
- Fix: "Our first two statement-match scripts printed MISMATCH — …; the third … matches; all three verdicts are in the bundle" — and
  add the v2/v3 scripts.

**21. WORDING — limits cosmetic note direction.**
- ¶Seats: "'−log|Z − b′| is nonconstant' needs b′ in the support, which the next sentence supplies".
- Evidence: referee_limits.md:42 "b′ ∈ supp β₂, which was fixed in the previous sentence"; paper.txt:1399 "Fix such a target pair
  in the stated supports." precedes it.
- Fix: "…which the previous sentence fixes".

**22. WORDING — Bloom's caveat.**
- ¶World: "with his standing caveat that he has read none of the proofs".
- Evidence: Bloom post: "I have not yet looked at in any serious way any of the proofs in this release".
- Fix: quote it, or "that he has not yet looked seriously at any of the proofs".

**23. WORDING — "Erdős 1957 Problem 16 and a dozen later lists".**
- Evidence: live_604.html cites [Er57] plus eleven later sources ([Er61] … [Er97f]); twelve in all.
- Fix: "and eleven later papers".

**24. WORDING — "that route died in May".**
- ¶Claim, right after "(May 2025, Conjecture 4.7 …)". The refutation is May 2026.
- Fix: "in May 2026".

**25. WORDING — "the small-ball bound fails by three orders of magnitude on explicit sets".**
- Evidence: limits Check 2 control: 0.25 vs 0.00083 (×300) and 0.918 vs 0.00083 (×1,100); the margin is set by the chosen n
  (1/n with n = 1,200), because the signed reading makes C₁ = 0.
- Fix: "fails outright (by factors of 300 and 1,100 at n = 1,200)" or drop the magnitude.

**26. WORDING — "disjoint" scopes.**
- ¶Seats "each assigned a disjoint stretch of the paper (… · the whole paper as a dependency graph …)"; ¶Labels "with disjoint
  scopes". The whole seat's scope overlaps all the others.
- Fix: "six disjoint stretches plus a whole-paper seat".

**27. WORDING — "Lemma 6.1 on 2,478 trees … are (a) elementary, checked here".**
- ¶Labels. Random trees cannot establish a lemma; the (a) grade rests on the transport seat's line-by-line hand check
  (referee_transport.md status table). Same for "the product-formula normalization against Milne" (a citation check).
- Fix: "Lemma 6.1 (re-derived by hand; numerically on 2,478 trees)".

**28. WORDING — "the large-s half of Theorem 1.1 is classical".**
- Evidence: referee_sources.md S2 — a two-line consequence of Katz–Tardos Cor. 8 that the seat derived; nothing says it was
  stated before. "Classical" reads as "in the literature". ("half" of (0,1] is also loose: s > 0.1359 is most of the range.)
- Fix: "the range s > 0.1359 of Theorem 1.1 already follows, in two lines, from Katz–Tardos's Corollary 8, and the paper does not
  say so". Same in the summary ("the s > 0.1359 half was already Katz–Tardos" → "…already followed from Katz–Tardos").

**29. WORDING — "--trust=0 axioms of main, …".**
- `#print axioms` is independent of the trust level, and on an imports-only probe (Axioms604.lean imports Pins) `--trust=0`
  re-checks nothing; the phrase suggests an extra check that did not happen (the re-check is the pending leanchecker run).
- Fix: drop "--trust=0", or "#print axioms (kernel-built modules) of main, …".

**30. WORDING — "the Lean proves (δ/2)³L by a three-line argument".**
- Evidence: the argument is three lines on paper (referee_transport.md obj. 1); TreeTransport.lean `fluctuation_lower`
  (l.283–) is ~40 Lean lines.
- Fix: "by a short minimal-cell argument".

**31. WORDING — "OpenAI's exists_pin_eventually implies it in a few lines".**
- ¶World, of FC's erdos_604. The bridge (FC uses sInf over n-sets of `A.sup distinctDistancesFrom`) was argued by the sources seat,
  not compiled; RightShape.lean proves the from-scratch page statement, not FC's.
- Fix: "implies it directly (argued; not compiled here)" — or compile a three-line bridge as for #341.

**32. WORDING — formalization.yaml lists the .json config.**
- ¶Lean: "against the comparator challenge ComparatorChallenges/PinnedDistances.lean". formalization.yaml:1469
  `comparator_config: ComparatorChallenges/PinnedDistances.json` (which points at the .lean).
- Fix: "against comparator config PinnedDistances.json (challenge PinnedDistances.lean)".

**33. WORDING — own604 LEAN_LABEL: "the problem page's first question itself".**
- Evidence: referee_whole.md §5 "logically equivalent … but not verbatim" (zero distance; ∀ε form). The body handles this
  correctly.
- Fix: "the problem page's first question (counting nonzero distances, in its ∀ε form)".

**34. WORDING — "the end of the Solymosi–Tóth n^{6/7} → Tardos → Katz–Tardos entropy line".**
- Solymosi–Tóth is not an entropy argument (paper p. 3: Tardos "improved this exponent using entropy inequalities").
- Fix: "the Solymosi–Tóth n^{6/7} → Tardos → Katz–Tardos line (the last two by entropy inequalities)".

**35. WORDING (optional) — the averaged form.**
- ¶World "anything about Erdős's averaged form Σd(x) ≫ n²/√log n" is correct as written, but referee_whole.md:289 notes Corollary
  1.2 does give Σ_x d(x) ≥ (1−o(1))n^{2−ε}, the n^{2−o(1)} weakening. The card/closed comment's "the averaged form stay[s] open"
  is fine. Consider adding the half-clause so a reader does not think Cor. 1.2 says nothing on averages.

**36. NOTE — pending sentence.** ¶Lean ships "this sentence is updated when it lands"; logs/leanchecker_fresh.log is empty
  (running since 15:26:38Z). Fine as an anchor, but someone must own the update.

---

## Summary (must-fix before deploy)

The replay facts and most seat numbers check out; I re-verified the 48/48 build, the axioms, and the pp.all match byte for byte
myself. The defects are counts, attributions, and claims one step stronger than the evidence. Must-fix:

1. **#1** "four tactic lines" → five (RightShape.lean has five).
2. **#2** "14,207 lines" is the non-blank count; wc gives 15,879.
3. **#3** Card: the Lean states Theorem G's core contradiction, not Theorem G. **#4** "a counterexample to Theorem G would
   contradict a kernel-checked theorem" needs the seat's own qualifier ("of the PreparedGraph form").
4. **#5** The Lemma 6.1 cosmetic note is wrong: the paper gives the w-support reason on p. 22; the seat's point was singleton-leaf
   edge lengths.
5. **#6** "fetched at the cited versions": FRT and Evans–Matsen were not.
6. **#7** The problem page shows no status; it does not "say open".
7. **#8** Eight reports, not seven; the bundle does not yet contain the reports or scripts the link promises.
8. **#9/#10/#11** "Three findings" lists four; "alone.Fourth" run-on; "certified by the seats' hand reading" contradicts the (c)
   label; "two different arguments" overstates (the Lean shares §3–§5 and the §7 route); "the whole yield" contradicts the four
   findings.
9. **#12** A bare CLOSED badge and "solved" card for a problem whose second question the page calls open; qualify it, and suppress
   the OAI-box clause claiming anything here that says "open" predates the release.
10. **#13/#14** Summary credits the Katz–Tardos point to the seven seats and says "nobody has stated"; "exactly three places" omits
    the factorization the page later calls load-bearing.

Also fix in the same pass: #17 (400, not thousands), #18 (11 configurations × 11 thresholds), #19 (cache unpacked, not fetched by
the driver), #20, #21, #22, #24.
