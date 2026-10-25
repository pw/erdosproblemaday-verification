# Seat W — WORLD + SOURCES
Read /tmp/oaimath/184/seats/COMMON.md first. Report: /tmp/oaimath/184/seats/W_report.md. Work dir: /tmp/oaimath/184/seats/W_work/.
You have web tools (WebSearch/WebFetch; curl). arXiv PDFs: `curl -sL https://arxiv.org/pdf/<id>` then pdftotext. Always check the CURRENT version (vN).
1. Every prior-result sentence in §1 and §1.1 against its source, quoting both: AEKS 1981 [1] (Combinatorica 1(4) 313–317) p. 314 Equation (3) — is
   that literally the conjecture as stated in Theorem 1.1 (average degree vs max degree; "d → ∞" vs uniform; any range of r)? and the claimed
   Ω_r(n log log d/d); AKS 1980 [2]; Shearer 1983 [14] coefficient 1; Shearer 1995 [15, Corollary 2] = n log d/(d log log d) in AVERAGE degree?;
   Alon 1996 [3, Thm 1.1 + remark]; Davies [6] "Random independent sets and local sparsity" arXiv:2609.04654v1 — does it exist? does its §3.3 /
   proof of Theorem 17 contain the potential Σ w(1 − log w) − M(w) (the paper says this functional is "the unit-parameter specialization" of Davies');
   is Davies itself a proof of anything that overlaps Theorem 1.1?; DKPS [7, Thm 30, Cor 31]; Dhawan [8, Thms 1.3, 1.4]; Dhawan–Janzer–Methuku [9,
   Thms 1.4, 1.6]; Dutta–Mubayi–Subramanian [10]; Kleinberg–Tardos [11, §3, Lemmas 3.1, 3.2]; Angel–Spinka [4, Thm 2, §2.1] (pairwise bound
   2d/(1+d)); Benjamini–Duminil-Copin–Kozma–Yadin [5, §2]. The lower-bound example "best possible up to a constant even for triangle-free graphs
   [1, pp. 314–315]" — is that what AEKS pp. 314–315 says?
2. World: has anyone else claimed a proof of the AEKS conjecture (arXiv, 2025–2026; search "Ajtai Erdős Komlós Szemerédi conjecture", "independence
   number K_r-free graphs log d/d", "clique-free graphs independence number logarithmic")? Has anyone publicly refereed, criticised, reproduced or
   built on OpenAI's family 184 since 6 Oct 2026 (GitHub issues/PRs on openai/math, Formal Conjectures PRs about erdos_802, erdosproblems.com/802
   forum, blogs, Mathstodon/X, Tao/Bloom posts)? Formal Conjectures' current status of erdos_802 (github.com/google-deepmind/formal-conjectures,
   FormalConjectures/ErdosProblems/802.lean, main branch) and any open PR changing it. The teorth/erdosproblems database status for 802.
   The companion paper (same family) "Correspondence coloring graphs with a forbidden clique" (5 Oct 2026) — note whether it depends on Theorem 1.1
   or vice versa (do not referee it).
3. Is the AEKS conjecture as stated on erdosproblems.com/802 (average degree t, ≫_r) exactly Theorem 1.1? Any subtlety (t ≤ 1, t < e) that the paper's
   d ≥ 2 hypothesis handles and the problem statement does not?
Fetch erdosproblems.com via the main seat's saved copies only: /tmp/oaimath/184/live/ep802*.html (the site 403s this machine).
