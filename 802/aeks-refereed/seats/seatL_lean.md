# Seat L — the Lean formalization vs the paper (no building)
Read /tmp/oaimath/184/seats/COMMON.md first. Report: /tmp/oaimath/184/seats/L_report.md. Work dir: /tmp/oaimath/184/seats/L_work/.
The main seat is kernel-replaying the 31 modules (do NOT build). Your job is to read the source.
1. The comparator statement (ComparatorChallenges/CliqueFreeLog.lean): does it say exactly Theorem 1.1? Check `averageDegree` (2|E|/|V| as a real; what if
   |V| = 0?), `G.indepNum` (Mathlib's definition — is it the independence number?), `G.CliqueFree r`, the order of quantifiers (c chosen before V and G),
   `Real.log` vs natural log, and the universe level `{V : Type}`. Could the statement be vacuous or weaker than the paper in any way?
2. Main.lean: find the theorem that proves `OAI.CliqueFreeLog.logarithmic_independence_bound` and the chain behind it. Build a table: paper item (Lemma 2.1 …
   Proposition 6.1, Theorem 1.1) → Lean file + declaration name. Flag any paper step with NO Lean counterpart and any Lean step that takes a different
   route (e.g. a different constant, a different multiplier construction, a different coupling, a weaker intermediate statement).
3. Audit the sources for anything that could make the kernel check weaker than it looks: `axiom`, `sorry`, `admit`, `native_decide`, `decide := true`,
   `implemented_by`, `extern`, `unsafe`, `opaque`, `set_option` (esp. `maxHeartbeats 0`, `debug.skipKernelTC`), custom `macro`/`elab`/`syntax`,
   `@[csimp]`, `#eval`, `local instance` hacks, `Classical.ofNonempty`-style tricks, `partial def`, `Inhabited`-based junk values reaching the statement.
   Report counts per pattern (the main seat's grep found none of the first block — confirm or refute).
4. Is there an exported max-degree version (the paper's Proposition 6.1: α ≥ n log Δ/(4 D_r Δ) for max degree ≤ Δ, Δ ≥ 3)? Give its exact Lean
   statement and name — the main seat wants to derive Formal Conjectures' `Erdos802.erdos_802` (which has NO d ≥ 2 hypothesis and quantifies over all r)
   from this library, and needs a usable small-degree bound for 0 < d < 2. Copy of FC's statement:
   /home/exedev/.cache/erdos-sources/formal-conjectures/FormalConjectures/ErdosProblems/802.lean. Also: how is `SimpleGraph.averageDegree` defined in FC
   or Mathlib (grep /home/exedev/.cache/erdos-sources/formal-conjectures and /tmp/erdos0300/lean/mathlib4)? Is it provably equal to OpenAI's averageDegree?
5. Note any place where the Lean statement of an intermediate lemma differs from the paper's (e.g. x ≥ 32 vs x > X, strict vs non-strict) — not errors
   necessarily, but the entry must not claim the Lean "follows the paper" where it does not.
