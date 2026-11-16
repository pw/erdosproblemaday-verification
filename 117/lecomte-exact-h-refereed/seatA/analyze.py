"""Seat A analyzer for survey.g output.

For every group: omega (max pairwise-noncommuting set) and a (min abelian cover) computed EXACTLY by CP-SAT
on the central quotient, using the maximal abelian subgroups (maximal cliques of the commuting graph on
central cosets) as the constraint / covering family.  Then:
  G1  a <= T(omega)                         (Theorem 1.1 upper bound)
  G2  a <  T(omega) if omega >= 9           (strictness, nonbinary-symplectic)
and per scalar commutator form (p-groups), predictions of the printed lemmas:
  L42  rank 2 (j=1) and R abelian           => a == omega                     (Lemma 4.2)
  L45a R abelian noncentral                 => omega >= p^2 j + 1              (Lemma 4.5(1))
  L45b R nonabelian                         => omega >= sigma*max(p+1,m+1); and >= sigma(m+1)+1 if Z(R)!=Z(P)
  L45w R nonabelian: every fibre width w(gR) >= p+1 and >= m+1+log_p[Z(R):C_Z(R)(g)]   (Lemma 4.5(2), 2.4, 4.4)
  L21  R abelian: width of gR == [R : C_R(g)]                                     (Lemma 2.1)
  L46  R central and e=dim P' >= 2          => omega >= p^2 (j-1) + 1          (Lemma 4.6)
  AVG  sum over lines of P/R of fibre widths <= C_p(2j) * omega / (p j + 1)     (Sec 4.2 average)
  EQ4  R abelian: a <= 1 + C_p(2j) omega/(pj+1)                                   (eq. (4))
"""
import ast, sys, math, collections
import networkx as nx
from ortools.sat.python import cp_model

def T(n):
    if n <= 2: return 1
    if n <= 6: return n
    if n <= 8: return 10
    return 1 + 2 ** ((n - 1) // 2)

def Cp(p, k):
    return (p ** k - 1) // (p - 1)

def parse(fn):
    with open(fn) as f:
        cur = None
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("GROUP "):
                _, o, i, z, isp, p = line.split()
                cur = dict(order=int(o), id=int(i), z=int(z), isp=(isp == "true"), p=int(p))
            elif line.startswith("ROWS "):
                cur["rows"] = ast.literal_eval(line[5:])
            elif line.startswith("FORMS "):
                s = line[6:].replace("true", "True").replace("false", "False")
                cur["forms"] = ast.literal_eval(s)
            elif line == "END":
                yield cur

def solve_omega(vertices, cliques, limit=300):
    """max set of vertices meeting every maximal commuting clique at most once"""
    if not vertices: return 1, True, 1
    m = cp_model.CpModel()
    x = {v: m.NewBoolVar("") for v in vertices}
    for c in cliques:
        cc = [v for v in c if v in x]
        if len(cc) >= 2:
            m.Add(sum(x[v] for v in cc) <= 1)
    m.Maximize(sum(x.values()))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = limit; s.parameters.num_workers = 8
    st = s.Solve(m)
    return int(round(s.ObjectiveValue())), st == cp_model.OPTIMAL, int(round(s.BestObjectiveBound()))

def solve_cover(vertices, cliques, limit=300):
    if not vertices: return 1, True, 1
    m = cp_model.CpModel()
    y = [m.NewBoolVar("") for _ in cliques]
    inc = collections.defaultdict(list)
    for k, c in enumerate(cliques):
        for v in c:
            inc[v].append(k)
    for v in vertices:
        m.AddBoolOr([y[k] for k in inc[v]])
    m.Minimize(sum(y))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = limit; s.parameters.num_workers = 8
    st = s.Solve(m)
    return int(round(s.ObjectiveValue())), st == cp_model.OPTIMAL, int(round(s.BestObjectiveBound()))

def width(sub, adjset, ident):
    """max pairwise-noncommuting subset of the central cosets in `sub` (list of coset indices)"""
    vs = [v for v in sub if v != ident]
    if not vs: return 1
    # small: build commuting graph on vs and solve max independent set
    m = cp_model.CpModel(); x = {v: m.NewBoolVar("") for v in vs}
    for i, u in enumerate(vs):
        for w in vs[i+1:]:
            if w in adjset[u]:
                m.AddBoolOr([x[u].Not(), x[w].Not()])
    m.Maximize(sum(x.values()))
    s = cp_model.CpSolver(); s.parameters.num_workers = 8; s.parameters.max_time_in_seconds = 120
    st = s.Solve(m); assert st == cp_model.OPTIMAL
    return max(1, int(round(s.ObjectiveValue())))

def analyze(g, stats, verbose=False, deep=True):
    rows = g["rows"]; z = g["z"]; p = g["p"]
    n = len(rows); assert n == z
    adjset = [set(r) for r in rows]
    ident = [k for k in range(1, n + 1) if len(rows[k - 1]) == n]
    assert len(ident) == 1, "exactly one central coset expected"
    ident = ident[0]
    adj1 = {k: adjset[k - 1] for k in range(1, n + 1)}
    V = [k for k in range(1, n + 1) if k != ident]
    G = nx.Graph(); G.add_nodes_from(V)
    for u in V:
        for w in adj1[u]:
            if w != ident and w > u:
                G.add_edge(u, w)
    cliques = [c for c in nx.find_cliques(G)] if V else []
    om, opt1, b1 = solve_omega(V, cliques)
    a, opt2, b2 = solve_cover(V, cliques)
    key = (g["order"], g["id"])
    res = dict(z=z, omega=om, a=a, opt=(opt1 and opt2))
    if not (opt1 and opt2):
        stats["nonopt"].append((key, om, b1, a, b2))
    stats["maxa"][om] = max(stats["maxa"].get(om, 0), a)
    if a > T(om):
        stats["G1"].append((key, om, a))
    if om >= 9 and a >= T(om):
        stats["G2"].append((key, om, a))
    if a == T(om) and om >= 3:
        stats["eq"].append((key, om, a, z))
    if deep and g.get("forms"):
        # identity coset label per form
        for f in g["forms"]:
            j, Rab, Rcen, mm, ZReq, labs, zr, xi = f
            e = len(xi)
            sigma = p * j + 1
            idlab = labs[ident - 1]
            byLab = collections.defaultdict(list)
            for k in range(1, n + 1):
                byLab[labs[k - 1]].append(k)
            Rset = byLab[idlab]
            if j == 1 and Rab:
                stats["n_L42"] += 1
                if a != om: stats["L42"].append((key, om, a, xi))
            if Rab and not Rcen:
                stats["n_L45a"] += 1
                if om < p * p * j + 1: stats["L45a"].append((key, om, p, j))
            if not Rab:
                stats["n_L45b"] += 1
                need = sigma * max(p + 1, mm + 1)
                if not ZReq: need = max(need, sigma * (mm + 1) + 1)
                if om < need: stats["L45b"].append((key, om, need, p, j, mm, ZReq))
            if Rcen and e >= 2:
                stats["n_L46"] += 1
                if om < p * p * (j - 1) + 1: stats["L46"].append((key, om, p, j, e))
            # fibre widths: only one fibre per line of P/R matters; compute all labels (small)
            nlab = len(byLab)
            if nlab <= 400 and z <= 800:
                W = {lab: width(byLab[lab], adj1, ident) for lab in byLab}
                for lab, w in W.items():
                    if lab == idlab: continue
                    if not Rab:
                        stats["n_L45w"] += 1
                        if w < p + 1 or w < mm + 1 + zr[lab - 1]:
                            stats["L45w"].append((key, lab, w, p, mm, zr[lab - 1]))
                    else:
                        # [R : C_R(g)] = |R/Z| / |C_R(g)/Z|, g = any coset in this fibre
                        g0 = byLab[lab][0]
                        cr = sum(1 for k in Rset if k in adj1[g0])
                        idx = len(Rset) // cr
                        stats["n_L21"] += 1
                        if w != idx: stats["L21"].append((key, lab, w, idx))
                # AVG: lines of V = P/R.  Group labels into lines: we only know labels, not the vector
                # structure; but widths are constant on generators of a cyclic subgroup (Lemma 2.2(i)),
                # so sum over lines = (sum over nonzero labels)/(p-1).
                tot = sum(w for lab, w in W.items() if lab != idlab)
                lines_sum = tot / (p - 1)
                bound = Cp(p, 2 * j) * om / sigma
                stats["n_AVG"] += 1
                if lines_sum > bound + 1e-9: stats["AVG"].append((key, xi, lines_sum, bound))
                if Rab:
                    stats["n_EQ4"] += 1
                    if a > 1 + bound + 1e-9: stats["EQ4"].append((key, a, 1 + bound))
    return res

def main(files, deep=True):
    stats = collections.defaultdict(list)
    stats["maxa"] = {}
    for k in ["n_L42", "n_L45a", "n_L45b", "n_L46", "n_L45w", "n_L21", "n_AVG", "n_EQ4"]:
        stats[k] = 0
    ng = 0
    for fn in files:
        for g in parse(fn):
            ng += 1
            analyze(g, stats, deep=deep)
    print(f"groups analysed: {ng}")
    print("max a by omega:", dict(sorted(stats["maxa"].items())), " T:", {k: T(k) for k in sorted(stats["maxa"])})
    for k in ["G1", "G2", "L42", "L45a", "L45b", "L45w", "L21", "L46", "AVG", "EQ4", "nonopt"]:
        cnt = stats.get("n_" + k)
        v = stats.get(k, [])
        print(f"  {k}: violations={len(v)}" + (f" (instances tested={cnt})" if cnt is not None else ""), v[:6])
    eqs = stats.get("eq", [])
    print(f"  equality a=T(omega) cases: {len(eqs)}; by omega:", collections.Counter(e[1] for e in eqs))
    return stats

if __name__ == "__main__":
    deep = True
    args = sys.argv[1:]
    if args and args[0] == "--shallow":
        deep = False; args = args[1:]
    main(args, deep=deep)
