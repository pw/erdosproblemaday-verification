import math, random
random.seed(18)
viol=0; fired=0; n=0; tight=0; quadcases=0
for i in range(300000):
    x=random.randint(18,200)
    y=random.randint(x+1, 10**random.randint(3,40))
    num=x+y; den=x*y; g=math.gcd(num,den); a=num//g; b=den//g
    n+=1
    if a*a>4*b:
        quadcases+=1
        Dl=a*a-4*b; s=math.isqrt(Dl); s+=(s*s<Dl)
        ub=(a-s)//2
        if x>ub: viol+=1
        if x==ub: tight+=1
        d=random.randint(18,x)      # any admissible lower bound <= x
        if ub < max(d,b//a+1): fired+=1
print(f"in-regime §3 control: {n} instances a/b=1/x+1/y (x in [18,200], y up to 1e40); a^2>4b in {quadcases}; "
      f"x above (a-s)//2: {viol}; quadratic prune fired despite a solution with x>=d: {fired}; bound tight (x==(a-s)//2): {tight}")
