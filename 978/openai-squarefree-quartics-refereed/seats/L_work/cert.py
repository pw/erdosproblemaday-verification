# Independent exact re-check of the Lean's quartic (QuarticComponents) and medium-degree (CurveThresholds) certificates.
from fractions import Fraction as F
from math import factorial
def A(j): return 101+j
def B(j): return 200-2*j
def num(j,h):
    if j<60: return 206 if h<=2 else (200 if h==3 else 191)
    return 252 if h==1 else (206 if h==2 else 175)
bad=[]; minmargin={}
for j in range(100):
    a,b=A(j),B(j)
    # full (h=5)
    if not a**4*b**4*1000**5 <= (2*a+b)**3*400**5*num(j,5)**5: bad.append(('full',j))
    for h in (3,4):
        if not a**h*b**h*1000**h <= min(a,b)*(2*a+b)**(h-1)*400**h*num(j,h)**h: bad.append(('gen',h,j))
    if not a**2*b**2*1000**2 <= min(2*a,b)*(2*a+b)*400**2*num(j,2)**2: bad.append(('aff',j))
    if not a*b**2*1000**2 <= (b+4*a)*400**2*num(j,2)**2: bad.append(('pole',j))
    U,V=F(a,400),F(b,400); e1=F(num(j,1),1000)
    if not 1/e1 <= min(2/U, max(1/U, 3/V)): bad.append(('curve',j))
    env=[None]+[F(num(j,h),1000) for h in range(1,6)]
    stage=[env[5-i] for i in range(5)]
    inc=[stage[0]]+[stage[i]-env[6-i] for i in range(1,5)]
    assert all(x>=0 for x in inc)
    s=sum((5-i)*inc[i] for i in range(5))+F(1,1000)
    if s>F(997,1000): bad.append(('sum',j,s))
    # tightness of full threshold: exact delta_5 vs envelope
    d5=float((U**4*V**4/(2*U+V)**3))**(1/5)
    minmargin[j]=float(env[5])-d5
# also check eta binning identities: U = eta_+/4, V = 1 - eta_-/2
for j in range(100):
    assert F(A(j),400)==(1+F(j+1,100))/4 and F(B(j),400)==1-(1+F(j,100))/2
print("quartic certificate failures:",bad)
jm=min(minmargin,key=minmargin.get); print("tightest full-threshold margin at j=%d: %.5f"%(jm,minmargin[jm]))
# medium degree d=5..8, U=1/3, V=2/5
def envm(d,h):
    if d==5: return F(196,1000) if h<=2 else (F(154,1000) if h==3 else F(150,1000))
    if d==6: return F(176,1000) if h<=2 else (F(134,1000) if h==3 else F(121,1000))
    if d==7: return {1:F(167,1000),2:F(161,1000),3:F(119,1000),4:F(102,1000)}.get(h,F(100,1000))
    return {1:F(167,1000),2:F(150,1000),3:F(108,1000),4:F(92,1000)}.get(h,F(85,1000))
U,V=F(1,3),F(2,5)
for d in range(5,9):
    k=d-2; ok=True
    for h in range(2,d+1):
        ok &= 1 <= 5*(k*5+6)**(h-1)*F(15)**h/(5**h*6**h)*envm(d,h)**h
    ok &= 1 <= F(k*5+6)**(d-1)*F(15)**(d+1)/(5**d*6**d)*envm(d,d+1)**(d+1)
    ok &= 1 <= 6*envm(d,1)
    stage=[envm(d,d+1-i) for i in range(d+1)]
    inc=[stage[0]]+[stage[i]-envm(d,d+2-i) for i in range(1,d+1)]
    s=sum((d+1-i)*inc[i] for i in range(d+1))+F(1,1000)
    full=float(U**d*V**d/(k*U+V)**(d-1))**(1/(d+1))
    print(f"d={d}: thresholds ok={ok}, exponent+1/1000={float(s):.4f} (<=0.997: {s<=F(997,1000)}), exact delta_full={full:.4f} vs env {float(envm(d,d+1))}")
# medium box check: U=eta/d <= 1/k <= 1/3, V = 1 - k*eta/d <= 2/d <= 2/5 for eta>=1
