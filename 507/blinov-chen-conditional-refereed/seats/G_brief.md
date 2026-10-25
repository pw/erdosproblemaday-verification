# Seat G — the geometric transfer (Blinov §§5–8; Chen §§3–4)
Read /tmp/oaimath/191b/seats/BRIEF_common.md first. Your report: /tmp/oaimath/191b/seats/G_report.md; work dir G_work/.

The authors claim OpenAI's §§5–8 survive with these parameter changes. Check every USE of each changed parameter in
OpenAI's TeX (grep the sections for H, q, N, w, s, S, h^{100}, h^{26}, etc.) — the failure mode we are hunting is an
inequality in the original that silently relied on the old, lavish sizes.

1. Slab cap: S = {(x,y,Q(x,y)): 0 ≤ x < w, y ∈ F_q}, s = wq, no translate. Is S ⊂ Γ with no three collinear?
   Is the box shape {0..w−1}³ of the original used ANYWHERE beyond the first coordinate (Lemma aux:random-set,
   Prop aux:weights, §7)? Is 0 ∉ V still right? s ≥ q²/(2000H²) and q³/s ≪ qH²?
2. H = 2h (was h²): every use — the short-relation exclusion |x| ≤ H, "a contributing shell satisfies R > H/2",
   Lemma zero:moment's hypothesis R ≥ h, q ≥ 2000H².
3. h⁶ < q ≤ 2h⁶ (was h^100): every inequality in §7 ((zero:equal-additional), (zero:special-rank-two),
   (zero:special-rank-one)) recomputed with q³/s ≪ qh²; τ < q; q ∤ E; Lemma zero:plane surjectivity; anything else.
4. N = (hq)⁴ (was (hq)^10): every use — hq | N, λ3(Λ) ≤ E ≤ h < 4N, Lemma sam:proportional and the first deletion
   term n_r(hq)⁶N^{−3} ≤ r^γ τ^{−1/2}, log(2N) = O(log r), null vectors |x| ≪ N², shell counts.
5. Corollary sam:bad-triple with E[D·1_J] in place of the collision probability (take Lemma orb:tagged-moment as
   given — seat P checks it); the deletion with a_r = r^γ√(N³/τ), γ = ρ/(ρ+1), ρ = 249k+3; recompute EXACTLY (integer
   arithmetic, e.g. python Fractions) β = 42k − (k−1)/2, α = γ + 6β = ρ + γ, η = 2γ/α = 2/(ρ+2) = 1/50,893,237 at
   k = 408,781; the B interval 40000k⁴r⁶ < B ≤ 80000k⁴r⁶; h/τ ≤ 3B = O(r⁶); second term O((log r)² r^{2γ−2}).
6. Interpolation: primes r ≡ 1 (mod 3) in (m, 2m] for all large m (PNT in APs) — enough? r ≥ 37?
7. Chen: N = (hq)⁴/B^{s0}, s0 = 102195 — SMALLER than Blinov's. Check every place where N's size matters with the
   smaller N (N ≥ h; N/(hq) integer; λ3 ≤ 4N; the first term of (B17); anything in the zero-determinant count that
   needs N large relative to q or h). Check his explicit constants (B2)–(B19) at least to the extent of catching a
   WRONG inequality (not merely a loose one), the effective transfer (B19) and the final constant c = 2^{−100ρ}.
   Fetch arXiv:1802.00085 (Bennett–Martin–O'Bryant–Rechnitzer; read the CURRENT version, Theorem 1.2 and (1.10)–(1.11))
   and check that it really gives |θ(x;3,1) − x/2| < x/(160 log x) for x ≥ 8·10⁹ as Chen uses it.
8. Slack and ceiling: is Chen's s0 = 102195 forced by anything, or does his own first-term constraint allow any
   s0 with 3s0 < k − 1 (i.e. s0 ≤ 136,259)? If so, what η results (with γ = ρ/(ρ+1), ρ = 249k + 3 − 9s0)? Is there a
   ceiling for this whole family of arguments when N is chosen optimally (not necessarily a power of B) and γ → 1 —
   my (the coordinator's) claim to refute is: sup η = 2/(246k + 8) = 1/(123k + 4) = 1/50,280,067, not attained.
