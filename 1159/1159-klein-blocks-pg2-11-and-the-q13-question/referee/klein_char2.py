"""Referee: does the explicit Klein construction survive in characteristic 2 (where -7 = 1 is a square)? q=2."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from klein_explicit_lib import klein
F, out = klein(2)
for c, Qp, Tp, Lp in out:
    print(f"q=2 c={c}: distinct 'quadruple' points {len(Qp)} (need 21), 'triple' points {len(Tp)} (need 28), lines {len(Lp)} (need 21) -> degenerate")
