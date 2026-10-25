# v3 (as run 15:3xZ; the one that is right): blocks split at declaration heads — `def NAME`, `'NAME' depends on axioms`, or
# `NAME :` — and keyed by the head itself. v1 (inside build.sh) split at blank lines, which the solution log lacks between the
# extra probes, so every solution block ran on into the next (prefix-equal, longer by exactly the next block) → MISMATCH.
import re
a=open("logs/axioms.log").read(); c=open("logs/comparator.log").read()
HEAD=re.compile(r"^(def \S+|'[^']+'|OAI\.WeakPinned\.\w+(?= :))", re.M)
def blocks(t):
    ms=list(HEAD.finditer(t)); out={}
    for m,nxt in zip(ms, ms[1:]+[None]):
        seg=t[m.start(): nxt.start() if nxt else len(t)]
        out[m.group(1)]=re.sub(r"\s+"," ",seg).strip()
    return out
A,C=blocks(a),blocks(c)
keys=["OAI.WeakPinned.main","def OAI.WeakPinned.F","def OAI.WeakPinned.pairFraction","def OAI.WeakPinned.richPairs","def OAI.WeakPinned.k","def OAI.WeakPinned.distanceFiber"]
res=[]
for k in keys:
    x=A.get(k); y=C.get(k); ok = x is not None and x==y
    res.append(ok); print(k, "MATCH" if ok else "MISMATCH", "| lens", None if x is None else len(x), None if y is None else len(y))
def axset(t,name):
    m=re.search(r"'%s' depends on axioms: \[([^\]]*)\]"%re.escape(name),t)
    return None if not m else set(x.strip().split('.{')[0] for x in m.group(1).split(','))
STD={"propext","Classical.choice","Quot.sound"}
ax=dict((n,axset(a,"OAI.WeakPinned."+n)) for n in ("main","pins","pinsStatement","exists_pin_eventually"))
allstd=all(v==STD for v in ax.values()); cmp_sorry="sorryAx" in axset(c,"OAI.WeakPinned.main")
v=("MATCH" if all(res) else "MISMATCH")+"\n"+("STD_AXIOMS" if ax["main"]==STD else "NONSTD")+"\n"+("CMP_SORRY_SEEN" if cmp_sorry else "CMP_SORRY_NOT_SEEN")+"\n"+("PIN_STD_AXIOMS" if allstd else "PIN_NONSTD")+"\n"
print(v)
