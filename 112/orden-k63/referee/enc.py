"""Own SAT encoding (written from scratch by seat O) for {I_k, L_3}-free oriented graphs.
Variables: a(i,j) for ordered pairs i != j, meaning arc i -> j.
"""
import itertools
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType

class Enc:
    def __init__(self, n, k, tt=True, indep=True):
        self.n, self.k = n, k
        self.pool = IDPool()
        self.cnf = CNF()
        V = range(n)
        # create arc variables first so they are 1..n(n-1)
        for i in V:
            for j in V:
                if i != j:
                    self.a(i, j)
        for i, j in itertools.combinations(V, 2):
            self.cnf.append([-self.a(i, j), -self.a(j, i)])        # oriented: no 2-cycle
        if tt:
            for x, y, z in itertools.permutations(V, 3):
                self.cnf.append([-self.a(x, y), -self.a(y, z), -self.a(x, z)])  # no x->y, y->z, x->z
        if indep:
            for S in itertools.combinations(V, k):
                cl = []
                for i, j in itertools.combinations(S, 2):
                    cl += [self.a(i, j), self.a(j, i)]
                self.cnf.append(cl)                                   # S is not independent

    def a(self, i, j):
        return self.pool.id(('a', i, j))

    def deg_lits(self, v):
        return [self.a(v, j) for j in range(self.n) if j != v] + [self.a(j, v) for j in range(self.n) if j != v]

    def card(self, lits, bound, kind):
        f = {'atmost': CardEnc.atmost, 'atleast': CardEnc.atleast, 'equals': CardEnc.equals}[kind]
        c = f(lits=lits, bound=bound, vpool=self.pool, encoding=EncType.seqcounter)
        self.cnf.extend(c.clauses)

    def fix_arc(self, i, j):
        self.cnf.append([self.a(i, j)])

    def fix_nonadj(self, i, j):
        self.cnf.append([-self.a(i, j)]); self.cnf.append([-self.a(j, i)])

    def arcs_from_model(self, model):
        s = set(l for l in model if l > 0)
        return sorted((i, j) for i in range(self.n) for j in range(self.n) if i != j and self.a(i, j) in s)
