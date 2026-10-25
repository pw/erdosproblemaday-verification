# Referee report — YOURTAG = sources
OpenAI, *The weak pinned planar distance theorem* (23 Sep 2026, 27 pp), sha256 6350959d…789f0 (re-hashed locally; git blob
bf80b588 = the file on openai/math `main` today; the preprint folder and `lean/OAI/Geometry/PinnedDistances/` have ONE commit
each, the initial `adc7f1241b`, 2026-10-06 — untouched by the 2026-10-08 "update-10-7" revision). Scope: the 14 references,
fetched and quoted; the state of the world on 14 Oct 2026; what is and is not novel. All fetched material is under
`/tmp/oaimath/604/refs/src/` (live erdosproblems pages under `refs/src/live/`, GitHub artefacts under `refs/src/gh/`);
finite checks under `/tmp/oaimath/604/seats/sources_checks/`. Fetched 2026-10-14 15:10–15:38Z.

## 1. Objections

**S1. COSMETIC (exposition) — [11] pinpoints are inconsistent, and Σ_{v|∞}σ_v = 1 is not in any cited item.**
p.3: "The normalized product formula balances the logarithms … [11, Theorem 7.15]." p.9: "The normalized product formula
[11, Theorems 7.14–7.15 and Lemma 8.6] reads Σ_v σ_v log|z|_v = 0 (z ∈ K∖{0}), Σ_{v|∞} σ_v = 1. (3.2)". Bibliography p.27:
"Version 3.08, Theorem 7.15 and Lemma 8.6." Three different pinpoints for one fact. Substance is right (table row [11],
and the numeric check in §3c): Milne's normalized values are (1/Np)^{ord_p} at finite primes and |σa|² at complex
embeddings; Lemma 8.6 gives ‖a‖ = |a|^{n} with n = [K_v:Q_p]; dividing Milne's Σ log‖z‖_v = 0 by [K:Q] gives exactly
the paper's σ_v = [K_v:Q_p]/[K:Q] and σ_v = 2/[K:Q]. But the second half of (3.2), Σ_{v|∞}σ_v = 1, is not Theorem 7.14,
7.15 or Lemma 8.6: it is r + 2s = [K:Q] with r = 0 (i ∈ K), which Milne states in Ch. 4, "Finiteness of the class number", printed p.79 of v3.08: "Suppose that K has r real
embeddings … and 2s complex embedding[s] … Thus n = r + 2s." Fix: cite that line, and make the three pinpoints agree. Not a gap in the proof.

**S2. UNCLEAR (framing of novelty, exposition only) — the large-s half of Theorem 1.1 is classical and unmentioned.**
p.3: "Theorem 1.1 controls the multiplicity of a distance chosen by sampling a distinct ordered pair." The paper never says
that F_n(s) → 0 is already a consequence of the cited Katz–Tardos paper for every s > 0.1359. Katz–Tardos, Corollary 8
(rendered p.6 of their PDF): "Any collection of n distinct points in the plane determine O(n^{(117−34e)/(55−16e)+ε})
isosceles triangles", exponent 2.13586. Two-line reduction: with A = #{(x,{y,z}) : |xy| = |xz|} (apex triples; collinear
midpoint triples add ≤ n²), every rich ordered pair lies in a fiber F with |F| ≥ T, and |F| ≤ |F|(|F|−1)/(T−1), so
#rich ≤ 2A/(T−1); with T = n^s this is n^{2.1359+ε−s} = o(n²) once s > 0.1359. Checked exactly on 121 small
configurations with a failing control (§3a). So the theorem's new content is exactly 0 < s ≤ 0.1359. Corollary 1.2 takes s = ε/2, so it needs that range only when
ε ≤ 0.272, and the single-pin form with exponent 1 − ε < 0.864 was already Katz–Tardos Cor. 6. Fix: one remark after Theorem 1.1. No effect on correctness.

**S3. UNCLEAR (framing, exposition only) — "all but o(n) pins" is not stronger than "one pin".**
Abstract: "For every fixed ε > 0, all but o(n) points of any n-point planar set determine at least n^{1−ε} distinct nonzero
distances." p.3: "Corollary 1.2 makes its almost-every-pin consequence explicit". The problem page itself records (Hunter,
comment 12:59 on 08 Feb 2026): "if there exists a single point, then by greedily repeating this you will of course get ≫ n
such points", and the greedy argument gives the full almost-all form with ε → 2ε: if every m-point set with m ≥ M_ε has a
pin with ≥ m^{1−ε} distances, strip such pins from P while |current| ≥ max(M_ε, n^{1−ε}); each stripped pin sees
≥ (n^{1−ε})^{1−ε} ≥ n^{1−2ε} distances inside a subset of P, so at most n^{1−ε} + M_ε = o(n) pins of P see fewer than
n^{1−2ε}, uniformly in P. Hence Corollary 1.2 ⟺ the weak pinned conjecture (Erdős 1957 / Dewar et al. Conj 4.7); the
"all but o(n)" wording adds nothing. True as stated; misleading only as a claim of extra strength.

**S4. COSMETIC (attribution) — the arithmetic toolkit is shared with an uncited companion paper of the same date, and the
grid's scale randomization is FRT's.** The companion OpenAI preprint *A power saving for planar unit distances* (23 Sep 2026,
same family 167, same `lean/docs/167.md`) uses the same three tools with the same citations: "The arithmetic input is the
normalized product formula [19]" (its p.2), "[19, Theorems 7.14–7.15 …] … Milne's local normalization formula [19, Lemma 8.6]"
(its §4.1), "The transfer principle for real closed fields [17, Theorems 3.1 and 4.1]" (its Lemma 2.1, [17] = Kuhlmann
Lecture 09), and the same place-by-place partition device (its Lemma 4.3): "At a nonarchimedean entry give two vertices the
same label if their U-coordinates differ by at most e^s in absolute value. The strong triangle inequality makes this an
equivalence relation. At an archimedean entry, use the cell of a square grid in C of side e^s, shifted by a uniformly random
fractional vector." Compare the pinned paper p.9: "The ultrametric inequality makes d_j(x,y) ≥ r an equivalence relation.
At a complex place we obtain the same nesting property from square grids". The pinned paper never mentions the companion.
Separately, §3.2's "ξ uniform on [0, log 2). The grid side lengths are l_m = e^ξ 2^m" is exactly the scale randomization of
FRT (JCSS 2004 p.489: "We also pick a β randomly in the interval [1, 2] from the distribution given by the probability
density function p(x) = 1/(x ln 2)", i.e. β = e^ξ with ξ uniform on [0, ln 2)), while the paper
credits FRT only with "Nested partitions and their associated trees". Not a mathematical issue.

**S5. COULD NOT FETCH — [1] Arora JACM 1998 §2.1 and [12] Solymosi–Tóth DCG 2001 Theorem 1.** dl.acm.org returns a Cloudflare
challenge (403) from exe.dev, from the Hetzner box, and through the residential tier; the Internet Archive was "Temporarily
Offline"; link.springer.com redirects to an auth wall from both egresses. The CONTENT of both citations is corroborated by
secondary sources (rows [1], [12]); the pinpoints "Section 2.1" and "Theorem 1" are unverified. [6] FRT was checked against
the JCSS 2004 journal version (69:485–497), not the cited STOC 2003 proceedings. [5] Evans–Matsen was checked in arXiv
1005.1699v3 (4 May 2011); the cited JRSS-B 2012 version could not be fetched (Europe PMC full text 500), so its equation
numbering is unverified. None of these are load-bearing.

No objection rises above UNCLEAR in my scope. No citation is a MISMATCH.

## 2. Coverage of my scope

| Item | Status |
|---|---|
| All 14 bibliography entries vs. the in-text uses (lines 52, 94–112, 132, 142–143, 284, 419–421, 451, 1108, 1242–1243 of paper.txt; PDF pp.2,3,7,9,20,23,27) | VERIFIED LINE BY LINE (12 of 14 against the primary source; [1] and [12] against secondary sources only) |
| (3.2) normalization vs Milne v3.08 (Thms 7.14, 7.15, Lemma 8.6, r+2s=n) | VERIFIED LINE BY LINE + numeric check in Q(i) with two failing controls |
| p.7 transfer step ("existential sentence holds over R and therefore over the real algebraic numbers") vs Kuhlmann Thms 3.1/4.1 | VERIFIED LINE BY LINE (as a citation; the system's construction is the extremal seat's) |
| (6.12) tree transport vs Evans–Matsen §2 eq (5) | VERIFIED (citation match; the finite-tree proof on p.20 is the transport seat's) |
| p.23 compactness/Portmanteau vs van Gaans Prop 5.3, Thm 4.2, Thm 3.2(d) | VERIFIED (citation match and direction of the open-set inequality) |
| Corollary 1.2's attribution (Erdős 1957 Problem 16; Dewar Conj 4.7) | VERIFIED LINE BY LINE (Erdős page rendered) |
| Intro history: Erdős 1946 Thm 1, Guth–Katz Thm 1.1, Solymosi–Tóth, Tardos, Katz–Tardos constant, Lund–Petridis | VERIFIED (constants numerically, with control) |
| OpenAI catalogue: formalization.yaml, docs_167.md, PinnedDistances.json, comparator .lean | VERIFIED (text) |
| Proof body §§2–7 | NOT READ beyond the citation sentences (other seats) |

## 3. Finite checks (scripts verbatim, outputs verbatim)

### 3a. `sources_checks/iso_reduction.py` — the isosceles reduction behind S2
```python
# Check: #{ordered (x,y), x!=y, k_P(x,y) >= T}  <=  2*A/(T-1)  for T >= 2,
# where A = #{(x,{y,z}) : y!=z, |xy| = |xz|} (apex-isosceles triples, degenerate ones included).
# This is the reduction "isosceles-triangle bound => Theorem 1.1 for large s".
# Exact integer squared distances. Control: a deliberately wrong bound (A/(10*(T-1))) must FAIL somewhere.
import itertools, random, sys
from collections import Counter
def stats(P, T):
    rich = 0; A = 0
    for x in P:
        c = Counter((y[0]-x[0])**2 + (y[1]-x[1])**2 for y in P if y != x)
        for d, k in c.items():
            A += k*(k-1)//2
            if k >= T: rich += k          # each y in a fiber of size k >= T is a rich pair (x,y)
    return rich, A
def check(bound_factor, label):
    bad = 0; tot = 0
    configs = []
    for m in (5, 6, 7, 8):
        configs.append(("grid%d" % m, [(i, j) for i in range(m) for j in range(m)]))
    random.seed(1)
    for t in range(6):
        configs.append(("rand%d" % t, list({(random.randrange(12), random.randrange(12)) for _ in range(45)})))
    configs.append(("circle+centre", [(0,0),(5,0),(-5,0),(0,5),(0,-5),(3,4),(4,3),(-3,4),(-4,3),(3,-4),(4,-3),(-3,-4),(-4,-3)]))
    for name, P in configs:
        for T in range(2, 13):
            rich, A = stats(P, T)
            tot += 1
            if not (rich * (T-1) <= bound_factor * A):
                bad += 1
                if bad <= 3: print("  %s VIOLATION %s n=%d T=%d rich=%d A=%d" % (label, name, len(P), T, rich, A))
    print("%s: %d/%d cases violate" % (label, bad, tot))
    return bad
b1 = check(2.0, "claimed bound rich*(T-1) <= 2A")
b2 = check(0.2, "CONTROL rich*(T-1) <= 0.2A (wrong)")
print("RESULT:", "PASS" if b1 == 0 and b2 > 0 else "FAIL")
```
```
claimed bound rich*(T-1) <= 2A: 0/121 cases violate
  CONTROL rich*(T-1) <= 0.2A (wrong) VIOLATION grid5 n=25 T=2 rich=524 A=516
  CONTROL rich*(T-1) <= 0.2A (wrong) VIOLATION grid5 n=25 T=3 rich=268 A=516
  CONTROL rich*(T-1) <= 0.2A (wrong) VIOLATION grid5 n=25 T=4 rich=160 A=516
CONTROL rich*(T-1) <= 0.2A (wrong): 53/121 cases violate
RESULT: PASS
```

### 3b. `sources_checks/constants.py` — the quoted constants
```python
# Numeric checks of constants quoted from sources (control: a transposed formula must NOT match).
import math
e = math.e
checks = [
  ("Katz-Tardos Cor.6 (48-14e)/(55-16e) vs paper's 0.864137", (48-14*e)/(55-16*e), 0.864137),
  ("Katz-Tardos Cor.5 (10-3e)/(24-7e) vs KT's 0.371107", (10-3*e)/(24-7*e), 0.371107),
  ("Tardos 2003 Cor.15 4e/(5e-1) (~0.8635)", 4*e/(5*e-1), 0.8635),
  ("Katz 19/22 vs KT's quoted 0.863636", 19/22, 0.863636),
  ("CONTROL transposed (48-16e)/(55-14e) vs 0.864137", (48-16*e)/(55-14*e), 0.864137),
]
for name, val, ref in checks:
    ok = abs(val - ref) < 5e-5
    print("%-58s %.7f  %s" % (name, val, "MATCH" if ok else "NO MATCH"))
iso = (117-34*e)/(55-16*e)
print("Katz-Tardos Cor.8 isosceles exponent (117-34e)/(55-16e) = %.6f => F_n(s)->0 already follows for s > %.4f" % (iso, iso-2))
```
```
Katz-Tardos Cor.6 (48-14e)/(55-16e) vs paper's 0.864137    0.8641375  MATCH
Katz-Tardos Cor.5 (10-3e)/(24-7e) vs KT's 0.371107         0.3711071  MATCH
Tardos 2003 Cor.15 4e/(5e-1) (~0.8635)                     0.8635354  MATCH
Katz 19/22 vs KT's quoted 0.863636                         0.8636364  MATCH
CONTROL transposed (48-16e)/(55-14e) vs 0.864137           0.2660220  NO MATCH
Katz-Tardos Cor.8 isosceles exponent (117-34e)/(55-16e) = 2.135862 => F_n(s)->0 already follows for s > 0.1359
```

### 3c. `sources_checks/product_formula_Qi.py` — the normalization (3.2) in K = Q(i)
```python
# Check the paper's normalisation (3.2) in K = Q(i), [K:Q] = 2 (one complex place, no real places):
#   finite place v | p: |.|_v extends |p|_p = 1/p, sigma_v = [K_v:Q_p]/[K:Q];  complex place: ordinary modulus, sigma = 2/[K:Q] = 1.
#   Claim: sum_v sigma_v log|z|_v = 0 for z != 0, and sum_{v|inf} sigma_v = 1.
# Gaussian-prime valuations computed by exact division in Z[i]. Controls: (a) squared modulus at the complex place
# with sigma=1 (double counting), (b) finite weights not divided by [K:Q]; both must FAIL.
import math, random
def gdivmod_exact(a, b):           # return a/b if b | a in Z[i], else None; a,b as (re,im)
    (x, y), (u, v) = a, b
    n = u*u + v*v
    re, im = x*u + y*v, y*u - x*v
    if re % n or im % n: return None
    return (re // n, im // n)
def val(z, pi):
    k = 0
    while True:
        q = gdivmod_exact(z, pi)
        if q is None: return k
        z, k = q, k + 1
def gaussian_prime_over(p):        # a Gaussian prime pi with N(pi)=p, p = 1 mod 4 or p = 2
    for a in range(1, int(p**0.5) + 1):
        b2 = p - a*a; b = int(round(b2**0.5))
        if b*b == b2: return (a, b)
def factor(n):
    f, d = {}, 2
    while d*d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def total(z, mode):
    N = z[0]**2 + z[1]**2
    s_fin = 0.0
    for p in factor(N):
        places = []                # (sigma_v, log|z|_v)
        if p == 2:
            places.append((2/2, -val(z, (1, 1)) * 0.5 * math.log(2)))      # e=2: |1+i|_v = 2^(-1/2), n_v = 2
        elif p % 4 == 3:
            places.append((2/2, -val(z, (p, 0)) * math.log(p)))            # inert: n_v = 2
        else:
            a, b = gaussian_prime_over(p)
            for pi in ((a, b), (a, -b)):
                places.append((1/2, -val(z, pi) * math.log(p)))           # split: n_v = 1 each
        for sig, lg in places:
            s_fin += sig * (2 if mode == "undivided" else 1) * lg
    mod = math.hypot(*z)
    s_inf = 1.0 * (2*math.log(mod) if mode == "squared" else math.log(mod))
    return s_fin + s_inf
random.seed(7)
zs = [(random.randint(-300, 300), random.randint(-300, 300)) for _ in range(400)]
zs = [z for z in zs if z != (0, 0)]
for mode in ("paper", "squared", "undivided"):
    worst = max(abs(total(z, mode)) for z in zs)
    print("%-10s max |sum sigma_v log|z|_v| over %d Gaussian integers = %.3e  -> %s" %
          (mode, len(zs), worst, "HOLDS" if worst < 1e-9 else "FAILS"))
print("sum_{v|inf} sigma_v = 2/[K:Q] * (#complex places = 1) =", 2/2*1)
```
```
paper      max |sum sigma_v log|z|_v| over 400 Gaussian integers = 8.882e-16  -> HOLDS
squared    max |sum sigma_v log|z|_v| over 400 Gaussian integers = 6.020e+00  -> FAILS
undivided  max |sum sigma_v log|z|_v| over 400 Gaussian integers = 6.020e+00  -> FAILS
sum_{v|inf} sigma_v = 2/[K:Q] * (#complex places = 1) = 1.0
```
(Algebraic integers only; multiplicativity extends it to K. One field, so this tests the normalization, not Milne's theorem.)

## 4. Citation table

| Ref | Where / what the paper claims | What the source says (quoted) | Verdict |
|---|---|---|---|
| [1] Arora, JACM 45(5) 1998 | p.3, p.9: "Randomly shifted (recursive) square dissections also appear in Arora's Euclidean approximation algorithms [1, Section 2.1]" | Primary blocked (ACM DL 403 ×3 egresses). Arora's own survey of the same algorithm ("Approximation schemes for NP-hard geometric optimization problems: A survey", Princeton COS521 copy): "position the enclosing box such that P has distance a from the left edge and b from the lower edge, where integers a, b ≤ l are chosen randomly. We refer to a, b as the horizontal and vertical shift respectively … The randomized dissection is the dissection of this enclosing box." Shift only — no rotation or scale randomization (the paper does not claim otherwise). | COULD NOT FETCH primary (content corroborated; §2.1 pinpoint unverified) |
| [2] Dewar–Frankl–Mansfield–Nixon–Passant–Warren, arXiv 2505.06590v1 (still the only version) | p.2: "the modern terminology appears, for example, in [2, Conjecture 4.7]" | "Conjecture 4.7 (Weak pinned distance conjecture). For any ε > 0, there exists a constant C_ε > 0 such that the following holds. For any finite point set P ⊆ R², there exists a point q ∈ P, which determines at least C_ε|P|^{1−ε} distances to the other points of P with respect to the Euclidean distance." Also "Theorem 4.10. The weak unit distance conjecture implies the weak pinned distance conjecture." (hypothesis = Conj 4.8 "at most C_ε|P|^{1+ε} distances of length 1", false given n^{1+c} unit distances; teorth DB #90 = "disproved (Lean)", 2026-06-07). Dewar says the conjecture "first appeared in [12]" = Erdős 1990; Erdős 1957 is earlier (row [4]). | MATCH |
| [3] Erdős, AMM 53 (1946) 248–250 (Rényi archive 1946-03) | p.2: "Erdős initiated the planar distinct-distance and repeated-distance problems in 1946 [3]"; "The square lattice gives … at most a constant multiple of n/√log n [3, Theorem 1]" | "THEOREM 1. The minimum number f(n) of distances determined by n points of a plane satisfies the inequalities (n − 3/4)^{1/2} − 1/2 < f(n) < cn/(log n)^{1/2}." Upper bound "Considering now the points (x, y) with integer coordinates for 0 ≤ x, y ≤ n^{1/2}". §3 treats g(n; r), the repeated-distance function. | MATCH |
| [4] Erdős, Michigan Math. J. 4(3) (1957) 291–300 (Rényi archive 1957-13; page 296 rendered; Crossref DOI 10.1307/mmj/1028997963 confirms vol 4 issue 3) | p.2: "Erdős explicitly stated this question in 1957 [4, Problem 16]" | Problem 16: "It can be conjectured that, for n > n_ε, f(n) > n^{1−ε}, and further, that there exists a point p_i such that more than n^{1−ε} different values occur among the distances p_ip_j." | MATCH — it states the pinned question exactly |
| [5] Evans–Matsen, JRSS-B 74(3) 2012 (checked arXiv 1005.1699v3) | p.20: "(6.12) … This standard formula is the finite-tree form of [5, Section 2, Equation (5)]" | §2 "The phylogenetic Kantorovich-Rubinstein metric": "(5) Z(P, Q) = ∫_T |P(τ(y)) − Q(τ(y))| λ(dy)", τ(y) the subtree below y, λ the length measure. Finite tree: Σ_edges length·|P(subtree) − Q(subtree)| = the paper's Σ_B l_j(B)|ρ(B) − α(B)|. | MATCH (journal numbering unverified) |
| [6] Fakcharoenphol–Rao–Talwar, STOC 2003 (checked JCSS 69 (2004) 485–497) | p.3: "Nested partitions and their associated trees also occur in probabilistic metric approximation … Their approximation controls multiplicative distortion." | "any n point metric space can be embedded into a distribution over dominating tree metrics such that the expected stretch of any edge is O(log n)"; "A hierarchical cut decomposition … is a sequence of … nested cut decompositions"; "A hierarchical cut decomposition defines a laminar family, and naturally corresponds to a rooted tree"; random scale "probability density function p(x) = 1/(x ln 2)". | MATCH (see S4: the ξ-scale randomization is also FRT's) |
| [7] Guth–Katz, Annals 181 (2015) (arXiv 1011.4105v3) | p.3: "every planar n-point set determines at least a constant multiple of n/log n distances [7, Theorem 1.1]" | "Theorem 1.1. A set of N points in the plane determines ≳ N/log N distinct distances." | MATCH |
| [8] Katz–Tardos, Contemp. Math. 342 (2004) 119–126 (Tardos's PDF) | p.3: "Katz and Tardos refined that method to obtain every exponent below (48−14e)/(55−16e) = 0.864137…"; "These results guarantee one pin" | "Corollary 6. For any constant ε > 0 … Any collection P of n distinct points in the plane has an element from which the number of distinct distances to the other points is Ω(n^{(48−14e)/(55−16e)−ε})"; "48−14e/55−16e = 0.864137…". Also Cor. 8 (isosceles, see S2). | MATCH (constant checked, §3b) |
| [9] Kuhlmann, RAG Lecture 09 (17/11/09) | p.7: "Their existential sentence holds over R and therefore over the real algebraic numbers, by transfer for real closed fields [9, Theorems 3.1 and 4.1]" | "Theorem 3.1. Let (K,⩽) be an ordered field, R1, R2 two real closed extensions of (K,⩽). Then a system … fi(X) ∈ K[X1,…,Xn], has a solution x ∈ R1^n ⟺ it has a solution x ∈ R2^n." "Theorem 4.1. Suppose that R ⊆ R1 are real closed fields. Then a system … with coefficients in R has a solution x ∈ R1^n ⟺ it has a solution x ∈ R^n." Relations allowed: {⩾, >, =, ≠}. K = Q, R1 = ℝ, R2 = R = real algebraic numbers. (That the real algebraic numbers are real closed is standard, not in the notes.) | MATCH |
| [10] Lund–Petridis, DCG 64(3) 2020 (arXiv 1810.00765v1, the only version) | p.3: "The sharper pinned conjecture asks for order n/√log n distances at a pin; see [10, Introduction]. Lund and Petridis also explain the distinction between the real planar problem and pinned-distance theorems over other fields." | "there must occur a point a ∈ A such that the remaining points of A are at Ω(N log^{−1/2}(N)) different distances from a. This is often called the pinned distances conjecture. The best known bound of Ω(N^{0.864...}) was proved by Katz and Tardos"; "These problems have also been considered over other fields … This simple bound is tight over fields of positive characteristic". | MATCH |
| [11] Milne, ANT v3.08 (July 19, 2020; 166 pp — version matches) | p.3 "[11, Theorem 7.15]"; p.9 "[11, Theorems 7.14–7.15 and Lemma 8.6]"; bib "Theorem 7.15 and Lemma 8.6" | "THEOREM 7.14 … exactly one prime of K (a) for each prime ideal p; (b) for each real embedding; (c) for each conjugate pair of complex embeddings." Normalizations: "for a prime ideal p of OK, |a|_p = (1/Np)^{ord_p(a)}"; "for a nonreal complex embedding σ: K ↪ C, |a| = |σa|²". "THEOREM 7.15 (PRODUCT FORMULA) … For every nonzero α ∈ K, Π|α|_v = 1". "LEMMA 8.6 In the above situation, ‖a‖ = |a|^n, where n = [L:K]." Dividing by [K:Q] gives (3.2)'s first half exactly; second half needs Milne's "Thus n = r + 2s" (p.79) with r = 0 (S1). | MATCH (pinpoint inconsistency S1) |
| [12] Solymosi–Tóth, DCG 25(4) 2001 629–634 | p.3: "Solymosi and Tóth proved a pinned lower bound of order n^{6/7} [12, Theorem 1]" | Primary behind Springer auth wall. Abstract (search-engine snippet of the Springer record): "every set of n points in the plane has an element from which there are at least cn^{6/7} other elements at distinct distances". Tardos 2003: "They proved an Ω(n^{6/7}) bound for an old problem of P. Erdős". | COULD NOT FETCH primary (content corroborated; "Theorem 1" label unverified) |
| [13] Tardos, Adv. Math. 180 (2003) 275–289 (Tardos's PDF) | p.3: "Tardos improved this exponent using entropy inequalities for patterns of sums and differences [13]" | "the UV pattern p_{U,V}(R) … consisting of the differences a_i − a_j … and the sums a_i + a_j"; "Lemma 3 … linear constraints on the entropies H(U,V)"; "Corollary 15. … any set P of n points in the plane has an element from which the number of distinct distances to the other points of P is Ω(n^{4e/(5e−1)−ε})" (= 0.86354). | MATCH |
| [14] van Gaans, Probability measures on metric spaces (2003 notes) | p.23: "The space of probability measures on a compact metric space is compact and metrizable for weak convergence [14, Proposition 5.3 and Theorem 4.2]. We also use the open-set inequality in the Portmanteau theorem [14, Theorem 3.2]." | "Proposition 5.3. If (X, d) is a compact metric space, then (P(X), d_P) is a compact metric space." "Theorem 4.2. If (X, d) is a separable metric space, then … µ_i ⇒ µ if and only if d_P(µ_i, µ) → 0." "Theorem 3.2 … (d) lim inf_{i→∞} µ_i(U) ≥ µ(U) for all open U ⊂ X". The paper applies (d) to open U = {|z|>R}∪{∞} and open disks, in the direction β(U) ≤ liminf α(U). | MATCH |

## 5. The world on 14 October 2026

**erdosproblems.com/604** (live copy fetched 15:27Z via the Hetzner box — the site 403s exe.dev; identical in substance to the
saved `live_604.html`): statement unchanged; "The best known bound is ≫ n^{c−o(1)}, due to Katz and Tardos [KaTa04], where
c = (48−14e)/(55−16e) = 0.864137⋯"; "This page was last edited 23 March 2026"; "Proof claims (0)"; "Comments (1)" — Zach
Hunter, 12:59 on 08 Feb 2026: "if there exists a single point, then by greedily repeating this you will of course get ≫ n
such points. (The site has been updated to address this comment.)"; and, under the thread: "The ability to post new
comments has been suspended." No status label is displayed (statuses hidden site-wide). **#89**: last edited 23 January
2026, Proof claims (0), Comments (0).

**Bloom, "Erdős problems in the OpenAI proofs", 8 October 2026** (saved copy and live copy, comments to 21:15 on 12 Oct):
#604 entry verbatim: "Problem [604] - Pinned distances This PDF claims a proof of the following. For every ε>0, if n is
sufficiently large, then any set of n points in ℝ² contains a point which determines at least n^{1−ε} distinct distances.
This proof has been formalised . The PDF is 27 pages long." No remark on method. Standing caveats: "Disclaimer : I have not
yet looked at in any serious way any of the proofs in this release" and "I have also not, where a Lean formalisation is
provided, yet checked myself that the formalisation compiles or that the statement in the challenge file accurately captures
the problem." No comment under the post mentions 604, "pinned", or distinct distances.

**teorth database.** Worktree `src/tracker_data.js` (TRACKER_SRC 86c3dc3e, 2026-10-13): `"604":{"s":"open","lu":"2025-08-31",
"pr":"$500",…,"cm":"pinned distance problem"}`; `"89":{"s":"open","lu":"2025-08-31",…}`. Live `data/problems.yaml` today:
604 `status: open, last_update 2025-08-31`, `formalized: yes, last_update 2026-10-08`, `formal_status: unformalized`.

**Formal Conjectures `ErdosProblems/604.lean`** (raw main today): added by PR #6796 (veljjanoski; opened 2026-10-02 — BEFORE the
release — merged 2026-10-08; "AI-usage disclosure: Claude (Anthropic) was used as assistant"; "Fixes #823"). Defines
`pinnedDistinctDistances n := sInf {m | ∃ A : Finset ℝ², #A = n ∧ A.sup (distinctDistancesFrom A) = m}` with
`distinctDistancesFrom points pt := #((points.erase pt).image fun x => dist x pt)`; `theorem erdos_604 : ∀ ε : ℝ, 0 < ε →
∀ᶠ n : ℕ in atTop, (n : ℝ) ^ (1 - ε) ≤ (pinnedDistinctDistances n : ℝ) := by sorry` tagged
`@[category research open, question, AMS 52]`; variants `sqrt_log` (open), `grid_upper_bound` (solved), `katz_tardos` (solved,
exponent (48−14e)/(55−16e) − ε), `average` (open). OpenAI's `OAI.WeakPinned.exists_pin_eventually` (∀ε>0, ∀ᶠ n, ∀ P, card = n
→ ∃ x ∈ P, n^{1−ε} ≤ #(distances P x), `distances P x = (P.erase x).image (dist · x)`) implies `erdos_604` directly (same
counting function; the sInf is attained). No PR or issue cites the OpenAI proof for 604 (GitHub searches "604",
"weak pinned", "PinnedDistances", "OpenAI 604", "pinned distance OpenAI": only #6796 and #823).

**OpenAI catalogue.** `formalization.yaml` lists the preprint as a source (lines 817–819) and under results
`comparator_config: ComparatorChallenges/PinnedDistances.json / declaration: OAI.WeakPinned.main / file:
OAI/Geometry/PinnedDistances/Main.lean` (lines 1469–1471). `PinnedDistances.json`: `"theorem_names": ["OAI.WeakPinned.main"]`,
`"permitted_axioms": ["propext","Quot.sound","Classical.choice"]`, `"enable_nanoda": false`. Comparator `main (s : ℝ)
(hs : 0<s) : Tendsto (fun n : ℕ => F n s) atTop (𝓝 0)` with `F n s = if 2 ≤ n then sSup {a | ∃ P, P.card = n ∧ a =
pairFraction P s} else 0`, `k P x y = #((P.erase x).filter (dist z x = dist y x))` (counts y) — matches Theorem 1.1.
`docs_167.md` maps the weak pinned theorem to `PinnedDistances.lean`. No `sorry`/`axiom` text in the 48 PinnedDistances files.
`history.md` (2026-10-07 update): three withdrawals (the split-abelian-eightfold Weil-class paper and two dependents) and 14
revisions — the pinned paper is in neither list.

**Third-party Lean.** (i) `carlostoledo1891/cert-machine`, `corpus/openai-math/kernel-runs/38019899278/PinnedDistances.json`:
`exit 0`, 567 s, Lean 4.34.1, log tail "Lean default kernel accepts the solution", "nanoda kernel accepts the solution",
"Your solution is okay!" — the comparator run, by a party describing itself as "Independent exact certification of
machine-generated mathematics". (ii) `plasma-ai/erdos` (created 2026-10-08) records the claim as `status: accepted, claim:
proved, scope: partial` (Q1 only) and states "The prose proof (Sections 2 through 7) is unreviewed; acceptance rests on the
audited Lean statements"; its library card says it built `main`, `pins`, `exists_pin_eventually` and found axioms
propext/Classical.choice/Quot.sound only. (iii) Justin Sun Prize catalogue JSP-001061 "Weak pinned planar distance problem":
"Current status Solved … independent mathematical review pending"; its review note: "no clean Lean build, target axiom audit,
kernel replay or Comparator execution was completed". (iv) Our replay (`lean-build/steps.tsv` at 15:26Z): build rc 0 (508 s),
axioms rc 0 with PIN_STD_AXIOMS, wrongshape rc 1, negcontrol rc 0 with sorryAx, statement_match_v3 rc 0; `leanchecker --fresh
OAI.Geometry.PinnedDistances.Pins` was running — not my scope, reported as read.

**Public discussion of THIS paper.** None that engages its mathematics. Searched: Kalai (blog front page + the 7 Oct post
"Updates: Sharing AI progress on mathematics (amazing!)", whose item 8 "Distinct distances and unit distances" covers the
d ≥ 3 distinct-distance and planar unit-distance results and never says "pinned"/604); Tao's Mastodon (120 posts back to
April — OpenAI parodies and the Fields declaration, nothing on 604); MathOverflow and Math.SE (API: no question or answer
on pinned distances since Sept; release-level threads only); Hacker News (Algolia since mid-Sept: release, withdrawal and
Navier–Stokes threads, nothing on pinned distances); WebSearch for the exact title returns only `lean/docs/167.md`;
lay explainer sites (Closed Form, kisonecat index) have no pinned entry in their static text. OpenAI's own CONTENTS entry
#167 repeats the abstract.

**Other improvements on Katz–Tardos 2004 (2024–2026).** None found. arXiv API abstract searches "pinned distance(s)",
"pinned distinct distances", "weak pinned", "distinct distances" (2023-06 → 2026-10): every pinned hit is Falconer-type
(Hausdorff dimension of pinned distance sets), finite-field, density, or higher-dimensional (Tidor–Yu–Zakharov 2608.14454,
d = 3, non-pinned); none touches the finite planar pinned exponent. Lund–Petridis (2018/2020), the erdosproblems page (Mar
2026), FC's `katz_tardos` variant and Dewar (2025) all still name Katz–Tardos as the record. This is a coverage claim about
the searched corpora.

## 6. What is novel and what is not

NOT novel:
- The statement: Erdős 1957 Problem 16 (verbatim above); named in Dewar et al. Conj 4.7.
- The "all but o(n) pins" form: equivalent to one pin by greedy removal, ε → 2ε (S3); the problem page already says so.
- Theorem 1.1 for s > 0.1359: from Katz–Tardos Cor. 8 by a two-line reduction (S2, §3a).
- Each tool: Tarski transfer [9], the product formula [11], randomly shifted nested grids [1] with FRT's log-uniform scale
  [6], the tree Kantorovich–Rubinstein formula [5], Prokhorov/Portmanteau [14]. The transfer + product-formula + random-grid
  combination is shared with the same-day OpenAI unit-distance preprint (S4), so it is not unique to this paper either.
- Dewar's conditional route (weak unit distance ⇒ weak pinned) is dead: its hypothesis is false.

Novel, on the record as of 14 Oct 2026:
- A proof of Theorem 1.1 for small s, hence of the weak pinned conjecture. No prior proof or claim exists on any tracker
  (erdosproblems 0 proof claims; teorth "open"; FC "research open"; no arXiv paper). The proof is ineffective: no rate,
  no explicit n₀(ε). Asymptotically it supersedes Katz–Tardos's exponent 0.864; Katz–Tardos remains the best EFFECTIVE bound.
- I found no earlier paper applying number-field product-formula balance to pinned distances (a coverage claim: arXiv
  abstracts plus the cited literature).
- Mechanically checked: one independent comparator run (cert-machine, two kernels) and our replay's build/axioms stage.
  No human has publicly reviewed the prose. plasma-ai says outright that §§2–7 are unreviewed.

## 7. Verdict for my scope

HOLDS AS READ. 12 of the 14 references were fetched at the cited (or matching) versions, and each says what the paper
attributes to it. The load-bearing ones are [9] Kuhlmann 3.1/4.1, [11] Milne 7.14/7.15/8.6 (+ r+2s=n), [14] van Gaans
5.3/4.2/3.2, [5] Evans–Matsen eq (5), [8] the constant and [4] Problem 16. There is no MISMATCH.
COULD NOT CHECK: [1] Arora §2.1 and [12] Solymosi–Tóth Theorem 1 at primary source (paywall and Cloudflare walls; content
corroborated secondarily); journal-version numbering of [5]; the STOC version of [6].
Findings are all expository: S1 (pinpoint inconsistency), S2 and S3 (the paper overstates what is new; the new content is
the small-s range, equivalent to the bare weak conjecture), and S4 (an uncited sibling and the FRT scale randomization).
