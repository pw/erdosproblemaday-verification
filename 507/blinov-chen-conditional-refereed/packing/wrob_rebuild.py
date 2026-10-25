# coordinator's independent rebuild of Wroblewski's a(2921) <= 137,693 set ("Theorem 216") from its description; compare to seat W's witness
P=3889; K=sorted(x for x in range(1,P) if pow(x,216,P)==1); assert len(K)==216
A14=[1,2,4,8,9,13,21,23,26,27,30,32,35,36]; c,d=1331,640
Kimg=sorted((c*x+d)%P for x in K)
S=[]
for a in A14[:-1]: S+=[P*(a-1)+y for y in Kimg]
S+=[P*(A14[-1]-1)+y for y in Kimg[:2921-len(S)]]
S=sorted(S); print(len(S), S[0], S[-1])
T=[int(x) for x in open('wroblewski2921.txt').read().split()]
print('equal to packing/wroblewski2921.txt after shifting by -1:', [x-1 for x in S]==T)
