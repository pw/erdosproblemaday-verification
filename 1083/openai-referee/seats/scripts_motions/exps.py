from fractions import Fraction as F
a=F(1,14)
# N exponents: A=N^(2/3). b = beta*A*t^-a ; r=t^(1+a); m=8N/r ; k=tA
# (7.17) b/m^(2/3) exponent of t:
print("7.17 t-exp", -a + F(2,3)*(1+a), "claimed", F(9,14))
# (7.18) q/sqrt N = eta beta N^(2/3-1/2) t^-a ; with N^(1/6)>=t^(1/2): t^(1/2-a)
print("7.18", F(2,3)-F(1,2), F(1,2)-a, "claimed 1/6, 3/7")
# (7.19) k r^2 m^3 / sqrt(b): N-exp and t-exp, A=N^(2/3)
Nexp = F(2,3) + 3 - F(1,2)*F(2,3); texp = 1 + 2*(1+a) - 3*(1+a) - F(1,2)*(-a)
print("7.19 N-exp",Nexp,"(N^4/A =",4-F(2,3),") t-exp",texp,"claimed",-a/2, -F(1,28))
# (7.24) A^2 (N/b)^4: N/b = N^(1/3) t^a
print("7.24 N",2*F(2,3)+4*F(1,3),"t",4*a,"claimed 8/3, 2/7")
print("7.25 N",3*F(2,3)+F(7,2)*F(1,3),"t",F(7,2)*a,"claimed 19/6, 1/4")
print("sums at t=N^(1/3):",F(8,3)+F(1,3)*4*a, F(19,6)+F(1,3)*F(7,2)*a, "claimed 58/21, 13/4; target",F(10,3))
print("savings",F(10,3)-F(58,21),F(10,3)-F(13,4))
print("b >= beta N^?:",F(2,3)-a*F(1,3),"claimed 9/14")
print("r<=N needs (1+a)/3<=1:",(1+a)/3)
# local Lemma 7.4 threshold: D ~ m/sqrt(l) < eps l  <=> l^(3/2) > m
# planar: m^4/l^3 <= m^3/l^(3/2) <=> l >= m^(2/3)
