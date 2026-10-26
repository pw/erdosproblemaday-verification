# Seat C — exact computation on small cases (read COMMON.md first)

You are the decorrelated COMPUTATIONAL instrument: build the paper's own objects for small parameters with exact arithmetic and test
its algebraic claims directly, independently of the Lean. Language: Python 3 (sympy, mpmath available; check `python3 -c "import
flint"` for python-flint, use it if present). Everything exact (integers / Fractions / arithmetic in R = Z[a,b], a²=d, b²=2, as
4-tuples in the basis 1,a,b,ab). Memory cap per script as in COMMON.md. Save every script and its output in C_work/.

Tasks, in priority order:
(1) Lemma 7 (p.7), the decisive algebra. For several squarefree d (both signs; e.g. d = −1, −3, 5, −7, 13, 3, −5; d ≠ 1, 2) and small
    N, H (start N=2, M=16; then N=3, M=81 if feasible), implement the paper's §4 construction exactly: E_N = {0..N−1}^4,
    θ_n = n1+n2a+n3b+n4ab, rows R_α (4.2) over α ∈ N^3, ordered by w(α)=α1+Hα2+Hα3 with a fixed tie-break, retain a row iff it
    increases the K-span of earlier rows (do the rank tests exactly — over K, or mod a large prime that splits completely in K
    after checking full rank is certified that way; note reduction mod p can only LOWER rank), stop at M retained rows. Compute
    Δ = det(R_α)_{α∈P} exactly in R (coordinates in Z^4). Then for every prime p ≤ some bound:
      E_p = Σ_{α∈P} floor(α1/p) and v_p(Δ) := largest e with all four coordinates of Δ divisible by p^e.
    Paper's claim: v_p(Δ) ≥ E_p for every ADMISSIBLE p (p > H, p ∤ 2q, χ(p) = −1, i.e. (d/p) = −1 for odd p ∤ d).
    Report a table per (d,N,H): p, Frobenius class (σ, στ, τ, id), E_p, v_p(Δ). Controls: (a) primes with Frobenius τ ((d/p)=+1,
    (2/p)=−1) — the paper predicts nothing; report whether v_p ≥ E_p there too (if it ALWAYS holds even where unpredicted, your
    instrument may not be discriminating — investigate, e.g. compare to a Δ built from a deliberately WRONG row order or perturbed
    θ). (b) a deliberately broken variant (e.g. weights that do NOT lower when θ^p → g_p(θ), or using the wrong conjugate for g_p)
    to show the check can fail. Also check the norm: Nm(Δ) ∈ Z, nonzero, and Π p^{4E_p} | Nm(Δ) over admissible p.
(2) Lemma 3 / Corollary 4 (pp.3–5): for the A of (4.1) with several d and N = 2, 3, compute the rank of the evaluation matrix
    (B ↦ (B(An))_{n∈E_N}) on the monomial box deg_{z_j} ≤ t_j for boxes satisfying (3.1) (e.g. N=2: t=(11,11,11); N=3: t=(25,25,25)),
    and also find (roughly) the SMALLEST boxes that are surjective, to see how much room (3.1) leaves. Any (A,t) satisfying the
    lemma's hypotheses with rank < M refutes Lemma 3 — try hard to find one, including unbalanced boxes (t1 large, t2,t3 = 3(N−1)
    + small). Negative control: a linear map whose kernel vector has Q-DEPENDENT coordinates (e.g. rational A, or d a perfect square)
    should fail surjectivity for some box satisfying (3.1) — show it does.
(3) Lemma 6 (p.6): for the retained sets you computed, report S1, S2, M, U and compare with the stated inequalities (note the lemma
    is asymptotic "for N large in terms of H"; report, don't over-interpret, small-N failures).
Report: /tmp/oaimath/003/seats/C_report.md with the tables, the exact commands, and what each control showed. Verdict for each of
Lemma 7 / Lemma 3 / Lemma 6: CONSISTENT WITH THE CLAIM on the tested cases · COUNTEREXAMPLE FOUND (give it in full) · COULD NOT TEST.
