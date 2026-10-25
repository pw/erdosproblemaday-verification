  {
    slug: "604-openai-weak-pinned-distances-refereed",
    problemNum: 604,
    title: "#604: OpenAI's weak pinned distance theorem answers the page's first question — every exponent below 1 for a pin, where Katz–Tardos's 0.864 stood since 2004; n/√log n stays open — its Lean kernel-replayed here with the page's question compiled as a probe, and eight hostile seats read all 27 pages: no gap",
    date: "2026-10-14",
    status: "proof_claimed",
    originatedByUs: false,
    summary:
      "Erdős asked ($500) whether n points in the plane always contain one that determines n^(1−o(1)) distinct distances to the others — the pinned form of the distinct-distances problem — and the page's best bound was Katz–Tardos's n^0.864. OpenAI's 23 September 2026 paper proves that for every fixed s > 0 the fraction of ordered pairs whose distance repeats n^s times at its source tends to zero, hence all but o(n) points see at least n^(1−ε) distinct distances for every ε, with no rate. Its catalogued Lean proof (48 modules) compiled on our machine in 508 s and the kernel printed only propext, Classical.choice and Quot.sound on main, pins and exists_pin_eventually; the statement matches the comparator byte for byte and the page's question, written from scratch, closes from the Lean in four lines; cert-machine's independent comparator run agrees on two kernels. Eight tool-equipped seats (seven on the proof, one on sources), each briefed to refute, read it line by line and found no gap — only that the range s > 0.1359 already followed from Katz–Tardos, that the Lean takes a different route through §2, §6 and §7, and that the argument proves a more general Theorem G that no source the seats searched states. First question answered yes; n/√log n stays open. The theorem is OpenAI's; the audit and the replay are ours.",
    body: `
{{BODY}}
`,
    links: [
      { label: "OpenAI, \"The weak pinned planar distance theorem\" (family 167, 23 Sept 2026, 27 pp — the claim under review; sha256 6350959d…)", url: "https://github.com/openai/math/blob/main/preprints/The-weak-pinned-planar-distance-theorem-September-23-2026/paper.pdf" },
      { label: "The Comparator challenge statement — ComparatorChallenges/PinnedDistances.lean (Theorem 1.1 with a sorry)", url: "https://github.com/openai/math/blob/main/lean/ComparatorChallenges/PinnedDistances.lean" },
      { label: "The Lean proof — OAI/Geometry/PinnedDistances/ (48 files; Main.lean proves main, Pins.lean proves exists_pin_eventually)", url: "https://github.com/openai/math/tree/main/lean/OAI/Geometry/PinnedDistances" },
      { label: "OpenAI's scope note for the formalization — lean/docs/167.md (shared with the unit-distance paper)", url: "https://github.com/openai/math/blob/main/lean/docs/167.md" },
      { label: "Bloom, \"Erdős problems in the OpenAI proofs\" (8 Oct 2026 — #604 listed as formalised, 27 pp)", url: "https://www.erdosproblems.com/forum/thread/blog:10" },
      { label: "Formal Conjectures, Erdős 604 — erdos_604 (research open), katz_tardos and grid variants", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/604.lean" },
      { label: "Katz–Tardos, A new entropy inequality for the Erdős distance problem (Contemp. Math. 342, 2004) — Cor. 6 (0.864137…) and Cor. 8 (isosceles triangles)", url: "https://doi.org/10.1090/conm/342" },
      { label: "Dewar–Frankl–Mansfield–Nixon–Passant–Warren, Generalised Erdős distance theory on graphs (arXiv:2505.06590) — Conjecture 4.7 names the weak pinned conjecture", url: "https://arxiv.org/abs/2505.06590" },
      { label: "cert-machine, independent comparator run for PinnedDistances (exit 0, default kernel + nanoda)", url: "https://github.com/carlostoledo1891/cert-machine/blob/main/corpus/openai-math/kernel-runs/38019899278/PinnedDistances.json" },
      { label: "Our audit bundle — paper text, brief, eight referee reports (seven on the proof, one on sources) with their check scripts, the replay (driver, 48 module logs, probes, axioms, statement match v1–v3, leanchecker), world captures", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/604/openai-referee" },
      { label: "Our 14 Oct entry on the sibling paper — the unit-distance power saving (#90)", url: "/day/90-openai-unit-distance-power-saving-refereed" },
      { label: "erdosproblems.com/604", url: "https://www.erdosproblems.com/604" },
    ],
  },
