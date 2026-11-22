# build_witnesses.py: builds every arc list in this record from its connection sets.
# Written 2026-11-20 (Claude Opus 5.5, under the author's direction). No libraries.
# Usage: python3 -I build_witnesses.py OUTDIR
# Output per graph: <name>.txt (arc list) and <name>.def.txt (its definition).
# Arc list format: first line "N A" (N vertices numbered 0..N-1, A arcs), then
# A lines "u v", each meaning the arc u -> v. Lines are sorted; no comments.
import sys, os

def circulant(N, S):
    # vertices Z_N; arc x -> x+s (mod N) for every s in S
    return {(x, (x + s) % N) for x in range(N) for s in S}

def bicirculant(p, S):
    # vertices Z_p x {0,1}; vertex (x,i) is numbered p*i + x;
    # arc (x,i) -> (x+s, j) for every s in S[(i,j)]
    A = set()
    for (i, j), Sij in S.items():
        for x in range(p):
            for s in Sij:
                A.add((p * i + x, p * j + (x + s) % p))
    return A

def bic_text(p, S):
    return ("Bicirculant on Z_%d x {0,1}. Vertex (x,i) is numbered %d*i + x.\n"
            "Arc (x,i) -> (x+s mod %d, j) for every s in S_ij:\n" % (p, p, p) +
            "".join("  S_%d%d = {%s}\n" % (i, j, ", ".join(map(str, S[(i, j)])))
                    for (i, j) in ((0, 0), (0, 1), (1, 0), (1, 1))))

def circ_text(N, S):
    return ("Circulant on Z_%d. Arc x -> x+s mod %d for every s in\n"
            "  S = {%s}  (|S| = %d; S and -S are disjoint mod %d)\n" % (N, N, ", ".join(map(str, S)), len(S), N))

G38 = {(0, 0): [5, 6, 16, 17], (0, 1): [16, 17], (1, 0): [5, 6], (1, 1): [10, 11, 16, 17]}
G46 = {(0, 0): [2, 5, 11, 19], (0, 1): [4, 10, 18], (1, 0): [0, 8, 17], (1, 1): [2, 11, 19, 20]}
S77 = [3, 11, 14, 19, 20, 22, 30, 35, 36, 40, 44, 46, 52, 64, 68, 75]
S70 = [1, 2, 7, 8, 14, 15, 16, 17, 21, 24, 26, 29, 30, 32, 37, 39, 45, 47, 48, 52, 60, 61, 64]
S69 = [16, 19, 27, 30, 32, 33, 35, 41, 43, 44, 46, 48, 49, 51, 55, 57, 58, 59, 60, 62, 63, 64, 65, 67]

# name: (N, arcs, definition, claim)
GRAPHS = {
 'witness_k73_ge39_N38': (38, bicirculant(19, G38), bic_text(19, G38),
     'k(7,3) >= 39: no transitive triangle and no 7 pairwise non-adjacent vertices'),
 'witness_k83_ge47_N46': (46, bicirculant(23, G46), bic_text(23, G46),
     'k(8,3) >= 47: no transitive triangle and no 8 pairwise non-adjacent vertices'),
 'witness_k64_ge78_N77': (77, circulant(77, S77), circ_text(77, S77),
     'k(6,4) >= 78: no transitive tournament on 4 vertices and no 6 pairwise non-adjacent vertices'),
 'witness_k36_ge71_N70': (70, circulant(70, S70), circ_text(70, S70),
     'k(3,6) >= 71: no transitive tournament on 6 vertices and no 3 pairwise non-adjacent vertices'),
 'witness_k36_ge70_N69': (69, circulant(69, S69), circ_text(69, S69),
     'k(3,6) >= 70 (weaker; a second, different graph): no transitive tournament on 6 vertices and no 3 pairwise non-adjacent vertices'),
 # controls: published graphs, used only to test the checkers
 'control_B8_k33_ge9': (8, circulant(8, [1, 6]), circ_text(8, [1, 6]),
     'control: Bermond\'s graph, k(3,3) >= 9'),
 'control_Z14_k43_ge15': (14, {(x, (x + 1) % 14) for x in range(14)} | {(x, (x - 2) % 14) for x in range(14)}
     | {(x, (x + 4) % 14) for x in range(0, 14, 2)} | {(x, (x - 6) % 14) for x in range(1, 14, 2)},
     'Ihringer, Rajendraprasad and Weinert (2021), Observation 4.1: vertices Z_14; arcs x -> x+1 and\n'
     '  x -> x-2 for every x; x -> x+4 for even x; x -> x-6 for odd x\n',
     'control: k(4,3) >= 15'),
 'control_Z28_k63_ge29': (28, circulant(28, [3, 8, 10, 12, 17]), circ_text(28, [3, 8, 10, 12, 17]),
     'control: Kirtchakov\'s circulant (Zenodo 10.5281/zenodo.21890619), k(6,3) >= 29'),
}

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for name, (N, A, text, claim) in GRAPHS.items():
    assert all(a != b for a, b in A), name
    with open(os.path.join(out, name + '.txt'), 'w') as f:
        f.write('%d %d\n' % (N, len(A)))
        for a, b in sorted(A):
            f.write('%d %d\n' % (a, b))
    with open(os.path.join(out, name + '.def.txt'), 'w') as f:
        f.write('%s\nClaim: %s\nVertices: %d. Arcs: %d. Arc list: %s.txt\n\n%s'
                % (name, claim, N, len(A), name, text))
    print('%s: N=%d arcs=%d' % (name, N, len(A)))
