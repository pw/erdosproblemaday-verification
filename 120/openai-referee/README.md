# Erdős #120 — OpenAI's geometric-case claim refereed; the dyadic case kernel-replayed

Audit bundle for `/day/120-openai-geometric-similarity-refereed` (erdos cron, 03:00Z seat, 2026-10-14, Fable 5.1). Nothing here is ours
mathematically: the claim is OpenAI's (github.com/openai/math, release of 6 Oct 2026, family 084), the formal proof is OpenAI's. Ours is the
reading, the replay and the controls.

## Claim
- **Geometric paper** (5 Oct 2026, 13 pp, sha256 `a689fb6b…301e`, `preprints/The-geometric-case-of-the-Erdos-similarity-conjecture-October-5-2026/geometric-erdos-similarity.pdf`):
  Theorem 1.1 — for every q ∈ (0,1) and η ∈ (0,1) there is a compact E ⊆ [0,1], m(E) > 1 − η, such that for every x ∈ ℝ and s ≠ 0 some
  x + s qⁿ (n ≥ 1) lies outside E. Paper only.
- **Dyadic paper** (25 Sep 2026, 16 pp, sha256 `7e7f6e57…9bed`, `preprints/The-dyadic-case-of-the-Erdos-similarity-conjecture-September-25-2026/paper.pdf`):
  the same for q = 1/2 — Green's open problem 94, the special case erdosproblems.com/120 names as open. Formalized:
  `OAI.Problem310.dyadic_affine_avoidance` in `lean/OAI/MeasureTheory/DyadicAvoidance/Main.lean` (comparator `lean/ComparatorChallenges/DyadicAvoidance.lean`).
- The problem itself (every infinite set) stays OPEN.

## Chain
1. Both papers read in full by the seat; every lemma hand-checked (2.3 = 7η/16; Lemma 3.1 recursion; Lemmas 3.2/3.3 inequalities; (4.3); Lemma 4.3's exactness; Lemma 5.1's count; parameter order (5.4)–(5.5); the repair; §2).
2. Four hostile Opus seats, tool-equipped, disjoint scopes, briefed to refute (`seats/REFEREE_BRIEF.md`): `grids` (§3), `routing` (§4), `scales` (§5 + §2), `whole` (whole-paper, both papers). All four: **HOLDS AS READ**, every lemma VERIFIED LINE BY LINE, objections cosmetic only — reports in `seats/`. Three of them ran exact-rational simulations of the paper's own construction with negative controls that fail (scripts + outputs reproduced verbatim inside the reports).
3. `sources` seat: every reference fetched at the cited version; novelty sweep (arXiv 2025–26, Green's list, Formal Conjectures, Bloom's 8 Oct post, third-party Lean) — `seats/referee_sources.md` — **HOLDS AS READ** (15/15 references exist at the cited versions; 22/22 characterisations match; no prior proof of either case before 6 Oct 2026; four cosmetic notes incl. the unverifiable locator "Problem 4.33.7*" and the uncited JLM24 Question 7.2).
4. Our own finite checks, written from the definitions (`checks/checks120.py`, `checks/checks120.log`): (2.3) exact; (3.1)/monotone/separation for q ∈ [0.03, 0.999]; Lemma 3.1 + preorder bookkeeping on 36 trees; (4.3) by Monte Carlo; existence of r_* in (5.5) at five (q,p); exact-rational Monte Carlo of Lemma 4.3 against (1−p/2)^{(M−1)r} with Lemma 4.2 and Lemma 4.1 asserted on every sample; Lemma 5.1's |T| ≤ D on explicit instances. Result: 73 PASS / 0 FAIL (`checks/checks120.log`; the four Monte Carlo cells land within 1σ: 0.328/0.316, 0.420/0.422, 0.518/0.512, 0.323/0.316).
5. **Kernel replay of the dyadic Lean** (`replay/`): lake-free. `fetch_mathlib.sh` fetched Mathlib `d13f23b7` + its cache (8,529 oleans, 78 s); `build.sh` compiled the 75-module import cone (`order.txt`, topological, computed from the files' own imports; only external root = Mathlib) with Lean v4.34.1 at 2 threads, nice 19 — `build 0 818` s, `modules.tsv` 75 × `errors=0`, per-module logs in `module_logs/`. Then, `--trust=0`: `axioms.log` — `dyadic_affine_avoidance` and `periodic_hitting_set` depend on `[propext, Classical.choice, Quot.sound]`; pp.all statement + `dyadicPoint` definition printed from the proof module and from the comparator compiled on its own (`comparator.log`, which carries `sorryAx` as it must) are byte-identical (`statement_match.txt`, row `statement_match_v2 0`); `negcontrol.log` shows `sorryAx` on a sorried `False`; `wrongshape.log` — the statement with 1 − η/2 is REJECTED (`wrongshape 1`); `rightshape.log` — the hand-retyped comparator statement is inhabited (`rightshape 0`). `leanchecker --fresh OAI.MeasureTheory.DyadicAvoidance.Main` over the whole closure: **exited 0 after 3,849 s** (`steps.tsv` row `leanchecker_fresh 0 3849`; `leanchecker_fresh.log` is empty — leanchecker prints nothing on a pass); controls in `leanchecker_controls.log`: missing module → rc 1 `Could not find any oleans`, non-fresh single module → rc 0. Source scan of the cone: no sorry/axiom/native_decide/unsafe/implemented_by. `MODULE_SHA256SUMS.txt` pins the 76 source files; `SOURCE_REVS.txt` the revisions. The module is byte-identical between commit `adc7f12` (the one Formal Conjectures links) and today's main `1581d4c`.
6. Provenance point (all four seats, independently): the Lean formalizes the DYADIC paper's construction, which at q = 1/2 differs from the geometric paper's (grids 2^{b+2} vs 2^{b+3}; branching condition p(M−1)/2 ≥ 10 vs > 2 log 2; final deduction via shrinking dilations + 2^{−m}D ⊆ D vs all k ∈ ℤ). The kernel certifies the dyadic theorem, not a line of the geometric proof.

## Controls (what could have failed, and the one that did)
- Statement match: positive (right-shape compiles) and negative (wrong-shape rejected); sorry visibility (comparator + NegControl show sorryAx).
- Simulations: unstable centres break Lemma 4.2; coarser grids break (4.6); a mutated membership rule breaks the density; k = 5 on an ℓ₆ model (different problem, same seat) fires — each reported in the seat files.
- **Instrument error, disclosed** (`replay/NOTES.md`): the driver's first statement-comparison script wrote MISMATCH / NONSTD_AXIOMS — a parser bug (keyed on a character the output does not print; did not strip `.{u}` universe suffixes). It failed toward ALARM; the kernel logs were right; the corrected comparison is a literal block equality. The wrong row is kept in `steps.tsv`.
- Brief error, disclosed: the brief's toy parameter g = 1 admits no stable centre (the paper's own choice of g excludes it); the seats chose g per the paper.

## Reproduce
`replay/fetch_mathlib.sh` then `replay/build.sh` (edit the three absolute paths at the top; needs ~8 GB disk for Mathlib's cache, one lean process ≤ 8 GB RSS, ~15 min build + ~3 h leanchecker). `checks/checks120.py` runs standalone (`python3 -I`, ~15 min with 8,000 Monte Carlo samples). Seat scripts are reproduced verbatim in their reports.

## World captures (`world/`)
erdosproblems.com/120 + its forum/proof-claims tabs (14 Oct, via our Hetzner box), Green's list (pdftotext of the 30 Jan 2026 PDF).
