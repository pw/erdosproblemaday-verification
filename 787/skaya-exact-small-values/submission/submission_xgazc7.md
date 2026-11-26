id xgazc7 created 2026-11-25T06:32:19.029Z name skaya claim partial consent 1
links:
https://github.com/tokbceliwemers/erdos-787-progress
https://github.com/tokbceliwemers/erdos-787-progress/blob/main/paper/erdos_787_monograph.md
https://github.com/tokbceliwemers/erdos-787-progress/blob/main/paper/asymptotic_closure_synthesis.md
https://github.com/tokbceliwemers/erdos-787-progress/blob/main/proofs/AsymptoticClosureStandalone.lean
https://github.com/tokbceliwemers/erdos-787-progress/blob/main/proofs/Threshold45Standalone.lean
https://github.com/tokbceliwemers/erdos-787-progress/blob/main/proofs/InfiniteFamilyStandalone.lean
https://github.com/tokbceliwemers/erdos-787-progress/blob/main/figures/erdos_787_all_figures.png

### 1. Exact Statement Worked On
For a finite set $A \subset \mathbb{Z}$ (equivalently $A \subset \mathbb{R}$) of size $|A| = n$, let $M(A) = \alpha(G_A)$ be the maximum cardinality of a subset $B \subseteq A$ that is sum-avoiding with respect to $A$ ($b_1 + b_2 \notin A$ for all distinct $b_1, b_2 \in B$), where $G_A$ is the conflict graph with edge $\{u, v\}$ whenever $u \neq v$ and $u + v \in A$. Define
$$g(n) = \phi(n) = \min_{|A| = n} M(A), \qquad n_{\max}(k) = \max\{|A| : M(A) \le k\}.$$
Erdős Problem #787 asks for the asymptotic behavior of $g(n)$ as $n \to \infty$ (together with exact extremal thresholds $n_{\max}(k)$).

**Status disclaimer:** The full asymptotic problem remains **open**. This submission reports partial progress: exact resolution of $n_{\max}(k)$ for $1 \le k \le 6$ (and $g(n)$ on $[1, 59]$), an infinite constructive refutation of $n_{\max}(k) = k^2 + k + 1$ for all $k \ge 7$, Pure Lean 4 formalizations (`Init`-only, zero `sorry`), extended witnesses through $n = 143$, a Lean-certified $D_d$ Ruzsa construction reaching $\sqrt{8\log 2}$, and a tightening of Beker's (2025) lower-bound exponent from $1/68$ to $1/44$.

### 2. What Was Known
- Small extremal thresholds suggested $n_{\max}(k) = k^2 + k + 1$, leaving higher $k$ and exact $g(n)$ intervals open.
- Ruzsa (2005) proved $g(n) \le \exp(O(\sqrt{\log n}))$ via multi-scale 2-adic lattice balls embedded carry-free into $\mathbb{Z}_+$.
- Sanders (2021) proved $g(n) \ge (\log n)^{1 + c}$ and Beker (2025) established $g(n) \ge (\log n)^{1 + 1/68 - o(1)}$ via Kelley–Meka density increments for $k$-configurations.

### 3. New Results & Theorem Labels (Partial Progress)
1. **Exact Finite Thresholds $k \le 6$ and $g(n)$ on $[1, 59]$ (`n_max_1_exact` .. `n_max_4_exact`, plus $k=5,6$ Farkas+SAT UNSAT):**
   - $n_{\max}(1) = 3$, $n_{\max}(2) = 7$, $n_{\max}(3) = 13$ are formally proved in Pure Lean 4 (`proofs/ThresholdsStandalone.lean`), and $n_{\max}(4) = 21$ is proved in Pure Lean 4 (`proofs/Threshold45Standalone.lean`: 5 exact integer Farkas cores + 483-step Hinted-RUP check over $\mathbb{R}$).
   - Over $\mathbb{R}$, SAT + `__int128`-verified Gordan/Farkas LP certificates establish UNSAT at $m_+ = 16$ ($k=5 \implies n_{\max}(5) = 31$) and across all 21 subcases at $m_+ = 22$ ($k=6 \implies n_{\max}(6) = 43$, `288,228` IIS Farkas cores in `code/solve_k6_pos.py` + `code/gordan_dll.cpp`). Paired with witness $A_{59}$, this fixes $g(n)$ unconditionally for all $n \in [1, 59]$ (including $g(n) = 7$ on $[44, 59]$).
2. **Breakdown of $k^2 + k + 1$ for All $k \ge 7$ (`infinite_family_n_max_ge`, `k7_beats_projective_bound`):**
   - Inductive doubling $F_{d+1} = \{\pm(2j+1) : 0 \le j \le k\} \cup 2 F_d$ starting from $F_0 = A_{43}$ proves $n_{\max}(k) \ge k^2 + 3k - 11$ for all $k \ge 6$ in `proofs/InfiniteFamilyStandalone.lean`, strictly refuting $k^2 + k + 1$ for every $k \ge 7$ ($59 > 57$, $77 > 73$, $97 > 91$, $119 > 111$, ...).
   - All 56 witness sets `A3..A100` are machine-checked exact in `proofs/WitnessesStandalone.lean` and `proofs/NewWitnessesStandalone.lean` (`all_seven_witnesses_certified`, `all_49_new_witnesses_certified`), and dual-exact C++ branch-and-bound extends certified upper bounds through $n = 143$ (`data/verified_100_143.txt`: $\alpha = 10$ on $[100, 119]$, $\alpha = 11$ on $[120, 143]$).
3. **Checkerboard $D_d$ Ruzsa Formalization & Orthant Limit (`AsymptoticClosureStandalone.lean`):**
   - `single_sphere_orthant_lower_bound`: every equal-norm subset $S \subset \mathbb{Z}^d \setminus \{0\}$ has $\alpha(G_S) \ge |S|/2^d$ across coordinate orthants (ruling out single-sphere constructions).
   - `dd_same_coset_drop`, `ddVecs_sum_avoiding_bound`, `ddIntSet_props`, `dd_beats_quadratic_explicit`: formalizes the full multi-scale 2-adic checkerboard $D_d$ construction with carry-free radix embedding, proving the explicit $D_5, L = 37$ super-quadratic crossover $k = 1185$, $|A| \ge 1{,}438{,}294 > 1{,}407{,}769 = k^2 + 3k - 11$.
   - `ruzsa_quasipolynomial_nat`: proves $2^{2m^2 + 4m} \le |A|$ with $M(A) \le 8m \cdot 2^{4m}$, attaining the asymptotic Ruzsa constant $g(n) \le \exp((\sqrt{8 \log 2} + o(1)) \sqrt{\log n})$.
   - Supporting C++ code verifies tight $D_5, L = 36$ ($k \le 1142, n = 1{,}309{,}341$), $E_8$ ($L = 16, k \le 4097$), Leech $\Lambda_{24}$ ($2.111\times$ quadratic at $L = 10$), and origin-centered $D_d$ ($2^d - 1$ per layer).
4. **Tightened Asymptotic Lower Bound (`1/68 -> 1/44`, paper derivation in `paper/asymptotic_closure_synthesis.md`):**
   - Replacing symmetric `[FHHK Cor 2.3]` graph counting in `Case (i)` of Beker (2025) (`thm:graph_counting`) with an asymmetric inductive peeling lemma preserves the smaller part's density $\mu_{B^{(j)}}(T) \ge (\alpha/2)^3$ in `Subcase B` (`b: 46 -> 28`, `c: 6 -> 1`), lowering $E_k$ from $68$ to $45$.
   - Separating zero-frequency `[FHHK Lem 3.4]` scale-uniformity steps ($\Delta_r = \emptyset$, density increment $1 + \Omega(k^{-5})$) from harmonic/graph-counting branches ($|H| \ll k^4\mathcal{L}(\alpha)$, all achieving $1 + \Omega(k^{-4})$) restricts nonzero $\Delta_r$ sums to $r \in H$, reducing Bohr rank $d_t$ from $k^{38}$ to $k^{37}$ and giving $E_k = 1 + (5 + 4 + 28) + (5 + 1) = 44$, so $g(n) \ge (\log n)^{1 + 1/44 - o(1)}$ ($\phi(n) \ge (\log n)^{1+c}$ for any $c \in (0, 1/44)$). This analytic tightening is on paper only (not formalized in Lean).

### 4. How to Check It
Clone the repository and run a single command (`lean` v4.36+, `g++` C++17, Python 3):

    python verify_all.py

This compiles all 8 standalone Pure Lean 4 files (`Init`-only, standard axioms `[propext, Classical.choice, Quot.sound]`, zero `sorry`, zero `native_decide`), audits `#print axioms`, compiles and runs the dual-exact Tomita MCQ C++ verifier (`code/verify_witnesses_143.cpp`) across all 143 witness sets in `data/verified_1_100.txt` and `data/verified_100_143.txt`, runs all C++ lattice executables, and verifies algebraic doubling identities. To regenerate and audit the $k=6$ ($m_+ = 22$) Farkas+SAT UNSAT proof, run `python code/solve_k6_pos.py` (with `g++ -O3 -shared code/gordan_dll.cpp -o code/gordan.dll` or SciPy + PySAT).

### 5. What Is Ours vs. Prior Work
- **Prior work:** Ruzsa (2005) multi-scale 2-adic $L^2$ construction; Sanders (2021) order peeling; Beker (2025) Kelley–Meka $k$-configuration reduction (`1/68`).
- **Ours:** Pure Lean 4 standalone formalizations for $n_{\max}(1..4)$, witnesses `A3..A100`, infinite doubling $n_{\max}(k) \ge k^2+3k-11$, single-sphere orthant lower bound, checkerboard $D_d$ multi-scale construction & explicit `D_5, L=37` crossover; C++ + `__int128` Farkas+SAT UNSAT for $k = 5, 6$; dual-verified witnesses up to $n = 143$; tight $D_d$/$E_8$/$\Lambda_{24}$ computations; and the analytic `1/68 -> 1/44` tightening of Beker (2025).
