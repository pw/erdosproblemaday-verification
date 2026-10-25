<!-- Written by the referee seat (Opus, separately briefed, 2026-10-20 ~06:2x–06:4xZ); saved verbatim by the erdos seat because the harness blocked the referee's own write. -->
# Hostile referee: Erdős #85, T1Rep0 external check (2026-10-20)

## C1: the CNF file is the DIMACS of `orderFortyNineGeneratedH7SatCnf (representativeMasks 1 0)`. HOLDS WITH FIXES

What I checked:
- **The `==` check is real but nearly tautological.** Equality on these types compares element by element, in order, so it is not vacuous. But `arr` is built from the same four Lean definitions in the same order as the Lean def. It proves there was no transcription slip, and nothing more.
- **The file itself is checked by nothing in the emitter.** I checked it directly with awk:
  - 1,329,041 clauses, matching the header.
  - No zero literal inside a clause, no empty clauses, no tautologies.
  - All tokens are canonical decimal; the largest variable is 29764.
  - Clause lengths fit the Lean size lemmas: 315 of length 1, and 294 of length 7 or 8.
- **The direction is right.** If the DIMACS file is UNSAT, then the Lean `CNF.Unsat` follows: any satisfying assignment of the Lean CNF pulls back to one for the file. The literal map `(natAbs−1, 0<lit)` is safe because no literal is 0.
- **No compiled-code escape hatches.** The authors' sources have no `implemented_by`, `extern` or `unsafe`, so the emitter's compiled evaluation carries the same trust as their native_decide.

Objections:
1. "c parsed a formula with 29764 variables and 1329041 clauses" (`lratcheck_t1r0.out`) is not evidence of anything. lrat-check prints the header's numbers back (`printf(..., nVar, nCls)`). It reads every clause to end of file regardless, and uses the header only to size memory.
2. "the seat claims this is a formatting difference only" (`source_cnf_sha256` 6699c73d… vs ours 4fc61de9…) is unverified.
   - I tried six format variants: no header, CRLF line endings, no final newline, double space before 0, trailing space, and sorted literals. None gives 6699c73d.
   - The authors' generator script is in neither the repo nor the receipts.
   - This is not a soundness problem, because the Lean definition is what counts. But call it "unexplained", not "formatting".

## C2: lrat-check `c VERIFIED` implies UNSAT. BROKEN as stated; the conclusion is rescued by an independent strict check

1. **lrat-check accepts the final empty clause without checking that it reaches a conflict.**
   - The empty clause has no first literal, so its "pivot" is literal 0. When its hints run out without a conflict, lrat-check falls back to a RAT test on that pivot (`intro[1]`). That entry is never set by any real literal, so the step passes.
   - Reproduced on small hand-made cases in `referee/`:
     - Satisfiable `{1∨2}` with proof `2 0 0` (empty clause, no hints): `c VERIFIED`.
     - Satisfiable `{1},{1∨2}` with `3 0 1 0`: `c VERIFIED`.
     - Satisfiable `{1∨2, ¬1∨2, 1∨¬2}`, one valid lemma, then an empty clause with one hint: `c VERIFIED`.
     - An UNSAT 4-clause formula whose empty clause has its last hint dropped (`p_drop_last.lrat`): `c VERIFIED`.
   - So VERIFIED only certifies the non-empty steps. The final step, which carries the whole claim, was never checked.
2. **lrat-check is not memory-safe on bad input.**
   - A hint pointing into an emptied or never-allocated bucket reads `clsList[-8192+offset]`, which is undefined behaviour. It segfaults on `p_c.lrat`.
   - On tiny CNFs it overflows its clause table ("realloc(): invalid next size"): it writes one more int per clause than it reserves room for.
3. **Your controls could not see the hole.**
   - "a hint dropped at the 4,000,000th multi-hint addition → NOT VERIFIED" only tests a step in the middle of the proof, never the empty-clause step.
   - Your first CNF control ("a negated CNF unit clause") came back `c VERIFIED`; `controls.rc` reads "cnfmut pipestatus 0 0".
   - That control was vacuous. My strict checker also accepts the full proof against the flipped CNF, so clause 1 is never needed by the proof.
   - Your second CNF control (`cnfmut2`, on clause 1302103) is the meaningful one.
4. **The other cases you asked about are fine.**
   - The index on deletion lines is ignored by lrat-check, so it doesn't matter.
   - An addition whose id collides with a live clause silently overwrites it. That acts as a deletion, which is sound.
   - A truncated stream gives VERIFIED only if the empty clause came before the cut, which is sound.
   - RAT steps: the decoder counts `rat_adds=0`.

**Rescue (done).** I built a route that shares no code with yours:
- `src/unpack7.c` does the 7-bit unpacking.
- zstd's own LZ4 decoder (`zstd -d --format=lz4`) replaces your LZ4 code.
- `src/rupcheck.c` is a strict checker that follows Std's binary parsing rules. It requires:
  - every hint to refer to a live clause;
  - every added clause, including the empty one, to reach a real conflict, with no RAT steps and no fallback;
  - no reused clause ids;
  - the CNF clause count to match the header.
- On the hand-made cases it rejects all four exploits above, plus use-after-delete and undefined ids, and it accepts a valid UNSAT proof.

Result on t1rep0 (`referee/t1r0.out`, 72 s, 172 MB peak memory):
- "EMPTY CLAUSE derived by conflict: id 10975255, action #14332419, 85 hints"
- "actions=14332419 adds=9646214 … del_of_nonlive=0 … nonmonotone_ids=0"
- "RUP-VERIFIED (strict)"

**`h7_t1_rep0.cnf` is UNSAT** on this route, and the empty clause is the very last action.

## C3: the stub axiom is no stronger than C1+C2, and exactly one axiom is swapped. HOLDS (its support now rests on the strict check, not lrat-check)

- I recomputed the axiom lists from `stub/axioms.out` against RUN.json (`completed`, both CapstoneH3 and FiniteDropCapstone): 601, 607 and 604 axioms, matching for both modules.
  - Only in the authors' list: `Erdos85.sevenHighT1Rep0_check._native.native_decide.ax_1_1`.
  - Only in ours: `Erdos85.erdos85_t1rep0_cnf_unsat_checked_externally`.
  - No `sorryAx`. Your earlier stub (v1) likewise swaps exactly one axiom.
- The axiom states `CNF.Unsat` for exactly the CNF that Std's `LRAT.check_sound` concludes about. That is weaker than the authors' `LRAT.check … = true`.
- The stub's derivation from that axiom is kernel-checked from the authors' own lemmas.
- The 9 rebuilt downstream modules' sources match RUN.json's `source_sha256`.
- The stub no longer exports `sevenHighT1Rep0Proof_size` or `sevenHighT1Rep0_check`, and no downstream module needs them.

**Fix needed:** the stub's docstrings cite lrat-check as the evidence. As written, the axiom is justified by a checker that accepts satisfiable formulas. Point them at the strict route, or at cake_lpr (which the authors themselves use for their external evidence).

## C4: the decoder reproduces the authors' certificate. HOLDS, and more strongly than claimed

- My independent decode, converted to text, hashes to `e83341791f8da4b1…`. That equals the `compact_lrat_sha256` in the authors' module header.
- Your `unpack_lrat` text gives the same hash (`referee/seatdec.sha256`).
- On t7 the same match holds (3d9940e3…), and my text is byte-identical to `t7r0.lrat`.
- The binary is 2,680,553,030 bytes, as the module declares, and the packed file's hash matches the manifest.

You only matched the action count. The header hash is a byte-exact check, and it passes. I agree that UNSAT soundness does not depend on C4.

## Coverage of other modules, and the larger problem

- `steps.tsv` against RUN.json: 883 Proofs modules plus 1 Archive module replayed with exit 0, and **zero** source or olean hash mismatches.
- The only gaps are T1Rep0 (checked externally, above) and its 9 downstream modules (rebuilt over the stub).
- The other 12 H7 representative modules were replayed in Lean itself. So the lrat-check VERIFIEDs in `all13.tsv` carry the same hole but don't matter.

**Major objection: the capstone does not state f(49)=7.**
- Every headline theorem has the form `…_of_h1_h7Evidence (hOne …) (depth) (hSeven …)`, i.e. it takes two hypotheses.
- `Erdos85FiniteDropCapstone.lean` says so itself: "The conclusions remain conditional in Lean… its receipts are not Lean proof terms."
- `hOne` asserts `OneHighFamilyV2CheckedUnsat` for every inventory table.
- `hSeven` asserts that the cover and leaf formulas are UNSAT for 28 structural cubes; for this the authors cite cake_lpr receipts.
- Neither the Lean replay nor any external route of ours has checked hOne or hSeven.

What we have actually verified is:

> (hOne ∧ hSeven) ⇒ minDegreeForC4 48 = 8 ∧ minDegreeForC4 49 = 7

That holds modulo about 600 native_decide axioms plus the one externally checked UNSAT. I did not examine the translation to R(C4, K_{1,42}) = 49.

## Overall

**HOLDS WITH FIXES.** The T1Rep0 UNSAT result now stands on a sound, strict, independent route, and the one-axiom swap is exact. But:
- The claim "lrat-check VERIFIED ⇒ UNSAT" is BROKEN and must not be cited.
- One of the CNF controls was vacuous.
- Any "f(49)=7" claim must be stated as conditional on hOne and hSeven unless we check those.

---

## Objections, in brief
1. **C2 BROKEN:** lrat-check passes an empty clause whose hints never reach a conflict. It printed `c VERIFIED` on three satisfiable formulas and on a proof with the empty clause's last hint dropped.
2. **C2:** lrat-check reads out of bounds on hints into freed or unallocated buckets (segfault reproduced) and overflows its table on tiny CNFs.
3. **C2:** the hint-drop control never touched the empty-clause step. The first CNF control returned VERIFIED and was vacuous because clause 1 isn't needed.
4. **C1:** the "parsed … 1329041 clauses" line just echoes the header.
5. **C1:** "formatting difference only" for the hash mismatch is unverified; six format variants don't reproduce 6699c73d.
6. **C1:** the `==` check is nearly tautological, and the file itself was never checked against `arr` by the emitter. I validated it externally with awk.
7. **C3 fix:** the stub docstrings justify the axiom with lrat-check; repoint them to the strict route or cake_lpr.
8. **Major:** the capstones are conditional on hOne and hSeven (the authors say so in `Erdos85FiniteDropCapstone.lean`), and we have checked neither. Any "f(49)=7" claim must say so.

What holds:
- The strict independent recheck: `RUP-VERIFIED (strict)`, empty clause derived by a real conflict at action #14,332,419.
- The axiom set difference is exactly one swap on all three theorems.
- My decode and yours both match the header's `compact_lrat_sha256`.
- Module coverage is complete, with zero hash mismatches.

Files are in `~/MathDyad/erdos85/t1rep0/referee/`:
- Tools: `src/unpack7.c`, `src/rupcheck.c`, `src/bin2text.c`, `run_ref.sh`
- Results: `t1r0.out`, `t1r0_cnfmut.out`, `t1r0_text.sha256`, `seatdec.sha256`
- Exploit cases: `sat*.cnf`, `unsat4.cnf`, `p_*.lrat`, `empty_*.lrat`