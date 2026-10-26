import LcBad
/-! Seat D: shows why the olean-trust gap is real — `lean` trusts imported oleans without re-checking. -/
theorem SeatD003.false_from_bad_olean : False := SeatD003.bad
#print axioms SeatD003.false_from_bad_olean
