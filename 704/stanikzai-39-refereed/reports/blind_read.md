# Blind read: #704 page, review and email (Stanikzai, α(J(13,5,3)) = 33)

Cold reader seat, 13 Nov 2026. I read `page/entry.html`, `page/review.md`, `page/email.txt` and `page/insert.py` (title, summary, card) first, then checked them against the paper text, `world_seat.md`, `referee_indep.md`, `indep/` and `indep/runs/`. My scratch work is in `(the blind reader's scratch, not bundled)/`. I modified nothing else.

Tags: **MUST** = factual error, overclaim or unsupported claim. **SHOULD** = clarity or precision. **NIT** = polish.

## Bottom line

The mathematics holds up. The Lemma is true. My own brute force found no counterexample in about 40,000 linked classes of random maximal families in J(9..13,5,3), nor in an exhaustive check of every linked triple and quadruple in J(9,5,3). The uniqueness argument is correct, and every number I could recompute matches.

The problems are elsewhere:
- **Pending runs.** Text outside the placeholders already assumes the cliquer run and the enumeration over the paper's leaves have both finished.
- **Bundle.** It contains only a README. Several page claims have no saved artifact at all.
- **Test sizes.** Two solver tests are described more strongly than the graph sizes they used.
- **Missing steps and caveats.** The uniqueness theorem needs one step it doesn't state and one caveat it doesn't carry.

## Independent recomputations (all match unless noted)

| Claim | My check | Result |
|---|---|---|
| 1,287 vertices, degree 280 | direct count | ✓ |
| 851 | sets with no 3-intersection with v or u | 853 including v, u; **851 excluding them** (see M5) |
| 286 triples, ≤ 28 members | C(13,3) = 286, ⌊286/10⌋ = 28 | ✓ |
| 105 leaves, 221–357 | `n13_s33_lg350/manifest.json` | ✓ (thresholds 27–32; one leaf at 357 because of the depth cap) |
| 63 million nodes, 71 s, 10 cores | `results_clq2.json` | ✓ 63,037,331 nodes; wall 70.9 s; 10 chunks |
| 3,184 CPU s | `their_leaves.log` | ✓ (this is the sum of per-leaf wall times of single-threaded runs) |
| 17–30 colours | re-verified all five certificates against the leaf files myself (sha256 match, 0 monochromatic edges) | ✓ distinct colours 17/30/26/29/30 for leaves 16/169/170/173/176, each below its threshold 33/31/32/30/31 |
| 151 / 115 solutions | `enum_all.txt` | ✓ 151 in 105 leaves (16 leaves with solutions, exactly the 16 SAT leaves of `results_clq2.json`); 115 in 1,876 leaves; 0 CAPPED |
| all solutions one type | **networkx VF2 isomorphism, no nauty**, all 266 vs Appendix A | ✓ 0 non-isomorphic |
| \|Aut\| = 48 | VF2 automorphism count on the point/set incidence graph | ✓ 48 |
| 13!/48 = 129,729,600 | arithmetic | ✓ exact |
| five classes: 3 blocks, sunflower 9, sunflower 6 | connected components of the linked graph on W | ✓ the 6-sets meet pairwise in exactly 2 |
| 1,876-leaf tree is a sound tree | ran `replay.py` (copy) on `n13_s32_lg300` and `n13_s32_lg350` | ✓ `REPLAY OK` for both (not saved in runs/; see M3) |
| 58 (Delsarte) | own LP (scipy, Eberlein eigenmatrix) | ✓ optimum 58.5 |
| 40.6 GB / 1.26 TB | 195 raw sizes from their result JSONs, plus Table 5 values for leaves 1, 10, 16, 25 and 77 | ✓ 1.258 TB |
| 28 and 6 gate leaves | gate manifests | ✓ n=11 gives 28 leaves (s=17: 13 SAT, s=18: 28 UNSAT); n=10 gives 6 leaves, UNSAT |
| CP-SAT 12 and 18 | `gate_cpsat_n1{0,1}.txt` | ✓ |
| 37 / 38 / 36 / 32 / 164 / 2,516 | world_seat.md (primary quotes) | ✓ |
| six negative controls | `runs/neg_replay13.txt` | ✓ six REJECTED |
| 60 min CP-SAT run | `cyc39_run.txt` | ✓ UNKNOWN at 3,601.7 s. The 10-minute frob39 run has **no saved log**. |

---

## Findings

### MUST

**M1. The pending runs leak into text that has no placeholder.**

The cliquer run has finished 5 of 105 leaves in `runs/n13_s33_lg350/cliquer/log.jsonl`; the referee's separate 41 sit in `/tmp/ref704`. The enumeration over the paper's 200 leaves is still running (`theirs_s32/enum/d*.txt`). The following sentences are only true if both finish clean.

- *insert.py summary:* "We checked it with our own code by a different tree and two solvers".
- *HEADLINES tag:* "RE-DERIVED HERE BY A DIFFERENT TREE + 2 SOLVERS".
- *review.md:* "Our own solver refutes all 105, and so does cliquer {{CLIQUER_REVIEW}}." This reads wrongly for any partial outcome, because "so does cliquer" asserts all 105.
- *review.md:* "We enumerated every 33-set in every leaf of three decompositions: two of ours and your own 200 leaves." There is no placeholder here.
- *email:* "Our own solver refutes all 105, and so does cliquer." There is no placeholder.
- *email:* "We listed every 33-set in every leaf of three decompositions: two of ours and your 200 leaves … All of them have the same nauty canonical form." There is no placeholder.
- *page:* "and the paper's own 200 leaves {{THEIRS_ENUM}}. Every solution in all three is a copy…". "All three" is wrong unless THEIRS completes.
- *page, referee bullet:* "And the second solver had not finished, so a single solver was reporting; see the leaves item above." This implies cliquer has since finished.

**Fix:**
- Gate the summary, card tag, review and email on the final counts.
- If the run is partial, write "cliquer, so far on N of 105 leaves (all infeasible)" and "two of ours, and the paper's 200 leaves (finished/N of 200)" everywhere, including the email.
- If cliquer ever returns SAT, or THEIRS_ENUM finds a second class, stop. That would contradict the VeriPB chain or our trees, and the page cannot ship as written.
- `{{CLIQUER_SHORT}}` reads correctly for any outcome.
- `{{CLIQUER}}` sits after "…with cliquer on about 1,000 more…". Start it with "On the real leaves, cliquer…" so the word doesn't repeat awkwardly.

**M2. "asked for four fixes, all made here" is not accurate.**

> "It broke nothing and asked for four fixes, all made here."

The referee's verdict lists **five** required fixes, (a)–(e). Two are not done in the files that will ship:
- **(d)** `indep/ESTIMATE.md` still says leaves are decided by "(ii) OR-tools CP-SAT", and still says the route "shares no code and no decomposition with theirs".
- **(e)** `indep/tree.py`'s docstring still says "Route (shares no code or decomposition with the submission)" and "Branch vertex = a max-degree vertex". That contradicts the page's corrected wording, and `tree.py` is in the bundle.

The page's own list also includes "the solver's multi-word code had not been tested; it now has been." Our test for that, `runs/test_clq2_vs_cliquer.txt`, which the bundle README cites, is **0 bytes**, and no process is running it. The only completed multi-word test is the referee's, in ephemeral `/tmp/ref704/diff/`.

**Fix:**
- Fix the `tree.py` docstring.
- Drop or fix `ESTIMATE.md`.
- Rerun `test_clq2_vs_cliquer.py` to completion, or copy the referee's `diff_test.py` and its logs into the bundle.
- Then write "asked for five fixes; all are made" or list them.

**M3. The bundle is empty, and several page claims have no artifact.**

`bundle/` holds only `README.md`, and label (d) says "reproducible from our bundle". Claims with nothing saved in `indep/` or `runs/`:
- **Colouring re-check.** "The five leaves the paper certifies by colouring are properly coloured…" has no script or log anywhere. The claim is **true**: I re-verified it myself, see the table. The README's "(page)" is not evidence.
- **nauty controls.** "equal labels on 200 random relabellings … different labels on 33 families with one set changed" is not in `classify.py`, and there is no log.
- **Referee material.** "per our referee instance, with cliquer on about 1,000 more up to 350 vertices" and the referee's 41 cliquer leaves exist only in `/tmp/ref704/` (`diff/`, `cliquer_tally.json`).
- **Smaller missing outputs.** There is no saved output for `test_clq.py` (the "1,800"), `test_enum.py` (the "300"), `track.py` ("lands in a leaf"), the `frob39` 10-minute run, or a replay of the two s=32 trees used for the uniqueness theorem.
- **Broken README pointer.** `runs/test_clq2_vs_cliquer.txt` is empty.

**Fix:** copy every script and log the page relies on into the bundle. That includes `/tmp/ref704`'s `check3.py`, `diff_test.py`, `cliquer_*`, `mutate.py` and their logs, plus a colouring-check script, which I can supply from `(the blind reader's scratch, not bundled)`. Push the bundle and confirm the GitHub URL in `insert.py` resolves before publishing.

**M4. The uniqueness theorem is uncertified, and neither the page nor the email says so.**

The paper's whole frame is certified versus uncertified. Our α ≤ 33 re-derivation is correctly flagged as resting on solver verdicts. Theorem (d) rests on the same kind of thing:
- an enumerating branch-and-bound (`clq3`) with no proof log,
- plus nauty, plus our tree.

The page states it as a flat theorem, and the email says "Your Question 5.2 has an answer, and the answer is yes."

**Fix:**
- *Page.* In "What this does not do", add: "The uniqueness theorem is likewise uncertified in the paper's sense: it rests on our enumerating solver's lists and on the canonical-form comparison, cross-checked on three decompositions, not on proof logs."
- *Email.* Write "…the answer is yes, by an uncertified computation (an exhaustive enumeration, cross-checked across three decompositions)".

**M5. The 851 count is mis-stated.**

> "Then α ≤ 33 says: among the 851 sets that share exactly 3 elements with neither, no 32 are pairwise free of 3-element intersections."

The 5-sets sharing exactly 3 with neither {0,1,2,3,4} nor {0,1,2,3,5} number **853**, because the two sets themselves qualify. 851 excludes them.

**Fix:** "among the 851 other sets that share exactly 3 elements with neither".

### SHOULD

**S1. The uniqueness argument skips the step it actually needs.**

> "Orbital branching never loses a solution: each one has an image in some leaf. So listing every solution in every leaf and sorting them by isomorphism type catches every type."

For the decision problem, "each generator is a symmetry mapping the candidate set onto itself" suffices. For **types**, the image of a solution must be the same family relabelled. That requires the branching permutations to fix the pair and every forced set (as a family).

- **It holds by construction.** The partition is refined by every forced set. I checked all 212 and 401 generator uses in the two s=32 trees, and every one maps the family of forced sets plus {v,u} onto itself.
- **But it is neither stated nor checked.** `replay.py` does not check it either.

**Fix:** "Orbital branching never loses a solution: the permutations used at each branch fix the pair and every set already forced, so each 33-set through the pair has a relabelled copy of itself in some leaf." Add that assertion to `replay.py`.

**S2. The 151 and 115 counts look like family counts.**

> "our 105-leaf tree (151 solutions), a 1,876-leaf tree (115 solutions)"

A reader will ask why the counts differ, and how 151 squares with 129,729,600. These are representatives left after symmetry pruning. 483,840 = 129,729,600 × 96 / 25,740 maximum families contain any given linked pair, since W has 96 linked pairs and J has 25,740.

**Fix:** "(151 and 115 representatives; how many survive depends on how much symmetry the tree used)".

**S3. Two of the "three decompositions" are nested.**

> "We ran this on three different decompositions"

The 1,876-leaf tree is a **refinement** of the 105-leaf tree: all 104 internal nodes of the latter are internal nodes of the former. Both trees come from the same rule and root.

**Fix:** "our 105-leaf tree, a finer 1,876-leaf refinement of it, and the paper's own 200 leaves". The paper's tree is the only genuinely different one.

**S4. The solver tests are described more strongly than their graph sizes support.**

> "It agrees with networkx on 1,800 random cases"

- **The 1,800 cases.** `test_clq.py` runs `./clq`, not `clq2`, on graphs of **≤ 60 vertices**: one 64-bit word.
- **The enumeration test.** "Our enumerating solver agrees with networkx's clique counts on 300 random graphs." `test_enum.py` uses graphs of **≤ 28 vertices**. The multi-word enumeration path that produced 151 and 115 on 210–357-vertex leaves has no independent count test.

Corroboration exists:
- clq3's 16 solution leaves are exactly clq2's 16 SAT leaves.
- The referee's 576 images of W landed in those 16 leaves.

**Fix:**
- State the sizes: "on 1,800 random graphs of up to 60 vertices", "300 random graphs of up to 28 vertices".
- Ideally run `clq3` against an independent all-cliques count (for example `cliquer -a -m τ`) on 65–360-vertex graphs and cite that.

**S5. "about 1,000 more" counts the same tests twice.**

> "with cliquer on about 1,000 more up to 350 vertices"

The referee's test was 107 graphs × τ ∈ {ω−2..ω+2}, about 535 decisions. Each was run on two builds of the same source, about 1,070 runs.

**Fix:** "with cliquer on 107 more random graphs (about 500 decisions) of 40–350 vertices, across every 64-bit word boundary".

**S6. The page uses two labellings of the ground set.**

> "…to {0,1,2,3,4} and {0,1,2,3,5}" and "x ↦ x+1 (mod 13)"

The same page uses Appendix A labels on {1,…,13}, for example {1,…,6} and core {2,8,11,13}.

**Fix:** use {1,2,3,4,5} and {1,2,3,4,6} for the pair, and "the 13 points as residues mod 13" for the CP-SAT sentence.

**S7. "Colourings unchanged by x ↦ x+1" is impossible as written.**

> "CP-SAT searches for colourings unchanged by x ↦ x+1 (mod 13), and by x ↦ ax+b…"

If "unchanged" means every set keeps its colour, each colour class is a union of Z₁₃-orbits of size 13, and 33 is not a multiple of 13. What `cyc39.py` and `frob39.py` actually search for are colourings whose colour **classes are permuted** by the group.

**Fix:** "colourings whose 39 colour classes are permuted among themselves by x ↦ x+1 (mod 13), and by the 39 maps x ↦ ax+b with a ∈ {1,3,9}".

**S8. "Nothing at 38 or above" collides with Davies and with the submission.**

> "We found nothing at 38 or above stated in print."

The next bullet quotes Davies at 2,516, and the submission itself states 38 and 39.

**Fix:** "Before this submission we found no bound of 38 or more from an explicit graph stated in print."

**S9. The Lemma leaves "linked classes" undefined, and the proof sketch is incomplete for blocks.**

- **Undefined term.** "Linked" is not transitive, so "linked classes" needs a definition: the connected pieces of the linking relation.
- **Gap in the proof.** "The same argument stops a block from leaving its 6-set" is the one step that is not the same argument. It also needs the class to have ≥ 3 members in the 6-set; two-member classes are both kinds.
- **Unstated role.** Say the lemma only names the family's shape and is not used in the computation.

**Suggested complete proof (the same length class):**

Proof. Let A = K+a and B = K+b be linked. Suppose a member C is linked to B but does not contain K. Then C contains b and three points of K, and if a ∉ C it meets A in exactly 3. So C = K−k+a+b, and A, B, C lie in the 6-set D = K+a+b.

Now let three members of a class lie in a 6-set D, and let E ⊄ D be linked to one of them, D−x. Then E = D−x−y+e, and every other member D−z inside D meets E in exactly 3 points unless z = y. So at most two members lie in D, a contradiction.

Hence if two linked pairs in a class have different cores, the class sits inside one 6-set: a block. Otherwise, by connectedness, every member contains one core: a sunflower. Members of different classes are not linked, cannot share 3, and are distinct, so they share at most 2. □

I verified the lemma by brute force: 0 counterexamples. Details are in `(the blind reader's scratch, not bundled)/lemma.py`.

**S10. The jargon has no glosses.**

A number theorist will stumble on these terms:
- "orbital branching"
- "clique problems": cliques of what? The graph is the complement of J, where independent sets of J are cliques.
- "threshold"
- "forced sets"
- "infeasible"

**Fix:** add one gloss in the referee-pass intro: "Independent sets of J are cliques in its complement. Orbital branching splits the search on whether a chosen set is in the family; when it is out, every set that a symmetry of the current subproblem maps it to is dropped too. Sets already put in are 'forced', and a leaf's threshold is how many more are needed."

**S11. The email's leaf-count comparison is misleading.**

> "Did you try fixing a pair sharing 4 elements instead of a single vertex? In our runs it brought the tree down to about a hundred leaves."

His tree has 200 leaves **by its stopping rule** ("until the tree has 200 leaves"), so leaf count is not what the pair changes. What it changes is the root: 851 candidates at threshold 32 instead of 1,006 at threshold 33. A fair cost comparison exists: our solver took 71 s × 10 cores on our 105 leaves, about 0.7 CPU-hours at most, against 3,184 CPU s on his 200.

**Fix:** reword around the root and the time. Or ask him something he'd enjoy more: did his DSATUR runs ever get the whole graph near 39 colours, now that Q5.1 is "39 disjoint copies of one family"?

**S12. The referee report would ship garbled.**

`referee_indep.md` has spliced and duplicated text, for example "Results are in ## Differential test of clq2 (finding 4)" followed by a copied section and "…these numbers. below.". It also cites `/tmp/ref704` paths that readers won't have.

**Fix:** clean the report and repoint its paths to the bundle before bundling it, since the email says "both referee reports are in the bundle".

**S13. The problem's classical name is missing.**

α(J(13,5,3)) is m(13,5,3) in the Frankl–Füredi "forbidding one intersection" notation (world_seat §3). One clause in "The value itself" helps combinatorialists and makes the literature search look complete.

### NIT

**N1. The colour list order matches no ordering of the leaves.**

> "(17, 26, 30, 29 and 30 colours)"

By leaf id (16, 169, 170, 173, 176) it is 17, 30, 26, 29, 30. **Fix:** "17 to 30 colours, each below its leaf's threshold".

**N2. The edit history refers to an unpublished draft.**

> "The page had said 'no decomposition in common'; it now says…"

Readers never saw that. **Fix:** "Our draft had said…", or drop the clause.

**N3. The email's 286/10 should be an integer.**

> "has at most 286/10 members"

**Fix:** "at most 28 members (286 triples, 10 in each set)".

**N4. Davies "proves".**

> "James Davies (… not yet refereed) proves that…"

Consider "gives a proof that…". The hedge is present, but "proves" asserts correctness.

**N5. The card tag's attribution is ambiguous.**

"…α(J(13,5,3)) = 33, VeriPB-CERTIFIED · RE-DERIVED HERE…" could read as if we certified it. **Fix:** "CERTIFIED BY HIS VeriPB LOGS".

**N6. The status badge.**

Status "partial" renders PARTIAL next to "#704", while the page says the result does not touch #704's questions. This is the house convention (compare 789), so this is optional. A one-line "partial = a verified piece, not progress on the growth question" would remove the tension.

**N7. Optional context from world_seat §2e.**

Exoo–Ismailescu's 46 had resisted reproduction: Parts ran mcqd for over a month, and Voronov estimated years. That makes the submission's uncertified reproduction of 46 a small piece of news in itself.

**N8. "3,184 CPU seconds" is a sum of wall times.**

It is the sum of per-leaf wall times of single-threaded processes. That is fine, but it is wall-seconds.

**N9. Email warmth.**

- The email has no specific compliment. The release's certified/uncertified discipline, encoding checker and claim-to-file map are unusually careful, and saying so is true and warm.
- Consider one clause saying who "Claude" is: the AI that writes the site with Patrick. He used Claude Code himself, so this is courtesy, not disclosure.

**N10. The Labels line sits between "Where it stands" and the referee pass.**

It is unclear which claims (a) and (d) attach to. The inline tags make this mostly moot.

## Overclaim sweep (item 4 of the brief)

| Possible overclaim | Status |
|---|---|
| A record for χ(ℝ¹²) overall | Correctly qualified everywhere: "from a finite graph anyone has exhibited", "not a record … if Davies's preprint stands". |
| Davies right or wrong | Neutral apart from N4. |
| That we re-ran VeriPB | Explicitly denied, correctly. |
| That our decomposition is independent of the paper's technique | Correct on the page ("same technique"). Contradicted by the `tree.py` and `ESTIMATE.md` text that ships (M2). Overstated by "three different decompositions" (S3). |
| That the result addresses Erdős's question | Disclaimed twice. Only the PARTIAL badge pulls the other way (N6). |
