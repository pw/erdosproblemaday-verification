# Own (3,3)-edge-colouring finder: DFS over edges with triangle propagation (no SAT/CP library). Prints a colouring
# with no monochromatic triangle if one exists, re-checks it literally by brute force over all vertex triples.
import sys, itertools, networkx as nx
def good_colouring(G):
    E=[tuple(sorted(e)) for e in G.edges()]; eid={e:i for i,e in enumerate(E)}
    tri=[tuple(eid[tuple(sorted(p))] for p in itertools.combinations(t,2)) for t in itertools.combinations(sorted(G.nodes()),3)
         if all(G.has_edge(a,b) for a,b in itertools.combinations(t,2))]
    on=[[] for _ in E]
    for t in tri:
        for e in t: on[e].append(t)
    col=[-1]*len(E); trail=[]
    def assign(e,c):
        stack=[(e,c)]
        while stack:
            e,c=stack.pop()
            if col[e]!=-1:
                if col[e]!=c: return False
                continue
            col[e]=c; trail.append(e)
            for t in on[e]:
                cs=[col[x] for x in t]
                if cs.count(c)==3: return False
                if cs.count(c)==2 and -1 in cs: stack.append((t[cs.index(-1)],1-c))
        return True
    nodes=[0]
    def dfs():
        nodes[0]+=1
        try: e=col.index(-1)
        except ValueError: return True
        for c in (0,1):
            mark=len(trail)
            if assign(e,c) and dfs(): return True
            while len(trail)>mark: col[trail.pop()]=-1
        return False
    ok=assign(0,0) and dfs()   # colour symmetry: first edge red
    return (dict(zip(E,col)) if ok else None), nodes[0], len(tri)
def literal_check(G,colour):
    mono=0
    for t in itertools.combinations(G.nodes(),3):
        if all(G.has_edge(a,b) for a,b in itertools.combinations(t,2)):
            cs={colour[tuple(sorted(p))] for p in itertools.combinations(t,2)}
            if len(cs)==1: mono+=1
    return mono
for name,G in [("K5",nx.complete_graph(5)),("K6",nx.complete_graph(6)),("K3+C5 (Graham)",nx.complement(nx.disjoint_union(nx.empty_graph(3),nx.complement(nx.cycle_graph(5)))))]:
    c,nodes,nt=good_colouring(G); print(f"control {name}: {'good colouring found' if c else 'NO good colouring (arrows)'}  ({nodes} DFS nodes)")
for s in sys.argv[1:]:
    G=nx.from_graph6_bytes(s.encode())
    c,nodes,nt=good_colouring(G)
    if c is None: print(f"{s}: ARROWS (no good colouring), {nodes} DFS nodes"); continue
    mono=literal_check(G,c); red=sorted(e for e,v in c.items() if v==0)
    print(f"{s}: n={G.number_of_nodes()} triangles={nt}: good colouring found ({nodes} DFS nodes); literal recount of monochromatic triangles = {mono}; red edges {len(red)}, blue {len(c)-len(red)}")
    print("   red edge list:", red)
