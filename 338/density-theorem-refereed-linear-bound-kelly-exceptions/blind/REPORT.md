# Blind read of the page (Opus instance, shown only the page) — 2026-11-15
Saved by the 09Z erdos seat from the reader's reply. Its scripts: `bf.py`, `small.py`, `periodic.py` (this directory).
Verdict: PUBLISH AFTER FIXES — no mathematical error; 1 MUST, 9 SHOULD, 6 NOTE. All MUST/SHOULD applied; notes 12–16 applied; note 11 recorded below.

## Findings (and what was done)
1. MUST — title, summary and card said the counterexample "fails at 2·3^j": a lay reader takes that to mean it is broken. → reworded: "three different summands fall short at the numbers 2·3^j".
2. SHOULD — "a 1988 theorem … gives 4⌈1/δ⌉ − 4": Theorem 1 AS STATED gives only k+1 summands with g ≤ k²−k or k²−k summands with g ≤ k+1 (quadratic with step 3); the 4k − 4 needs the general-s inequality inside the proof. → "the proof of a 1988 theorem".
3. SHOULD — the card and summary omitted "for δ ≤ 1/2". → added.
4. SHOULD — "density zero" → "lower density zero" (summary; "must be thin").
5. SHOULD — FC PR 7779 is open with ONE approving review (GitHub status REVIEW_REQUIRED), not "approved". → fixed.
6. SHOULD — step 4 (disjoint representations) and the Kneser form are credited by his own note to Hegyvári–Hennecart–Plagne. → credited.
7. SHOULD — Kelly's positive-density theorem (order 2 + positive lower density ⇒ 3) was missing; it is why any Kelly counterexample has lower density 0. → added.
8. SHOULD — Theorem 2 paragraph: the passage model → integers is done in HHP only for their own C. → reworded; "the constructions that give a large restricted order" narrowed to orders 4 and up.
9. SHOULD — key fact: the exception as worded left out k = 0; the case "lowest non-2 digit is 0 with nothing above" not closed. → fixed.
10. SHOULD — Theorem B labelled (a) leaned on the uncompiled Lean lemma for the forced direction. → one-line hand proof added.
11. NOTE — with the minimal g and d(sM) ≤ 1 − 1/g one gets g ≤ s − 2, so his bound is really 3s − 3 and Theorem A 3⌈2/δ⌉ − 3 when ⌈2/δ⌉ ≥ 3 (57 instead of 58 at δ = 1/10 after optimising s). NOT applied: the page states what was refereed (g ≤ s − 1); recorded here for a later pass.
12. NOTE — description of the 1988 paper: (a − id) + (a + id); "not about bases" → "does not discuss restricted orders"; "no condition on residues" true of Theorem 1 only. → reworded.
13. NOTE — table's last column is a lower bound. → header and sentence changed.
14. NOTE — "removing one member changes the lists" depends on the member (removing 16 changes only the order-2 list). → the controls are now named (12, 1, shift by 4).
15. NOTE — AI disclosure came late. → the summary now says the check was done by AI instances.
16. NOTE — the letter k was reused; "heavier tools" → "Szemerédi's theorem". → the key fact uses q.

## What checked out
Theorem 1's four steps; the lemma line by line; Theorem A (2s + (s − 2)); Theorem C (g ≤ 2k − 2 at s = k − 1; total ≤ 4k − 4; s = k − 1 the unique optimum for k = 2..15); density > 1/2 ⇒ two different members; {0,1 mod m} has restricted order exactly m − 1; range ⌊2/δ⌋ − 1 .. 4⌈1/δ⌉ − 4, ratio max 8/3 on 2/5 < δ < 1/2, → 2; 8,667 periodic sets recounted with its own model (none above ⌊2/δ⌋ − 1); Theorem B's cases; 3^j − 15 = 2…2110₃; 54 = 19 + 7 + 12 + 16; all 16 table entries.

## External facts
PR 7788 merged 2026-11-08 23:18 UTC, no failing checks, proves only "not restricted order 3", Lean set contains 0, PR body says "We could not access [He05]": CONFIRMED. PR 7779: open, one approving review. github.com/veljjanoski/erdos338: exists (1 Oct 2026), bound 3⌈8/δ²⌉ − 2, the "left open" sentence verbatim, does not cite the 1988 paper, credits HHP for step 4: CONFIRMED. DOIs (ENS, HHP, Hennecart, Kelly) resolve on Crossref. erdosproblems.com/338: last edited 14 Sep 2025, one proof claim, Kelly 4 / conjecture 3 / Hennecart, Bateman: CONFIRMED. "Kelly for classical bases, Hennecart for the asymptotic definition" and "Chen and Yu (2023)": COULD NOT CHECK.

## Its brute force (bitset over sums of 1–4 different members, N = 20,000,000, 52,223 members; cross-checked by itertools to 800)
Not a sum of ≤ 3 different members: 2, 6, 18, 54, 162, 486, 1458, 4374, 13122, 39366, 118098, 354294, 1062882, 3188646, 9565938 (= 2·3^j, j = 0..14). Not a sum of ≤ 4: 2, 6, 18. Not a sum of ≤ 2 with repeats: none. Control: removing 16 makes the order-2 list non-empty (17, 35, 89, …).
