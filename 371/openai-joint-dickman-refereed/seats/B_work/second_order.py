import math
g=0.5772156649015329; X=1e10; L=math.log(X)
# li(X) by Ramanujan series
def li(x):
    lx=math.log(x); s=0.0; term=1.0; inner=0.0
    for nn in range(1,200):
        term*=lx/nn
        inner+= 1.0/(2*((nn-1)//2)+1) if True else 0
        s+=((-1)**(nn-1))*term/(2**(nn-1))*sum(1.0/(2*k+1) for k in range((nn-1)//2+1))
    return g+math.log(lx)+math.sqrt(x)*s
liX=li(X)
for a,ru,ru1 in [(0.5,1-math.log(2),1.0),(0.7,1-math.log(1/0.7),1.0)]:
    pt=ru-g*ru1/L; av_li=ru-g*ru1*liX/X; av_m1=ru-g*ru1/(L-1)
    print(f"a={a}: rho(1/a)={ru:.6f} pointwise@X={pt:.4f} avg(li)={av_li:.4f} avg(1/(logX-1))={av_m1:.4f}")
print("li(1e10)=",liX)
