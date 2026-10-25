# Seat CERT — the flag-algebra certificate for Proposition 3.1 (an INDEPENDENT second instrument)
Read COMMON.md first. Then the paper's Section 3 and 5 (claim.txt), the JSON, and the author's verifier.

The claim: for every triangle-free graphon W, t(C₄,W) ≥ ρ³ − γρ with γ = 3/64 + 1/(5·10¹⁰), ρ = t(K₂,W),
t = homomorphism density. The author's verifier (which passes) checks that at "level six" the coefficient of each
of the 38 triangle-free 6-vertex host graphs in t(C₄) − ρ³ + γρ dominates the sum of the corresponding
coefficients of 34 rational rank-one "averaged squares of flags" (blocks s0_root0, s2_root0, … = flag types).

Your task is to re-establish the inequality by YOUR OWN implementation, not by rerunning theirs:
1. Read verify_clebsch_tangent_certificate.py only to learn the JSON FORMAT (what a block/type is, how a vector
   indexes flags, what "averaged square" means in their encoding). Then write /tmp/erdos1800/seats/cert/myverify.py
   from scratch: enumerate the 38 triangle-free graphs on 6 vertices yourself (nauty-geng -t 6 or networkx atlas),
   compute the exact rational expansion of t(C₄) − ρ³ + γρ in the basis of induced 6-vertex densities (derive the
   coefficients by sampling semantics: for a host H on 6 labelled vertices, the coefficient is the probability that
   a uniformly random map of the 4 cycle vertices / 2 edge vertices etc. into [6] WITH the right semantics gives the
   pattern — decide and state whether the semantics is injective sampling (standard flag algebras: t(F,H) over
   injective maps) or with repetition; the two agree in the graphon limit but the certificate must use ONE
   consistently). Then expand each averaged square into the same basis and check domination coefficient-wise.
   Print, per host, the two sides. If any host fails, that is FATAL for Prop 3.1.
2. Controls: (i) a mutated certificate (scale one weight by 1.01, or change γ to 3/64 − 10⁻⁶) must FAIL in your
   verifier; (ii) your expansion of t(C₄) alone must reproduce the known value for the Clebsch graph
   (65/4096 at ρ = 5/16) and for the balanced C5 blow-up (hom density of C₄ in C5 is 30/625 = 6/125 … recompute)
   when evaluated on a graph by direct counting, to show the basis coefficients are right.
3. Independent sanity (necessary condition): evaluate g(W) = t(C₄,W) − ρ³ + γρ by direct counting for (a) all
   triangle-free graphs on ≤ 10 vertices (nauty-geng -t), (b) the 7 triangle-free SRGs you can construct
   (C5, Petersen, Clebsch, Hoffman–Singleton, Gewirtz, M22, Higman–Sims — construct what you can in ≤ 10 min;
   the census repo /tmp/erdos1800/census/srg.py builds them, you may import its constructions after reading them),
   (c) weighted blow-ups: for every connected triangle-free graph on ≤ 7 vertices, minimise g over vertex weights on
   the simplex (t(C₄) of a weighted graph = trace((AD)⁴), ρ = wᵀAw; multistart SLSQP) — print the global minimum
   found and where. A negative value anywhere beyond 1e-9 refutes the certificate. Expect ≈ +6e-12 at Clebsch.
4. Read the Lean side of the same step: lean/Erdos128/C4Certificate/{Semantics,Soundness,GlobalBridge,Provider}.lean
   and say in two paragraphs what `certificate_all_triangleFree_masks` and `checkedC4FlagCertificateProvider`
   STATE (types), what sampling semantics the Lean uses (6 vertices with or without repetition; how the step from a
   6-vertex identity to an arbitrary finite graph is made), and whether the statement proved is exactly
   `C4FlagCertificate G` for every finite triangle-free G (ExternalInputs.lean).
Write REPORT.md as specified; include the per-host table in a file HOSTS.tsv.
