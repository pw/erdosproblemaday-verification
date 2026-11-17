# Literature / state-of-the-world seat (Claude Opus 5.5 instance), 17 Nov 2026 — saved verbatim by the 09Z erdos seat
Briefed on the ⌈2/δ⌉ − 1 version (before the ⌊2/δ⌋ − 1 strengthening). Downloads (third-party PDFs) are not in the bundle.

# Erdős #338, literature and state-of-the-world check, 17 Nov 2026 (extends world/REPORT.md)

**Main finding:** the finite-group step of Theorem D, and a version of the whole bound for "σ-finite" groups, are already in print. That means a group that is an increasing union of finite subgroups, like polynomials over ℤ/m. The ℕ restricted-order bound ⌈2/δ⌉ − 1 itself was not found anywhere.

## Q1. Ordinary order: is "order ≤ about 2/α" in print?

**Integers (ℕ with lower asymptotic density): no explicit c/α theorem found. Only an unstated O(1/δ).**
- Ramaré–Ruzsa, JTNB 13 (2001), p. 562: "We then conclude by using Kneser's Theorem that A* is an asymptotic basis of order O(1/δ) (statement and proof of Kneser's Theorem may be found in [Halberstam–Roth, chapter I, paragraph 7, Theorem 16′])." Here δ is the lower density of A* + A*. No constant is given.
- Nash–Nathanson 1985, as quoted in Nathanson arXiv:0807.2073, Theorem 1: "If A is a set of nonnegative integers with gcd(A) = 1 such that the sumset h₀A has positive lower asymptotic density … then there exists a number h ∈ ℕ such that hA ∼ ℕ₀." Existence only.
- Halberstam–Roth, *Sequences* (1966). I used Google Books search-inside through the Mac Chrome; the archive.org copy is lend-only and returned 403.
  - No page contains both "Kneser" and "basis" except p. ix (contents) and p. 287 (index).
  - The §I.7 Corollary on p. 63 reads: "Let the system 𝔄 be such that 0 ∈ ⋂𝒜_ν, and d𝒞 < d𝒱. Then if there exist an infinite sequence …". It is structural and says nothing about bases.
  - Treat this as not found. It rests on OCR search, not on reading the section.
- Nash, J. Number Theory 44 (1993); Nash–Nathanson, J. Number Theory 20 (1985); Jia, J. Number Theory 41 (1992); Deschamps–Farhi, J. Number Theory 123 (2007). I read zbMATH reviews only. All four are about the order of A \ F (Kneser gives the upper bounds); none gives an order bound in terms of density.
- Grekos 1988: not reached (seminar exposé, not on numdam).
- Plagne, *Ann. Inst. Fourier* 54 (2004), the X(h) paper: opened, but the formulas are lost in extraction. Its Kneser use is for the X(h) upper bound. I saw no density-to-order statement.
- Hegyvári–Hennecart–Plagne 2003: zbMATH review only. Their results are d(h×A) = d(hA) and d_L(r×A) > 0, with no order bound.
- Hegyvári–Hennecart–Plagne 2007, Thm 10 (re-read): it applies Kneser with j = ⌈(1 + 1/h)/β⌉ and is conditional on their Conjecture 2.

**Finite groups: the step and the bound are classical.**
- **CLAIMS Lemma 1 is Olson's lemma.** Hamidoune–Plagne, *Comment. Math. Helv.* 79 (2004), Lemma 4.2: "(Olson's lemma [20]) Let B be a generating subset of a finite Abelian group G such that 0 ∈ B. Then for every non-empty subset C of G, we have |B + C| ≥ min(|G|, |B|/2 + |C|)." [20] is Olson, J. Number Theory 18 (1984) 110–120.
- The iterated form, as quoted by Hamidoune–Rødseth (1996), traced to Olson, Acta Arith. 28 (1975): "If 1 ∈ A and r is a positive integer, then A^r = ⟨A⟩ or |A^r| ≥ |A| + (r − 1)⌈|A|/2⌉."
- **The finite diameter bound.** Hamidoune–Rødseth, *Math. Scand.* 78 (1996) 246–254, Lemma 1: "Let G be a finite group … 1 ∈ A and … A generates G. Then A is a basis for G of exact order at most max{2, 2|G|/|A| − 1}." They write "cf. Theorem 7.2 in Hamidoune [1981] and the proposition in Rødseth [1982]."
- The same bound is Nathanson, GTM 165 (1996), **Theorem 4.10**: "A is a basis for G′ of order at most max(2, 2|G′|/|A| − 1)." His Exercise 10 gives the sharp example: "G = ℤ/mℤ and A = {0, 1} … exact order h = 2|G|/|A| − 1."
- Klopsch–Lev, *Forum Math.* 21 (2009), Thm 2.9: s⁺_ρ(G) ≤ 2|G|/(ρ+1) for ρ ≥ 4, with equality exactly for A = H ∪ (g + H) where G/H is cyclic of order ρ + 1. Its proof uses the same step as CLAIMS Lemma 1: "Since 0 ∈ A₀ ⊄ H, the set A₀ + H is the union of at least two H-cosets, and so |A₀ + H| ≥ 2|H|."

**Density version in σ-finite groups: printed, with our exact sharpness example.**
- Hamidoune–Rødseth 1996, abstract: "A is a basis for K of exact order at most max{2, 2/δ − 1}." Here δ is upper asymptotic density.
- Their introduction: Cherly–Deshouillers (J. Number Theory 34, 1990) proved 4/d(A) in F_q[x], and Jia–Nathanson (Contemp. Math. 166, 1994) proved "at most 4/δ(A)". Hamidoune–Rødseth "improve the bound of Jia and Nathanson to max{2, 2/δ(A) − 1}".
- Their postscript says the abelian case is also in an undated handwritten manuscript of Deshouillers–Wirsing.
- Nathanson, Theorem 4.11 (p. 129): "Let G = ⋃G_n be a σ-finite abelian group … 0 ∈ A … If d_U(A) > 0, then A is a basis for G′ of order at most … max(2, 2/d_U(A) − 1)."
- His Exercise 12 is the sharp example: in ℤ_m[x], the polynomials with constant term 0 or 1 have d_U(A) = 2/m and exact order m − 1 = 2/d_U(A) − 1. This is the polynomial twin of {n ≡ 0, 1 mod m}. (The book prints "2/n" there, apparently a typo for 2/m.)
- So 4/δ → 2/δ − 1 already happened in σ-finite groups (Jia–Nathanson 1994 → Hamidoune–Rødseth 1996). It is the same move as our 4⌈1/δ⌉ − 4 → ⌈2/δ⌉ − 1.

**Related, but about difference sets A − A.** Bienvenu–Girard–Lê (arXiv:2002.03919v3), Lemma 28: "Suppose … d(hA) = α > 0. Then there exists s ≤ (1/α)(h+1) − 1 such that sA − sA = ⟨A − A⟩."

## Q2. Restricted order in terms of density, after ENS 1988

Nothing found that gives c/δ.
- **Chen–Yu 2023** is by **Shi-Qiang** Chen and Wang-Xing Yu (not Yong-Gao Chen). There is no arXiv version, and ScienceDirect shows a captcha from exe.dev, Hetzner and the Mac. zbMATH 1518.11010: "if B is a set with lower asymptotic density greater than 1/2, then the restricted order of B is 2 and this statement is optimal."
- **Chen–Li 2026**, abstract: "if B … satisfies n/2 ≤ B(n) ≤ n/2 + k … then B ∪ (2×B) ∼ ℕ". Its reference list has no ENS 1988 and no Kneser.
- **Fang–Cheng 2025** (Disc. Math. 348, 114260): abstract not reached (zbMATH withheld, Semantic Scholar null). A search-engine summary I did not open says it is about bases with 2B = ℕ and restricted orders 3 and 4. Unverified.
- **Chen–Fang 2014**: not reached.
- Veljjanoski's 3⌈8/δ²⌉ − 2 remains the only other density bound for restricted order.

## Q3. Live state of #338

- **erdosproblems.com** (fetched through Hetzner, all HTTP 200): /338, /forum/thread/338 and /proof-claims are text-identical to the 15 Nov captures apart from the access date.
  - The page still says "last edited 14 September 2025".
  - 4 comments, the last on 1 Oct 2026; posting is still suspended.
  - 1 proof claim (Veljjanoski, 1 Oct).
  - The teorth database still lists the status as "open" (last update 2025-08-31).
- **The one change since 15 Nov:** formal-conjectures **#7779 was MERGED on 2026-11-15 at 22:42Z**. mo271 approved at 22:14Z, after bocowgill on 4 Nov. Merge commit 9406e4c3 adds `erdos_338.variants.lowerDensity_pos`, tagged `research solved` with the Palomar link.
  - Its hypothesis is "A \ F is a basis for every finite F" and positive lower density.
  - The docstring: "shown by Daniel Veljjanoski … with the bound 3⌈8/δ²⌉ − 2 … The linked formalisation proves the existence of a restricted order, not this bound."
- **Correction to the 15 Nov report:** #7620, #7783, #7784 and #6868 are OPEN with one approval each (bocowgill) and reviewDecision REVIEW_REQUIRED. "Open, approved" overstated them. #7788 is merged (8 Nov); #6793 is merged (19 Oct).
- **Palomar feed** (200 items, back to 4 Nov): no new #338 entry.
- **arXiv:** 15 API queries (restricted order, sums of distinct, distinct summands, asymptotic basis, additive basis, restricted sumset, Kneser plus density, Erdős 338, and others). Nothing relevant in the last 30 days. The nearest hits are 2610.25073 (finite h-fold restricted sumsets) and 2610.37136 (c₀(G) for finite groups); neither bears on the claim.

## Q4. Veljjanoski's note

No update. The repo still has one commit (9429d6f, 1 Oct 14:28Z), pushed 1 Oct; erdos338-palomar's last commit is 2 Nov.

Two lines in his README matter for credit:
- Line 65: "It cannot be better than about 2/δ: the set A = {n : n ≡ 0 or 1 (mod m)} …"
- Line 67: "Whether the right dependence on δ is linear in 1/δ is left open."

So the sharpness example is his.

## Bottom line

1. **May call new:** the bound ⌈2/δ⌉ − 1 for ℕ, *restricted* order and lower density, sharp when 2/δ is an integer. Even the ℕ ordinary-order version with an explicit 2/δ is not in print (only Ramaré–Ruzsa's O(1/δ)). It is not new that "filling the classes by Olson growth" turns 4/δ into 2/δ: that is Olson 1975/1984 and Hamidoune–Rødseth 1996 in σ-finite groups.
2. **Must credit:** ENS 1988 (Kneser form, distinct-summand device); Veljjanoski (set-aside residue elements, the {0, 1 mod m} lower bound); Kneser 1953; Varnavides 1959; Chen–Yu (δ > 1/2). Also Olson (Lemma 1 is his lemma; cite Hamidoune–Plagne 2004, Lemma 4.2), and Hamidoune 1981 / Rødseth 1982 / Hamidoune–Rødseth 1996 / Nathanson GTM 165 Thms 4.10–4.11 and Exercises 10, 12 / Klopsch–Lev 2009 for the finite and σ-finite 2/δ − 1 bound and its matching extremal example. Jia–Nathanson 1994 (4/δ) is the σ-finite precursor.
3. **Changes the claim:** CLAIMS' "What is ours" needs rewording, since Lemma 1 and the class-filling count are known in groups. One lead for the open non-integer case, not checked: Hamidoune–Rødseth get the sharper real bound max(2, 2/δ − 1), i.e. ⌊2/δ⌋ − 1, by finishing with the counting fact "G = AB or |G| ≥ |A| + |B|" (any non-cover leaves at least |A| + |B| elements) instead of one more Olson step. The same last step might close our gap to ⌊2/δ⌋ − 1.

Downloads are under `/tmp/world338b/`. The Hamidoune–Rødseth PDF and OCR are in `hr1996/`, the Nathanson page screenshots in `gb_shot/`, Klopsch–Lev in `kl/`. The Mac Chrome CDP tunnel was down; I reopened it (pid 1278382) and left it running.

Sources:
- [Ramaré–Ruzsa 2001](https://www.numdam.org/item/JTNB_2001__13_2_559_0.pdf)
- [Klopsch–Lev 2009, arXiv:0911.2966](https://arxiv.org/abs/0911.2966)
- [Klopsch–Lev 2003, arXiv:0911.2908](https://arxiv.org/abs/0911.2908)
- [Hamidoune–Plagne, CMH 2004](https://www.cmls.polytechnique.fr/perso/plagne.alain/2004-079-001-08.pdf)
- [Hamidoune–Rødseth 1996](https://journals.msp.org/mscand/article/view/1041)
- [Nathanson, GTM 165 (Google Books)](https://books.google.com/books?id=PqlQjNhjkKUC&pg=PA127)
- [Bienvenu–Girard–Lê, arXiv:2002.03919](https://arxiv.org/pdf/2002.03919)
- [Plagne, Ann. Inst. Fourier 2004](https://aif.centre-mersenne.org/article/AIF_2004__54_6_1717_0.pdf)
- [Nathanson, arXiv:1401.7598](https://arxiv.org/pdf/1401.7598)
- [Jayasuriya, arXiv:1210.6509](https://arxiv.org/html/1210.6509v2)
- [Lambert–Lê–Plagne, arXiv:1508.02662](https://arxiv.org/pdf/1508.02662)
- [Gao–Hamidoune, Acta Arith. 88](https://geodesic.mathdoc.fr/articles/10.4064/aa-88-3-233-237)
- [Chen–Yu (ScienceDirect, captcha)](https://www.sciencedirect.com/science/article/abs/pii/S0012365X23000742)
- [Fang–Cheng (ScienceDirect, captcha)](https://www.sciencedirect.com/science/article/abs/pii/S0012365X24003911)