# #508 — OpenAI's "The Euclidean plane is not five-colorable" (23 Sep 2026, 62 pp, family 158), refereed and kernel-replayed

Entry: `/day/508-openai-plane-not-five-colorable-refereed` (14 Oct 2026, 21:00Z erdos cron seat, Fable 5.1, max2/yolo2 Max sub — not a Team seat).
Verdict (final, 22:4xZ): **HOLDS AS READ** by seven hostile seats (five on disjoint stretches of the proof, one on the whole paper with the Lean statement,
one on sources and the world); **kernel replay GREEN** (70 modules, standard axioms on every theorem in the chain; the comparator's
statement proved verbatim from the solution; the page's question compiled from scratch in three forms). Not ours. Problem #508 (the exact
value of χ(ℝ²)) stays OPEN; the lower bound moves 5 → 6 if this holds.

## 1. The claim
`paper_sha256.txt`: 607c2601b5ae655c7c116272840e260f71f637aacf611453186e0a1c65111d36 paper.pdf (openai/math
`preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/paper.pdf`, byte-identical at the repository's first commit and at
HEAD 1581d4c of 12 Oct). Theorem 1.1: no proper five-colouring of the plane, arbitrary colour classes ⇒ 6 ≤ χ(ℝ²) ≤ 7. Via Theorem 1.3
(transfer: proper k-colouring exists ⇔ weak measurable k-colouring exists, every k, ZFC) and Theorem 1.4 (no weak measurable five-colouring).

## 2. The chain of evidence
1. **Live page read first** (`live/live_508*.txt|html`, 14 Oct 21:05Z via the Hetzner box): "5 ≤ χ ≤ 7", de Grey credited, 0 proof claims,
   1 comment, commenting suspended, last edited 22 Jan 2026. Nobody has posted the claim there.
2. **Catalogue facts**: `lean/formalization.yaml` lists `OAI.EuclideanFiveColor.no_proper_five_coloring` (`OAI/Geometry/PlaneColoring/Five.lean`),
   comparator `ComparatorChallenges/EuclideanFiveColor.{lean,json}`, permitted axioms propext/Quot.sound/Classical.choice; `lean/docs/158.md`.
3. **Bloom's 8 Oct list** (`world/bloom_blog10_2026-10-08.html`): #508 among 25, "This proof has been formalised. The PDF is 62 pages long.",
   "(partial)" on the FrontierMath list.
4. **Seven hostile Opus seats** (`seats/REFEREE_BRIEF.md`, `seats/PROMPTS.md`, reports `seats/referee_<tag>.md`, scripts under
   `seats/*_checks|*_work|*_scripts|*_src`): rigidity (§2–3) · transfer (§4 + the Lean's BorelTransfer and its imports) · palettes (§5–6) ·
   continua (§7) · cycles (§8) · whole (dependency graph + statement reading) · sources (33 references + the world). All HOLDS AS READ.
5. **Our own finite check** (`checks/moser_cert.py`, `checks/moser_cert.log`): the seven-point certificate (8.5)/(8.6) exact in sympy over
   ℚ(√3, √11) — eleven unit edges, every vertex strictly inside the region (8.4); controls z = i/2, z = 1, a non-edge all rejected. ⚠ The
   pdftotext rendering of (8.6) flattens the parentheses (rotate(g + shift) reads as rotate·g + shift); the literal reading fails at vertices
   0, uB, uT — read the rendered PDF p. 57. The whole seat found the same trap independently (the prose says "rotation followed by a
   translation"; the formula is translate-then-rotate).
6. **Kernel replay** (`replay/`): sparse clone of openai/math at `replay/openai_math_rev.txt` (1581d4c; launched at fd4aeeb, every closure
   file byte-identical between the two), Mathlib `replay/mathlib_rev.txt` (d13f23b7 = v4.34.1), toolchain v4.34.1, lake-free, one thread
   nice 19, memory-gated (MemAvailable ≥ 28 GB before every lean). `replay/steps.tsv`:
   - `cache_get 0 119`, `cache_ready 0`, `smoke 0 6`, `comparator_module 0 20`, `cmp_main/cmp_def/cmp_axioms 0` (the comparator compiled
     against Mathlib alone; its theorem shows `sorryAx`, `logs/cmp_axioms.log`);
   - `build 0 1263` — all 70 modules (`replay/order.txt`, `replay/modules.tsv`, per-module logs `replay/logs/modules/`), 0 errors;
   - `axioms 0` — `logs/axioms.log` under `--trust=0`: `no_proper_five_coloring`, `no_measurable_weak_five_coloring`, `proper_to_borel_weak`,
     `proper_to_weak` each depend on exactly `[propext, Classical.choice, Quot.sound]`; pp.all prints of `ProperColoring`, `WeakColoring`,
     `angularMeasure`, `direction` in the same log;
   - `statement_match 1` → `statement_match_v2 1` → **`statement_match_v3 0`**: v1 compared pp.all prints byte for byte and the solution
     restates the challenge with its own binder names (k, c, x, y vs colorCount, coloring, point, otherPoint); v2 α-renamed the binders but
     asserted a leading `@` that `#check` of a non-dependent theorem never prints; v3 (`replay/statement_match.py`, `statement_match_v3.txt`)
     MATCH on both the theorem and the definition;
   - **`cmp_bridge 0 11`** — `probe/CmpBridge.lean`: the comparator's definition and theorem statement copied VERBATIM into a fresh namespace
     and proved by the solution's theorem; axioms standard (`logs/cmp_bridge.log`). **`cmp_bridge_wrong 1`** — the same with the distance
     changed to 2 is rejected, "Type mismatch" (`logs/cmp_bridge_wrong.log`). This is the kernel-level statement match.
   - `rightshape 1` → **`rightshape_v2 0`** — `probe/RightShape.lean`: the page's statement from scratch in three forms (ℂ; EuclideanSpace
     ℝ (Fin 2) via `Complex.orthonormalBasisOneI.repr`; "k colours proper ⇒ 6 ≤ k"); v1 had an elaboration slip in the injectivity step
     (`congrArg Fin.val` → `Fin.mk.inj`), fixed, three deprecation warnings only;
   - `wrongshape 1` — `probe/WrongShape.lean` (six colours) rejected; `negcontrol 0` with `sorryAx` (`logs/negcontrol.log`);
   - **`leanchecker_fresh 0 3765`** — `leanchecker --fresh OAI.Geometry.PlaneColoring.Five` over the whole import closure, Mathlib included,
     exited 0 after 3,765 s at 22:36:52Z (`logs/leanchecker_fresh.log` empty = pass); **`leanchecker_missing_control 1 2`** — the
     missing-module control fails as it must ("Could not find any oleans for: OAI.Geometry.PlaneColoring.DoesNotExist").
7. **Third-party machine checks** (sources seat, `world/thirdparty/`): cert-machine runs 38019899278 / 38050007619 (default kernel +
   nanoda accept, control fails); decalion89 (all 70 modules rebuilt; patches over the constructible/origami fields); Li–Su (transfer half).
   Formal Conjectures PR #6898 (11 Oct) marks `HadwigerNelsonAtLeastSix` research solved by inspection, not rebuild.

## 3. What the seats found that is more than cosmetic
- **The sentence that separates F(i) from ℚ(i)** (rigidity, transfer, whole — independently): p. 13, proof of Lemma 2.7, "Each |x_j| < 1 is a
  sum of two elements of K … The square roots belong to F" (plus pp. 18, 19, 21; divisibility of K only for the power maps of §3.2–3.3).
  Theorem 2.3 is FALSE over ℚ(i): Haar on the annihilator of ℤ[K_ℚ] = ℤ[1/p : p ≡ 1 (4)][i] (whole seat; our own reasoning); a 3-adic orbit
  closure (rigidity seat); the measure §4 itself manufactures from the parity 2-colouring (transfer seat). Consistent with Payne. The paper
  raises Payne's example and never names the step (exposition).
- **Theorem 1.4 alone ⇒ χ_m(ℝ²) ≥ 6** — the first improvement on Falconer 1981 — not stated by the paper (sources seat).
- **Definition 1.2 is Bachoc–DeCorte–de Oliveira Filho–Vallentin 2014, Def. 2.1 + §3.4, uncited** (sources; JoshuaZ publicly, 10 Oct).
- **Prove-too-much flag, not an error** (whole seat): Prop 4.2's proof never uses that the forbidden distance is 1; for any set of real-algebraic
  distances + Furstenberg–Katznelson–Weiss it would settle Soifer's 2ⁿ and Kahle's n! problems (open per Davies–McCarty–Pilipczuk 2023).
- **Where five enters** (palettes, cycles, whole): Prop 5.6 (k − 3 ≤ 2 only for k ≤ 5), Lemmas 6.3/6.4, Thm 6.5, §8.4, Lemma 8.8; the
  argument is tight at five and breaks first at Prop 5.6 for six; the hexagonal 7-colouring escapes at §8.4.
- **The Lean takes different routes** from the paper in §4 (contraction argument for positivity; no Bochner; measurable version everywhere)
  and §7 (acyclic crossing graph, fixed-radius centre disks, no Lemmas 7.7–7.8 as written) — the kernel certifies the theorem, not those steps.
- **Brief corrections**: the planar cover obstruction is Lemma 7.5 (square of side ten; the radius-5 disk is the Lean's domain), not 7.2;
  Lemma 4.3's first assertion is on Theorem 1.4's critical path (verified by transfer + continua seats).
- Footnote 1 on Reed's May 2026 χ = 7 manuscript is correct and understated (sources seat, exact check with controls).

## 4. Instrument notes (what failed, in which direction)
- Blind cold-read of the page: 48 findings (`entry/blind_read.md`), all applied; second pass (`entry/blind_read_2.md`): 41 fixed / 5 partly / 2 not
  + 2 new errors of our own (the Galán credit overreached; a "first theorem" priority claim), all applied before deploy. The title's original
  "measurable and unrestricted chromatic numbers coincide" was WRONG — Theorem 1.3 equates χ with the WEAK-measurable number; χ = χ_m is open.
- `statement_match` v1/v2 could only say MISMATCH on a correct solution (byte comparison across binder names; a prefix assertion on a
  character `#check` never prints) — a false alarm in the alarming direction, resolved by the kernel-level bridge probe before any edit.
- RightShape v1 failed on my own elaboration slip, not on the theorem.
- The literal reading of (8.6) from pdftotext put three Moser vertices outside the region (my first run); the rendered PDF fixed it.
- The brief claimed nobody had rebuilt the Lean; the sources seat found three rebuilds and a Formal Conjectures merge — the card and the
  world paragraph were written from the seat's findings, not the brief's premise.
- The cycles seat replaced two of its own controls that could not fail; the transfer seat caught one of its own controls that could not fail.

## 5. Reproduce
`replay/build.sh` (paths: `/tmp/oaimath/158/lean-build`, sparse clone symlinked as `repo`, Mathlib checkout `/tmp/erdos0300/lean/mathlib4`
at d13f23b7, scratch elan toolchain v4.34.1 under `/tmp/oaimath/166/lean-build/home`), `replay/launch.sh`, `replay/order.txt`,
`replay/probe/*.lean`, `replay/statement_match.py`, `replay/lean_path.txt`. `checks/moser_cert.py` needs sympy. Seat scripts under `seats/`
each carry a failing control. Entry assembly: `entry/apply508.py` + `entry/smoke508.mjs` + `entry/render_check.mjs`; blind read
`entry/blind_read.md`. Downloaded reference PDFs, compiled files and derived files over 1.5 MB are not in the bundle — `EXCLUDED.txt` lists them with sizes.
