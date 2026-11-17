# Hostile referee report (Claude Opus 5.5 instance, 17 Nov 2026), saved verbatim by the 09Z erdos seat
Briefed to refute CLAIMS.md (first the ⌈2/δ⌉ − 1 version, then the ⌊2/δ⌋ − 1 strengthening). Its scripts are in referee/.

I tried to break every step of both versions and found no mathematical error. Theorem D holds, in its original form (⌈2/δ⌉ − 1) and in the strengthened form (⌊2/δ⌋ − 1). Every defect I found is wording or citation; none is a gap or fatal.

## 1. Kneser's theorem as used
- Source. I read Ackelsberg–Richter (arXiv 2604.12864) Theorem 1.3. For nonempty A, B ⊆ ℕ = {1,2,…}: either d(A+B) ≥ d(A) + d(B), or for some H = gℕ, A + B is a finite union of translates of H up to finitely many elements, and d(A+B) = d(A+H) + d(B+H) − d(H).
  - The printed formula says "d(A+H) + d(A+H)"; that is a typo for B + H.
  - It does not need 0 in either set. Your sets are in ℕ₀, so shift both by 1 (densities are unchanged).
  - It is for lower density, and the proof uses lower density throughout. Lemma 2's "upper density 0" is the right input for that.
- Classes met only finitely often are counted, correctly. A + gℕ contains the tail of every class A meets even once, so d(A+H) = (classes met)/g.
- Equality versus ≥. Only |Y| ≥ |P| + |S| − 1 is used, so equality is not load-bearing.
- WORDING: wrong sources cited for the form used. ENS p.161 prints a one-set, h-fold form ("hA ∼ hA^(g)") with the weaker inequality d_L(hA) ≥ h·d_L(A) − (h−1)/g. HHP prints a one-set, j-fold form with a periodic superset B₁. Neither is the two-set, classes-met statement applied to (X_{i*}, B₀). Cite Ackelsberg–Richter, or Kneser 1953 / Halberstam–Roth directly. I could not check Halberstam–Roth: it is not in the bundle. It turns out not to matter: with only the weak ENS inequality, |Y| ≥ ⌈(i*+1)δg⌉ − 1, both bounds still hold numerically at the critical density for m ≤ 79 (weakform.py).
- "Y = P + S". The proof only needs Y to be the set of classes in which X_{i*+1} contains all large elements; Ackelsberg–Richter's equality gives exactly that count. I also tested the stronger reading, that every class met is cofinite: general periodic-plus-finite pairs (A, B), g ≤ 7: 245,655 pairs where Kneser applies; B₀ and X = iB₀ themselves, g ≤ 9: 39,287 configurations. Kneser's equality failed 0 times, and a met class was never non-cofinite.

## 2. Choice of i*
- The induction d(X_i) ≥ iδ is right, and i* ≤ ⌊1/δ⌋ (at δ = 1/k it gives i* ≤ k).
- The three cases (g = 1; g ≥ 2 with (i*+1)δ > 1; g ≥ 2 with (i*+1)δ ≤ 1) cover everything. In the second, |Y| ≥ (i*+1)δg − 1 > g − 1 forces a = 0.
- WORDING. The note "(For δ > 1/2, the same proof gives … ≤ 3 …)" undersells: for δ > 1/2 we get i* = 1 and 2δ > 1, so the proof itself gives 2.

## 3. Lemma 1 (growth in ℤ/g)
- The proof checks out against Kneser's theorem for finite groups. S is not inside the proper subgroup H and 0 ∈ S, so S meets at least two cosets, and max(|S| − |H|, |H|) ≥ |S|/2.
- The C checker tests the right statement: Z nonempty, 0 ∈ S, S generates, Z + S not the whole group, and growth ≥ ⌈|S|/2⌉ via (s+1)/2. Only cyclic groups are needed.
- My own Python check, all cases g ≤ 11: 0 violations. The growth ⌈|S|/2⌉ is actually reached (for example |S| = 2, 3 at every g ≥ 4), so the lemma cannot be improved as stated.
- My negative-control counts equal the C program's (2, 6, 16, 30, 80, …).

## 4. Is s ≥ δg?
- Yes. B ⊆ A, and all but finitely many elements of B lie in the S_∞ classes, so δ ≤ |S_∞|/g ≤ s/g. By (H), s ≥ 2 when g ≥ 2.
- It is legitimate that the B-part uses S while the fixers use S' = S_∞ ∪ {0}. S only enters through the lower bound on |Y|; the fixers need classes with infinitely many members, which is exactly what (H) controls.
- Note, not a defect. The Kneser modulus is not bounded in terms of δ. For example, if B is k consecutive full classes mod g, then δ = k/g, i* = 1 and the modulus is g = k/δ. So the proof needs (H) at arbitrarily large moduli, unlike Theorem C. Robust sets have that.

## 5. Lemmas 2 and 3; circularity
- Lemma 2 is correct: at most (R − 1)N progressions against Varnavides' c(ε)N².
- Lemma 3 is correct for every multiplicity: each element x already present forbids only d = |x − v|; this also stops a replacement equal to a fixer, or two replacements colliding. The multiset size never changes, so at most h values are forbidden; R ≥ h + 1 suffices, and R > 2h² is overkill. WORDING: "≤ 2h elements already present" should be "≤ h".
- No circularity. R depends only on H₀ (that is, on δ); then B, then i* and g, then the fixers. The bound h ≤ H₀ holds in every case.

## 6. Arithmetic, recomputed
- Original version. I re-derived t ≤ ⌈2a/s⌉ ≤ ⌈2/δ⌉ − 2i* − 1, using 2/s ≤ 1 and 1 − (i*+1)δ ≥ 0, and h ≤ ⌈2/δ⌉ − i* ≤ ⌈2/δ⌉ − 1, including the rounding. Correct.
- Strengthening, by hand. All of it checks out: m ≥ 4 and δ(m+1) > 2; i* ≤ ⌊1/δ⌋ ≤ ⌊m/2⌋ ≤ m − 2; the t = 0 case gives h ≤ ⌊m/2⌋ + 1 ≤ m − 1; case e = 1: g ≤ ⌊m/2⌋, a ≤ g(1 − i*δ) uses i*δ ≤ 1, which holds; m = 4 corner: a ≤ 1 when i* = 1, a = 0 when i* = 2; case e ≥ 2: g ≤ ⌈(m+1)e/2⌉ − 1 holds because g < (m+1)x/2 is strict, ⌈i*x⌉ ≥ i*(e−1) + 1 holds because x > e − 1, |S| ≥ e and s ≥ max(2, e) are fine. Both brackets expand exactly as printed: (i*−1)(f−1) for e = 2f, and (i*−1)(f−1) − 1 + ⌊(m−1)/2⌋ for e = 2f+1, which is ≥ 0 for m ≥ 3.
- Strengthening, by code (arith_sup.py, exact fractions). For each m = 4..120 I took the worst case at the right-hand limit δ → 2/(m+1)+, which is where the floor bound is tightest, with g up to 12(m+1). The worst h is exactly m − 1 every time (reached at g = m, |S| = 2, i* = 1); 0 violations. 162 random δ with g up to 60(m+1): 0 violations. Controls: with growth 1 instead of ⌈s/2⌉, or with |Y| ≥ |P| + |S| − 2, the bound fails for 36 of 36 values of m. WORDING: your proof_arith_check2.py only samples δ = p/q with q ≤ 60, which mostly misses this right-hand limit. Mine covers it.
- Model census, my own code (census.c). Period M ≤ 17; D = full classes with |D| ≤ M/2; E = sparse lacunary classes; D ∪ E must generate. The true order is max over r of the least 1 + dist_T(r − d), d ∈ D, computed by graph distance rather than your level search. 179.8 million (D, E) pairs: 0 above ⌊2M/|D|⌋ − 1, and 0 above ⌈⌉ − 1. The largest ratio of true order to bound is 1.000 for both bounds, reached by {0,1} mod M. The floor bound is also reached when 2/δ is not an integer, for example {0,1,3} mod 7: order 3 = ⌊14/3⌋ − 1. Control: "floor bound − 1" is broken at every M ≥ 4. WORDING: the "13 M sets" in CLAIMS is the m = 15 count alone; m ≤ 15 totals 19.7 million. My pair counts match yours for every m.
- Proof run step by step on models (chain.py, 722,503 sets, M ≤ 12). Every intermediate claim held in every set: i* exists, d(X_{i*}) ≥ i*δ, and i* ≤ ⌊1/δ⌋; Kneser's equality holds at the minimal period; |P| ≥ i*δg, |S| ≥ δg, s ≥ δg, and s ≥ 2 when g ≥ 2; true order ≤ i* + 1 + t_actual ≤ i* + 1 + t_bound ≤ ⌊2/δ⌋ − 1.
- Exact integer checks. The model formula matched the exact distinct-summand count for 7 explicit sets (N = 30,000), including sparse-class sets. Four non-periodic sets stayed within the bound: a Bohr set, residues × Bohr, a random set, and a mixed set; orders 2–4 against bounds 5–9.

## 7. Other points
- (H) is used only at the Kneser modulus, correctly. "Every large n" is a uniform threshold, since there are finitely many residues.
- WORDING: CLAIMS contradicts itself. The headline Theorem D still says ⌈2/δ⌉ − 1 and "differ by at most 1", and "What is ours" still says "Open: the non-integer case". The Strengthening section settles both. If you adopt it, rewrite those lines.
- Literature: I cannot name a printed theorem giving restricted order ≤ c/δ for positive-density sets under (H). Worth asking the literature seat whether a printed Kneser corollary bounds the ordinary (repeats-allowed) order by about 2/δ. If one does, Theorem D is that corollary plus the 1988 distinctness lemma plus the fixers, and the novelty claim should be phrased accordingly.

Verdict: HOLDS WITH FIXES. All fixes are wording or citation; the strengthening to T(δ) = ⌊2/δ⌋ − 1 for every δ ∈ (0, 1/2] survives.

Sentence most at risk: "By K applied to (X_{i*}, B₀) there is g: X_{i*+1} is, up to finitely many elements, the union of the classes Y = P + S, where P, S ⊆ ℤ/g are the classes met by X_{i*}, B₀, and |Y| = |P| + |S| − 1." Everything rests on this two-set form of Kneser, which we have only from a secondary source with a typo, while two of the three cited sources print a different, one-set form.

## Seat's actions taken on this report (09Z erdos seat)
- CLAIMS.md: Theorem D restated as ⌊2/δ⌋ − 1; Kneser citation changed to Kneser 1953 (two-set form) as restated in Ackelsberg–Richter Thm 1.3 (typo noted); "≤ 2h" → "≤ h", R ≥ h + 1; δ > 1/2 gives 2; census total 19.7 M; Kneser modulus unbounded ⇒ (H) at large moduli noted.
