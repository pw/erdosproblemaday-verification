import sys, collections
from sympy import isprime, factorint
rows=[]
for line in open(sys.argv[1]):
    if '|' not in line: continue
    head,tail=line.split('|'); h=head.split()
    N,m,L,mx,R,nt=map(int,h[:6]); tail=[int(x) for x in tail.strip().split(',') if x]
    rows.append((N,m,L,mx,R,nt,tail))
rows.sort()
for fam in (1,2):
    rs=[r for r in rows if r[1]==fam]
    Ns=[r[0] for r in rs]
    print(f"== family 3/({fam}*N!-1): {len(rs)} values of N, N in [{min(Ns)},{max(Ns)}]")
    assert all(r[5]==r[2] for r in rs), "trace length != reported length"
    print("  all terminate:", all(r[2]>0 for r in rs), "| all lengths odd:", all(r[2]%2==1 for r in rs))
    print("  Brown's lower bound L >= N-2 holds for all:", all(r[2]>=r[0]-2 for r in rs))
    over=[r[4]-r[0] for r in rs]; tailL=[r[2]-(r[4]-2) for r in rs]   # ramp 3..R has R-2 numerators
    big=[r for r in rs if r[0]>=100]
    print("  overshoot R-N (N>=100): min",min(r[4]-r[0] for r in big),"max",max(r[4]-r[0] for r in big),
          "mean %.2f"%(sum(r[4]-r[0] for r in big)/len(big)))
    print("  worst overshoots:", sorted(((r[4]-r[0],r[0]) for r in rs), reverse=True)[:6])
    print("  numerators after the ramp ends: max count", max(tailL), "at", [r[0] for r in rs if r[2]-(r[4]-2)==max(tailL)][:5])
    print("  max numerator anywhere:", max(r[3] for r in rs), "vs N+? : max(maxnum-N) =", max(r[3]-r[0] for r in rs))
    cls=collections.Counter()
    for N,m_,L,mx,R,nt,tail in rs:
        c=R+1
        if tail==[1]: k='terminates at R+1 (prime)' if isprime(c) else 'terminates at R+1 (composite)'
        elif isprime(c): k='breaks at prime R+1, then a short tail'
        else: k='breaks at composite R+1 (=%s-type), then a short tail'%('p*k' )
        cls[k]+=1
    for k,v in cls.most_common(): print("   ",v,k)
    # where does the ramp end relative to the first prime above N?
    from sympy import nextprime
    firstp=collections.Counter()
    for N,m_,L,mx,R,nt,tail in big:
        p=nextprime(N); firstp['ends before first prime >N' if R+1<p else ('ends AT first prime >N' if R+1==p else 'passes first prime >N')]+=1
    print("   (N>=100)", dict(firstp))
