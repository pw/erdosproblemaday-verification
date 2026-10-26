# Seat C report — exact computation on small cases
Object: OpenAI, "Uniform exclusion of Landau–Siegel zeros" (1 Oct 2026, family 003). Seat C = decorrelated computational
instrument (exact arithmetic, independent of the Lean). All scripts/outputs: `/tmp/oaimath/003/seats/C_work/`.

STATUS: FINAL (2026-10-26 ~10:20Z). All batches complete; every number below is from the saved JSON/logs in C_work/runs/.

## 1. Verdicts
| Item | Verdict |
|---|---|
| **Lemma 7** (p.7, eq. (5.5)) | **CONSISTENT WITH THE CLAIM on all tested cases.** 0 violations in 188 (field, N, H, tie-break, admissible p) cases with E_p>0 (d ∈ {−1,−3,5,−7,13,3,−5}, N=2,3 all H∈{1,2,3,5,8} × 2 tie-breaks; N=4 six runs, H=2..6). The bound is **attained** (v_p(Δ)=E_p exactly) in 91/188 cases, so it is sharp and an off-by-one overclaim would have been refuted. The check is discriminating: it fails where the paper predicts nothing and fails for deliberately broken constructions (§3). |
| **Lemma 3 / Cor 4** (pp.3–5) | **CONSISTENT WITH THE CLAIM; for N=2 and N=3 verified for EVERY box satisfying (3.1), all 7 fields** (each such box contains the corner box (3(N−1),3(N−1),3(N−1)), which is certified surjective; surjectivity is monotone in the box). No counterexample possible at these N. Hypothesis is genuinely used: a deliberately Q-dependent kernel gives a (3.1)-box with rank 75 < 81 (§4). |
| **Lemma 6** (p.6, eq. (4.4)) | **CONSISTENT WITH THE CLAIM** (stated inequalities hold with enormous room at every tested size, including small N where the lemma is not asserted). Observed H·S2/S1 ∈ [0.66, 1.66] for the `lex` tie-break (up to 3.86 for `rev` at H=1; ≤2.01 for H≥2), i.e. S2/S1 ≈ 1–2/H, matching the lemma's S2/S1 = O(1/H) scaling (the lemma's constant C0/c0 ≈ 7.2·10^6 is very loose). |

No counterexample found. No objection to file in my scope.

## 2. Construction (exactly as §4 of the paper)
- R = Z[a,b], a²=d, b²=2, elements as integer 4-tuples in basis 1,a,b,ab (`biq.py`). σ: a↦−a, τ: b↦−b.
- E_N = {0..N−1}⁴ (columns in lexicographic order), θ_n = n1+n2a+n3b+n4ab, rows R_α (4.2) =
  (θ_n^{α1} σ(θ_n)^{α2} στ(θ_n)^{α3})_n.
- Candidates α ∈ N³ by increasing w(α)=α1+H(α2+α3); tie-break `lex` (α1 descending) or `rev` (α1 ascending).
- Greedy retention over K: decided modulo a prime of K above each of 3 independent split primes p≈2³¹ (all three must agree —
  they always did), then **certified exactly**: for every gap between consecutive retained rows, the skipped rows are shown to lie in
  the K-span of the earlier retained rows by an exact Q-rank computation (python-flint `fmpz_mat.rank`) of the regular
  representation (Q-rank = 4·K-rank). Every run below has exact certification = True.
- Δ = det(R_α)_{α∈P} ∈ R computed EXACTLY by multimodular CRT over split primes p≈2⁶² (the four embeddings R→F_p give the four
  conjugates of Δ mod p, solved for the 4 coordinates), with enough primes to exceed 2⁶⁴× the Hadamard bound on |coordinates|;
  checks: reconstruction stable when the last 2 primes are dropped, and agreement at a fresh prime not used in the CRT. Δ ≠ 0 always.
- v_p(Δ) := min over the 4 coordinates of v_p (= largest e with Δ ∈ p^e R). E_p = Σ_{α∈P} ⌊α1/p⌋.
- Nm(Δ) = Δ·σΔ·τΔ·στΔ computed exactly; asserted to have zero a,b,ab-coordinates (arithmetic self-check).

Command (per case): `bash -c 'ulimit -v 8000000; exec timeout 1800 nice -n 19 ~/.venv/bin/python3 lemma7.py d N H [variant] [tiebreak] 1 out.json'`
(python-flint lives in `~/.venv`; batches `batch1.sh` (paper variant, 140 runs), `batch2.sh` (controls), `batch3.sh` (N=4).)

### 2a. Lemma 7 results, paper construction
Summary (`summarize.py 'runs/paper_*.json'`, N=2,3, 7 fields × H∈{1,2,3,5,8} × 2 tie-breaks = 140 runs; plus N=4 runs):
- admissible (p>H, p∤2q, (d/p)=−1) pairs with E_p>0: **167 (N≤3, 140 runs) + 21 (N=4, 6 runs) = 188; violations: 0.**
- by class: σ: 0 fail / 71, στ: 0 fail / 117. All 146 runs exact-certified greedy; Δ≠0 in all.
- Π_{admissible p} p^{4E_p} | Nm(Δ): true in every run.
- Tightness: v_p(Δ) − E_p histogram over the 188 cases: slack 0: 91, 1: 43, 2: 14, 3: 3, 4: 3, 5: 3, ≥6: 31.
- N=4 admissible (p, class, E_p, v_p): d=−1,H=3: (7,σ,128,129) (11,στ,51,51) (19,στ,5,6); d=−1,H=6: (7,σ,231,235) (11,στ,115,115)
  (19,στ,35,35) (23,σ,17,17) (31,σ,1,1); d=−3,H=4: (5,στ,254,270) (11,στ,66,66) (17,σ,18,18) (23,σ,3,3); d=−7,H=5:
  (13,στ,66,66) (17,σ,35,35) (19,στ,23,24); d=13,H=2: (5,στ,131,177) (7,σ,69,77) (11,στ,19,27); d=5,H=3: (7,σ,120,121)
  (13,στ,29,29) (17,σ,9,9).

Representative tables (class = Frobenius of p in Gal(K/Q); adm = admissible; Lext = my extended prediction, §3c):

d=−1, N=4 (M=256), H=3, lex — S1=1546, S2=738, max α=(22,6,7), certified, log10|NmΔ|=4821.3
```
   p   class  adm   E_p   v_p  Lext  v_p(Nm)  E_p<=v_p
   2     ram    F   713  2067     0     8268  True
   3  sigtau    F   438   593    73     2372  True     (p<=H: not claimed)
   5     tau    F   218    67    22      268  False    (tau class: not claimed)
   7   sigma    T   128   129   128      516  True
  11  sigtau    T    51    51    51      204  True     <- equality
  13     tau    F    33     0     0        0  False    (tau class: not claimed)
  17      id    F    11    21    11       84  True
  19  sigtau    T     5     6     5       24  True
```
d=−1, N=3 (M=81), H=5, lex — S1=443, S2=107
```
   3  sigtau    F   124   109     4      436  False    (p<=H: claim would FAIL; condition p>H is needed)
   5     tau    F    61     8     0       32  False
   7   sigma    T    33    33    33      132  True     <- equality
  11  sigtau    T    14    14    14       56  True     <- equality
  13     tau    F     8     0     0        0  False
  17      id    F     2     8     2       32  True
```
d=13, N=3, H=3, lex — S1=321, S2=135
```
   3     tau    F    84    45    12      180  False
   5  sigtau    T    37    46    37      184  True
   7   sigma    T    19    22    19       88  True
  11  sigtau    T     4    10     4       40  True
  13     ram    F     2    82     0      328  True
```

## 3. Controls for Lemma 7 (each must be able to fail — they do)
(a) **τ-class primes** ((d/p)=+1, (2/p)=−1; paper predicts nothing for the first coordinate): "v_p ≥ E_p" FAILS in 84 of 93 (run,p)
    cases with E_p>0 (N≤3, paper variant) and 11 of 12 at N=4. So the instrument is not trivially satisfied (Δ is not just very smooth).
(b) **σ/στ primes with p ≤ H** (weight would rise when θ^p → g_p(θ)): "v_p ≥ E_p" FAILS in 56 of 84 cases (N≤3; 2 of 5 at N=4) — the hypothesis p>H is
    load-bearing, as the proof says.
(c) **Broken constructions** (same code, one ingredient changed; 56 runs each: 7 fields × N∈{2,3} × H∈{1,2,3,5}), admissible
    pairs with E_p>0, failures by class:
    - `tau`: slot 2 = τ(θ) instead of σ(θ) (wrong conjugate): σ-class 27 fail / 29, στ-class 0 / 46; Π p^{4E_p} ∤ Nm(Δ) in 25/56 runs.
    - `permslot2`: slot 2 = σ(θ_{π(n)}) with π a shift of n2 (points perturbed in one slot): σ-class 25 / 29, στ-class 0 / 50;
      norm-product check fails in 23/56 runs.
    Failures occur exactly in the class whose Frobenius target is no longer a row coordinate, never in the class whose target is
    intact — precisely what the proof mechanism predicts.
    - relabelled/positive variants `swap` (slots 2,3 exchanged) and `wrong2` (slot 2 = σθ+1, an affine function of σθ, so the
      replacement rows are still lower-weight rows): 0 failures in 75 + 75 admissible pairs, as the argument predicts.
      (`swap` shows 7 'Lext' mismatches only because my extended-prediction formula is hard-coded to the paper's slot order.)
(d) **Same mechanism, stronger predictions (my derivation; outside the paper's claim):** the proof's replacement trick also works
    (i) for identity-Frobenius primes (θ^p ≡ θ, weight drops by m(p−1)) — tested: 0 fail / 46 (N≤4); and (ii) on the 2nd/3rd slot
    ((σθ)^p ≡ g_pσ(θ) whenever that is a slot), giving Lext_p = Σ c1⌊α1/p⌋+c2⌊α2/p⌋+c3⌊α3/p⌋. Lext ≤ v_p held in every
    paper-variant case (0 failures). These are consistency checks of the mechanism, not claims of the paper.
    Unconditional sanity check (by hand): with all valid extractions, the generic forced divisibility per unit of α1 is
    (3/4)·log U = log N (Chebotarev 3/4 = log N/log U), equal to — not larger than — the Hadamard size per unit degree, so the
    paper's algebra does not prove a falsehood unconditionally at leading order; the Siegel hypothesis is what moves the
    {σ,στ}-mass from 1/2 to ≈1. Consistent with Theorem 1's mechanism as described on p.2.

## 4. Lemma 3 / Corollary 4
Script `lemma3.py` (rank of {R_α : α ≤ t} = rank of B ↦ (B(An))_n on the box; rank mod a prime of K is a LOWER bound for the
rank over K = rank over C, so rank M mod p certifies surjectivity).
- Boxes named in the brief: N=2, t=(11,11,11): rank 16=M for all 7 fields. (3.1) holds.
- **Complete check for N=2,3**: every (3.1)-box contains the corner box c=(3(N−1),3(N−1),3(N−1)). Box (3,3,3) (N=2) and (6,6,6)
  (N=3) are certified surjective for d ∈ {−1,−3,5,−7,13,3,−5} (and also for the Q-dependent d=2,4,8). By monotonicity Lemma 3's
  conclusion holds for **all** (3.1)-boxes at N=2,3 for these A. (`l3_cornerboxes.txt`)
- Room left by (3.1) — least t1 making (t1,t2,t3) surjective (d=−1; d=5 identical at N=3):
  N=2 (M=16): (15,0,0), (7,1,0), (5,1,1), (2,3,1), (1,2,2) …; cube t=2 suffices; (3.1) needs t≥11 per coordinate (cube).
  N=3 (M=81): (80,0,0), (40,1,0), (20,1,1), (9,2,2), (5,3,3), (3,4,4), (1,7,7)…; cube t=4 suffices (t=3 does not); (3.1) needs 24.
  (d=5 at N=3: same table except 3 entries smaller by 1, e.g. (8,2,2).)
  Minimal boxes are close to the dimension count ∏(t_j+1) ≥ M but not equal to it (e.g. N=2 (3,1,1) and (4,1,1) fail despite
  16, 20 ≥ 16 monomials) — the point set is special, but (3.1) has a large safety margin at these N. Tables: `l3_minbox_*`.
- Unbalanced (3.1)-boxes, e.g. N=3 (87,6,87): surjective for d=−1 (also implied by the corner argument).
- **Negative controls (the rank code can report failure):**
  (i) rational A=[[1,0,0,1],[0,1,0,1],[0,0,1,1]], kernel (1,1,1,−1) (Q-dependent, rational): points collide; rank 15<16 (N=2,
      box (11,11,11)) and 65<81 (N=3, box (24,24,24)) at 3 primes; both boxes satisfy (3.1).
  (ii) `qdep`: A=[[u,1,1,0],[v,x,y,w],[1,0,0,0]] with generic u,v,x,y,w, kernel (0,1,−1,(y−x)/w) (first coordinate 0 ⇒
      Q-dependent, points still distinct). N=3, box (87,6,87) satisfies (3.1) but rank = 75 < 81; (87,7,87): 78; (87,8,87): 81.
      This matches the exact structural count: on each of the 3 planes z3=n1, the 9 points with n2+n3=2 have constant z1 and z3,
      so only the 7 (resp. 8) powers of z2 act there ⇒ deficit 2 (resp. 1) per plane. So the Q-independence hypothesis is used
      (it excludes exactly this: in the proof, r=(1,0,0,0) gives r·c=0 and A|_H is not injective).
  (iii) The paper's Q-dependent "d perfect square / d=2m²" cases (d=4, 2, 8) did NOT fail at N=2,3 — the hypothesis is
      sufficient, not necessary, at these sizes.
- Reading: I re-derived the proof of Lemma 3 line by line (counting (3.3), nearest-point/face step (3.4)–(3.5), Lagrange
  interpolation on the face, final contradiction) and found no gap.

## 5. Lemma 6
`lemma6.py` over the retained sets (full table in `lemma6_table.txt`): with c0=(4·97²)⁻¹, C0=192, every run satisfies
S1 ≥ c0·M·H^{2/3}U, S2 ≤ C0·M·H^{−1/3}U and max weight ≤ 96H^{2/3}U (the last is a Cor-4 consequence, asserted only for H ≤ N),
by 1–4 orders of magnitude. E.g. N=3, H=8: S1=624 vs 0.04; S2=80 vs 33,645; max weight 24 vs 1,661.
Observed H·S2/S1: N=3: 1.39, 1.53, 1.12, 1.21, 1.03 for H=1,2,3,5,8 (d=−1, lex); N=4: 1.43–1.66 over the six runs. A simplex model of the
retained set (α1+H(α2+α3) ≤ W, volume = M) predicts S2/S1 → 2/H and mean α1 ≈ 0.45·H^{2/3}U; data are in that regime.
Not over-interpreted: the lemma is asymptotic in N.

## 6. What I could NOT check
- Asymptotic regime: N ≤ 4 only (M ≤ 256); U ≤ 6.35, so only primes ≤ 31 carry E_p>0 at admissible p. Lemma 7 is an exact algebraic identity
  (no asymptotics), so small cases test its mechanism fully; Lemma 3 at N≥4 and Lemma 6's asymptotics are not tested.
- Lemma 2 / §6 parameter bookkeeping are outside my brief (I re-read them; no objection, but not computationally tested).
- The Lean development and the statement/definition audit (other seats).

## 7. Where a hole would most likely hide in my scope, and whether it does
The load-bearing algebra is Lemma 7: the replacement row θ^r(θ^p−g_p(θ))^k must (i) have all entries in p^kR, (ii) differ from
R_α by rows of STRICTLY smaller weight (so tie-breaks cannot matter), and (iii) those rows must lie in the K-span of retained rows
preceding α, so the change of basis is unitriangular over K and the determinant is unchanged without any integrality of L.
All three hold on reading (weight drop m(p−H)>0 needs p>H; (i) is the Frobenius relation in R/pR, valid for any θ∈R), and the
computation confirms it with zero exceptions, frequent equality, and failures exactly where (ii) or the slot/Frobenius match is
broken. Lemma 3's danger would be unbalanced boxes or a non-injective face projection; the corner-box argument rules out any
failure at N=2,3 and the proof's use of Q-independence is exactly where the `qdep` control breaks. I found no hole in my scope.

## 8. Housekeeping / rule disclosure
- A backgrounded `cd … && nohup … &` ran a follow-on command from the wrong cwd and created two error-only files
  (`l3_minbox_d5_N3.txt`, `l3_negctl_N2.txt`, each a one-line "can't open file" message) in /home/exedev/MathDyad/ at 09:34Z;
  I deleted both within a minute and re-ran from C_work. Nothing else was written outside C_work/ and this report.
- `batch2.sh` was wrapped in `timeout 3000` (each inner python call is seconds; total ~25 min) rather than 1800; every other script
  ran under `ulimit -v 8000000; timeout 1800 nice -n 19`. No processes of mine remain running.
