# Check of the upper-bound construction on p.2-3 (attributed to Hadwiger [13]):
# hexagons of circumradius r, centres on a triangular lattice of spacing sqrt(3) r, 7-colouring by cosets of (2-w)Z[w].
# Need: (a) diameter 2r < 1; (b) same-colour centre distance sqrt(21) r and (sqrt(21)-2) r > 1.
from fractions import Fraction as Fr
from itertools import product
def ok(r):
    a = 2*r < 1
    b = 21*r*r > (1+2*r)**2          # (sqrt21 - 2) r > 1  <=>  sqrt21 r > 1 + 2r  (both sides positive)
    return a, b
for r in [Fr(2,5), Fr(1,2), Fr(3,8), Fr(39,100)]:
    print(f"r={r}: 2r<1 {ok(r)[0]}, (sqrt21-2)r>1 {ok(r)[1]}", "<- paper's choice" if r==Fr(2,5) else "(control)")
# index of (2-w)Z[w] and its minimal nonzero norm (norm of a+bw is a^2 - ab + b^2)
N = lambda a,b: a*a - a*b + b*b
print("|2-w|^2 =", N(2,-1))
# elements of the sublattice (2-w)(x+yw) = (2x+y) + (2y - x - y... ) compute via multiplication in Z[w], w^2 = -1 - w
def mul(p,q):
    a,b=p; c,d=q
    return (a*c - b*d, a*d + b*c - b*d)
norms = sorted({N(*mul((2,-1),(x,y))) for x,y in product(range(-4,5),repeat=2) if (x,y)!=(0,0)})
print("smallest nonzero norms in (2-w)Z[w]:", norms[:4], "-> min distance sqrt(7) in lattice units; times spacing sqrt(3) r = sqrt(21) r")
# index = number of cosets: count residues of Z[w] mod (2-w) by brute force on a box
reps=set()
for a,b in product(range(-10,11),repeat=2):
    # reduce (a,b) modulo the sublattice by checking equivalence with a small representative set
    found=None
    for (c,d) in reps:
        # (a-c, b-d) in (2-w)Z[w] iff (a-c,b-d)*(2-w̄)/7 is integral; (2-w)(2-w̄)=7, w̄ = -1-w so 2-w̄ = 3+w
        x,y = mul((a-c,b-d),(3,1))
        if x%7==0 and y%7==0: found=(c,d); break
    if found is None: reps.add((a,b))
print("number of cosets of (2-w)Z[w] in Z[w]:", len(reps))
