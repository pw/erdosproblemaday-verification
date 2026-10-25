import random, math
random.seed(1)
# 1. Holder: T(L)^3 <= L * (sum (b/L)^{1/2} N_b^2) * (sum (b/L)^{1/4})^2 over dyadic b<=L
viol=0
for trial in range(2000):
    J=random.randint(1,25); L=2**J
    bs=[2**i for i in range(J+1)]
    Nb={b: random.random()*10**random.randint(0,6) for b in bs}
    T=sum(b**(1/3)*Nb[b]**(2/3) for b in bs)
    rhs=L*sum((b/L)**0.5*Nb[b]**2 for b in bs)*sum((b/L)**0.25 for b in bs)**2
    if T**3>rhs*(1+1e-9): viol+=1
print("holder violations",viol)
# negative control: drop the (sum (b/L)^{1/4})^2 factor -> should fail sometimes
neg=0
for trial in range(2000):
    J=random.randint(1,25); L=2**J
    bs=[2**i for i in range(J+1)]
    Nb={b: 1.0 for b in bs}
    T=sum(b**(1/3)*Nb[b]**(2/3) for b in bs)
    rhs=L*sum((b/L)**0.5*Nb[b]**2 for b in bs)
    if T**3>rhs*(1+1e-9): neg+=1
print("holder negative-control failures (expect >0)",neg)
# geometric constant sum (b/L)^{1/4} over dyadic <= 1/(1-2^{-1/4})
print("sum (b/L)^{1/4} bound", 1/(1-2**-0.25), "squared", (1/(1-2**-0.25))**2)
# 2. parabolic lift identity
for _ in range(1000):
    a=random.uniform(-5,5); x1=random.uniform(-5,5); x2=random.uniform(-5,5)
    r2=(x1-a)**2+x2**2
    u=x1; v=x1**2+x2**2
    assert abs((v-2*a*u)-(r2-a*a))<1e-9
print("parabolic lift ok")
# 3. count of points with mult m > D/2 on irreducible plane curve, using sum_{m>=2} m^2 <= 2D(D-1)
mx=0
for D in range(2,500):
    m=D//2+1
    if m<2: continue
    if D==2: continue  # irreducible conic: no singular points
    cnt=(2*D*(D-1))//(m*m)
    mx=max(mx,cnt)
print("max count via (4.3) for D in [3,500):",mx)
# using genus/polar bound sum m(m-1) <= D(D-1) directly
mx2=0
for D in range(3,500):
    m=D//2+1
    mx2=max(mx2,(D*(D-1))//(m*(m-1)))
print("max count via m(m-1) form:",mx2)
# 4. (5.4) exponent and threshold sums
for s in [1e3,1e6,1e12,1e30]:
    G=1+math.isqrt(int(max(1,math.log(s))))  # O(1+sqrt log s)
    K=4*G
    a=[0]*(K+1)
    a[K]=s**0.1
    for i in range(K-1,0,-1): a[i]=10*a[i+1]
    ok=all(sum(a[r] for r in range(i+1,K+1)) < a[i]/9 for i in range(1,K))
    print(f"s={s:.0e} K={K} a1={a[1]:.3e} s^(1/3)={s**(1/3):.3e} tail<a_i/9: {ok}  -1/2+1/9={-0.5+1/9:.4f} vs -7/18={-7/18:.4f}")
