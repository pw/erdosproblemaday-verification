# Numeric checks of constants quoted from sources (control: a transposed formula must NOT match).
import math
e = math.e
checks = [
  ("Katz-Tardos Cor.6 (48-14e)/(55-16e) vs paper's 0.864137", (48-14*e)/(55-16*e), 0.864137),
  ("Katz-Tardos Cor.5 (10-3e)/(24-7e) vs KT's 0.371107", (10-3*e)/(24-7*e), 0.371107),
  ("Tardos 2003 Cor.15 4e/(5e-1) (~0.8635)", 4*e/(5*e-1), 0.8635),
  ("Katz 19/22 vs KT's quoted 0.863636", 19/22, 0.863636),
  ("CONTROL transposed (48-16e)/(55-14e) vs 0.864137", (48-16*e)/(55-14*e), 0.864137),
]
for name, val, ref in checks:
    ok = abs(val - ref) < 5e-5
    print("%-58s %.7f  %s" % (name, val, "MATCH" if ok else "NO MATCH"))
iso = (117-34*e)/(55-16*e)
print("Katz-Tardos Cor.8 isosceles exponent (117-34e)/(55-16e) = %.6f => F_n(s)->0 already follows for s > %.4f" % (iso, iso-2))
