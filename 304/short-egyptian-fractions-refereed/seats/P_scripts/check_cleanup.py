# Lemma 6.1 (repetition removal at total one preserving a multiple of odd Q), random stress test,
# plus a concrete Section-6 pipeline for Q = 3*5*7 = 105.
import random, math
from fractions import Fraction
from collections import Counter
random.seed(3)
def cleanup(lst, Q, rng):
    lst = sorted(lst); steps = 0
    while True:
        c = Counter(lst); reps = [x for x, k in c.items() if k >= 2]
        if not reps: return lst, steps
        mm = rng.choice(reps); steps += 1
        lst.remove(mm); lst.remove(mm)
        if mm % 2 == 0: lst.append(mm // 2)
        else: lst += [(mm + 1)//2, mm*(mm + 1)//2]
        lst.sort()
        assert sum(Fraction(1, x) for x in lst) == 1
        assert any(x % Q == 0 for x in lst), "lost multiple of Q"
        if steps > 100000: raise RuntimeError("no termination")
fails = 0; maxsteps = 0
for trial in range(4000):
    Q = random.choice([3, 5, 15, 21, 105, 9, 45])
    lst = [Q]*Q                     # Q copies of 1/Q
    for _ in range(random.randint(0, 6)):   # random splits, some creating duplicates
        i = random.randrange(len(lst)); x = lst.pop(i)
        op = random.random()
        if op < 0.4: lst += [2*x, 2*x]
        elif op < 0.7: lst += [x+1, x*(x+1)]
        else: lst += [3*x, 3*x, 3*x]
    if len(lst) > 400: continue
    t = len(lst)
    out, st = cleanup(lst, Q, random.Random(trial))
    maxsteps = max(maxsteps, st)
    ok = len(out) <= t and len(set(out)) == len(out) and sum(Fraction(1, x) for x in out) == 1 and any(x % Q == 0 for x in out)
    if not ok: fails += 1; print("FAIL", Q, lst, out)
print("Lemma 6.1 random stress: fails", fails, "max steps", maxsteps)

# Section 6 pipeline, r = 3: Q = 105, find a short expansion of 104/105 by brute force (min length), append 1/105
Q = 105
def short_exp(num, den, t, lo):
    x = Fraction(num, den)
    if t == 1:
        return [x.denominator] if x.numerator == 1 and x.denominator >= lo else None
    for n in range(max(lo, math.floor(1/x) + 1 if t > 1 else lo), math.ceil(t/x) + 1):
        if Fraction(1, n) >= x: continue
        r = x - Fraction(1, n)
        s = short_exp(r.numerator, r.denominator, t - 1, n + 1)
        if s: return [n] + s
    return None
for t in range(1, 6):
    e = short_exp(104, 105, t, 2)
    if e: break
S0 = sorted(e + [Q]); print("expansion of 104/105:", e, "-> list", S0)
S, _ = cleanup(S0, Q, random.Random(0)); S = sorted(S)
s = len(S); n = next(x for x in S if x % Q == 0)
divs = [d for d in range(1, n) if n % d == 0]
tau = len(divs) + 1
rest = [x for x in S if x != n]
sets = set()
for d in divs:
    a, b = n + d, n + n*n//d
    if a in rest or b in rest: continue
    T = tuple(sorted(rest + [a, b]))
    assert sum(Fraction(1, x) for x in T) == 1 and len(set(T)) == len(T)
    sets.add(T)
print(f"S={S}, s={s}, n={n}, tau(n)={tau}, distinct expansions of length {s+1}: {len(sets)}  (claimed >= 2^r-2s+1 = {2**3-2*s+1})")
