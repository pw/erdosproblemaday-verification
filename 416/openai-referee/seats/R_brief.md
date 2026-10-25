# Seat R — refute OUR claims (erdosproblemaday.com, #416, 2026-10-21)
Read COMMON.md for context (OpenAI's paper, files). This seat does NOT referee OpenAI's paper; it attacks what WE (the site) are about to
publish as our own contribution. Be hostile. Quote the claim you object to. Work in /tmp/oaimath/024/seats/R_work/. Report to R_report.md
(first line: REFUTED / GAP / HOLDS AS READ, then numbered findings with severity). ≤ 8 GB, ≤ 30 min per job, ≤ 2 cores, no sub-agents.

## Claim 1 (label (b), modulo OpenAI's Theorem 2.1): the phase coefficient A(1; s) is not constant; sup A / inf A ≥ λ/γ ≈ 1.8902.
Argument as we state it: with B = log log x, ψ(B) = (log B − log log B)/λ, m = ⌊ψ⌋, θ = ψ − m, G_j = B^j/(j! g_1⋯g_j).
Theorem 2.1: V(x) ~ (x/log x) G_m A(θ) and V(cx)/V(x) → c. For large integer M let y_M solve ψ(B(y_M)) = M. Fix c > 1 and put
x = y_M/√c, x' = √c·y_M. Then m(x) = M−1, m(x') = M, θ(x) → 1⁻, θ(x') → 0⁺ (because ψ(B(c^{±1/2} y)) − ψ(B(y)) → 0).
V(x')/V(x) → c. The main-term ratio is (x'/log x')/(x/log x) · G_M(B')/G_{M−1}(B) · A(θ')/A(θ) with B' = B(x') = B + O(1/log x).
G_M(B')/G_{M−1}(B) = B'^M/(B^{M−1} M g_M) = (1+o(1))·B/(M g_M) (since M = O(log B) ≪ log x). At ψ(B) = M: B = e^{λM}·log B;
g_M = γρ^{−M}(1+o(1)) = γe^{λM}(1+o(1)) (Ford's (3.5)); so B/(M g_M) → (log B)/(Mγ) → λ/γ. Hence A(θ(x'))/A(θ(x)) → γ/λ along
this sequence, and since c₋ ≤ A ≤ c₊: inf A ≤ A(θ') = (γ/λ + o(1))A(θ) ≤ (γ/λ + o(1)) sup A, so sup A/inf A ≥ λ/γ.
Numerics we cite: λ = 0.61138548455047…, γ = 0.32345753419138…, λ/γ = 1.89015688281582; G_{m+1}/G_m at the exact wrap point =
2.018 (m=100), 1.910 (m=1000), 1.901 (m=2000) — script ~/MathDyad/erdos416/wrap.py, output wrap.out.
Attack: is any step wrong (direction of the jump, use of x vs x/c in the paper's own Prop 6.1, whether θ and m are as defined in the
Lean (Lean: m x = ⌊psi (B x)⌋₊ with Nat.floor), whether A could fail to be measurable/whatever and break inf/sup, whether "sup/inf" is
the right conclusion vs. "A(1⁻) and A(0) differ")? Also: is this remark trivial or already in the paper (search paper.txt)?

## Claim 2 (label (d)): our census. Files in ~/MathDyad/erdos416/ (vdfs.c route A DFS, vsieve.c route B φ-sieve, vdfs2.c threshold
seed search, invphi.py route C divisor recursion, analyze.py/analyze.out, seeds9.out, runs/SHA256_bigfiles.txt). Claims: V(10^6..10^9)
= 180,184 / 1,634,372 / 15,037,909 / 139,847,905; V(2x)/V(x) values in analyze.out; route A and B ℓ arrays to 10^8 byte-identical;
smallest d with ℓ(d) > 2d is 5888 (ℓ = 11985 = 3·5·17·47); 133 such d ≤ 10^8; max ℓ(d)/d for d ≤ 10^9 is 2.043447 at d = 387,383,296;
every totient ≤ 10^9 has a preimage ≤ 2.5d. Attack the CODE: overflow (v*(p−1) in uint64? n up to ~6.6e9 fits?), the DFS
completeness (does it generate every n with φ(n) ≤ N? prime powers? φ(1)=φ(2)=1?), the sieve bound n ≤ 6.6N (is Rosser–Schoenfeld
applied correctly at n < 3 and is 6.55 right for n ≤ 1e10?), the threshold comparison done in double precision (n ≤ t·v with t=2.0414:
could rounding flip a case? at t=2.5? at t = 2 in the control?), off-by-one at the endpoints. Re-run small cases yourself (≤ 10^7) with
an independent brute force and compare. Do NOT rerun the 10^9 jobs.

## Claim 3: the bridge /tmp/oaimath/024/bridge/Bridge416.lean is a VERBATIM copy of FC's statements (FC_416.lean @ 32ac619d) and the
proof of V_eq is about the right objects. Read both files; check that nothing in our copy changes meaning (binder names, open scopes,
`abbrev` vs `def`, `𝓝`, coercions). Do not build Lean; we compile it separately.
