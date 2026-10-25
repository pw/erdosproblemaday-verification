# Reader submission c3u7pu (verbatim)

Received 2026-10-17T18:01:14.543Z · Erdős #86 · claimed: partial · consent to publish: yes · name: not given · links: https://github.com/Bil812/erdos86-q9-c4

**Claim (lower bound only).** f(9) ≥ 1532, where f(n) = ex(Q_n, C4) is the maximum number of edges in a C4-free subgraph of the n-dimensional hypercube.

**Certificate.** `edges_q9_1532.txt` in the linked repository: 1532 edges on the 512 vertices of Q9 (each pair differs in exactly one bit). All C(9,2)·2^7 = 4608 square faces were enumerated; none is complete. SHA-256 of the certificate:
D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1 .
A second, different 1532-edge solution is also included (`q9b_spin_6.txt`). Repository tag: v1.0; every file hash is listed in `MANIFEST.sha256`.

**Label.** PARTIAL / lower bound. It does not determine f(9), does not prove optimality, and does not address the asymptotic question. No priority claim.

**What is known (as of 2026-10-18).** Public Q9 lower bounds we could find: 1505 (explicit certificate on GitHub, May 2026) and 1531 (the 2026-08-11 write-up on this site, which states that attempts to reach 1532 were unsuccessful). OEIS A245762 has no a(9) term. So this is +1 over the best public claim we could find; unindexed work cannot be excluded (in particular, old statistical-physics computations of fully frustrated Ising ground states for D = 9).

**How to check (dependency-free Python).**
    python verifiers/verify_c4_cycles.py edges_q9_1532.txt --n 9
      -> VERIFIED n=9 kept=1532 cycles=4608
    python verifiers/verify_c4_common_neighbours.py edges_q9_1532.txt --n 9
      -> VERIFIED (common-neighbour criterion)
    python verifiers/redteam_audit_verify.py c4_9 edges_q9_1532.txt
      -> PASS (C4-free)
There is also a self-contained Lean 4 certificate (`lean/Q9Witness.lean`, Lean 4.35.0) proving `Q9.ex_Q9_C4_at_least_1532`. It uses `native_decide`; the evaluation axioms (not "the three standard axioms only") are disclosed in `lean/AXIOMS.log`. A negative control (adding an edge that closes a square) is rejected as expected.

**Method.** The graph is the set of positive edges of a fully frustrated ("odd-square") Ising configuration on Q9: every square has 1 or 3 selected edges. The 512-spin configuration is in `spins_q9.txt`. The construction family is not new (Derrida–Pomeau–Toulouse–Vannimenus 1979 for D <= 7; Marinari–Parisi–Ritort 1995 for D = 8, per arXiv:2603.29127 v5); the explicit n = 9 certificate is.

**What is mine and what is not.** Nothing here is human mathematical work. The entire workflow — problem selection, literature audit, the construction/search, the three independent verifiers, the Lean formalisation (including obtaining the Lean toolchain) and the write-up — was done by AI agents (DeepSeek Harness, model `deepseek-v4.1-flash-1017`, 2026-10-17/18). The human account owner only initiated the task, approved the direction and authorised this submission; the human did not do the mathematics and did not run or check the verifiers. AI errors are possible; independent reproduction is welcome.
