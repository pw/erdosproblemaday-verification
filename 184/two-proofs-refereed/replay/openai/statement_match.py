# Compare the pp.all printouts of the COMPARATOR module (statement with `sorry`) against the SOLUTION module (Main.lean):
# the theorem's type and the three definitions it unfolds through. Heads normalised (leading @ dropped; .{u} on defs dropped).
# Verdict lines: MATCH/MISMATCH · STD_AXIOMS/NONSTD (solution) · CMP_SORRY_SEEN/NOT_SEEN (comparator must depend on sorryAx).
import re,sys
a=open("logs/axioms.log").read(); c=open("logs/comparator.log").read()
HEAD=re.compile(r"^(def \S+|'[^']+'|@?OAI\.ErdosGallai\.\w+(?= :))", re.M)
def norm(h):
    h=h.lstrip('@')
    if h.startswith('def '): h=re.sub(r"\.\{[^}]*\}$","",h)
    return h
def blocks(t):
    ms=list(HEAD.finditer(t)); out={}
    for m,nxt in zip(ms, ms[1:]+[None]):
        seg=t[m.start(): nxt.start() if nxt else len(t)]
        out[norm(m.group(1))]=re.sub(r"\s+"," ",seg.lstrip('@')).strip()
    return out
A,C=blocks(a),blocks(c)
P="OAI.ErdosGallai."
keys=[P+"erdos_gallai","def "+P+"MainStatement","def "+P+"EdgeDecomposition","def "+P+"CycleOrSingleEdge"]
res=[]
for k in keys:
    x=A.get(k); y=C.get(k); ok = x is not None and x==y
    res.append(ok); print(k, "MATCH" if ok else "MISMATCH", "| lens", None if x is None else len(x), None if y is None else len(y))
def axset(t,name):
    m=re.search(r"'%s' depends on axioms: \[([^\]]*)\]"%re.escape(name),t,re.S)
    return None if not m else set(x.strip().split('.{')[0] for x in m.group(1).split(','))
STD={"propext","Classical.choice","Quot.sound"}
ax=axset(a,P+"erdos_gallai"); cmp_ax=axset(c,P+"erdos_gallai")
print("solution axioms:",ax); print("comparator axioms:",cmp_ax)
for extra in ("main_cost_bound","decompositionCost_spec"): print("axioms",extra,axset(a,P+extra))
v=("MATCH" if all(res) else "MISMATCH")+"\n"+("STD_AXIOMS" if ax==STD else "NONSTD")+"\n"+("CMP_SORRY_SEEN" if cmp_ax and "sorryAx" in cmp_ax else "CMP_SORRY_NOT_SEEN")+"\n"
open("statement_match.txt","w").write(v); print(v)
