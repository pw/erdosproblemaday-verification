# Simulate the exponent-graph update (4.9) [src24] of Section 4 and check the
# anchor-code claims (4.13) [characters-anchor-pair] and "code + final parity
# determines the path", plus the net-exponent claims used for the diagonal and
# the final permutation comparison.
import itertools, sys

def run(k, alpha_override=None):
    # slot: dict(name, kind, step(for pivot/anchor), path(tuple), eps, active)
    slots = []
    def add(**kw):
        slots.append(kw); return len(slots)-1
    W = add(kind='word', path=(), eps=1, active=True, step=None, sz=None)
    piv = {}
    for j in range(1, k+1):
        piv[j] = add(kind='pivot', path=(), eps=1, active=True, step=j, sz=None)
    anchors = {}
    for j in range(1, k+1):
        for sz in ('small','big'):
            anchors[(j,sz)] = add(kind='anchor', path=(), eps=1, active=False, step=j, sz=sz, fresh=True)
    F = add(kind='filler', path=(), eps=1, active=False, step=None, sz=None)
    # conjugate copies (outside)
    n0 = len(slots)
    for i in range(n0):
        s = dict(slots[i]); s['active']=False; s['kind']='conj_'+s['kind']; s['eps']=-1; s['fresh']=False
        slots.append(s)
    b = {}
    N = len(slots)
    for i in range(N):
        for h in range(N):
            if i != h: b[(i,h)] = 1
    cur = list(range(N))
    for j in range(1, k+1):
        P = [i for i in cur if slots[i]['kind']=='pivot' and slots[i]['active'] and slots[i]['step']==j]
        assert len(P)==1; P = P[0]
        H = [i for i in cur if (slots[i]['kind']=='word' and slots[i]['active'])
             or (slots[i]['kind']=='pivot' and slots[i]['active'] and slots[i]['step']>j)
             or (slots[i]['kind']=='anchor' and slots[i].get('fresh') and slots[i]['step']==j)]
        Y = [i for i in cur if i not in H and i != P]
        # regular invariant check before step
        for i in cur:
            if slots[i]['active']:
                for h in cur:
                    if h!=i and b[(i,h)] != slots[i]['eps']:
                        raise SystemExit(f'regular invariant fails step {j} slot {i} {slots[i]["kind"]}')
        # incoming rows into pivot constant? (single atom here) record b_iP
        newid = {}
        newslots = {}
        for i in H:
            for t in (1,-1):
                s = dict(slots[i]); s['path'] = slots[i]['path']+(t,) if slots[i]['kind']=='word' else slots[i]['path']
                s['eps'] = slots[i]['eps']*t
                if slots[i]['kind']=='word':
                    s['active']=True
                elif slots[i]['kind']=='pivot':
                    s['active'] = (t==1)
                    if t==-1: s['kind']='pivot_neg_out'
                elif slots[i]['kind']=='anchor':
                    s['active']=False; s['fresh']=False; s['clone']=t
                slots.append(s); newid[(i,t)] = len(slots)-1
        nb = {}
        for i in H:
            for t in (1,-1):
                for h in H:
                    for u in (1,-1):
                        if (i,t)==(h,u): continue
                        if t==u:
                            if i!=h: nb[(newid[(i,t)],newid[(h,u)])] = t*b[(i,h)]
                        else:
                            nb[(newid[(i,t)],newid[(h,u)])] = b[(i,P)]
                for y in Y:
                    nb[(newid[(i,t)],y)] = t*b[(i,y)]
                    nb[(y,newid[(i,t)])] = t*b[(y,i)]
        for y in Y:
            for y2 in Y:
                if y!=y2: nb[(y,y2)] = 0
        # NOTE: rows i^t -> h^u for i==h, t!=u: cross copy of same slot gets t*b_iP
        b = nb
        cur = [newid[(i,t)] for i in H for t in (1,-1)] + Y
    return slots, b, cur

def check(k):
    slots, b, cur = run(k)
    words = [i for i in cur if slots[i]['kind']=='word']
    assert len(words)==2**k
    anc = [i for i in cur if slots[i]['kind']=='anchor']
    # code of each word slot: tuple over anchors of b_{y i}/eps_i
    codes = {}
    for i in words:
        t = slots[i]['path']; eps = 1
        for x in t: eps*=x
        assert eps == slots[i]['eps'], 'eps != product of path signs'
        code = tuple(b[(y,i)]*eps for y in sorted(anc, key=lambda y:(slots[y]['step'],slots[y]['sz'],slots[y]['clone'])))
        codes[t]=code
        # predicted pair formula
        e=[1]
        for x in t: e.append(e[-1]*x)
        for j in range(1,k+1):
            for sz in ('small','big'):
                yp=[y for y in anc if slots[y]['step']==j and slots[y]['sz']==sz and slots[y]['clone']==1][0]
                ym=[y for y in anc if slots[y]['step']==j and slots[y]['sz']==sz and slots[y]['clone']==-1][0]
                pair=(b[(yp,i)]*eps, b[(ym,i)]*eps)
                alpha=1
                pred=(1,-alpha*e[j-1]) if t[j-1]==1 else (-alpha*e[j-1],1)
                assert pair==pred, (k,t,j,sz,pair,pred)
            # bulk->anchor rows equal eps (regular)
            for y in anc:
                assert b[(i,y)]==eps
    # at most two paths per code; code+parity determines path
    from collections import defaultdict
    byc=defaultdict(list)
    for t,c in codes.items(): byc[c].append(t)
    mx=max(len(v) for v in byc.values())
    par_ok=all(len({(lambda t: __import__('math').prod(t))(t) for t in v})==len(v) for v in byc.values())
    # net exponent claims for two paths with same parity, different code: exists small anchor with
    # anchor->bulk net = +-2 and bulk->anchor net 0
    ok_same=True; ok_diff=True
    for t1 in codes:
        for t2 in codes:
            if t1==t2: continue
            e1=__import__('math').prod(t1); e2=__import__('math').prod(t2)
            i1=[i for i in words if slots[i]['path']==t1][0]; i2=[i for i in words if slots[i]['path']==t2][0]
            if codes[t1]==codes[t2]: continue
            found=False
            for y in anc:
                if b[(y,i1)]!=b[(y,i2)] or True:
                    a2b=b[(y,i1)]-b[(y,i2)]; b2a=b[(i1,y)]-b[(i2,y)]
                    want_sz = 'small' if e1==e2 else 'big'
                    if slots[y]['sz']==want_sz and abs(a2b if e1==e2 else b2a)==2 and (b2a if e1==e2 else a2b)==0:
                        found=True
            if e1==e2: ok_same &= found
            else: ok_diff &= found
    return mx, par_ok, ok_same, ok_diff, len(byc)

for k in range(1,7):
    print(k, check(k))
