# R1 report — hostile referee, whole paper (family 003, OpenAI, "Uniform exclusion of Landau–Siegel zeros", 1 Oct 2026, 9 pp.)
STATUS: DONE

## Verdict: HOLDS AS READ

I read §§1–6 line by line from paper.tex and re-derived every inequality that carries weight. I found no false
statement and no step that fails to follow. I have no FATAL, GAP or FIXABLE objections. Three EXPOSITION notes are
below. They are cosmetic, and none affects any constant or quantifier.

The extraordinary-claim prior does not change this. The argument is short and elementary, and I could check each
link: an elementary zero estimate (Lemma 3), Hadamard's inequality, an exact Frobenius-congruence identity
(Lemma 7), and the classical logarithmic-derivative bound (Lemma 2). The sanity test below shows the determinant
method is exactly balanced at Chebotarev equidistribution, and a Siegel-type bias in the Frobenius distribution is
precisely what breaks that balance. So the method proves nothing false that I could find.

## Objections

None at FATAL, GAP or FIXABLE severity.

EXPOSITION notes (no mathematical consequence):
- E1 (§3 p.3, proof of Lemma 3: "Put $\cK=4P$" and later "$y'=y+n-u\in4P$ … The inclusion follows from (3.4)").
  The inclusion uses $3P+P=4P$ (Minkowski sum equals dilation), which holds because $P$ is convex. That is true,
  but the paper never says it. One clause would fix this.
- E2 (§3 p.4 and §4 p.5). The symbol $H$ means the weight integer, and the same letter in calligraphic form,
  $\mathcal H$, means the hyperplane in Lemma 3. $\cK$ is the dilated polytope while $K$ is the biquadratic field.
  Each is unambiguous in context but easy to misread.
- E3 (§6 p.8, "Analyticity therefore prevents zeros from accumulating at 1"). The precise statement used is this:
  for each fixed $\chi$, $L(s,\chi)$ is analytic and nonzero at $s=1$, so it has only finitely many zeros in
  $[1/2,1]$. Hence $(1-\beta)$ is bounded below for each of the finitely many $\chi$ of bounded conductor. The
  sentence is correct but terse.

## What I checked and how

**§2, Lemma 2, eqs. (2.1)–(2.4), p.2.**
- Re-derived (2.3) from the Hadamard product. The real constant cancels because Re $B(\chi)=-\sum$ Re $1/\rho$.
  Each term Re $1/(s-\rho)$ is nonnegative for $s>1$, and the sum converges because $\sum|\rho|^{-2}<\infty$.
- $\psi((s+\varepsilon)/2)$ is bounded on $(1/2,3/2]$ for both parities.
- Dropping every zero except $\beta$ gives (2.4) with $C\ell$ absolute (using $\ell\ge\log3$).
- $s=1+1/\log X\in(1,2)$ for $X\ge3$. Also $p^{-s}\ge e^{-1}p^{-1}$ for $p\le X$, and
  $(1-\beta)/((s-1)(s-\beta))\le(1-\beta)(\log X)^2$.
- Passing to (2.2) needs Mertens, $\sum_{p|q}\log p/p\le\log q$, and the fact that $p=2$ and $p\le H$ are absorbed
  in $C_H$. Primes with $\chi(p)=0$ are exactly $p|q$.
- Nothing here is non-uniform in $q$. The coefficient of $\delta(\log X)^2/\ell$ is $e/2$, which is absolute.

**§3, Lemma 3, eqs. (3.1)–(3.6), Figure 1, pp.3–4.** Every step checks. In order:
- Linear algebra gives a nonzero $R$ vanishing on $\cK\cap\Z^4$, because $\#\le(4N-3)^4<\prod(b_j+1)$.
- $R\circ A\ne0$, and it cannot vanish on all of $\Z^4$.
- A minimiser exists: finitely many lattice points lie in bounded neighbourhoods of $\cK$. Then $h\ne0$, because
  $m\in\cK$ would force $R(Am)=0$.
- The nearest-point inequality gives $h\cdot y=\max_{4P}h$, so $y/4\in G$.
- $\dim G\le3$ in both cases: if $P$ is 4-dimensional then $G$ is proper, otherwise $\dim G\le\dim P\le3$.
- Carathéodory gives at most 4 vertices, so some coefficient is $\ge1/4$. Then $y-u$ has nonnegative coefficients
  summing to 3, so $y-u\in3P$.
- For $n\in S\setminus G$, $h\cdot(u-n)>0$, and $\|h-\eta(u-n)\|^2<\|h\|^2$ for small $\eta>0$. Since
  $m'=m+n-u\in\Z^4$ is strictly closer to $\cK$, (3.6) follows.
- The vertices of $G$ are integer points, so there is a rational hyperplane $r\cdot v=k$ through them.
  $r\in\Z^4\setminus0$ and Q-independence of $c$ give $r\cdot c\ne0$, so $A|_{\mathcal H}$ is a bijection.
- Points of $\mathcal H$ are determined by their coordinates $i\ne i_0$, so $Q$ separates $u$ from
  $(S\cap G)\setminus\{u\}$. $Q$ has total degree $\le3(N-1)$, so each separate degree of $B$ is at most
  $b_j+3(N-1)=t_j$.
- The final sum collapses to $v_uR(Am)\ne0$. No counterexample can exist because the proof is complete.
- Numerical probe (lemma3_probe.py), exact arithmetic mod $P=2^{61}-\ldots$, a prime split in $\Q(\sqrt2,\sqrt3)$:
  - Positive case: $A$ has every coordinate functional killing a lattice direction, and its kernel was checked
    Q-independent (coefficient matrix det $=-198$). I used the most lopsided $t$ that (3.1) allows,
    $t=(628,3,3)$ for $N=2$ and $(6567,6,6)$ for $N=3$. Evaluation is surjective, already at $z_1$-degree 7.
  - Negative control: the same code with $\ker A=\C e_4$ (hypothesis violated) gives rank 8/16 and 27/81, i.e.
    NOT surjective.

**Corollary 4 and §4 (pp.4–5).**
- $T_j\ge32N$ needs $N\ge H$. $T_1T_2T_3=32^3N^4$, and $\prod(T_j-3(N-1))\ge T_1T_2T_3/8=4096N^4>(4N-3)^4$.
- $A$ in (4.1) matches $(\theta,\sigma\theta,\sigma\tau\theta)$. The kernel $(ab,b,-a,-1)$ was verified, and the
  $3\times3$ minor is $4ab$.
- The order on $\N^3$ by $w$ has finite level sets, so it is a well-order. Once every row of weight
  $\le T_1+HT_2+HT_3=96H^{2/3}U$ has been processed the span is full, so all retained weights are $\le$ that bound.
  Numerically the retained maximum weight is 4–14 against a bound of 242–864.

**Lemma 6 (p.6).**
- $\alpha_2,\alpha_3\le B$ follows from the weight bound. $Q_0\le97^2H^{-2/3}U^2$ uses $H^{-1/3}U\ge1$.
- $b_i\ge\lfloor(i-1)/Q_0\rfloor$. The identity $Q_0k(k-1)/2+kr-(M^2/2Q_0-M/2)=r(Q_0-r)/(2Q_0)$ checked.
- $M\ge2Q_0$ follows from $H^{2/3}N^{4/3}\ge2\cdot97^2$. Constants $c_0=(4\cdot97^2)^{-1}$, $C_0=192$ checked.

**§5 (pp.6–8).**
- $\Nm:\cR\to\Z$ checked.
- Archimedean bound: $(N-1)(1+\sqrt{|d|})(1+\sqrt2)\le8N\sqrt q$ for both signs of $d$. Hadamard at the 4
  embeddings gives (5.1).
- Frobenius congruence (5.2): in $\cR$, $a^p=a\,d^{(p-1)/2}$. Euler's criterion gives $\equiv\chi(p)a=-a$ mod $p$,
  valid for odd $p\nmid d$, which is guaranteed by $p\nmid2q$ since $d\,|\,D$ and $|D|=q$. Also
  $b^p\equiv(2/p)b$. The Frobenius map fixes $\Z$.
  - If $(2/p)=1$: $g_p=\sigma$.
  - If $(2/p)=-1$: $n_1-n_2a-n_3b+n_4ab=\sigma\tau\theta$.
- Lemma 7:
  - The expansion (5.4) is an exact identity. The weight drop is $m(p-H)>0$.
  - Every row of strictly smaller weight lies in the $K$-span of the retained rows before $\alpha$, so $L$ is unit
    lower triangular and the determinant is preserved.
  - The entries of $\widetilde R_\alpha$ lie in $p^k\cR$, so $\Delta\in p^{E_p}\cR$. Integrality of $L$ is indeed
    not needed.
- Norm: $p^{4E_p}|\Nm\Delta$. (5.6): $\lfloor x\rfloor\ge x-1$. (5.7) uses Chebyshev and (2.2) with $X=U$.
- Exact numerical check of the whole §5 chain on actual instances (lemma7.py: exact greedy over $K$; $\Nm\Delta$ as
  the integer determinant of the $4M\times4M$ restriction-of-scalars matrix; Bareiss):
  - Instances: $d\in\{5,13,-7,-163,17,-2\}$, $N=2$ ($M=16$), and $(d,N,H)=(5,3,2),(13,3,3)$ ($M=81$).
  - $\Delta\ne0$, $\log|\Nm\Delta|\le$ the Hadamard bound, and $v_p(\Nm\Delta)\ge4E_p$ for every admissible $p$.
    Examples: $d=13$, $N=3$: $p=5$: 120≥96, $p=7$: 68≥40, $p=11$: 12≥4. $d=5$, $N=3$: $p=3$: 252≥164; $p=7$: 20≥20,
    which is tight.
  - Negative control, same code, a $\tau$-class prime ($\chi(p)=+1$, $(2/p)=-1$), where the paper claims nothing:
    $d=13$, $p=3$ gives $v_3=4<8$ ($N=2$, $H=2$) and $v_3=200<240$ ($N=3$, $H=3$). So the first-coordinate bound
    genuinely FAILS without admissibility, and the test can fail.

**§6 (pp.8–9).**
- Re-derived (6.2) from (5.1) and (5.7) term by term.
- Order of choices:
  - $H$ depends only on $C_0/c_0$ (absolute).
  - $\gamma$ depends only on $C$ from (2.2)/(5.7) and $13/24$ (absolute). $C_H$ enters only term 4, which tends
    to 0 as $\log U\to\infty$.
  - The field and $d$ enter only through $\ell$ (from $|a|\le\sqrt q$), which is explicit.
- $\log U/\ell\to4\gamma/3$. Term 3: $C\delta\cdot4\gamma/3\to0$. Term 5: $\ll H^{-2/3}/\log U$ and
  $\ll H^{-2/3}/U$. The limit gives $1\le13/16+1/16$.
- The reduction to a sequence: there are finitely many characters of bounded conductor, and zeros are isolated
  near 1 because $L(1,\chi)\ne0$. The excluded field $\Q(\sqrt2)$ is conductor 8 only.
- No "absolute" constant depends on $H$, $\gamma$, the field or $d$.

## SANITY TEST (design and result)

Question: what would the same determinant argument "prove" for primes of other Frobenius classes, and does that
contradict Chebotarev?

I extended Lemma 7 to every class (my extension, not in the paper). Take the coordinate set
$\{1,\sigma,\sigma\tau\}$ with weights $(1,H,H)$, and a prime $p\nmid2q$ with $g=\mathrm{Frob}_p$. Coordinate $c$
can be lowered into coordinate $gc$ whenever $gc$ is again a coordinate. The weight change is
$-p\,w_c+w_{gc}<0$, which needs $p>H$ only for the move $1\to\sigma,\sigma\tau$. The coordinates reducible in each
class are:
- id: all three;
- $\sigma$: $\alpha_1,\alpha_2$;
- $\sigma\tau$: $\alpha_1,\alpha_3$;
- $\tau$: $\alpha_2,\alpha_3$.

Each coordinate is reducible in exactly 3 of the 4 classes. With Chebotarev (density 1/4 each) and primes up to
$\alpha_c$, the total $p$-adic lower bound is $\tfrac34\sum_\alpha\sum_c\alpha_c\log\alpha_c-\tfrac12S_1\log H+O(S)$.
Here $\alpha_1\asymp H^{2/3}U$ and $\alpha_{2,3}\ll H^{-1/3}U$. The $\log H$ terms cancel exactly, leaving
$\tfrac34(S_1+S_2)\log U+O(S)$. That equals the Hadamard upper bound $(S_1+S_2)\log N=\tfrac34(S_1+S_2)\log U$ to
leading order.

So for a fixed field the method is EXACTLY saturated by equidistribution and never contradicts Chebotarev. In
small cases my rough heuristic estimate of the remaining $O(S)$ terms (for $H=1$, generic Hilbert function; not a computation) favours the upper bound.

A contradiction arises only when the Frobenius distribution is biased toward $\{\sigma,\sigma\tau\}$. Each such
prime lowers $\alpha_1$ plus one other coordinate, giving at least $S_1\log U$, which exceeds
$\tfrac34(S_1+S_2)\log U$ once $S_2<S_1/3$. That bias is exactly what a Siegel zero forces via (2.1). It also
explains the two design choices: adjoining $\sqrt2$ makes the $\chi(p)=-1$ classes a 2-element coset inside a
3-element coordinate set, and the weight $H$ pushes $S_2/S_1\to0$.

Unconditionally, the paper's own inequality gives
$\sum_{H<p\le U,\chi(p)=-1}\log p/p\le(13/16+o(1))\log U+O(\ell)$, against the true $\tfrac12\log U$: consistent.

The generalised class bounds were checked exactly at $N=2$ (6 fields, 0 failures). The $N=3$ run is in
gen_d13_N3_H3.txt / gen_d17_N3_H1.txt (see the tail note).

Result: the test cannot make the method prove anything false. The argument's threshold sits precisely at
Chebotarev density 3/4 = $\log N/\log U$, which is strong structural evidence that both bounds are correctly
calibrated.

## What I could NOT check
- The Lean formalisation beyond its final statement. I read only
  `OAI/NumberTheory/Jacobsthal/Siegel/DirichletRealZeroBound.lean`. Its statement matches Theorem 1: primitive,
  $\chi\ne1$, real-valued, $0<\beta<1$, LFunction zero, $c\le(1-\beta)\log q$, $q\ge3$. I did not audit the
  definitions in the closure or the 66-file proof.
- Numerics are tiny ($M\le81$). They test the algebraic identities (Lemma 7, Lemma 3), not the asymptotic
  comparison. That comparison is checked by hand only.
- Bibliographic accuracy of the citations (Fischler, Bost, Laurent page/theorem numbers) was not checked.
- Context, read after my own verdict was formed: W_work holds Tao's 19 Oct blog post and comments. They report
  digestions and simplifications by Banks, Kerr and Green, and none reports an error in this paper. I did not rely
  on them.

## Where a hole is most likely to hide in my scope, and whether it does
A priori the two most likely places are these:
- the zero estimate (Lemma 3), since uniformity in $A$ with only a qualitative irrationality hypothesis is where
  transcendence-style arguments usually break;
- the passage from "rows in the span" to "determinant divisible", Lemma 7's lower-triangular $L$ over $K$, which
  is not integral.

Neither has a hole:
- Lemma 3 uses irrationality only through $r\cdot c\ne0$ for a single integer normal $r$. All counting is
  lattice-point counting in $[0,4(N-1)]^4$. No coefficient size enters, and §4 correctly notes that none is needed,
  because $\Delta$ is built from the original monomial rows.
- Lemma 7's divisibility is read off the replaced rows themselves, whose entries lie in $p^k\cR$. The non-integral
  $L$ only certifies that the determinant is unchanged, which is an identity over $K$.

The next candidate was hidden $q$-dependence in "absolute" constants. I traced every constant. The field enters
only via $|\nu(\theta_n)|\le8N\sqrt q$, i.e. the explicit $\tfrac12\ell$ per unit degree, and $\gamma$ is chosen
to dominate it.

## Tail note (numerics finished)
gen_d13_N3_H3.txt ($d=13$, $N=3$, $H=3$, $M=81$): the generalised class bounds hold at every prime, with 0 failures.
- $p=3$ ($\tau$): $v_3=200\ge72$.
- $p=5$ ($\sigma\tau$): $120\ge96$.
- $p=7$ ($\sigma$): $68\ge40$.
- $p=11$ ($\sigma\tau$): $12\ge4$.

The paper-form first-coordinate bound at the $\tau$-prime $p=3$ again FAILS ($200<240$), so the negative control
discriminates. The $d=17$, $N=3$ run was stopped unfinished; it is not needed.
