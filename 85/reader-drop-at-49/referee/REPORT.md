# Hostile referee report — #85 submission jhpvtq ("A Drop at Forty-Nine", Zenodo 10.5281/zenodo.23325806)
Seat: separately briefed Opus (claude-opus-5-5) with tools, told to refute; 2026-10-19 ~09:30–09:55Z, 128 tool calls.
(The seat could not write this file itself; the main seat transcribed its final message verbatim in substance.)

**Verdict: HOLDS WITH GAPS.** Could not refute f(48)=8, f(49)=7; no FATAL finding.

## Findings
1. SUBSTANTIVE (declared): Result A is conditional on hH1/hH7, supported only by external cake_lpr checks of ~48 TB of proofs, most discarded (retained: 12,094 bank proofs on a Requester-Pays bucket; the 28 H7 cover proofs; re-solve recipes ~3,400 CPU-h H1 census, ~4,300 H7). Lean: Erdos85OrderFortyNineCapstoneH3.lean:18-29 takes (hOne) (depth) (hSeven); no sorry.
2. SUBSTANTIVE (partly undeclared): native_decide trust base — 598 native axioms in the capstone (408 H3 + 58 H5 + 91 H7 + 23 H1 + 18 h=9). Erdos85OneHighV2CnfEmit.lean:64-66: "Building and printing the entire 12+ MiB formula as one `String` has produced duplicated trailing bytes in the native executable" — an unexplained wrong-output bug in compiled code, worked around, not in the paper. Mitigations: compiled emitter matched the Python generator on 13,351 instances; independent H1 orbit recount agrees; H7 streams reproduce byte for byte. Not corroborated outside compiled code: H3 (408 parts via a leanc -O3 plugin), H5 (58), h=9 (18), the 13 in-Lean LRAT replays for H7 t>=1.
3. MINOR: hH1's structure OneHighFamilyV2CheckedUnsat also requires a `nonzero` field (no literal 0) with no generic Lean proof; implied only by a successful `v2cnf check`. One native_decide over the inventory would close it.
4. MINOR: the 96 historical H1 orbits — checked files are archived sweep CNFs; no receipt shows regeneration with v2cnf; the manifest of expected hashes (9d04a66c…) is not in the bundle. Our sample's historical orbit b953a73b0e372480 re-emission closes it for that orbit.
5. MINOR: hardest orbit h1_81494a6ef36d3ec9 — solve receipts for nodes 54, 61, 64, 65, 70 record cube_sha_ok: null; per-leaf expected hashes / cube_verdict.py not in the bundle. Lean side fine (36 cubes = 36 receipt literal sets; brute force over 2^19 assignments covered; all 36 cake_lpr-verified).
6. MINOR (wording): the H7 "native generator" IS the compiled Lean definitions; the byte comparison was against Python gen_pilot.py. Leaf files are assembled in Python (h7_common.py).
7. NOTE: imported Mathlib .oleans trusted (cache), not re-checked; leanchecker --fresh would close it.
8. NOTE: cake_lpr exits 0 on failure, so the success-detection scripts are load-bearing; they are on GitHub at 2029149d7e42, not in the Zenodo bundle. Census README records a duplicate-claim bug that deleted a live work dir; "no certified receipt affected" not checkable.
9. NOTE: f(50)=8 (Hoffman–Singleton; δ>=8 needs n>=57), so f = 8, 7, 8 at 48, 49, 50.
10. NOTE: hypotheses can't be met trivially: soundness proved for every depth; cube list and inventory fixed, non-empty.

## Checked and found sound
- Statement fidelity (C4, containsC4, minDegreeForC4, Erdos85Question; witness/threshold duality).
- Case split ranges over all C4-free 49-vertex graphs with δ>=7 ("high" = degree exactly 8).
- Hand re-derivation of degrees 7/8, h odd, h ∉ {11,13,...}, H7 split (7−t, 14+3t, 21−3t), t<=7, H3 b∈{0,1}, H5 t<=2, H1 structure; f(40)=7 so a 6-regular C4-free 40-vertex graph exists (H1 is not vacuous).
- H1 cover ranges over every one-high graph; capacity inequality is a kernel proof.
- Independent H1 orbit recount (h1_orbits_indep.py): profiles 0–4 labelled tables 449,358 / 169,668 / 70,070 / 31,512 / 16,692; groups 384/48/16/12/24; orbits 1536/3662/4801/2700/842 = inventory rows, each orbit hit once.
- H1 evidence set (h1_setmatch.py): capacity filter keeps 13,351, removes 190; bank 12,094 + census 1,160 + historical 96 + hardest 1 = that set exactly, profiles match.
- H7 (h7_receipt_cover.py): 28 cubes and masks match Lean at depth 3; all 377,776 leaf indices have receipts; cover hashes match; 256+1 split matches spec. SB soundness is a kernel proof (no native_decide).
- Closure: no sorry/axiom/opaque/implemented_by/@[extern]/unsafe/skipKernelTC/custom elaborators; partial defs only in proof decoders (bad decode fails the check).
- Novelty: Boza v1 tex "≤ 50" where v2 prints "/50"; r(41)=49 (Parsons); Zhang–Chen–Cheng 2017 covers n=48,47,45 (q=7), not 42; OEIS A006672 ends at n=38; erdosproblems #85 no proof claims; Cambie 17 Sep 2026 calls f(49) "tough".

## Not checked by the referee
Lean replay; H1 re-emission sample; H7 leaf hashes; any SAT/cake_lpr rerun; H3/H5/h=9/H7 t>=1 native_decide content; Theorem B beyond statement + axiom line.
