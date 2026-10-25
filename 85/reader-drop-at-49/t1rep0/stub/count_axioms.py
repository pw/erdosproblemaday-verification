import re,sys
t=open(sys.argv[1]).read()
for m in re.finditer(r"'([^']+)' depends on axioms: \[(.*?)\]", t, flags=re.S):
    ax=[a.strip() for a in m.group(2).replace('\n',' ').split(',') if a.strip()]
    nd=[a for a in ax if '.native_decide.' in a or '_native' in a]
    other=sorted(set(ax)-set(nd))
    print(m.group(1), 'total', len(ax), 'native_decide', len(nd), 'other', other, 'sorryAx' in ax)
