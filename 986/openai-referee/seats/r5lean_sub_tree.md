# Sub-seat r5lean_sub_tree: paper compression-tree.tex vs Lean (fresh test, pivot tree, retention, stage output)

Lean read as TEXT only. Paths relative to /tmp/oaimath/170/repo/lean/OAI/Combinatorics/RamseyFive/ ; paper = preprints/.../build/compression-tree.tex (CT) and compression-local.tex (CL).

## 1. lem:fresh-test (CT:24-118)

### 1a. The test set — SAME threshold .2h/q
- `Decoding/ReverseCap.lean:14-15` `cap R U q row := U.filter fun a => hits (neighbors R a) row < n/(5q)` = paper eq:fresh-test-set {y : Σ 1[x_j ⊥ y] < .2h/q} (n = row length h). The AMBIENT version is `cap R Finset.univ q row` (`Entropy/FreshPublicFamily.lean:43-45 freshDecoded`; `Probability/AmbientPublicTest.lean:11-15 ambientCapLaw`), and `cap_inter` (AmbientPublicTest.lean:17) shows U ∩ ambient = cap R U. This is the paper's "ambient" wording (CT:19-20) made literal.

### 1b. Acceptance event and proposal mechanism — SAME
- `Decoding/FreshValidation.lean:91-94 validationRows R S U C n q M` = rows with every entry in the hidden source C, |cap R U q row| ≤ M and .9|S| ≤ |S ∩ cap|. = paper CT:91-95 "accepting precisely when every entry lies in A∩W and both requirements hold".
- Proposal tape: `FreshPublicFamily.lean:30-41` `cardCutoff q m w n = ⌈q/(.9 (m/w)^n)⌉`, `FreshTape W n q := (m : Fin (|W|+1)) → Fin (cardCutoff q m |W| n) → Fin n → B`, `freshTapeLaw` = product of iid-uniform-on-W rows, one block per possible source size m. The encoder (`freshEncoded`, l.47-52) uses block m = |C| and sends `⟨m, accepted index⟩`. So the decoder learns |C| from the message, and the tape is fixed before C is known (public, independent of hidden data). Paper: "Stop after ⌈e^{C'hP}⌉ proposals" (CT:99). Lean's cutoff is ADAPTIVE to the true ratio (|W|/|C|)^n·q/.9 rather than a uniform e^{C'hP}; cost `fresh_payload_cost` (l.82-90): log #indices ≤ log(2q) − log .9 + n log(|W|/|C|). Under the paper's |W|/|C| ≤ e^{CP} this is O(q + hP) — same as paper's O(hP) (plus log 2q, harmless). STRUCTURALLY slightly different (index range depends on source size, the size is part of the message), same strength.
- Failure: `publicCapLaw_failure` (Probability/PublicCapLaw.lean:44-53): P(no accepted row) ≤ e^{−q}, from hE : .9 ≤ P_{iid C}(validationRows). = paper O(e^{−q}).
