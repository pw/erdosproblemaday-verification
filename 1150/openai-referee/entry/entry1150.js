  {
    slug: "1150-openai-ultraflat-littlewood-refereed",
    problemNum: 1150,
    title: "#1150: OpenAI answers Erdős's ultraflat question for ±1 polynomials with NO — the Lean states the theorem that negates what was asked, our kernel replay printed the three standard axioms, and seven hostile seats read the proof and the ultraflat paper: no gap",
    date: "2026-10-12",
    status: "proof_claimed",
    originatedByUs: false,
    summary:
      "Erdős asked whether every polynomial of degree n with coefficients ±1 has maximum modulus at least (1+c)√n on the unit circle; Parseval gives √(n+1) for free and the question was whether real signs are forced a fixed fraction above it. OpenAI's 23 September 2026 paper proves the minimum over all sign choices is (1+o(1))√N at every large length N — the limit is 1, not the ≈1.27 that Odlyzko's exhaustive search had suggested — and its Lean states precisely that. On our machine the 28-module proof compiled from the pinned sources and the kernel printed only propext, Classical.choice and Quot.sound on a statement matched byte-for-byte to the challenge; seven tool-equipped referee seats, briefed to refute, found no gap in the formalized paper or in the two-sided ultraflat one. Answer: NO. The theorem is OpenAI's; the audit and the replay are ours.",
    body: `
{{BODY}}
`,
    links: [
      { label: "OpenAI, \"Asymptotically minimal maxima of real Littlewood polynomials\" (family 076, 23 Sept 2026, 26 pp — the formalized theorem)", url: "https://github.com/openai/math/blob/main/preprints/Asymptotically-minimal-maxima-of-real-Littlewood-polynomials-September-23-2026/paper.pdf" },
      { label: "OpenAI, \"Ultraflat real Littlewood polynomials\" (5 Oct 2026, 16 pp — the two-sided headline, paper-only)", url: "https://github.com/openai/math/blob/main/preprints/Ultraflat-real-Littlewood-polynomials-October-5-2026/ultraflat-real-littlewood-polynomials.pdf" },
      { label: "OpenAI, \"Nearly minimal maxima and positive minima of Littlewood polynomials\" (5 Oct 2026, 28 pp — √N/16 lower bound, paper-only)", url: "https://github.com/openai/math/blob/main/preprints/Nearly-minimal-maxima-and-positive-minima-of-Littlewood-polynomials-October-5-2026/littlewood-lower-envelope.pdf" },
      { label: "The Comparator challenge statement — ComparatorChallenges/AsymptoticallyMinimalLittlewood.lean", url: "https://github.com/openai/math/blob/main/lean/ComparatorChallenges/AsymptoticallyMinimalLittlewood.lean" },
      { label: "The Lean proof — OAI/Analysis/Littlewood/Main.lean (theorem main at line 187)", url: "https://github.com/openai/math/blob/main/lean/OAI/Analysis/Littlewood/Main.lean" },
      { label: "OpenAI's scope note for the formalization — lean/docs/076.md", url: "https://github.com/openai/math/blob/main/lean/docs/076.md" },
      { label: "Formal Conjectures, Erdős 1150 — answer(False), citing the Lean proof (PR #6898, 11 Oct)", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/1150.lean" },
      { label: "Odlyzko, \"Search for ultraflat polynomials with plus and minus one coefficients\" (2018; exhaustive n ≤ 52, conjectured limit ≈ 1.27)", url: "https://www-users.cse.umn.edu/~odlyzko/doc/ultraflat.pdf" },
      { label: "Balister–Bollobás–Morris–Sahasrabudhe–Tiba, Flat Littlewood polynomials exist (Annals 2020)", url: "https://arxiv.org/abs/1907.09464" },
      { label: "Erdélyi, On an Erdős problem about the maximum modulus of Littlewood polynomials (Aug 2026)", url: "https://arxiv.org/abs/2608.00744" },
      { label: "Our audit bundle — Lean source audit + scan, the replay (driver, module logs, axioms, controls, statement match), seven referee reports, brief, world captures", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/1150/openai-referee" },
      { label: "erdosproblems.com/1150", url: "https://www.erdosproblems.com/1150" },
    ],
  },
