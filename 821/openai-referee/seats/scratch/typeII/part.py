# Simulate the slot allocation of Section 6.3 with Section 7 constants; check
# 0 <= log E - log e <= (c2+1) s_jx whenever log E <= sum of prime-slot logs,
# under random AND adversarial choices on the transition region 0<gamma<1.
import random, math
random.seed(1)
lam=2.0; c1=1.0; c2=1.2; r0=6
sp=1.0/(r0*(c1+c2))
worst=0.0; maxratio=0.0; viol=0
for trial in range(4000):
  L=random.choice([1e4,1e5,1e6,1e8])
  T=math.log(L)
  s=lambda j: sp*L*lam**(-j)
  jx=0
  while c1*s(jx+1)>=20*T: jx+=1
  jss=random.randint(0,min(jx,6))
  slots=[]
  for j in range(jx+1):
    for r in range(r0):
      if j==jss and r==random.randint(0,r0-1) and not any(js==j and ex for (js,_,ex) in slots):
        slots.append((j,None,True)); continue
      slots.append((j,random.uniform(c1*s(j),c2*s(j)),False))
  prime=[(j,v) for (j,v,ex) in slots if not ex]
  tot=sum(v for j,v in prime)
  mode=trial%3
  logE=random.uniform(0.0,tot) if trial%2 else tot*random.uniform(0.95,1.0)
  R=logE
  for idx,(j,v) in enumerate(prime):
    t=(R-v)/s(j)
    maxratio=max(maxratio,R/s(j))
    if t>=1: take=True
    elif t<=0: take=False
    else:
      take = (random.random()<0.5) if mode==0 else (mode==1)  # random / always take / always skip
    if take:
      assert R>v
      R-=v
    # induction target
    rem=sum(vv for (jj,vv) in prime[idx+1:])
    if not (0<=R<=rem+(c2+1)*s(jx)+1e-9): viol+=1
  worst=max(worst,R/((c2+1)*s(jx)))
print("violations",viol,"max (logE-loge)/((c2+1)s_jx)",round(worst,4),"max R_i/s_j(i)",round(maxratio,3))
print("bound r0*c2*lam/(lam-1)+c2+1 =",r0*c2*lam/(lam-1)+c2+1)
