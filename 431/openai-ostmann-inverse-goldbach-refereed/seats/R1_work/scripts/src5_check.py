# Check (3.5): |H^k - J^{-k} sum_{distinct ordered} y_i1..y_ik| <= sum_{1<=j<=k/2} (k^C/J)^j |H|^{k-2j}, y_i in {0,1,-1}, k even.
# paper: C absolute (proof gives C=3). Control: replace k^C by 1 -> must FAIL somewhere.
from fractions import Fraction as Fr
import random, sys, math
C = float(sys.argv[1]); random.seed(7)
worst = 0.0; fails = 0; tests = 0
for trial in range(3000):
    J = random.randint(3,40); k = random.choice([2,4,6,8,10])
    if k > J: continue
    mode = random.random()
    if mode < 0.3: y = [1]*J
    elif mode < 0.6: y = [random.choice([0,1,-1]) for _ in range(J)]
    else:
        p = random.random(); y = [1 if random.random()<p else random.choice([0,-1]) for _ in range(J)]
    e = [Fr(1)] + [Fr(0)]*k
    for yi in y:
        for t in range(k,0,-1): e[t] += e[t-1]*yi
    distinct = math.factorial(k)*e[k]
    H = Fr(sum(y),J)
    lhs = abs(H**k - distinct/Fr(J)**k)
    rhs = sum((k**C/J)**j * float(abs(H))**(k-2*j) for j in range(1,k//2+1))
    tests += 1
    if float(lhs) > rhs*(1+1e-12): fails += 1
    if rhs>0: worst = max(worst, float(lhs)/rhs)
print(f"C={C}: tests={tests} fails={fails} max lhs/rhs={worst:.4f}")
