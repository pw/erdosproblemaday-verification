# Erdős 821 — audit of OpenAI's "Weighted dilation graphs, smooth shifted primes and totient fibers" (24 Sept 2026)

**Claim under audit (theirs, not ours):** Theorem 1.2 — for every fixed 0 < δ < 1/4, #{p prime : 2x < p ≤ 5x, P⁺(p−1) ≤ x^δ} ≥ x^{1−o(1)};
hence Theorem 1.1, Erdős's conjecture that φ(m) = n has more than n^{1−ε} solutions for infinitely many n (erdosproblems.com/821, Formal
Conjectures `erdos_821`). Paper: openai/math, family 011, 68 pages; SHA-256 in `paper.sha256`. **Nothing mathematical in this directory is
ours.** The companion paper of the same family (the Poisson–Dirichlet law for prime predecessors) imports Theorems 3.5/4.1, Corollary 3.11 and
Lemmas 3.4/4.3 from this one and is NOT audited here.

## The chain of evidence, strongest first

1. **No kernel-checked proof exists for the theorem.** The release's `formalization.yaml` has no entry for family 011. OpenAI's library contains
   one sorry-free file, `lean/OAI/NumberTheory/TotientFibers/FiniteFiber.lean` (312 lines, imports only Mathlib), formalizing the CONDITIONAL §8
   step (enough primes with smooth predecessors ⇒ some fiber is large). We compiled it under `--trust=0` against the Mathlib build of our #172
   replay: no errors, `finite_large_fiber_rpow` depends on [propext, Classical.choice, Quot.sound] — `replay/finitefiber/`. No third-party
   formalization of Theorem 1.1/1.2 exists (search log in `world/`).
2. **Hostile machine referee of the paper as written** — ten Opus seats, tool-equipped, briefed to refute (`seats/REFEREE_BRIEF.md`,
   `seats/PROMPTS.md`), reports `seats/referee_<tag>.md`: transference (§3) · ideal (§4) · lift (§5.1–5.3) · energy (§5.4–5.8) · typeII (§6) ·
   sieve (§7–8) · citations (bibliography + world) · whole (counterexample hunt on Theorem 5.1 + global parameter graph) · numerics (exact
   identities by brute force with negative controls) · memory (a DECORRELATED second instrument on Lemma 3.7 and the §3.8 large-rank induction,
   briefed blind to the other reports). Verdict: **HOLDS AS READ in every scope; no FATAL, no mathematical GAP.** Toy computations with mutation
   controls are in `seats/scratch/<tag>/` (the §3 seat's memory-identity check: 13 instances to 1e-15, four mutations fail, two rules vacuous,
   the "group primes exceed |k|" hypothesis load-bearing; the §4 seat's exact cancellation toy; the lift seat's raw-pattern = (5.5) toy to
   1e-18; the sieve seat's Buchstab identity to 1e-16 with perturbed-identity controls; the typeII seat's determinant-bijection enumeration).
   Findings, in order of weight: Lemma 3.7's bijection is a sketch (true; verified by computer); C₄ > max(C, C₇) used but never written;
   Theorem 4.1's first paragraph vacuous without its "More precisely" clause, and "input" means source; Theorem 5.1's uniformity in k and Z used
   in §6 but not listed; the proof uses nothing about the second endpoint beyond invariance + a size bound (so it proves a stronger one-sided
   statement than claimed; no precedent in the cited literature); Pomerance's Theorem B cited for a transfer with a stronger hypothesis than
   Theorem 1.2 delivers (§8 self-contained); ℓ ≥ 1, the free-draw law, "C_bal independent of κ" implicit/misworded; 4δ < ε where 3δ < ε is
   used; dozens of "Theorem" labels on lemmas; overloaded symbols (C₄, C₆, B₀, S, D, h, θ).
3. **Primary-source checks** — `seats/referee_citations.md`: all 23 references exist as cited, every arXiv version and date correct, 21 of 22
   theorem-number locators quoted beside the paper's paraphrase and matching (Montgomery–Vaughan 1974 unfetched; its Lemma 2.6 is proved in the
   paper). Sources downloaded under `/tmp/oaimath/011/refs/` at audit time (not banked; identifiers in the report).
4. **Our own checks** (the cron seat, before the seats reported): the full 68-page read; (7.18), (7.22), the subtraction directions, the unit
   class in Prop 7.2, Corollary 3.11's exponents, (3.37)/(3.47), (4.22)–(4.26), the §5.3 minor-arc arithmetic, (6.16); and that Theorem 6.1 does
   not yield a Chowla-type statement for λ(2u+1) (λ·1_{W-rough} fails (5.4) on the dyad [W, 2W], where the harmonic prime sum is ≈ 1/√log x).
5. **World state** — `world/`: Formal Conjectures `821.lean` at main (11 Oct) + its history; `WORLD_FINDINGS.md` + `agent_world_notes.md`
   (every query tried); OpenAI's `FiniteFiber.lean` snapshot. erdosproblems.com/821: no status shown, last edited 2025-10-01, no mention of OpenAI;
   teorth DB: open; FC: research open (PR #6898 of 11 Oct marked 12 OpenAI claims solved and left 821 out); Bloom 8 Oct: "This proof has not
   been formalised"; no human proof, no improvement on Lichtman's 15/(32√e), no expert comment on the proof found.

## Labels
Theorem: **(c) plausible/unverified by a human** — ten machine seats, each briefed to refute, found no mathematical gap; two rebuilt the
decisive identity as an exact computation and could make it fail. The §8 transfer alone: (d) computer-assisted, kernel-checked here. Citation
checks, the Buchstab and determinant identities, our spot reads: (a)/(b), ours. The /day entry does not change the scoreboard: #821 is not
closed by our standard (no formal proof, no human referee).

## Reproduce
- Seats: the brief + prompts are verbatim; each report lists what it verified line by line vs skimmed. Toy scripts run with
  `nice -n 19 python3 -I <script>`; each report quotes its outputs.
- §8 Lean check: `lake env lean --trust=0 replay/finitefiber/FiniteFiber_with_axiom_audit.lean` inside any project with the pinned Mathlib
  built (we used the #172 replay's); expected: three `#print axioms` lines, each [propext, Classical.choice, Quot.sound].
- Paper: `sha256sum paper.pdf` must match `paper.sha256`.

## World state at audit time (2026-10-11)
teorth DB: 821 OPEN (lu 2025-08-31), fz 1. OpenAI CONTENTS.md: family 011, two PDFs, no Lean link. Formal Conjectures: research open.
Bloom's 8 Oct post: listed, "not formalised". Nobody but OpenAI has built the §8 file; the count has no formal object anywhere.
