# R3 report — scope §6–§8 (printed pp. 45–74)

STATUS: COMPLETE (2026-10-23). Equation numbers below are the PRINTED ones (paper.pdf).

## 1. VERDICT for §§6–8: HOLDS AS READ

I found no FATAL and no GAP in §§6–8. I read every lemma line by line and re-derived each load-bearing display
by hand. The algebraic identities in §6 were also checked numerically, each with a perturbed control that
fails (see §3). The remarks below are exposition only. The few things I could not check are listed in §4.

## 2. Objections

None at severity FATAL, GAP or FIXABLE.

EXPOSITION-1 (Lemma 8.1 statement, p. 66): the lemma says *"There is at most one primitive real character
\(\chi_*\), with conductor at most \(\exp(\exp(\mu L))\), and one associated real zero \(\beta_*<1\) which must be
retained in the following formula."* The statement never defines which zero counts as exceptional. The
definition is in the proof: a zero with \(1-\beta_*<c_0e^{-\theta L}\) for \(Q=\exp(e^{\mu L})\), \(S=\exp(e^{\theta L})\)
(eq. (8.9)). Read with the proof the lemma is correct, but the statement alone does not
determine \(\chi_*\). Fix: put "the exceptional zero (if any) of the Landau–Page region \(\sigma>1-c_0e^{-\theta L}\),
\(|t|\le S\), conductors \(\le Q\)" into the statement.

EXPOSITION-2 (proof of (7.2), p. 56): *"Replacing \((\log p)/p\) by \(1/p\) in this cell does not change
this conclusion: the log coordinate has relative variation \(o(1)\), and the same error bound applies."*
This is true, but the test \(\widetilde F_p\) is not pointwise bounded. The step therefore needs the
Cauchy–Schwarz bound \(\sum_{\rm cell}\varphi(\log p-n)p^{-1}|{\rm err}_p|\ll (L/n)^{1/2}\cdot n^{-1/2}\), together
with \(|\E_{S_p}\widetilde F_p|\le\sqrt3\). The paper leaves this implicit. I reconstructed it and it works.

## 3. What I checked and how

**§6, Lemma 6.1 (tree comparison) — read in full; holds.**
- **Density bound (6.3).** \(H_{n,-}/H_{n,+}=\)const\(\cdot M_n/M_{n,+}^2\). The ratio and the difference fix the
  child pair, so each split costs \(\le2/(q-1)\) and the total density is \(\le2^{r-1}\). Exact enumeration at
  depth 2 (r=4), q=7,11,13 gives maximum multiplicity exactly 8 = \(2^{r-1}\): the bound is sharp. The
  control "\(\le2^{r-2}\)" is violated, so the check can fail. The bound is an integral of
  \(|g|^2\)-products; no sup bound on \(g\) is used.
- **Consistency of (6.2).** \(C_{c,+}C_{c,-}=u_nC_{n,\pm}\) is equivalent to the child's own \(y\)-formula.
  Verified algebraically, and numerically over \(\F_{1000003}\) (2000 random trials, 0 failures).
- **Cycle reduction.** Each graph has \(b+r/4\le r\) vertices and \(r\) edges, so it has a cycle. The cycle is
  even because the graph is bipartite. The alternating \(z^{\pm1}\) action preserves every component product
  and every quartet product, and is measure-preserving on the fibres. So
  \(\E(W_1|\mathcal T)=\E(\mathcal PW_1|\mathcal T)\). Conditional Cauchy–Schwarz plus (6.3) applied to the
  marginal of diagram 2 gives (6.6). Correct.
- **Bottom-pair estimates.**
  - \(P_\chi(d)\) is exactly the Mellin coefficient of \(h(d,\cdot)\). Numerically, error \(10^{-14}\); the
    wrong-shift control is off by \(0.8\)–\(0.9\).
  - \(w_\chi(a)=\frac q{q-1}|\widehat{g_*\bar\chi}(\sigma a)|^2\): error \(10^{-16}\); the wrong-sign control is
    off by \(0.15\)–\(0.34\).
  - \(\max w\le\frac q{q-1}\eps^2\) holds, with equality attained.
  - \(\sum_\chi r_\chi\le 2q/(q-1)\): measured 1.79 against bound 2.07.
- **Uniform Mellin estimate (6.14).**
  - Parametrisation \(x=z^2/(z-\sigma/\lambda)\), \(d=z/(\lambda z-\sigma)\), \(1/x=r'-tr'^2\): re-derived.
  - Representation count: \(U_r^*U_s\) is \(t\mapsto (s/r)^2t+s-s^2/r\). A nonidentity map has \(\le2\)
    representations because the identity arises only from \(z=1\) (\(z=-1\) gives \(b=-2r\ne0\) for odd q).
  - Hilbert–Schmidt bound \(\le\sqrt{3/q}\) on the mean-zero space. Constant part: \(T1=\overline{m_G}\).
  - The identity "LHS = \(\E_\lambda|\E_dh(d,\lambda d)\eta(d)e(-ad)|^2\)" holds to \(10^{-16}\) at q=13,31,
    for all \(\eta,a\), both \(\sigma\), \(g\) and \(\bar g\). The control parametrisation \(t=\lambda/d\)
    breaks it.
  - The bound holds; at q=31 the largest ratio LHS/bound was 0.11. The test \(g\) was deliberately spiky
    (one value scaled ×8, log-normal moduli).
- **Quartet majorants.**
  - Same-pair case, and the formulas (6.18) and (6.19): verified symbolically and
    numerically. The exponent-1 control never matches.
  - Friendly/bad parametrisation, and all four rows of the twist table: re-derived from
    \(h_L(d,\lambda_Ld)\), \(h_L(d,\lambda_L/e)\), etc.
  - Convolution Parseval \(\E_y|q^{-1}\sum_dF(d)G(d-y)|^2=\sum_a|\hat F(a)|^2|\hat G(-a)|^2\): checked.
  - Two-bad case:
    - Gauss modulus \(q^{-1/2}\), and \(\hat\alpha(0)=0\).
    - 4th-moment count: equal pairs give \(\le2qr_w^2\); unequal pairs give a degree-\(\le1\) polynomial in
      \(a\), so total \(\le J^4\). Verified numerically at q=11,13,17,19 (ratios 0.52–0.67). The too-strong
      control bound \(qr_w^2+J^4/2\) fails.
    - Principal subtraction \((J-w)^4\ge J^4-4J^3w\).
    - Principal cases.
- **Completion.** Held variables are independent across quartets, conditional on the quartet products. The
  quartet-root arguments are dominated by \(C_l\times\)uniform. One character is fixed by the cycle
  relation, giving \(\sup b_\rho(\sum b_\rho)^{t-1}b_0^{r/4-t}\). The 2-cycle (\(t=1\), principal \(\rho\)) is
  covered because \(\eps_q\) includes the principal character with all \(a\).
- **Hypotheses.** The proof uses only \(g(0)=0\), \(\E|g|^2\le1\) and \(\eps_q\to0\); no boundedness or
  uniformity of \(g\) enters anywhere.
- **Match with Corollary 4.2.** \(g_p(0)=\sqrt p\,\E F_p=0\); \(\E|g_p|^2=\E|F_p|^2=1\). Cor 4.2's maximum runs
  over all \(a\) and all multiplicative \(\lambda\), principal included. That is literally \(\eps_q\) of
  (6.1). On the spectator subset it holds uniformly, so it applies at every spectator, not on average.

**§7 — read in full; holds.**
- **(7.2).** Block selection from (5.1): \(\sum ch/u\approx .85cL<.15L\). The collision error
  \(\sum(\log p/p)|{\rm err}_p|^2\ll\log\log X=O(L)\) gives \(O(\sqrt{Lh})=o(h)\). Cell selection uses the
  partition of unity. Unfavourable primes have \(\widetilde F_p\equiv0\).
- **Positivity.**
  - The statistic \(I=\sum\psi(n/X)T(n)^2\) is nonnegative TERMWISE: \(T(n)\) is real because \(F_p\) and
    \(\widetilde F_p\) are real.
  - The lower bound restricts to \(n\in A'\). There, every nongiant exact test equals
    \(\sqrt{(1-\sigma_p)/\sigma_p}>0\), using \(a>p+N_*\): all nongiant primes have
    \(\log p\ll 2^kh<\tfrac9{10}\log X\).
  - So \(T(a)=c_L\E_{\mu_G}\widetilde F_p(a)\). With Jensen, \(I\ge\sqrt Xe^{-Cm}\). Here \(C\) is independent
    of \(k\): only \(O(k)\) cell positions, and \(|A'|\) loses only \(e^{O(L)}\).
- **Repeated primes.**
  - \(Q=o(X)\), because the smallest prime exceeds \(\exp(\exp(.0005L))\gg\Delta_0\).
  - The residue mean is 0 if some prime is a singleton, and \(\le p^{e/2-1}\) otherwise.
  - \(\prod p^{e_p/2-1}=M^{1/2}/Q\).
  - \(b^bL^{-2m}=\exp(2m\log(2z)+o_k(m))\), so the bound \(\sqrt X\exp(-\Delta_0/2+(2\log z+C)m)\) is right.
  - \(B_*\) is independent of \(B_D\), \(B_z\) and \(k\).
- **Poisson formula (7.9).** Re-derived. CRT gives \(G_M(s)=G_R(s/d)\prod_qg_q(s/((d/q)R))\). The \(s=0\)
  term vanishes. \(|s|\le cM/X\le V_0\).
- **Transfer.**
  - \(G_{PH}(v/d)=G_P(t/d)G_H(v/(Pd))\).
  - Row norm \(\le P\), by CRT and \(\sum_x|g|^2\le\ell\).
  - \(p\mu_G(p)=e^{c_g}\varphi\); extension to integers keeps nonnegative terms.
  - Off-diagonal substitution \(s=(vH_--wH_+)/(pu)\) is one-to-one, with \(\log|s|<E_j\) and margin
    \(2^{j-1}\sqrt m\).
  - \(H_+\) and \(H_-\) share no prime: a shared prime would divide \(s\), but it exceeds \(|s|\). This
    includes the giants.
  - At \(\ell\mid H_-\): \(-w/P\equiv s/H_+\); with \(g(-b)=\overline{g(b)}\) this gives exactly
    \(G_{H_+H_-}(s/d)\).
  - Diagonal \(vH_-=wH_+\Rightarrow H_+=H_-,\ v=w\). Grouping before expanding gives \(\sum_h|G_h|^2|S_h|^2\ge0\).
    Dropping the giant factor \(|\tilde g|^2\le1\) is legitimate in a nonnegative sum.
  - Counterpart mass: \(C_H\le L^{-r_jm}e^{Cr_jm}\), with cell costs \(e^{O(kr_jL)}\subset e^{Cr_jm}\).
  - \(e^{-T_H+G+r_jw_j}=e^{-\Delta_j}\).
  - The \(J/w_j\) recursion gives \(J+\sum w_j=2^kJ-\sum\Delta_j\), so \(\log M=\log X+\Delta_0+O_k(1)\).
    Checked by telescoping \(T_j=2T_{j+1}-\Delta_j/r_j\).
  - Disjointness of the ±3% neighbourhoods: checked.

**§8 — read in full; holds.**
- **Support descent.**
  - \(N\) is a unit at every prime of \(H_\pm\), so \(p\) and \(u\) are automatically coprime to the inherited
    slots.
  - The remaining tests (\(s\mid N\) mod \(Q_f\); \(b\,\|\,N\); units mod \(c_{\rm sm}d\); the zero convention
    at spectators) are exhaustive.
  - The precision \(Q_f=R_f^{k+2}\) is enough.
- **Lemma 8.1 (prime progressions).** The statement used is the uniform Landau–Page theorem: for conductors
  \(\le Q\) and \(|t|\le S\), at most one exceptional zero, real and simple, of a real primitive character.
  This is standard; see Iwaniec–Kowalski Thm 5.28 and Davenport Ch. 14. Re-derived:
  - The explicit-formula error budget: low zeros give \(\exp(-ce^{(a_0-\theta)L}+e^{\theta L})\), which needs
    \(a_0-\theta>\theta\). Giant row: .027 > .022. Bulk row: .0021 > .0018.
  - High zeros \(\ll\exp(C_je^{\delta'L}-(j-1)e^{\theta L})\), using \(\theta>\delta'\).
  - The residue at the shifted contour, using \(a_0>\delta'\).
  - Moduli range: \(\log M_*\le e^{.012L}\) (giant) and \(\log(dQ_f)<e^{.0012L}\) (bulk). These are within
    each row's \(\mu\) (\(Q=\exp(e^{\mu L})\)) and far beyond Siegel–Walfisz. That is exactly why Page's
    theorem is used.
  - The absolute error \(\exp(-ce^{\delta'L})\) is below the main term \(1/\phi(M_*)\ge\exp(-e^{\mu L})\),
    since \(\delta'>\mu\), and stays negligible after summing over all classes and boxes.
  - The exceptional density factor \(1-\chi_*(a)e^{(\beta_*-1)t}\in[0,2]\).
  - **No step uses an ineffective constant.** Siegel's theorem is never invoked; the exceptional zero is
    retained rather than bounded.
- **Exceptional character, every case.** For each row there is at most one \(\chi_*\), fixed from \(L\) alone,
  before the nongiant priors.
  - (i) The conductor has a prime factor \(\ge T_*=\exp(e^{.0004L})\). One such prime is deleted from every
    nongiant prior. Every prime of \(c_{\rm sm}\), \(d\) and the \(b\)'s comes from a nongiant prior, and all
    such primes are \(\ge\exp(e^{.0005L})>T_*\). So the conductor cannot divide \(M_*\) or \(dQ_f\), and no
    exceptional term appears.
  - (ii) All conductor primes are \(<T_*\). Then the conductor divides \(M_*\) only if it divides \(Q_f\),
    since all \(Q_f\) primes are \(\le e^{O_k(m)}<T_*\). The correction then depends only on the real
    coordinate and the \(Q_f\) residue.
  - (iii) Otherwise the term is absent.
  - In every case the spectator (mod \(d\)) bulk residues remain exact independent Haar units. Downstream,
    only \(0\le\)factor\(\le2\) is used: absolute values in (7.18), and domination in (7.17). No lower bound
    on the corrected density is ever needed.
  - So every possible exceptional modulus is covered, not just the generic one.
- **Integration at the small primes.**
  - Giant coordinates mod \(c_{\rm sm}\): (8.18) \(=\prod_{\ell|u_{\rm out}}(1-1/\ell)\le1\). This uses only
    \(g(0)=0\) and \(\E|g|^2=1\).
  - Internal \(b\): the forms are nonzero, because the ancestor substitution matrices have unit determinants
    \(-vC_-M_-/(su)\) and \(-wC_+M_+/(su)\) mod \(b\) and \(b^2\). Line probabilities are \(1/(b-1)\), \(1/b\)
    or 0.
  - Repeated internal labels: \(b^{n_b}\prod\mu_i\le2\mu_1e^{C(n_b-1)L}\), hence \(e^{CkrL}\). This is
    harmless because \(kL\asymp m/k^3\), so it is absorbed in an absolute \(Crm\).
  - Symbolic replacement: the max-atom Schwartz–Zippel step is re-derived. \(b\) is independent of the
    polynomial, which contains no variable of \(b\)'s type.
  - Dropping distinctness of the bulk samples: checked.
- **Joint idealisations.** Giant mesh \(e^{-e^{.015L}}\), error \(e^{-e^{.013L}}\). Bulk mesh
  \(e^{-e^{.0014L}}\), error \(e^{-e^{.00125L}}\). Box and class counts, and pointwise costs including the
  spectator bound \(e^{O_k(me^{.001L})}\), all checked.
- **Signed comparison (7.18).**
  - The overlap-graph homomorphism maps onto exactly the "equal products per component" subgroup, via the
    spanning-tree argument. This matches the hypothesis of Lemma 6.1, with \(b\) = number of components.
  - All tree constants are units mod \(q\). The ancestor/child relations are those of (6.2): the child
    current entries are \((p,X_\pm)\), and the consistency relation holds.
  - Bottom sibling pairs have opposite conjugations, since the recursion conjugates the right child.
  - So the per-spectator bound is \(C_l(\eps+q^{-1/4})\), and CRT gives \(\epsilon_k(L)^m\).
- **Norm comparison (7.17).**
  - At each node the congruence forces \((v,s)=(w,s)\) and fixes \(M_+^2\) mod \(a=|s|/(v,w,s)\). This gives at
    most \(2^{\omega+1}\) roots, so probability \(\le e^{o_k(m)}/[a,a']\).
  - \(\sum_{a,a'}1/[a,a']\ll(\log V)^3\), and the multiplicity of \(s\) given \(a\) is \(\le2\tau((v,w))\).
  - The leaves give \((2V_0)^{2r}e^{-r\Delta_0}=e^{r\Delta_0+o_k(m)}\).
  - The constant \(C\) is absolute: \(3^{rm}\), \(2^{rm}\), \(e^{CkrL}\subset e^{Crm/k^3}\).

**Parameter order (§§6–8).**
- §6: depth \(l\) fixed, \(q\to\infty\); \(C_l\) depends only on \(l\).
- §§7–8: \(B_s\) first, which fixes \(B_*\). Then \(B_z\), \(B_D\), then \(k\), with \(z=k^4\) and
  \(m\asymp k^4L\). Finally \(L\to\infty\).
- Every "\(Crm\)" constant I traced is independent of \(k\) and of the gap constants. Every \(k\)-dependent
  loss is \(o_k(m)\) or \(e^{O_k(m)}\), and is beaten by \(\exp(-e^{cL})\) errors or by \(\epsilon_k(L)^m\) at
  fixed \(k\).
- \(E_L\) depends on \(L\) only and is chosen before the priors; no circularity.

**Scripts** are in `R3_work/`: `tree_checks.py`, `quartet_checks.py`, `density_check.py`. All were run under
`ulimit -v 8000000`. Every check has a control that fails.

## 4. What I could NOT check

- The textbook numbering in Montgomery–Vaughan (Thm 11.3, Cor 11.10, Thm 11.16, Cor 11.17/11.20) and
  Helfgott §3.7.3. I have no copy of either source. The mathematical statements used are the standard uniform
  Landau–Page theorem, the explicit formula, and \(N(T,\chi)\ll T\log(q(T+2))\); these say what is claimed.
- The proofs of Proposition 3.1 and Proposition 4.1 behind Corollary 4.2, and Prop 5.1 (5.1). I took their statements as
  given; they are in other seats' scope. I checked only that the statements deliver exactly the hypotheses
  §§6–7 use.
- §9's use of (7.17)/(7.18) in the bad-arrangement count and final symmetrisation (R4's scope). I read only
  the parameter-choice paragraph, to confirm that the \(C\) in (7.17) must be \(k\)-uniform, which it is.
- The Lean. I glanced at its directory: it contains a ZeroDensity / "MainWithoutPage" route, which suggests the
  formal proof may handle progressions differently from the paper. I did not need it, because I found no gap.

## 5. Where a hole would most likely hide

The most likely place is the claim at the start of §8.7 (p. 72): after (8.18), the symbolic replacement of
the line flags, and the bulk idealisation, "the only remaining factor using [the bulk residues mod d] is
(8.5)". The application of Lemma 6.1 needs the leaf products mod each spectator to be
exactly uniform on the component subgroup, independently of everything conditioned on.

Three things could leak into the mod-\(d\) coordinates:
- the exceptional character, through its conductor;
- the internal line conditions, through bulk residues mod \(b\);
- the support conditions.

I traced all three.
- The conductor is kept out of \(d\) by the \(T_*\) deletion.
- The line conditions involve only residues mod \(b\), and the symbolic replacement makes them
  bulk-independent.
- The support descent shows the only mod-\(q\) test is "inserted pivot \(\not\equiv0\)", which is the zero
  convention built into \(W_q\).

I therefore believe this step holds as written.
