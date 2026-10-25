from fractions import Fraction as F
U,V=F(1,3),F(2,5)
env={5:F(150,1000),6:F(121,1000),7:F(100,1000),8:F(85,1000)}
for d in range(5,9):
    k=d-2
    full=float(U**d*V**d/(k*U+V)**(d-1))**(1/(d+1))
    print(d, 'full threshold', full, 'env', float(env[d]), 'margin', float(env[d])-full)
