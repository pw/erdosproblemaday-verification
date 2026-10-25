  {
    slug: "821-openai-totient-fibers-refereed",
    problemNum: 821,
    title: "#821: OpenAI's proof of Erdős's totient conjecture — x^(1−o(1)) smooth shifted primes for every exponent — 68 pages read by {{TEN_SEATS}} hostile seats, sources checked, the decisive identity rebuilt by computer",
    date: "2026-10-11",
    status: "posted",
    originatedByUs: false,
    summary:
      "Erdős asked whether φ(m) = n can have more than n^(1−ε) solutions for infinitely many n; he proved n^c, Baker–Harman and " +
      "Lichtman pushed c to 0.7156, and the conjecture C = 1 reduces to a count of primes p with p − 1 having no prime factor above " +
      "p^δ, a barrier of sieve theory below δ ≈ 0.284. OpenAI's 24 September 2026 paper claims x^(1−o(1)) such primes for every " +
      "δ, hence the conjecture, in 68 machine-written pages with no Lean for anything but the last page. We read it in {{TEN_SEATS}} " +
      "sectioned hostile seats briefed to refute, checked every cited theorem against its source, had the parity-breaking " +
      "step's exact identity coded independently twice and made it fail on purpose, and tried nine counterexamples to its " +
      "shifted-correlation theorem. Verdict on the paper as written: holds as read, {{SEATS_OF_SEATS}} — no mathematical gap, " +
      "a sketched bijection, one unwritten inequality, and a theorem that proves more than it claims. Unverified by any human or any kernel.",
    body: `
{{BODY}}
`,
    links: [
      { label: "OpenAI, Weighted dilation graphs, smooth shifted primes and totient fibers (24 Sept 2026, family 011)", url: "https://github.com/openai/math/blob/main/preprints/Weighted-Dilation-Graphs-Smooth-Shifted-Primes-and-Totient-Fibers-September-24-2026/paper.pdf" },
      { label: "Our audit bundle — ten referee reports, brief and prompts, toy computations with mutation controls, source quotes, world search, the §8 Lean check", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/821/openai-referee" },
      { label: "OpenAI's FiniteFiber.lean — the §8 transfer only (kernel-checked on our box 11 Oct 2026)", url: "https://github.com/openai/math/blob/main/lean/OAI/NumberTheory/TotientFibers/FiniteFiber.lean" },
      { label: "Lichtman, Primes in arithmetic progressions to large moduli, and shifted primes without large prime factors (arXiv:2211.09641) — the previous record", url: "https://arxiv.org/abs/2211.09641" },
      { label: "Baker–Harman, Shifted primes without large prime factors (Acta Arith. 1998)", url: "https://doi.org/10.4064/aa-83-4-331-361" },
      { label: "Pomerance, Popular values of Euler's function (Mathematika 1980) — where C = 1 is attributed to Erdős", url: "https://doi.org/10.1112/S0025579300009967" },
      { label: "Erdős 1935, On the normal number of prime factors of p − 1 … — the original construction (§3)", url: "https://www.renyi.hu/~p_erdos/1935-08.pdf" },
      { label: "Formal Conjectures, Erdős 821 — research open (11 Oct 2026)", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/821.lean" },
      { label: "Bloom, Erdős problems in the OpenAI proofs (8 Oct 2026)", url: "https://www.erdosproblems.com/forum/thread/blog:10" },
      { label: "erdosproblems.com/821", url: "https://www.erdosproblems.com/821" },
      { label: "OEIS A014197 — g(n), the number of m with φ(m) = n", url: "https://oeis.org/A014197" },
    ],
  },
