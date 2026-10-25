# blocks split at declaration heads (`def NAME`, `'NAME' depends on axioms`, `NAME :`), keyed by head — the v3 shape that was right for #604
import re
a=open("logs/axioms.log").read(); c=open("logs/comparator.log").read()
HEAD=re.compile(r"^(def \S+|'[^']+'|OAI\.QuantitativeVanDerWaerden\.\w+(?= :))", re.M)
def blocks(t):
    ms=list(HEAD.finditer(t)); out={}
    for m,nxt in zip(ms, ms[1:]+[None]):
        seg=t[m.start(): nxt.start() if nxt else len(t)]
        out[m.group(1)]=re.sub(r"\s+"," ",seg).strip()
    return out
A,C=blocks(a),blocks(c)
P="OAI.QuantitativeVanDerWaerden."
keys=[P+"uniform_lower_bound","def "+P+"W","def "+P+"IsRamsey","def "+P+"HasMonoAP","def "+P+"MonoAP"]
res=[]
for k in keys:
    x=A.get(k); y=C.get(k); ok = x is not None and x==y
    res.append(ok); print(k, "MATCH" if ok else "MISMATCH", "| lens", None if x is None else len(x), None if y is None else len(y))
def axset(t,name):
    m=re.search(r"'%s' depends on axioms: \[([^\]]*)\]"%re.escape(name),t)
    return None if not m else set(x.strip().split('.{')[0] for x in m.group(1).split(','))
STD={"propext","Classical.choice","Quot.sound"}
names=("uniform_lower_bound","uniform_lower_bound_floor","exists_uniform_lower_bound","kthRoot_tendsto","length_rate_tendsto","exists_cyclic_coloring")
ax=dict((n,axset(a,P+n)) for n in names)
for n in names: print("axioms",n,ax[n])
allstd=all(v==STD for v in ax.values()); cmp_ax=axset(c,P+"uniform_lower_bound"); cmp_sorry=cmp_ax is not None and "sorryAx" in cmp_ax
v=("MATCH" if all(res) else "MISMATCH")+"\n"+("STD_AXIOMS" if ax["uniform_lower_bound"]==STD else "NONSTD")+"\n"+("CMP_SORRY_SEEN" if cmp_sorry else "CMP_SORRY_NOT_SEEN")+"\n"+("ALL_STD_AXIOMS" if allstd else "SOME_NONSTD")+"\n"
open("statement_match.txt","w").write(v); print(v)
