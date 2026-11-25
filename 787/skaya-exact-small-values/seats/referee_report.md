# #787 referee report (Opus seat, briefed to refute), returned 2026-11-25 ~10:35Z. Working dir /tmp/e1125/787work/ (bundled). erdosproblems.com not read.

Overall verdict: PARTIAL. Both rows have the same body; f3h93p filed "solved", xgazc7 "partial"; the body says "The full asymptotic problem remains open", so the "solved" row overclaims. Repo cloned at /tmp/e1125/dl787/repo (commit e2cbd9b).

## 1. Witnesses: VERIFIED
- Checker mis.py: CP-SAT maximisation + SAT decision (size α exists, α+1 does not). Edges = distinct pairs only (u≠v, u+v∈A).
- Controls: 300 random small sets (brute force, CP-SAT, SAT agree); {1..n} gives ⌊n/2⌋+1 (3,6,11,21 for n=5,10,20,41); raising A43's last element by 1 moves α 6→9; adding any of 5 random elements to A43 gives α=7.
- Data files (check_data.py → data_check.log): all 144 rows (n=1..143; n=100 in both files) match size, distinctness, edge count, α. BAD 0. All integer sets.
- Lean witness lists (lean_sets.py): 7 sets in Witnesses + 49 in NewWitnesses match claimed α.
- Their C++ verifier: exit 0 on both data files; exit 1 on mutated copies (mut_alpha.txt, mut_set.txt).

## 2. Doubling family: construction VERIFIED; "refutation of k²+k+1" is a strawman
- Hand proof: each step adds 2(k+1)+2 odd numbers, n += 2k+4 ⇒ k²+3k−11. F contains every integer in [−(2k+2), 2k+2] ⇒ the odd block is a clique; even–even sums land only in 2F ⇒ α(F′) ≤ α(F)+1; interval property carries over.
- family.py: sizes 43,59,77,97,119,143,169 have α exactly 6..12.
- Lean infinite_family_n_max_ge, k7_beats_projective_bound compile, standard axioms.
- Nobody conjectured k²+k+1; their monograph §2.3 retracts their own earlier claim. Choi (1971) φ(n) ≤ n^{2/5+o(1)} ⇒ n_max(k) ≥ k^{5/2−o(1)}. New = explicit small-k lower bounds n_max(7) ≥ 59, n_max(8) ≥ 77, ...

## 3. Upper bounds k ≤ 6
- Reduction sound over ℝ: positive sums positive ⇒ graph on A₊ is G_{A₊}; 0 at most once ⇒ n_max(k) ≤ 2n⁺(k)+1. k ≤ 4 Lean statements over ℤ (fine by Choi's reduction); k=5,6 LPs over ℝ.
- k=1..3 Lean compile (standard axioms); monograph hand proofs checked correct. k=4 n_max_4_exact compiles in 748 s; all 60 theorems standard axioms; no sorry/native_decide/extern/implemented_by.
- Own route cegar_pos.py (different encoding, no case split, every blocking core certified exactly in integers; SAT side unproof-logged CaDiCaL): k=3 m=6 SAT / 7 UNSAT; k=4 m=10 SAT / 11 UNSAT (8 cores); k=5 m=15 SAT, {1..10,12,14,16,18,30} α=5 after 6,559 iterations; m=16 UNSAT (2,168 cores, 289 s). ⇒ n_max(5)=31 by two pipelines. Their selftest m=16 UNSAT with 1,814 cores, not the monograph's "68 IIS Farkas cores".
- k=6: re-ran their all_waves: all 21 cases UNSAT in 4,399 s, 314,159 cores (claim 288,228). Case split checked by hand: complete and sound. Re-certified all 214,328 cached short cores (≤8 literals) with own exact routine: all pass; controls show the audit can fail. Later waves reuse cached cores. Negative control on their solver: on m=15/k=5 and m=10/k=4 it does not say UNSAT (reaches the feasible branch, crashes on missing z3). Status: one pipeline only; plain CEGAR at m=22 too slow (400 iterations in 7 min, stopped); no DRAT log; cores longer than 8 literals never logged. g confirmed on [1,43]; g=7 on [44,59] rests on this single k=6 run.
- Reproducibility: `python code/solve_k6_pos.py` with no argument runs only the selftest (m=11,16). gordan_dll.cpp uses __declspec(dllexport), won't compile on Linux without -D'__declspec(x)='; without the library the code silently falls back to float SciPy LP with no exact check.

## 4. 1/68 → 1/44: UNVERIFIED (sketch)
- Against Beker v2 (arXiv 2501.10203v2): Case (10) bounds k⁴⁶·L¹¹ and the k⁶ width loss from S,T density exp(−O(k⁶L²)); E = 1+56+11 = 68.
- The "asymmetric inductive peeling lemma" (synthesis §2.2 l.40) is never stated with hypotheses/conclusion, never proved; per-branch bounds asserted.
- Two-bucket step count looks right ([FHHK Lem 3.4] branch only adds γψ₂^σ ⇒ Δ=∅); alone ≈ 66 (back-of-envelope).
- Referee reconstruction: smallest s with E μ(T(x))^p ≥ ((1+δ)α)^{sp}, weights μ(T)^p, Markov ⇒ μ(T) ≥ (α²/2)^{s−1}, μ(S) ≥ α^p/8; plugged into Beker Prop 3.4 reproduces k²⁸ and E=44. Plausible; needs a full write-up.

## 5. Ruzsa constant: EXPOSITION
- ruzsa_quasipolynomial_nat compiles (standard axioms): ∀ m ≥ 1 ∃ A ⊆ ℤ₊, |A| ≥ 2^{2m²+4m}, M(A) ≤ 8m·2^{4m} ⇒ exp((√(8 log 2)+o(1))√log n) along a subsequence. Ruzsa 2005 paywalled; "sharp"/"pinning Ruzsa's sharp upper constant" unsupported.

## Other
- GeometryAndCarriesStandalone.lean does not compile as shipped: lines 948, 1089, 1442 `/-! --- … --- -/` (unterminated comment); fails v4.27.0, v4.34.1, v4.35.0-rc2 (repro bisect/t1.lean), v4.33.1 exit 1. Fixed copy compiles (standard axioms). verify_all.py cannot pass step 1.
- Other 7 Lean files compile, standard axioms: Erdos787 (64 s), Thresholds, Witnesses, InfiniteFamily, NewWitnesses (1,046 s), AsymptoticClosure (160 s), Threshold45 (748 s). v4.36 not tested.
- C++ PASS only means it ran: ruzsa_lattice_test prints "d=2 r=1 … EXACT alpha=4 (upper bound=3" and exits 0. Lean-proven crossover only D₅ L=37 (dd_beats_quadratic_explicit); "tight" D₅ L=36 rests on an unproved formula.
- Strawmen: "single-sphere myth" refutes the authors' own notes; Erdos787Standalone padded with identities like 4(k²+k+2)−7 = (2k+1)².
