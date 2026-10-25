# Hostile referee report 2 — h1cube2.py additions (Opus seat, 2026-10-19 ~15:52–16:45Z)
(Saved by the 15Z erdos seat; the seat's harness blocked its own write. Its harness/tests/outputs are beside this file;
h1cube2.py was not modified by it.)

**VERDICT: HOLDS WITH FIXES.** --pairsb, --slots and --ph are sound and do what their comments say (slots and PH are
implied by the case formula; pairsb is valid symmetry breaking jointly with the within-block transposition clauses).
The one failure is the --relax-pairs CONTROL: it cannot serve as a positive control.

Method: lib.py runs the real h1cube2.py source verbatim up to the solver call with markers inserted, so every test
checks exactly the clauses each option emits. All runs < 2 min, ulimit -v 6e6.

1. SUBSTANTIVE — --relax-pairs is not a working positive control (line 30 `RELAX = …  # CONTROL ONLY …`).
   k=5 decided without SAT (geng_blocks.py, T7_geng_k5.out): `nauty-geng -f -d4 -D4 18` = all 64 4-regular C4-free
   graphs on 18 vertices (re-checked); under RELAX a block = 3 vertices pairwise without common neighbour; across the 64
   graphs there are 7 such block partitions and NONE has e ≡ 1 (the pattern h1cube2 5 0 fixes). Positive control: the
   known SAT relaxed block-form model (K5_sb_relax.out) is graph 29 and the search recovers its blocks (pattern
   (0,0,1,1,1,1)). ⇒ `h1cube2 5 0 --relax-pairs` can never be SAT; its UNSAT with --ph --pairsb is CORRECT, not an alarm;
   UNKNOWN without --pairsb is hardness. **Side result: none of the 7 partitions can be paired with no edges between
   paired blocks ⇒ the k=5 analogue of H1 is EMPTY BY ENUMERATION (independent of SAT; confirms README §4).**
   k=7: never SAT (j=0..4 at 95 s with --ph --pairsb; j=0 60 s without; j=4 600 s). Root cause: RELAX switches off
   (ii) but keeps the case's edge pattern, which comes from Lemma D, whose step 1 uses (ii). A SAT result would only show
   the PH/pair clauses don't empty that one formula; it would not show implication, nor test the PH paths the real runs
   use (partner block ⇒ ew None + forced unit [m]), nor slots (off under RELAX) nor Lemma D (off). FIX: stop citing
   --relax-pairs as evidence; use the implication/equivalence tests below as standing controls; for a SAT relaxed
   instance free the internal edge pattern too.
2. MINOR — SAT recheck ignores RELAX (line 246 partner-edge check): relaxed models print non-zero "structural
   violations" (18 at k=5, 26 at k=7 j=3, with --drop-c4); only bad[:3] shown, so a real violation is indistinguishable.
3. MINOR — pair-perm recheck and --check-only mirror add_perm_sb, so they can't detect a direction/order mismatch with
   the transposition clauses (the actual soundness condition). That mismatch matters: orbit test (test_orbit.py) —
   pair-level direction flipped ⇒ 10/12 full-group orbits at k=5 lose every member; order reversed ⇒ 2/12; real code ⇒
   0. --check-only works on --drop-c4 models (5/47 at k=5, 217/383 at k=7 j=4) but is vacuous on the relaxed control.
   Keep test_orbit.py as a standing control.
4. MINOR — docs/dead code: PH comment cites a README §2b that did not exist when read (added later by the seat); usage
   line omits --slots/--ph/--relax-pairs/--check-only; "6 H-neighbours … (5 vertices)" is k=7 wording on generic code;
   never-taken branches mvar.get(…,"na"), `if m is None`, `if any(l is True …)`. certify_case.sh DRAT-certifies the
   emitted CNF only — the soundness of every SB/derived/implied clause rests on the arguments here, which must be in the
   README with labels before any case result is banked.

A. --pairsb HOLDS: automorphism of the case formula (asserts: pattern preserved, maps commute with partner, fixed edges
   map to themselves; Lemma D set symmetric; C4 clauses cover all pairs; clause level: lex-smallest orbit member of every
   sampled base model is again a model, 0 failures). NOT an automorphism of formula + transposition clauses (132/138
   images violate them) and need not be: soundness = lex-leader over the combined group G. Same variable order (constant
   pairs map to constant pairs with equal value ⇒ dropping them changes no comparison; row-lex = full row-major order
   restricted to free pairs = sorted(var)). Same direction (both X ≤lex X∘g, 0<1 — load-bearing, see 3). Enumerated set
   = full stabiliser of the edge pattern minus identity (23/11/15/47/383 for j=0..4, 47 at k=5). Evidence: k=5 full group
   3,072 elements, 53+54 sampled orbits, 0 failures (every raw sample violates the SB clauses ⇒ not vacuous); k=7
   subgroups containing all pair perms + every transposition type, every j, up to 98,304 elements, 121 orbits, 0
   failures; both mutations caught 10/10.
B. --slots HOLDS: counts right; base(drop-c4) + ¬(each slot clause) SAT for 0 of 96/456/492/528 clauses (k=5; k=7 j=0,
   2, 4); the false stronger "matched vertex hits every block" refutable 144/144, 168/168, 192/192.
C. --ph HOLDS and the encoding equals the statement exactly. Re-derivation (f(z) = z's unique Y-neighbour; f(z1)=f(z2)=y
   ⇒ w–z1–y–z2 C4; y ≠ w; triangles harmless; z ∈ Y misses Y iff unmatched; partner block fine; only Y = own block
   excluded). m defined both directions; t one-directional, sound (positive-only); no clause stronger than the statement.
   Equivalence (test_ph.py): 0 mismatches — 3,600 checks at k=5, 11,200 per case at k=7 (j=0..4 + relaxed j=0,4);
   mutations caught: m direction flipped 1,158/3,520/4,191; neighbours inside Y dropped 51/93/45; matched inside-Y counted
   as missing 60/100/114. Implication (test_ph_implied.py): premises (deg d, ≤1 nbr in Y, ≤1 common nbr with each vertex
   of Y) + ¬PH UNSAT for every (w,Y): 0/90 at k=5, 0/280 at k=7 j=0, j=4, relaxed j=2 (w's neighbourhood fixed to a
   sampled valid set; negation written independently AND via h1cube2's variables); dropping the shared-neighbour premise
   ⇒ SAT 78/90, 28/280, 34/280, 204/280 (that premise carries the weight; the test can fail). With w's neighbourhood free
   one k=7 vertex did not finish in 60 s — PH is a pigeonhole fact the solver does not find by itself.
