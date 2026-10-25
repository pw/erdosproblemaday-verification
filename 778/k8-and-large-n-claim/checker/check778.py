#!/usr/bin/env python3
"""Independent checker for solve778 strategy certificates (Erdős #778, (1:2) clique game on K_n).

Shares NOTHING with the solver except the edge numbering convention (lexicographic i<j) and the game rules.
Canonical forms: nauty (pynauty) on a 2-layer graph (layer 0 = red edges, layer 1 = blue edges, rungs i--n+i).
Clique numbers: own subset enumeration. Cutoffs: re-derived here from first principles (see bob_cutoff/alice_cutoff).

Certificate (winner = bob): lines "R B e f" — at the Bob-to-move state (R,B) (a representative), Bob replies with free edges e,f.
Certificate (winner = alice): lines "R B e" — at the Alice-to-move state (R,B), Alice plays e.
Verdict: ACCEPT iff the winner's strategy is complete and wins against every opponent move, exploring the whole tree
(opponent moves enumerated exhaustively), with transposition only through nauty canonical forms.
Exit 0 ACCEPT, 1 REJECT (with reason), 2 cannot-see (bad file).
"""
import sys, itertools, collections
from pynauty import Graph, canon_label, certificate

def parse(path):
    hdr = None; rows = []
    with open(path) as f:
        for line in f:
            if line.startswith('#'):
                hdr = dict(kv.split('=') for kv in line[1:].split() if '=' in kv); continue
            p = line.split()
            if p: rows.append(tuple(int(x) for x in p))
    if hdr is None: raise SystemExit("CANNOT SEE: no header")
    return hdr, rows

class Game:
    def __init__(self, n, mode, alice_edges):
        self.n = n; self.mode = mode; self.A = alice_edges
        self.edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        self.m = len(self.edges); self.full = (1 << self.m) - 1
        self.eidx = {}
        for k, (i, j) in enumerate(self.edges): self.eidx[(i, j)] = self.eidx[(j, i)] = k
        assert self.A == (self.m + 2) // 3
    # --- cliques (own code) ---
    def omega(self, mask):
        for size in range(self.n, 1, -1):
            for S in itertools.combinations(range(self.n), size):
                if all(mask >> self.eidx[(a, b)] & 1 for a, b in itertools.combinations(S, 2)): return size
        return 1
    def alpha(self, mask): return self.omega(self.full & ~mask)
    def omega_budget(self, R, B, k):
        # largest S with no blue edge inside and at most k non-red edges inside
        for size in range(self.n, 1, -1):
            for S in itertools.combinations(range(self.n), size):
                es = [self.eidx[(a, b)] for a, b in itertools.combinations(S, 2)]
                if any(B >> e & 1 for e in es): continue
                if sum(1 for e in es if not (R >> e & 1)) <= k: return size
        return 1
    def triangle_completable(self, R, B, k):
        for S in itertools.combinations(range(self.n), 3):
            es = [self.eidx[(a, b)] for a, b in itertools.combinations(S, 2)]
            if any(B >> e & 1 for e in es): continue
            if sum(1 for e in es if not (R >> e & 1)) <= k: return True
        return False
    # --- terminal + cutoffs (re-derived) ---
    def terminal_bob_wins(self, R, B):
        assert (R | B) == self.full and (R & B) == 0
        if self.mode == 'triangle': return self.omega(R) <= 2
        return self.alpha(R) > self.omega(R)
    def bob_cutoff(self, R, B):
        """Bob has already won: the final alpha(R_final) >= omega(B) (blue cliques survive since B is disjoint from red),
        and omega(R_final) <= omega_budget (a final red clique has no blue edge and Alice adds <= kA edges inside it)."""
        kA = self.A - bin(R).count('1')
        if self.mode == 'triangle': return not self.triangle_completable(R, B, kA)
        return self.omega(B) > self.omega_budget(R, B, kA)
    def alice_cutoff(self, R, B):
        """Alice has already won: omega only grows and alpha only shrinks as red edges are added."""
        if self.mode == 'triangle': return self.omega(R) >= 3
        return self.omega(R) >= self.alpha(R)
    # --- canonical form via nauty ---
    def layered(self, R, B):
        n = self.n; g = Graph(2 * n, directed=False, vertex_coloring=[set(range(n)), set(range(n, 2 * n))])
        adj = collections.defaultdict(list)
        for k, (i, j) in enumerate(self.edges):
            if R >> k & 1: adj[i].append(j)
            if B >> k & 1: adj[n + i].append(n + j)
        for i in range(n): adj[i].append(n + i)
        for v, lst in adj.items(): g.connect_vertex(v, lst)
        return g
    def canon(self, R, B):
        g = self.layered(R, B)
        lab = canon_label(g)            # lab[pos] = vertex at canonical position pos
        assert all(lab[p] < self.n for p in range(self.n)), "layer order not preserved"
        pos = {lab[p]: p for p in range(self.n)}   # original vertex -> canonical position (layer 0)
        return certificate(g), pos
    def transport(self, pos_from, pos_to, e):
        """edge index e in coordinates where vertex v has canonical position pos_from[v] -> coordinates of pos_to."""
        a, b = self.edges[e]
        inv = {p: v for v, p in pos_to.items()}
        return self.eidx[(inv[pos_from[a]], inv[pos_from[b]])]

NO_CUTOFF = False  # --no-cutoff: never close a branch by the Bob/Alice cutoffs; walk every line to a full board

def check(path, max_nodes=10**8):
    hdr, rows = parse(path)
    n = int(hdr['n']); mode = hdr['mode']; winner = hdr['winner']; A = int(hdr['aliceEdges'])
    G = Game(n, mode, A)
    table = {}
    for r in rows:
        R, B = r[0], r[1]
        if winner == 'bob':
            e, f = r[2], r[3]
            if e == f or R >> e & 1 or B >> e & 1 or R >> f & 1 or B >> f & 1: return 1, f"reply not free at {R} {B}"
        else:
            e = r[2]
            if R >> e & 1 or B >> e & 1: return 1, f"move not free at {R} {B}"
        key, pos = G.canon(R, B)
        if key in table and table[key][:2] != (R, B): pass  # duplicates allowed if consistent (isomorphic reps)
        table[key] = (R, B, pos, r[2:])
    seen = set(); stack = [(0, 0)]; nodes = 0; leaves = 0; cutoffs = 0
    while stack:
        R, B = stack.pop(); nodes += 1
        if nodes > max_nodes: return 2, "node budget exceeded"
        # (R,B) is an Alice-to-move position
        free = [e for e in range(G.m) if not (R | B) >> e & 1]
        if winner == 'bob':
            if not free:
                if not G.terminal_bob_wins(R, B): return 1, f"terminal lost at R={R} B={B}"
                leaves += 1; continue
            if not NO_CUTOFF:
                if G.alice_cutoff(R, B): return 1, f"alice cutoff holds inside Bob's tree at R={R} B={B}"
                if G.bob_cutoff(R, B): cutoffs += 1; continue
            for e in free:
                R2 = R | (1 << e)
                free2 = [x for x in free if x != e]
                if not free2:
                    if not G.terminal_bob_wins(R2, B): return 1, f"terminal lost at R={R2} B={B}"
                    leaves += 1; continue
                if not NO_CUTOFF and G.bob_cutoff(R2, B): cutoffs += 1; continue
                key, pos = G.canon(R2, B)
                ent = table.get(key)
                if ent is None: return 1, f"no Bob reply recorded for R={R2} B={B}"
                rR, rB, rpos, mv = ent
                a = G.transport(rpos, pos, mv[0]); b = G.transport(rpos, pos, mv[1])
                if a == b or (R2 | B) >> a & 1 or (R2 | B) >> b & 1: return 1, f"transported reply not free at R={R2} B={B}"
                if len(free2) == 1:  # Bob takes the single remaining edge (cannot happen when m ≡ 1 mod 3 like 28)
                    B2 = B | (1 << a)
                else:
                    B2 = B | (1 << a) | (1 << b)
                key2, _ = G.canon(R2, B2)
                if key2 in seen: continue
                seen.add(key2); stack.append((R2, B2))
        else:  # winner == alice
            if not free:
                if G.terminal_bob_wins(R, B): return 1, f"terminal lost (Bob wins) at R={R} B={B}"
                leaves += 1; continue
            if G.bob_cutoff(R, B): return 1, f"bob cutoff holds inside Alice's tree at R={R} B={B}"
            if G.alice_cutoff(R, B): cutoffs += 1; continue
            key, pos = G.canon(R, B)
            ent = table.get(key)
            if ent is None: return 1, f"no Alice move recorded for R={R} B={B}"
            rR, rB, rpos, mv = ent
            e = G.transport(rpos, pos, mv[0])
            if (R | B) >> e & 1: return 1, f"transported move not free at R={R} B={B}"
            R2 = R | (1 << e)
            free2 = [x for x in free if x != e]
            if not free2:
                if G.terminal_bob_wins(R2, B): return 1, f"terminal lost (Bob wins) at R={R2} B={B}"
                leaves += 1; continue
            if G.alice_cutoff(R2, B): cutoffs += 1; continue
            if G.bob_cutoff(R2, B): return 1, f"bob cutoff holds after Alice's move at R={R2} B={B}"
            pairs = list(itertools.combinations(free2, 2)) if len(free2) >= 2 else [(free2[0],)]
            for pr in pairs:
                B2 = B
                for x in pr: B2 |= 1 << x
                key2, _ = G.canon(R2, B2)
                if key2 in seen: continue
                seen.add(key2); stack.append((R2, B2))
    return 0, f"ACCEPT winner={winner} n={n} mode={mode}: {nodes} {('Alice' if winner=='bob' else 'Alice')}-to-move positions explored, {leaves} terminal leaves, {cutoffs} cutoff leaves, {len(table)} certificate entries"

if __name__ == '__main__':
    if '--no-cutoff' in sys.argv: NO_CUTOFF = True; sys.argv.remove('--no-cutoff')
    rc, msg = check(sys.argv[1])
    print(("ACCEPT" if rc == 0 else ("REJECT" if rc == 1 else "CANNOT SEE")) + " :: " + msg)
    sys.exit(rc)
