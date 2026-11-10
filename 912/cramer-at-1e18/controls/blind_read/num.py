import math
from mpmath import mp, quad, exp, log, sqrt, pi, euler, inf
mp.dps=30
g=float(euler)
# Bernstein
for tag,t,sd in [("1e15",348987.1,1959.74),("1e16",1026993.9,3451.81),("1e17",3038563.5,6082.01),("1e18",9000142.1,10719.91)]:
    v=sd*sd; ex=t*t/(2*(v+t/3)); print(tag,"Bernstein log10 P <=", -ex/math.log(10))
# pair asymptotic constant
A=0.5*(2-g-math.log(2*math.pi))
print("D coeff A/2 =",A)
I0=quad(lambda t: (2/t**2)*exp(-2/t**2),[0,1,inf]); print("int 2/t^2 e^-2/t^2 =",I0, "sqrt(pi/2)=",sqrt(pi/2))
I1=quad(lambda t: (2/t**2)*exp(-2/t**2)*(-2*log(t)),[0,1,inf]); print("const from -2log t:", I1/I0, " -(g+log8)=", -(g+math.log(8)))
c = -2*A + float(I1/I0)
print("constant in (loglog n + c):", c, " = -(2 - log(pi/4)) ->", -(2-math.log(math.pi/4)))
print("(g+log2pi-1)/2 =", (g+math.log(2*math.pi)-1)/2)
print("1+g+log8 =", 1+g+math.log(8))
for e in (12,15,16,17,18):
    L=e*math.log(10); LL=math.log(L)
    print(e, "GI 2nd+3rd coeff (x log n):", (-LL+1+g+math.log(8))/2, " loglog n=",LL)
print("crossover n = 10^", math.exp(1+g+math.log(8))/math.log(10))
# data coefficients
s2p=math.sqrt(2*math.pi)
data={12:2.591407,15:2.571663,16:2.566861,17:2.562793,18:2.559085}
for e,r in data.items():
    L=e*math.log(10); print(e,"data coeff", (r/s2p-1)*L)
# pair-corrected finite-n model coefficient
rows={15:(2.506873,283973.2,5380795.988,1951957,0.06486),16:(2.504571,845454.0,16475255.725,0,0),17:(2.502695,2524290.0,50543777.292,0,0),18:(2.501154,7556372.9,155330200.595,0,0)}
for e,(ec,pair,scale,_,__) in rows.items():
    L=e*math.log(10); m=ec+pair/scale; print(e,"Cramer+pair ratio",m," coeff",(m/s2p-1)*L)
# gap as % of L and of mean, sd as % of L
for e,(gap,sd,scale,Eh) in {15:(348987.1,1959.74,5380795.988,2.506873),18:(9000142.1,10719.91,155330200.595,2.501154)}.items():
    print(e,"gap/L=",gap/scale," gap/E[h]=",gap/(Eh*scale)," sd/L=",sd/scale)
# calibrated shares with z=5 and z=19
for e,(sh,F19,F5) in {15:(0.8137,1.2136,1.1788),16:(0.8232,1.2010,1.1675),17:(0.8308,1.1897,1.1574),18:(0.8396,1.1796,1.1485)}.items():
    print(e,"calib z19",sh*F19," z5",sh*F5)
# small primes / L
for e,pis,scale in [(9,3401,math.sqrt(1e9/math.log(1e9))),(17,17082666,50543777.292)]:
    print(e,"pi(sqrt n)/L",pis/scale," 2/sqrt(log n)",2/math.sqrt(e*math.log(10)))
