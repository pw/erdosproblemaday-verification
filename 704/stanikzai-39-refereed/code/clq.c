/* clq.c — our own bitset branch-and-bound clique DECISION solver (erdos704 independent route).
   Usage: clq <graph.dimacs> <tau>
   Prints "SAT v1 v2 ..." (1-based DIMACS labels of a clique of size tau) or "UNSAT nodes=<k>".
   Algorithm: min-width initial order, greedy sequential bitset colouring bound (Tomita/San Segundo style).
   Written from scratch for this check; shares no code with MaxCliqueDyn, MoMC, cliquer or Glasgow. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXN 1024
#define MAXW (MAXN/64)
typedef uint64_t word;

static int n, W, tau;
static word adj[MAXN][MAXW];          /* adjacency in the REORDERED labelling */
static int orig[MAXN];                /* reordered index -> original 0-based vertex */
static int clique[MAXN], csize;
static long long nodes;
static int found;

static inline void setbit(word *b, int i) { b[i >> 6] |= (word)1 << (i & 63); }
static inline int testbit(const word *b, int i) { return (b[i >> 6] >> (i & 63)) & 1; }
static inline int popc(const word *b) { int c = 0; for (int i = 0; i < W; i++) c += __builtin_popcountll(b[i]); return c; }
static inline int empty(const word *b) { for (int i = 0; i < W; i++) if (b[i]) return 0; return 1; }

static void expand(word *P) {
    nodes++;
    int need = tau - csize;               /* clique vertices still needed */
    /* greedy sequential colouring of P; vertices with colour < need cannot complete a clique */
    int order[MAXN], col[MAXN], cnt = 0;
    word U[MAXW], Q[MAXW];
    memcpy(U, P, sizeof(word) * W);
    int k = 0;
    while (!empty(U)) {
        k++;
        memcpy(Q, U, sizeof(word) * W);
        for (int w = 0; w < W; w++) {
            while (Q[w]) {
                int b = __builtin_ctzll(Q[w]);
                int v = (w << 6) | b;
                U[w] &= ~((word)1 << b);
                Q[w] &= ~((word)1 << b);
                for (int x = 0; x < W; x++) Q[x] &= ~adj[v][x];
                if (k >= need) { order[cnt] = v; col[cnt] = k; cnt++; }
            }
        }
    }
    if (k < need) return;                  /* whole P can be coloured with fewer than need colours */
    for (int i = cnt - 1; i >= 0; i--) {
        if (col[i] < need) return;         /* colours are non-decreasing in order[] */
        int v = order[i];
        clique[csize++] = v;
        if (csize >= tau) { found = 1; return; }
        word NP[MAXW];
        for (int x = 0; x < W; x++) NP[x] = P[x] & adj[v][x];
        if (!empty(NP)) { expand(NP); if (found) return; }
        csize--;
        P[v >> 6] &= ~((word)1 << (v & 63));
    }
}

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: clq graph tau\n"); return 2; }
    tau = atoi(argv[2]);
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 2; }
    static unsigned char A[MAXN][MAXN];
    char line[256]; int m = 0, ne = 0;
    while (fgets(line, sizeof line, f)) {
        if (line[0] == 'p') { if (sscanf(line, "p edge %d %d", &n, &m) != 2) { fprintf(stderr, "bad p line\n"); return 2; } }
        else if (line[0] == 'e') {
            int a, b; if (sscanf(line, "e %d %d", &a, &b) != 2) { fprintf(stderr, "bad e line\n"); return 2; }
            if (a < 1 || b < 1 || a > n || b > n || a == b) { fprintf(stderr, "bad edge %d %d\n", a, b); return 2; }
            A[a-1][b-1] = A[b-1][a-1] = 1; ne++;
        }
    }
    fclose(f);
    if (n > MAXN) { fprintf(stderr, "n too large\n"); return 2; }
    if (ne != m) { fprintf(stderr, "edge count mismatch %d vs %d\n", ne, m); return 2; }
    W = (n + 63) / 64; if (W == 0) W = 1;
    if (tau <= 0) { printf("SAT\n"); return 0; }
    /* min-width (degeneracy) order: repeatedly remove a min-degree vertex; removed vertices go to the END */
    int deg[MAXN], removed[MAXN] = {0}, pos;
    for (int i = 0; i < n; i++) { deg[i] = 0; for (int j = 0; j < n; j++) deg[i] += A[i][j]; }
    for (pos = n - 1; pos >= 0; pos--) {
        int best = -1;
        for (int i = 0; i < n; i++) if (!removed[i] && (best < 0 || deg[i] < deg[best])) best = i;
        removed[best] = 1; orig[pos] = best;
        for (int j = 0; j < n; j++) if (A[best][j] && !removed[j]) deg[j]--;
    }
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (A[orig[i]][orig[j]]) setbit(adj[i], j);
    word P[MAXW]; memset(P, 0, sizeof P);
    for (int i = 0; i < n; i++) setbit(P, i);
    csize = 0; found = 0; nodes = 0;
    expand(P);
    if (found) {
        /* self-check before printing */
        for (int i = 0; i < tau; i++) for (int j = i + 1; j < tau; j++)
            if (!A[orig[clique[i]]][orig[clique[j]]]) { fprintf(stderr, "INTERNAL: bad clique\n"); return 3; }
        printf("SAT");
        for (int i = 0; i < tau; i++) printf(" %d", orig[clique[i]] + 1);
        printf("\n");
    } else printf("UNSAT nodes=%lld\n", nodes);
    return 0;
}
