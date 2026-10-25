# Seat B: blind consistency read of the #507 page (entry_rendered.txt), 2026-10-22

Seat B, blind. I checked every claim on `/tmp/oaimath/191/entry/entry_rendered.txt` (and the source pieces body.html,
reading.html, world.html, world_replays.html, summary.txt, links.json, headline.js, lean_label.txt) against the paper's
LaTeX and printed numbering, OpenAI's Lean, our replay logs, our bridge Lean and logs, the four seat reports, the live
pages and `compute/sizes.py`. Line numbers `L…` refer to entry_rendered.txt. Scratch: `seats/B_work/`.

**What I re-ran myself:**
- `verbatim_check.py Bridge507.lean` gives 20 chunks, 0 missing, rc 0. `verbatim_check.py Extra507.lean` gives 7 chunks, 0 missing, rc 0.
- The mutant logs fail as claimed: `verbatim_mut.log` and `verbatim_mut2.log` each report 1 missing, and so does `verbatim_extra_mut.log`.
- `sizes.py`: M has 39 digits, T has 116, k has 232. log₁₀η = −235.4982, so η ≈ 3.18·10⁻²³⁶. The Lean exponent is 7.2·10⁻²³⁷.
- n₀ digits (`B_work/n0digits.py`): (400k²)^α has about 2.93·10²³⁸ digits.
- The closure has 195 modules and 24,275 lines, and imports only Mathlib.
- A forbidden-token grep over the 196 files finds exactly the challenge's two `sorry`s and no `set_option`.
- The folder has 242 files. 47 lie outside the closure, `MainDigitBadTripleBound` among them, and none states an every-n theorem.
- The build ran 15:06:01–15:16:43, i.e. 10 min 42 s.
- Toolchain v4.34.1 and Mathlib d13f23b7 match the repo pins at 1581d4c.

**What holds:**
- Every Lean claim on the page except the ones flagged below. `EveryN507.lean` really proves `every_large_n` as described:
  - the statement is the paper's Theorem 1.1 in OpenAI's matched vocabulary;
  - n₀ = (max(r₀, 400k²)+2)^α + 1;
  - the interpolation is exactly as described.
- The axiom logs say what the page says.
- The planted-`sorry` mutants surface `sorryAx`.
- The matcher's eight mutants all return their wanted codes.
- The mathematics descriptions are mostly faithful.
- The page never says that OpenAI's Lean proves the every-n theorem, never says #507 is solved, and never claims an expert endorsement.

---

## MUST-FIX

**1. The digit mechanism is misdescribed (body and teaser).**
- Page, L41: "Lemma 3.3 plants those T determinants at one designated base-B digit position, k−1, of the columns' entries modulo h = B^k, so that carries cannot reach it."
- headline.js `line`: "hide the field norm of the labels' Vandermonde determinant in one base-B digit of the coordinates."

What is wrong: the T pieces are placed at T different designated digit positions in each row. Those positions are i_a = a, j_a = Ta and ℓ_a = T² − (T+1)a, by (3.6). The matching rule (3.7) says only matched triples sum to k−1. So the norm appears (mod r) as the coefficient γ_{k−1} of the *determinant's* base-B expansion. It is not stored in any one digit of the entries or coordinates. Also, Lemma 3.3 does not plant anything: the construction (3.6)–(3.8) does the planting, and Lemma 3.3 proves the obstruction.

Evidence: `03-norm-digits.tex`, the positions/matching paragraph and the proof of Lemma 3.3 ("γ_{k−1} ≡ 𝒩(X(ξ₁),X(ξ₂),X(ξ₃)) (mod r)").

Replacement for L41: "The digit construction (3.6)–(3.8) puts the three factors of each of those T determinants at designated base-B digit positions of the three rows, chosen by (3.7) so that only matched positions add up to k−1. Modulo r, the coefficient of B^{k−1} in the determinant is then the norm. Lemma 3.3 shows that the coefficients are too small for carries to cancel it. So three distinct labels force every integer representative of det mod h = B^k to exceed τ ≈ B^{k−1}/2 in absolute value."

Replacement for the teaser: "…and arrange the coordinates' base-B digits so that one digit of every triangle's determinant carries the field norm of the labels' Vandermonde determinant."

**2. One "false strengthening" is not known to be false.**
Page, L127: "Two false strengthenings fail to compile with the same proofs: α ≫ 1/n (the trivial upper order), and the answer n^{−2+4/α}."

What is wrong:
- α ≫ 1/n is false, since α ≪ n^{−7/6+o(1)}.
- n^{−2+4/α} ≪ FC's α is **not known to be false**. Since 4/α ≈ 6·10⁻²³⁶, it is most likely true. Blinov and Chen, on this same page, claim exponents near 2·10⁻⁸. If either is right, that statement is true.
- In any case, a proof script failing on a changed statement shows the control is sensitive. It does not show the statement is false.

Evidence: `BridgeMutAnswer.lean:83` (answer 4/α), log "unsolved goals"; `BridgeMutExp.lean:313` (α ≫ 1/n); the page's own L219–221.

Replacement: "Two stronger statements fail to compile with the same proofs: α ≫ 1/n, which is false because α ≪ n^{−7/6+o(1)}, and the answer n^{−2+4/α}, which is not proved here. So the proofs are not passing vacuously."

**3. nealmcb did not note the narrower scope.**
Page, L73: "Three third-party replays ran OpenAI's Comparator on this challenge before us, and each also noted that the Lean states less than the paper:"

What is wrong: this holds for mathvet ("weaker-statement") and for cert-machine ("NARROWER — DECLARED"). Nothing in the evidence shows nealmcb noting it:
- W's list of who noticed the sequence-only scope (W §7) omits nealmcb.
- `W_work/gh/nm_REPORT.md` mentions Heilbronn once, line 601, and only about the nanoda failure.

Replacement: "Three third-party replays ran OpenAI's Comparator on this challenge before us. Two of them also noted that the Lean states less than the paper:" Then drop the implication from the nealmcb bullet, or add a receipt if one exists.

**4. A seat's computation is overstated.**
Page, L157: "2,100 random digit matrices on small cases, with the paper's positions and its bound on B, never put a representative of the determinant within 1.9995·τ of zero."

What is wrong: the 1.9995 minimum was taken only over matrices whose planted coefficient was nonzero mod r. One third of the 2,100 trials had a repeated label, which forces target = 0, and random residues also give 0 about 1/r of the time. Those matrices were excluded from the margin. Repeated labels *do* give small determinants, as the page itself says at L189.

Evidence: `R1_work/lem33.py`, lines 64–68 (`if target!=0: … minmargin`) and its print string "min |rep|/tau over nonzero-target cases".

Replacement: "Of 2,100 random digit matrices on small cases (the paper's positions, its bound on B, arbitrary prescribed residues), every one whose planted coefficient was nonzero mod r kept every representative of its determinant at least 1.9995·τ from zero."

**5. "log_r a_r … exactly" is false.**
Page, L183: "Recomputed symbolically: α = log_r a_r = 45435k + 16 exactly".

What is wrong: a_r = r√(N³/τ), and B is a prime in a window, not a power of r. So log_r a_r is not α. The paper's (8.6) says only A_k r^α ≤ n_r ≤ D_k r^α. The phrase is copied from R2's report. C stated it correctly as "the exponent of r in a_r is 45435k + 16".

Replacement: "Recomputed symbolically: the exponent of r in a_r is α = 1 + 30β = 45435k + 16, so A_k r^α ≤ n_r ≤ D_k r^α as in (8.6)".

**6. The engineering note on @[irreducible] is contradicted by our own run.**
Page, L99: "A single push_cast on the concrete cast of 45435k+16 drove one compile past 17 GB, until we killed it. OpenAI's own files avoid the same trap by marking k @[irreducible]."

What is wrong, in two parts:
- (a) No file records 17 GB. The two logged attempts were both killed by our own RSS cap at about 10 GB: `bridge/T1.log` and `bridge/TC.log` both read "RSSCAP KILLED … rss_kb≈10,0xx,xxx after 41–43 s". The only other "17 GB" is a sentence in `entry/mkhandoff.py`.
- (b) In those runs k *was* already `@[irreducible]`. `Definitions.lean:38` has `@[irreducible] def heilbronnK`, imported through Main into EveryN507Core and T1. So the attribute did not avoid the trap. What worked was proving the inequality for a variable K (`exponent_le_alpha`, `cast_eta`).

The page's L63 also says the attribute "keeps tactics away from a 232-digit number", which our own run contradicts.

Replacement: "A single push_cast on the cast of 45435k+16 with the concrete k ran past our 10 GB memory cap within a minute, even though k is @[irreducible] in OpenAI's Definitions.lean. We avoided it by proving the inequality for a variable K and then instantiating." For L63, drop "which keeps tactics away from a 232-digit number", or soften it to "which stops the elaborator from unfolding k".

---

## SHOULD-FIX

**7. The status framing is inconsistent: claim or established?**
- L27: "That stood as the best lower bound until this release". The H1 says "OpenAI's first power improvement over Komlós–Pintz–Szemerédi" with no "claimed".
- The top badge reads CONFIRMED (L13; `status: "posted"` maps to "CONFIRMED" in `index.js.orig` STATUS).
- Elsewhere the page says "The claim." and "No human has refereed the paper or our files", and that #507 stays open.

The closest precedent, #90 (a power saving that leaves the problem open, "OpenAI claims the first power saving…"), uses `in_progress`, i.e. LIVE. #508 and #120 do the same. A CONFIRMED badge directly under "ERDŐS #507" on an open problem reads as "confirmed / solved".

Fixes:
- Use `in_progress` (LIVE) or `partial` (PARTIAL), as the old report did.
- L27: "That was the best proven lower bound before this release. The two earlier claims of a power gain, described below, do not hold up."
- H1: "OpenAI's claimed first power improvement…". Alternatively, state the actual verification status once: sequence form kernel-checked in OpenAI's Lean, every-n form in ours, no human referee.

**8. Our replay is credited with "adding the definition match".**
L81: "Ours is a fourth, independent replay. It adds the definition match, the kernel probe that clears the one attribute difference, and the closure scan."

Comparator's acceptance (mathvet, cert-machine, nealmcb 11 Oct) already includes a check that the solution's theorems and the definitions they use are the challenge's. That is what Comparator is for. Our pp.all match is a second, independent method of the same check, not an addition. The `@[irreducible]` flag is an elaborator attribute that a kernel-level comparison does not see.

Replacement: "Ours is a fourth, independent replay. It repeats the statement and definition match by a second method (pp.all text plus a probe of the kernel's records, which clears the one attribute difference) and adds a scan of the whole closure."

**9. The Big O Speedrun attributions are unsupported by any saved evidence.**
- L225: "On 19 October Joshua Cortez proposed … Its own README notes that OpenAI's comparator theorem is weaker, a sequence of n only. … Their record for the statement says it 'proves no board record'."
- links.json: "(Joshua Cortez, PR #20, opened 19 Oct, on main 21 Oct 2026)".

"Joshua Cortez", "PR #20", the README remark and the quote "proves no board record" appear in **no** evidence file. A grep of the whole `/tmp/oaimath/191` tree finds them only in entry/ files. W's report names no author and quotes the *PR* ("Subsequence instead of every large n…"), not a README. `BOS_SHA.txt` records only commit 0efdd614 (22 Oct 13:17Z).

Fix: save a receipt (PR page or `gh pr view 20` JSON, README text, the board record) into `bridge/` or `seats/W_work/`. Until then:
- drop the name and PR number, or write "a contributor";
- replace "Its own README notes" with "The pull request notes";
- quote only what the saved board HTML shows.

**10. "Neither has a Lean proof."**
L223: "Neither has a Lean proof."

The saved board says Chen supplies "No Lean proof". For Blinov it says "Lean covers the degree-five norm decomposition, interpolation descent, finite packing, tag separation and the finite fresh-digit probability theorem; the interface instantiation … [are] written proofs only". See `W_work/dl/bigo_board.html`, and `W_work/gh/littlebro_review.md` lines 31–32 and 129.

Replacement: "Neither has a complete Lean proof: Chen supplies none, and Blinov's Lean covers some of the finite and algebraic steps."

**11. A search negative is stated as fact.**
L231: "Formal Conjectures still marks erdos_507 open, and no issue or pull request there mentions OpenAI's proof."

W ran seven specific search strings (W §6). That makes this a coverage claim.

Replacement: "Formal Conjectures still marks erdos_507 open, and W's searches of its issues and pull requests found none mentioning OpenAI's proof."

**12. teorth "unchanged since 31 August 2025".**
L233: "The teorth database entry for #507 is 'open', unchanged since 31 August 2025."

Per W §6, `status.last_update` is 2025-08-31 but `formalized.last_update` is 2026-02-10, so the entry itself did change in 2026.

Replacement: "The teorth database still lists #507 as open (status last updated 31 August 2025)."

**13. The Agama sentence contradicts itself.**
L211/L215: "The paper describes two older preprints accurately. … W found the paper's objection right but understated. The centre makes a collinear triple only when the polygon has an even number of vertices."

If the collinear triple occurs only for even polygons, the paper's objection, stated without qualification, is only partly right. W graded it "ACCURATE but incomplete … EXPOSITION / ERROR-NONFATAL".

Replacement: "W found the paper's objection to Agama correct only in part and too weak. The centre gives a collinear triple only when the polygon has an even number of vertices. The real failure is that three consecutive vertices of a regular m-gon span area of order m⁻³, which W checked numerically, so the claimed bound fails for every large s." Also change the lead to "The paper describes Ellmann accurately and Agama in part."

**14. "C suggests the paper say so": the paper already says it.**
L203: "So its hypothesis R ≥ h is necessary, and the affine case meets it because the auxiliary prime excludes every relation with |x| ≤ H = h². C suggests the paper say so."

The paper already says this, three times:
- Lemma 7.3: "In particular, this estimate holds when R > H/2".
- Its proof: "h ≥ 2 implies H/2 = h²/2 ≥ h".
- Case 1: "Hence a contributing shell satisfies R > H/2".

C's actual suggestion (C report, objection 2) is only to say up front that this is *why* the auxiliary prime exists. C itself adds "As written it is correct".

Also, "fails by up to 2,048×" overstates the gap. C's normalised ratio Σg³/(R³I) reaches 2,048.75 for R < h, against about 24–26 for R ≥ h, so it exceeds the observed constant by about 80×.

Replacement: "Lemma 7.3's normalised moment Σg³/(R³I) stays near 24–26 for R ≥ h and reaches 2,048 for R < h, so the hypothesis R ≥ h is needed. The paper meets it in the affine case, as it says, because the restricted shift excludes every relation with |x| ≤ H = h². C's only suggestion is to say up front that this is what the auxiliary prime is for."

**15. "the full construction" (C).**
L187: "C ran the full construction at d = 1 …"

C ran the §3 digit encoding and obstruction only: no SL₃ mixing, auxiliary prime, lifting or deletion (C check 1a).

Replacement: "C ran the full §3 digit construction at d = 1 …".

**16. The §7 counting is misdescribed.**
L45: "Triples whose residues repeat are counted by their primitive null vector, in three cases."

§7 counts *all* determinant-zero triples by their primitive null vector. The three cases are: affinely independent residues, which do not repeat; an equal pair with an extra equation; and an equal pair without one.

Replacement: "Determinant-zero triples are counted by their primitive integer null vector, in three cases: affinely independent residues, and two cases with an equal pair of residues."

**17. The Bertrand step is misdescribed.**
L47: "Bertrand's postulate between consecutive primes r then reaches every large n."

The paper takes m = ⌈(n/A_k)^{1/α}⌉ and a prime r ∈ (m, 2m] (Lemma 3.2). This gives n ≤ n_r ≤ C_k n, and keeping any n points finishes the proof.

Replacement: "For every large n, a prime r ∈ (m, 2m] from Bertrand's postulate gives n ≤ n_r ≤ C_k n. Keeping any n of the points reaches every large n."

**18. Wrong equation number for the exponent.**
L83: "That is the paper's own exponent (8.6)."

In the printed PDF, η = 2/α is display (8.7). (8.6) is A_k r^α ≤ n_r ≤ D_k r^α with α = 45435k+16; see `paper.txt` lines 1202 and 1206. The same slip appears in BRIEF.md and in EveryN507.lean's docstrings, which cite "(8.6)" for η and "(8.5)" for α.

Replacement: "…That is the paper's own exponent η = 2/α (8.7), with α from (8.6)." Fix the two docstrings in the bundle.

**19. The matcher mutant is described in the wrong notation.**
L65: "k + 2 in place of k + 1".

The mutant changes `heilbronnK`'s body from T² + 1 to T² + 2 (`mutate_matcher.sh`, K_body_plus2). Since k = T² + 1, "k + 1" is a different number. A further detail: `area_no_abs` replaces `abs` with `neg`.

Replacement: "k = T² + 2 in place of T² + 1, …, the absolute value in the area replaced by a negation, …".

**20. The engineering note on the timeout has no evidence.**
L97: "With the concrete k in place, Lean's definitional unfolding of R0^{45435k+16} timed out."

No log in `bridge/` or `bridge/bisect/` records a timeout or heartbeat error. TA, TB and B2–B4 are "unsolved goals" or "No goals" errors. R₀ is also undefined on the page.

Fix: attach the log, or soften to "we proved the interpolation for a general k and then instantiated it, so that no tactic meets the concrete k". Define R₀ = max(r₀, 400k²)+2, or drop it.

**21. One symbol, three meanings (readability).**
- α is first Erdős's α(n) (L19 onward), then the exponent α = 45435k+16 (L47, L83 and later), then FC's `α` function.
- The worst instance is L109, where "…minTriangleArea, α and lowerBest. It supplies the answer n ↦ n^{−2+2/α}" uses both meanings in adjacent sentences.
- M is C(163,41) at L35 and hq at L87.
- U is a dyadic scale at L145 and the constant 3·2³⁰·(200k²)^{3029k+1} at L87.

Fix: call the exponent A (or write 45435k+16 out) wherever FC's α or α(n) is nearby, and rename M = hq to Q or "hq".

**22. The seat-note count is wrong.**
L141: "R1 and R2 returned HOLDS AS READ, with three expository notes each."

R1's report labels only two notes, EXPOSITION 2.4-a and 2.5-a, although its verdict line says three. R2 has three.

Replacement: "R1 and R2 returned HOLDS AS READ, with only expository notes."

---

## NIT

**23. Unqualified "verbatim" and "declarations".**
- L109 and L123: "copies FC's definitions verbatim" and "checks all 20 copied declarations".
- The check is whitespace-normalised substring containment with docstrings, attributes and `public` stripped.
- The 20 items are chunks, including `namespace`, `variable`, `open` and `end` lines, not 20 declarations.
- Suggested wording: "copies FC's definitions verbatim (docstrings and attributes stripped)"; "checks all 20 copied blocks".

**24. Area sentence.**
L113: "FC's oriented area of the moved points equals OpenAI's area formula." Suggested: "The absolute value of FC's oriented area of the moved points equals OpenAI's area formula" (`abs_area_φ`).

**25. Lemma 4.3 sentence.**
L163: "…so it is sharp rather than wrong." Equality in one case shows there is no slack. It shows nothing about correctness. Suggested: "…so (4.5) has no slack; no case violated it."

**26. Children of the reading paragraph.**
- L131 "I read all nine sections": the paper prints eight sections and Appendix A.
- "four seats … read the paper": W read the sources, not the mathematics.
- "all Claude Opus 5.5": no seat file records a model.
- L139 "seat W: the sources and the world (above)": the world section is *below* the reading.

**27. "Bloom never listed #507".**
L239. Supported only for his 8 October post. Suggested: "but #507 is not on Bloom's 8 October list."

**28. The matched-to-family phrase.**
Banner: "the match to family 191 is ours". W found a `plasma-ai/erdos` claim card for this family dated 7 Oct. Suggested: "the match to family 191 is our own reading, not Bloom's."

**29. `OAI.Problem355`.**
L49: a combinatorialist will read "Problem355" as Erdős #355. Add "(OpenAI's internal label)".

**30. Undefined jargon for the target reader.**
- "Comparator" is never defined. One clause would do: "a tool that checks a solution proves exactly the challenge's statements".
- D in "h·D", at L47.
- "pp.all" and "regular 7".

**31. "repeated labels … even exactly zero ones".**
L189. What C found is a determinant residue ≡ 0 mod h, not an integer determinant 0. Suggested: "…and even a determinant ≡ 0 mod h (r = 3, labels (0, 2, 0))."

**32. "orbit of known size".**
L43. Lemma 4.2 bounds the orbit size from below. Suggested: "an orbit whose size Lemma 4.2 bounds from below".

**33. "The exponent is explicit and absurd."**
L35. "Absurd" is editorialising; the paper says "extremely small".

**34. `--trust=0` for the bridge axiom probes.**
The command line is not recorded in any log; only the README says so. post.sh does record it for OpenAI's replay. Either log the command or drop the qualifier.

**35. Bundle files that will ship (not the page).**
- C_report.md gives log₁₀η = −249.4982 and −250.1418, which is off by 14. `sizes.py` gives −235.4982 and −236.1418, which the page uses correctly.
- EveryN507.lean's docstrings cite (8.5) and (8.6) wrongly; see item 18.

**Checked and correct:**
- Every other number: 195, 24,275, 11 minutes, 196, 242, 232/116/39 digits, 3.18·10⁻²³⁶, 7.2·10⁻²³⁷, ~3·10²³⁸ digits, 7,630, 179,910 and 241,122, 165³, 180/180, 4⁹, 0.65625, 27³, 2,029, 53 matrices, 24.4, 18/18, 89–394, 453–825, 22 radius triples, 85–275, (B, r, L) = (7, 3, 6), η values for Blinov and Chen, the 25 on Bloom's list, the 24-page PDF, and all dates.
- The live page reading.
- The KPS, Roth, CPZ and Zakharov attributions.
- The teorth "open".
- The four Bloom-list banners: the BLOOM_8OCT set in apply507.py matches Bloom's list, and 142, 505, 507 and 978 are the four OAI_CLAIMS keys not on it.

VERDICT: SHIP AFTER FIXES
