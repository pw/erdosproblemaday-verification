<!-- Saved verbatim by the 09:00Z erdos seat (2026-10-28) from the referee seat's final message; the harness blocked the seat's own write. -->

**VERDICT: HOLDS WITH FIXES.** I could not break the claim that all 13,351 H1 cell CNFs are UNSAT and DRAT-verified, or that the cells cover H1. Fixes:
1. Say what DRAT certifies and what it does not.
2. Disclose that the proofs were deleted and publish what is needed to reproduce them.
3. Update README §4/§5 and pin the files.
4. Two minor documentation errors.

Hostile referee seat, Opus 5.5, 2026-10-28 ~09:10–09:45Z. Every run used nice 19 and `ulimit -v 4000000`, with at most 2 at a time, each under 30 min. I killed nothing I did not start.

### Attacks and results

| # | Attack | Result | Artefact |
|---|---|---|---|
| 1 | drat-trim source: every path that prints `s VERIFIED` | 3 paths (drat-trim.c:1480–1481). Empty clause in the formula and unit-propagation refutation of the input are both ruled out (no empty clause; min proof 973,798 B). The third is a completed backward check. | source read |
| 2 | My DRAT negative controls N1–N4, each with a twin | all behave | `drat_negctl.out` |
| 3 | Re-run 8 random cells end to end (seed 4242) | 8/8 match hash, proof bytes and VERIFIED | `repro.out` |
| 4 | Orbit-representative test, all four flags plus transposition SB | 125/125 orbits keep a representative. Mutations killed 6/6 (pair-flip, j=0), 6/6 (forced edge-swap invariance, j=0), 3/3 (pair-flip, Stab 128). | `orbit_batch.out`, `orbit_mut_j0.out`, `orbit_mut_stab128.out` |
| 5 | Campaign formula minus C4, 150 random cells | 150/150 SAT, recheck clean | `posctl.out` |
| 6 | Bare cell: no flags, `--no-sb` | 2/2 UNSAT (139 s, 550 s) | `ablate.out` |
| 7 | Coverage with cut/sort/comm | key sets exactly equal to `classes_all.tsv` | inline |

flipcheck's rerun reads ALL PASS. Its first run failed C2 only because `kissat` is not on PATH ("kissat none"); you already fixed that.

### Objections

**1. Scope overclaim in the public sentence.**
- Quoted: "Every one of the 13,351 H1 cells is unsatisfiable: each came back UNSAT under Kissat, and again under CaDiCaL with a DRAT proof that drat-trim verified."
- Why it matters: DRAT certifies only that 13,351 specific CNF files (identified by sha256[:16]) are UNSAT. The encoder (h1mcell, h1cube2, pysat), the SB soundness, PH/slots, M1–M4, the enumeration, coverage and the reduction are all hand proof plus review. README.md:98 says this; the sentence drops it.
- Can it fail in practice? No defect found; this is an omission, not a gap.
- Fix: add one clause saying what is machine-certified and what rests on the refereed proofs.

**2. Certificates destroyed.**
- Quoted: campaign.sh:33 `rm -f $cnf $pf`.
- Why it matters: 253.7 GB of proofs are gone, so each verdict now rests on a log row. A full re-check costs about 280 CPU-h for DRAT plus 207 h for Kissat.
- Can it fail in practice? I tried to catch the log misreporting. In 10 from-scratch re-runs (8 repro cells, the smallest cell, and flipcheck C6's 90th-percentile cell), the proof byte count matched the log exactly every time. CaDiCaL is deterministic, so these are the same computations the log records. The 8 repro cells and the smallest cell also matched the CNF hash, and the 8 repro cells matched VERIFIED. flipcheck B separately re-emits 30 cells, all hash-equal.
- Fix: say "checked, then deleted", and publish:
  - the runner;
  - the tools: CaDiCaL 1.7.3, drat-trim 2e3b2dc, Kissat 4.0.4, pysat 1.9.dev7, Python 3.12.3;
  - the per-cell table: j, M, hash, proof bytes.

**3. README is stale and nothing is pinned.**
- Quoted: README.md:102–103 "NOT started from a cron tick: Patrick's call. Runner (ready, resumable, not launched)".
- Fix: add the campaign facts:
  - Kissat pass: 10-25 09:02Z to 10-26 05:49Z, one pass, 206.9 h, max 1,347.7 s per cell.
  - DRAT pass: 10-26 05:49Z to 10-27 09:55Z, one pass, 280.1 h, max 4,926 s per cell.
  - Proofs: 0.97 to 354 MB.
  - sha256 of `classes_all.tsv` (`dfbf69ca7215cfd0`) and of both TSVs.
- Scope note: "independently reproduces f(49) ≤ 7" also rests on strata h=3,5,7,9 and the hand case split. Those are outside this report.

**4. (minor) Wrong header comment.**
- Quoted: campaign.sh:9 "Every child: nice 19, ulimit -v 4 GB."
- Why it matters: drat-trim (line 30) runs without ulimit. Harmless for soundness: a memory failure never prints `s VERIFIED`.
- Fix: correct the comment.

**5. (minor) Kissat pass never hashed its CNFs.**
- Why it matters: "again under CaDiCaL" assumes both passes solved the same formula, but that was inferred, not recorded.
- What I checked: h1mcell.py, fsenc.py and pysat's card.py were all last modified before 10-25. Emission is identical under PYTHONHASHSEED 1, 2 and 99, and equals the DRAT row (`ef6319776081b016`).
- Fix: state this in the README, or hash in Kissat mode next time.

### Residual risk (not an objection)

The C4 and PH clauses cannot be exercised by any positive control: if H1 is empty, no model exists. They rest on:
- h1mcell's C4/PH/slots code being byte-identical to h1cube2 (the diff touches only the docstring and the print line);
- h1k/referee2 tests T4 (PH equivalence), T5 (PH implied) and T6 (slots);
- my reading that codegree ≤ 1 with fixed edges as constants is exactly C4-freeness;
- the ablation in attack 6, which shows two cells need neither PH, slots nor any SB.

### Detail

**drat-trim.**
- Timeout prints `s TIMEOUT` and exits (line 905).
- An empty lemma with no conflict gives "conflict claimed, but not detected" (line 845); no conflict at all gives "ERROR: no conflict" (line 874).
- The lrat-check hole (#42/#43) is in `lrat-check.c`, which this pipeline never runs.
- Ignoring unit deletions (line 1170) is sound: it can only make RAT checks stricter.
- Binary detection: CaDiCaL proofs start with byte 'a', which drat-trim classifies as binary.
- A header undercount only weakens the formula; N4 shows the real proof then fails.
- Open upstream issues #39 (comment parsed as header) and #3 (variable overflow above 2^31) don't apply: the CNF has `p cnf` on line 1, no comments, and max variable about 30k.

**N1–N4.** Twins (expected VERIFIED) are in brackets.
- N1, invalid lemma on a SAT formula, text and binary: rejected [twins verified].
- N2, real proof with additions reversed: rejected [original order verified].
- N3, proof A against CNF B: rejected [proof A against CNF A verified].
- N4, header count cut to 60%: rejected.

**Formula.**
- `menum.PAIRS` (menum.py:37) equals `MPAIRS`.
- h1mcell asserts row sums.
- In the positive control (150 cells, 8/27/53/52/10 per case j = 0..4, 19 with non-trivial pair SB), the recheck found 0 violations of structure, cell membership, edge-swap lex, transposition lex, pair lex and PH.

**Orbit test.**
- Cells: 25, namely the top-3 stabilisers per case (including both Stab-128 cells), plus 10 random; 5 models each.
- Method: g = β∘σ, where β is drawn from D4 on e=2 blocks or Z2×S3 on e=1 blocks, and σ from Stab(M).
- Result: 0/125 raw models already satisfied the SB clauses, so the test is not vacuous.

**Coverage.**
- 13,351 distinct keys in each source.
- No duplicates, no conflicting verdicts, no CR bytes.
- orbit × |Stab| = |G_j| on every row.
- Both passes completed in one go.
- tally.py cannot pass with cells missing.
---
**Seat note (09:00Z erdos seat, 2026-10-28), on attack 6:** `ablate.out` shows `sb=0 slots=0 ph=0 edgeswap=0` but `trans_sb=16`
and `trans_sb=20`: the "bare" runs removed the four flags and the lex-leader SB, NOT the transposition symmetry breaks. So
"no flags and no SB at all" overstates it; the public page says "with the four extra clause families and the lex-leader
breaks removed". Every other count above was re-read from its output file (orbit 25 cells / 125 models / 125 with rep;
posctl 150/150 SAT, 0 violations; N1–N4 PASS; repro 8/8) and stands.
