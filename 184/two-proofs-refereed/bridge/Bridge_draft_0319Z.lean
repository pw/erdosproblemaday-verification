import Mathlib
import OAI.Combinatorics.CycleDecomposition.Main

/-!
# Bridge: OpenAI's `MainStatement` ⇒ Formal Conjectures' `Erdos184.erdos_184` (verbatim copy)

DRAFT, written by the formal-referee seat 2026-10-20, NOT YET COMPILED. Intended to be compiled
inside the OpenAI project (`/tmp/oaimath/604/lean-build/repo/lean`, Lean v4.34.1, Mathlib
d13f23b7) as e.g. `OAI/Combinatorics/CycleDecomposition/Bridge184.lean` or via
`lake env lean Bridge.lean`.

Why a copy and not an import: Formal Conjectures (2424bb48 and current main) is pinned to Lean
v4.33.1 / Mathlib 0df444a3, the OpenAI tree to Lean v4.34.1 / Mathlib d13f23b7, so the two cannot
be imported into one environment. The two FC definitions and the statement below are therefore
COPIED VERBATIM (only the namespace changed: `SimpleGraph.IsDecomposition` → `Bridge184.IsDecomposition`,
`Erdos184.IsCycleOrEdge` → `Bridge184.IsCycleOrEdge`; FC's `@[category …]` attributes and module
headers dropped). Sources:
* `FormalConjecturesForMathlib/Combinatorics/SimpleGraph/Decomposition.lean`
  (sha256 86bf339a… at FC 2424bb48 AND at FC main — identical);
* `FormalConjectures/ErdosProblems/184.lean` at FC 2424bb48 (sha256 9f36e4e0…); at FC main the
  statement of `erdos_184` and `IsCycleOrEdge` are textually unchanged (only attributes/docstrings).
The Mathlib definitions the statement unfolds to (Subgraph, Subgraph.coe, Connected, Preconnected,
Reachable, Walk, neighborSet, neighborFinset, degree, IsRegularOfDegree, edgeSet, edgeFinset,
neighborSetFintype, fintypeEdgeSet) are textually identical between Mathlib 0df444a3 and d13f23b7
(checked by the referee seat; see referee_formal.md).

Proof strategy (instance-generic, as in Coffey's `EGCheck/BridgeLemmas.lean`): prove the body of
`IsCycleOrEdge H.coe` for ARBITRARY instances `i₁ : H.coe.LocallyFinite`, `i₂ : Fintype H.coe.edgeSet`,
then close the verbatim statement by `hcyc H hH _ _` (the kernel unfolds `IsCycleOrEdge` and
instantiates the classical instances picked by elaboration).
-/

namespace Bridge184

open Filter SimpleGraph

universe u

/-! ## Verbatim copies of the Formal Conjectures definitions -/

/--
`D` is a decomposition of `G` into edge-disjoint subgraphs: the edge sets of the members of `D`
are pairwise disjoint and their union is the edge set of `G`.
-/
def IsDecomposition {V : Type*} (G : SimpleGraph V) (D : Finset G.Subgraph) : Prop :=
  Set.PairwiseDisjoint (D : Set G.Subgraph) (fun H ↦ H.edgeSet) ∧
  (⋃ H ∈ D, H.edgeSet) = G.edgeSet

/--
A graph $H$ is a cycle or an edge if it is connected and 2-regular, or if it has exactly one edge.
-/
def IsCycleOrEdge {U : Type*} [Fintype U] (H : SimpleGraph U) : Prop :=
  open scoped Classical in
  (H.Connected ∧ H.IsRegularOfDegree 2) ∨ H.edgeFinset.card = 1

/-! ## Instance-generic helper lemmas -/

/-- The degree, for an arbitrary `Fintype` instance on the neighbour set, is the `ncard`. -/
theorem degree_eq_ncard {W : Type*} (H : SimpleGraph W) (v : W)
    (inst : Fintype (H.neighborSet v)) :
    @SimpleGraph.degree W H v inst = (H.neighborSet v).ncard := by
  rw [← card_neighborSet_eq_degree, ← Nat.card_eq_fintype_card, Nat.card_coe_set_eq]

/-- The number of edges, for an arbitrary `Fintype` instance on the edge set, is the `ncard`. -/
theorem card_edgeFinset_eq_ncard {W : Type*} (H : SimpleGraph W) (inst : Fintype H.edgeSet) :
    (@SimpleGraph.edgeFinset W H inst).card = H.edgeSet.ncard := by
  rw [← Set.ncard_coe_finset, coe_edgeFinset]

theorem mem_edgeSet_comap {V W : Type*} (f : V → W) (G : SimpleGraph W) (e : Sym2 V) :
    e ∈ (G.comap f).edgeSet ↔ Sym2.map f e ∈ G.edgeSet := by
  induction e using Sym2.ind with
  | _ a b => simp

/-- One OpenAI part (a cycle edge set or a single edge of `G'`), pushed forward along an injective
homomorphism `φ : G' →g G`, is the edge set of a subgraph of `G` satisfying the body of
`IsCycleOrEdge` on its coe, for arbitrary instances. -/
theorem exists_sub {W : Type} (G' : SimpleGraph W) {V : Type u} (G : SimpleGraph V)
    (φ : G' →g G) (hφ : Function.Injective φ) (s : Set (Sym2 W))
    (hs : OAI.ErdosGallai.CycleOrSingleEdge G' s) :
    ∃ H : G.Subgraph, H.edgeSet = Sym2.map φ '' s ∧
      ∀ (i₁ : H.coe.LocallyFinite) (i₂ : Fintype H.coe.edgeSet),
        (H.coe.Connected ∧ @IsRegularOfDegree _ H.coe i₁ 2) ∨
          (@edgeFinset _ H.coe i₂).card = 1 := by
  rcases hs with ⟨v, p, hp, rfl⟩ | ⟨x, hx, rfl⟩
  · -- a cycle: the subgraph of the mapped cycle walk
    have hq : (p.map φ).IsCycle := hp.map hφ
    refine ⟨(p.map φ).toSubgraph, ?_, ?_⟩
    · rw [Walk.edgeSet_toSubgraph, Walk.edgeSet_map]
    · intro i₁ i₂
      left
      refine ⟨(p.map φ).toSubgraph_connected.coe, fun w => ?_⟩
      rw [degree_eq_ncard, ← Nat.card_coe_set_eq,
        Nat.card_congr (Subgraph.coeNeighborSetEquiv w), Nat.card_coe_set_eq]
      exact hq.ncard_neighborSet_toSubgraph_eq_two ((p.map φ).mem_verts_toSubgraph.1 w.2)
  · -- a single edge: the one-edge subgraph
    induction x using Sym2.ind with
    | _ a b =>
      have hab : G.Adj (φ a) (φ b) := φ.map_adj hx
      refine ⟨G.subgraphOfAdj hab, ?_, ?_⟩
      · rw [edgeSet_subgraphOfAdj, Set.image_singleton, Sym2.map_mk]
      · intro i₁ i₂
        right
        rw [card_edgeFinset_eq_ncard,
          ← Set.ncard_image_of_injective _ (Sym2.map.injective Subtype.val_injective),
          Subgraph.image_coe_edgeSet_coe, edgeSet_subgraphOfAdj, Set.ncard_singleton]

/-- An OpenAI decomposition of the copy `G.comap e.symm` on `Fin m` gives a Formal Conjectures
decomposition of `G` with at most `k` members. -/
theorem per_graph_aux {V : Type u} {m : ℕ} (e : V ≃ Fin m) (G : SimpleGraph V) (k : ℕ)
    (hdec : OAI.ErdosGallai.EdgeDecomposition (G.comap e.symm) k) :
    ∃ D : Finset G.Subgraph,
      (∀ H ∈ D, ∀ (i₁ : H.coe.LocallyFinite) (i₂ : Fintype H.coe.edgeSet),
        (H.coe.Connected ∧ @IsRegularOfDegree _ H.coe i₁ 2) ∨
          (@edgeFinset _ H.coe i₂).card = 1) ∧
      IsDecomposition G D ∧ D.card ≤ k := by
  classical
  obtain ⟨parts, hparts, hdisj, hunion⟩ := hdec
  let φ : G.comap e.symm →g G := SimpleGraph.Hom.comap (⇑e.symm) G
  have hφ : Function.Injective φ := e.symm.injective
  have key : ∀ i, ∃ H : G.Subgraph, H.edgeSet = Sym2.map φ '' parts i ∧
      ∀ (i₁ : H.coe.LocallyFinite) (i₂ : Fintype H.coe.edgeSet),
        (H.coe.Connected ∧ @IsRegularOfDegree _ H.coe i₁ 2) ∨
          (@edgeFinset _ H.coe i₂).card = 1 :=
    fun i => exists_sub (G.comap e.symm) G φ hφ (parts i) (hparts i)
  choose H hHe hHc using key
  -- `⇑φ` is `⇑e.symm` by definition
  have hHe' : ∀ i, (H i).edgeSet = Sym2.map e.symm '' parts i := hHe
  refine ⟨Finset.univ.image H, ?_, ⟨?_, ?_⟩, ?_⟩
  · intro K hK i₁ i₂
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.1 hK
    exact hHc i i₁ i₂
  · intro K₁ hK₁ K₂ hK₂ hne
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.1 (Finset.mem_coe.1 hK₁)
    obtain ⟨j, -, rfl⟩ := Finset.mem_image.1 (Finset.mem_coe.1 hK₂)
    have hij : i ≠ j := fun h => hne (congrArg H h)
    show Disjoint (H i).edgeSet (H j).edgeSet
    rw [hHe' i, hHe' j]
    exact Set.disjoint_image_of_injective (Sym2.map.injective e.symm.injective) (hdisj hij)
  · ext x
    rw [Set.mem_iUnion₂]
    constructor
    · rintro ⟨K, hK, hxK⟩
      obtain ⟨i, -, rfl⟩ := Finset.mem_image.1 hK
      exact (H i).edgeSet_subset hxK
    · intro hx
      have hy : Sym2.map e x ∈ (G.comap e.symm).edgeSet :=
        (mem_edgeSet_comap _ _ _).2 (by simpa [Sym2.map_map] using hx)
      rw [← hunion, Set.mem_iUnion] at hy
      obtain ⟨i, hi⟩ := hy
      refine ⟨H i, Finset.mem_image.2 ⟨i, Finset.mem_univ _, rfl⟩, ?_⟩
      rw [hHe' i]
      exact ⟨Sym2.map e x, hi, by simp [Sym2.map_map]⟩
  · calc (Finset.univ.image H).card ≤ (Finset.univ : Finset (Fin k)).card :=
          Finset.card_image_le
      _ = k := by simp

/-- Per graph: OpenAI's bound on `Fin (card V)` transported to `V`. -/
theorem per_graph (C : ℝ)
    (hmain : ∀ (n : ℕ) (G : SimpleGraph (Fin n)),
      ∃ k : ℕ, OAI.ErdosGallai.EdgeDecomposition G k ∧ (k : ℝ) ≤ C * n)
    {V : Type u} [Fintype V] (G : SimpleGraph V) :
    ∃ D : Finset G.Subgraph,
      (∀ H ∈ D, ∀ (i₁ : H.coe.LocallyFinite) (i₂ : Fintype H.coe.edgeSet),
        (H.coe.Connected ∧ @IsRegularOfDegree _ H.coe i₁ 2) ∨
          (@edgeFinset _ H.coe i₂).card = 1) ∧
      IsDecomposition G D ∧ (D.card : ℝ) ≤ C * (Fintype.card V : ℝ) := by
  classical
  obtain ⟨k, hdec, hk⟩ := hmain (Fintype.card V) (G.comap (Fintype.equivFin V).symm)
  obtain ⟨D, hcyc, hD, hcard⟩ := per_graph_aux (Fintype.equivFin V) G k hdec
  exact ⟨D, hcyc, hD, le_trans (by exact_mod_cast hcard) hk⟩

/-! ## The bridge, with the Formal Conjectures statement copied verbatim -/

open scoped Classical in
/--
OpenAI's `MainStatement` implies the Formal Conjectures statement of Erdős Problem 184
(`Erdos184.erdos_184`, copied verbatim; `IsCycleOrEdge`/`IsDecomposition` are the verbatim copies
above), with `f n = C * n`.
-/
theorem bridge : OAI.ErdosGallai.MainStatement →
    ∃ f : ℕ → ℝ,
      (f =O[atTop] fun n : ℕ ↦ (n : ℝ)) ∧
      ∀ {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V),
      ∃ (D : Finset G.Subgraph),
        (∀ H ∈ D, IsCycleOrEdge H.coe) ∧
        IsDecomposition G D ∧
        (D.card : ℝ) ≤ f (Fintype.card V) := by
  intro h
  unfold OAI.ErdosGallai.MainStatement at h
  obtain ⟨C, -, hmain⟩ := h
  refine ⟨fun n : ℕ ↦ C * (n : ℝ), (Asymptotics.isBigO_refl _ _).const_mul_left C, ?_⟩
  intro V _ _ G
  obtain ⟨D, hcyc, hD, hcard⟩ := per_graph C hmain G
  exact ⟨D, fun H hH => hcyc H hH _ _, hD, hcard⟩

open scoped Classical in
/-- The Formal Conjectures statement, discharged by OpenAI's kernel-checked theorem. -/
theorem erdos_184 :
    ∃ f : ℕ → ℝ,
      (f =O[atTop] fun n : ℕ ↦ (n : ℝ)) ∧
      ∀ {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V),
      ∃ (D : Finset G.Subgraph),
        (∀ H ∈ D, IsCycleOrEdge H.coe) ∧
        IsDecomposition G D ∧
        (D.card : ℝ) ≤ f (Fintype.card V) :=
  bridge OAI.ErdosGallai.erdos_gallai

end Bridge184

-- Expected: [propext, Classical.choice, Quot.sound]
#print axioms Bridge184.erdos_184
