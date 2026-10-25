import re,sys
L=sys.argv[1]
ALPHA={"colorCount":"k","coloring":"c","point":"x","otherPoint":"y"}   # the comparator's binder names → the solution's (pp.all prints binders; the terms are otherwise identical — the kernel-level check is probe/CmpBridge.lean)
def norm(p):
    t=re.sub(r"\s+"," ",open(p).read()).strip()
    for a,b in ALPHA.items(): t=re.sub(r"\b%s\b"%a,b,t)
    return t
cm,sm=norm(f"{L}/logs/cmp_main.log"),norm(f"{L}/logs/sol_main.log")
cd,sd=norm(f"{L}/logs/cmp_def.log"),norm(f"{L}/logs/sol_def.log")
ax=open(f"{L}/logs/axioms.log").read(); cax=open(f"{L}/logs/cmp_axioms.log").read()
def axset(t,name):
    m=re.search(r"'%s' depends on axioms: \[([^\]]*)\]"%re.escape(name),t)
    return None if not m else set(x.strip() for x in m.group(1).split(','))
STD={"propext","Classical.choice","Quot.sound"}
names=["OAI.EuclideanFiveColor.no_proper_five_coloring","OAI.EuclideanFiveColor.no_measurable_weak_five_coloring","OAI.EuclideanFiveColor.proper_to_borel_weak","OAI.EuclideanFiveColor.proper_to_weak"]
out=[]
out.append("MAIN_STATEMENT(alpha-normalised binders) "+("MATCH" if cm==sm and cm and cm.startswith("OAI.EuclideanFiveColor.no_proper_five_coloring :") else "MISMATCH"))
out.append("DEF_ProperColoring(alpha-normalised binders) "+("MATCH" if cd==sd and cd and "ProperColoring" in cd else "MISMATCH"))
for n in names:
    a=axset(ax,n); out.append(f"AXIOMS {n} {'STD' if a==STD else 'NONSTD'} {sorted(a) if a else None}")
ca=axset(cax,"OAI.EuclideanFiveColor.no_proper_five_coloring")
out.append("CMP_SORRY "+("SEEN" if ca and "sorryAx" in ca else "NOT_SEEN")+f" {sorted(ca) if ca else None}")
print("\n".join(out)); open(f"{L}/statement_match.txt","w").write("\n".join(out)+"\n")
print("CMP main:",cm[:400]); print("SOL main:",sm[:400]); print("CMP def:",cd[:300]); print("SOL def:",sd[:300])
ok = cm==sm and cd==sd and cm.startswith("OAI.EuclideanFiveColor.no_proper_five_coloring :") and axset(ax,names[0])==STD
sys.exit(0 if ok else 1)
