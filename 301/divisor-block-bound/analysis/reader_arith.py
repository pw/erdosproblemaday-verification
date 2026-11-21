from fractions import Fraction as F
iv=[(36,42,1,F(1,252)),(55,77,1,F(2,385)),(77,80,2,F(3,3080)),(80,84,1,F(1,1680)),(84,90,2,F(1,630)),(90,105,1,F(1,630))]
tot=F(0)
for x,y,inc,w in iv:
    calc=inc*(F(1,x)-F(1,y)); print(f"[{x},{y}) inc {inc}: stated {w}, recomputed {calc}, {'OK' if calc==w else 'DIFF'}"); tot+=calc
print("total", tot, "stated 257/18480:", tot==F(257,18480))
W5=F(3907,5040); W55=F(12,11)*W5+tot; print("W55440 =", W55, "stated 1059/1232:", W55==F(1059,1232))
W72=F(14,13)*W55+(F(1,65)-F(1,66)); print("1/65-1/66 =", F(1,65)-F(1,66), "W720720 =", W72, "stated 15889/17160:", W72==F(15889,17160))
d72=F(55,248); C3=1-d72*W72; print("C3 =", C3, "stated 61487/77376:", C3==F(61487,77376), float(C3))
prev=F(92413,116064); print("improvement", prev-C3, "stated 121717/77376000:", prev-C3==F(121717,77376000))
# delta check
def delta(M):
    r=F(1); m=M; p=2
    while m>1:
        if m%p==0:
            e=0
            while m%p==0: m//=p; e+=1
            r*=F(p-1,p)/(1-F(1,p**(e+1)))
        p+=1
    return r
for M in (5040,55440,720720): print(M, delta(M))
print("prev bound as delta55440*W:", 1-prev, "=> W55440 =", (1-prev)/delta(55440))
