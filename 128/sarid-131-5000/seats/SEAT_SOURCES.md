# Seat SOURCES+WORLD — does every cited result say what is quoted, and what is the state of the world
Read COMMON.md first.

1. Balogh–Clemen–Lidický. The paper quotes "Theorem 2(a) of arXiv:2103.14179v1": D₂(G) ≤ n²/23.5 for triangle-free G
   on n ≥ n₀ vertices. The arXiv text is a 6-page EXTENDED ABSTRACT with a proof SKETCH (read bcl.txt). The comments
   tab cites a journal version: European J. Combin. 2024, doi 10.1016/j.ejc.2023.103841 ("Max cuts in triangle-free
   graphs"). Find it (doi, journal page, arXiv v2 if any, authors' pages, Lidický's flag-algebra repository / data
   pages — he usually posts certificates). Establish: (i) the exact statement in the published version (constant,
   "n large" or all n, definition of D₂); (ii) whether a verifiable certificate for Thm 2(a) is public anywhere;
   (iii) whether anything stronger than n²/23.5 is now known (search arXiv/Google Scholar 2021–2026: "make bipartite
   triangle-free n^2/25", "Erdős bipartite conjecture triangle-free", Balogh/Clemen/Lidický/Norin/Sun/Volec).
   Quote what you find; give URLs; say what you could not access.
2. Razborov. Confirm from razborov.txt: Prop 1.1's statement and normalisation (C₄ = 3·t ?), Theorem part 1
   (C₄ ≥ (3/2)ρ² − (81/256)ρ), the sentence that 27/1024 is the best achievable by the edge-splitting method with
   constant weights per part (Sarid's Section 3 IS that method). Does Razborov anywhere already use a max-cut /
   bipartition input or a perturbation like Sarid's §4? Does he state the SRG result that would make Sarid's
   intro sentence "settled the conjecture … for strongly regular graphs" accurate?
3. The intro's attributions: EFRS94 β ≤ 1/30 (the live page says "50 replaced by 16" for EFRS — reconcile: which
   statement is in EFRS94?), Krivelevich 1/36 and "3n/5 with 25", Keevash–Sudakov ρ ≤ 1/6 and ρ ≥ 2/5 (the live page
   says "at most n²/12 edges or at least n²/5 edges" — same thing in ρ = 2e/n²? check), Norin–Yepremyan
   ρ ≥ 2/5 − ε₀ and "normalized minimum degree ≥ 5/14", Razborov's three classes. Fetch abstracts/first pages
   (arXiv/doi) and say for each: MATCHES / DIFFERS (how). Not load-bearing for the theorem, but the page we publish
   will restate history.
4. World: (i) teorth/erdosproblems database status for 128 (~/.cache/erdos-sources/teorth/data/problems.yaml —
   find the entry); (ii) Formal Conjectures 128.lean: any PR/issue mentioning Sarid or 131/5000
   (github.com/google-deepmind/formal-conjectures search); (iii) arXiv 2025–2026 search "sparse halves" /
   "Erdős half-graph conjecture" / "triangle-free n^2/50": anything newer than Razborov 2021? anything citing or
   superseding Sarid? (iv) the OpenAI math release (github.com/openai/math CONTENTS.md) — is #128 among its 25
   Erdős claims? (host grep says no; confirm); (v) Bloom's blog/X or the forum: any reaction to Sarid's claim?
   (vi) is Amir Sarid / "aimir" identifiable (affiliation, other repos) — one line, no speculation.
5. Priority/novelty: state exactly what is NEW in Sarid relative to Razborov + BCL, in one paragraph, and whether
   the 131/5000 bound is the best bound in print or on the tab today.
Write REPORT.md as specified, with a SOURCES.tsv (claim | source | URL | MATCHES/DIFFERS | quote).
