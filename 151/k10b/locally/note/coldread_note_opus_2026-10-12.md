# Cold read: `locally_wagner_note.md` (blind, with tools)
(Claude Opus 5.5, 2026-10-12 ~16:50Z. Scratch scripts copied to `note/coldread_opus_2026-10-12_scripts/` (`inv.py`, `col.py`, `cap.py`). Every "verified" below is my own run unless I say it comes from a referee log.)

**Bottom line.** The mathematics holds. Every invariant of P(17) and F₂₁ that the note states is correct. The classification is reproduced: 17,950 nodes, two graphs, 0 refused at cap 1000. The Smallwood quotations are accurate, and the thesis's standing assumptions (finite, connected, induced neighbourhood) are the note's, so "counterexample" needs no qualification. What would embarrass the author:
- an over-general claim in the abstract;
- a vertex count that the bundle's own referee report contradicts;
- "flag graph" used for two different graphs;
- a completeness "proof" that is one sentence;
- controls described as "classical" or "agreeing with the literature" when they were not checked against any source.

---

## Findings, most important first

**1. SUBSTANTIVE — the abstract claims more than the files prove.**
> "where an 8-regular K₄-free minimal (3,3)-Ramsey graph would have to be locally Wagner."

Read as a general statement, this is not established. `NOTES_k10b.md` T7(a) gets "locally Wagner" in two steps:
- Seymour/Berge plus Bikov Thm 8.2 give links in {N8.3, N8.7 = M₈}.
- N8.3 is then excluded using T6(iv), the bound |X| ≤ 3 on exceptional vertices. That bound holds only for the core of a K₄-free counterexample with H(n) = 10. In a general 8-regular K₄-free minimal (3,3)-Ramsey graph, nothing in the files rules out a cluster of N8.3 vertices (an N8.3 vertex forces four N8.3 neighbours, but there is no contradiction without the |X| bound).

§4 has related slips:
- "every degree 8 or 9 (Bikov, Thm 8.2)": Thm 8.2 gives only δ ≥ 8. The bound Δ ≤ 9 comes from the counterexample (Δ(G) ≤ H(n) − 1).
- "on 21 to 41 vertices (Seymour's bound … via Bikov's list …)": 21 is Bikov–Nenov's F_e(3,3;4) ≥ 21. 41 is n ≤ R(3,10) ≤ 41. Neither comes from Seymour.
- H(n) is never defined. The notes define it as H(n) = max{k : R(3,k) ≤ n}.

*Fix:* In the abstract write "where the (3,3)-Ramsey core of a K₄-free counterexample with H(n) = 10, if 8-regular, would have to be locally Wagner". In §4, define H(n) and τ, and credit each step to its actual source: δ ≥ 8 to Bikov Thm 8.2, Δ ≤ 9 to the counterexample, Seymour/Berge to the triangle count, the |X| ≤ 3 argument to the exclusion of N8.3, and Bikov–Nenov to 21 ≤ n.

**2. SUBSTANTIVE — "21 vertices" is contradicted by the bundle's own referee report.**
> §1: "never needs more than 21 vertices before every branch either closes or dies"
> §3: "the largest partial graph it ever holds has 21 vertices"

`locally.py` measures `maxn` only on entry to `rec()`, so it counts only states that survived a completion. The referee's `capcheck_M8_{41,1000}.log` says **"locally.py … max vertices ever in a state 23"**; the independent search reaches 21. I re-ran it with an instrumented `complete()` (`cap.py`): `maxn(rec) 21`, `max n+newcount in complete() 23`, refused 0, nodes 17950. So `locally.py` does allocate 23 vertices in branches that then die.

The logical conclusion (no bound on order) is unaffected. It rests on "cap 1000, 0 refused", which is correct, and which also rules out infinite connected locally-M₈ graphs (see 13).

*Fix:* "every state that survives a completion step has at most 21 vertices (at most 23 counting new vertices allocated in a step that then fails; the second program never exceeds 21), and with a cap of 1000 no branch is refused."

**3. SUBSTANTIVE — "flag graph" names two different graphs.**
- The abstract and §1 call F₂₁ "the flag graph of the Fano plane".
- §2 then defines F₂₁ as the distance-3 graph of "the flag graph of PG(2,2)". There "flag graph" means L(Heawood), where flags are adjacent when they share an element.

The second usage is the standard one: the flag graph of an incidence structure is the line graph of its incidence graph. A graph theorist will read the abstract as naming L(Heawood), which is 4-regular.

*Fix:* Name F₂₁ "the graph of opposite flags of PG(2,2)". In the A₂ building of PG(2,2), two flags are opposite exactly when p ∉ M and q ∉ L, and that is distance 3 in L(Heawood) = the collinearity graph of GH(2,1). Keep "flag graph" only for L(Heawood), or avoid the term altogether. I checked that the relation is identical, not merely isomorphic: in the share-an-element graph on the 21 flags, distance 3 ⇔ p ∉ M and q ∉ L, for all 210 pairs. `models_g21.py` also calls F₂₁ the "Fano flag graph"; rename it there too.

**4. SUBSTANTIVE — the completeness argument, which is the proof, is a one-line assertion and is slightly wrong as worded.**
> "Every connected locally-X graph is reached: order its vertices by breadth-first search from any vertex and the construction follows that order."

The construction does not follow an arbitrary BFS order. New neighbours of v are numbered in X-position order of the chosen Aut(X)-orbit representative. What is reached is an isomorphic copy of G along a BFS order whose tie-breaks the search imposes. The sentence also never says why the two reductions lose nothing:
- the Aut(X) quotient: the set of valid embeddings is Aut(X)-invariant, and completions from s∘φ differ only by renumbering new vertices;
- the single new-vertex branch: new vertices carry no relations until `complete()`.

The referee report §(a), (b), (e) has the right argument: the state agrees with G at every step and closed vertices carry their full G-neighbourhoods. The algorithm is correct; I read `locally.py` and found no gap. The written argument is what's thin.

*Fix:* Replace the sentence with 4–5 sentences giving the invariant and the two reductions. Label the result "Theorem (computer-assisted)".

**5. SUBSTANTIVE — controls described as "classical" or "agreeing with the literature" when they were not checked against a source.**
> "Controls (classical answers, all reproduced exactly …): … locally C₆, order ≤ 16 → eleven triangulated-surface quotients"
> "Further controls on which both programs agree with the literature: locally Q₃ → … ; locally 3×3-rook → … ; locally C₆, order ≤ 20 → 25 graphs."

- The C₆ counts are program outputs, not classical answers. The note cites no source for 11 or 25. The referee's only third check (`torus.py`) covers the 18 orientable graphs and leaves the 7 Klein-bottle ones. I re-ran `locally.py C6 16` and got 11 graphs (5.3 s), which matches the orders ≤ 16 in `ctrl_c6_20.log`. The number is right; its provenance is not "classical".
- For Q₃ and the 3×3 rook graph the referee writes: "I took the statement from Smallwood's survey §2.2, which I did not check against Buset". That is the thesis this note refutes. The Q₃ statement is in fact correct: Buset, *Graphs which are locally a cube*, Discrete Math. 46 (1983) 221–226, gives exactly two graphs on 15 and 24 vertices (abstract confirmed by search).
- The note also omits the controls that did not finish:
  - `locally.py` did not finish locally-Petersen ≤ 65 (Hall's 63/65 were never reproduced by either program);
  - `locally.py` did not finish locally-icosahedron ≤ 40, though the independent search did.

*Fix:* Cite Buset 1983 and Hall 1980 directly, and Brouwer (in Buset) for the 3×3 grid. Call the C₆ runs "multi-answer consistency checks (two programs agree; orientable cases cross-checked by lattice quotients)". Add one sentence listing the controls that did not finish.

**6. MINOR — the Aut ≅ PGL(2,7) receipt is missing; a better argument is available.**
> "Aut ≅ PGL(2,7) (the collineations and dualities of the Fano plane; computed in GAP by the referee seat)"

There is no GAP script or log for IdGroup in `referee_opus_2026-10-12/`; `ident21.log` holds Python counts only. The claim is true. I checked it constructively: the 168 collineations together with the 168 compositions with a correlation give exactly 336 distinct permutations of the flags, all automorphisms, and |Aut| = 336. So Aut is the collineation-correlation group PSL(3,2):2 ≅ PGL(2,7). The element-order profile also matches PGL(2,7) exactly: {1:1, 2:49, 3:56, 4:42, 6:56, 7:48, 8:84}.

*Fix:* State it that way, and drop "computed in GAP by the referee seat".

**7. MINOR — the "link count by hand" counts neighbours, not the link.**
> "The link count by hand: … — 8 neighbours."

The count is correct. q ranges over the 4 points off L; q ≠ p, so exactly one of the 3 lines through q contains p, leaving 2. I verified that the hand description equals the computed neighbourhood for all 21 flags. But this is the degree, not a proof that the link is M₈.

*Fix:* Call it "degree count by hand", or add the short link argument.

**8. MINOR — the P(17) link argument is complete but leaves two steps implicit.**
> "Every link is a 3-regular triangle-free graph on 8 vertices with independence number 3, hence M₈ (the only other cubic triangle-free graph on 8 vertices is the cube, with α = 4)."

The argument is complete:
- λ = 3 ⇒ the link is cubic;
- K₄-free ⇒ the link is triangle-free;
- α(P17) = 3 ⇒ α(link) ≤ 3;
- `nauty-geng -t -d3 -D3 8` gives exactly 2 graphs, and the cube has α = 4.

*Fix:* Say "independence number at most 3 (as α(P17) = 3)", and tie "3-regular" to λ = 3.

**9. MINOR — two different numbers for the same run.**
§3 says "≈30 s" and Reproduce says "≈40 s" for the same `M8 1000` run. The logs show 34.6 s (cap 41) and 38.3 s (cap 1000); my run took 34 s. Use "≈35 s". Also, "(optionally) a vertex cap": the code requires NMAX. Say "a vertex cap (set large enough never to bind)".

**10. MINOR — "at any cap" overstates what was run.**
> "no branch refused at any cap"

The referee ran caps 41, 60 and 1000, and only 41 and 1000 are logged. Say so.

**11. MINOR — every graph covers itself.**
> "neither graph has a connected locally-M₈ covering graph"

Write "no connected proper (non-trivial) locally-M₈ cover".

**12. MINOR — the two programs share a method.**
> "two independent implementations"

They are independently written implementations of the *same* completion method: an Aut(X) orbit quotient plus a single new-vertex branch. A flaw in the method's correctness argument would be shared. The Cayley scan and the cover argument are method-independent, but only partial. Say "two independently written implementations of the same completion method", and keep "proof" for the logic in finding 4.

**13. MINOR — "of any order" leaves infinite graphs open.**
> "There are no others, of any order."

The argument also excludes *infinite* connected locally-M₈ graphs (they are 8-regular, hence countable). A branch following one could never close, and none exceeds 23 vertices. Say "finite or infinite", or keep "finite" explicitly. Smallwood assumes finite graphs.

**14. MINOR — facts stated in the note's own voice whose only receipts are the referee's.**
- "they form an edge / a 4-cycle" appears only in the referee's `links.log`. `invariants.py` prints μ counts but not the induced structure.
- The Cayley model is in `fano.log`. "Not a circulant" rests on `cayley_counts.txt`, line `21 2 0 C21`, which shows no locally-M₈ connection set on ℤ₂₁. I re-checked it two ways: Aut has no element of order 21, and the referee's S on ℤ₇⋊ℤ₃ is inverse-closed and gives F₂₁.
- `invariants.py` and `models_g21.py` have no saved logs. I ran both; the outputs match the note.
- `invariants.py` *overwrites* `G21.colouring` and `P17.colouring` when run, so a reproducer may replace the shipped certificates.

*Fix:* Commit the logs, and point each fact at its receipt.

**15. MINOR — accuracy of the Smallwood paragraph.**
All quotes are verified against `smallwood2019_text.txt`:
- Theorem 4.17's proof ends: "Thus, it has been shown that (Z17 , Q) is the only M8 -local graph."
- Its *statement* reads: "Let u and v be vertices in G such that d(u,v) = 2. Then Gu,v ≠ C4. Furthermore, (Z17 , Q) is the only Mobius ladder local graph."
- Case 1: "Let (p2 ,p3 ,c4 ) = (8,0,4). … This is a contradiction since N(v,w1 ) = {1,4,v1 ,v3 } induces a P4."
- Corollary 4.7: "Then Gu,v is isomorphic to P2 , P3 , 2P2 , P4 , P5 , or C5." C₄ is missing.
- The paragraph before Lemma 4.5: "must be isomorphic to P4 , P5 , 2P2 , C4 , or C5". C₄ is present.

F₂₁ satisfies Lemma 4.15's equations with (8,0,4): 2·8 + 4·4 = 32 and 8 + 4·4 = 24. Definitions match ours:
- graphs are finite ("a graph consists of a finite set of elements…");
- only connected local graphs are considered (§1.3);
- H-local means "the neighborhood N(x) induces a subgraph isomorphic to H";
- M₈ is the 8-seat ladder with rungs across, i.e. C₈(1,4).

So "counterexample" needs no qualification.

Improvements:
- F₂₁'s 42 pairs with G_{u,v} ≅ C₄ contradict the *first* assertion of Thm 4.17 directly. Lead with that; it is cleaner than the case analysis.
- Say that the thesis writes P₂ for the 2-vertex path (= K₂).
- The thesis title is spelled "Mobius" (no umlaut). Quote it as printed.
- Give the Wayback URL the referee used: `web.archive.org/web/20240606050855id_/https://louis.uah.edu/cgi/viewcontent.cgi?article=1295&context=uah-theses`.

**16. MINOR — MathWorld's "likewise".**
> "MathWorld's 'Local Graph' table likewise lists only P(17) for the Wagner graph."

MathWorld's table lists named graphs and their local graphs. It is not a classification claim, so "likewise" implies MathWorld asserted uniqueness, which it does not. It also uses the name "4-Möbius ladder" (17-Paley graph), not "Wagner graph" (fetched today).

*Fix:* "MathWorld's table of local graphs lists only the 17-Paley graph against the 4-Möbius ladder."

**17. MINOR — presentation for a public note.**
- Internal jargon: "erdos seat", "hostile referee seat", "`~/MathDyad/...`". Replace with a public repository URL and a plain description of who checked what, including an explicit statement that the code and checks were AI-written, as arXiv policy requires.
- There is no bibliography. Needed: Hall 1980 (J. Graph Theory 4, 173–187); Buset 1983 (Discrete Math. 46, 221–226); Seymour 1974 / Berge 1994 Thm 3; Bikov arXiv:1604.03716; Bikov–Nenov AJC 77 (2020); Smallwood 2019.
- "girth 3" is vacuous for a graph whose every edge lies in 3 triangles. Drop it.
- In the abstract, "(q, M)" is used without being introduced. Write "flags (p, L) and (q, M) adjacent when …". The adjacency rule is otherwise consistent between the abstract and §2.
- "The first version failed the C₄/C₅ controls": there is no log of the failed version in the bundle (`dbg.py` only). That's fine as narrative; don't present it as a receipt.

## What I verified that is fine

- **F₂₁, from the Fano definition:** ≅ the graph6 given; 21 vertices, 84 edges, 8-regular, 84 triangles, λ = 3 on every edge, all links ≅ C₈(1,4), ω = 3, α = 5, diameter 2. Non-adjacent pairs: 84 with μ = 2 (induced K₂) and 42 with μ = 4 (induced C₄), so the graph is not strongly regular. |Aut| = 336, vertex-transitive, no element of order 21 (not a circulant). ≅ distance-3 graph of L(Heawood). ≅ Cay(ℤ₇⋊ℤ₃, S) with S as given. Aut = collineations + correlations.
- **P(17):** strongly regular (17,8,3,4), self-complementary, ω = 3, α = 3, |Aut| = 136, 68 edges, 68 triangles; the links are cubic, triangle-free, α = 3.
- **Colourings:** `G21.colouring` has 37 red of 84 edges and `P17.colouring` 29 of 68; a literal recount over all triangles gives 0 monochromatic in each.
- **Search:** `locally.py M8 1000` gives 17,950 nodes, graphs [21, 17], 0 refused (my run and `M8_1000.log`). Controls re-run: C₆ ≤ 16 gives 11; Petersen ≤ 21 gives one graph, ≅ K(7,2).
- **Cayley scan and covers:** `cayley_counts.txt` has 168 groups of orders 9–41; the only hits are 17/1, 21/1, 34/1 and 34/2. The mutation table matches `mutate.log`. The cover claim matches `pi1.log`.

## Literature (brief search, 2026-10-12)

- **"locally Möbius ladder" / "locally Wagner":** the only hit is Smallwood's thesis ([louis.uah.edu/uah-theses/296](https://louis.uah.edu/uah-theses/296)). Nothing else treats locally-M₈ graphs.
- **MathWorld [Local Graph](https://mathworld.wolfram.com/LocalGraph.html):** lists "4-Möbius ladder" with the 17-Paley graph and "7-Möbius ladder" with the 43-cyclotomic graph. Its references are Brouwer–Cohen–Neumaier pp. 4–5, 256, 434. It is a table of examples, not a classification.
- **F₂₁ as a named graph:** not found. Searches for "flag graph" + Fano + 21 vertices, and for the distance-3 graph of L(Heawood) / GH(2,1), returned nothing that names it. The surrounding objects are standard:
  - MathWorld ([Heawood graph](https://mathworld.wolfram.com/HeawoodGraph.html), [generalized hexagon](https://mathworld.wolfram.com/GeneralizedHexagon.html)) identifies L(Heawood) with GH(2,1).
  - Brouwer's [Heawood page](https://aeb.win.tue.nl/graphs/Heawood.html) identifies the 21 Heawood edges with the Fano flags (stabilizer D16) and builds the **Coxeter graph on the 28 antiflags**. That is the closest analogue: a classical graph on antiflags where F₂₁ is the graph on flags. Worth citing in the note.
  - Structurally, F₂₁ is the "opposite chambers" orbital graph of PGL(2,7) on 21 = 336/16 points (suborbits 1, 8, 8, 4; the 4-valent orbital graph is L(Heawood)).
  - I did not check House of Graphs.
- **Classifications that do not cover M₈:**
  - Hall, "Locally Petersen graphs", JGT 4 (1980) 173–187.
  - Hall, "Graphs with constant link and small degree or order", JGT 8 (1985) 419–444. Per [Caro–Hansberg–Tuza 2024](https://arxiv.org/html/2409.12875v1), this covers all links with at most 6 vertices; M₈ has 8.
  - Buset, "Graphs which are locally a cube", Discrete Math. 46 (1983) 221–226 (two graphs, 15 and 24 vertices; confirmed via search).
  - Blokhuis–Brouwer–Buset–Cohen (locally icosahedron) and Blokhuis–Brouwer (locally 4×4 grid; locally K₃,₃ or Petersen) as surveyed in Smallwood §2. I did not read the primaries.
  - [Garcia-Colin–Leemans, arXiv:1811.11438](https://arxiv.org/abs/1811.11438) builds locally-X graphs from incidence geometries; the abstract does not mention this graph.
- **Conclusion:** I found no prior correct classification of locally-M₈ graphs and no prior appearance of F₂₁ as a locally-Wagner graph. That supports the note's novelty, with the usual caveat that a negative search is a coverage claim.

5 substantive, 12 minor.

Cold read written.
