import math, random
random.seed(1)
J=[[0,-1],[1,0]]
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mv(A,v): return [A[0][0]*v[0]+A[0][1]*v[1], A[1][0]*v[0]+A[1][1]*v[1]]
def add(A,B,s=1): return [[A[i][j]+s*B[i][j] for j in range(2)] for i in range(2)]
I=[[1,0],[0,1]]
def sc(a,A): return [[a*A[i][j] for j in range(2)] for i in range(2)]
def inv(A):
    d=A[0][0]*A[1][1]-A[0][1]*A[1][0]; return [[A[1][1]/d,-A[0][1]/d],[-A[1][0]/d,A[0][0]/d]]
# 1. (tI+J)(I+tJ) = (1+t^2) J
for _ in range(3):
    t=random.uniform(-5,5)
    L=mm(add(sc(t,I),J),add(I,sc(t,J))); R=sc(1+t*t,J)
    print('id1', max(abs(L[i][j]-R[i][j]) for i in range(2) for j in range(2)))
# 2. Cayley line: c=(x-y)/2 - tJ(x+y)/2  <=> y = (I+tJ)^{-1}((I-tJ)x - 2c) and the map is a rotation
for _ in range(3):
    t=random.uniform(-5,5); x=[random.gauss(0,1) for _ in range(2)]; y=[random.gauss(0,1) for _ in range(2)]
    s=[x[0]+y[0],x[1]+y[1]]; Js=mv(J,s)
    c=[(x[0]-y[0])/2 - t*Js[0]/2, (x[1]-y[1])/2 - t*Js[1]/2]
    Z=sc(t,J); Rm=mm(inv(add(I,Z)),add(I,Z,-1))
    y2=mv(inv(add(I,Z)), [v-2*w for v,w in zip(mv(add(I,Z,-1),x),c)])
    RtR=mm([[Rm[0][0],Rm[1][0]],[Rm[0][1],Rm[1][1]]],Rm); det=Rm[0][0]*Rm[1][1]-Rm[0][1]*Rm[1][0]
    print('cayley', max(abs(a-b) for a,b in zip(y,y2)), 'orth', abs(RtR[0][0]-1)+abs(RtR[0][1])+abs(RtR[1][1]-1), 'det', round(det,12))
# 3. W_x tangency: along line for fixed x,y, dc/dt = -J(x+y)/2 equals (tI+J)(c-x)/(1+t^2)
for _ in range(3):
    t=random.uniform(-5,5); x=[random.gauss(0,1) for _ in range(2)]; y=[random.gauss(0,1) for _ in range(2)]
    s=[x[0]+y[0],x[1]+y[1]]; Js=mv(J,s)
    c=[(x[0]-y[0])/2 - t*Js[0]/2, (x[1]-y[1])/2 - t*Js[1]/2]
    w=mv(add(sc(t,I),J),[c[0]-x[0],c[1]-x[1]]); w=[v/(1+t*t) for v in w]
    print('Wx', max(abs(a-b) for a,b in zip(w,[-Js[0]/2,-Js[1]/2])))
# 4. constants
print('GK-induction factor', (20/9)*(1/100)*(10/9)**3)
print('B.10: 36864*4 =',36864*4, ' 18*2048 =',18*2048, ' 16*128=',16*128)
print('B.10: max m e^{-2 sqrt m} over m>=1:', max(m*math.exp(-2*math.sqrt(m)) for m in range(1,10**5)), 'e^-2=',math.exp(-2))
print('B.10: tail exponent log2/2-1/2 =', math.log(2)/2-0.5, ' vs -1/8')
worst=max((math.ceil(math.sqrt(6*q)))/math.sqrt(q) for q in range(1,10**6)); print('B.10: max D/sqrt(q) =',worst,'(claim <4)')
print('B.7 deg R: 3(3d-4)+2(4d-6) =', [3*(3*d-4)+2*(4*d-6) for d in range(3,7)], ' 17d-24 =',[17*d-24 for d in range(3,7)])
print('B.10 final: 6*8 + 1/2 =',6*8+0.5,' (<=49)  ; (1/4)^1.5 =',0.25**1.5)
