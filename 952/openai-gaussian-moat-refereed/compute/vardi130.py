# Largest component of Gaussian integers coprime to 130 = 2*5*13 (i.e. not divisible by 1+i, 2+-i, 3+-2i),
# step <= sqrt(2) (8-neighbourhood), compared with Vardi 1998 Sec.7 ("largest connected component has 580 elements")
# and with our compute/scan_R1.log (A({5,13}), step 1, max_component=580).
from collections import deque
def coprime130(x,y):
    if (x+y)%2==0: return False          # divisible by 1+i
    for p,r in ((5,2),(13,5)):            # r^2 = -1 mod p
        if (x+r*y)%p==0 or (x-r*y)%p==0: return False
    return True
def coprimeA(x,y):                        # A({5,13}) of the paper
    for p,r in ((5,2),(13,5)):
        if (x+r*y)%p==0 or (x-r*y)%p==0: return False
    return True
def largest(pred, steps, Q):
    seen=set(); best=0; inf=False
    for x0 in range(Q):
        for y0 in range(Q):
            if not pred(x0,y0) or (x0,y0) in seen: continue
            comp={(x0,y0)}; dq=deque([(x0,y0)])
            while dq:
                X,Y=dq.popleft()
                for a,b in steps:
                    w=(X+a,Y+b)
                    if w in comp or not pred(*w): continue
                    comp.add(w); dq.append(w)
                    if len(comp)>4*Q*Q: inf=True; break
                if inf: break
            if inf: return 'INFINITE'
            seen|={(x%Q,y%Q) for x,y in comp}; best=max(best,len(comp))
    return best
s8=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if (a,b)!=(0,0)]
s4=[(1,0),(-1,0),(0,1),(0,-1)]
print('coprime to 130, step<=sqrt2: largest component =', largest(coprime130,s8,130))
print('A({5,13}), step<=1: largest component =', largest(coprimeA,s4,65))
