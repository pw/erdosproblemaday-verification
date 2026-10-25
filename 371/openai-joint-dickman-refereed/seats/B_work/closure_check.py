import re
ROOTS={'OAI':'/tmp/oaimath/012/src/oai','ComparatorChallenges':'/tmp/oaimath/012/src/oai','PrimeNumberTheoremAnd':'/tmp/oaimath/012/src/pnt','StrongPNT':'/tmp/oaimath/012/src/strongpnt','Architect':'/tmp/oaimath/024/architect'}
order=[l.strip() for l in open('/tmp/oaimath/012/lean-build/all_order.txt') if l.strip()]
S=set(order)
def strip(t):
    # remove nested block comments
    out=[];i=0;depth=0
    while i<len(t):
        if t.startswith('/-',i): depth+=1;i+=2;continue
        if depth and t.startswith('-/',i): depth-=1;i+=2;continue
        if not depth: out.append(t[i])
        i+=1
    return re.sub(r'--[^\n]*','',''.join(out))
def imports(m):
    t=strip(open(f"{ROOTS[m.split('.')[0]]}/{m.replace('.','/')}.lean",encoding='utf-8').read())
    res=[]
    for line in t.splitlines():
        w=line.split()
        if not w: continue
        if w[0] in ('import','public','meta','private') and 'import' in w:
            res.append(w[-1])
        elif w[0] not in ('module','prelude'): break
    return res
def closure(root):
    seen=set();st=[root];ext=set()
    while st:
        m=st.pop()
        if m in seen: continue
        seen.add(m)
        for d in imports(m):
            if d.split('.')[0] in ROOTS: st.append(d)
            else: ext.add(d.split('.')[0])
    return seen,ext
c,ext=closure('OAI.NumberTheory.JointDickman.PaperMain')
print('PaperMain closure',len(c),'external roots',sorted(ext))
print('in all_order not in PaperMain closure',sorted(S-c)[:10], len(S-c))
print('in PaperMain closure not in all_order',sorted(c-S)[:10])
