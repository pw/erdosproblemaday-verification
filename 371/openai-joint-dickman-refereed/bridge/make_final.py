# Bridge371.lean = BridgeCore.lean with the import swapped to OpenAI's PaperMain closure + the unconditional instantiations.
core=open('BridgeCore.lean').read()
assert core.startswith('import OAI.NumberTheory.JointDickman.Amplification.Ordering\n')
body=core.replace('import OAI.NumberTheory.JointDickman.Amplification.Ordering\n','import OAI.NumberTheory.JointDickman.PaperMain\n',1)
tail='''
/-! ## Unconditional instantiations from OpenAI's library (`OAI.NumberTheory.JointDickman.UnconditionalMain`) -/

namespace Erdos371

/--
Let $P(n)$ denote the largest prime factor of $n$. Show that the set of $n$
with $P(n+1) > P(n)$ has density $\\frac{1}{2}$.

This was proved by an internal OpenAI model in September 2026 [OAI26a]; see the linked Lean proof.
-/
theorem erdos_371 :
    { n | Nat.maxPrimeFac (n + 1) > Nat.maxPrimeFac n }.HasDensity (1/2) := by
  exact erdos_371_of_increasingOrderLaw OAI.JointDickman.increasingOrderLaw_unconditional

end Erdos371

namespace EPAD371

/-- Erdős #928, as posed (strict inequalities, threshold (n+1)^β): for α, β ∈ (0,1) the density of
{n : P(n) < n^α, P(n+1) < (n+1)^β} exists and equals ρ(1/α)ρ(1/β). -/
theorem erdos_928 {α β : ℝ} (hα : 0 < α) (hα1 : α < 1) (hβ : 0 < β) (hβ1 : β < 1) :
    {n : ℕ | (n.maxPrimeFac : ℝ) < (n : ℝ) ^ α ∧
        ((n + 1).maxPrimeFac : ℝ) < (((n + 1 : ℕ) : ℝ)) ^ β}.HasDensity
      (OAI.Erdos970.NumberTheoryLean.Dickman.rho (1 / α) *
        OAI.Erdos970.NumberTheoryLean.Dickman.rho (1 / β)) :=
  erdos_928_of_jointLaw OAI.JointDickman.jointDickmanLaw_unconditional hα hα1 hβ hβ1

/-- #928's literal question: the density exists. -/
theorem erdos_928_exists {α β : ℝ} (hα : 0 < α) (hα1 : α < 1) (hβ : 0 < β) (hβ1 : β < 1) :
    ∃ d : ℝ, {n : ℕ | (n.maxPrimeFac : ℝ) < (n : ℝ) ^ α ∧
        ((n + 1).maxPrimeFac : ℝ) < (((n + 1 : ℕ) : ℝ)) ^ β}.HasDensity d :=
  ⟨_, erdos_928 hα hα1 hβ hβ1⟩

end EPAD371
'''
open('Bridge371.lean','w').write(body+tail)
open('AxBridge.lean','w').write('''import Bridge371
#print axioms Erdos371.erdos_371
#print axioms EPAD371.erdos_928
#print axioms EPAD371.erdos_928_exists
#print axioms OAI.JointDickmanPaper.joint_law
''')
# mutants: each must FAIL to compile
mut=[('MutValue', 'HasDensity (1/2) := by\n  exact erdos_371_of_increasingOrderLaw OAI', 'HasDensity (1/3) := by\n  exact erdos_371_of_increasingOrderLaw OAI'),
     ('MutStrict928', "(((n + 1 : ℕ) : ℝ)) ^ β}.HasDensity\n      (OAI.Erdos970", "(((n + 1 : ℕ) : ℝ)) ^ (β / 2)}.HasDensity\n      (OAI.Erdos970"),
     ('MutDensityDef', '((S ∩ A) ∩ Iio b).ncard / (A ∩ Iio b).ncard', '((S ∩ A) ∩ Iic b).ncard / (A ∩ Iio b).ncard')]
full=open('Bridge371.lean').read()
for name,a,b in mut:
    assert full.count(a)>=1, name
    open(f'Bridge{name}.lean','w').write(full.replace(a,b,1))
print('written')
