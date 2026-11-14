# #704 Question 5.1 (is χ(J(13,5,3)) = 39?): world / literature seat

Checked 14 Nov 2026, about 09:30–10:00Z. This builds on `../world_seat.md` (13 Nov) and does not repeat it. Raw downloads are in `/tmp/ws51/`.
Labels: CONFIRMED = quoted from a primary source. NOT FOUND = the places searched are listed. UNVERIFIED = could not be settled.

## 1. Has anyone addressed χ(J(13,5,3)) or the partition question?

**NOT FOUND anywhere.**
- **Stanikzai's own material has not been updated.** He has no public code repository; the deposit is Zenodo. The Zenodo API for record 24145863 shows exactly one version (1.0.0): created 2026-11-11T23:44Z, metadata updated 2026-11-12T13:59Z, 42 downloads. Hexagon https://hexagonmath.org/2611.00358 is still "Version 2 / Nov 12, 2026", and `…/2611.00358v3` returns 404. The paper's only statement on Q5.1 is the question itself (tex lines 683–688). His deposit tried colourings only on leaf subgraphs: `R/out/color_attempts*.csv` covers cubes of the T₃₃ and T₄₆ trees and is marked "no certificate (proves nothing)". He gives **no colouring of the full J(13,5,3) and no upper bound on χ**.
- **arXiv** (API, sorted by date): searches for `Stanikzai` (one unrelated 2022 hit), `"generalized Johnson graph"`, `"Johnson graph" AND chromatic`, `"distance graph" AND chromatic`, `"chromatic number" AND Euclidean`, `"unit-distance graph"`, `"forbidden intersection"` and `"Kneser-type"`. The newest relevant hits are 2611.10735 and 2611.06269 (both about the plane). Nothing mentions (13,5,3).
- **GitHub** code search for `J(13,5,3)`: apart from our own repos, the only hit is an automated paper digest (`cxy0714/research-news`, docs/daily/2026-11-13.md) that lists the Hexagon paper with "相关性 2/10" ("relevance 2/10"). Repository searches for "Stanikzai", "generalized Johnson graph chromatic" and "chromatic number R^12" found nothing relevant.
- **MathOverflow** (StackExchange API): nothing on generalized Johnson graphs since 2015 (question 145904, about naming), and nothing on the Euclidean chromatic number since 1 Nov 2026.
- **Polymath16 thread 18**: the newest comment is still domotorp, 5 Nov 2026. No 19th thread exists (blog feed checked).
- **Web search** for "J(13,5,3) chromatic", "Stanikzai … R^12 39" and "hexagonmath 2611.00358": no third-party discussion.
- One search-engine hit, preprints.org 202608.0921, could not be opened from either of our machines. UNVERIFIED, but it is very unlikely to bear on this.

## 2. Upper bounds in the literature that apply to (13,5,3)

None gives a usable number. These are the ones worth citing:
- **Trivial bounds.** Brooks gives χ ≤ Δ = C(5,3)·C(8,2) = 280. Lovász's bound for vertex-transitive graphs, χ ≤ (1+ln α)·|V|/α, gives (1+ln 33)·39 ≈ 175.4, so χ ≤ 175. Cherkashin quotes that inequality as eq. (2) in arXiv:2508.19775v1. Our N ≈ 45–50 beats both by a wide margin.
- **Zakharov, arXiv:1811.10567v4 (13 Dec 2019; J. Combin. Theory Ser. A 172 (2020)).** Theorem 1.1: "Let r > s. Then χ(G(n,r,s)) ⩽ (1+o(1)) n^{r−s} (r−s−1)!/(2r−2s−1)! as n → ∞." It is asymptotic only, via Keevash, and for (5,3) the leading term n²/6 ≈ 28 at n = 13, which is below the true lower bound of 39. **Do not quote it as a bound at n = 13.** His Claim 2.1, which is not asymptotic, is relevant in spirit. It says: if an (n, 2r−s−1, r)-design decomposes into (n, 2r−s−1, s)-designs, then χ(G(n,r,s)) ≤ N. Its colour classes are "all r-subsets of the blocks of a packing". For (13,5,3) the required S(5,6,13) does not exist (C(13,5)/6 = 214.5), so the claim gives nothing here. Our W does contain three such 6-set blocks B_i.
- **Kupavskii–Raigorodskii, "On the chromatic number of R⁹", Fundam. Prikl. Mat. 14:5 (2008) 139–154 = J. Math. Sci. 163:6 (2009) 720–731.** This is the closest precedent: **G(10,5,3)**. Theorem 2 gives α(G) = 12, so χ ≥ 252/12 = 21. Theorem 4: "χ(G) ⩽ 63", proved with colour classes covered by pairs of 6-sets meeting in 2 elements. Also: "Был также реализован стандартный «жадный» алгоритм … Вычисления показали, что χ(G) ⩽ 30" ("a standard greedy algorithm was also run … computations showed χ(G) ⩽ 30"). The authors call the 21–63 gap "огромен" ("huge").
  ⚠ **Citation discrepancy.** Balogh–Kostochka–Raigorodskii, DMGT 33 (2013) 25–31, p. 29, writes "χ(G(10,5,3)) = 21 (see [4])", where [4] is the Kupavskii–Raigorodskii paper. That source proves only 21 ≤ χ ≤ 63 (and ≤ 30 by computer). I found no proof that χ(G(10,5,3)) = 21. The 2025 Raigorodskii–Sinelnikov-Murylev survey says only that [69] "найдены оценки" ("found estimates"). This is the exact n = 10 analogue of Q5.1: can the vertex set be partitioned into |V|/α maximum independent sets? It has 252 vertices, so **a math seat could settle it in minutes**. Either answer is a good sentence for the page.
- **BKR 2013 on G(13,3,1)** (a different graph): "the proof of Theorem 3 applied for n = 13 yields a bound χ(G13) ≤ 31", against a lower bound of 24. This shows that small-n upper bounds of this kind are rare and loose.
- Koshelev, arXiv:2610.13723v2, is about the *list* chromatic number for r ≥ 2s+2, outside our regime. Luo–Cao–Li–Li, arXiv:2609.04677v1 (the quantum chromatic number), covers the families J(4r, 2r−a, r−a); 13 is not of the form 4r. Neither applies.

## 3. The χ(ℝ¹²) lower bound as of today

Unchanged from 13 Nov. The printed refereed explicit-graph record is 37 (Cherkashin–Kulikov–Raigorodskii, DAM 243 (2018)). The abs page for Davies, arXiv:2610.12301, still shows only "[v1] Thu, 8 Oct 2026 16:50:24 UTC (78 KB)": an unrefereed preprint claiming 164 (with BPT) and 2,516, with no exhibited graph. Bikeev–Voronov–Raigorodskii is still v2. Nothing newer than Stanikzai's 39 has been exhibited.

## 4. The live Erdős page (fetched 14 Nov)

`/704`: "This page was last edited 10 April 2026", with "Comments (5)". `/forum/thread/704` has the same 5 comments; the newest is from pollodumas at 21:10 on 22 Jul 2026, and the thread still says "The ability to post new comments has been suspended." **There are no comments from the last 14 days, and none on ℝ¹², J(13,5,3) or Stanikzai.** In teorth/erdosproblems, 704 is still `open`, last_update 2025-08-31.

## 5. Terminology

The standard name is **an F-decomposition (F-design) of the complete 5-uniform hypergraph K₁₃⁽⁵⁾**, where F is the 33-edge hypergraph W: the 5-sets are split into edge-disjoint copies of F. See Glock–Kühn–Lo–Osthus, "The existence of designs via iterative absorption: hypergraph F-designs for arbitrary F", arXiv:1611.06827v3. That result only covers sufficiently large n. When F is itself a Steiner system, such a partition is called a **large set** of designs (Keevash, arXiv:1802.05900v1, abstract: "large sets of hypergraph designs"). W is not a design, so "large set" would be wrong here. "W-decomposition of K₁₃⁽⁵⁾" is accurate.

## What the page may claim as OURS

(a)–(d) as computed today, worded as "we checked/found", plus "we found no earlier colouring or upper bound for χ(J(13,5,3)) in [the places listed]". A sentence we can support: "Our N-colouring is far below the general bounds that apply (280 from Brooks, 175 from Lovász's vertex-transitive bound)."

## Sentences to avoid

- Any "first upper bound" or "first colouring" of J(13,5,3). That is an absence claim; say "we found no earlier one".
- "χ(G(10,5,3)) = 21 is known." Its source proves 21–63. Use it only after our own check, and cite it as such.
- Zakharov's n²/6 as a bound at n = 13.
- "Partial progress on Erdős #704." Q5.1 is Stanikzai's question about one graph. A "no" would raise the explicit-graph bound for ℝ¹² to 40. It touches neither Davies's 2,516 nor #704's limit question.
- "Large set of W", and "Stanikzai's repository": he has only a Zenodo deposit.
