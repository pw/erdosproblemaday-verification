# Literature search: is "no blocking set of PG(2,13) has all line intersections <= 4" known?

Date of search: 2026-10-14. Searcher: sub-agent (WebSearch/WebFetch + curl). Budget ~25 min.

## VERDICT

**NOT FOUND** (neither KNOWN-YES nor KNOWN-NO) for the statement
"no blocking set of PG(2,13) has all line intersections <= 4".

What IS established (c = least C such that some blocking set meets every line in 1..C points):

* **c(PG(2,13)) <= 5 is KNOWN-YES with an explicit published witness**: Illes and Pisinger's 24-point blocking set,
  line intersection distribution 1:117, 2:9, 3:33, 4:18, 5:6 (published table AND the published point file; I re-verified it,
  see section A and B).
* **c(PG(2,13)) >= 4 by pure counting** (my own arithmetic, section E): max intersection 3 is impossible, so c is 4 or 5.
* Whether c = 4 is **not settled in any source I could open**. The only evidence about 4 is search-negative:
  a simulated-annealing heuristic (10 restarts) did not find one at q=13 (it did at q=7,8,9,11), and a non-exhaustive
  census of (k,4)-arcs in PG(2,13) found none with fewer than 9 external lines. Neither is a nonexistence proof.

Coverage caveats are listed in section G (several primary sources could not be opened). "Not found" below is a COVERAGE
statement about what I could read, not evidence of nonexistence.

---

## A. Illes and Pisinger, DIKU Technical Report 97-13 (OPENED, full text read)

* URL: https://www.di.ku.dk/forskning/Publikationer/tekniske_rapporter/tekniske-rapporter-1997/97-13.pdf (16 pp, downloaded and pdftotext'd)
* Title: "Upper bounds on the covering number of Galois-planes with small order", T. Illes and D. Pisinger.
  Journal version: Journal of Heuristics 7:59-76 (2001) (bib record: https://hjemmesider.diku.dk/~pisinger/publications/class_type.html ; Crossref confirms vol 7, pp 59-76). Journal text NOT opened (Springer blocks).
* Conventions (quoted): "A projective plane Pi(q) has property B(gamma) if there is a blocking set B whose intersection with each line of Pi(q) contains less than gamma points. For a blocking set B, rho(B) denotes the maximum number of collinear points of B, and rho(B) is called the covering number of the blocking set B." and "gamma(Pi(q)) = 1 + min_B rho(B)" (eq. 8). (Greek letters are garbled in the pdftotext output; the meaning is unambiguous from the surrounding text and from the numeric check below.)
  So rho = max line intersection, gamma = rho + 1. The question asked here is rho(PG(2,13)) in {4,5}.
* Table 1 ("General information about the found solutions"), row for q=13, quoted verbatim from the extracted text:
  `13    183    24      5    1.95 2262`   (columns: q, n=q^2+q+1, |B|, rho(B), rho/ln q, t seconds).
  Control that rho(B) is the max line intersection: 5/ln(13) = 1.949, matching the printed 1.95.
  Neighbouring rows: `7 57 12 4`, `8 73 19 4`, `9 91 13 4`, `11 133 21 4 1.67 54`, `16 273 33 5`. So the heuristic reached max intersection 4 for q=7,8,9,11 and only 5 for q=13.
* Table 3 ("Geometrical properties", numbers of i-secants of the best set found), row q=13: `13 117 9 33 18 6`
  (117 tangents, 9 bisecants, 33 3-secants, 18 4-secants, 6 5-secants; sum = 183 lines).
* Sentence on strength of the result: "Thus we have shown that projective planes of order q, 7 <= q <= 607, q prime or prime power, has covering number (rho(Pi(q))) < 2 ln(q). This does not answer Erdos problem, but may help future investigation." (this is an upper-bound statement only).
* Heuristic nature: "we propose a heuristic based on simulated annealing"; "each problem was restarted 10 times"; "The total CPU time used for this series of tests was more than 38 days." The q=13 run: 10 restarts gave |B| = 24..29, best (rho=5, |B|=24); the file reports `time = 2261.78` (seconds) for the q=13 block. No optimality or nonexistence claim for any q.
* On the literature at that date: "the only computational investigation is due to Beres and Illes [2] for small prime orders up to q = 89."
  and "Figure 2 shows that our numerical experiences does not give indication of existence (or non-existence) of absolute constant."
* The report also reproduces (Result 1, Beres-Illes) the size window for a minimal blocking set with a given covering number; with their gamma-hat = rho+1 convention it gives, at q=13 and rho=4, 19.5 <= |B| <= 37.5, which agrees with my own counting in section E.

## B. Illes-Pisinger found-solutions file: the explicit witness (OPENED, independently VERIFIED)

* Page: http://www.diku.dk/~pisinger/erdos.html (now served at https://hjemmesider.diku.dk/~pisinger/erdos.html; "Last Update: January 5, 1998"). Quote: "People studying covering numbers of blocking sets of finite projective planes may wish to see the solutions we found. They are available as a compressed file (664kB). The file contains the best found blocking sets, as well as the corresponding difference sets."
* File: https://hjemmesider.diku.dk/~pisinger/output.c.gz (gunzip -> erdos.out, 1,675,176 bytes). The q=13 block (verbatim):
  ```
  SOLUTION: 6 (alpha 4)
  q    = 13
  n    = 183
  alfa = 4
  gam  = 5
  y[1] = 117  y[2] = 9  y[3] = 33  y[4] = 18  y[5] = 6
  |B|  = 24
  difference set:
  5,19,31,37,61,64,65,84,100,105,113,115,122,177
  solution:
  3,5,7,26,37,39,42,46,50,54,61,75,81,83,84,85,89,97,109,118,124,134,139,166
  ```
  (the file's `gam = 5` is the max line intersection; consistent with Table 1.)
* My verification (script run with `python3 -I`, not stored in the repo): D is a planar difference set mod 183 (all 182 nonzero differences distinct); the translates of D form a projective plane of order 13 (any two lines meet in exactly 1 point); lines per the report's eq. (4) (line i contains point j iff 1+((i+j-2) mod 183) is in D); the 24 listed points meet the 183 lines in exactly the distribution `1:117, 2:9, 3:33, 4:18, 5:6`, min 1, max 5.
  The plane is PG(2,13): D = 19*S + 65 (mod 183) for the Singer set S built from the primitive polynomial x^3 = 2x + 6 over GF(13).
  Transported to standard homogeneous coordinates, the same 24-set (re-checked against all 183 lines a*x+b*y+c*z=0) is:
  (0,1,2) (1,0,5) (1,1,7) (1,2,4) (1,2,9) (1,2,11) (1,3,0) (1,3,2) (1,3,5) (1,3,9) (1,3,10) (1,4,7) (1,5,6) (1,6,8) (1,7,1) (1,8,1) (1,9,9) (1,10,1) (1,10,3) (1,10,5) (1,10,11) (1,11,9) (1,11,12) (1,12,5)
  with line-intersection distribution again `1:117, 2:9, 3:33, 4:18, 5:6`.
  => **Explicit published blocking set of PG(2,13) with max line intersection 5: YES (c(PG(2,13)) <= 5).**
  It is a near miss to 4: only six lines carry 5 points.

## C. Beres and Illes (1993) (abstract only; full text NOT opened)

* URL: https://www.iaorifors.com/paper/22084 ("Computational investigation of the covering number of finite projective planes with small order", Alkalmazott Matematikai Lapok 17(3/4), 379-411, 1993; the page's author field is garbled "Ills Tibor, Bres Lszl").
* Quoted abstract lines: "Our paper deals with Erdos' problem related to the covering number of blocking sets of finite projective planes." "We produced a suboptimal solution for ILP (denoted by alpha_G(q)) for 7 <= q <= 89, q prime and for q = 8,9,16." "According to our computational results the approximate value of alpha_G(q) is c log q, where 1 <= c <= 2 holds."
* Suboptimal greedy values only; the abstract gives no value for q=13 and no lower-bound table. I could not open the body. (Illes-Pisinger describe it: "For all prime orders up to q = 89 they were able to obtained better bounds ... than those known from the theoretical considerations".)

## D. Theoretical upper bounds that touch q=13 (none close to 4 or 5)

* Asgarli, Ghioca, Yip, "Blocking sets from a union of plane curves", arXiv:2510.15332v2 (30 Sep 2026) (OPENED, pdf read). URL https://arxiv.org/pdf/2510.15332 .
  Their convention: k(n) = least k with a blocking set B with |B cap L| < k for all lines, so k = rho + 1.
  Quotes: "Erdos' question is still wide open, and much of the subsequent work has focused on the case of a projective plane P^2(F_q)." ; "Bruen and Fisher [12] found a blocking set in P^2(F_{3^r}) formed by taking a union of geometrically irreducible cubic curves and showing that k <= 5 for Erdos' question. More generally, Boros [11] proved that if q = p^r with a prime p >= 3, then k <= p + 2" (Illes-Pisinger state the Boros result for r >= 2, so it is vacuous for q=13 prime); "Illes, Szonyi, and Wettl [18] showed that for Erdos' question in P^2(F_{2^r}), the bound k <= 6 holds if r is even, and k <= 7 holds if r is odd."
  The paper has no table of small-q values, no mention of Illes-Pisinger, Beres, or q=13 (grep for 13/Pisinger/Illes confirmed).
* Szonyi's parabola construction (as summarised in Illes-Pisinger, section 2): union of k parabolas, pairwise nonsquare differences, maximal => property B(2k+1) (max intersection <= 2k). For q=13 the Paley graph's maximal independent sets all have size 3 (my own check: all nonsquare pairs are equivalent under multiplication by squares, and {0,2} extends to {0,2,7}), giving only max intersection <= 6. Abbott-Liu: PG(2,p) has B(2h(p)+3). Neither gets to 4 or 5 at q=13 (these two are quoted second-hand from Illes-Pisinger; originals not opened).

## E. Counting bound (my own arithmetic, NOT from a source) -- c(PG(2,13)) >= 4

For a point set B of size k in PG(2,q) with every line meeting it in 1..rho points, let t_i be the number of i-secants. Then
sum t_i = q^2+q+1, sum i t_i = k(q+1), sum i(i-1) t_i = k(k-1), and sum (i-1)(rho-i) t_i >= 0 gives
k^2 - (1+rho(q+1))k + rho(q^2+q+1) <= 0.
q=13: rho=3 -> discriminant 43^2 - 12*183 = -347 < 0, impossible (also confirmed by brute force: no nonneg integer (t1,t2,t3) for any k).
rho=4 -> discriminant 57^2 - 16*183 = 321 > 0, roots 19.54..37.46; brute force over (t1..t4) gives integer-feasible k = 20..37. With the standard Blokhuis bound |B| >= 3(q+1)/2 = 21 for a nontrivial blocking set in PG(2,p) (not re-sourced here), a rho=4 blocking set would have 21 <= k <= 37.
This matches the Beres-Illes window quoted in Illes-Pisinger Result 1. So counting alone cannot exclude 4.

## F. (k,4)-arc angle: blocking = (k,4)-arc with no external line (nothing found that settles it)

* Complement relation, S. Ball, "Multiple blocking sets and arcs in finite planes" (J. London Math. Soc. 54 (1996)), https://web.mat.upc.edu/simeon.michael.ball/blocking.pdf (OPENED): "Note that (k, n)-arcs and multiple blocking sets are in fact just complements of each other in a projective plane, with n + t = q + 1." So S is blocking with max 4 <=> the complement is a 10-fold blocking set (every line >= 10 points) containing no full line. Ball's Table 3 gives m_4(2,13) in "34 .. 40" (1996; with a (34,4)-arc, secant distribution tau_0 = 24 external lines). He does not discuss external-line-free (k,4)-arcs at q=13.
* Current bound on the largest (k,4)-arc in PG(2,13): "38-40". Source: Daskalov and Wassermann, "The best known (n,r)-arcs in PG(2,13)", https://epub.uni-bayreuth.de/id/eprint/3394/1/arcs_in_PG_2_13.pdf (OPENED): table "r=4: 38-40"; "A (38,4)-arc ... The secant distribution of the arc is tau = (24, 14, 19, 24, 102, 0, ...)" (24 external lines, so NOT a blocking set). S. Ball's table page, https://web.mat.upc.edu/simeon.michael.ball/codebounds.html (opened): "The table indicates the largest set of points in PG(2,q) with at most r points incident with any line." The q=13 cells for r=4 were not recoverable from the HTML I fetched (only r=16,17,19 cells visible), so I rely on Daskalov-Wassermann for 38-40.
* Hirschfeld-type bound quoted in the thesis below: "Theorem 1.21. If K is a (k; n)-arc in PG(2, q) that has no external line, then k <= (n-1)q + q - sqrt(q^2 + q - nq)." At n=4, q=13 this gives k <= 40.6, i.e. k <= 40 (weaker than the 37 from section E).
* Z. S. Hamed, PhD thesis, Univ. of Sussex, "Arcs of degree four in a finite projective plane" (OPENED, downloaded): https://sussex.figshare.com/articles/thesis/Arcs_of_degree_four_in_a_finite_projective_plane/23460560 (file https://ndownloader.figshare.com/files/41168426). It builds many (k;4)-arcs, k = 6..38, in PG(2,13) and lists secant distributions {t4,t3,t2,t1,t0}. Scope warning, verbatim: "This classification method may not produce all sd-inequivalent classes of (k; 4)-arcs." Also: "the smallest size of complete (k; 4)-arc is at most k = 24 and the largest size is at least k = 38". My scan of every `{a,b,c,d,e}` secant distribution in the thesis (523 distinct, each checked against sum = 183, 4t4+3t3+2t2+t1 = 14k and 12t4+6t3+2t2 = k(k-1)): **minimum t0 (external lines) = 9** (at k = 26 and 27); none has t0 = 0. This is a census of a restricted, non-exhaustive family of arcs: search-negative only. It does not say "every (k,4)-arc in PG(2,13) has an external line", and no source I found says that.
* Searches for "every (k,4)-arc in PG(2,13) has an external line", "(k,n)-blocking set", "blocking (k,n)-arc", "arcs without external lines" returned nothing that states or proves it for q=13. Ughi's Geom. Dedicata 26 (1988) paper "On (k,n)-blocking sets which can be obtained as a union of conics" uses exactly the notion "blocking set that is a (k,n)-arc", but only secondary descriptions were readable (a web-search summary of its abstract, plus the Asgarli-Ghioca-Yip sentence that Ughi "proved that the number of nonsingular conics required to form a blocking set must tend to infinity as q -> infinity"; Crossref/OpenAlex carry no abstract); no q=13 value seen. Full text NOT opened.

## G. Not opened / could not verify (so "not found" has these holes)

* Springer pages (Journal of Heuristics 2001 version of Illes-Pisinger, Ughi 1988, Gacs-Szonyi "Random constructions and density results" DCC 47 (2008)) -- redirect to a JS client challenge. OpenAlex lists only two works citing the J. Heuristics paper: Gacs-Szonyi (10.1007/s10623-007-9149-3) and "On the spectrum of minimal blocking sets in PG(2,q)" (10.1007/s00022-003-1702-2); neither opened. If the 2001 version re-ran q=13 and got rho=4, I would not know (the 1998 web page and the 1997 report say 5).
* Beres-Illes 1993 body text; Illes-Szonyi-Wettl, Mitt. Math. Sem. Giessen 201 (1991) 97-107; Abbott-Liu, Ars Combin. 20 (1985); Boros, Ars Combin. 25 (1988); Bruen-Fisher, Pacific J. Math 53 (1974); Erdos-Silverman-Stein, Ars Combin. 15 (1983); Szonyi, Ratio Math. 5 (1992); Illes' 1989 Budapest thesis (in Hungarian).
* erdosproblems.com/1159 direct fetch: HTTP 403 (also for /latex, /history, /forum). Read via Wayback instead: https://web.archive.org/web/2026/https://www.erdosproblems.com/1159 and .../forum/thread/1159. Content: asymptotic constant-C question ("Must there exist a set of points S such that 1 <= |S cap l| <= C for all lines l?"); "Erdos, Silverman, and Stein [ESS83] proved this is true with |S cap l| << log n"; thread banner "This is open, and cannot be resolved with a finite computation."; "Comments (1)" (only a pointer to Green's list, Problem 68). No small-q data. The teorth/erdosproblems database (raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml) lists #1159 as state "open", last_update 2026-01-23.
* Szonyi's slides https://conferences.famnit.upr.si/event/28/attachments/44/182/Szonyi.pdf (opened via pdftotext) list "(Erdos) Is there a constant C such that there is a blocking set in any Pi_q meeting every line in at most C points?" under "Some open questions"; nothing on small q.
* No Ball/Kohnert/Wassermann/Braun database entry for "(k,4)-arcs with no external line in PG(2,13)" was found; the Bayreuth arc database itself is offline (stated in Daskalov-Wassermann: "the database for (n, r)-arcs is no longer available").

## H. One-line answers to the specific questions

1. Is c(PG(2,13)) known to be 4? -- No source says so. Known: 4 <= c <= 5 (counting + Illes-Pisinger witness).
2. Known to be 5? -- Not proved. Only the upper bound 5 (heuristic search, explicit set, verified).
3. Published statement "every (k,4)-arc in PG(2,13) has an external line"? -- NOT FOUND.
4. Explicit published blocking set of PG(2,13) with max line intersection 5? -- YES (section B, 24 points, re-verified).
5. Largest (k,4)-arc in PG(2,13): 38-40 (Daskalov-Wassermann; Ball); blocking needs k in 21..37 by counting+Blokhuis, so the arc-size bounds do not exclude it.
