# Compare pp.all printouts of the COMPARATOR (statement with sorry) vs SOLUTION module for both family-170 mains:
# theorem type + every definition it unfolds through. Heads normalised (leading @ dropped; .{u} on defs dropped).
# Per main: MATCH/MISMATCH · STD_AXIOMS/NONSTD (solution) · CMP_SORRY_SEEN/NOT_SEEN (comparator must depend on sorryAx).
import re
STD={"propext","Classical.choice","Quot.sound"}
def blocks(t,P):
    HEAD=re.compile(r"^(def \S+|@?%s\w+(?= :))"%re.escape(P), re.M)
    ms=list(HEAD.finditer(t)); out={}
    for m,nxt in zip(ms, ms[1:]+[None]):
        seg=t[m.start(): nxt.start() if nxt else len(t)]
        h=m.group(1).lstrip('@')
        if h.startswith('def '): h=re.sub(r"\.\{[^}]*\}$","",h)
        # strip trailing axioms lines that follow the last block
        seg=re.split(r"\n'[^']+' depends on axioms",seg)[0]
        out[h]=re.sub(r"\s+"," ",seg.lstrip('@')).strip()
    return out
def axset(t,name):
    m=re.search(r"'%s' depends on axioms: \[([^\]]*)\]"%re.escape(name),t,re.S)
    return None if not m else set(x.strip().split('.{')[0] for x in m.group(1).split(','))
lines=[]
for tag,P,defs in (("SL","OAI.SharpLogRamsey.",["MainBounds","MainLimit","ramsey","RamseyProperty"]),
                   ("R5","OAI.SharpRamseyFive.",["SharpBounds","SharpExponent","ramsey","RamseyProperty"])):
    a=open(f"logs/ax{tag}.log").read(); c=open(f"logs/cmp{tag}.log").read()
    A,C=blocks(a,P),blocks(c,P)
    keys=[P+"main"]+["def "+P+d for d in defs]; res=[]
    for k in keys:
        x=A.get(k); y=C.get(k); ok = x is not None and x==y; res.append(ok)
        print(tag,k,"MATCH" if ok else "MISMATCH","| lens",None if x is None else len(x),None if y is None else len(y))
    ax=axset(a,P+"main"); cax=axset(c,P+"main")
    print(tag,"solution axioms:",ax,"comparator axioms:",cax)
    lines+= [f"{tag} "+("MATCH" if all(res) else "MISMATCH"), f"{tag} "+("STD_AXIOMS" if ax==STD else "NONSTD"),
             f"{tag} "+("CMP_SORRY_SEEN" if cax and "sorryAx" in cax else "CMP_SORRY_NOT_SEEN")]
open("statement_match.txt","w").write("\n".join(lines)+"\n"); print("\n".join(lines))
