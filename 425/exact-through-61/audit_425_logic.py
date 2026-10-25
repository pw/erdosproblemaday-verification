#!/usr/bin/env python3
"""Small exhaustive audit of the independent #425 SAT reduction's logic."""

from itertools import combinations

from audit_425_sat import at_most_sinz, make_cnf, obstruction_edges


def dpll(clauses, assignment=None):
    assignment = {} if assignment is None else dict(assignment)
    while True:
        residual = []
        units = []
        for clause in clauses:
            undecided = []
            satisfied = False
            for lit in clause:
                var = abs(lit)
                if var in assignment:
                    if assignment[var] == (lit > 0):
                        satisfied = True
                        break
                else:
                    undecided.append(lit)
            if satisfied:
                continue
            if not undecided:
                return False
            residual.append(tuple(undecided))
            if len(undecided) == 1:
                units.append(undecided[0])
        if not residual:
            return True
        if not units:
            break
        for lit in units:
            var, value = abs(lit), lit > 0
            if var in assignment and assignment[var] != value:
                return False
            assignment[var] = value

    clause = min(residual, key=len)
    var = abs(clause[0])
    for value in (True, False):
        child = dict(assignment)
        child[var] = value
        if dpll(residual, child):
            return True
    return False


def valid_by_definition(values):
    products = set()
    for a, b in combinations(values, 2):
        if a * b in products:
            return False
        products.add(a * b)
    return True


def exact_f_bruteforce(n):
    answer = 0
    for mask in range(1 << n):
        if mask.bit_count() <= answer:
            continue
        values = [i + 1 for i in range(n) if mask >> i & 1]
        if valid_by_definition(values):
            answer = len(values)
    return answer


def edges_by_pair_collisions(n):
    owners = {}
    edges = set()
    for a, b in combinations(range(1, n + 1), 2):
        product = a * b
        for c, d in owners.get(product, ()):
            assert len({a, b, c, d}) == 4
            edges.add(tuple(sorted((a, b, c, d))))
        owners.setdefault(product, []).append((a, b))
    return sorted(edges)


def main():
    # Off-by-one audit of the independently written sequential counter.
    counter_cases = 0
    for n in range(1, 9):
        inputs = list(range(1, n + 1))
        for k in range(0, n + 1):
            clauses, _ = at_most_sinz(inputs, k, n + 1)
            for mask in range(1 << n):
                fixed = [(i + 1 if mask >> i & 1 else -(i + 1),)
                         for i in range(n)]
                assert dpll(clauses + fixed) == (mask.bit_count() <= k)
                counter_cases += 1
    print(f"Sinz counter exhaustive truth-table cases={counter_cases} OK")

    # Independent edge-construction agreement, larger than the tiny F audit.
    for n in range(1, 21):
        assert obstruction_edges(n) == edges_by_pair_collisions(n)
    print("edge generators agree for every n<=20 OK")

    # Definition-level exact values and full CNF satisfiability equivalence.
    # make_cnf(n,k) asks whether a valid set of size at least k+1 exists.
    exact = []
    cnf_cases = 0
    for n in range(1, 10):
        f = exact_f_bruteforce(n)
        exact.append(f)
        for k in range(0, n + 1):
            variables, clauses, _ = make_cnf(n, k)
            del variables
            assert dpll(clauses) == (f >= k + 1)
            cnf_cases += 1
    assert exact == [1, 2, 3, 4, 5, 5, 6, 6, 7]
    print(f"full-CNF/direct-definition cases={cnf_cases}, F(1..9)={exact} OK")
    print("OFF-BY-ONE AND COMPLETENESS AUDIT PASSED")


if __name__ == "__main__":
    main()
