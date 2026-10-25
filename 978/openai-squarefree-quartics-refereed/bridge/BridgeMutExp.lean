import Bridge978
open Polynomial Set
namespace Erdos978
open Erdos978Bridge OAI.QuarticPowerFree
theorem mut_parts_ii_exp :
    ∀ {f : ℤ[X]}, Irreducible f → f.natDegree > 3 →
    (¬ ∃ l : ℕ, f.natDegree = 2 ^ l) → 0 < f.leadingCoeff →
    (∀ (p : ℕ), p.Prime → ∃ n : ℕ, ¬ (p : ℤ) ^ (f.natDegree - 2) ∣ f.eval (n : ℤ)) →
    {n : ℕ | Powerfree (f.natDegree - 3) (f.eval (n : ℤ))}.Infinite := by
  intro f hi hd _ _ hp
  have hD := allDegrees f (irreducible_map_of_irreducible hi (by omega)) (by omega)
    (locallyAdmissible_of_exists f _ hp)
  exact (infinite_of_densityStatement f _ hD).mono (fun n hn => powerfree_of_PowerFree hn)

end Erdos978
