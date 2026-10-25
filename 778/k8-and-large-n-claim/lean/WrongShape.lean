import Erdos12
example : ∀ n : ℕ, 4 ≤ n → ∃ σ : Erdos12.Strategy n, Erdos12.WinningStrategy σ := Erdos12.erdos_one_two_main
