# #138 — OpenAI's "Quantitative Superexponential Bounds for van der Waerden Numbers" (23 Sep 2026, 25 pp, family 160), refereed and kernel-replayed

Entry: `/day/138-openai-superexponential-van-der-waerden-refereed` (15 Oct 2026, 06:00Z erdos cron seat, Fable 5.1, max2/yolo2 Max sub — not a Team seat).
Verdict: **HOLDS AS READ** by seven hostile seats; **kernel replay GREEN** (statement and its four definitions matched to the comparator byte for byte; the page's
sentence W(k)^(1/k) → ∞ compiled as a probe from `kthRoot_tendsto`). Not ours. Erdős's $500 question on erdosproblems.com/138 (two colours) is answered YES by
Theorem 1.1; the page's open-ended "improve the bounds" stays open. Status on the site: proof_claimed, CLOSED_BY_LITERATURE += 138.

## 1. The claim
`paper_sha256.txt`: 042acea33a57b58d17600a9ec5e0d8d6f424787c5edf28b9d8d5f9bd9297bd18 paper.pdf (openai/math `preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/paper.pdf`,
first public 6 Oct 2026 at adc7f124, unchanged at 1581d4c). `paper_pdftotext.txt` is the lossy text; `paper_tex/` is the paper's OWN LaTeX source from the repository
(what every seat quoted from — no extraction artefacts). Theorem 1.1: ∃ absolute K₀ such that for every k ≥ K₀ and every r ≥ 2, W_r(k) > k^{ck⌊log₂ r⌋}, c = 10⁻⁵;
hence W_r(k)^{1/k} → ∞ for each fixed r ≥ 2, including r = 2.

## 2. The chain of evidence
1. **Live page read first** (`world/e138.html`, `world/e138_thread.html`, `world/e138_claims.html`, 15 Oct 06:06Z via the Hetzner box): 0 proof claims, 8 comments
   (newest 24 Aug 2026: Campos–Fox–Schildkraut arXiv 2608.20824), Kozik–Shabanov ≫ 2^k listed as the best general lower bound, last edited 2 June 2026.
2. **Catalogue facts** (`world/openai_formalization.yaml`, `world/openai_lean_docs_160.md`, `world/openai_CONTENTS.md`, `world/QuantitativeVanDerWaerden.{lean,json}`):
   the paper is catalogued; the comparator names solution module `OAI.Combinatorics.ProgressionColoring.Main`, theorem `OAI.QuantitativeVanDerWaerden.uniform_lower_bound`,
   permitted axioms propext/Quot.sound/Classical.choice, `enable_nanoda: false`; docs/160.md: "the sharper intermediate estimates used in the paper are not part of the
   described formalization".
3. **Bloom's 8 Oct list** (`world/bloom_blog10_2026-10-08.html`): #138 among the 25 and among the 12 FrontierMath Erdős-list problems.
4. **Formal Conjectures** (`world/formal_conjectures_138.lean`): `erdos_138` research solved (11 Oct, commit 3dfd999d) citing this Lean at Main.lean#L12; the difference
   variant (DeepMind) and the W(k)/2^k variant (atlas-lean, citing CFS26) solved separately. teorth DB (`world/tracker_138_2026-10-15.txt`): open, last updated 2025-08-31.
5. **Seven hostile Opus seats** (`seats/REFEREE_BRIEF.md`, `seats/PROMPTS.md`, reports `seats/referee_<tag>.md`, scripts under `seats/*_checks|sources_scripts`):
   setup (§2) · counting (§3) · outer (§4) · dichotomy (§5) · perturbation (§6) · whole (dependency graph, §1, §7, appendix, Lean statements) · sources (25 references +
   the world). Every seat: HOLDS AS READ — no FATAL, no GAP in the proof; cosmetic/exposition notes only. Finite checks with failing controls in every seat (see the
   reports; e.g. the §5 toy cyclic model at k = 12/100/1056; the §3 arrangement lemma against three independent methods; the §6 separation over 5.76 M pairs).
   Findings more than cosmetic: (a) the Lean proves the §3 and §6 counts in WEAKER forms than printed (arrangement (e+2)²(s+1)^{2(e+1)}, word count 16(·)⁶, local
   (16005Dh)^{14D}, signatures exponent 8; prime lemma via Mathlib's Bertrand) — enough for §4/§6, but "Lean-verified as stated" would overclaim Lemmas 3.1/3.2/3.4/6.2;
   (b) the introduction's "at most quasipolynomial" upper half for k ≥ 4 rests on the unrefereed companion paper's (1.3) (its Lean leaves that bound out) — an aside,
   not Theorem 1.1; (c) sizes: k^{ck} > 2^k only for k > 2^{100000} ≈ 10^{30103}; K₀ from the paper's own inequalities ≈ 10^{41}–10^{45} (three seats' estimates);
   (d) the key-multiplicity bound is 2, not 4 (the Lean proves 2 — `affine_norm_band_card_le_two` — then weakens). The brief's description of Fox–Hunter as a
   Behrend-type covering was OUR error (sources seat); nothing on the page rests on it.
6. **Kernel replay** (`replay/`): sparse clone of openai/math at `replay/openai_math_rev.txt` (1581d4c), Mathlib `replay/mathlib_rev.txt` (d13f23b7 = v4.34.1), toolchain
   `replay/lean_toolchain.txt` (v4.34.1), lake-free, one thread nice 19, memory-gated (MemAvailable ≥ 28 GB before every lean). `replay/build.sh` (estimate written before
   CPU: `replay/ESTIMATE.md`), `replay/order.txt` (115 modules, import-topological), `replay/modules.tsv` (115 × rc=0 errors=0), `replay/steps.tsv`:
   - `steps_attempt1_smoke_import_error.tsv`: the first launch died at `smoke 1` on OUR probe (norm_num not imported) — nothing of the proof was touched; relaunched;
   - `cache_ready 0`, `smoke 0 2`, `comparator_module 0 12`, `comparator 0 8` (the comparator with its sorry compiled against Mathlib only; its pp.all block is the reference);
   - `build 0 430` — all 115 modules, 0 errors (`logs/mod_*.txt`);
   - `axioms 0 6` — `logs/axioms.log` under `--trust=0`: `uniform_lower_bound`, `uniform_lower_bound_floor`, `exists_uniform_lower_bound`, `kthRoot_tendsto`,
     `length_rate_tendsto`, `exists_cyclic_coloring` each depend on exactly [propext, Classical.choice, Quot.sound];
   - `rightshape 1 7` then `rightshape_v2 0` — v1 failed on OUR `simpa` (cannot evaluate Nat.log 2 2; `logs/rightshape_v1.log`, `probe/RightShape_v1.lean`); v2 uses
     `decide` (`probe/LogTactics_test.lean` shows which tactics work) and compiles: the page's sentence from `kthRoot_tendsto`, the explicit two-colour bound
     k^{k/100000} < W(2,k), non-vacuity 0 < W(2,k), and Theorem 1.1 in the comparator's exact type;
   - `wrongshape 1 6` — coefficient 1 for 1/100000 rejected, "Type mismatch" (`logs/wrongshape.log`) — the control that RightShape can fail;
   - `negcontrol 0 7` with `sorryAx` (`logs/negcontrol.log`) — the planted-sorry control;
   - `statement_match 1` then `statement_match_v2 0` — see §4; v2 (`statement_match.py`, `statement_match_v2.txt`): MATCH on the theorem and the four definitions
     W/IsRamsey/HasMonoAP/MonoAP (1,238/304/187/664/355 chars), STD_AXIOMS, CMP_SORRY_SEEN, ALL_STD_AXIOMS;
   - `leanchecker_fresh` — `leanchecker --fresh OAI.Combinatorics.ProgressionColoring.Main` over the whole import closure, Mathlib included, started 06:26:51Z;
     `leanchecker_fresh 0 3494` — exited 0 at 07:25:05Z, `logs/leanchecker_fresh.log` empty (silence is success); `leanchecker_missing_control 1 2` — a
     non-existent module exits 1 with "Could not find any oleans" (`logs/leanchecker_missing.log`), so the checker can fail. Closed on the entry 07:3xZ by the same seat.
7. **Third-party checks** (sources seat): two independent comparator runs report a pass (mathvet, 8 Oct; nealmcb, 11 Oct) — recorded in `seats/referee_sources.md`.

## 3. What is ours
The audit, the replay on a machine that is not OpenAI's, and the statement of exactly what the kernel did and did not certify. The theorem, the construction and the Lean
are OpenAI's; the identification of the Lean's weaker §3/§6 constants is the seats'.

## 4. Instrument notes (what failed, in which direction)
- Statement-match v1 printed MISMATCH on correct logs: `#check @kthRoot_tendsto` prints a leading `@`, which v1's head regex did not accept, so the solution's
  `uniform_lower_bound` block ran on into the next #check (1,911 vs 1,238 chars); and the universe-polymorphic defs print as `def …MonoAP.{u}`, which v1 keyed without
  the suffix (None → MISMATCH). v2 normalises heads. Both failures toward the alarming direction. v1 script/verdict kept beside v2.
- RightShape v1 failed on our `simpa using h` (Nat.log 2 2 not simplified); `decide` proves it. The theorem was never the issue; the v1 log is kept.
- The first driver launch died at smoke on our own probe's missing import — before any module was compiled.
- The brief told the seats Fox–Hunter's r ≥ 3 bound uses a Behrend-type covering; it does not (sources seat). Nothing on the page rests on it.
- `PRUNED.txt`: fetched files over 1 MB (and GitHub/Zulip API dumps over 500 KB under world/ — none load-bearing for the page) were not banked in git; their sha256 and sizes are recorded and every PDF's text extraction is kept.
- A blind consistency read of the rendered page (`entry/BLIND_READ.md`) was applied before deploy.

## 5. Reproduce
`replay/build.sh` (paths: `/tmp/oaimath/160/lean-build`, Mathlib checkout `/tmp/erdos0300/lean/mathlib4` at d13f23b7, scratch elan toolchain v4.34.1 at
`/tmp/oaimath/166/lean-build/home/.elan`), `replay/order.txt`, `replay/probe/*.lean`, `replay/lean_path.txt`. Seat scripts under `seats/` each print their own controls.
`SHA256SUMS` covers every file here.
