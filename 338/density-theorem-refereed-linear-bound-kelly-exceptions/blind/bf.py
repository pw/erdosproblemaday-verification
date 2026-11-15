import sys, time
N=int(sys.argv[1])
def inX(a):
    while a:
        if a%3==2: return False
        a//=3
    return True
A=sorted(set([2*a+1 for a in range(N//2+1) if inX(a) and 2*a+1<=N]+[4*a for a in range(1,N//4+1) if inX(a)]))
if len(sys.argv)>2: A.remove(int(sys.argv[2]))
print("first",A[:15],"size",len(A))
mask=(1<<(N+1))-1
S1=0;S2=0;S3=0;S4=0
T1=0;T2=0;T3=0;T4=0
t=time.time()
for c in A:
    # sums whose largest member is c
    S4|=(S3<<c)&mask
    S3|=(S2<<c)&mask
    S2|=(S1<<c)&mask
    S1|=1<<c
upto3=S1|S2|S3
upto4=upto3|S4
# order 2 with repeats
R2=S1
for c in A:
    R2|=(S1<<c)&mask
def miss(B):
    st=bin(B|(1<<(N+1)))[3:][::-1]  # index n -> bit n
    return [n for n in range(1,N+1) if st[n]=='0']
m3=miss(upto3); m4=miss(upto4); r2=miss(R2)
print("not <=3 distinct:",m3)
print("not <=4 distinct:",m4)
print("not <=2 with repeats:",r2)
print("time",time.time()-t)
