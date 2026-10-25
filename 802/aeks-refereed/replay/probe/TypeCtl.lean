import OAI.Combinatorics.CliqueFree.Main
-- type control: the theorem must NOT prove the r = 3 hypothesis shape directly (it needs 4 ≤ r); this must fail to elaborate
example (r : ℕ) (hr : 3 ≤ r) := OAI.CliqueFreeLog.logarithmic_independence_bound r hr
