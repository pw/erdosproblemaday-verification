# Probe drafts (formal referee seat) — NOT COMPILED HERE. For the replay seat.
Place each file at the OAI repo root (`lean/`) and run `lake env lean <file>` AFTER the Main closures are built.

| file | expected | what it tests |
|---|---|---|
| RightShape_SharpLog.lean | COMPILES, `#print axioms` ⊆ {propext, Classical.choice, Quot.sound} | (i) page shape "∃ c>0, eventually k^{s-1}/(log k)^c ≤ r(s,k)" (Erdős #986 form) for s ≥ 6 in 6 lines; (ii) the false strengthening "log-exponent s-3" is REFUTED from `main` itself (proves the upper bound has real content: the theorem is not satisfiable by a junk `ramsey`). |
| RightShape_RamseyFive.lean | COMPILES, same axioms | same for s = 5 (exponents 4, 3, 2). |
| WrongShape_SharpLog.lean | MUST FAIL, with the error at the line marked `-- EXPECTED ERROR`, of kind type mismatch / `simpa` failed / linarith failed — NOT parse error / unknown identifier (those would make the probe vacuous). | the lower-bound exponent cannot be read as `s-3` (genuinely false: AKS 1980 gives r(s,t) ≤ C t^{s-1}/(log t)^{s-2} < t^{s-1}/(log t)^{s-3} once log t > C). |
| WrongShape_RamseyFive.lean | MUST FAIL likewise | `t^4/(log t)^2 ≤ r(5,t)` eventually — genuinely false by AKS (also refuted in RightShape_RamseyFive). |
| **Probe_SmallDimension.lean** (HIGH PRIORITY) | expected COMPILES | the s≥6 tree's `actual_prime_construction (i : ℕ) : PrimeConstruction (i+3)` is uniform in i; instantiating i = 0, 1 gives `MainBounds 4` (sharp exponent for r(4,t) — claimed by NEITHER paper) and a second proof of `MainBounds 5`. A compile = the formal development proves strictly more than its papers; a failure = locates a hidden dimension dependence. |
| WrongShape_TrivialUpper.lean | MUST FAIL | `t^s ≤ r(s,t)` eventually — genuinely false by Erdős–Szekeres `r(s,t) ≤ t^{s-1}` (Lean: `Foundation.ramsey_le_pow`); guards against an encoding in which `ramsey` is unboundedly large. |

Why both kinds: a WrongShape that fails proves little alone (anything can fail to elaborate); paired with the
RightShape REFUTATION of the same false statement, compiled from `main`, it shows the statement is contentful
in exactly the direction the false strengthening would exploit.
