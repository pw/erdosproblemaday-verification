import lab
from fractions import Fraction
def F(x): return Fraction(x)
fails=0
def chk(c,msg):
    global fails
    print(("  PASS " if c else "  FAIL ")+msg)
    if not c: fails+=1

print("== V1 indexing identities (1)&(4) ==")
a=F('809/500'); t=F('5/2')
# (1): floor((t/a)*a^n, n>=1) == floor(t*a^(n-1)), n>=1  i.e. 1-idx at t/a == 0-idx at t
lhs=[lab.floors(t/a, a, n_terms=8, start=1)[i] for i in range(8)]
rhs=lab.floors(t, a, n_terms=8, start=0)
chk(lhs==rhs, "identity (1): A0(t)==S1(t/alpha)  %s==%s"%(lhs,rhs))
# (4): 0-idx terms == [floor(t)] ++ 1-idx-at-same-t terms
one_idx_same=lab.floors(t, a, n_terms=7, start=1)
chk([int(t)]+one_idx_same == lab.floors(t,a,n_terms=8,start=0), "identity (4): A0(t)={floor(t)}++S1(t)")

print("== V6 exact separation (13/8, 3/2): 0-idx entire, 1-idx incomplete ==")
a=F('13/8'); t=F('3/2')
b=min(F(3)/(a*a), F(5)/(a*a*a))
chk(b==F('192/169'), "b(13/8)=192/169 (=%s)"%b)
chk(F('3/2')>b, "1-idx u=3/2 > b => incomplete expected")
chk(F('3/2')/a==F('12/13') and F('12/13')<b, "0-idx reindex u=12/13 < b => complete expected")
e0=lab.entire_cert_0indexed(t,a)
chk(e0['proven'], "0-idx (13/8,3/2) entirely complete (proven)")
g1=lab.greedy_entire(t,a,n_terms=30,start=1)
chk(not g1['entire'], "1-idx (13/8,3/2) NOT entire (gap@%s)"%g1.get('gap_at'))

print("== V4 lag-2 erosion 4528->150 at (809/500, 5/2) : R0 == R | (R<<2) ==")
a=F('809/500'); t=F('5/2'); cap=3_000_000
terms1=lab.floors(t, a, n_terms=46, start=1)         # 1-indexed at u=2.5
R=lab.subsetsum_bits(terms1, cap)
R0=lab.subsetsum_bits([int(t)]+terms1, cap)           # 0-indexed at t=2.5
mask=((1<<(cap+1))-1)
chk((R0 & mask)==((R | (R<<2)) & mask), "R0 == R | (R<<2) on [0,%d] (exact erosion identity)"%cap)
# exception counts in [1, 2_900_000]
hi=2_900_000
mh=((1<<(hi+1))-1)>>1
G_count = hi - (R & mh).bit_count()
Gp_count= hi - (R0 & mh).bit_count()
print("    |G| (1-idx exceptions <=2.9M)=%d  |G'| (0-idx exceptions <=2.9M)=%d"%(G_count,Gp_count))
chk(G_count==4528, "|G|==4528")
chk(Gp_count==150, "|G'|==150")

print("== V5 permanent-gap mechanism: alpha=17/10 (my observed point) + ratio at 171/100 ==")
def mk_gaps(alpha, tval, nterms=44):
    aa=lab.floors(tval, alpha, n_terms=nterms, start=0)
    M=[1]
    k=1
    while 2*k < len(aa):
        M.append(M[-1]+aa[2*k]); k+=1
    return aa, M
a17=F('17/10'); a17seq, M17 = mk_gaps(a17, F(2))
cap17=50_000_000
bits17=lab.subsetsum_bits(a17seq, cap17)
miss17=[m for m in M17 if m<=cap17 and not ((bits17>>m)&1)]
print("    alpha=1.7: M_k<=50M = %d ; of those MISSING from subset sums = %d"%(len([m for m in M17 if m<=cap17]), len(miss17)))
chk(len(miss17)==len([m for m in M17 if m<=cap17]), "every formula M_k <=50M is a real gap at alpha=1.7")
chk(42597428 in M17, "my observed L=42597428 is one of the forced M_k at alpha=1.7")
a171=F('171/100'); a171seq, M171 = mk_gaps(a171, F(2))
print("    alpha=1.71 first M_k:", M171[:8])
chk(M171[:6]==[1,6,23,73,219,646], "alpha=1.71 M_k prefix matches Pro (1,6,23,73,219,646)")
chk(253899772 in M171 and 742428345 in M171, "boxed gaps 253899772,742428345 in M_k list")
ratios=[round(M171[i+1]/M171[i],4) for i in range(8,14)]
print("    alpha=1.71 M_{k+1}/M_k (should -> 2.9241):", ratios)
chk(all(2.9< r <2.95 for r in ratios), "ratios converge to alpha^2=2.9241")

print("== V2 Lemma-5 certificate 1-idx (9/2, 809/500) -> 0-idx 7281/1000 cofinite ==")
a=F('809/500'); u=F('9/2')
s=lab.floors(u, a, n_terms=36, start=1)
chk(s[35]==150120200, "s_36==150120200 (got %d)"%s[35])
chk(sum(s[:35])==242912917, "sum s_1..s_35==242912917 (got %d)"%sum(s[:35]))
cap2=207472253
bits2=lab.subsetsum_bits(s[:35], cap2)
lo,hi2=35440664,207472253
length=hi2-lo+1
have=(bits2>>lo) & ((1<<length)-1)
chk(have==((1<<length)-1), "subset sums contain full interval [35440664,207472253], length %d > s_36"%length)
print("    => via identity (1), 0-idx t=7281/1000 (=alpha*9/2) is cofinite; t1^(0)(809/500)>=7.281 vs t0=1500/809=%.5f"%(1500/809))

print()
print("RESULT:", "ALL GOOD" if fails==0 else "%d FAILURE(S)"%fails)
import sys; sys.exit(1 if fails else 0)
