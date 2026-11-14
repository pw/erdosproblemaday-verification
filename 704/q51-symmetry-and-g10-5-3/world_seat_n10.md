# χ(G(10,5,3)): does a printed 21-colouring or an upper bound below 30 already exist? (literature seat)

Checked 14 Nov 2026, about 10:00–10:15Z. This builds on `world_seat_q51.md`. New downloads are in `/tmp/ws51n/`.

## Verdict: NOT FOUND
There is no explicit 21-colouring, no proof that χ = 21 and no upper bound below 30. The printed upper bounds are **63** (by hand) and **30** (a greedy computer colouring), both from Kupavskii–Raigorodskii (KR) 2008.

## Primary texts read
1. **KR, Fundam. Prikl. Mat. 14:5 (2008)**. Quoted: "Теорема 4. … χ(G) ⩽ 63" ("Theorem 4. … χ(G) ⩽ 63"); "зазор между оценками 21 и 63 огромен" ("the gap between the bounds 21 and 63 is huge"); greedy colouring: "χ(G) ⩽ 30".
2. **Balogh–Kostochka–Raigorodskii, DMGT 33 (2013)**: "χ(R9) ≥ 21 is due to the fact that χ(G(10, 5, 3)) = 21 (see [4])". The cited [4] is KR, which proves only 21 ≤ χ ≤ 63. This is the only place where equality is asserted.
3. **Bobu–Kupriyanov, PPI 52:4 (2016)** (mathnet ppi2222). It covers G(n, n/2, s), which contains (10,5,3). Theorem 4 gives χ ≤ 2·C(2s+1, s+1), which is **70** at s = 3. Its only exact values are χ(G(6,3,1)) = 6 and χ(G(8,4,1)) = 5, the latter with an explicit colouring.
4. **Bobu–Kostina–Kupriyanov, PPI 51:2 (2015)** (ppi2172): G(n,r,r−1) and G(n,4,2) only.
5. **Raigorodskii–Sinelnikov-Murylev survey, UMN 80:3 (2025)**. The only mention is in §2.3.4: "[69], где найдены оценки хроматического числа графа с параметрами 10, 5, 3" ("[69], in which estimates of the chromatic number of the graph with parameters 10, 5, 3 were found"). These are estimates, not a value. The exact small values it cites ([66] = item 4) do not include (10,5,3).
6. **Cherkashin–Kulikov–Raigorodskii, arXiv:1512.03472v2 (DAM 243, 2018)**. G(10,5,3) is never mentioned. Their Prop. 1 gives **χ(R⁹) ⩾ χ(Q⁹) ⩾ 22** using a different graph: {−1,0,1}⁹ vectors of weight 3, adjacent at scalar product 1. So 21 has not been the R⁹ record since 2015/16.
7. **No mention of χ(G(10,5,3))** in any of these:
   - Bogolubsky–Raigorodskii, Mat. Zametki 105:2 (2019): Table 1 gives R⁹ ≥ 21.
   - Bogolubsky's 2020 thesis.
   - Kupavskii, Mat. Sb. 202:6 (2011) and Izv. RAN (2014).
   - Kalai, arXiv:1505.04952v1.
   - Kozhevnikov–Zhukovskii, arXiv:2203.03006v1.
   - Bachoc–Passuello–Thiery, arXiv:1401.6140v2: its α-table has (10,5,2), not (10,5,3).
   - Balogh–Cherkashin–Kiselev, arXiv:1805.09394v1.
   - Brešar et al., arXiv:1810.10198v1.
   - Zakharov, arXiv:1608.01873v1.
   - Prosanov, arXiv:1711.03193v2.

**Citation sweep.** I took every work citing KR from OpenAlex (12) and Semantic Scholar (9), and read all of them except two that are paywalled: Raigorodskii's "Coloring distance graphs…" (Thirty Essays, 2013) and "Cliques and cycles…" (Contemp. Math. 625, 2014). The 2025 survey above is his later, fuller account. zbMATH has no review text for KR (Zbl 1288.05093: "unavailable due to conflicting licenses"), and its BKR review does not mention (10,5,3).

## Online and computational sources
- **OEIS** (JSON search): no relevant sequence.
- **Brouwer's Johnson-graph page**: χ(J(10,5)) = 8, distance-1 graphs only.
- **MathOverflow and Math.SE** (API): nothing.
- **GitHub code search**, positive control passed: "G(10,5,3)", "G(10, 5, 3)", "J(10,5,3)", "J(10,5)" chromatic and "chromatic number of R^9" all return 0 hits.
- **House of Graphs**: web search only.
- **Web search** in English and Russian: nothing.

## Design-theory angle
I found nothing concrete. **Our own remark:** KR's colour classes are all 5-subsets of two 6-sets meeting in 2 points. Tiling the 252 5-sets with such classes would need an S(5,6,10), which does not exist (its derived S(4,5,9) needs 126/5 blocks). That is why their method stops at 63. Our classes are of a different shape.

## (A) Strongest honest sentence
"Kupavskii and Raigorodskii (2008) proved α(G(10,5,3)) = 12, so χ ≥ 21. They proved χ ≤ 63 by hand and reported χ ≤ 30 from a greedy computer colouring. Balogh, Kostochka and Raigorodskii (2013) state χ(G(10,5,3)) = 21, citing that paper. In the works we checked we found no published colouring with fewer than 30 colours and no proof of equality. Here is an explicit 21-colouring, which confirms the stated value."

## (B) Sentences to avoid
- "First proof", "new result", "settles an open problem" or "previously unknown". BKR stated 21 in print. Say "first exhibited colouring we could find".
- "BKR is wrong." The value is right; only the cited source lacks a proof.
- Anything linking this to χ(R⁹). That record is 22, from a different graph, and an upper bound on χ(G) is irrelevant to it.
- "Raigorodskii's 2013/2014 surveys are silent." We did not read them (paywalled).
- "Large set" or "design" for our colour classes.

Links: https://arxiv.org/abs/1512.03472 · https://www.mathnet.ru/eng/ppi2222 · https://www.mathnet.ru/eng/ppi2172 · https://doi.org/10.4213/rm10233 · https://www.mathnet.ru/eng/mzm11736 · https://doi.org/10.7151/dmgt.1641 · https://doi.org/10.1007/s10958-009-9708-4 · https://arxiv.org/abs/1810.10198 · https://aeb.win.tue.nl/graphs/Johnson.html
