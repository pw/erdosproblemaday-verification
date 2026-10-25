# Print the per-place table (b, b', u, alpha, T_v, (5.14) both sides) for one explicit pair in Q(i).
import sys, math
sys.argv=['x','7','paper']
src=open('/tmp/oaimath/167/checks/scores_toy_qi.py').read().split('# --- unit Gaussian')[0]
exec(src)
def fmt(d): 
    return " + ".join(f"{k}*log{p}" for p,k in sorted(d.items())) or "0"
for (d,dp) in [(G(F(3,5),F(4,5)),G(F(5,13),F(12,13))),(G(F(3,5),F(4,5)),G(F(4,5),F(3,5)))]:
    print("d =",d," d' =",dp," d-d' =",d-dp," 1/d-1/d' =",d.inv()-dp.inv())
    PL=places_for([d,dp,d-dp,d.inv()-dp.inv()])
    sumb=F(0); tot={}; sumbb={}; sumT={}
    for pl in PL:
        w=F(1,2)*pl[4]
        n1=sym_add((-1,logabs_sym(d,pl))); n2=sym_add((-1,logabs_sym(dp,pl)))
        u=sym_add((-1,logabs_sym(d-dp,pl)))
        b,bp=(n1,n2) if sym_val(n1)<=sym_val(n2) else (n2,n1)
        al=sym_add((1,u),(-1,b))
        cv={} if pl[0]=="na" else {2:F(1)}
        T=sym_add((1,al),(1,cv))
        lhs=sym_add((-1,logabs_sym((d-dp)*(d.inv()-dp.inv()),pl)))
        rhs=sym_add((2,al),(-1,bp),(1,b))
        name=f"{pl[1]}|{pl[2]}" if pl[0]=="na" else f"arch {pl[1]}"
        print(f"  {name:14s} wt={w}  b={sym_val(b):+.4f} b'={sym_val(bp):+.4f} u={sym_val(u):+.4f} alpha={sym_val(al):+.4f} T={sym_val(T):+.4f}  (5.14) lhs==rhs: {lhs==rhs}  [{fmt(lhs)}]")
        tot=sym_add((1,tot),(w,lhs)); sumbb=sym_add((1,sumbb),(w,bp),(-w,b)); sumT=sym_add((1,sumT),(w,T))
    print("  Sum* of (5.14) lhs =",fmt(tot),"(product formula: must be 0)")
    print("  Sum*(b'-b) =",fmt(sumbb)," 2 Sum* T_v - 2 log2 =",fmt(sym_add((2,sumT),(-2,{2:F(1)}))),
          " equal:",sumbb==sym_add((2,sumT),(-2,{2:F(1)})))
