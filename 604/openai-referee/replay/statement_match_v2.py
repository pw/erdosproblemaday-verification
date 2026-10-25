# v2 (as run 15:3xZ; MIS-KEYED — kept for the record). Split at declaration heads but keyed each block by its whole first line
# split on ' :=', so no key equalled "OAI.WeakPinned.main :" and every lookup returned None → MISMATCH.
import re
a=open("logs/axioms.log").read(); c=open("logs/comparator.log").read()
HEAD=re.compile(r"^(def |theorem |'[^']+' depends on axioms|OAI\.WeakPinned\.[A-Za-z_]+ :)", re.M)
def blocks(t):
    idx=[m.start() for m in HEAD.finditer(t)]+[len(t)]
    out={}
    for i,j in zip(idx,idx[1:]):
        seg=t[i:j]; key=seg.split('\n',1)[0].split(' :=',1)[0].split(' depends',1)[0].strip()
        out[key]=re.sub(r"\s+"," ",seg).strip()
    return out
A,C=blocks(a),blocks(c)
for k in ["OAI.WeakPinned.main :","def OAI.WeakPinned.F","def OAI.WeakPinned.pairFraction","def OAI.WeakPinned.richPairs","def OAI.WeakPinned.k","def OAI.WeakPinned.distanceFiber"]:
    x=A.get(k); y=C.get(k); print(k, "MATCH" if (x is not None and x==y) else "MISMATCH")
