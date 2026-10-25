SUBSTANTIVE: 13 · MINOR: 21

Seat D (blind consistency), 2026-10-13. Read: entry/rendered.txt + rendered.html (incl. meta/og description = `summary`),
rendered_home.html (#778 card, = `HEADLINES[0]` in src/index.js), the whole bundle, live captures, MathDyad logs.
Placeholders ⟨SEAT_C_SHORT⟩ / ⟨VERDICT_DP⟩ ignored. Quotes are from rendered.txt line numbers (L) or src/index.js.

## SUBSTANTIVE

S1. Title (L2/L7, <title>, og:title): "exact, certified, three instruments"
- Evidence: the body's own "third opinion" is Cambie–Provoost's solver, which "contributes nothing here" (L65). README calls
  it "Third instrument … ATTEMPTED, NO RESULT". The instruments that actually agree are two engines plus one checker.
  The homepage tag already says "TWO ENGINES".
- Replace: "exact, certified, two engines". Or keep "three" and name them in the body: "Three instruments agree: our
  engine, the nauty checker and the July engine."

S2. Summary / meta description / og:description: "We refereed it (three hostile Opus seats, …)". Homepage card:
"holds as read under three hostile seats"
- Evidence: one seat was hostile. The body (L36–44) says a hostile referee, a Lean seat and a judgment seat. Seat B's
  brief was a statement audit.
- Replace (summary): "We refereed it with three Opus seats (a hostile referee who re-derived every step and ran an
  exact-arithmetic instrument over 2,444 games with zero violations, a Lean seat that matched the formal statement to the
  literal game, and a judgment seat) and kernel-replayed the Lean on our box: standard axioms."
- Replace (card): "holds as read under three Opus seats (one hostile) and kernel-replays green here."

S3. Homepage card: "accepted by an independent nauty-based checker that rejects every mutation"
- Evidence: controls.txt mut2 (one swapped reply) is ACCEPT, and the body says so (L63–64).
- Replace: "accepted by an independent nauty-based checker that rejects deleted, flipped, fabricated and mass-swapped
  certificates".

S4. L49–50: "What it leaves open is every n from 8 to 3^158 − 1"
- Evidence: L69 says "the finite gap 9 ≤ n < 3^158", the card says "Everything from 9 to 3^158 − 1 is still open", and
  README says "n = 8 is now closed". The page contradicts itself.
- Replace: "What it leaves open, after the July table (n ≤ 7) and today's n = 8 below, is every n from 9 to 3^158 − 1, the
  unbiased game (Erdős's own conjecture) and the degree game."

S5. L18–19: "Bob simply keeps Alice's graph triangle-free, and then α(R) ≥ 3 > 2 by R(3,3) ≤ 6"
- Evidence: R(3,3) = 6 says nothing on 4 or 5 vertices; C₅ is triangle-free with α = 2. The July report proves n = 4, 5 by
  separate explicit arguments: P₃ plus an isolated vertex, and "a triangle-free 4-edge graph on 5 vertices has α ≥ 3".
  R(3,3) is used only for n = 6, 7 (july-report §"Exact computation", "on at least six vertices"). A combinatorialist sees
  this in one line.
- Replace: "for 4 ≤ n ≤ 7 Bob can keep Alice's graph triangle-free, and then α(R) ≥ 3 > 2 (by R(3,3) = 6 at n = 6, 7, and by
  a direct check of her two and four edges at n = 4, 5)".

S6. L24–25: "On 14 August they added a Lean 4 formalization … The one commenter, StijnC, proofread it and confirmed."
- Evidence: proof-claim-193-comments capture.
  - StijnC's confirmation is dated 08:16, 7 Aug 2026: "I have (proof)read the paper, confirming correctness". That is a
    week BEFORE the Lean existed. "it" right after the Lean sentence reads as if he checked the Lean.
  - He is not the only commenter: maximdidin posted 3 of the 6 comments.
- Replace: drop the sentence there, and after "…for all sufficiently large n." insert: "StijnC, the only commenter on the
  claim besides Didin, proofread the paper and wrote on 7 August 'I have (proof)read the paper, confirming correctness';
  nobody on the thread reports checking the Lean."

S7. L59–61: "… and demands α(R) > ω(R) at every terminal position: ACCEPT — 122,288 Alice-to-move positions walked,
57,512 branches closed by the checker's own re-derived cutoff …"
- Evidence: check_n8_clique.log says "0 terminal leaves". At n = 8 the full-board test never fires: every one of the 57,512
  leaves is a Bob-cutoff leaf, so the n = 8 verdict rests entirely on check778.py `bob_cutoff`.
  - That cutoff is sound. It is ω(B) > the largest S with no blue edge and ≤ kA non-red edges. Blue cliques persist, and a
    final red clique has no blue edge and needs ≤ kA more red edges.
  - The page should say this rather than imply terminal checks happened. The terminal path is exercised only by the n = 6
    and 7 controls (3 and 24 terminal leaves).
- Replace: "… and closes a branch only at a full board (where it demands α(R) > ω(R)) or by its own re-derived Bob cutoff:
  ACCEPT — 122,288 Alice-to-move positions walked. At n = 8 no branch reaches a full board. All 57,512 leaves close by the
  cutoff (Bob's current clique already exceeds the largest red clique Alice can still complete with her remaining edges),
  so the n = 8 verdict rests on that two-line cutoff. The full-board test is exercised by the n = 6 and 7 controls (3 and 24
  terminal leaves). Every transported reply was free."

S8. L45–46: "Our own kernel replay: … lake build 959 jobs with no errors, lean --trust=0 on the root file, …"
- Evidence: the root file is `Erdos12.lean`. It holds three `import` lines and a doc comment, with no declarations.
  - steps.tsv shows trust0 took 5 s, which is far too short to re-check imported Mathlib.
  - So `--trust=0` re-checked nothing. Listing it as part of the replay is a green that could not have been red.
  - The real kernel check is that lake build compiled the 15 project files from source here (build.log.tail: "Built
    Erdos12.Main" etc.).
- Replace: "Our own kernel replay: Lean v4.24.0 and Mathlib at the claim's pinned commit f897ebcf (oleans from the community
  cache). `lake build` compiled the 15 project files from source here, 959 jobs with no errors, so every declaration of the
  formalization passed the kernel on our box. `#print axioms …` → [propext, Classical.choice, Quot.sound]; … The v4.24.0
  toolchain ships no leanchecker, so the cached Mathlib oleans are trusted as downloaded (`lean --trust=0` on the root file
  adds nothing: that file only imports the others)."

S9. L42–43: "the comparison ω_B ≤ 2k+3 < 2k+4 ≤ ω_C"
- Evidence: in seat B, B = Bella (Alice) and C = Chingiz (Bob). On this page Bob is blue, and "Bella" is never introduced
  as Alice, so ω_B reads as Bob's clique number and the inequality reads backwards. k is also undefined on the page.
- Replace: "the comparison ω(R) ≤ 2k+3 < 2k+4 ≤ α(R) with k = ⌊log₃ n⌋ (Alice's clique number against Bob's), resting on …"

S10. L32–33: "… below 1 by less than one percent, so ℓ must be about 230 log n and the threshold is astronomical."
- Evidence:
  - θ = 0.990335 and η = 0.009712. The paper needs ℓ = ⌈C log n⌉ with Cη > 2, i.e. C > 205.92 (seat A).
  - About 228 is the Lean's own choice, 250·log₃ n = 227.6 ln n, not a requirement.
  - Seat A also names the binding constraint for the threshold as the final clique comparison. The margin
    (1/log(5/3) − 2/log 3) log n = 0.137 log n must beat log_{5/3} ℓ. "The loss is in θ" is only half of that.
- Replace: "… which is below 1 by less than one percent (η = −log θ ≈ 0.0097). So ℓ = ⌈C log n⌉ needs C > 2/η ≈ 206 (the
  Lean takes 250 log₃ n ≈ 228 log n), and the clique comparison has only about 0.137 log n to spend against log_{5/3} ℓ.
  That is why the threshold is astronomical: about 10^67.7 with the paper's constants, 3^158 ≈ 2.4·10^75 in the Lean."

S11. Summary / meta description: "and reproduced by the same engine with reversed move ordering and with its cutoffs
disabled. At n = 8 the triangle-avoidance route that carried n ≤ 7 breaks — Alice wins the (1:2) triangle game on K₈ — so
this is the first value …"
- Evidence: the summary reads as written before results landed.
  - (a) It omits the July engine, the only decorrelated re-derivation (old_clique_n8.log: Bob, 547,700 states,
    2,490.7 s). The body and the card both cite it.
  - (b) It states the triangle result without the hedge the body carries (L56: "from one engine so far").
    - The only record is the certificate header, written after solve() returned. stdout was lost and the certificate was
      stopped unfinished, so nothing checked it.
    - The no-cert rerun and the July engine's triangle solver are still running (ps 12:59Z, pids 333477/333479).
  - (c) "carried n ≤ 7" includes n = 3, where triangle-freeness gives only a tie.
- Replace: "… checked by an independent nauty-based verifier, reproduced by the same engine with reversed move ordering and
  with its cutoffs disabled, and by our July engine (separate code, Python, 41½ minutes). At n = 8 the triangle-avoidance
  route that carried 4 ≤ n ≤ 7 appears to break: our engine finds that Alice wins the (1:2) triangle game on K₈ (one engine
  so far, not yet certificate-checked). So this is the first value where Bob has to win the clique game as such."

S12. L71: "Problem status on the site: PARTIAL, not ours."
- Evidence: erdosproblems.com shows OPEN (problem-page capture), and the header strip says "Community database OPEN". The
  sentence reads as if some site lists the problem PARTIAL.
- Replace: "Our verdict on this entry: PARTIAL. The problem remains OPEN on erdosproblems.com and in the community database."

S13. Sources link (L72): "Verification bundle — solver, certificate, checker + controls, the Lean replay … ↗" →
github.com/pw/ErdosProblemADay.com/tree/main/verification/778/…
- Evidence: `gh api repos/pw/ErdosProblemADay.com` returns private=true, and an anonymous curl of
  …/tree/main/verification returns 404. Every "How we know it is right" claim points into a bundle no reader can open. This
  is site-wide (46 such links; CLAUDE.md flags it), but this entry leans on the bundle harder than most.
- Replace: publish the bundle somewhere public (make the repo public, or mirror the bundle to a public repo or Zenodo) and
  link that. Otherwise label it: "Verification bundle (private repository; available on request)".

## MINOR

M1. Homepage card title: "the first value past the table, and the only one between 7 and 3^158"
- Evidence: the intended reading is literally true (n ≤ 7 table, n = 8 today, n ≥ 3^158 by Didin–Pimenov, 9…3^158−1 open).
  But "the only one" parses as "the only value". The "3^158" end also rests on a third-party claim whose verdict is still
  ⟨VERDICT_DP⟩.
- Replace: "… and the only decided value between 7 and 3^158".

M2. L64 and card: "after 41 minutes"
- Evidence: 2,490.7 s is 41.5 min.
- Replace: "after 41½ minutes".

M3. L21: "using ChatGPT 5.6 sol pro"
- Evidence: the tab capture reads "(using ChatGpt 5.6 sol pro)". The quotation should be verbatim.
- Replace: "using ChatGpt 5.6 sol pro".

M4. L30: "every ℓ-set is 3/5 blue"
- Evidence: the paper says e_C(U) ≥ (3/5)C(ℓ,2).
- Replace: "every ℓ-set is at least 3/5 blue".

M5. L27: "a weight (4/3)^{3H/5 − x_U}(5/6)^{f_U} that rewards blue density inside U"
- Evidence: P_U is a danger weight. It is large while U is short of blue edges, ×9/10 per blue edge inside U and ×6/5 per
  red one. "Rewards" can be read as the weight growing with blue density.
- Replace: "a weight … that stays large while U is short of blue edges (×9/10 per blue edge inside U, ×6/5 per red one, zero
  once U is 3/5 blue)". Also define H = C(ℓ,2), x_U and f_U, which are used undefined.

M6. L37: "(five Bella strategies, two adversarial) … raised it by exactly 2d*(z)"
- Evidence:
  - "Bella" is never introduced; only "Bob — Chingiz" is.
  - Seat A's report names the five as random, max-danger, min-danger, clique-builder and density attacker. It never says
    "two adversarial"; that phrase comes from README.
  - d*(z) is undefined on the page.
- Replace: "(five Alice strategies: random, max-danger, min-danger, clique-builder and density attacker) … 19,816 Alice
  moves raised it by exactly twice the danger of her edge".

M7. L37: "(its only objections: …)"
- Evidence: seat A lists 8 items. The two quoted are the MINOR/size items, and six more NOTEs exist, e.g. "Lemma 1 … read
  literally … is false within a round".
- Replace: "(its two non-trivial objections, both minor: …; six further notes, none touching the proof)".

M8. L56: "her ten edges beat Bob's eighteen at keeping a triangle"
- Evidence: the phrase is garbled.
- Replace: "Bob's eighteen edges cannot keep her ten triangle-free".

M9. L62–63: "a deleted entry REJECT, the header's winner flipped REJECT, … thirty replies swapped … REJECT; one single swapped
reply was accepted"
- Evidence: all four mutations were made on the n = 7 certificate (controls.txt mut1/2/3/5). The page lets a reader assume
  n = 8.
- Replace: insert "(mutations of the n = 7 certificate)" after "Its controls:" before the mutation list.

M10. L61: "every recorded reply free and transported correctly"
- Evidence: the checker asserts only that the transported reply is free. Transport correctness is not separately tested,
  and the verdict does not need it, because the checker plays whatever edge it transported.
- Replace: "every transported reply free".

M11. L67: "the winner re-derived by reversed ordering and by cutoff-free backward induction"
- Evidence: both runs are the same program with flags (n8_clique_reverse.out 28.3 s, n8_clique_nocut.out 28.4 s; the brief's
  "26 s" for reverse is wrong, but the page states neither time). The one decorrelated re-derivation, the July engine, is
  missing from the labels.
- Replace: "… re-derived by the same engine with reversed ordering and with cutoffs off, and independently by the July engine
  (separate code, Python)".

M12. L64: "a different author's code with its own canonicaliser"
- Evidence: it is an independent implementation of the SAME algorithm (july-report: "colour refinement on the three edge
  colours, then explicitly enumerates every ordering inside every remaining vertex cell"). What genuinely differs is its Bob
  cutoff, which ignores Alice's edge budget ("after giving every free edge to red"). Its author is a Codex seat (log
  `codex_erdos_wavew014778.log`), so the card's "TWO AUTHORS" is two models.
- Replace: "a different author's Python code, with its own implementation of the same refinement-plus-orderings canonical
  form and a coarser Bob cutoff".

M13. L65: "its retrograde pass found no parent configurations for the (1:2) game on K6 or K7"
- Evidence: the recorded output is "childrennumber: 0 … 0 out of 0" with no winner printed. "Parent configurations" is an
  interpretation of that output.
- Replace: "its retrograde pass reported zero configurations ("childrennumber: 0 … 0 out of 0") and no winner for the (1:2)
  game on K6 or K7 by either entry point".

M14. L70: "What is ours: the n = 8 value and its certificate, the checker, and the referee report."
- Evidence: there are three seat reports (the sources line says "the three referee reports"), and the solver is also ours.
- Replace: "What is ours: the n = 8 value, the solver and its certificate, the checker, and the referee reports."

M15. Summary: "…the formal statement matched to the literal game) and kernel-replayed the Lean on our box: standard axioms,
statement matched to the literal game."
- Evidence: the phrase is duplicated, and the statement match was seat B's audit, not part of the replay.
- Replace: covered by the S2 text.

M16. Title and card: "refereed: holds as read"
- Evidence: this pre-commits the verdict while L49 is still ⟨VERDICT_DP⟩.
- Replace: when it lands, make the title and card read exactly ⟨VERDICT_DP⟩.

M17. L36: "Three separately briefed Opus seats with tools"
- Evidence: README lists seat C as "judgment seat, Opus" with no tools, and seats/C_judgment/ is still empty.
- Replace: once C lands, confirm it had tools, or write "Three separately briefed Opus seats (the first two with tools)".

M18. L23–24: "On 14 August they added a Lean 4 formalization"
- Evidence: maximdidin's 14 Aug comment says "GPT Codex formalized the proof". The provenance clause at L21–22 covers only
  the paper.
- Replace: "On 14 August they added a Lean 4 formalization (written by GPT Codex, per Didin's comment) …".

M19. Card tag: "CERTIFICATE CHECKED BY NAUTY"
- Evidence: nauty supplies canonical forms; the check is check778.py.
- Replace: "CERTIFICATE CHECKED BY A NAUTY-BASED CHECKER".

M20. Bundle README, linked from the page (not page text):
- "all 210,325 entries consumed": check778.py never tracks consumption. The 210,325 is `len(table)`, the distinct keys
  loaded. Replace with "210,325 entries loaded (no duplicate classes)".
- "`SHA256SUMS` covers everything in this directory": the file does not exist yet. Generate it before commit.

M21. Links:
- Header strip "Community database OPEN as of 2025-08-31": that is the record's last-update date (`lu`), not our refresh
  date (TRACKER_AT = 2026-10-13). This is site template wording; it reads as a stale snapshot.
- Cambie–Provoost link label "… and their solver": the solver lives at
  github.com/Algorithmic-Graph-Theory-Group/edge-colouring-games (commit b698f00), not at the arXiv URL. Either add that
  link or drop "and their solver".

## Checked, no finding
- n8_clique.out: 824,319 nodes, memo 306,185, 11.9 s ("twelve seconds"), BOB WINS. I recompiled the bundled solve778.cpp
  and re-ran it: n=3 Alice, n=4–7 Bob, and n=8 gives identical nodes and memo.
- Certificate: 210,325 lines.
  - Per-|R| counts are 1/5/63/477/3,375/18,774/73,983/98,946/14,701, sum 210,325.
  - Every row has |B| = 2|R| − 2.
- check log: 122,288 / 57,512 / 210,325.
- Controls match L62–64.
- Seat A: 2,444 / 43,320 / 19,816 / five breakages / 10^67.7.
- Seat B: 2⌊log₃n⌋+4; 250(⌊log₃n⌋+1)+1; 1/9, 8/9; 125·25^k(500k+505) ≤ 2·27^(k+1) first holds at k = 158 and holds for all
  k ≥ 158 (recomputed).
- Lean replay: Lean v4.24.0, f897ebcf, 959 jobs, axioms, sorryAx, wrong-shape type mismatch.
- θ^5 = 6250/6561 exactly; 1 − θ = 0.97% (< 1%).
- 1/log(5/3) = 1.9576 > 2/log 3 = 1.8205 ⇔ 27 > 25.
- 3^158 ≈ 2.4·10^75.
- Game statement vs the live capture: Alice first, Bob two per turn, strict, n > 3.
- α(R) > ω(R) reformulation correct (Bob's graph = complement of R).
- Edge counts: 28/10 and 36/12.
- Provenance paraphrase faithful to the paper's paragraph.
- Dates 5 Aug (tab submitted 2026-08-05) and 14 Aug (Lean comment 23:02, 14 Aug).
- CP Theorem 8 (every n ≥ 4); the "We conjecture this is indeed the case" sentence; Conjecture 17 = (p,p+1) large n; no
  (1,2) small-n table (Table 1 covers symmetric games only).
- Triangle header says winner=alice and is written only after solve() returns. The July engine's n = 8 triangle run is live,
  so the L56 hedge is accurate.
- No page sentence implies Bob keeps Alice triangle-free at n = 8.
