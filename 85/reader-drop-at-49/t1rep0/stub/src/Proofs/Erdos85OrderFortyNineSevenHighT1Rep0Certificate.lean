import Proofs.Erdos85OrderFortyNineSevenHighCertificateBridge
import Proofs.Erdos85OrderFortyNineLratCertificateBase

/-! STUB written by the erdos cron seat (2026-10-20) — NOT the authors' module.
    The authors' module checks its 1.6 GB packed LRAT certificate by `native_decide`
    (`sevenHighT1Rep0_check`); on our shared box that build exceeds the memory left by
    other tenants (earlyoom SIGTERM at 28 GB, 10,579 s).  The same certificate was checked
    OUTSIDE Lean against the CNF rendered from `orderFortyNineGeneratedH7SatCnf
    (representativeMasks 1 0)` by cake_lpr (CakeML-verified, commit a36874a) and by the
    referee's strict RUP checker (see ../README.md).  NOT by drat-trim's lrat-check alone:
    lrat-check accepts a final empty clause whose hints never reach a conflict (referee,
    2026-10-20; reproduced on t7 with the empty clause's last hint dropped).  This stub
    exports the one declaration downstream modules use, from a single, clearly named axiom
    (the CNF's `Unsat`), so `#print axioms` on the capstones shows exactly what is
    substituted and nothing else. -/

namespace Erdos85

open Std.Tactic.BVDecide

open Std Sat in
/-- What the external runs establish: cake_lpr and a strict RUP checker each accept the
authors' certificate against the DIMACS rendering of exactly this CNF (EmitT1Rep0.lean checks,
at run time, that the rendered clause array maps clausewise to this CNF's clauses). -/
axiom erdos85_t1rep0_cnf_unsat_checked_externally :
    (orderFortyNineGeneratedH7SatCnf
      (OrderFortyNineSevenHighCensus.representativeMasks 1 0)).Unsat

open Std Sat in
theorem sevenHighT1Rep0_excluded :
    SevenHighCanonicalRepresentativeExcluded 1 0 := by
  intro edges hc
  obtain ⟨val, hsegments, _⟩ :=
    orderFortyNineH7CnfSegments_satisfied hc (representativeMasks_h7_high_zero 1 0)
  have hsat := sat_of_orderFortyNineH7CnfSegmentsSatisfied_of_covered
    hsegments (orderFortyNineGeneratedH7SatCnf_covered _)
  have hfalse := erdos85_t1rep0_cnf_unsat_checked_externally (satAssignmentOfDimacs val)
  rw [hsat] at hfalse
  contradiction

end Erdos85
