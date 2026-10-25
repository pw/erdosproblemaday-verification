import FormalConjectures.ErdosProblems.«184»
import EGCheck.Final
-- Our own statement check: FC's elaborated statement (imported from FC's own module, built from the pinned FC source) as the TYPE,
-- Coffey's term as the proof. If this elaborates, the term proves FC's erdos_184; #print axioms walks the whole proof.
theorem ours184.{u} : type_of% @_root_.Erdos184.erdos_184.{u} := @EGCheck.erdos_184.{u}
#print axioms ours184
#print axioms EGCheck.erdos_184
#print axioms EGCheck.Bridge.solution
set_option pp.all true in
#check @Erdos184.erdos_184
set_option pp.all true in
#print Erdos184.IsCycleOrEdge
set_option pp.all true in
#print SimpleGraph.IsDecomposition
