# #338 follow-up (a), 2026-11-17 (09Z erdos seat, Opus 5.5, Team seat 3): the density bound is 2/δ − 1, sharp

## Setting (as in the 15 Nov entry)
A ⊆ ℕ = {1,2,…}, lower asymptotic density d(A) = δ > 0.
(H) for every modulus g, the residue classes mod g that contain infinitely many members of A generate ℤ/g under
addition. (Robust sets satisfy (H); this is the hypothesis of Veljjanoski's Theorem 1.)
T(δ) := sup over such A with d(A) ≥ δ of the restricted order (least t: every large n is a sum of at most t
DISTINCT members of A).
Known before today: ⌊2/δ⌋ − 1 ≤ T(δ) ≤ 4⌈1/δ⌉ − 4 (δ ≤ 1/2), lower bound from {n ≡ 0,1 mod m}.

## Theorem D (label (b): rigorous modulo Kneser's density theorem (1953) and Varnavides' counting form of Roth's theorem (1959))
For 0 < δ ≤ 1/2: every large integer is a sum of at most ⌊2/δ⌋ − 1 distinct members of A, and T(δ) = ⌊2/δ⌋ − 1.
(The fractional count below gives ⌈2/δ⌉ − 1; the integer bookkeeping in "Strengthening" gives ⌊2/δ⌋ − 1.
For δ > 1/2 the same proof gives 2: i* = 1 and 2δ > 1 force t = 0.)  [referee 17 Nov: HOLDS WITH FIXES, all wording]

## Tools
K (Kneser, lower asymptotic density). For nonempty A, B ⊆ ℕ₀: either d(A+B) ≥ d(A) + d(B), or there is g ≥ 1 such that
A + B coincides, up to finitely many elements, with a union of residue classes mod g, and
d(A+B) = d(A + gℕ₀) + d(B + gℕ₀) − 1/g. [Kneser 1953 (two-set form), as restated in Ackelsberg–Richter arXiv:2604.12864 Thm 1.3 (whose printed
"d(A+H) + d(A+H)" is a typo for d(A+H) + d(B+H)); no 0 needed (shift by 1). ENS 1988 p.161 and HHP 2007 print a
one-set h-fold form instead; only |Y| ≥ |P| + |S| − 1 is used, not equality.] Note d(X + gℕ₀) = (number of classes mod g met by X)/g.
KG (Kneser in a finite abelian group G). |X + Y| ≥ |X + H| + |Y + H| − |H|, H = stabiliser of X + Y.
V (Varnavides 1959). For ε > 0 there is c(ε) > 0: any C ⊆ [1,N] with |C| ≥ εN contains ≥ c(ε)N² three-term APs (N ≥ N₀(ε)).

## Lemma 1 (growth in ℤ/g; = OLSON's lemma, Olson JNT 18 (1984), as stated in Hamidoune–Plagne CMH 79 (2004) Lemma 4.2:
## |Z + S| ≥ min(g, |Z| + |S|/2)). If 0 ∈ S ⊆ ℤ/g, S generates ℤ/g, and Z + S ≠ ℤ/g, then |Z + S| ≥ |Z| + ⌈|S|/2⌉.
(The hypothesis Z + S ≠ ℤ/g is essential: without it the statement is false, e.g. S = ℤ/g, |Z| = g − 1.)
Proof. H = Stab(Z+S) is a proper subgroup (else Z+S = ℤ/g). S ⊄ H (S generates), and 0 ∈ S, so S meets ≥ 2 cosets of
H: |S + H| ≥ max(|S|, 2|H|). By KG, |Z+S| ≥ |Z| + max(|S|, 2|H|) − |H| = |Z| + max(|S| − |H|, |H|) ≥ |Z| + ⌈|S|/2⌉.
[Checked exhaustively for g ≤ 12: growth_lemma_check.c; controls: drops without generation, and the sharper
|S| − 1 version fails for composite g.]

## Lemma 2 (good centres). Fix R. Let B = {a ∈ A : a is the middle term of at least R three-term APs inside A}.
Then A \ B has upper density 0; so d(B) = d(A) = δ.
Proof. If C = A \ B had upper density ≥ ε along N → ∞, V gives ≥ c(ε)N² 3-APs in C ∩ [1,N]; each is an AP in A whose
middle term lies in C and so is the middle of < R APs in A; at most R·N such APs. Contradiction for large N.

## Lemma 3 (making summands distinct). Let n = f₁ + … + f_t + b₁ + … + b_u with f_i ∈ A pairwise distinct, b_j ∈ B
(repetition allowed), t + u ≤ h, and R ≥ h + 1. Then n is a sum of t + u distinct members of A.
Proof. For each value v, let c_v = number of occurrences of v among all f's and b's. If c_v ≥ 2 then v = some b_j ∈ B
(the f's are distinct). Write c_v = 2j + ε (ε ∈ {0,1}); keep v ε times and replace the other 2j copies by
v ± d₁, …, v ± d_j: same sum. Choose the d's one value at a time, one d at a time; each choice must avoid the
≤ h elements already present (each forbids at most one d, namely |x − v|), so R ≥ h + 1 suffices.
All new elements lie in A and are distinct from each other and from everything else.

## Proof of Theorem D
H₀ := ⌈2/δ⌉ − 1 (an upper bound for every case below). Fix R ≥ H₀ + 1, let B be as in Lemma 2, d(B) = δ, B₀ = B ∪ {0}, X_i = iB₀ (sums of at most i members
of B, repetition allowed; X_i ⊆ X_{i+1}). Let i* ≥ 1 be least with d(X_{i*} + B₀) < d(X_{i*}) + δ.
It exists and d(X_{i*}) ≥ i*δ: by induction d(X_i) ≥ iδ for i ≤ i*, and densities are ≤ 1, so i* ≤ ⌊1/δ⌋.
By K applied to (X_{i*}, B₀) there is g: X_{i*+1} is, up to finitely many elements, the union of the classes Y = P + S,
where P, S ⊆ ℤ/g are the classes met by X_{i*}, B₀, and |Y| = |P| + |S| − 1.
  |P| ≥ i*δg (X_{i*} lies in its classes and has density ≥ i*δ); |S| ≥ δg (likewise).
Let S_∞ = classes mod g containing infinitely many members of A, S' = S_∞ ∪ {0}, s = |S'|.
  B minus finitely many elements lies in classes of S_∞ (B ⊆ A), so δ ≤ |S_∞|/g ≤ s/g, i.e. g/s ≤ 1/δ.
  By (H), S' generates ℤ/g; if g ≥ 2 then s ≥ 2.
By Lemma 1 (applied to Z = Y + uS', u = 0,1,…), Y + tS' = ℤ/g with t = ⌈a/⌈s/2⌉⌉, a := g − |Y|.
Representation. Fix, for each residue r mod g, y_r ∈ Y and c₁,…,c_t ∈ S' with r = y_r + Σc_i; for each c_i ≠ 0 pick
a member of A in class c_i, all picks distinct (classes in S_∞ are infinite). This is a finite set of choices.
For large n ≡ r: n − Σ(picks) is large and ≡ y_r, so lies in X_{i*+1}: a sum of at most i*+1 members of B.
Lemma 3 (h = i* + 1 + t) makes all summands distinct. So every large n is a sum of at most h = i* + 1 + t distinct members.
Counting. If g = 1: t = 0, h = i* + 1 ≤ ⌊1/δ⌋ + 1 ≤ ⌈2/δ⌉ − 1 (δ ≤ 1/2).
If g ≥ 2 and (i*+1)δ > 1: a ≤ g − (i*+1)δg + 1 < 1, so a = 0, t = 0, h = i* + 1 ≤ ⌊1/δ⌋ + 1 ≤ ⌈2/δ⌉ − 1.
If g ≥ 2 and (i*+1)δ ≤ 1: a ≤ g(1 − (i*+1)δ) + 1, t ≤ ⌈2a/s⌉, and
  2a/s ≤ (2g/s)(1 − (i*+1)δ) + 2/s ≤ (2/δ)(1 − (i*+1)δ) + 1 = 2/δ − 2i* − 1,
  so t ≤ ⌈2/δ⌉ − 2i* − 1 and h ≤ i* + 1 + t ≤ ⌈2/δ⌉ − i* ≤ ⌈2/δ⌉ − 1.   ∎
(H₀ was fixed before B so that R does not depend on the run of the argument; h ≤ H₀ in every case.)


## ★ Strengthening (added ~10:2xZ): integer bookkeeping gives ⌊2/δ⌋ − 1, so T(δ) = ⌊2/δ⌋ − 1 EXACTLY for every δ ∈ (0, 1/2]
Same proof; only the final count changes. Let m = ⌊2/δ⌋ ≥ 4, so δ(m+1) > 2. Goal: h = i* + 1 + t ≤ m − 1.
(i) i* ≤ ⌊1/δ⌋ ≤ ⌊m/2⌋, because 1/δ < (m+1)/2. Hence if t = 0 (in particular g = 1): h = i* + 1 ≤ ⌊m/2⌋ + 1 ≤ m − 1.
(ii) g ≥ 2. Put x = δg, e = ⌈x⌉. Then |S| ≥ e, s ≥ max(2, e) (both are integers ≥ x), |P| ≥ ⌈i*x⌉, and
     g < (m+1)x/2 (from δ(m+1) > 2). It suffices to show a ≤ (m − 2 − i*)·⌈s/2⌉ (then t ≤ m − 2 − i*); note m − 2 − i* ≥ 0.
     Use a ≤ g + 1 − ⌈i*x⌉ − e.
  e = 1 (x ≤ 1): g ≤ ⌈(m+1)/2⌉ − 1 = ⌊m/2⌋ and a ≤ g − ⌈i*x⌉ ≤ g(1 − i*δ) < (m/2)(m+1−2i*)/(m+1) < (m+1−2i*)/2.
     For m ≥ 5, (m+1−2i*)/2 ≤ m − 2 − i*; for m = 4, a < (5 − 2i*)/2 gives a ≤ 2 − i* (i* ∈ {1,2}). And ⌈s/2⌉ ≥ 1.
  e ≥ 2: g ≤ ⌈(m+1)e/2⌉ − 1 (since x ≤ e) and ⌈i*x⌉ ≥ i*(e−1) + 1 (since x > e − 1); ⌈s/2⌉ ≥ ⌈e/2⌉.
     e = 2f:   (m−2−i*)f − [ (m+1)f − 1 + 1 − (2i*f − i* + 1) − 2f ] = (i* − 1)(f − 1) ≥ 0.
     e = 2f+1 (f ≥ 1): (m−2−i*)(f+1) − [ (m+1)f + ⌈(m+1)/2⌉ − 1 + 1 − (2i*f + 1) − (2f+1) ]
                     = (i* − 1)(f − 1) − 1 + ⌊(m−1)/2⌋ ≥ 0  (m ≥ 3).
So every large integer is a sum of at most ⌊2/δ⌋ − 1 distinct members of A; {n ≡ 0, 1 mod ⌊2/δ⌋} (density ≥ δ) needs
exactly that many. [Second route: proof_arith_check2.py enumerates the proof's integer constraint system for all
551 δ = p/q ≤ 1/2 with q ≤ 60, g ≤ 60/δ: worst case = ⌊2/δ⌋ − 1 at every δ, never above. Model census
model_census.c (periodic + sparse classes, m ≤ 15, 19.7 M sets in all): true order never exceeds ⌊2/δ⌋ − 1; ⌈⌉ − 2 violated (control).]

## Sharpness
{n ≡ 0,1 mod m} (δ = 2/m, satisfies (H)) has restricted order exactly m − 1 = 2/δ − 1.

## What is ours / what is not (rewritten after the literature seat, 17 Nov)
- Kneser 1953, Varnavides/Roth 1959 and the repeated-summand → AP device are ENS 1988's tools (they used Szemerédi;
  Roth suffices by pairing). The residue-fixing members set aside per class are Veljjanoski's step 3; the sharp example
  {0,1 mod m} is his (README line 65).
- Lemma 1 is OLSON's lemma (Olson, JNT 18 (1984); stated as Hamidoune–Plagne, CMH 79 (2004), Lemma 4.2).
- The class-filling count that turns ~4/δ into 2/δ − 1 is already in print for σ-finite groups: Hamidoune–Rødseth,
  Math. Scand. 78 (1996): order ≤ max(2, 2/δ − 1) (improving Jia–Nathanson 1994's 4/δ); = Nathanson GTM 165 Thm 4.11,
  Exercise 12 gives the extremal polynomials with constant term 0 or 1.
- Ours: the integer case (lower asymptotic density, Kneser supplies the modulus) for RESTRICTED order under (H), with
  the integer bookkeeping that makes it exactly ⌊2/δ⌋ − 1. Not found in print for ℕ even for ordinary order
  (Ramaré–Ruzsa 2001: O(1/δ), no constant).
- Open: question (b) (bounded in the order h alone); density zero. Note (referee): the Kneser modulus is not
  bounded in terms of δ (k consecutive full classes mod g: g = k/δ), so the proof uses (H) at arbitrarily large moduli,
  unlike Theorem C; robust sets have that.

## ★ Simplest form of the count (blind reader, 17 Nov; this is the version on the page)
Z₀ = T (|T| ≥ (k+1)δg − 1), Z_i = Z_{i−1} + S′, j = first i with Z_i = ℤ/g. Total ≤ k + 1 + j.
j = 0: ≤ ⌊1/δ⌋ + 1 ≤ ⌊2/δ⌋ − 1 (δ ≤ 1/2). j ≥ 1: Z_{j−1} ≠ ℤ/g so |Z_{j−1}| ≤ g − 1, and steps 1..j−1 each gained ≥ s/2 ≥ δg/2:
g − 1 ≥ (k+1)δg − 1 + (j−1)δg/2 ⇒ j ≤ 2/δ − 2k − 1 ⇒ total ≤ 2/δ − k ≤ 2/δ − 1 ⇒ (integer) ≤ ⌊2/δ⌋ − 1.
(The fractional count earlier lost the +1 by bounding the deficit by g − |Y| with a ceiling; the "Strengthening" case
analysis recovers it the long way. Both are correct; this one is shorter.)

## Literature added by the blind reader (17 Nov)
- Hegarty, J. Number Theory 129 (2009) 3052–3058 (arXiv:0904.1871v2), Lemma 3.3: S ⊆ ℤ, |S ∩ ℤ⁻| < ∞, d(S) > 0,
  S an asymptotic basis ⇒ G(S) ≤ 4/d(S); proof = Kneser on 2^j S, then Klopsch–Lev |A|·ρ(A) < 2n in ℤ/n. (Read by
  the seat, lines 229–242 of the pdftotext.) So an explicit c/δ for integer ORDINARY order IS in print (c = 4);
  ours improves it to the exact ⌊2/δ⌋ − 1 and gives it for RESTRICTED order under (H).
- Chen–Yu (Shi-Qiang Chen, Wang-Xing Yu), Discrete Math. 346 (2023) 113388: lower density > 1/2 ⇒ restricted order 2.
