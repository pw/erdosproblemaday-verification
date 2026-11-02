import sys; sys.path.insert(0,'.')
from examples import check  # reuses the controlled checker (re-runs its controls/examples on import)
s48=[(2,3),(3,4),(4,5),(1,6),(5,8),(3,9),(2,10),(10,12),(1,15),(9,16),(6,18),(8,20),(12,24),(10,30),(18,36),(0,40),(36,45),(33,48)]
print("Sec 8.6 18-class system, moduli <= 48:", len(s48), check(s48), "max", max(n for a,n in s48))
s216=[(2,3),(2,4),(1,6),(0,8),(3,9),(4,12),(15,18),(15,24),(9,27),(24,36),(45,54),(36,72),(81,108),(27,216)]
print("Table 7 L=216 14-class system:", len(s216), check(s216), sorted(n for a,n in s216)==sorted(d for d in range(3,217) if 216%d==0))
