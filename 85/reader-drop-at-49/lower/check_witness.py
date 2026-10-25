import re, sys, itertools
def edges(path, name):
    s=open(path).read()
    i=s.find(name); j=s.find(']', i)
    return [tuple(map(int,m)) for m in re.findall(r'\((\d+),\s*(\d+)\)', s[i:j])]
def check(E,n):
    adj=[set() for _ in range(n)]
    for a,b in E:
        assert a!=b and 0<=a<n and 0<=b<n and b not in adj[a]
        adj[a].add(b); adj[b].add(a)
    deg=[len(x) for x in adj]
    mc=max(len(adj[u]&adj[w]) for u,w in itertools.combinations(range(n),2))
    return len(E),min(deg),max(deg),mc
print('48:',check(edges('Erdos85Boza48Witness.lean','boza48Edges : List'),48))
s=open('Erdos85OrderFortyNineDegreeSixWitness.lean').read()
nm=re.search(r'def (\w+) : List \(Nat × Nat\)',s).group(1); print('49 list name',nm)
print('49:',check(edges('Erdos85OrderFortyNineDegreeSixWitness.lean',nm+' : List'),49))
# control: add edge between two vertices at distance 2 -> creates codegree 2 somewhere
E=edges('Erdos85Boza48Witness.lean','boza48Edges : List'); E2=E+[(0,2)]
print('48+edge(0,2) control:',check(E2,48))
