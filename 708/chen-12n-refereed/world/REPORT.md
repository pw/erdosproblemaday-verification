# World seat (Claude Opus 5.5, 2026-11-12) — state of Erdős #708, sources and dates

1. Zenodo concept 10.5281/zenodo.22267395 → latest record 22660853 = v14 (2026-09-08), main.pdf 44 pp; 14 versions
   (v1 2026-09-03). Changelog: "New Section 18 (refereed, not formalised) … hence g(n) ≤ 11n". v14 lacks g(10) ≥ 14 /
   g(12) ≥ 17 — those are only in the repo PDF (51 pp, §19, commit 643b3c2, 2026-09-08). Upstream HEAD dc150fd
   (2026-10-12); lean/README: "`Hinge883` itself, and hence `g_le 11`, is not proved" (only `g_le_11n_of_hinge`).
2. erdosproblems.com/708: last edited 2025-10-20; one forum comment (L. Mazur, 2026-05-06: |B| = g(n) vs ≤); one proof
   claim (#262, chenhaoyu, 2026-09-05), its only comment Chen's own v11 update; comments suspended. #709 thread: f(n)
   only. VLT26 (arXiv:2603.28636) solves #650, cites ErSu59, never mentions #708. arXiv (API + listing search), Tao's
   blog (WP API), MathOverflow (SE API), web: no paper/post on #708.
   GitHub only: Ziming Wang (science-prince/erdos-708-interval-divisor-covers, v1.0.0 2026-10-21): "g(n) ≤ min{10n,
   ⌈cn⌉+π(⌈cn⌉)−1}" resting on Chen's written H883; M ≥ 16n² ⇒ ≤ 2n; ≤ 2n+4 with ≤ 5 primes. Dovid Preil / Claude Fable
   (dpreil-ydlp/open-problems NOTES.md, 2026-10-15): proof of the ES count 2n−2ℓ+1; its upper bounds are
   "independent rediscoveries of results in Haoyu Chen's 2026 manuscript". No lower-bound improvement on (2−o(1))n and
   no independent g(4)/g(5) found.
3. Third-party replays of Chen's Lean: none (gh search code/repos: Erdos708, g_le_12n, Erdos708H97, Erdos708Statement,
   chy4pro; cert-machine corpus/ and nealmcb results/ have no 708). Chen's CI: runs 38165611266 (cold, success) and
   38187931698 (dc150fd, success). 0 issues on his repo.
4. Formal Conjectures: no ErdosProblems/708.lean on main; PR #4388 (JuanMarchetto, 2026-07-03) open, approved
   2026-10-05, "+awaiting-author" 2026-10-08; its HasCoveringSize statement reads the same as Chen's g_le (read side by
   side, not formally checked).
5. teorth database: 708 state "open" (last_update 2025-08-31), formalized "no" (HEAD 4d9c8b9, 2026-11-12).
6. ErSu59 (users.renyi.hu/~p_erdos/1959-07.pdf): Theorem II gives "legfeljebb 4" for three numbers; the general
   construction takes all p_i p_j, i, j = 1..l (squares included), k = l(l+1)/2, and needs l(l−1)+1; "Azt nem tudjuk,
   hogy lehet-e ez az arány lényegesen kedvezőtlenebb is." Er92c (hrj.episciences.org/125): "Is it true that
   g(n) < (2+ε)n or perhaps even g(n) ≤ 2n. I offer 100 dollars or 1000 rupees, whichever is more".
Raw fetches were kept on the box (MANIFEST.txt lists URLs); third-party files are not redistributed here.
