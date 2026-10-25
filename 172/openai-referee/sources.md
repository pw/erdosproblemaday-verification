# Primary-source checks for the OpenAI #172 paper (fetched 2026-10-11, pdftotext -layout)

Each block is the verbatim text of the cited result in the CURRENT arXiv version, so the paper's use of it can be checked against the source rather than a memory of it.

## [37] Zorin-Kranich, arXiv:1206.0287v4 (latest version listed on arXiv: v4) — Corollary 3.7, used in §8.1 for the finite word plan
```
Corollary 3.7. Let G• be a filtration on a countable nilpotent group G, m ∈ N,
A ⊂ VIP(G• )⊗m a finite set, and l ∈ N>0 . Then there exists N ∈ N and finite sets
S, T ⊂ G such that for every l-coloring of T there exist α1 < · · · < αm ⊂ N and
s ∈ S such that the set {sg(~
                            α), g ∈ A} is monochrome (and in particular contained
in T ).

Proof. Let X := lG be the compact metrizable space of all l-colorings of G with the
right G-action xg(h) = x(gh). We apply Theorem 3.6 to this space, the system A,
the set H = ∅, and an  > 0 that is sufficiently small to ensure that ρ(x, x0 ) < 
implies x(eG ) = x0 (eG ).
   This yields certain N ∈ N and S ⊂ G that enjoy the following property: for every
coloring x ∈ X there exist α1 < · · · < αm ⊂ N and s ∈ S such that {sg(~    α), g ∈
A} is monochrome. Observe that this property only involves a finite subset T =
∪g∈A Sg(F(N )m < ) ⊂ G.                                                           

```

## [34] Tao–Ziegler, arXiv:1603.07815v4 (latest: v4) — Theorem 1.23, used as (5.11) in Lemma 5.5
```
Theorem 1.23 (Qualitative Bessel inequality for uniformity norms). Let (Qi )i∈I be a finite non-empty
family of coset progressions Qi , all of rank at most r, in an additive group G. Let (X, T ) be a G-system,
and let d be a positive integer. Let f lie in the unit ball of L∞ (X), and suppose that

                                               Ei, j∈I k f kU 2d−1             ≤ε                                         (15)
                                                              εQi +εQ j (X)


for some ε > 0. Then
                                                 Ei∈I k f kU d (X) ≤ c(ε)                                                 (16)
                                                              Qi


where c : (0, +∞) → (0, +∞) is a function such that c(ε) → 0 as ε → 0. Furthermore, c depends only on
r and d. (In particular, c is independent of the size of I.)
```

## [18] Green–Tao–Ziegler erratum (author-hosted, 2024) — what it corrects (the paper says it uses only the inverse conclusion, not Prop 8.3)
```
ERRATUM FOR “AN INVERSE THEOREM FOR THE GOWERS
                  U s+1 [N ]-NORM”


                BEN GREEN, TERENCE TAO, AND TAMAR ZIEGLER


        Abstract. We correct some minor issues in our paper An inverse theorem
        for the Gowers U s+1 [N ]-norm, Ann. Math 176 (2012), 1231–1372.




                                  1. Introduction
   In this erratum we correct some minor issues in [2]. These have come to light on
account of the close study of [2] made by James Leng, Ashwin Sah and Mehtaab
Sawhney in the course of preparing their work [3]. We are very grateful to James,
Ashwin and Mehtaab for drawing these issues to our attention and for discussions
relating to them.
   To keep the erratum relatively short we assume familiarity with the concepts
and notation of [2]. The primary issues in [2] are (with references here being to
that paper):

• Insufficient care was taken with the top groups in various filtrations, for example
  we allow filtrations G0 ⊃ G1 ⊇ . . . with G0 6= G1 , but this is best avoided for
  several reasons. One is that the equidistribution results of [1], cited in Appendix
  D, are stated with the condition G0 = G1 . This turns out to be a minor issue, in
  that the main statements of [1] continue to hold without this condition. However,
  somewhat more annoying problems arise with top-order Taylor coefficients (for
  instance in the display after (12.7) on page 1310), with final groups in such
  filtrations not necessarily being central (for instance on page 1311, or Example
  6.10) and with the fact that the degree of the filtration does not control the
  nilpotency class of G0 (an issue in Appendix C).
• The proof of Proposition 8.3 is incorrect, and this proposition does not hold as
  stated. The problem is with the deduction of (8.4). When π(g0 (n)∗ Γ) ∈ B, one
  can express g0 (n) = ι(xn )tn γn for some xn ∈ B, tn ∈ G(1,0) , and γn ∈ Γ, and
  then
               g(n, h) = ι(xn )tn γn g1 (n)h = ι(xn )tn (γn g1 (n)γn−1 )h γn ,
  which when combined with (8.3) gives
              χ̃k,k0 (n) = e(hξ(γn g1 (n)γn−1 mod Γ(1,0) ))F̃k,k0 (g0 (n)∗ Γ)
  rather than
                 χ̃k,k0 (n) = e(hξ(g1 (n) mod Γ(1,0) ))F̃k,k0 (g0 (n)∗ Γ)
  as claimed.
• Some minor issues in Sections 9–12 and Appendix E of the paper, at least one of
  which rises above the level of a mere typo.

  2020 Mathematics Subject Classification. 11B30.
                                            1
2                 BEN GREEN, TERENCE TAO, AND TAMAR ZIEGLER


These three bullet points are addressed in Sections 2, 3 and 4 respectively, with
the middle one of these being the most substantial. We note that all issues are also
fixed in [3]; in particular, we remark that the authors of that paper independently
found a fix for the second issue which is related to the one we shall present, though
a little different in the details.



                                   2. Filtrations
```

## [13] Green–Tao erratum, arXiv:1311.6170v3 (latest: v3) — the multiparameter Theorem 8.6 is proved only in the equal-sides case N1=…=Nt, which is the case Theorem 6.1 uses
```
Theorem [GT, Theorem 8.6]. Let 0 < δ < 1/2, and let m, t ⩾ 1,
N1 , . . . , Nt ⩾ 1 and d ⩾ 1 be integers. Write N        ~ = (N1 , . . . , Nt ) and
  ~ = [N1 ] ×· · · ×[Nt ]. Suppose that G/Γ is an m-dimensional nilman-
[N]
ifold equipped with a 1δ -rational Mal’cev basis X adapted to some filtra-
tion G• of degree d, and that g ∈ poly(Zt , G• ). Then either (g(~n)Γ)~n∈[N~ ]
is δ-equidistributed, or Ni ≪ δ −Od,m,t (1) for some i = 1, . . . , t, or else
there is some horizontal character η with 0 < kηk ≪ δ −Od,m,t (1) such
that
                                            −Od,m,t (1)
                          kη ◦ gkC ∞ [N]
                                      ~ ≪ δ             .
In the “equal sides” case N1 = · · · = Nt , the alternative Ni ≪ δ −Od,m,t (1)
may be deleted.
   Notation. We will not explicitly indicate the dependence of con-
stants C or implied constants O() on the parameters m, t and d, which
will remain fixed throughout this erratum. We will write I for the set
of multi-indices ~i = (i1 , . . . , it ) of total degree at most d, that is to say
tuples of non-negative integers with i1 + · · · + it ⩽ d.

                   2. Some results on polynomials
  In this section we record some useful distribution results on poly-
nomials which we will need in both of the proofs of [GT, Theorem
8.6].
  We start with some remarks about Taylor coefficients and smooth-
ness norms. If f : Zt → R is a polynomial map then in [GT, Definition
```

## [1] Alweiss, arXiv:2307.08901v6 (latest: v6) — Theorem 1.3 (the Q theorem) and Proposition 4.1 (compensating rescalings adapted in (8.1)–(8.2))
```
(not found)
Proposition 4.1. For any finite coloring χ of Q, any M , and any integer n ≥ 2, there are numbers
xn , xn−1 , xn−2 , · · · , x1 ∈ Q so thatQfor each Q
                                                   i ∈ [n] and T ⊆ [i−1] (possibly empty),
                                                                                        Q if P is good with
s(P ) ≤ M then the color of P (xi j∈T xj ; j∈S xj ) is the same as that of P (xi j∈T xj ), where S
consists of all nonempty subsets S of [i − 1] so that S > T .
```

## Versions on arXiv at fetch time
- 1009.3998 (GTZ inverse theorem): v1–v5 listed (v5 = the April 2026 revision the paper cites)
- 1206.0287 (Zorin-Kranich): v1–v4
- 2307.08901 (Alweiss over Q): v1–v6
- 1603.07815 (Tao–Ziegler concatenation): v1–v4
- 1311.6170 (GT erratum): v1–v3
- 2507.00515 (Richter): v1–v2
- 2210.12290 (Bowen–Sabok): v1

