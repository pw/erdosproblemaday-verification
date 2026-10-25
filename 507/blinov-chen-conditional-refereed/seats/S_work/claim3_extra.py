# Seat S: side computation (not a claim under review): if the (1,2)-minor is also used, alpha forces equal labels,
# giving an extra factor r^-5 in the pair bound.  Exponent bookkeeping as in claim3.py.
from fractions import Fraction as F
for name, k in [("Blinov", 408781), ("bt163", 356155), ("Wroblewski", 275385)]:
    # pair r-exponent with the extra r^-5:  gamma + 123k + 3 - 5 - 9u < 0 for all gamma<1  <=>  9u >= 123k - 1 ... take smallest u with 9u > 123k - 1
    u = next(u for u in range(13*k, 15*k) if 9*u > 123*k - 2 + 1)    # gamma -> 1 worst case
    X = 60*k + 9*u + 3; g = F(X, X+1)
    assert g + 123*k - 2 - 9*u < 0 and not (g + 123*k - 2 - 9*(u-1) < 0)
    print(f"{name}: k={k} u={u} X={X} eta=2/{X+2} ~{2/(X+2):.6e}   sup with r^-5: 2/{183*k+3}   (claimed: u={-(-(41*k+2)//3)})")
