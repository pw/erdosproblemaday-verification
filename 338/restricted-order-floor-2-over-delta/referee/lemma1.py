# Independent exhaustive check of Lemma 1 in Z/g (g<=11): 0 in S, <S> = Z/g, Z nonempty, Z+S != Z/g
#  => |Z+S| - |Z| >= ceil(|S|/2). Also: is ceil(|S|/2) attained (lemma tight)? And controls.
import sys
def run(g):
    full=(1<<g)-1
    rot=lambda x,k: ((x<<k)|(x>>(g-k)))&full if k else x
    def sumset(Z,S):
        r=0
        for k in range(g):
            if S>>k&1: r|=rot(Z,k)
        return r
    def gen(S):
        c=1
        while True:
            n=c|sumset(c,S)
            if n==c: return c==full
            c=n
    viol=0; tight=set(); ctrl=0; minslack=99
    for S in range(1,full+1,2):
        s=bin(S).count('1'); G=gen(S)
        for Z in range(1,full+1):
            ZS=sumset(Z,S)
            if ZS==full: continue
            gr=bin(ZS).count('1')-bin(Z).count('1')
            need=(s+1)//2
            if G:
                if gr<need: viol+=1
                if gr==need: tight.add(s)
            elif gr<need: ctrl+=1
    return viol,sorted(tight),ctrl
for g in range(1,int(sys.argv[1])+1):
    v,t,c=run(g); print(f"g={g} violations={v} |S| values where growth=ceil(|S|/2) is attained={t} control(non-generating) violations={c}")
