# Seat B — blind hostile copy-and-fact check of the #952 entry page (2026-10-22, ~03:40–04:05Z)

Read: `entry/entry_rendered.txt`, `entry/entry952.js` (incl. `summary`), `headline.js`, `lean_label.txt`, `closed_by.txt`,
against the paper (LaTeX + pdftotext), `repo` @1581d4c with git history, `lean-build/*`, `bridge/*`, `compute/*`, seat reports
G/S/I/L/W, `main_reading.md`, `MODEL_RECEIPTS.txt`, W's downloads (Gethner–Stark, Vardi, FME, Bloom blog, FC commit), the live
page snapshots, teorth yaml, and the July `{n:952,` ledger record. I also re-fetched: arXiv abs pages (1908.10392, 2401.08441,
2609.25050), Crossref for both DOIs, PR #6898 via `gh api`, FC `lean-toolchain` + `952.lean` at 3b7c94ec (sha256 matches
`FC_SHA.txt`), and HTTP status of every link. My own scripts and logs are in `seats/B_work/`.

Placeholder `BFS_PENDING_SENTENCE` ignored as instructed (note: `bfs_all.log` / `bfs_R4.log` are partial — they stop at
Q = 2465 / 1261 — and the replacement `bfs_slice.py` jobs were still running at 03:44Z; the sentence must not ship until those
logs end in a `finite_count` line for both R2 = 2 and R2 = 4).

---

## MUST-FIX

### M1. Jordan–Rabung "at most 48 steps" is false for the graph this page is about, and contradicts the page's own 100-point figure
> "Jordan and Rabung found the first moat around the origin (1970) and proved the uniform bound for steps of length √2, at most 48 steps (1976); Gethner and Stark say so on the page the paper cites."

- Gethner–Stark p. 290 do say "Jordan and Rabung [1976] proved that the conjecture is true for k = √2, with M_k = 48", and their
  conjecture is "starting on any Gaussian prime one can take at most M_k steps on distinct Gaussian primes". **That paraphrase is
  false for G_√2 with all associates (the paper's G_D).** I found a self-avoiding walk of **60 steps on 61 distinct Gaussian
  primes**, every step ≤ √2, inside the 100-point component through 1+i (verified twice, `B_work/jr48b.py`, `jr48b.log`):
  −4−11i → −3−10i → −4−9i → … → −7 → … → 7i → … → 3i → … → −1+i → … → −3 → … → −1−i → … → −3i → … → 1−i → … → 3 → … → 1+i → … → 7 → … → 4−11i.
- Vardi 1998 (p. 285, the page's own source) states JR precisely: **"Theorem 7.2 [Jordan and Rabung 1976]. The largest admissible
  √2-connected component has size 48."** Admissible = no congruence obstruction, i.e. it says nothing about the components that
  contain the small primes themselves (exactly the 1+i component). Restricted to the closed first quadrant the 1+i component has
  27 points and my search found only 21 steps (`jr48q.log`), so GS's "48" is probably a quadrant/admissible convention. Either way
  the page's sentence, read with the page's own G_D, is false, and a reader sees it two paragraphs after "the largest component
  has 100 points".
- Corrected: "Jordan and Rabung found the first moat around the origin (1970), and in 1976 showed that the largest *admissible*
  √2-connected set of Gaussian integers has 48 points (Vardi 1998, Theorem 7.2), which bounds every component of G_√2 that avoids
  the small primes; Gethner and Stark (p. 290) report this as their conjecture for k = √2 with M_k = 48. Near the origin that
  paraphrase is too strong: the component through 1+i has 100 points and contains a 60-step walk on distinct Gaussian primes."
- The July report (`ledger_data.js`, #952 md, §3) repeats the error ("the named Jordan–Rabung bound of 48 steps in a simple walk")
  — it needs a dated correction note too (SHOULD-FIX outside this page).

### M2. "the 154 split-prime sets with Q ≤ 4,000" — there are 416
> "For D = √2 and D = 2, none of the 154 split-prime sets with Q ≤ 4,000 blocks walks: their densities are at least 0.48, and walks percolate."

`scan.py` (and `bfs_all.py`) build sets only from split primes **p < 400**. There are **416** sets of split primes with product
≤ 4000 (all singletons p ≡ 1 mod 4 up to 4000, and {5, p} for p up to 800, are missing). Corrected: "none of the 154 sets of
split primes below 400 with Q ≤ 4,000 blocks walks". (0.48 is right: min density 0.4831 at {5,13,17}, also over all 416.)

### M3. The "where to look for the hole" sentence and the (c) label are incomplete and inconsistent with the paragraph above them
> "The printed proofs of Lemma 4.1, of (3.1)'s use, and of Proposition 6.2 rest on reading alone, by our seats and by us."
> "The paper's printed route through Lemma 4.1, (3.1) and Proposition 6.2 is (c), read but not machine-checked, since the Lean goes around it."
> "If there is a hole, it is not in the checked statement. It could be in Mathlib or the Lean kernel, which everything here trusts. Or it could be in the paper's §6.3–6.4 and Lemma 4.1 as printed, which the Lean does not follow."

- The page names **four** departures; the "rest on reading alone" list and the (c) label name three — difference (4), the paper's
  growing-window schedule (§6.1, Lemma 6.1's log(1+S_V) ≤ 2gV, hence (6.8) and the paper's own instantiation of §§7–8 and the
  final count), is not machine-checked either (seat L: "the paper's base-B, M-window schedule", "Lemma 6.1's 2gV bound",
  "(6.10)–(6.11) as stated" — all "not covered").
- L also records that the Lean **does not verify the explicit bound of Proposition 2.1** ("Same route, different explicit bound"),
  yet the page quotes "the paper's bound is max{Q², |E| + (K_D − 1)|E|Q²}". That formula rests on reading (L and main_reading
  checked it by hand).
- The final sentence then drops (3.1) as well — three different lists in one entry.
- It also conflates two kinds of hole. A hole in **Theorem 1.1** could only be in Mathlib, the kernel/leanchecker, or the
  statement's fidelity (pp.all proves comparator = solution; comparator = paper/problem rests on seat L's *reading*). A hole in the
  **paper as printed** could be anywhere the Lean takes another route, and would not touch the theorem.
- Corrected (one option): "A hole in Theorem 1.1 itself would have to be in Mathlib, the Lean kernel or leanchecker, or in the
  match between the comparator statement and the problem, which is mechanical against the comparator and by reading against the
  paper (seat L). A hole in the paper as printed could be in any step the Lean does not follow: the use of (3.1), the torus-degree
  proof of Lemma 4.1, the growing-window schedule of §6.1 with Lemma 6.1, the ladder of §6.3–6.4 and Proposition 6.2, and the
  explicit bound in Proposition 2.1; such a hole would be in the exposition, not the theorem." Make the (c)-list and the "rest on
  reading alone" list say the same.

### M4. Misattribution: the norm-vs-distance note is the PR author's, not "FC's reviewers"
> summary: "FC's reviewers listed the norm-to-distance step as missing from the linked proof."
> "Its only value is that it supplies the step FC's reviewers recorded as missing."

`gh api …/pulls/6898`: PR #6898 was **opened and merged by mo271**; the text is a section headed "Reviewer notes" in the PR
author's own description (notes *for* reviewers), squashed into commit 3dfd999. Corrected: "FC's PR #6898 (by maintainer mo271)
recorded the norm-to-distance step as not in the linked proof" / "…the step PR #6898 recorded as missing". The quoted words
themselves are verbatim and fine. Also fix the garbled gloss "among links that differ from the linked theorem" — the PR says the
links "differ from the repository statement": "among the links whose theorem differs from FC's statement 'by a routine transport
that is not in the linked proof'".

---

## SHOULD-FIX

S1. **Theorem 5.2 misdescribed.** "§5: a coverage-transfer theorem (5.2) turns near-maximal joint entropy into the statement that
the terminal residue … outside fewer than p^{1−β} exceptions." Theorem 5.2's hypotheses include *coverage of every later
conditional law* (at τ′ = τ + 4δ, β′ ≤ β); it lowers the floor and improves the exceptional exponent. Corrected: "turns
near-maximal joint entropy, together with coverage at a later checkpoint, into coverage at the earlier one: …".

S2. **Labels have no legend and (c) is miscalibrated.** The page uses (a), (c), (d) without defining them; elsewhere the site
defines (c) as "plausible, unverified (by a human)" and labels seat-read printed proofs (a)/(b) (#1150 "the whole proof is (a)",
#416 "(b), rigorous modulo cited results"). Add the legend, and either label the printed route as it is — (b) modulo Selberg for
(3.1) and Hatcher for Lemma 4.1's degree step, (a) for Prop 6.2 as read — with "not machine-checked", or say explicitly why (c).
The sections where the Lean follows the paper (Lemmas 4.2–4.3, Thm 5.2, Prop 7.1, Lemma 8.1) carry no label at all.

S3. **"If there is a hole, it is not in the checked statement."** The statement is checked mechanically only against the
comparator; its fidelity to Theorem 1.1/#952 is seat L's reading. Say so (folded into M3's rewrite).

S4. **Unbanked evidence.** "Both of our programs, and a separate script of seat W's, reproduce his figure. With 17 added (Q = 1105)
the largest component has 80 points, again in both programs." `compute/` contains a C log for 580 only (`scan_R1.log`); there is
**no log** of the BFS program on {5,13} or of either program on {5,13,17} at D = 1. I re-ran both: C `FINITE max_component=80`,
BFS `FINITE max_component=580` and `=80` (`B_work/bfs_1105_R1.log`). The numbers are right; bank logs in the bundle, which promises
"the two miniature-sieve programs and their logs". Also say "for unit steps" in the 80-point sentence.

S5. **Gethner–Stark's 2-moat is not a split-prime sieve.** "Gethner and Stark's obstruction for steps of length 2 has period
7,113,990 = 2·3·5·13·17·29·37" sits right after the split-only search; GS also sieve out 1+i and 3, which Theorem 1.2's sieve never
uses, so the comparison with Q ≤ 4,000 is not like for like. Add "(it also removes 1+i and 3, which Theorem 1.2's sieve does not)".

S6. **Our heuristic reads as the paper's.** "The paper calls the method 'related to Tao's entropy-decrement argument'. The heuristic
behind it: keeping a walk inside a set of density ρ costs log(1/ρ) per step…" — the heuristic is not in the paper (grep). Prefix
"Our gloss, not the paper's:".

S7. **S's §§5–6 check is sampled in T.** "every explicit inequality of §§5–6 at every checkpoint of every window for M = 84, 86 and
90" — S_params.py checks every i ≤ J and every window but **seven values of log T per window** (S report: "7 points per window").
Say "at every checkpoint, at seven batch sizes in each window".

S8. **Periodicity sentence skips finiteness.** "A periodic set with no infinite walk has no component with more than Q² points,
since two points of one component that differ by a period would make it invariant under that translation." Invariance is only
absurd for a *finite* set; add "every component is finite (König, local finiteness), and …". Also E and K_D in the quoted bound are
undefined on the page.

S9. **"A seat that read all 41 files"** — L read "the comparator statement, Model.lean, Main.lean, and the declarations that carry
the argument across all 41 files". Say that.

---

## NIT

- "3,480 s": log says 3479.61 s — fine as rounded. "peak 6.7 GiB" with four workers is a per-process peak (max 7,071,816 kB); say
  "per process". 7 min 39 s, 41/41, 12,703 lines, 6.7/8.2 GiB, tree c84262a9 at adc7f12/fd4aeeb/1581d4c, comparator/scope/preprint
  unchanged, seven matcher mutations, sorryAx control, leanchecker missing-module rc 1, forbidden-token grep: all **verified**.
- "Theorem 1.1 is therefore machine-checked" — "therefore" reads as if it follows from the route differences; drop it.
- "sum … is at most log K_D, the entropy of one increment" — Lemma 8.1 gives ≤ log K_D + o(1), and log K_D *bounds* one
  increment's entropy.
- "the file the release asks readers to check" — `docs/028.md` only links it as the "Comparator statement"; say "the statement the
  release designates for comparison".
- "Tao's database still lists #952 as open" — footer calls it the community database teorth/erdosproblems; use that name.
- FME: "68 problems" — the paper says 68 *conjectures* (50 from FC covering 48 problems + 17 others); abstract says "68 Erdős
  problems". Prefer "68 conjectures".
- FC statement: tagged solved 11 Oct, but the `¬ ∃ … .norm < C` form dates from 7db2ea3 (14 Oct); "It states" → "It now states".
- Bridge control: "the same file with OpenAI's theorem replaced by sorry" — the mutant replaces the *proof that invokes* fullMain
  by `sorry`. `steps.tsv` also shows first-attempt `mut_sorry_*` rc=1 runs superseded by `_v2`; explain in the bundle.
  `BridgeMutStep.lean` mtime (00:21:12) is after its log (00:16:25); content still matches the logged error (line 30:30) — re-run
  before bundling.
- "Seat W searched GitHub … found none" — W's caveat: default branches only; Lean Zulip/X not searched (page says the latter later).
- S's fifth exposition note (S5, O_{g₀} notation) is omitted from "S's exposition notes: (1)…(4)" — harmless.
- Seats S and W died at session limits at 00Z and were re-run at 03Z (MODEL_RECEIPTS); sibling entries cite the receipts file.
- "Our bundle" link 404s (private; disclosed). DOIs redirect to T&F (403 to bots; Crossref confirms both titles/pages). All other
  links resolve (200). erdosproblems.com 403 from this egress only.
- Headline line "The Lean takes a shorter route than the paper through its middle" — L says "different route"; "shorter" is a judgment.

## Verified without objection (sample)
Problem paragraph (page text, Er77c/Er80 quotes, edited 08 Apr 2026, 0 proof claims, comments suspended, no OpenAI mention; teorth
open 2025-08-31). Theorem 1.1/1.2, Prop 2.1 bound, Lemma 4.1/4.2/4.3 glosses, log T ≈ 100^m, g₁ = e^{−M³}, g₂ = e^{−100M²⁰},
L ≈ T^{2/5}, c₁/log T (Prop 7.1), Tao quote, equation/lemma numbering ((3.1), (4.2), 5.2, 6.1, 6.2, 7.1, 8.1). The four Lean
departures match L's table. All seat numbers (1,547; 65,535; 4,001; i < 1,500; M = 84/86/90; C_D = 10⁹, g₀ = 10⁻⁶ at M = 90/120;
four negative controls; 30-digit artefacts; constant order). FC text, sha, PR date (merged 2026-10-11T08:10Z), FC pin v4.33.1,
bridge Lean + axioms + controls (norm < C + N(xₙ) false via primes ≡ 3 mod 4; no-injectivity false via constants), verbatim check
and its mutation. Miniature: singles < 65 infinite, {5,13} = 580, map z ↦ (1+i)z+1 onto odd integers prime to 65 = GS's √2 moat,
Vardi §7's 580 (verbatim), 7,113,990 factorisation, parity remark, July checker rerun (global max 100, one exceptional component,
generic ≤ 49). Das and Stumpenhusen both withdrawn (arXiv comments re-fetched). FME arXiv 2609.25050 v1 6 Sep 2026, #952 listed.
Bloom's "should not be read as any kind of endorsement". KitaKen1 variant (standard axioms, implies FC's statement).
