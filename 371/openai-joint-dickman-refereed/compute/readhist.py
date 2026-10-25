import numpy as np, sys
f=open(sys.argv[1],'rb'); nd=np.frombuffer(f.read(4),dtype=np.int32)[0]; decs=np.frombuffer(f.read(8*nd),dtype=np.uint64)
H=np.frombuffer(f.read(),dtype=np.uint64).reshape(nd,101,101).astype(np.int64)
C=np.cumsum(H,axis=0)  # cumulative over decades: C[d] = counts for 2<=n<=decs[d]
def joint(d,A,B): # #{u<=A, v<=B} with bins k=ceil(100u)
    i=int(round(100*A)); j=int(round(100*B)); return int(C[d,:i+1,:j+1].sum())
if __name__=='__main__':
    X=int(sys.argv[2]); d=list(decs).index(X)
    for A in (0.2,0.3,0.5,0.7):
        for B in (0.2,0.3,0.5,0.7): print(f"HIST X={X} a={A} b={B} count={joint(d,A,B)}")
