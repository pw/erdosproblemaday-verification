# Second verifier (Claude instance, Opus 5.5), written without the author's code, 2026-11-24

Brief: build a decorrelated verifier from the paper (§§3–7) and the data format only. The seat never opened,
imported or copied the deposit's `verify.py`; it read the orchestrator's log of that run only after its own
results were final (to compare timings). Sources and logs: `second-verifier/` (`run_all.sh` reruns everything).

## What it built

1. **Graph basis (`basis.py`).** `nauty-geng -q 7`, own graph6 decoder, own canonical form (smallest mask over all
   5040 relabellings). 1044 distinct graphs; Σ 7!/|Aut| = 2,097,152 = 2²¹, so the list is complete. The model's
   1044 `graph_slack_flags` match one-to-one, no duplicates.
2. **Identity, route A (`counts.py` + `evalA.py`).** For each graph H, counts every placement of roots and disjoint
   extension sets (denominators 2520·2, 210·6, 7·20, 210·24, 210·4, 840·3). D (new vertex adjacent to ≥ 2 roots),
   ρ = ½·(K2 density), the 816 generators [[(c* − D)F]]_τ and the rooted Bollobás term X³ − 11XE + 30T + 15P3 on
   type K4 minus edge 01 (sector = common neighbours of roots 0, 1) rebuilt from the paper; each descriptor in the
   model matches.
   - Exact: 1044/1044 residuals exactly zero over Q(√3).
   - Modular: three fresh random 62-bit primes p ≡ ±1 (mod 12) per run, √3 mod p by Tonelli–Shanks, evaluated at
     both roots: 6/6 evaluations give 1044/1044 zero, each matching the exact residual reduced mod p.
3. **Identity, route B (`routeB.py`)**, sharing no counting code with route A: takes H from the model's masks,
   averages over all 5040 orderings of H's vertices, identifies flags through a dictionary of all root-fixing
   relabellings, evaluates vᵀQv in exact Fractions, builds the Bollobás term from the model's indicators. Run on
   all 1044 graphs: every residual exactly zero, and all 87 per-term values (ρ, 82 blocks, λ total, β, constant,
   slack) equal route A's exactly. 409 s on one core.
4. **PSD and signs (`psd.py`).** Symmetric elimination with largest-diagonal pivoting in exact Q(√3); signs decided
   exactly (squaring when the rational and √3 parts have opposite signs); if the largest remaining diagonal is 0 the
   whole remaining submatrix must be exactly zero. All 82 matrices pass; 22 are exactly singular (kernel dimensions
   per block in psd.log, matching a floating-point eigenvalue survey block by block). Block 0 (the localizer) is
   positive definite. No λ_j is negative (596 of 816 exactly zero); β = 1917/10 − (1648/15)√3 ≈ 1.405 as in (32);
   λ817 − λ818 = −1/4 exactly; no slack is negative, 40 are zero.

## Controls (all behaved as required)

Identity mutations (each + 1e-6; exact and both modular roots flag the same graphs every time):
slack[517] rational part → exactly {517}; slack[517] √3 part → exactly {517}; λ[101] → 40 graphs; λ[1] (was 0) →
36; Q0[1,2]=Q0[2,1] → 549; Q5[3,17] → 10; Q40[0,1] → 4; β → 33 (exactly the graphs the Bollobás term touches);
c* → 937; the constant → all 1044.

Convention controls (route B on 30 graphs): D = exactly 2 root neighbours breaks 11/30; D = at least 1 breaks
26/30; ρ without the ½ breaks 30/30; Bollobás sector at roots {2,3} breaks 7/30; flags treated as fully labelled
breaks 30/30.

PSD/sign controls: [[1,2],[2,1]] fails; zero pivot with nonzero column fails (zero-pivot branch); [[0,1],[1,5]]
fails; singular PSD [[2,1,0],[1,½,0],[0,0,0]] passes; [[2,√3],[√3,3/2]] passes and fails at 3/2 − 1e-40; real
singular blocks 5, 12, 7 minus 1e-30·I all fail (a floating-point check would pass these); block 3 with an
off-diagonal pushed past det = 0 fails; sign(1.732050807568877 − √3) = −1 and sign(1.732050807568878 − √3) = +1;
one slack negated is flagged, exactly that slack.

## Timings (peak RSS < 200 MB, ≤ 6 cores)

basis 0.6 s · counts 8 s · evalA exact + 6 modular 17 s · evalA with controls 2:14 · psd (82 matrices) 87 s,
7:22 with the single-threaded planted controls · routeB all 1044 graphs 409 s.

## Notes

- The 816 `P_flag` generators are every order-6 τ-flag (816 of 816); 220 have nonzero λ.
- 1003 of 1044 slacks have rational and √3 parts of opposite sign: the sign check must be exact.
- The Bollobás term is nonzero on only 33 graphs, with negative per-graph coefficient on some (normal).
- The model's identity string reads "rho + … = 0", meaningful only with constant −1/4, which holds exactly.
- Paper side checks (exact): (12) from (11); (k−5)(k−6)/k²; α6 = (6+√3)/11 solves α − (11/12)α² = 1/4;
  c6 = (36−5√3)/66; c6 < 83/200 < c5. §§3–8 read; no gap found.
