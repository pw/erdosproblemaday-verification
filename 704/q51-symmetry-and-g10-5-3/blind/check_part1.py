import re, itertools
html=open('/home/exedev/MathDyad/erdos704/q51/page/entry.html').read()
# extract the three <li> lines that consist of 5-digit tokens
fams=[]
for li in re.findall(r'<li>([0-9, ;.]+)</li>', html):
    toks=re.findall(r'\b\d{5}\b', li)
    fams.append([frozenset(int(c) for c in t) for t in toks])
print('families parsed:', len(fams), [len(f) for f in fams])
for f in fams:
    assert all(len(s)==5 for s in f)
def sh(s): return frozenset(((x+1)%7 if x<7 else x) for x in s)
classes=[]
for f in fams:
    cur=f
    for i in range(7):
        classes.append(cur); cur=[sh(s) for s in cur]
allsets=[s for c in classes for s in c]
print('classes',len(classes),'total sets',len(allsets),'distinct',len(set(allsets)))
full=set(frozenset(c) for c in itertools.combinations(range(10),5))
print('cover all 252:', set(allsets)==full)
bad=sum(1 for c in classes for a,b in itertools.combinations(c,2) if len(a&b)==3)
print('bad pairs (share exactly 3):', bad)
print('each class size 12:', all(len(set(c))==12 for c in classes))
# negative control: perturb one set
c2=[list(c) for c in classes]; c2[0][0], c2[1][0] = c2[1][0], c2[0][0]
print('neg control bad pairs:', sum(1 for c in c2 for a,b in itertools.combinations(c,2) if len(a&b)==3))
