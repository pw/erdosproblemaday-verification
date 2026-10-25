VERDICT: SHIP AFTER FIXES — every number on the page checks against the files and my own exact arithmetic. Five sentence-level defects must be fixed before shipping: a checking claim inflated from two seats to four (title, HEADLINES card, summary, "What is ours"); a false statement that Chen's checker is not in his release; an exponent rule (η = 2/κ) that contradicts the page's own η = 2/(ρ+2); priority stated as fact; and a supremum that the page's own 2/50,395,460 exceeds.

Seat B, blind reader. I read page.txt cold first and listed every sentence I would challenge. Then I checked each one against the bundle (README, the four seat reports, lean-replay/, packing/, compute/, live/, sources/), Blinov's checkout, Chen's PDF/text (pp. 1–10 read in full), OpenAI's TeX §§1–9, and the BOS snapshot. I recomputed with Python Fractions: k = C(C(163,41),3)²+1 has 232 digits, and OpenAI's η = 3.1757·10⁻²³⁶. I also recomputed 249k+5 = 101,786,474 = 2·50,893,237; Chen's ratio 1.00912; s0 ≤ 136,259 ⇒ 2/100,560,143 = 2/(246k+17); u and X at all three k; 2/74,806,940, 2/50,395,469, 2/50,395,460 and 1/34,285,435; 183k+8 = 50,395,463; C(2921,2)+2921 = 4,267,581; the counts 5/2921; max 204,390; and 163·1092+81 = 178,077. All of these match the page.

I used no third-party script. Chen's attached ZIP was listed and READ as text (unzip -l / unzip -p). It was not executed.

## MUST-FIX

**1. "Four AI seats" for a verdict that two seats gave.** Seat W's report says "Scope: world, priority and prior art only, not the mathematics." Seat S's report says it did not check the drafts' algebra or carry bound: "I relied on Blinov's text and Lean statements for these". Only P and G returned HOLDS AS READ on the drafts, as the body itself says: "P and G found no gap". Five places claim more.

- Title: "…hold as read by four AI seats, and the same argument gives η = 2/50,395,469 ≈ 3.97·10⁻⁸ (ours, under the same conditions)"
  → "…hold as read by two AI referee seats (four seats in all), and the same argument gives η = 2/50,395,469 ≈ 3.97·10⁻⁸ (ours, under the same conditions, read by one further seat)"
- HEADLINES tag: "HOLD AS READ BY FOUR AI SEATS"
  → "HOLD AS READ BY TWO AI REFEREE SEATS"
- HEADLINES line: "four seats found no gap."
  → "two referee seats found no gap."
- Summary (and the page's meta description): "Four seats read them, each briefed to refute: the algebra (a new determinant decomposition, checked symbolically and end to end in two finite fields), a new collision lemma (exact toy enumerations, tight, with controls that fail), the transfer of OpenAI's geometry to the new parameters, and the world. Both hold as read, with notes."
  The list names four topics as if they were four seats. Algebra and lemma were both P, S is missing, and the decomposition is CGLV's, not new.
  → "Four seats were briefed to refute. P took the algebra (Blinov's use of Conner–Gesmundo–Landsberg–Ventura's 18-term determinant decomposition, checked symbolically and end to end in two finite fields) and the new collision lemma (exact toy enumerations, tight, with controls that fail). G took the transfer of OpenAI's geometry to the new parameters, W the world and credits, and S our own additions. P and G find that both drafts hold as read, with notes."
- "What is ours": "Ours: the first independent reading of both drafts (four seats; …"
  → see finding 4 for the full replacement.

**2. Chen's checker IS in his public release; the page says it is not.** Page (notes): "Chen's §2.1 cites "the packet's checker", which is not in his public release (an attached ZIP was not opened)."

The sentence contradicts itself: the ZIP it mentions is the release. `pdfdetach -list chen191.pdf` shows `mathematical-supplement.zip`. Chen's last page says "The exact arithmetic programs are included in the attached mathematical supplement (ZIP)." I listed it: it holds one file, `checkers/check_exact_inputs.py`, dated 2026-10-18. I read it as text and did not run it.

- It implements exactly the multiplication his §2.1 describes, `(a0*b0 − a1*b1, a0*b1 + a1*b0 + a1*b1)`.
- Its 18-form table matches the PDF's.
- It asserts that the actual coefficients equal `3·sign(a)·sign(b)` on permutation pairs.
- It also checks the packing and the scale arithmetic.

P's finding 4, which the page inherited, is wrong. It looked only at the repository directory.

Replacement: "Chen's §2.1 cites "the packet's checker". It is not a file in his repository. It ships inside the PDF, as the attachment mathematical-supplement.zip (one file, checkers/check_exact_inputs.py), which implements the 486-term expansion his text describes. We did not run it."

Fix the bundle README's "Not checked: Chen's attached ZIP supplement" line to match. For your information: the script's own scale check carries the scope line "Exact arithmetic only; full construction and all-n transfer unproved."

**3. The stated exponent rule contradicts the stated exponent.** Page: "So n_r²·Δ ≈ r², and if n_r ≈ r^κ the gain is η = 2/κ." Later: "the deletion closes with r^γ in place of r … That gives κ = ρ + γ and η = 2/(ρ+2)."

With η = 2/κ and κ = ρ+γ, γ = ρ/(ρ+1), you get 2(ρ+1)/(ρ(ρ+2)), not 2/(ρ+2). The right rule once r becomes r^γ is n_r²Δ ≈ r^{2γ}, so η = 2γ/κ. That is what G's arith.py and Chen's (9) use ("2γ/α = 2/(ρ+2)"). The same gap appears in "Ours": "n_r ≍ r^{γ+X} … with γ = X/(X+1), η = 2/(X+2)". A reader applying η = 2/κ gets 2/(X+γ).

Replacements:
- "So n_r²·Δ ≈ r², and if n_r ≈ r^κ the gain is η = 2/κ (η = 2γ/κ when, as below, the deletion only closes with r^γ in place of r, so that n_r²·Δ ≈ r^{2γ})."
- "That gives κ = ρ + γ and η = 2γ/κ = 2/(ρ+2)."
- "So n_r ≍ r^{γ+X} with X = 60k + 9u + 3, and with γ = X/(X+1), η = 2γ/(γ+X) = 2/(X+2)."

**4. Priority stated as fact.** Seat W reports that it found no check, and it lists places it could not read: X, Reddit, the BOS Discord, the Lean Zulip archive (searched by web only), Mathstodon full text, and Chinese-language forums. The page turns that absence into fact in four places.

- HEADLINES tag: "THE FIRST CHECK OF EITHER"
  → "THE FIRST CHECK OF EITHER THAT WE COULD FIND"
- Body: "Nobody else has checked either one (see "The world", below)."
  → "We found no one else who has checked either one (see "The world", below, which also lists what we could not read)."
- Summary: "and nobody had checked either"
  → "and we found no one who had checked either"
- "What is ours": "Ours: the first independent reading of both drafts (four seats; the 18-term identity checked symbolically; the full norm decomposition checked in two real finite fields; the packing and the fresh-digit lemma checked by exhaustive enumeration, with controls that fail);"
  → "Ours: an independent reading of both drafts, the first we could find (two referee seats, P and G; the 18-term identity checked symbolically; the full norm decomposition checked in two real finite fields; the packing checked exhaustively at the real parameters; the fresh-digit lemma read line by line and tested on exhaustively enumerated toy models, with controls that fail);"
  This also fixes the "four seats" count from finding 1. It also fixes the overclaim that the fresh-digit lemma was "checked by exhaustive enumeration": only toy models with k ≤ 8 and B ≤ 600011 were enumerated, per P item 4.

**5. The page's own improvement exceeds the "supremum" it states for the same bound.** Page: "S also found a rigorous extra factor r⁻⁵ in step 1 (proportional points force equal labels), which gives 2/50,395,460. We state the round version. With these two estimates (step 1's pair bound and the printed triple bound) the supremum is 2/(183k+8), not attained."

At k = 275,385, 183k+8 = 50,395,463. So the 2/50,395,460 just announced is larger than the "supremum", and the r⁻⁵ factor is part of step 1's pair bound once adopted. S's report gives the sup with that factor as 2/(183k+3); I re-derived it: X > 183k+1+γ, so η < 2γ/(183k+1+2γ) → 2/(183k+3). "Round version" is also unclear.

Replacement: "S also found a rigorous extra factor r⁻⁵ in step 1 (proportional points force equal labels), which gives 2/50,395,460. We state the version without it. With step 1's pair bound as stated above (without that factor) and the printed triple bound, the supremum over boxes and γ is 2/(183k+8) = 2/50,395,463 at this k, not attained; with the extra factor it is 2/(183k+3) = 2/50,395,458."

## SHOULD-FIX

**6. Lean replay: "from source" and "--trust=0".** Page: "We compiled the 48-module import closure … from source. We used Lean 4.11.0 and Mathlib 20c73142, his pins. … #print axioms under --trust=0 gives…"

`lean-replay/cache.sh` runs `lake exe cache get`, so Mathlib's oleans are the published cache, not rebuilt. `drive.py` compiles only Blinov's 48 modules. The bundle has no command line showing `--trust=0`: probe.out has none, and only the README asserts it. In any case `--trust=0` does not re-check cached Mathlib oleans.

Replacement: "We compiled, from his source, the 48 modules of his that the theorems his review guide cites import (…), against Mathlib 20c73142's published build cache (Mathlib itself was not rebuilt). Lean 4.11.0 and Mathlib 20c73142 are his pins. … #print axioms gives…"

Alternatively, bank the exact probe command and keep the flag. The claims "48 of 48, 0 errors", "16 of 17 standard axioms" and "gain_from_five none" all check against steps.tsv, the logs and probe.out. My own grep of all 99 files in lean/ for sorry, admit, axiom, native_decide, implemented_by, unsafe, #eval, run_cmd, macro and IO also finds nothing. The bundle should carry that scan too, because the page states it as done.

**7. "I rebuilt it again" is not in the bundle.** Page: "Seat W rebuilt it from that description and I rebuilt it again; the two agree element for element."

The bundle has W's rebuild (`W_work/ap3_check.py`, `witness_2921_in_1_137693.txt`). `packing/wroblewski2921.txt` is that witness minus 1; I checked, and they are equal. The second independent rebuild in the bundle is seat S's `wrob_recon.py`. There is no coordinator rebuild script.

Replacement: "Seat W rebuilt it from that description, and seat S rebuilt it again from his recipe (the 216th roots mod 3889 under x ↦ 1331x + 640, in 14 blocks); the two agree element for element." Alternatively, bank your own script.

**8. Chen's paper is understated.** Page: "Neither draft has a human referee, and neither is a self-contained paper. Blinov's is a patch to OpenAI's paper. Chen's rests on Blinov's checkpoint for the algebra and the collision lemma."

Chen's §2 restates the norm decomposition, the packing, the Smith tails and the fresh-digit argument. §§3–4 prove the lattice, orbit, cap, zero-count, deletion and transfer estimates with explicit constants. His only outside theorems are CGLV and BMOR. His p.1 "supplies" sentence is attribution, not a deferral of proof. The page's own Chen bullet says he "reproves the geometric estimates".

Replacement: "Neither draft has a human referee. Blinov's is not a self-contained paper: it is a patch to OpenAI's. Chen's is a 12-page paper that credits Blinov's checkpoint for the algebra and the collision lemma and restates their proofs in compressed form (its §2), and proves the geometric estimates afresh with explicit constants (§§3–4)."

**9. Wróblewski is missing from the "not a new method" credit line.** Page: "It is not a new method: every idea except step 1 is Blinov's or Chen's, and step 1 is a short observation about OpenAI's lemma in their setting."

Step 2's set is Wróblewski's, and the construction is OpenAI's.

Replacement: "It is not a new method: the construction is OpenAI's, every other step except step 1 is Blinov's or Chen's, the set in step 2 is Wróblewski's, and step 1 is a short observation about OpenAI's lemma in their setting."

**10. The BMOR input is described as "exactly" Chen's bound.** Page: "Theorem 1.2 with c0(3) = 1/840 and x0 = 8·10⁹ gives exactly the bound he uses."

Chen's (B1) uses 1/160 and says "For m = 3 the displayed bound is weaker than the source's 1/840 bound." G's report says the same.

Replacement: "Theorem 1.2 with (1.10)–(1.11) gives, at q = 3 and x ≥ 8·10⁹, the constant 1/840, which implies the weaker 1/160 he uses, as he notes."

**11. The HEADLINES card omits the smaller box, and "again" misleads.** Tag: "WITH A SHARPER PAIR BOUND AND WRÓBLEWSKI'S PROGRESSION-FREE SET, GIVES η = 2/50,395,469". Line: "A sharper bound for coinciding points and a better progression-free set for the digit positions double it again."

Step 1 acts only through the smaller box (step 3). Without it, step 2 alone gives 1/34,285,435. The drafts did not "double" OpenAI's exponent, so "again" is wrong.

- Tag → "WITH A SHARPER PAIR BOUND, WRÓBLEWSKI'S PROGRESSION-FREE SET AND A SMALLER BOX, GIVES η = 2/50,395,469"
- Line → "A sharper bound for coinciding points, a better progression-free set for the digit positions and a smaller box double it."

## NIT

12. "The other uses a base above 100k²P": P is never defined on the page. → "The other uses a base B above 100k²P, with P = L₁L₂L₃ = 400k²r⁶ as the lemma requires,"

13. "One uses small bases with tags, label-dependent residues and three choices of third-row residues": this reads as M = 3. → "…and three regimes for the third-row residues (label-dependent, all zero, shared)"

14. "Moving one tag (to 0, 1, 3, 4, 8) creates a spurious triple." → "Moving one tag (tags 0, 1, 3, 4, 8 in place of 0, 1, 3, 4, 9) creates a spurious triple, (12, 8, 408,760)."

15. "Dropping a node agrees only at chance level (1/20)" → "Dropping a node agrees on 1 of 20 inputs, chance level (about 1/r)"

16. "B ≈ r^(power) is the digit base" reads like an unfilled placeholder. → "B, a fixed power of r up to constants, is the digit base"

17. "a 'slab' cap, {(x, y, x²−νy²) : 0 ≤ x < w}, in place of OpenAI's cube {0..w−1}³": OpenAI's cap is the part of a translate of Γ inside the cube, not the cube itself. Blinov's H = 2h (OpenAI: H = h²) is also part of what allows q ≈ h⁶. → "…in place of OpenAI's cap cut out by the cube {0..w−1}³, together with H = 2h in place of OpenAI's H = h²."

18. "Wróblewski's table of non-averaging sets lists a 2,921-element one inside [1, 137,693]": the table lists the bound, not the set. → "Wróblewski's table of non-averaging sets gives a(2921) ≤ 137,693, i.e. a 2,921-element 3-AP-free set inside [1, 137,693]."

19. "Then 3·det A·det C = Σ Π h_t reduces to zero over ℤ[u]/(u²−u+1)" → "Then Σ Π h_t − 3·det A·det C reduces to zero in ℤ[u]/(u²−u+1)"

20. Note on one-line notation: "…which fixes the reading, but neither says so." Chen's §2.1 does say it: "satisfying a_j = p(b_j) for all j". → "Blinov's patch does not say so; Chen's coefficient rule (a_j = p(b_j)) does."

21. "The tag argument needs three more things … The five tags are its five smallest elements. All five lie below the first norm word T." The third condition follows from the second, since T is the sixth element. → "…The five tags are its five smallest elements, so all five lie below the first norm word T."

Checked and fine, so the panel need not re-flag them:

- The threshold rendering ("2^{100866718·2^50}" vs BOS's "2^{100866718·250}") is correct in the HTML; only the .txt render flattens it.
- BOS quote, nine rows, "Data updated Oct 22, 1:17 PM PT".
- PR #13 / e29a291 / 15 Oct; main at 1/145,278,430; 13 PRs with no comments.
- Chen's c, N0, s0 = (k−1)/4, the 0.9% gap.
- G's 8000²h⁶/q, 8000h⁴/q, 8000²h⁶/q²; β = (83k+1)/2.
- CGLV Theorem 4.1 (v2) / 2.11 (v1), ℂ, ϑ = e^{2πi/6}.
- Erdős–Turán p. 263 footnote; slab cap first in a84a29b on 8 Oct.
- Appendix A is OpenAI's prime-interval appendix; the patch moves r to PNT mod 3 while B, q keep Bertrand, so the stale-sentence note is right.
- The 7/6 upper exponent appears in OpenAI's §1.
- r^{63k} = M^k·s ≈ r^{3k}·r^{60k}; the pair-term exponent 20.5k+0.5−1.5u; 3u ≥ 41k+2 is the exact integer condition.
- The r₃ table gives 23 as optimal in [0,81] (82 → 23, 84 → 24).
- Model receipts: claude-opus-5-5 for all four seats.
