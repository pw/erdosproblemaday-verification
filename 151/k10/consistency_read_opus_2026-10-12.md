18 ISSUES (6 substantive, 12 minor). The lemma statements T1–T5, the θ table, 53/55, ≥ 11 / ≥ 12, the 7.2 M instance count (7,169,689), the 99/428/568 mutation counts, β = 28 for the crasher, min β = 14 in the search and the wording of Bikov Thm 8.2 all check out. The issues below are in the prose around them.

Ground truth used: NOTES_k10.md, the referee report, link_census.log, vt_search.log / .run1, and Bikov 1604.03716.txt. I decoded the three census graph6 strings with networkx. The bundle copies in verification/151/k10/ are byte-identical to the MathDyad files.

## Substantive

1. **"degree 8 with no lone edge allows exactly three neighbourhood graphs, all cubic and triangle-free."**
   - Not all cubic. The census only reports Δ = 3 (the "Delta range 3..3" column). Degree sequences:
     - GCQb`o: 2,2,2,2,3,3,3,3
     - GCR`r_: 2,2,3,3,3,3,3,3
     - GCrb`o: 3,3,3,3,3,3,3,3 (the only cubic one)
   - Supported wording: "maximum degree 3, triangle-free".

2. **"every neighbourhood triangle-free with independence number ≤ 5"** (side conditions of the missing lemma).
   - False as written. The bound α ≤ B (5 at n = 40, 4 at n = 41) applies to the link P_v, which is the neighbourhood with its lone-edge (isolated) vertices removed, not to G[N(v)].
   - The census admits degree-9 vertices with independent neighbourhoods (i = 9, so α = 9).
   - The page's own T4 consequence gives a vertex with ≥ 6 lone edges, so its neighbourhood has α ≥ 6.
   - The referee's objection 3 made exactly this point: "the number of lone edges is unbounded".

3. **"Vertex-transitive candidates are already gone: … on 36, 39, 40, 42 or 44 vertices"**
   - That list does not contain 41, and n = 41 is inside the window. The notes only claim "no K4-free vertex-transitive graph on 40 vertices".
   - Knock-on: **"Our circulant search … therefore bears only on graphs with K4's"** is false for the Z_41 (degree-8) part of the family. The notes carry the same overreach.

4. **Novelty and priority claims the files do not justify.**
   - (a) **"T2–T5 and their consequences are (a) elementary and, as far as we can find, not written down before".** The files record no literature search for T2–T5. The referee reviewed a draft that made no such claim ("T2–T5 are elementary and not claimed as new").
   - (b) **"a bounded-degree Folkman problem … that nobody has posed in that form."** This is a priority claim with no support in the notes. It has the same shape as the first draft's "nothing in print bounds the maximum degree…", which the referee found false.
   - (c) Lighter: "T2–T5 are ours" says the same thing; "elementary; not claimed as new" is what the files support.

5. **"a lazy SAT search for a 40-vertex K4-free graph with all degrees in {8, 9} … or the one-vertex extensions … whose conditions are written out in the notes."**
   - Only the minimal (3,3)-Ramsey core G_0 ⊆ G is forced into degrees {8, 9}.
   - G itself only has δ ≥ 4 (5 at n = 41), and G_0 may have fewer than 40 vertices. So the search as described would not be exhaustive and would not close the case. The notes share this.
   - NOTES_k10.md does not write out the extension conditions; it says "conditions in the session notes", and those are not in the bundle.
   - Nothing in the bundle explains why extensions of triangle-free (3,10;39)-graphs bear on G, which has triangles.

6. **"β ≥ H(n) follows from any red/blue colouring of the edges with no monochromatic triangle (red triangle-free and meeting every triangle; an independent set of the red graph is free)."**
   - This drops the step "lone edges red", which is in both the notes and the referee report.
   - If a lone edge is blue, an independent set of the red graph can contain it, so the set is not free.
   - Supported wording: "…, after recolouring every lone edge red".

## Minor

7. **T3 statement.** "blocked when N(u) ∩ N(w) contains a maximal clique of G[N(u)]" drops "isolated vertices of G[N(u)] counting". The control mutation that drops exactly this clause fails 428 times.

8. **"some vertex carries six lone edges with a neighbourhood graph on at most three vertices."**
   - The notes say *at least* six.
   - The part on ≤ 3 vertices is P_v (the rest of the neighbourhood). The neighbourhood graph itself has d(v) vertices.

9. **"every lemma in its full generality on all 13,598 graphs … 7.2 million instances".**
   - For T1, only the clique bound was checked exhaustively; t(v) ≥ g needs minimality.
   - The minimality consequences (θ table, Caro–Wei, the W_J refinement, the 53) were checked by hand and by misc.py arithmetic, not exhaustively.
   - The mutations ran on n ≤ 6, not n ≤ 8.

10. **"the three cited papers".** The report draws on four arXiv files (1604.03716, 1904.01937, 2401.00392, 2605.16542) plus the Formal Conjectures 151.lean file. The report does not record its brief, so "briefed to refute" rests on its title only.

11. **"Its findings were all in the surrounding prose …: [five items]".**
    - The list reads as complete but omits objections 2 ("bounded degree" ill-posed), 3 ("exactly/equivalently" overclaim), 4 (the B formula), 9 ("cheap to hit" with the direction inverted), 11 (the controls section overstated) and 12.
    - "All in the surrounding prose" is also slightly strong: one point in objection 12 is a non sequitur inside T2's consequence. The referee did find no gap in any proof.

12. **Circulant search scope.** "(all degree-8 and degree-9 circulants on 40 vertices, degree-8 on 41)" is the planned family, not what was searched.
    - At read time vt_search.log had 53 candidates, all on Z_40, none on Z_41, no progress line past [0/12597], and fewer candidates than run1 reached before dying at job 513 (~4 %).
    - "none with β below 14 so far" is correct, and none of the 53 is flagged as unproved.
    - The bundle ships only vt_search.log.run1, not the live log.

13. **"the upper bound 42 came down to 41 last year … Angeltveit, EJC 2025".**
    - No file states the previous bound of 42.
    - The referee: "EJC 32(4) P4.30 cannot be verified from the arXiv file".
    - arXiv 2401.00392 dates the result to 2024. "Last year" is at best the journal year.

14. **"no solver campaign, the box was carrying four other seats' jobs".**
    - "Four other seats" is unsupported; the files say load 24 and "a loaded box".
    - "No solver campaign" sits awkwardly beside the CP-SAT circulant search reported two paragraphs later.

15. **"The claim's Case C turns out to be Seymour 1974 in disguise".** The referee notes Seymour's theorem "is quoted from memory … and is not among the PDFs". The page asserts it without that caveat, and in a sentence about another author's novelty statement.

16. **The "(b) rigorous modulo …" list** omits sources the page relies on:
    - Lange–Radziszowski–Xu (the 786 bound)
    - Hassan–Radziszowski–Van Overberghe (the vertex-transitive exclusion, itself a computation)
    - Seymour

    Bikov 8.2 is itself computer-derived ("with the help of a computer").

17. **"what it settles is what a counterexample must be".** The files give necessary conditions, not a characterisation. Suggest "what a counterexample would have to satisfy".

18. **"β = the largest vertex set containing no maximal clique".** The notes say "maximal clique of size ≥ 2". As written, any set containing an isolated vertex fails.
