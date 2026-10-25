#!/usr/bin/env python3
"""Exact Hamming-ball repair of the best one-violation local-search state."""

from __future__ import annotations

import argparse
import json
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

from generate_n21_cnf import ORDER, build


ARC_TEXT = """1>0 2>0 0>4 0>6 0>7 0>11 12>0 13>0 0>15 17>0 0>18 0>19 20>0 1>2 4>1 1>5 1>6 7>1 8>1 9>1 1>12 14>1 1>15 17>1 2>4 2>5 6>2 7>2 11>2 13>2 15>2 2>16 2>17 2>18 2>20 5>3 3>8 3>9 10>3 11>3 3>12 13>3 14>3 15>3 3>16 3>18 19>3 3>20 5>4 4>6 7>4 4>8 9>4 11>4 12>4 4>13 4>15 4>17 4>20 5>6 5>7 8>5 5>9 10>5 12>5 5>14 5>15 16>5 17>5 6>7 6>8 6>9 10>6 6>12 14>6 6>16 6>17 19>6 8>7 7>12 7>13 7>14 15>7 17>7 7>18 20>7 8>9 8>10 11>8 12>8 14>8 16>8 8>19 8>20 9>10 9>11 9>12 9>14 9>16 17>9 18>9 19>9 11>10 10>12 14>10 10>16 18>10 10>19 20>10 11>13 15>11 16>11 11>18 19>11 20>11 12>14 15>12 12>17 12>19 13>15 13>16 17>13 18>13 13>19 20>13 16>14 14>17 14>18 19>14 15>17 18>15 15>20 16>18 16>19 20>16 18>17 18>19 18>20 19>20"""


def near_arcs() -> set[tuple[int, int]]:
    return {tuple(map(int, token.split(">"))) for token in ARC_TEXT.split()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-changes", type=int, default=1)
    parser.add_argument("--max-changes", type=int, default=12)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--states", help="210-character lexicographic pair-state string (+,-,0)")
    args = parser.parse_args()

    if args.states:
        assert len(args.states) == ORDER * (ORDER - 1) // 2
        old_arcs=set(); at=0
        for u in range(ORDER):
            for v in range(u + 1, ORDER):
                state=args.states[at]; at+=1
                if state=="+": old_arcs.add((u,v))
                elif state=="-": old_arcs.add((v,u))
                else: assert state=="0"
    else:
        old_arcs = near_arcs()
    if not args.states:
        assert len(old_arcs) == 139
    assert all((v, u) not in old_arcs for u, v in old_arcs)
    base, pool, var = build(None, degree_bounds=True)
    old_state: dict[tuple[int, int], int] = {}
    for u in range(ORDER):
        for v in range(u + 1, ORDER):
            if (u, v) in old_arcs:
                old_state[(u, v)] = var.fwd(u, v)
            elif (v, u) in old_arcs:
                old_state[(u, v)] = var.fwd(v, u)
            else:
                old_state[(u, v)] = var.none(u, v)

    # Preserve the canonical-root profile; search only changes internal pairs.
    root_units = [[old_state[(0, v)]] for v in range(1, ORDER)]
    change_literals = [-old_state[(u, v)] for u in range(1, ORDER) for v in range(u + 1, ORDER)]

    for bound in range(args.min_changes, args.max_changes + 1):
        extra = CardEnc.atmost(
            lits=change_literals,
            bound=bound,
            vpool=pool,
            encoding=EncType.seqcounter,
        ).clauses
        started = time.perf_counter()
        with Solver(name=args.solver, bootstrap_with=base.clauses + root_units + extra) as solver:
            sat = solver.solve()
            elapsed = time.perf_counter() - started
            print(f"bound={bound} status={'SAT' if sat else 'UNSAT'} seconds={elapsed:.3f}", flush=True)
            if not sat:
                continue
            true = {literal for literal in solver.get_model() if literal > 0}
        arcs=[]; nonedges=[]; changes=[]
        for u in range(ORDER):
            for v in range(u + 1, ORDER):
                if var.fwd(u, v) in true:
                    arcs.append((u,v)); literal=var.fwd(u,v)
                elif var.fwd(v, u) in true:
                    arcs.append((v,u)); literal=var.fwd(v,u)
                else:
                    nonedges.append((u,v)); literal=var.none(u,v)
                if literal != old_state[(u,v)]: changes.append((u,v))
        print(json.dumps({"status":"SAT","bound":bound,"changes":changes,"arcs":arcs,"nonedges":nonedges},separators=(",", ":")))
        return
    print("NO REPAIR WITHIN REQUESTED HAMMING BALL")


if __name__ == "__main__":
    main()
