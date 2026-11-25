/-!
# GeometryAndCarriesStandalone.lean
### Machine-Checked Pure Lean 4 Formalization of General-d Spherical Rigidity,
### Sharp Carry-Free Radix Thresholds, and Additive Energy Rigidity

This module is completely self-contained in **Pure Lean 4** (`Init` only, zero
external Mathlib imports, zero `sorry`) and formalizes the structural pillars
underlying the asymptotic theory of Erdős Problem #787:

1. **General-Dimension Euclidean Vector Algebra (`List Int`)**
   - `vecAdd`, `vecSub`, `vecScale`, `dot`, `normSq`
   - `normSq_nonneg`, `dot_comm`, `dot_add_left`, `dot_add_right`, `normSq_add`
   - General-d Integer Cauchy-Schwarz: `(dot u p)^2 ≤ normSq u * normSq p`
2. **General-d Spherical Rigidity**
   - Spherical 120-degree Angle Criterion: `2 * dot u v = -Rsq`
   - General-d Spherical `K_4`-Freeness (`‖v_1 + v_2 + v_3 + v_4‖^2 = -2 * Rsq < 0`)
   - General-d 60-degree Directional Cap Sum-Avoidance (threshold, squared, and unit forms)
3. **Sharp Carry-Free Radix Threshold Theorems**
   - `pi_B`, uniqueness of bounded representations (`pi_B_zero_of_bounded`)
   - Injectivity for `B ≥ 2L + 1`, Equation Preservation for `B ≥ 3L + 1`,
     Freiman 2-Isomorphism for `B ≥ 4L + 1`, and explicit sharpness counterexamples
4. **Integer Cauchy-Schwarz, Turán / Caro-Wei Rigidity, and Additive Energy Inequality**
   - List Cauchy-Schwarz `(∑ f(i))^2 ≤ n * ∑ f(i)^2`
   - Representation counts `repSum`, `repSumDistinct`, and additive energy `energy`
   - `n * energy A ≥ (∑_{w ∈ A} repSum A w)^2` and `∑_{w ∈ A} repSumDistinct A w = 2 * numConflictEdges A`
   - Turán / Caro-Wei conflict bound and combined small-α additive energy rigidity
-/

set_option maxRecDepth 2000000

namespace Erdos787GeometryAndCarries

/-! ==================================================================== -/
/-! ### Section 1: General-Dimension Euclidean Vector Algebra (`List Int`) -/
/-! ==================================================================== -/

/-- Componentwise addition of integer vectors represented as `List Int`. -/
def vecAdd : List Int → List Int → List Int
  | x :: xs, y :: ys => (x + y) :: vecAdd xs ys
  | _, _ => []

/-- Componentwise subtraction of integer vectors represented as `List Int`. -/
def vecSub : List Int → List Int → List Int
  | x :: xs, y :: ys => (x - y) :: vecSub xs ys
  | _, _ => []

/-- Scalar multiplication of an integer vector. -/
def vecScale (c : Int) : List Int → List Int
  | [] => []
  | x :: xs => (c * x) :: vecScale c xs

/-- Euclidean inner product (dot product) over `List Int`. -/
def dot : List Int → List Int → Int
  | x :: xs, y :: ys => x * y + dot xs ys
  | _, _ => 0

/-- Squared Euclidean norm `‖u‖^2 = ⟨u, u⟩`. -/
def normSq (u : List Int) : Int :=
  dot u u

/-- Non-negativity of integer squares. -/
theorem int_sq_nonneg (x : Int) : 0 ≤ x * x := by
  cases x with
  | ofNat n => exact Int.natCast_nonneg (n * n)
  | negSucc n => exact Int.natCast_nonneg ((n + 1) * (n + 1))

theorem vecAdd_length : ∀ (u v : List Int), (vecAdd u v).length = min u.length v.length
  | [], _ => by simp [vecAdd]
  | _ :: _, [] => by simp [vecAdd]
  | _ :: xs, _ :: ys => by
    simp only [vecAdd, List.length_cons, vecAdd_length xs ys]
    omega

theorem vecAdd_length_eq (u v : List Int) (h : u.length = v.length) :
    (vecAdd u v).length = u.length := by
  rw [vecAdd_length, h, Nat.min_self]

theorem vecSub_length : ∀ (u v : List Int), (vecSub u v).length = min u.length v.length
  | [], _ => by simp [vecSub]
  | _ :: _, [] => by simp [vecSub]
  | _ :: xs, _ :: ys => by
    simp only [vecSub, List.length_cons, vecSub_length xs ys]
    omega

theorem vecSub_length_eq (u v : List Int) (h : u.length = v.length) :
    (vecSub u v).length = u.length := by
  rw [vecSub_length, h, Nat.min_self]

theorem vecScale_length (c : Int) : ∀ (u : List Int), (vecScale c u).length = u.length
  | [] => rfl
  | _ :: xs => by simp [vecScale, vecScale_length c xs]

theorem vecAdd_comm : ∀ (u v : List Int), vecAdd u v = vecAdd v u
  | [], [] => rfl
  | [], _ :: _ => rfl
  | _ :: _, [] => rfl
  | x :: xs, y :: ys => by
    simp [vecAdd, Int.add_comm x y, vecAdd_comm xs ys]

theorem vecAdd_assoc : ∀ (u v w : List Int), vecAdd (vecAdd u v) w = vecAdd u (vecAdd v w)
  | [], _, _ => by simp [vecAdd]
  | _ :: _, [], _ => by simp [vecAdd]
  | _ :: _, _ :: _, [] => by simp [vecAdd]
  | x :: xs, y :: ys, z :: zs => by
    simp [vecAdd, Int.add_assoc x y z, vecAdd_assoc xs ys zs]

/-- Non-negativity of squared Euclidean norm in arbitrary dimension. -/
theorem normSq_nonneg : ∀ (u : List Int), 0 ≤ normSq u
  | [] => by simp [normSq, dot]
  | x :: xs => by
    have hx : 0 ≤ x * x := int_sq_nonneg x
    have hxs : 0 ≤ normSq xs := normSq_nonneg xs
    have hdef : normSq (x :: xs) = x * x + normSq xs := rfl
    omega

/-- Symmetry of the Euclidean dot product in arbitrary dimension. -/
theorem dot_comm : ∀ (u v : List Int), dot u v = dot v u
  | [], [] => rfl
  | [], _ :: _ => rfl
  | _ :: _, [] => rfl
  | x :: xs, y :: ys => by
    simp [dot, Int.mul_comm x y, dot_comm xs ys]

/-- Left linearity of dot product with respect to vector addition of equal-length vectors. -/
theorem dot_add_left : ∀ (u v w : List Int), u.length = v.length →
    dot (vecAdd u v) w = dot u w + dot v w
  | [], [], _, _ => by simp [vecAdd, dot]
  | _ :: _, [], _, h => by simp at h
  | [], _ :: _, _, h => by simp at h
  | _ :: _, _ :: _, [], _ => by simp [vecAdd, dot]
  | x :: xs, y :: ys, z :: zs, h => by
    simp only [List.length_cons, Nat.succ.injEq] at h
    have ih := dot_add_left xs ys zs h
    simp only [vecAdd, dot]
    rw [ih, Int.add_mul]
    omega

/-- Right linearity of dot product with respect to vector addition of equal-length vectors. -/
theorem dot_add_right (u v w : List Int) (hvw : v.length = w.length) :
    dot u (vecAdd v w) = dot u v + dot u w := by
  rw [dot_comm u (vecAdd v w), dot_add_left v w u hvw, dot_comm v u, dot_comm w u]

/-- Left homogeneity of dot product under scalar multiplication. -/
theorem dot_scale_left (c : Int) : ∀ (u v : List Int), dot (vecScale c u) v = c * dot u v
  | [], _ => by simp [vecScale, dot]
  | _ :: _, [] => by simp [vecScale, dot]
  | x :: xs, y :: ys => by
    simp only [vecScale, dot]
    rw [dot_scale_left c xs ys, Int.mul_add, Int.mul_assoc]

/-- Right homogeneity of dot product under scalar multiplication. -/
theorem dot_scale_right (c : Int) (u v : List Int) : dot u (vecScale c v) = c * dot u v := by
  rw [dot_comm u (vecScale c v), dot_scale_left c v u, dot_comm v u]

/-- Polarization / sum-norm expansion: `‖u + v‖^2 = ‖u‖^2 + ‖v‖^2 + 2⟨u, v⟩`. -/
theorem normSq_add (u v : List Int) (huv : u.length = v.length) :
    normSq (vecAdd u v) = normSq u + normSq v + 2 * dot u v := by
  unfold normSq
  rw [dot_add_left u v (vecAdd u v) huv]
  rw [dot_add_right u u v huv, dot_add_right v u v huv]
  rw [dot_comm v u]
  omega

/-- Squared norm of a scaled vector: `‖c • u‖^2 = c^2 * ‖u‖^2`. -/
theorem normSq_scale (c : Int) (u : List Int) :
    normSq (vecScale c u) = c * c * normSq u := by
  unfold normSq
  rw [dot_scale_left, dot_scale_right, Int.mul_assoc]

/-- Squared norm of a linear combination `a • u + b • v`. -/
theorem normSq_scale_add (a b : Int) (u v : List Int) (huv : u.length = v.length) :
    normSq (vecAdd (vecScale a u) (vecScale b v)) =
      a * a * normSq u + b * b * normSq v + 2 * a * b * dot u v := by
  have hlen : (vecScale a u).length = (vecScale b v).length := by
    rw [vecScale_length, vecScale_length, huv]
  rw [normSq_add (vecScale a u) (vecScale b v) hlen]
  rw [normSq_scale a u, normSq_scale b v, dot_scale_left a u (vecScale b v), dot_scale_right b u v]
  have h2ab : 2 * (a * (b * dot u v)) = 2 * a * b * dot u v := by
    rw [← Int.mul_assoc 2 a (b * dot u v), ← Int.mul_assoc (2 * a) b (dot u v)]
  omega

/-- If `‖p‖^2 = 0`, then `⟨u, p⟩ = 0` for every vector `u`. -/
theorem dot_eq_zero_of_normSq_eq_zero : ∀ (u p : List Int), normSq p = 0 → dot u p = 0
  | _, [], _ => by simp [dot]
  | [], _ :: _, _ => by simp [dot]
  | _ :: xs, y :: ys, hp => by
    have hy_nn : 0 ≤ y * y := int_sq_nonneg y
    have hys_nn : 0 ≤ normSq ys := normSq_nonneg ys
    have hdef : normSq (y :: ys) = y * y + normSq ys := rfl
    rw [hdef] at hp
    have hy_sq : y * y = 0 := by omega
    have hys0 : normSq ys = 0 := by omega
    have hy0 : y = 0 := by
      rcases Int.mul_eq_zero.mp hy_sq with h | h <;> exact h
    have ih := dot_eq_zero_of_normSq_eq_zero xs ys hys0
    simp [dot, hy0, ih]

private theorem cs_algebra (U P D : Int) :
    P * P * U + (-D) * (-D) * P + 2 * P * (-D) * D = P * (U * P - D * D) := by
  have h1 : P * P * U = P * (U * P) := by
    rw [Int.mul_assoc, Int.mul_comm P U]
  have h2 : (-D) * (-D) * P = P * (D * D) := by
    rw [Int.neg_mul, Int.mul_neg, Int.neg_neg, Int.mul_comm (D * D) P]
  have h3 : 2 * P * (-D) * D = - (2 * (P * (D * D))) := by
    calc 2 * P * (-D) * D
        = (2 * (P * (-D))) * D := by rw [Int.mul_assoc 2 P (-D)]
      _ = (2 * (-(P * D))) * D := by rw [Int.mul_neg]
      _ = (-(2 * (P * D))) * D := by rw [Int.mul_neg]
      _ = -((2 * (P * D)) * D) := by rw [Int.neg_mul]
      _ = -(2 * ((P * D) * D)) := by rw [Int.mul_assoc 2 (P * D) D]
      _ = -(2 * (P * (D * D))) := by rw [Int.mul_assoc P D D]
  have h4 : P * (U * P - D * D) = P * (U * P) - P * (D * D) := by
    rw [Int.sub_eq_add_neg, Int.mul_add, Int.mul_neg, ← Int.sub_eq_add_neg]
  omega

/--
General-Dimension Integer Cauchy-Schwarz Inequality:
For any two vectors `u, p : List Int` of equal length,
  `(dot u p)^2 ≤ normSq u * normSq p`.
Proved via `‖normSq p • u - dot u p • p‖^2 ≥ 0`.
-/
theorem cauchy_schwarz_int (u p : List Int) (hup : u.length = p.length) :
    dot u p * dot u p ≤ normSq u * normSq p := by
  by_cases hp0 : normSq p = 0
  · have hd0 := dot_eq_zero_of_normSq_eq_zero u p hp0
    rw [hd0, hp0]
    simp
  · have hp_nn : 0 ≤ normSq p := normSq_nonneg p
    have hp_pos : 0 < normSq p := by omega
    have hnn : 0 ≤ normSq (vecAdd (vecScale (normSq p) u) (vecScale (-dot u p) p)) :=
      normSq_nonneg _
    rw [normSq_scale_add (normSq p) (-dot u p) u p hup] at hnn
    rw [cs_algebra (normSq u) (normSq p) (dot u p)] at hnn
    have hmul : normSq p * 0 ≤ normSq p * (normSq u * normSq p - dot u p * dot u p) := by
      simpa [Int.mul_zero] using hnn
    have hdiff := Int.le_of_mul_le_mul_left hmul hp_pos
    omega


/-! ==================================================================== -/
/-! ### Section 2: General-d Spherical Rigidity & Directional Caps         -/
/-! ==================================================================== -/

/--
Theorem 2.1 (General-d Spherical 120° Angle Criterion):
If equal-length vectors `u, v` and their sum `u + v` all satisfy `normSq x = Rsq`,
then `2 * ⟨u, v⟩ = -Rsq`.
-/
theorem spherical_angle_criterion (u v : List Int) (Rsq : Int)
    (huv : u.length = v.length)
    (hu : normSq u = Rsq) (hv : normSq v = Rsq)
    (hsum : normSq (vecAdd u v) = Rsq) :
    2 * dot u v = -Rsq := by
  have hexp := normSq_add u v huv
  omega

/-- Four-vector squared norm expansion in arbitrary dimension `d`. -/
theorem normSq_sum4 (v1 v2 v3 v4 : List Int)
    (h12 : v1.length = v2.length) (h23 : v2.length = v3.length) (h34 : v3.length = v4.length) :
    normSq (vecAdd (vecAdd v1 v2) (vecAdd v3 v4)) =
      normSq v1 + normSq v2 + normSq v3 + normSq v4 +
      2 * dot v1 v2 + 2 * dot v1 v3 + 2 * dot v1 v4 +
      2 * dot v2 v3 + 2 * dot v2 v4 + 2 * dot v3 v4 := by
  have h12_len : (vecAdd v1 v2).length = v1.length := vecAdd_length_eq v1 v2 h12
  have h34_len : (vecAdd v3 v4).length = v3.length := vecAdd_length_eq v3 v4 h34
  have hlen : (vecAdd v1 v2).length = (vecAdd v3 v4).length := by omega
  rw [normSq_add (vecAdd v1 v2) (vecAdd v3 v4) hlen]
  rw [normSq_add v1 v2 h12, normSq_add v3 v4 h34]
  rw [dot_add_left v1 v2 (vecAdd v3 v4) h12]
  rw [dot_add_right v1 v3 v4 h34, dot_add_right v2 v3 v4 h34]
  omega

/--
Theorem 2.2 (General-d Spherical `K_4`-Freeness):
If four equal-length vectors `v1, v2, v3, v4` satisfy `‖v_i‖^2 = Rsq > 0`
and all 6 pairwise dot products satisfy `2 * ⟨v_i, v_j⟩ = -Rsq`, then
`‖v_1 + v_2 + v_3 + v_4‖^2 = -2 * Rsq < 0`, yielding `False`.
-/
theorem spherical_k4_freeness
    (Rsq : Int) (hR : 0 < Rsq)
    (v1 v2 v3 v4 : List Int)
    (h12 : v1.length = v2.length) (h23 : v2.length = v3.length) (h34 : v3.length = v4.length)
    (hn1 : normSq v1 = Rsq) (hn2 : normSq v2 = Rsq)
    (hn3 : normSq v3 = Rsq) (hn4 : normSq v4 = Rsq)
    (hd12 : 2 * dot v1 v2 = -Rsq) (hd13 : 2 * dot v1 v3 = -Rsq)
    (hd14 : 2 * dot v1 v4 = -Rsq) (hd23 : 2 * dot v2 v3 = -Rsq)
    (hd24 : 2 * dot v2 v4 = -Rsq) (hd34 : 2 * dot v3 v4 = -Rsq) :
    False := by
  have hexp := normSq_sum4 v1 v2 v3 v4 h12 h23 h34
  have hnn := normSq_nonneg (vecAdd (vecAdd v1 v2) (vecAdd v3 v4))
  omega

/--
Theorem 2.3 (General-d Spherical `K_4`-Clique Impossibility):
Four equal-length vectors on a sphere `‖v_i‖^2 = Rsq > 0` cannot have all
six pairwise sums `v_i + v_j` also lying on the sphere.
-/
theorem spherical_k4_clique_impossible
    (Rsq : Int) (hR : 0 < Rsq)
    (v1 v2 v3 v4 : List Int)
    (h12 : v1.length = v2.length) (h23 : v2.length = v3.length) (h34 : v3.length = v4.length)
    (hn1 : normSq v1 = Rsq) (hn2 : normSq v2 = Rsq)
    (hn3 : normSq v3 = Rsq) (hn4 : normSq v4 = Rsq)
    (hs12 : normSq (vecAdd v1 v2) = Rsq) (hs13 : normSq (vecAdd v1 v3) = Rsq)
    (hs14 : normSq (vecAdd v1 v4) = Rsq) (hs23 : normSq (vecAdd v2 v3) = Rsq)
    (hs24 : normSq (vecAdd v2 v4) = Rsq) (hs34 : normSq (vecAdd v3 v4) = Rsq) :
    False := by
  have h13 : v1.length = v3.length := by omega
  have h14 : v1.length = v4.length := by omega
  have h24 : v2.length = v4.length := by omega
  exact spherical_k4_freeness Rsq hR v1 v2 v3 v4 h12 h23 h34 hn1 hn2 hn3 hn4
    (spherical_angle_criterion v1 v2 Rsq h12 hn1 hn2 hs12)
    (spherical_angle_criterion v1 v3 Rsq h13 hn1 hn3 hs13)
    (spherical_angle_criterion v1 v4 Rsq h14 hn1 hn4 hs14)
    (spherical_angle_criterion v2 v3 Rsq h23 hn2 hn3 hs23)
    (spherical_angle_criterion v2 v4 Rsq h24 hn2 hn4 hs24)
    (spherical_angle_criterion v3 v4 Rsq h34 hn3 hn4 hs34)

/-- A list `S` of vectors is spherical of dimension `d` and squared radius `Rsq > 0`. -/
def IsSphericalSetVec (d : Nat) (Rsq : Int) (S : List (List Int)) : Prop :=
  0 < Rsq ∧ ∀ v ∈ S, v.length = d ∧ normSq v = Rsq

/-- Sum-avoidance predicate for integer vector lists in `ℤ^d`. -/
def IsSumAvoidingVec (S B : List (List Int)) : Prop :=
  ∀ u ∈ B, ∀ v ∈ B, u ≠ v → vecAdd u v ∉ S

/--
Theorem 2.4 (Set-Level General-d `K_4`-Freeness):
No duplicate-free 4-element subset `C` of a spherical vector set `S`
can form a 4-clique in the vector sum-conflict graph.
-/
theorem spherical_k4_free_set (d : Nat) (Rsq : Int) (S C : List (List Int))
    (hS : IsSphericalSetVec d Rsq S)
    (hNodup : C.Nodup) (hLen : C.length = 4)
    (hSub : ∀ v ∈ C, v ∈ S)
    (hClique : ∀ u ∈ C, ∀ v ∈ C, u ≠ v → vecAdd u v ∈ S) :
    False := by
  rcases hS with ⟨hR, hSph⟩
  match C with
  | [v1, v2, v3, v4] =>
    have hm1 : v1 ∈ [v1, v2, v3, v4] := by simp
    have hm2 : v2 ∈ [v1, v2, v3, v4] := by simp
    have hm3 : v3 ∈ [v1, v2, v3, v4] := by simp
    have hm4 : v4 ∈ [v1, v2, v3, v4] := by simp
    rcases List.nodup_cons.mp hNodup with ⟨hn1_mem, hNodup234⟩
    rcases List.nodup_cons.mp hNodup234 with ⟨hn2_mem, hNodup34⟩
    rcases List.nodup_cons.mp hNodup34 with ⟨hn3_mem, _⟩
    have hne12 : v1 ≠ v2 := fun h => hn1_mem (by simp [h])
    have hne13 : v1 ≠ v3 := fun h => hn1_mem (by simp [h])
    have hne14 : v1 ≠ v4 := fun h => hn1_mem (by simp [h])
    have hne23 : v2 ≠ v3 := fun h => hn2_mem (by simp [h])
    have hne24 : v2 ≠ v4 := fun h => hn2_mem (by simp [h])
    have hne34 : v3 ≠ v4 := fun h => hn3_mem (by simp [h])
    rcases hSph v1 (hSub v1 hm1) with ⟨hl1, hn1⟩
    rcases hSph v2 (hSub v2 hm2) with ⟨hl2, hn2⟩
    rcases hSph v3 (hSub v3 hm3) with ⟨hl3, hn3⟩
    rcases hSph v4 (hSub v4 hm4) with ⟨hl4, hn4⟩
    exact spherical_k4_clique_impossible Rsq hR v1 v2 v3 v4
      (by omega) (by omega) (by omega) hn1 hn2 hn3 hn4
      (hSph _ (hClique v1 hm1 v2 hm2 hne12)).2
      (hSph _ (hClique v1 hm1 v3 hm3 hne13)).2
      (hSph _ (hClique v1 hm1 v4 hm4 hne14)).2
      (hSph _ (hClique v2 hm2 v3 hm3 hne23)).2
      (hSph _ (hClique v2 hm2 v4 hm4 hne24)).2
      (hSph _ (hClique v3 hm3 v4 hm4 hne34)).2
  | [] => simp at hLen
  | [_] => simp at hLen
  | [_, _] => simp at hLen
  | [_, _, _] => simp at hLen
  | _ :: _ :: _ :: _ :: _ :: _ => simp at hLen

/--
Theorem 2.5 (General-d 60° Directional Cap Sum-Avoidance — Threshold Form):
If `2 * ⟨u, p⟩ > T` and `2 * ⟨v, p⟩ > T` where `T ≥ 0` and `T^2 ≥ Rsq * ‖p‖^2` (`‖p‖^2 > 0`),
then `‖u + v‖^2 * ‖p‖^2 ≥ ⟨u + v, p⟩^2 > T^2 ≥ Rsq * ‖p‖^2`, hence `‖u + v‖^2 > Rsq`.
-/
theorem directional_cap_sum_avoidance (u v p : List Int) (Rsq T : Int)
    (hup : u.length = p.length) (hvp : v.length = p.length)
    (hp : 0 < normSq p) (hT_nonneg : 0 ≤ T)
    (hT_sq : Rsq * normSq p ≤ T * T)
    (hu : T < 2 * dot u p) (hv : T < 2 * dot v p) :
    Rsq < normSq (vecAdd u v) := by
  have huv : u.length = v.length := by omega
  have hsum_len : (vecAdd u v).length = p.length := by
    rw [vecAdd_length_eq u v huv, hup]
  have hlin : dot (vecAdd u v) p = dot u p + dot v p := dot_add_left u v p huv
  have hs_gt : T < dot (vecAdd u v) p := by omega
  have hTs1 : T * T ≤ T * dot (vecAdd u v) p :=
    Int.mul_le_mul_of_nonneg_left (by omega) hT_nonneg
  have hTs2 : T * dot (vecAdd u v) p < dot (vecAdd u v) p * dot (vecAdd u v) p :=
    Int.mul_lt_mul_of_pos_right hs_gt (by omega)
  have hcs := cauchy_schwarz_int (vecAdd u v) p hsum_len
  have hlt_prod : Rsq * normSq p < normSq (vecAdd u v) * normSq p := by omega
  exact Int.lt_of_mul_lt_mul_right hlt_prod (by omega)

/--
Theorem 2.6 (General-d 60° Directional Cap Sum-Avoidance — Squared Form):
Without square roots or auxiliary `T`, if `⟨u, p⟩ > 0`, `⟨v, p⟩ > 0`,
`4 * ⟨u, p⟩^2 > Rsq * ‖p‖^2`, and `4 * ⟨v, p⟩^2 > Rsq * ‖p‖^2` (`‖p‖^2 > 0`),
then `‖u + v‖^2 > Rsq`.
-/
theorem directional_cap_sum_avoidance_sq (u v p : List Int) (Rsq : Int)
    (hup : u.length = p.length) (hvp : v.length = p.length)
    (hp : 0 < normSq p)
    (hu_pos : 0 < dot u p) (hv_pos : 0 < dot v p)
    (hu : Rsq * normSq p < 4 * (dot u p * dot u p))
    (hv : Rsq * normSq p < 4 * (dot v p * dot v p)) :
    Rsq < normSq (vecAdd u v) := by
  have huv : u.length = v.length := by omega
  have hsum_len : (vecAdd u v).length = p.length := by
    rw [vecAdd_length_eq u v huv, hup]
  have hlin : dot (vecAdd u v) p = dot u p + dot v p := dot_add_left u v p huv
  have hsq_ge : Rsq * normSq p < dot (vecAdd u v) p * dot (vecAdd u v) p := by
    by_cases hab : dot u p ≤ dot v p
    · have h4 : 4 * (dot u p * dot u p) = (2 * dot u p) * (2 * dot u p) := by
        calc 4 * (dot u p * dot u p)
            = (2 * 2) * (dot u p * dot u p) := rfl
          _ = 2 * (2 * (dot u p * dot u p)) := by rw [Int.mul_assoc 2 2 _]
          _ = 2 * ((2 * dot u p) * dot u p) := by rw [Int.mul_assoc 2 (dot u p) (dot u p)]
          _ = 2 * (dot u p * (2 * dot u p)) := by rw [Int.mul_comm (2 * dot u p) (dot u p)]
          _ = (2 * dot u p) * (2 * dot u p) := by rw [Int.mul_assoc 2 (dot u p) (2 * dot u p)]
      have hle : (2 * dot u p) * (2 * dot u p) ≤ (dot u p + dot v p) * (dot u p + dot v p) :=
        Int.mul_le_mul (by omega) (by omega) (by omega) (by omega)
      rw [hlin]
      omega
    · have h4 : 4 * (dot v p * dot v p) = (2 * dot v p) * (2 * dot v p) := by
        calc 4 * (dot v p * dot v p)
            = (2 * 2) * (dot v p * dot v p) := rfl
          _ = 2 * (2 * (dot v p * dot v p)) := by rw [Int.mul_assoc 2 2 _]
          _ = 2 * ((2 * dot v p) * dot v p) := by rw [Int.mul_assoc 2 (dot v p) (dot v p)]
          _ = 2 * (dot v p * (2 * dot v p)) := by rw [Int.mul_comm (2 * dot v p) (dot v p)]
          _ = (2 * dot v p) * (2 * dot v p) := by rw [Int.mul_assoc 2 (dot v p) (2 * dot v p)]
      have hle : (2 * dot v p) * (2 * dot v p) ≤ (dot u p + dot v p) * (dot u p + dot v p) :=
        Int.mul_le_mul (by omega) (by omega) (by omega) (by omega)
      rw [hlin]
      omega
  have hcs := cauchy_schwarz_int (vecAdd u v) p hsum_len
  have hlt_prod : Rsq * normSq p < normSq (vecAdd u v) * normSq p := by omega
  exact Int.lt_of_mul_lt_mul_right hlt_prod (by omega)

/--
Theorem 2.7 (Unit-Direction 60° Directional Cap Sum-Avoidance):
When `‖p‖^2 = 1` and `R ≥ 0`, `2 * ⟨u, p⟩ > R` and `2 * ⟨v, p⟩ > R` imply `‖u + v‖^2 > R^2`.
-/
theorem directional_cap_sum_avoidance_unit (u v p : List Int) (R : Int)
    (hup : u.length = p.length) (hvp : v.length = p.length)
    (hp : normSq p = 1) (hR : 0 ≤ R)
    (hu : R < 2 * dot u p) (hv : R < 2 * dot v p) :
    R * R < normSq (vecAdd u v) := by
  exact directional_cap_sum_avoidance u v p (R * R) R hup hvp
    (by omega) hR (by rw [hp]; omega) hu hv

/-- Computable 60-degree directional cap extracted from `S` around direction `p`. -/
def directionalCapVec (S : List (List Int)) (p : List Int) (T : Int) : List (List Int) :=
  S.filter (fun x => decide (T < 2 * dot x p))

/--
Theorem 2.8 (Set-Level 60° Directional Cap Sum-Avoidance):
Every directional cap `directionalCapVec S p T` with `T^2 ≥ Rsq * ‖p‖^2` (`T ≥ 0, ‖p‖^2 > 0`)
is unconditionally sum-avoiding with respect to any spherical set `S` of dimension `d` and squared radius `Rsq`.
-/
theorem directionalCapVec_sum_avoiding (d : Nat) (Rsq T : Int)
    (S : List (List Int)) (p : List Int)
    (hS : IsSphericalSetVec d Rsq S) (hp_len : p.length = d)
    (hp_pos : 0 < normSq p) (hT_nn : 0 ≤ T) (hT_sq : Rsq * normSq p ≤ T * T) :
    IsSumAvoidingVec S (directionalCapVec S p T) := by
  intro u hu v hv _ hmem
  rcases List.mem_filter.mp hu with ⟨huS, hu_cap⟩
  rcases List.mem_filter.mp hv with ⟨hvS, hv_cap⟩
  have hu_gt : T < 2 * dot u p := by
    simpa [decide_eq_true_eq] using hu_cap
  have hv_gt : T < 2 * dot v p := by
    simpa [decide_eq_true_eq] using hv_cap
  have hgt := directional_cap_sum_avoidance u v p Rsq T
    (by rw [(hS.2 u huS).1, hp_len])
    (by rw [(hS.2 v hvS).1, hp_len])
    hp_pos hT_nn hT_sq hu_gt hv_gt
  have heq := (hS.2 (vecAdd u v) hmem).2
  omega


/-! ==================================================================== -/
/-! ### Section 3: Sharp Carry-Free Radix Threshold Theorems             -/
/-! ==================================================================== -/

/-- Radix-`B` polynomial projection `π_B(x) = ∑_{i=0}^{d-1} x_i B^i` via Horner's rule. -/
def pi_B (B : Int) : List Int → Int
  | [] => 0
  | x :: xs => x + B * pi_B B xs

/-- Explicit power-series form `∑_{i} x_i B^{k+i}` to confirm equivalence with Horner's rule. -/
def pi_B_pow (B : Int) (k : Nat) : List Int → Int
  | [] => 0
  | x :: xs => x * B ^ k + pi_B_pow B (k + 1) xs

theorem pi_B_pow_shift (B : Int) :
    ∀ (k : Nat) (u : List Int), pi_B_pow B (k + 1) u = B * pi_B_pow B k u
  | _, [] => by simp [pi_B_pow]
  | k, x :: xs => by
    simp only [pi_B_pow, pi_B_pow_shift B (k + 1) xs, Int.mul_add]
    have hpow : x * B ^ (k + 1) = B * (x * B ^ k) := by
      rw [Int.pow_succ, Int.mul_comm (B ^ k) B, ← Int.mul_assoc, Int.mul_comm x B, Int.mul_assoc]
    rw [hpow]

/-- Equivalence `pi_B B u = ∑_i u_i B^i`. -/
theorem pi_B_eq_pow_sum (B : Int) : ∀ (u : List Int), pi_B B u = pi_B_pow B 0 u
  | [] => rfl
  | x :: xs => by
    simp only [pi_B, pi_B_pow, Int.pow_zero, Int.mul_one]
    rw [pi_B_eq_pow_sum B xs, pi_B_pow_shift B 0 xs]

/-- Additivity of `pi_B` on equal-length vectors. -/
theorem pi_B_add (B : Int) : ∀ (u v : List Int), u.length = v.length →
    pi_B B (vecAdd u v) = pi_B B u + pi_B B v
  | [], [], _ => by simp [vecAdd, pi_B]
  | _ :: _, [], h => by simp at h
  | [], _ :: _, h => by simp at h
  | x :: xs, y :: ys, h => by
    simp only [List.length_cons, Nat.succ.injEq] at h
    have ih := pi_B_add B xs ys h
    simp only [vecAdd, pi_B]
    rw [ih, Int.mul_add]
    omega

/-- Subtractivity of `pi_B` on equal-length vectors. -/
theorem pi_B_sub (B : Int) : ∀ (u v : List Int), u.length = v.length →
    pi_B B (vecSub u v) = pi_B B u - pi_B B v
  | [], [], _ => by simp [vecSub, pi_B]
  | _ :: _, [], h => by simp at h
  | [], _ :: _, h => by simp at h
  | x :: xs, y :: ys, h => by
    simp only [List.length_cons, Nat.succ.injEq] at h
    have ih := pi_B_sub B xs ys h
    simp only [vecSub, pi_B]
    have hmul : B * (pi_B B xs - pi_B B ys) = B * pi_B B xs - B * pi_B B ys := by
      rw [Int.sub_eq_add_neg, Int.mul_add, Int.mul_neg, ← Int.sub_eq_add_neg]
    rw [ih, hmul]
    omega

/-- Absolute value on `Int`. -/
def absInt (x : Int) : Int :=
  if 0 ≤ x then x else -x

theorem absInt_lt_iff (x B : Int) : absInt x < B ↔ -B < x ∧ x < B := by
  unfold absInt
  split <;> omega

theorem absInt_le_iff (x L : Int) : absInt x ≤ L ↔ -L ≤ x ∧ x ≤ L := by
  unfold absInt
  split <;> omega

/--
Theorem 3.1 (Unique Zero Representation Below Base `B`):
If every coordinate `d_i` of `Δ : List Int` satisfies `|d_i| < B`, and `pi_B B Δ = 0`,
then every coordinate `d_i = 0`. Proved by induction on vector length `d`.
-/
theorem pi_B_zero_of_bounded (B : Int) :
    ∀ (Δ : List Int), (∀ d ∈ Δ, absInt d < B) → pi_B B Δ = 0 → ∀ d ∈ Δ, d = 0
  | [], _, _, _, hmem => by cases hmem
  | d :: ds, hbound, hpi, x, hx => by
    have hd_abs : absInt d < B := hbound d (by simp)
    have hd_bnd : -B < d ∧ d < B := (absInt_lt_iff d B).mp hd_abs
    have hB_pos : 0 < B := by omega
    have hpi_def : d + B * pi_B B ds = 0 := hpi
    let q : Int := -pi_B B ds
    have hd_eq_Bq : d = B * q := by
      have hneg : B * (-pi_B B ds) = -(B * pi_B B ds) := Int.mul_neg B (pi_B B ds)
      change d = B * (-pi_B B ds)
      omega
    have hq_zero : q = 0 := by
      by_cases hq_ge : 1 ≤ q
      · have hle : B * 1 ≤ B * q := Int.mul_le_mul_of_nonneg_left hq_ge (by omega)
        rw [Int.mul_one, ← hd_eq_Bq] at hle
        omega
      · by_cases hq_le : q ≤ -1
        · have hle : B * q ≤ B * (-1) := Int.mul_le_mul_of_nonneg_left hq_le (by omega)
          rw [← hd_eq_Bq, Int.mul_neg, Int.mul_one] at hle
          omega
        · omega
    have hd_zero : d = 0 := by
      rw [hd_eq_Bq, hq_zero, Int.mul_zero]
    have hds_zero : pi_B B ds = 0 := by
      change -pi_B B ds = 0 at hq_zero
      omega
    have ih := pi_B_zero_of_bounded B ds (fun z hz => hbound z (by simp [hz])) hds_zero
    simp only [List.mem_cons] at hx
    rcases hx with rfl | hx_tail
    · exact hd_zero
    · exact ih x hx_tail

/-- Coordinate box `[-L, L]^d`. -/
def inBox (L : Int) (u : List Int) : Prop :=
  ∀ x ∈ u, -L ≤ x ∧ x ≤ L

theorem inBox_iff_absInt (L : Int) (u : List Int) :
    inBox L u ↔ ∀ x ∈ u, absInt x ≤ L := by
  constructor
  · intro h x hx
    exact (absInt_le_iff x L).mpr (h x hx)
  · intro h x hx
    exact (absInt_le_iff x L).mp (h x hx)

private theorem vecSub_all_zero_imp_eq :
    ∀ (u v : List Int), u.length = v.length → (∀ d ∈ vecSub u v, d = 0) → u = v
  | [], [], _, _ => rfl
  | _ :: _, [], h, _ => by simp at h
  | [], _ :: _, h, _ => by simp at h
  | x :: xs, y :: ys, h, hzero => by
    simp only [List.length_cons, Nat.succ.injEq] at h
    have hxy0 : x - y = 0 := hzero (x - y) (by simp [vecSub])
    have hxy : x = y := by omega
    have ih := vecSub_all_zero_imp_eq xs ys h (fun z hz => hzero z (by simp [vecSub, hz]))
    simp [hxy, ih]

private theorem vecAdd_bounds (a1 b1 a2 b2 : Int) :
    ∀ (u v : List Int), u.length = v.length →
      (∀ x ∈ u, a1 ≤ x ∧ x ≤ b1) →
      (∀ y ∈ v, a2 ≤ y ∧ y ≤ b2) →
      ∀ z ∈ vecAdd u v, a1 + a2 ≤ z ∧ z ≤ b1 + b2
  | [], [], _, _, _, _, hz => by simp [vecAdd] at hz
  | _ :: _, [], h, _, _, _, _ => by simp at h
  | [], _ :: _, h, _, _, _, _ => by simp at h
  | x :: xs, y :: ys, h, hu, hv, z, hz => by
    simp only [List.length_cons, Nat.succ.injEq] at h
    simp only [vecAdd, List.mem_cons] at hz
    rcases hz with rfl | hz_tail
    · have hx := hu x (by simp)
      have hy := hv y (by simp)
      omega
    · exact vecAdd_bounds a1 b1 a2 b2 xs ys h
        (fun a ha => hu a (by simp [ha]))
        (fun b hb => hv b (by simp [hb]))
        z hz_tail

private theorem vecSub_bounds (a1 b1 a2 b2 : Int) :
    ∀ (u v : List Int), u.length = v.length →
      (∀ x ∈ u, a1 ≤ x ∧ x ≤ b1) →
      (∀ y ∈ v, a2 ≤ y ∧ y ≤ b2) →
      ∀ z ∈ vecSub u v, a1 - b2 ≤ z ∧ z ≤ b1 - a2
  | [], [], _, _, _, _, hz => by simp [vecSub] at hz
  | _ :: _, [], h, _, _, _, _ => by simp at h
  | [], _ :: _, h, _, _, _, _ => by simp at h
  | x :: xs, y :: ys, h, hu, hv, z, hz => by
    simp only [List.length_cons, Nat.succ.injEq] at h
    simp only [vecSub, List.mem_cons] at hz
    rcases hz with rfl | hz_tail
    · have hx := hu x (by simp)
      have hy := hv y (by simp)
      omega
    · exact vecSub_bounds a1 b1 a2 b2 xs ys h
        (fun a ha => hu a (by simp [ha]))
        (fun b hb => hv b (by simp [hb]))
        z hz_tail

/--
Theorem 3.2 (Injectivity for `B ≥ 2L + 1`):
On equal-length vectors in `[-L, L]^d`, `pi_B B` is injective whenever `B ≥ 2 * L + 1`.
-/
theorem pi_B_inj_of_ge_2L_add_1 (B L : Int) (u v : List Int)
    (huv : u.length = v.length) (hu : inBox L u) (hv : inBox L v)
    (hB : 2 * L + 1 ≤ B) :
    pi_B B u = pi_B B v ↔ u = v := by
  constructor
  · intro hpi
    have hsub_pi : pi_B B (vecSub u v) = 0 := by
      rw [pi_B_sub B u v huv]
      omega
    have hsub_bnd := vecSub_bounds (-L) L (-L) L u v huv hu hv
    have hsub_abs : ∀ d ∈ vecSub u v, absInt d < B := by
      intro d hd
      have hdb := hsub_bnd d hd
      exact (absInt_lt_iff d B).mpr (by omega)
    have hzeros := pi_B_zero_of_bounded B (vecSub u v) hsub_abs hsub_pi
    exact vecSub_all_zero_imp_eq u v huv hzeros
  · intro heq
    rw [heq]

/--
Theorem 3.3 (Equation Preservation for `B ≥ 3L + 1`):
For equal-length vectors `u, v, w ∈ [-L, L]^d` and `B ≥ 3 * L + 1`:
  `pi_B B u + pi_B B v = pi_B B w ↔ vecAdd u v = w`.
-/
theorem pi_B_eq_preservation (B L : Int) (u v w : List Int)
    (huv : u.length = v.length) (hvw : v.length = w.length)
    (hu : inBox L u) (hv : inBox L v) (hw : inBox L w)
    (hB : 3 * L + 1 ≤ B) :
    pi_B B u + pi_B B v = pi_B B w ↔ vecAdd u v = w := by
  have huv_len : (vecAdd u v).length = w.length := by
    rw [vecAdd_length_eq u v huv, huv, hvw]
  constructor
  · intro hpi
    have hsub_pi : pi_B B (vecSub (vecAdd u v) w) = 0 := by
      rw [pi_B_sub B (vecAdd u v) w huv_len, pi_B_add B u v huv]
      omega
    have hadd_bnd := vecAdd_bounds (-L) L (-L) L u v huv hu hv
    have hsub_bnd := vecSub_bounds (-L + -L) (L + L) (-L) L (vecAdd u v) w huv_len hadd_bnd hw
    have hsub_abs : ∀ d ∈ vecSub (vecAdd u v) w, absInt d < B := by
      intro d hd
      have hdb := hsub_bnd d hd
      exact (absInt_lt_iff d B).mpr (by omega)
    have hzeros := pi_B_zero_of_bounded B (vecSub (vecAdd u v) w) hsub_abs hsub_pi
    exact vecSub_all_zero_imp_eq (vecAdd u v) w huv_len hzeros
  · intro heq
    rw [← pi_B_add B u v huv, heq]

/--
Theorem 3.4 (Freiman 2-Isomorphism for `B ≥ 4L + 1`):
For equal-length vectors `u, v, u', v' ∈ [-L, L]^d` and `B ≥ 4 * L + 1`:
  `pi_B B u + pi_B B v = pi_B B u' + pi_B B v' ↔ vecAdd u v = vecAdd u' v'`.
-/
theorem pi_B_freiman_2_iso (B L : Int) (u v u' v' : List Int)
    (huv : u.length = v.length) (huu' : u.length = u'.length) (hu'v' : u'.length = v'.length)
    (hu : inBox L u) (hv : inBox L v) (hu' : inBox L u') (hv' : inBox L v')
    (hB : 4 * L + 1 ≤ B) :
    pi_B B u + pi_B B v = pi_B B u' + pi_B B v' ↔ vecAdd u v = vecAdd u' v' := by
  have hlen : (vecAdd u v).length = (vecAdd u' v').length := by
    rw [vecAdd_length_eq u v huv, vecAdd_length_eq u' v' hu'v', huu']
  constructor
  · intro hpi
    have hsub_pi : pi_B B (vecSub (vecAdd u v) (vecAdd u' v')) = 0 := by
      rw [pi_B_sub B (vecAdd u v) (vecAdd u' v') hlen, pi_B_add B u v huv, pi_B_add B u' v' hu'v']
      omega
    have hadd1 := vecAdd_bounds (-L) L (-L) L u v huv hu hv
    have hadd2 := vecAdd_bounds (-L) L (-L) L u' v' hu'v' hu' hv'
    have hsub_bnd := vecSub_bounds (-L + -L) (L + L) (-L + -L) (L + L)
      (vecAdd u v) (vecAdd u' v') hlen hadd1 hadd2
    have hsub_abs : ∀ d ∈ vecSub (vecAdd u v) (vecAdd u' v'), absInt d < B := by
      intro d hd
      have hdb := hsub_bnd d hd
      exact (absInt_lt_iff d B).mpr (by omega)
    have hzeros := pi_B_zero_of_bounded B (vecSub (vecAdd u v) (vecAdd u' v')) hsub_abs hsub_pi
    exact vecSub_all_zero_imp_eq (vecAdd u v) (vecAdd u' v') hlen hzeros
  · intro heq
    rw [← pi_B_add B u v huv, ← pi_B_add B u' v' hu'v', heq]

/-- Sharpness of `B ≥ 2L + 1`: at `B = 2L` (`L ≥ 1`), injectivity fails. -/
theorem carry_inj_sharp_at_2L (L : Int) (hL : 1 ≤ L) :
    let B := 2 * L
    let u : List Int := [L, 0]
    let v : List Int := [-L, 1]
    inBox L u ∧ inBox L v ∧ u ≠ v ∧ pi_B B u = pi_B B v := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl <;> omega
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl <;> omega
  · simp
  · simp [pi_B]
    omega

/-- Sharpness of `B ≥ 3L + 1`: at `B = 3L` (`L ≥ 1`), equation preservation fails. -/
theorem carry_eq_sharp_at_3L (L : Int) (hL : 1 ≤ L) :
    let B := 3 * L
    let u : List Int := [L, 0]
    let v : List Int := [L, 0]
    let w : List Int := [-L, 1]
    inBox L u ∧ inBox L v ∧ inBox L w ∧
      pi_B B u + pi_B B v = pi_B B w ∧ vecAdd u v ≠ w := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl <;> omega
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl <;> omega
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl <;> omega
  · simp [pi_B]
    omega
  · simp [vecAdd]

/-- Sharpness of `B ≥ 4L + 1`: at `B = 4L` (`L ≥ 1`), Freiman 2-isomorphism fails. -/
theorem carry_freiman_sharp_at_4L (L : Int) (hL : 1 ≤ L) :
    let B := 4 * L
    let u  : List Int := [L, 0]
    let v  : List Int := [L, 0]
    let u' : List Int := [-L, 1]
    let v' : List Int := [-L, 0]
    inBox L u ∧ inBox L v ∧ inBox L u' ∧ inBox L v' ∧
      pi_B B u + pi_B B v = pi_B B u' + pi_B B v' ∧ vecAdd u v ≠ vecAdd u' v' := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl <;> omega
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl <;> omega
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl <;> omega
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | rfl <;> omega
  · simp [pi_B]
    omega
  · simp [vecAdd]

/-- Sum-avoidance predicate for `List Int`. -/
def IsSumAvoiding (A B : List Int) : Prop :=
  ∀ b1 ∈ B, ∀ b2 ∈ B, b1 ≠ b2 → (b1 + b2) ∉ A

/--
Theorem 3.5 (Carry-Free Sum-Avoidance Transport for `B ≥ 3L + 1`):
If `S ⊆ [-L, L]^d` has uniform vector length `d`, and `B ≥ 3 * L + 1`,
then a subset `C ⊆ S` is sum-avoiding in `ℤ^d` if and only if its projection
`C.map (pi_B B)` is sum-avoiding in `ℤ` with respect to `S.map (pi_B B)`.
-/
theorem sumAvoiding_transport_3L_add_1 (d : Nat) (L B : Int)
    (S C : List (List Int)) (hB : 3 * L + 1 ≤ B)
    (hS : ∀ x ∈ S, x.length = d ∧ inBox L x)
    (hCS : ∀ x ∈ C, x ∈ S) :
    IsSumAvoidingVec S C ↔ IsSumAvoiding (S.map (pi_B B)) (C.map (pi_B B)) := by
  constructor
  · intro hAvoid b1 hb1 b2 hb2 hne hsum
    rcases List.mem_map.mp hb1 with ⟨u, huC, rfl⟩
    rcases List.mem_map.mp hb2 with ⟨v, hvC, rfl⟩
    rcases List.mem_map.mp hsum with ⟨w, hwS, hw_eq⟩
    have huv_ne : u ≠ v := fun h => hne (by rw [h])
    rcases hS u (hCS u huC) with ⟨hul, hub⟩
    rcases hS v (hCS v hvC) with ⟨hvl, hvb⟩
    rcases hS w hwS with ⟨hwl, hwb⟩
    have hvec : vecAdd u v = w :=
      (pi_B_eq_preservation B L u v w (by omega) (by omega) hub hvb hwb hB).mp hw_eq.symm
    exact hAvoid u huC v hvC huv_ne (by rw [hvec]; exact hwS)
  · intro hAvoid u huC v hvC hne hsum
    rcases hS u (hCS u huC) with ⟨hul, hub⟩
    rcases hS v (hCS v hvC) with ⟨hvl, hvb⟩
    have hL_nn : 0 ≤ L := by
      cases u with
      | nil =>
        have h0 : d = 0 := by rw [← hul]; rfl
        have hv_len0 : v.length = 0 := by rw [hvl, h0]
        have hv_nil : v = [] := List.eq_nil_of_length_eq_zero hv_len0
        subst hv_nil
        exact absurd rfl hne
      | cons a _ =>
        have ha := hub a (by simp)
        omega
    have hB2 : 2 * L + 1 ≤ B := by omega
    have hpi_ne : pi_B B u ≠ pi_B B v := by
      intro heq
      exact hne ((pi_B_inj_of_ge_2L_add_1 B L u v (by omega) hub hvb hB2).mp heq)
    have hpi_sum : pi_B B u + pi_B B v ∈ S.map (pi_B B) := by
      rw [← pi_B_add B u v (by omega)]
      exact List.mem_map.mpr ⟨vecAdd u v, hsum, rfl⟩
    exact hAvoid (pi_B B u) (List.mem_map.mpr ⟨u, huC, rfl⟩)
      (pi_B B v) (List.mem_map.mpr ⟨v, hvC, rfl⟩) hpi_ne hpi_sum


/-! ==================================================================== -/
/-! ### Section 4: Cauchy-Schwarz, Turán / Caro-Wei, and Additive Energy -/
/-! ==================================================================== -/

/-- Sum of a list of natural numbers. -/
def sumNat : List Nat → Nat
  | [] => 0
  | x :: xs => x + sumNat xs

/-- Sum of a list of integers. -/
def sumInt : List Int → Int
  | [] => 0
  | x :: xs => x + sumInt xs

/-- Sum of squares of a list of integers. -/
def sumSqInt : List Int → Int
  | [] => 0
  | x :: xs => x * x + sumSqInt xs

theorem dot_replicate_one : ∀ (xs : List Int), dot xs (List.replicate xs.length 1) = sumInt xs
  | [] => by simp [dot, sumInt]
  | x :: xs => by
    simp only [List.length_cons, List.replicate_succ, dot, sumInt, Int.mul_one]
    rw [dot_replicate_one xs]

theorem normSq_replicate_one : ∀ (n : Nat), normSq (List.replicate n (1 : Int)) = (n : Int)
  | 0 => by simp [normSq, dot]
  | n + 1 => by
    simp only [List.replicate_succ]
    have hdef : normSq ((1 : Int) :: List.replicate n 1) =
        1 * 1 + normSq (List.replicate n (1 : Int)) := rfl
    rw [hdef, normSq_replicate_one n]
    omega

theorem normSq_eq_sumSqInt : ∀ (xs : List Int), normSq xs = sumSqInt xs
  | [] => rfl
  | x :: xs => by
    have hdef : normSq (x :: xs) = x * x + normSq xs := rfl
    rw [hdef, normSq_eq_sumSqInt xs]
    rfl

/--
Theorem 4.1 (Integer Cauchy-Schwarz Inequality for Lists):
For any list `xs : List Int`, `(∑ x_i)^2 ≤ xs.length * (∑ x_i^2)`.
-/
theorem cauchy_schwarz_sum (xs : List Int) :
    sumInt xs * sumInt xs ≤ (xs.length : Int) * sumSqInt xs := by
  have hlen : xs.length = (List.replicate xs.length (1 : Int)).length := by
    simp [List.length_replicate]
  have hcs := cauchy_schwarz_int xs (List.replicate xs.length (1 : Int)) hlen
  rw [dot_replicate_one xs, normSq_eq_sumSqInt xs, normSq_replicate_one xs.length] at hcs
  rw [Int.mul_comm (sumSqInt xs) (xs.length : Int)] at hcs
  exact hcs

theorem sumSqInt_map {α : Type} (f : α → Int) :
    ∀ (l : List α), sumSqInt (l.map f) = sumInt (l.map fun x => f x * f x)
  | [] => rfl
  | x :: xs => by
    simp only [List.map_cons, sumSqInt, sumInt, sumSqInt_map f xs]

/--
Theorem 4.2 (Mapped Integer Cauchy-Schwarz Inequality):
For any list `l : List α` of length `n` and function `f : α → Int`,
  `(∑_{i ∈ l} f(i))^2 ≤ n * ∑_{i ∈ l} f(i)^2`.
-/
theorem cauchy_schwarz_list {α : Type} (l : List α) (f : α → Int) :
    sumInt (l.map f) * sumInt (l.map f) ≤
      (l.length : Int) * sumInt (l.map fun x => f x * f x) := by
  have h := cauchy_schwarz_sum (l.map f)
  rw [List.length_map, sumSqInt_map f l] at h
  exact h

theorem sumInt_map_ofNat {α : Type} (f : α → Nat) :
    ∀ (l : List α), sumInt (l.map fun x => (f x : Int)) = (sumNat (l.map f) : Int)
  | [] => rfl
  | x :: xs => by
    simp only [List.map_cons, sumInt, sumNat, sumInt_map_ofNat f xs]
    rw [Int.natCast_add]

theorem cauchy_schwarz_nat_list {α : Type} (l : List α) (f : α → Nat) :
    sumNat (l.map f) * sumNat (l.map f) ≤ l.length * sumNat (l.map fun x => f x * f x) := by
  have h := cauchy_schwarz_list l (fun x => (f x : Int))
  rw [sumInt_map_ofNat f l] at h
  have hsq : sumInt (l.map fun x => (f x : Int) * (f x : Int)) =
      (sumNat (l.map fun x => f x * f x) : Int) := by
    clear h
    induction l with
    | nil => rfl
    | cons a as ih =>
      simp only [List.map_cons, sumInt, sumNat, Int.natCast_mul, Int.natCast_add, ih]
  rw [hsq] at h
  rw [← Int.natCast_mul, ← Int.natCast_mul] at h
  exact Int.ofNat_le.mp h


/-! Sum and Indicator Machinery for Finite Lists -/

/-- Boolean indicator `1` if `true`, `0` if `false`. -/
def ind (b : Bool) : Nat :=
  if b then 1 else 0

theorem ind_le (a b : Bool) (h : a = true → b = true) : ind a ≤ ind b := by
  cases a with
  | false => simp [ind]
  | true => simp [ind, h rfl]

theorem ind_and (a b : Bool) : ind (a && b) = ind a * ind b := by
  cases a <;> cases b <;> rfl

theorem length_filter_eq_sumNat {α : Type} (p : α → Bool) :
    ∀ (l : List α), (l.filter p).length = sumNat (l.map fun x => ind (p x))
  | [] => rfl
  | x :: xs => by
    simp only [List.filter_cons, List.map_cons, sumNat]
    cases hp : p x with
    | true => simp [ind, length_filter_eq_sumNat p xs]; omega
    | false => simp [ind, length_filter_eq_sumNat p xs]

theorem sumNat_map_add {α : Type} (f g : α → Nat) :
    ∀ (l : List α), sumNat (l.map fun x => f x + g x) = sumNat (l.map f) + sumNat (l.map g)
  | [] => rfl
  | x :: xs => by
    simp only [List.map_cons, sumNat, sumNat_map_add f g xs]
    omega

theorem sumNat_map_le {α : Type} (f g : α → Nat) :
    ∀ (l : List α), (∀ x ∈ l, f x ≤ g x) → sumNat (l.map f) ≤ sumNat (l.map g)
  | [], _ => Nat.le_refl 0
  | x :: xs, h => by
    have hx := h x (by simp)
    have ih := sumNat_map_le f g xs (fun y hy => h y (by simp [hy]))
    simp only [List.map_cons, sumNat]
    omega

theorem sumNat_map_congr {α : Type} (f g : α → Nat) :
    ∀ (l : List α), (∀ x ∈ l, f x = g x) → sumNat (l.map f) = sumNat (l.map g)
  | [], _ => rfl
  | x :: xs, h => by
    have hx := h x (by simp)
    have ih := sumNat_map_congr f g xs (fun y hy => h y (by simp [hy]))
    simp only [List.map_cons, sumNat, hx, ih]

theorem sumNat_map_const {α : Type} (c : Nat) :
    ∀ (l : List α), sumNat (l.map fun _ => c) = l.length * c
  | [] => by simp [sumNat]
  | _ :: xs => by
    simp only [List.map_cons, sumNat, List.length_cons, sumNat_map_const c xs, Nat.succ_mul]
    omega

theorem sumNat_map_mul_left {α : Type} (c : Nat) (f : α → Nat) :
    ∀ (l : List α), sumNat (l.map fun x => c * f x) = c * sumNat (l.map f)
  | [] => by simp [sumNat]
  | x :: xs => by
    simp only [List.map_cons, sumNat, sumNat_map_mul_left c f xs, Nat.mul_add]

theorem sumNat_map_mul_right {α : Type} (f : α → Nat) (c : Nat) :
    ∀ (l : List α), sumNat (l.map fun x => f x * c) = sumNat (l.map f) * c
  | [] => by simp [sumNat]
  | x :: xs => by
    simp only [List.map_cons, sumNat, sumNat_map_mul_right f c xs, Nat.add_mul]

theorem sumNat_mul_sumNat {α β : Type} (xs : List α) (ys : List β)
    (f : α → Nat) (g : β → Nat) :
    sumNat (xs.map f) * sumNat (ys.map g) =
      sumNat (xs.map fun x => sumNat (ys.map fun y => f x * g y)) := by
  induction xs with
  | nil => simp [sumNat]
  | cons x xs ih =>
    simp only [List.map_cons, sumNat, Nat.add_mul, ih]
    rw [sumNat_map_mul_left (f x) g ys]

theorem sumNat_swap {α β : Type} (ys : List β) (f : α → β → Nat) :
    ∀ (xs : List α),
      sumNat (xs.map fun x => sumNat (ys.map fun y => f x y)) =
      sumNat (ys.map fun y => sumNat (xs.map fun x => f x y))
  | [] => by simp [sumNat, sumNat_map_const]
  | x :: xs => by
    simp only [List.map_cons, sumNat]
    rw [sumNat_swap ys f xs]
    rw [← sumNat_map_add (fun y => f x y) (fun y => sumNat (xs.map fun x' => f x' y)) ys]

theorem sumNat_filter_partition {α : Type} (p : α → Bool) (f : α → Nat) :
    ∀ (l : List α),
      sumNat (l.map f) =
        sumNat ((l.filter p).map f) + sumNat ((l.filter fun x => !p x).map f)
  | [] => by simp [sumNat]
  | x :: xs => by
    have ih := sumNat_filter_partition p f xs
    by_cases hp : p x = true
    · simp [List.map_cons, hp, sumNat]
      omega
    · have hpf : p x = false := Bool.eq_false_iff.mpr hp
      simp [List.map_cons, hpf, sumNat]
      omega

private theorem sumNat_nodup_contains_eq (s1 s2 : Int) :
    ∀ (W : List Int), W.Nodup →
      sumNat (W.map fun w => ind (decide (s1 = w) && decide (s2 = w))) =
        ind (decide (s1 = s2) && W.contains s1)
  | [], _ => by simp [sumNat, ind]
  | w :: ws, hnd => by
    rcases List.nodup_cons.mp hnd with ⟨hw_not, hws_nd⟩
    have ih := sumNat_nodup_contains_eq s1 s2 ws hws_nd
    simp only [List.map_cons, sumNat, List.contains_cons]
    by_cases h1 : s1 = w
    · subst h1
      have hrest : sumNat (ws.map fun w' => ind (decide (s1 = w') && decide (s2 = w'))) = 0 := by
        have hzero : sumNat (ws.map fun _ => (0 : Nat)) = 0 := by
          rw [sumNat_map_const]; omega
        rw [← hzero]
        apply sumNat_map_congr
        intro w' hw'
        have hne : s1 ≠ w' := fun h => hw_not (h ▸ hw')
        simp [ind, hne]
      rw [hrest]
      by_cases h2 : s2 = s1
      · subst h2; simp [ind]
      · have h2' : s1 ≠ s2 := fun h => h2 h.symm
        simp [ind, h2, h2']
    · have heq_b : (s1 == w) = false := beq_false_of_ne h1
      simp only [decide_eq_false h1, Bool.false_and, ind] at *
      rw [ih, heq_b, Bool.false_or]
      simp

private theorem sumNat_nodup_contains_single (s : Int) (W : List Int) (hW : W.Nodup) :
    sumNat (W.map fun w => ind (decide (s = w))) = ind (W.contains s) := by
  have h := sumNat_nodup_contains_eq s s W hW
  have hcongr : sumNat (W.map fun w => ind (decide (s = w))) =
      sumNat (W.map fun w => ind (decide (s = w) && decide (s = w))) := by
    apply sumNat_map_congr
    intro w _
    simp
  rw [hcongr, h]
  simp


/-! Representation Counts, Additive Energy, and Conflict Edges -/

/-- Number of ordered pairs `(x, y) ∈ A × A` with `x + y = w`. -/
def repSumNat (A : List Int) (w : Int) : Nat :=
  sumNat (A.map fun x => (A.filter fun y => decide (x + y = w)).length)

def repSum (A : List Int) (w : Int) : Int :=
  (repSumNat A w : Int)

/-- Number of ordered distinct pairs `(x, y) ∈ A × A` with `x ≠ y` and `x + y = w`. -/
def repSumDistinctNat (A : List Int) (w : Int) : Nat :=
  sumNat (A.map fun x => (A.filter fun y => decide (x ≠ y ∧ x + y = w)).length)

def repSumDistinct (A : List Int) (w : Int) : Int :=
  (repSumDistinctNat A w : Int)

/-- Additive energy `E(A, A) = #{(x1, x2, x3, x4) ∈ A^4 : x1 + x2 = x3 + x4}`. -/
def energyNat (A : List Int) : Nat :=
  sumNat (A.map fun x1 =>
    sumNat (A.map fun x2 =>
      sumNat (A.map fun x3 =>
        (A.filter fun x4 => decide (x1 + x2 = x3 + x4)).length)))

def energy (A : List Int) : Int :=
  (energyNat A : Int)

/-- Number of undirected conflict edges `{u, v}` (`u < v`, `u + v ∈ A`). -/
def numConflictEdges (A : List Int) : Nat :=
  sumNat (A.map fun u => (A.filter fun v => decide (u < v) && A.contains (u + v)).length)

/-- Number of ordered distinct conflict pairs `(u, v) ∈ A × A` (`u ≠ v`, `u + v ∈ A`). -/
def twoNumConflictEdges (A : List Int) : Nat :=
  sumNat (A.map fun u => (A.filter fun v => decide (u ≠ v) && A.contains (u + v)).length)

private theorem repSumNat_eq_ind (A : List Int) (w : Int) :
    repSumNat A w =
      sumNat (A.map fun x => sumNat (A.map fun y => ind (decide (x + y = w)))) := by
  unfold repSumNat
  apply sumNat_map_congr
  intro x _
  exact length_filter_eq_sumNat (fun y => decide (x + y = w)) A

private theorem repSumDistinctNat_eq_ind (A : List Int) (w : Int) :
    repSumDistinctNat A w =
      sumNat (A.map fun x => sumNat (A.map fun y => ind (decide (x ≠ y) && decide (x + y = w)))) := by
  unfold repSumDistinctNat
  apply sumNat_map_congr
  intro x _
  rw [length_filter_eq_sumNat]
  apply sumNat_map_congr
  intro y _
  simp [Bool.decide_and]

theorem repSumDistinctNat_le_repSumNat (A : List Int) (w : Int) :
    repSumDistinctNat A w ≤ repSumNat A w := by
  rw [repSumDistinctNat_eq_ind, repSumNat_eq_ind]
  apply sumNat_map_le
  intro x _
  apply sumNat_map_le
  intro y _
  apply ind_le
  intro h
  simp only [Bool.and_eq_true] at h
  exact h.2

/-- For any duplicate-free list `W`, `∑_{w ∈ W} repSum(A, w)^2 ≤ E(A, A)`. -/
theorem sum_repSum_sq_le_energy (A W : List Int) (hW : W.Nodup) :
    sumNat (W.map fun w => repSumNat A w * repSumNat A w) ≤ energyNat A := by
  have h1 : sumNat (W.map fun w => repSumNat A w * repSumNat A w) =
      sumNat (W.map fun w =>
        sumNat (A.map fun x1 => sumNat (A.map fun x2 =>
          sumNat (A.map fun x3 => sumNat (A.map fun x4 =>
            ind (decide (x1 + x2 = w) && decide (x3 + x4 = w))))))) := by
    apply sumNat_map_congr
    intro w _
    rw [repSumNat_eq_ind]
    have hprod1 : (sumNat (A.map fun x1 => sumNat (A.map fun x2 => ind (decide (x1 + x2 = w))))) *
        (sumNat (A.map fun x3 => sumNat (A.map fun x4 => ind (decide (x3 + x4 = w))))) =
        sumNat (A.map fun x1 =>
          sumNat (A.map fun x2 =>
            sumNat (A.map fun x3 =>
              sumNat (A.map fun x4 => ind (decide (x1 + x2 = w) && decide (x3 + x4 = w)))))) := by
      rw [sumNat_mul_sumNat]
      apply sumNat_map_congr
      intro x1 _
      have hinner : sumNat (A.map fun x3 =>
          sumNat (A.map fun x2 => ind (decide (x1 + x2 = w))) *
          sumNat (A.map fun x4 => ind (decide (x3 + x4 = w)))) =
          sumNat (A.map fun x3 => sumNat (A.map fun x2 =>
            sumNat (A.map fun x4 => ind (decide (x1 + x2 = w) && decide (x3 + x4 = w))))) := by
        apply sumNat_map_congr
        intro x3 _
        rw [sumNat_mul_sumNat]
        apply sumNat_map_congr
        intro x2 _
        apply sumNat_map_congr
        intro x4 _
        rw [ind_and]
      rw [hinner, sumNat_swap A _ A]
    exact hprod1
  rw [h1]
  rw [sumNat_swap A _ W]
  have hswap1 : sumNat (A.map fun x1 =>
      sumNat (W.map fun w => sumNat (A.map fun x2 =>
        sumNat (A.map fun x3 => sumNat (A.map fun x4 =>
          ind (decide (x1 + x2 = w) && decide (x3 + x4 = w))))))) =
      sumNat (A.map fun x1 => sumNat (A.map fun x2 =>
        sumNat (A.map fun x3 => sumNat (A.map fun x4 =>
          sumNat (W.map fun w => ind (decide (x1 + x2 = w) && decide (x3 + x4 = w))))))) := by
    apply sumNat_map_congr
    intro x1 _
    rw [sumNat_swap A _ W]
    apply sumNat_map_congr
    intro x2 _
    rw [sumNat_swap A _ W]
    apply sumNat_map_congr
    intro x3 _
    rw [sumNat_swap A _ W]
  rw [hswap1]
  unfold energyNat
  apply sumNat_map_le; intro x1 _
  apply sumNat_map_le; intro x2 _
  apply sumNat_map_le; intro x3 _
  rw [length_filter_eq_sumNat]
  apply sumNat_map_le; intro x4 _
  rw [sumNat_nodup_contains_eq (x1 + x2) (x3 + x4) W hW]
  apply ind_le
  intro h
  simp only [Bool.and_eq_true] at h
  exact h.1

/--
Theorem 4.3 (Cauchy-Schwarz Additive Energy Rigidity Inequality):
For any duplicate-free finite set `A : List Int` of length `n`:
  `n * energy A ≥ (∑_{w ∈ A} repSum A w)^2`.
-/
theorem energy_ineq_all (A : List Int) (hA : A.Nodup) :
    sumInt (A.map (repSum A)) * sumInt (A.map (repSum A)) ≤ (A.length : Int) * energy A := by
  have hnat : sumNat (A.map (repSumNat A)) * sumNat (A.map (repSumNat A)) ≤
      A.length * energyNat A := by
    have hcs := cauchy_schwarz_nat_list A (repSumNat A)
    have hle := sum_repSum_sq_le_energy A A hA
    exact Nat.le_trans hcs (Nat.mul_le_mul_left A.length hle)
  have hcast := Int.ofNat_le.mpr hnat
  have hsum : (sumNat (A.map (repSumNat A)) : Int) = sumInt (A.map (repSum A)) := by
    rw [← sumInt_map_ofNat (repSumNat A) A]
    rfl
  rw [Int.natCast_mul, Int.natCast_mul, hsum] at hcast
  exact hcast

/--
Theorem 4.4 (Cauchy-Schwarz Energy Rigidity for Distinct Pairs):
For any duplicate-free finite set `A : List Int` of length `n`:
  `n * energy A ≥ (∑_{w ∈ A} repSumDistinct A w)^2`.
-/
theorem energy_ineq_distinct (A : List Int) (hA : A.Nodup) :
    sumInt (A.map (repSumDistinct A)) * sumInt (A.map (repSumDistinct A)) ≤
      (A.length : Int) * energy A := by
  have hnat : sumNat (A.map (repSumDistinctNat A)) * sumNat (A.map (repSumDistinctNat A)) ≤
      A.length * energyNat A := by
    have hcs := cauchy_schwarz_nat_list A (repSumDistinctNat A)
    have hle_sq : sumNat (A.map fun w => repSumDistinctNat A w * repSumDistinctNat A w) ≤
        sumNat (A.map fun w => repSumNat A w * repSumNat A w) := by
      apply sumNat_map_le
      intro w _
      have hw := repSumDistinctNat_le_repSumNat A w
      exact Nat.mul_le_mul hw hw
    have hle := Nat.le_trans hle_sq (sum_repSum_sq_le_energy A A hA)
    exact Nat.le_trans hcs (Nat.mul_le_mul_left A.length hle)
  have hcast := Int.ofNat_le.mpr hnat
  have hsum : (sumNat (A.map (repSumDistinctNat A)) : Int) = sumInt (A.map (repSumDistinct A)) := by
    rw [← sumInt_map_ofNat (repSumDistinctNat A) A]
    rfl
  rw [Int.natCast_mul, Int.natCast_mul, hsum] at hcast
  exact hcast

theorem twoNumConflictEdges_eq_two_mul (A : List Int) :
    twoNumConflictEdges A = 2 * numConflictEdges A := by
  have h1 : twoNumConflictEdges A =
      sumNat (A.map fun u => sumNat (A.map fun v =>
        ind (decide (u < v) && A.contains (u + v)) +
        ind (decide (v < u) && A.contains (u + v)))) := by
    unfold twoNumConflictEdges
    apply sumNat_map_congr
    intro u _
    rw [length_filter_eq_sumNat]
    apply sumNat_map_congr
    intro v _
    by_cases hc : u + v ∈ A
    · by_cases hlt : u < v
      · have hne : u ≠ v := by omega
        have hgt : ¬(v < u) := by omega
        simp [ind, hc, hlt, hne, hgt]
      · by_cases hgt : v < u
        · have hne : u ≠ v := by omega
          simp [ind, hc, hlt, hne, hgt]
        · have heq : u = v := by omega
          simp [ind, heq]
    · simp [ind, hc]
  rw [h1]
  have hsplit : sumNat (A.map fun u => sumNat (A.map fun v =>
      ind (decide (u < v) && A.contains (u + v)) +
      ind (decide (v < u) && A.contains (u + v)))) =
      sumNat (A.map fun u => sumNat (A.map fun v =>
        ind (decide (u < v) && A.contains (u + v)))) +
      sumNat (A.map fun u => sumNat (A.map fun v =>
        ind (decide (v < u) && A.contains (u + v)))) := by
    rw [← sumNat_map_add]
    apply sumNat_map_congr
    intro u _
    exact sumNat_map_add _ _ A
  rw [hsplit]
  have hleft : sumNat (A.map fun u => sumNat (A.map fun v =>
      ind (decide (u < v) && A.contains (u + v)))) = numConflictEdges A := by
    unfold numConflictEdges
    apply sumNat_map_congr
    intro u _
    exact (length_filter_eq_sumNat _ A).symm
  have hright : sumNat (A.map fun u => sumNat (A.map fun v =>
      ind (decide (v < u) && A.contains (u + v)))) = numConflictEdges A := by
    rw [sumNat_swap A _ A]
    unfold numConflictEdges
    apply sumNat_map_congr
    intro v _
    rw [length_filter_eq_sumNat]
    apply sumNat_map_congr
    intro u _
    rw [Int.add_comm u v]
  rw [hleft, hright]
  omega

/--
Theorem 4.5 (Degree-Sum / Representation Identity for Distinct Conflict Pairs):
For any duplicate-free `A : List Int`,
  `∑_{w ∈ A} repSumDistinct A w = 2 * numConflictEdges A`.
-/
theorem sum_repSumDistinct_eq_two_mul_edges (A : List Int) (hA : A.Nodup) :
    sumNat (A.map (repSumDistinctNat A)) = 2 * numConflictEdges A := by
  have h1 : sumNat (A.map (repSumDistinctNat A)) =
      sumNat (A.map fun w => sumNat (A.map fun u =>
        sumNat (A.map fun v => ind (decide (u ≠ v) && decide (u + v = w))))) := by
    apply sumNat_map_congr
    intro w _
    exact repSumDistinctNat_eq_ind A w
  rw [h1, sumNat_swap A _ A]
  have hswap : sumNat (A.map fun u => sumNat (A.map fun w =>
      sumNat (A.map fun v => ind (decide (u ≠ v) && decide (u + v = w))))) =
      sumNat (A.map fun u => sumNat (A.map fun v =>
        sumNat (A.map fun w => ind (decide (u ≠ v) && decide (u + v = w))))) := by
    apply sumNat_map_congr
    intro u _
    exact sumNat_swap A _ A
  rw [hswap]
  have heval : sumNat (A.map fun u => sumNat (A.map fun v =>
      sumNat (A.map fun w => ind (decide (u ≠ v) && decide (u + v = w))))) =
      twoNumConflictEdges A := by
    unfold twoNumConflictEdges
    apply sumNat_map_congr
    intro u _
    rw [length_filter_eq_sumNat]
    apply sumNat_map_congr
    intro v _
    by_cases huv : u = v
    · simp only [decide_eq_false (by omega : ¬(u ≠ v)), Bool.false_and, ind]
      have hzero : sumNat (A.map fun _ => (0 : Nat)) = 0 := by
        rw [sumNat_map_const]; omega
      exact hzero
    · have heq : sumNat (A.map fun w => ind (decide (u ≠ v) && decide (u + v = w))) =
          sumNat (A.map fun w => ind (decide (u + v = w))) := by
        apply sumNat_map_congr
        intro w _
        simp [huv]
      rw [heq, sumNat_nodup_contains_single (u + v) A hA]
      simp [huv]
  rw [heval, twoNumConflictEdges_eq_two_mul]

/-- Int-valued form of `sum_repSumDistinct_eq_two_mul_edges`. -/
theorem sum_repSumDistinct_int_eq_two_mul_edges (A : List Int) (hA : A.Nodup) :
    sumInt (A.map (repSumDistinct A)) = 2 * (numConflictEdges A : Int) := by
  have hnat := sum_repSumDistinct_eq_two_mul_edges A hA
  have hsum : sumInt (A.map (repSumDistinct A)) = (sumNat (A.map (repSumDistinctNat A)) : Int) := by
    rw [← sumInt_map_ofNat (repSumDistinctNat A) A]
    rfl
  rw [hsum, hnat, Int.natCast_mul]
  rfl

/--
Theorem 4.6 (Exact Identity When `A` Contains No Doubles `x + x`):
If `A.Nodup` and `∀ x ∈ A, (x + x) ∉ A`, then
  `∑_{w ∈ A} repSum A w = 2 * numConflictEdges A`.
-/
theorem sum_repSum_eq_two_mul_edges_of_no_double (A : List Int) (hA : A.Nodup)
    (hNoDouble : ∀ x ∈ A, x + x ∉ A) :
    sumInt (A.map (repSum A)) = 2 * (numConflictEdges A : Int) := by
  have hcongr : sumNat (A.map (repSumNat A)) = sumNat (A.map (repSumDistinctNat A)) := by
    apply sumNat_map_congr
    intro w hw
    rw [repSumNat_eq_ind, repSumDistinctNat_eq_ind]
    apply sumNat_map_congr
    intro x hx
    apply sumNat_map_congr
    intro y _
    by_cases hxy : x = y
    · subst hxy
      have hne : x + x ≠ w := fun heq => hNoDouble x hx (by rw [heq]; exact hw)
      simp [hne]
    · simp [hxy]
  have hsum : sumInt (A.map (repSum A)) = (sumNat (A.map (repSumNat A)) : Int) := by
    rw [← sumInt_map_ofNat (repSumNat A) A]
    rfl
  rw [hsum, hcongr, sum_repSumDistinct_eq_two_mul_edges A hA, Int.natCast_mul]
  rfl

/-- General lower bound without `hNoDouble`: `∑_{w ∈ A} repSum A w ≥ 2 * numConflictEdges A`. -/
theorem sum_repSum_ge_two_mul_edges (A : List Int) (hA : A.Nodup) :
    2 * (numConflictEdges A : Int) ≤ sumInt (A.map (repSum A)) := by
  have hle : sumNat (A.map (repSumDistinctNat A)) ≤ sumNat (A.map (repSumNat A)) :=
    sumNat_map_le (repSumDistinctNat A) (repSumNat A) A (fun w _ => repSumDistinctNat_le_repSumNat A w)
  rw [sum_repSumDistinct_eq_two_mul_edges A hA] at hle
  have hcast := Int.ofNat_le.mpr hle
  have hsum : (sumNat (A.map (repSumNat A)) : Int) = sumInt (A.map (repSum A)) := by
    rw [← sumInt_map_ofNat (repSumNat A) A]
    rfl
  rw [hsum, Int.natCast_mul] at hcast
  exact hcast

/--
Theorem 4.7 (Energy Lower Bound in Terms of Conflict Edges):
For any duplicate-free `A : List Int` of length `n`:
  `n * energy A ≥ 4 * (numConflictEdges A)^2`.
-/
theorem energy_ge_four_edges_sq (A : List Int) (hA : A.Nodup) :
    4 * (numConflictEdges A : Int) * (numConflictEdges A : Int) ≤ (A.length : Int) * energy A := by
  have hineq := energy_ineq_distinct A hA
  rw [sum_repSumDistinct_int_eq_two_mul_edges A hA] at hineq
  have h4 : (2 * (numConflictEdges A : Int)) * (2 * (numConflictEdges A : Int)) =
      4 * (numConflictEdges A : Int) * (numConflictEdges A : Int) := by
    calc (2 * (numConflictEdges A : Int)) * (2 * (numConflictEdges A : Int))
        = 2 * ((numConflictEdges A : Int) * (2 * (numConflictEdges A : Int))) := by
            rw [Int.mul_assoc]
      _ = 2 * ((2 * (numConflictEdges A : Int)) * (numConflictEdges A : Int)) := by
            rw [Int.mul_comm (numConflictEdges A : Int) (2 * (numConflictEdges A : Int))]
      _ = 2 * (2 * ((numConflictEdges A : Int) * (numConflictEdges A : Int))) := by
            rw [Int.mul_assoc 2 (numConflictEdges A : Int) (numConflictEdges A : Int)]
      _ = (2 * 2) * ((numConflictEdges A : Int) * (numConflictEdges A : Int)) := by
            rw [← Int.mul_assoc 2 2 _]
      _ = 4 * (numConflictEdges A : Int) * (numConflictEdges A : Int) := by
            rw [Int.mul_assoc 4 _ _]
            rfl
  rw [← h4]
  exact hineq


/-! Turán / Caro-Wei Conflict Graph Bound & Combined Energy Rigidity -/

/-- Degree of vertex `x` in subgraph `V` under boolean adjacency `adj`. -/
def deg (adj : Int → Int → Bool) (V : List Int) (x : Int) : Nat :=
  (V.filter (adj x)).length

/-- Twice the number of edges in subgraph `V` (`∑_{x ∈ V} deg_V(x)`). -/
def twoE (adj : Int → Int → Bool) (V : List Int) : Nat :=
  sumNat (V.map (deg adj V))

private theorem exists_min_by (f : Int → Nat) :
    ∀ (V : List Int), V ≠ [] → ∃ v ∈ V, ∀ u ∈ V, f v ≤ f u
  | [], h => absurd rfl h
  | [x], _ => ⟨x, by simp, fun u hu => by simp_all⟩
  | x :: y :: ys, _ => by
    rcases exists_min_by f (y :: ys) (by simp) with ⟨v, hv_mem, hv_min⟩
    by_cases hxy : f x ≤ f v
    · refine ⟨x, by simp, fun u hu => ?_⟩
      rcases List.mem_cons.mp hu with rfl | hu_tail
      · exact Nat.le_refl _
      · exact Nat.le_trans hxy (hv_min u hu_tail)
    · refine ⟨v, by simp [hv_mem], fun u hu => ?_⟩
      rcases List.mem_cons.mp hu with rfl | hu_tail
      · omega
      · exact hv_min u hu_tail

private theorem filter_or_disjoint_length (p q : Int → Bool)
    (hpq : ∀ x, !(p x && q x) = true) :
    ∀ (l : List Int), (l.filter fun x => p x || q x).length =
      (l.filter p).length + (l.filter q).length
  | [] => rfl
  | x :: xs => by
    have ih := filter_or_disjoint_length p q hpq xs
    have hdisj := hpq x
    cases hpx : p x <;> cases hqx : q x <;> simp_all <;> omega

private theorem filter_eq_length_of_mem_nodup (v : Int) :
    ∀ (V : List Int), V.Nodup → v ∈ V → (V.filter fun u => decide (u = v)).length = 1
  | [], _, hv => by simp at hv
  | x :: xs, hnd, hv => by
    rcases List.nodup_cons.mp hnd with ⟨hx_not, hxs_nd⟩
    simp only [List.mem_cons] at hv
    simp only [List.filter_cons]
    rcases hv with rfl | hv_xs
    · have hrest : (xs.filter fun u => decide (u = v)).length = 0 := by
        rw [length_filter_eq_sumNat]
        have hzero : sumNat (xs.map fun _ => (0 : Nat)) = 0 := by
          rw [sumNat_map_const]; omega
        rw [← hzero]
        apply sumNat_map_congr
        intro u hu
        have hne : u ≠ v := fun h => hx_not (h ▸ hu)
        simp [ind, hne]
      simp [hrest]
    · have hne : x ≠ v := fun h => hx_not (h ▸ hv_xs)
      simp [hne, filter_eq_length_of_mem_nodup v xs hxs_nd hv_xs]

private theorem turan_alg_step (K k' n m X : Nat) (hK : K = k' + 1) (hk' : 1 ≤ k')
    (hm : m ≤ n) (hIH : (n - m) * (n - m) ≤ k' * X) :
    n * n ≤ K * (m * m + X) := by
  have hk'_pos : (0 : Int) < (k' : Int) := by omega
  have hIH_int : ((n : Int) - (m : Int)) * ((n : Int) - (m : Int)) ≤ (k' : Int) * (X : Int) := by
    have h := Int.ofNat_le.mpr hIH
    have hsub : ((n - m : Nat) : Int) = (n : Int) - (m : Int) := by omega
    rw [Int.natCast_mul, Int.natCast_mul, hsub] at h
    exact h
  have hK_int : (K : Int) = (k' : Int) + 1 := by omega
  have hnonneg : 0 ≤ ((n : Int) - (K : Int) * (m : Int)) * ((n : Int) - (K : Int) * (m : Int)) :=
    int_sq_nonneg _
  have h1 : (k' : Int) * ((K : Int) * ((m : Int) * (m : Int) + (X : Int))) =
      (K : Int) * ((k' : Int) * (X : Int)) + (K : Int) * (k' : Int) * ((m : Int) * (m : Int)) := by
    rw [Int.mul_add, Int.mul_add]
    have ha : (k' : Int) * ((K : Int) * ((m : Int) * (m : Int))) =
        (K : Int) * (k' : Int) * ((m : Int) * (m : Int)) := by
      rw [← Int.mul_assoc, Int.mul_comm (k' : Int) (K : Int)]
    have hb : (k' : Int) * ((K : Int) * (X : Int)) = (K : Int) * ((k' : Int) * (X : Int)) := by
      rw [← Int.mul_assoc, Int.mul_comm (k' : Int) (K : Int), Int.mul_assoc]
    omega
  have h2 : (K : Int) * (((n : Int) - (m : Int)) * ((n : Int) - (m : Int))) ≤
      (K : Int) * ((k' : Int) * (X : Int)) :=
    Int.mul_le_mul_of_nonneg_left hIH_int (by omega)
  have h3 : (k' : Int) * ((n : Int) * (n : Int)) ≤
      (K : Int) * (((n : Int) - (m : Int)) * ((n : Int) - (m : Int))) +
      (K : Int) * (k' : Int) * ((m : Int) * (m : Int)) := by
    have hsub_sq : ((n : Int) - (m : Int)) * ((n : Int) - (m : Int)) =
        (n : Int) * (n : Int) + (m : Int) * (m : Int) - 2 * ((n : Int) * (m : Int)) := by
      rw [Int.sub_eq_add_neg, Int.mul_add, Int.add_mul, Int.add_mul]
      simp only [Int.mul_neg, Int.neg_mul, Int.neg_neg]
      rw [Int.mul_comm (m : Int) (n : Int)]
      omega
    have hKm_sq : ((n : Int) - (K : Int) * (m : Int)) * ((n : Int) - (K : Int) * (m : Int)) =
        (n : Int) * (n : Int) + (K : Int) * (K : Int) * ((m : Int) * (m : Int)) -
        2 * (K : Int) * ((n : Int) * (m : Int)) := by
      rw [Int.sub_eq_add_neg, Int.mul_add, Int.add_mul, Int.add_mul]
      simp only [Int.mul_neg, Int.neg_mul, Int.neg_neg]
      have hkm1 : (n : Int) * ((K : Int) * (m : Int)) = (K : Int) * ((n : Int) * (m : Int)) := by
        rw [← Int.mul_assoc, Int.mul_comm (n : Int) (K : Int), Int.mul_assoc]
      have hkm2 : (K : Int) * (m : Int) * (n : Int) = (K : Int) * ((n : Int) * (m : Int)) := by
        rw [Int.mul_assoc, Int.mul_comm (m : Int) (n : Int)]
      have hkm3 : (K : Int) * (m : Int) * ((K : Int) * (m : Int)) =
          (K : Int) * (K : Int) * ((m : Int) * (m : Int)) := by
        calc (K : Int) * (m : Int) * ((K : Int) * (m : Int))
            = (K : Int) * ((m : Int) * ((K : Int) * (m : Int))) := by rw [Int.mul_assoc]
          _ = (K : Int) * (((K : Int) * (m : Int)) * (m : Int)) := by
                rw [Int.mul_comm (m : Int) ((K : Int) * (m : Int))]
          _ = (K : Int) * ((K : Int) * ((m : Int) * (m : Int))) := by rw [Int.mul_assoc]
          _ = (K : Int) * (K : Int) * ((m : Int) * (m : Int)) := by rw [← Int.mul_assoc]
      have h2km : 2 * (K : Int) * ((n : Int) * (m : Int)) = 2 * ((K : Int) * ((n : Int) * (m : Int))) :=
        Int.mul_assoc 2 (K : Int) ((n : Int) * (m : Int))
      rw [hkm1, hkm2, hkm3, h2km]
      omega
    have hdiff : (K : Int) * ((n : Int) * (n : Int) + (m : Int) * (m : Int) - 2 * ((n : Int) * (m : Int))) +
        (K : Int) * (k' : Int) * ((m : Int) * (m : Int)) - (k' : Int) * ((n : Int) * (n : Int)) =
        ((n : Int) - (K : Int) * (m : Int)) * ((n : Int) - (K : Int) * (m : Int)) := by
      rw [hKm_sq]
      have hexp1 : (K : Int) * ((n : Int) * (n : Int) + (m : Int) * (m : Int) - 2 * ((n : Int) * (m : Int))) =
          (K : Int) * ((n : Int) * (n : Int)) + (K : Int) * ((m : Int) * (m : Int)) -
          2 * (K : Int) * ((n : Int) * (m : Int)) := by
        rw [Int.sub_eq_add_neg, Int.mul_add, Int.mul_add, Int.mul_neg]
        have h2k : (K : Int) * (2 * ((n : Int) * (m : Int))) = 2 * (K : Int) * ((n : Int) * (m : Int)) := by
          rw [← Int.mul_assoc, Int.mul_comm (K : Int) 2, Int.mul_assoc 2 (K : Int) _]
        rw [h2k, ← Int.sub_eq_add_neg]
      have hexp2 : (K : Int) * ((n : Int) * (n : Int)) - (k' : Int) * ((n : Int) * (n : Int)) =
          (n : Int) * (n : Int) := by
        rw [hK_int, Int.add_mul, Int.one_mul]
        omega
      have hexp3 : (K : Int) * ((m : Int) * (m : Int)) + (K : Int) * (k' : Int) * ((m : Int) * (m : Int)) =
          (K : Int) * (K : Int) * ((m : Int) * (m : Int)) := by
        have hk_sum : (K : Int) * ((m : Int) * (m : Int)) + (K : Int) * (k' : Int) * ((m : Int) * (m : Int)) =
            (K : Int) * (1 + (k' : Int)) * ((m : Int) * (m : Int)) := by
          rw [Int.mul_add, Int.mul_one, Int.add_mul]
        rw [hk_sum]
        have hK1 : 1 + (k' : Int) = (K : Int) := by omega
        rw [hK1]
      omega
    rw [hsub_sq]
    omega
  have hcomb : (k' : Int) * ((n : Int) * (n : Int)) ≤
      (k' : Int) * ((K : Int) * ((m : Int) * (m : Int) + (X : Int))) := by
    omega
  have hcancel := Int.le_of_mul_le_mul_left hcomb hk'_pos
  rw [← Int.natCast_mul, ← Int.natCast_mul, ← Int.natCast_add, ← Int.natCast_mul] at hcancel
  exact Int.ofNat_le.mp hcancel

private theorem turan_graph_bound_aux (adj : Int → Int → Bool)
    (hirr : ∀ x, adj x x = false) (hsymm : ∀ x y, adj x y = adj y x) :
    ∀ (N : Nat) (V : List Int), V.length ≤ N → V.Nodup →
      ∀ (K : Nat),
        (∀ I : List Int, I.Nodup → (∀ x ∈ I, x ∈ V) →
          (∀ x ∈ I, ∀ y ∈ I, adj x y = false) → I.length ≤ K) →
        V.length * V.length ≤ K * (twoE adj V + V.length)
  | 0, V, hlen, _, K, _ => by
    have hV0 : V.length = 0 := by omega
    rw [hV0]
    simp
  | N + 1, [], _, _, K, _ => by
    simp
  | N + 1, a :: as, hlen, hnd, K, halpha => by
    let V := a :: as
    have hK_ge1 : 1 ≤ K := by
      have h1 := halpha [a] (by simp) (fun x hx => by simp at hx; subst hx; simp)
        (fun x hx y hy => by simp at hx hy; subst hx; subst hy; exact hirr _)
      simpa using h1
    rcases exists_min_by (deg adj V) V (by simp) with ⟨v, hv_mem, hv_min⟩
    let p : Int → Bool := fun u => decide (u = v) || adj v u
    let S := V.filter p
    let V' := V.filter (fun u => !p u)
    have hpart_len : S.length + V'.length = V.length := by
      have h1 : V.length = sumNat (V.map fun _ => (1 : Nat)) := by
        rw [sumNat_map_const]; omega
      have h2 := sumNat_filter_partition p (fun _ => (1 : Nat)) V
      have hs1 : sumNat (S.map fun _ => (1 : Nat)) = S.length := by
        rw [sumNat_map_const, Nat.mul_one]
      have hv1 : sumNat (V'.map fun _ => (1 : Nat)) = V'.length := by
        rw [sumNat_map_const, Nat.mul_one]
      rw [← h1, hs1, hv1] at h2
      exact h2.symm
    have hS_len : S.length = deg adj V v + 1 := by
      have hdisj : ∀ x, !(decide (x = v) && adj v x) = true := by
        intro x
        by_cases hxv : x = v
        · subst hxv; simp [hirr x]
        · simp [hxv]
      have hfor := filter_or_disjoint_length (fun u => decide (u = v)) (adj v) hdisj V
      have hfeq := filter_eq_length_of_mem_nodup v V hnd hv_mem
      change (V.filter fun x => decide (x = v) || adj v x).length = _ at hfor
      rw [hfor, hfeq]
      unfold deg
      omega
    have hS_ge1 : 1 ≤ S.length := by omega
    have hV'_le : V'.length ≤ N := by
      have hVlen : V.length ≤ N + 1 := hlen
      omega
    have hV'_nd : V'.Nodup := (List.filter_sublist).nodup hnd
    have halpha' : ∀ I' : List Int, I'.Nodup → (∀ x ∈ I', x ∈ V') →
        (∀ x ∈ I', ∀ y ∈ I', adj x y = false) → I'.length ≤ K - 1 := by
      intro I' hI'_nd hI'_sub hI'_ind
      have hv_not_V' : v ∉ V' := by
        intro hmem
        have hpv := (List.mem_filter.mp hmem).2
        simp [p] at hpv
      have hv_not_I' : v ∉ I' := fun h => hv_not_V' (hI'_sub v h)
      have hv_I'_nd : (v :: I').Nodup := List.nodup_cons.mpr ⟨hv_not_I', hI'_nd⟩
      have hv_I'_sub : ∀ x ∈ v :: I', x ∈ V := by
        intro x hx
        simp only [List.mem_cons] at hx
        rcases hx with rfl | hx_tail
        · exact hv_mem
        · exact (List.mem_filter.mp (hI'_sub x hx_tail)).1
      have hv_I'_ind : ∀ x ∈ v :: I', ∀ y ∈ v :: I', adj x y = false := by
        intro x hx y hy
        simp only [List.mem_cons] at hx hy
        rcases hx with rfl | hx_t <;> rcases hy with rfl | hy_t
        · exact hirr _
        · have hpy := (List.mem_filter.mp (hI'_sub y hy_t)).2
          simp only [p, Bool.not_eq_true'] at hpy
          by_cases hbad : adj x y = true
          · simp [hbad] at hpy
          · exact Bool.eq_false_iff.mpr hbad
        · have hpx := (List.mem_filter.mp (hI'_sub x hx_t)).2
          simp only [p, Bool.not_eq_true'] at hpx
          rw [hsymm x _]
          by_cases hbad : adj y x = true
          · simp [hbad] at hpx
          · exact Bool.eq_false_iff.mpr hbad
        · exact hI'_ind x hx_t y hy_t
      have hlen_le := halpha (v :: I') hv_I'_nd hv_I'_sub hv_I'_ind
      simp only [List.length_cons] at hlen_le
      omega
    have hIH := turan_graph_bound_aux adj hirr hsymm N V' hV'_le hV'_nd (K - 1) halpha'
    have htwoE_split : twoE adj V = sumNat (S.map (deg adj V)) + sumNat (V'.map (deg adj V)) :=
      sumNat_filter_partition p (deg adj V) V
    have hS_deg_lb : S.length * deg adj V v ≤ sumNat (S.map (deg adj V)) := by
      rw [← sumNat_map_const (deg adj V v) S]
      apply sumNat_map_le
      intro u hu
      exact hv_min u (List.mem_filter.mp hu).1
    have hV'_deg_lb : twoE adj V' ≤ sumNat (V'.map (deg adj V)) := by
      unfold twoE
      apply sumNat_map_le
      intro u _
      unfold deg
      exact (List.filter_sublist.filter (adj u)).length_le
    have hbound_twoE : S.length * S.length + (twoE adj V' + V'.length) ≤ twoE adj V + V.length := by
      have hm_eq : S.length * S.length = S.length * deg adj V v + S.length := by
        rw [hS_len, Nat.mul_add, Nat.mul_one]
      omega
    by_cases hK1 : K = 1
    · subst hK1
      simp only [Nat.sub_self, Nat.zero_mul, Nat.le_zero, Nat.mul_eq_zero] at hIH
      have hV'0 : V'.length = 0 := by rcases hIH with h | h <;> exact h
      have hVS : V.length = S.length := by omega
      have hS_le : S.length * S.length ≤ twoE adj V + V.length := by omega
      rw [hVS, Nat.one_mul]
      simpa [hVS] using hS_le
    · have hk'_ge1 : 1 ≤ K - 1 := by omega
      have hV'len : V'.length = V.length - S.length := by omega
      rw [hV'len] at hIH
      have hstep := turan_alg_step K (K - 1) V.length S.length (twoE adj V' + (V.length - S.length))
        (by omega) hk'_ge1 (by omega) hIH
      rw [← hV'len] at hstep
      exact Nat.le_trans hstep (Nat.mul_le_mul_left K hbound_twoE)

/--
Theorem 4.8 (Pure Lean 4 Turán / Caro-Wei Graph Bound):
For any duplicate-free vertex list `V` and symmetric loopless boolean adjacency `adj`,
if every independent subset of `V` has size at most `K`, then:
  `|V|^2 ≤ K * (2|E| + |V|)`.
-/
theorem turan_graph_bound (adj : Int → Int → Bool)
    (hirr : ∀ x, adj x x = false) (hsymm : ∀ x y, adj x y = adj y x)
    (V : List Int) (hV : V.Nodup) (K : Nat)
    (halpha : ∀ I : List Int, I.Nodup → (∀ x ∈ I, x ∈ V) →
      (∀ x ∈ I, ∀ y ∈ I, adj x y = false) → I.length ≤ K) :
    V.length * V.length ≤ K * (twoE adj V + V.length) :=
  turan_graph_bound_aux adj hirr hsymm V.length V (Nat.le_refl _) hV K halpha

/-- Conflict graph boolean adjacency on `A`: `u ≠ v` and `u + v ∈ A`. -/
def conflictAdjBool (A : List Int) (u v : Int) : Bool :=
  decide (u ≠ v) && A.contains (u + v)

/--
Theorem 4.9 (Turán / Caro-Wei Conflict Graph Rigidity for Sum-Avoidance):
If `A : List Int` is duplicate-free and every sum-avoiding subset `B ⊆ A` satisfies
`B.length ≤ K`, then:
  `A.length^2 ≤ K * (2 * numConflictEdges A + A.length)`.
-/
theorem turan_conflict_bound (A : List Int) (hA : A.Nodup) (K : Nat)
    (halpha : ∀ B : List Int, B.Nodup → (∀ b ∈ B, b ∈ A) → IsSumAvoiding A B → B.length ≤ K) :
    A.length * A.length ≤ K * (2 * numConflictEdges A + A.length) := by
  have hirr : ∀ x, conflictAdjBool A x x = false := by
    intro x
    simp [conflictAdjBool]
  have hsymm : ∀ x y, conflictAdjBool A x y = conflictAdjBool A y x := by
    intro x y
    by_cases hxy : x = y
    · subst hxy; simp [conflictAdjBool]
    · have hyx : y ≠ x := fun h => hxy h.symm
      simp [conflictAdjBool, hxy, hyx, Int.add_comm x y]
  have hbind : ∀ I : List Int, I.Nodup → (∀ x ∈ I, x ∈ A) →
      (∀ x ∈ I, ∀ y ∈ I, conflictAdjBool A x y = false) → I.length ≤ K := by
    intro I hI_nd hI_sub hI_adj
    apply halpha I hI_nd hI_sub
    intro b1 hb1 b2 hb2 hne hsum
    have hfalse := hI_adj b1 hb1 b2 hb2
    simp only [conflictAdjBool, decide_eq_true hne, Bool.true_and, List.contains_eq_mem,
      decide_eq_false_iff_not] at hfalse
    exact hfalse hsum
  have htur := turan_graph_bound (conflictAdjBool A) hirr hsymm A hA K hbind
  have htwoE : twoE (conflictAdjBool A) A = 2 * numConflictEdges A := by
    rw [← twoNumConflictEdges_eq_two_mul A]
    rfl
  rw [htwoE] at htur
  exact htur

/--
Theorem 4.10 (Combined Small-α Additive Energy Rigidity):
If `A : List Int` (`A.Nodup`, length `n`) has maximum sum-avoiding subset size `≤ K`
(`1 ≤ K ≤ n`), then Turán rigidity combined with Cauchy-Schwarz forces large additive energy:
  `K^2 * (n * energyNat A) ≥ n^2 * (n - K)^2`
(equivalently `energy A ≥ n * (n - K)^2 / K^2`).
-/
theorem energy_rigidity_from_small_alpha (A : List Int) (hA : A.Nodup) (K : Nat)
    (_hK_le : K ≤ A.length)
    (halpha : ∀ B : List Int, B.Nodup → (∀ b ∈ B, b ∈ A) → IsSumAvoiding A B → B.length ≤ K) :
    A.length * A.length * ((A.length - K) * (A.length - K)) ≤
      K * K * (A.length * energyNat A) := by
  have htur := turan_conflict_bound A hA K halpha
  have hedge : A.length * (A.length - K) ≤ 2 * K * numConflictEdges A := by
    have hmul_sub : A.length * (A.length - K) = A.length * A.length - K * A.length := by
      rw [Nat.mul_sub_left_distrib, Nat.mul_comm A.length K]
    have hmul_add : K * (2 * numConflictEdges A + A.length) =
        2 * K * numConflictEdges A + K * A.length := by
      rw [Nat.mul_add, Nat.mul_left_comm K 2 (numConflictEdges A), ← Nat.mul_assoc 2 K (numConflictEdges A)]
    omega
  have hedge_sq : (A.length * (A.length - K)) * (A.length * (A.length - K)) ≤
      (2 * K * numConflictEdges A) * (2 * K * numConflictEdges A) :=
    Nat.mul_le_mul hedge hedge
  have hE_nat : 4 * numConflictEdges A * numConflictEdges A ≤ A.length * energyNat A := by
    have hE_int := energy_ge_four_edges_sq A hA
    unfold energy at hE_int
    have hE_cast : ((4 * numConflictEdges A * numConflictEdges A : Nat) : Int) ≤
        ((A.length * energyNat A : Nat) : Int) := by
      simpa [Int.natCast_mul] using hE_int
    exact Int.ofNat_le.mp hE_cast
  have h_rearrange1 : (A.length * (A.length - K)) * (A.length * (A.length - K)) =
      A.length * A.length * ((A.length - K) * (A.length - K)) := by
    calc (A.length * (A.length - K)) * (A.length * (A.length - K))
        = A.length * ((A.length - K) * (A.length * (A.length - K))) := by rw [Nat.mul_assoc]
      _ = A.length * (A.length * ((A.length - K) * (A.length - K))) := by
            rw [Nat.mul_left_comm (A.length - K) A.length (A.length - K)]
      _ = A.length * A.length * ((A.length - K) * (A.length - K)) := by rw [← Nat.mul_assoc]
  have h_rearrange2 : (2 * K * numConflictEdges A) * (2 * K * numConflictEdges A) =
      K * K * (4 * numConflictEdges A * numConflictEdges A) := by
    have h2 : 2 * K * numConflictEdges A = K * (2 * numConflictEdges A) := by
      rw [Nat.mul_comm 2 K, Nat.mul_assoc]
    have h3 : (K * (2 * numConflictEdges A)) * (K * (2 * numConflictEdges A)) =
        K * K * (4 * numConflictEdges A * numConflictEdges A) := by
      calc (K * (2 * numConflictEdges A)) * (K * (2 * numConflictEdges A))
          = K * ((2 * numConflictEdges A) * (K * (2 * numConflictEdges A))) := by rw [Nat.mul_assoc]
        _ = K * (K * ((2 * numConflictEdges A) * (2 * numConflictEdges A))) := by
              rw [Nat.mul_left_comm (2 * numConflictEdges A) K (2 * numConflictEdges A)]
        _ = K * K * ((2 * numConflictEdges A) * (2 * numConflictEdges A)) := by rw [← Nat.mul_assoc]
        _ = K * K * (4 * numConflictEdges A * numConflictEdges A) := by
              congr 1
              calc (2 * numConflictEdges A) * (2 * numConflictEdges A)
                  = 2 * (numConflictEdges A * (2 * numConflictEdges A)) := by rw [Nat.mul_assoc]
                _ = 2 * (2 * (numConflictEdges A * numConflictEdges A)) := by
                      rw [Nat.mul_left_comm (numConflictEdges A) 2 (numConflictEdges A)]
                _ = (2 * 2) * (numConflictEdges A * numConflictEdges A) := by
                      rw [← Nat.mul_assoc 2 2 _]
                _ = 4 * numConflictEdges A * numConflictEdges A := by
                      rw [Nat.mul_assoc 4 _ _]
    rw [h2, h3]
  rw [h_rearrange1, h_rearrange2] at hedge_sq
  exact Nat.le_trans hedge_sq (Nat.mul_le_mul_left (K * K) hE_nat)

end Erdos787GeometryAndCarries

#print axioms Erdos787GeometryAndCarries.int_sq_nonneg
#print axioms Erdos787GeometryAndCarries.vecAdd_length
#print axioms Erdos787GeometryAndCarries.vecAdd_length_eq
#print axioms Erdos787GeometryAndCarries.vecSub_length
#print axioms Erdos787GeometryAndCarries.vecSub_length_eq
#print axioms Erdos787GeometryAndCarries.vecScale_length
#print axioms Erdos787GeometryAndCarries.vecAdd_comm
#print axioms Erdos787GeometryAndCarries.vecAdd_assoc
#print axioms Erdos787GeometryAndCarries.normSq_nonneg
#print axioms Erdos787GeometryAndCarries.dot_comm
#print axioms Erdos787GeometryAndCarries.dot_add_left
#print axioms Erdos787GeometryAndCarries.dot_add_right
#print axioms Erdos787GeometryAndCarries.dot_scale_left
#print axioms Erdos787GeometryAndCarries.dot_scale_right
#print axioms Erdos787GeometryAndCarries.normSq_add
#print axioms Erdos787GeometryAndCarries.normSq_scale
#print axioms Erdos787GeometryAndCarries.normSq_scale_add
#print axioms Erdos787GeometryAndCarries.dot_eq_zero_of_normSq_eq_zero
#print axioms Erdos787GeometryAndCarries.cauchy_schwarz_int
#print axioms Erdos787GeometryAndCarries.spherical_angle_criterion
#print axioms Erdos787GeometryAndCarries.normSq_sum4
#print axioms Erdos787GeometryAndCarries.spherical_k4_freeness
#print axioms Erdos787GeometryAndCarries.spherical_k4_clique_impossible
#print axioms Erdos787GeometryAndCarries.spherical_k4_free_set
#print axioms Erdos787GeometryAndCarries.directional_cap_sum_avoidance
#print axioms Erdos787GeometryAndCarries.directional_cap_sum_avoidance_sq
#print axioms Erdos787GeometryAndCarries.directional_cap_sum_avoidance_unit
#print axioms Erdos787GeometryAndCarries.directionalCapVec_sum_avoiding
#print axioms Erdos787GeometryAndCarries.pi_B_pow_shift
#print axioms Erdos787GeometryAndCarries.pi_B_eq_pow_sum
#print axioms Erdos787GeometryAndCarries.pi_B_add
#print axioms Erdos787GeometryAndCarries.pi_B_sub
#print axioms Erdos787GeometryAndCarries.absInt_lt_iff
#print axioms Erdos787GeometryAndCarries.absInt_le_iff
#print axioms Erdos787GeometryAndCarries.pi_B_zero_of_bounded
#print axioms Erdos787GeometryAndCarries.inBox_iff_absInt
#print axioms Erdos787GeometryAndCarries.pi_B_inj_of_ge_2L_add_1
#print axioms Erdos787GeometryAndCarries.pi_B_eq_preservation
#print axioms Erdos787GeometryAndCarries.pi_B_freiman_2_iso
#print axioms Erdos787GeometryAndCarries.carry_inj_sharp_at_2L
#print axioms Erdos787GeometryAndCarries.carry_eq_sharp_at_3L
#print axioms Erdos787GeometryAndCarries.carry_freiman_sharp_at_4L
#print axioms Erdos787GeometryAndCarries.sumAvoiding_transport_3L_add_1
#print axioms Erdos787GeometryAndCarries.dot_replicate_one
#print axioms Erdos787GeometryAndCarries.normSq_replicate_one
#print axioms Erdos787GeometryAndCarries.normSq_eq_sumSqInt
#print axioms Erdos787GeometryAndCarries.cauchy_schwarz_sum
#print axioms Erdos787GeometryAndCarries.sumSqInt_map
#print axioms Erdos787GeometryAndCarries.cauchy_schwarz_list
#print axioms Erdos787GeometryAndCarries.sumInt_map_ofNat
#print axioms Erdos787GeometryAndCarries.cauchy_schwarz_nat_list
#print axioms Erdos787GeometryAndCarries.ind_le
#print axioms Erdos787GeometryAndCarries.ind_and
#print axioms Erdos787GeometryAndCarries.length_filter_eq_sumNat
#print axioms Erdos787GeometryAndCarries.sumNat_map_add
#print axioms Erdos787GeometryAndCarries.sumNat_map_le
#print axioms Erdos787GeometryAndCarries.sumNat_map_congr
#print axioms Erdos787GeometryAndCarries.sumNat_map_const
#print axioms Erdos787GeometryAndCarries.sumNat_map_mul_left
#print axioms Erdos787GeometryAndCarries.sumNat_map_mul_right
#print axioms Erdos787GeometryAndCarries.sumNat_mul_sumNat
#print axioms Erdos787GeometryAndCarries.sumNat_swap
#print axioms Erdos787GeometryAndCarries.sumNat_filter_partition
#print axioms Erdos787GeometryAndCarries.repSumDistinctNat_le_repSumNat
#print axioms Erdos787GeometryAndCarries.sum_repSum_sq_le_energy
#print axioms Erdos787GeometryAndCarries.energy_ineq_all
#print axioms Erdos787GeometryAndCarries.energy_ineq_distinct
#print axioms Erdos787GeometryAndCarries.twoNumConflictEdges_eq_two_mul
#print axioms Erdos787GeometryAndCarries.sum_repSumDistinct_eq_two_mul_edges
#print axioms Erdos787GeometryAndCarries.sum_repSumDistinct_int_eq_two_mul_edges
#print axioms Erdos787GeometryAndCarries.sum_repSum_eq_two_mul_edges_of_no_double
#print axioms Erdos787GeometryAndCarries.sum_repSum_ge_two_mul_edges
#print axioms Erdos787GeometryAndCarries.energy_ge_four_edges_sq
#print axioms Erdos787GeometryAndCarries.turan_graph_bound
#print axioms Erdos787GeometryAndCarries.turan_conflict_bound
#print axioms Erdos787GeometryAndCarries.energy_rigidity_from_small_alpha
