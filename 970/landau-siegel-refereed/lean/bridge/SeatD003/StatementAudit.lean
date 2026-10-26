import SeatD003.NoLSStatement
import SeatD003.ConstAudit
/-! Seat D: Mathlib-only side. Print the elaborated statement in full and audit its constants. -/
set_option pp.all true in
#print SeatD003.NoLandauSiegel
#seatD_audit SeatD003.NoLandauSiegel
-- the instances synthesized for the statement, spelled out
set_option pp.explicit true in
#print SeatD003.NoLandauSiegel
