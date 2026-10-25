  {
    slug: "138-openai-superexponential-van-der-waerden-refereed",
    problemNum: 138,
    title: "{{TITLE}}",
    date: "2026-10-15",
    status: "{{STATUS}}",
    originatedByUs: false,
    summary:
      "{{SUMMARY}}",
    body: `
{{BODY}}
`,
    links: [
      { label: "OpenAI, \"Quantitative Superexponential Bounds for van der Waerden Numbers\" (family 160, 23 Sept 2026, 25 pp — the claim under review; sha256 042acea3…)", url: "https://github.com/openai/math/blob/main/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/paper.pdf" },
      { label: "The paper's LaTeX source (build/sections/01–08) — what the seats quoted from", url: "https://github.com/openai/math/tree/main/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections" },
      { label: "The Comparator challenge statement — ComparatorChallenges/QuantitativeVanDerWaerden.lean (Theorem 1.1 with c = 1/100000 and a sorry)", url: "https://github.com/openai/math/blob/main/lean/ComparatorChallenges/QuantitativeVanDerWaerden.lean" },
      { label: "The Lean proof — OAI/Combinatorics/ProgressionColoring/ (115 files; Main.lean proves uniform_lower_bound, kthRoot_tendsto, length_rate_tendsto)", url: "https://github.com/openai/math/tree/main/lean/OAI/Combinatorics/ProgressionColoring" },
      { label: "OpenAI's scope note for the formalization — lean/docs/160.md (the sharper intermediate estimates are not formalized)", url: "https://github.com/openai/math/blob/main/lean/docs/160.md" },
      { label: "Bloom, \"Erdős problems in the OpenAI proofs\" (8 Oct 2026 — #138 listed, and among the 12 FrontierMath Erdős-list problems)", url: "https://www.erdosproblems.com/forum/thread/blog:10" },
      { label: "Formal Conjectures, Erdős 138 — erdos_138 (research solved, citing this Lean), the difference variant (DeepMind), the W(k)/2^k variant (atlas-lean)", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/138.lean" },
      { label: "Campos–Fox–Schildkraut, A new lower bound for two-color van der Waerden numbers (arXiv:2608.20824, 21 Aug 2026) — W(k) ≥ (1−o(1))k·2^(k−1), the colouring found by ChatGPT 5.6 Sol Pro", url: "https://arxiv.org/abs/2608.20824" },
      { label: "Fox–Hunter, Three-color van der Waerden numbers grow super-exponentially (arXiv:2606.02541, 1 June 2026)", url: "https://arxiv.org/abs/2606.02541" },
      { label: "Kozik–Shabanov, Improved algorithms for colorings of simple hypergraphs and applications (JCTB 116, 2016) — W_r(k) ≥ β·r^(k−1)", url: "https://doi.org/10.1016/j.jctb.2015.09.004" },
      { label: "Berlekamp, A construction for partitions which avoid long arithmetic progressions (Canad. Math. Bull. 11, 1968) — W(p+1) > p·2^p", url: "https://doi.org/10.4153/CMB-1968-047-7" },
      { label: "Our audit bundle — the paper's TeX and text, brief, seven referee reports with their check scripts, the replay (driver, 115 module logs, probes, axioms, statement match, leanchecker), world captures", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/138/openai-referee" },
      { label: "erdosproblems.com/138", url: "https://www.erdosproblems.com/138" },
    ],
  },
