#!/usr/bin/env python3
"""Write control / pre-deletion sets from the DEFINITIONS (no use of simple.c).

usage: mksets.py KIND N [L] > file
  full      : [1, N]
  third     : (N/3, N]           (all integers above N/3)
  quarter   : (N/4, N]
  pre       : top half [ceil(N/2), N]  U  L-rough a in (N/3, N/2)   (before deletions)
  c236      : {2, 3, 6}
  c23742    : {2, 3, 7, 42}      (only a length-3 relation: 1/2 = 1/3 + 1/7 + 1/42)
"""
import sys


def rough(a, L):
    return all(a % p for p in range(2, L) if all(p % q for q in range(2, p)))


def main():
    kind, N = sys.argv[1], int(sys.argv[2])
    L = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    if kind == "full":
        s = range(1, N + 1)
    elif kind == "third":
        s = [x for x in range(1, N + 1) if 3 * x > N]
    elif kind == "quarter":
        s = [x for x in range(1, N + 1) if 4 * x > N]
    elif kind == "pre":
        s = [a for a in range(1, N + 1) if 3 * a > N and 2 * a < N and rough(a, L)]
        s += list(range((N + 1) // 2, N + 1))
    elif kind == "c236":
        s = [2, 3, 6]
    elif kind == "c23742":
        s = [2, 3, 7, 42]
    else:
        raise SystemExit("unknown kind")
    sys.stdout.write("".join(f"{x}\n" for x in s))


if __name__ == "__main__":
    main()
