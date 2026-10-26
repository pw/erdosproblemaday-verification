# Seat W — the world: who has read this, who has replayed it, and is the method new (read COMMON.md first)

Today is 2026-10-26. Find out what is publicly known about OpenAI's "Uniform exclusion of Landau–Siegel zeros" (1 Oct 2026) and its
family-003 sibling "The Quasi-Riemann Hypothesis" (30 Sep / 5 Oct 2026). Use WebSearch/WebFetch and `gh` (GitHub CLI, authenticated).
Pages that 403 from this box can be fetched through our server:
`ssh -i ~/.ssh/hetzner_prod deploy@100.103.211.37 'curl -s -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36" <URL>'`.
Save every fetched page/search result you rely on under W_work/ with the date; quote what matters.

Questions:
(1) Public expert reaction or refereeing: has anyone (a number theorist, a blog — e.g. Terence Tao's, MathOverflow, Lean Zulip,
    Hacker News, X, Quanta/news) claimed a GAP, an error, a fix, or endorsed the Landau–Siegel or QRH preprint? Dates, names, links,
    exact quotes. Also GitHub issues/discussions on openai/math mentioning 003, SiegelZeros, Landau, Siegel, QuasiRiemann
    (`gh issue list -R openai/math --search ... --state all`, `gh search issues`).
(2) Third-party kernel replays of the comparator `SiegelZeros` (and QuasiRiemannHypothesis / DirichletSevenEighths): the
    cert-machine corpus (GitHub org/user "cert-machine", path corpus/openai-math/kernel-runs/; earlier we found "SiegelZeros accepted
    11 Oct" there) and nealmcb's results (results/cmp-all/configs.csv). Search by the CHALLENGE name, not the Lean namespace
    (lesson from a past miss). Which kernels (Lean, nanoda), which dates, which commit. Our earlier notes: /tmp/oaimath/013/world/.
(3) Is the METHOD new? The paper excludes Siegel zeros with an interpolation determinant over Q(√d, √2) plus Frobenius congruences
    (no zero-density, no Deuring–Heilbronn). Check its cited sources say what it cites them for (exact theorem/section numbers):
    Friedlander–Iwaniec, Expo. Math. 36 (2018) §5; Laurent, Astérisque 198–200 (1991) §6; Fischler, Compos. Math. 141 (2005)
    Thm 1.1 & Lemma 1.3; Bost, Publ. IHÉS 93 (2001) Thms 2.1, 2.3; Benli–Goel–Twiss–Zaman, PAMS 154 (2026) 509–525 (does this exist?
    DOI 10.1090/proc/17450); Page 1935; Davenport ch. 12/14. Flag any reference that does not exist or does not say what is claimed.
    Any prior literature attempting Siegel zeros by transcendence/interpolation-determinant methods (Gelfond–Linnik, Baker–Stark
    class-number work, Goldfeld) — one paragraph on how this differs.
(4) erdosproblems.com/970 and /431 (fetch via the server): do they mention a dependence on this result? Formal Conjectures
    (google-deepmind/formal-conjectures): is there a Landau–Siegel / Siegel-zero statement, and what status does it carry?
Report: /tmp/oaimath/003/seats/W_report.md — facts with links and dates; separate "found" from "searched and found nothing" (a search
that finds nothing is a statement about the search, list the queries).
