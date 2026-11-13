/* clq2.c — batch version of clq.c: our own bitset branch-and-bound clique DECISION solver.
   Usage: clq2 <global.dimacs> <leaves.txt>   (leaf line: id tau k v1..vk, 1-based global labels)
   Output per leaf: "id SAT g1 .. g_tau" (global labels) or "id UNSAT nodes=<k>".  Shares no code with the
   submission's solvers (MaxCliqueDyn, MoMC, cliquer, Glasgow). Same algorithm as clq.c (tested vs networkx). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define MAXN 1024
#define MAXW (MAXN/64)
#define GMAX 4096
typedef uint64_t word;
static int n, W, tau;
static word adj[MAXN][MAXW];
static int orig[MAXN];
static int clique[MAXN], csize, found;
static long long nodes;
static unsigned char *GA; static int GN;
#define GADJ(a,b) GA[(size_t)(a)*GN+(b)]
static inline void setbit(word *b, int i) { b[i >> 6] |= (word)1 << (i & 63); }
static inline int empty(const word *b) { for (int i = 0; i < W; i++) if (b[i]) return 0; return 1; }
static void expand(word *P) {
    nodes++;
    int need = tau - csize;
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
    if (k < need) return;
    for (int i = cnt - 1; i >= 0; i--) {
        if (col[i] < need) return;
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
    if (argc != 3) { fprintf(stderr, "usage: clq2 global leaves\n"); return 2; }
    FILE *f = fopen(argv[1], "r"); if (!f) { perror("graph"); return 2; }
    char line[256]; int m = 0, ne = 0;
    while (fgets(line, sizeof line, f)) {
        if (line[0] == 'p') { sscanf(line, "p edge %d %d", &GN, &m); GA = calloc((size_t)GN * GN, 1); }
        else if (line[0] == 'e') { int a, b; sscanf(line, "e %d %d", &a, &b);
            if (a < 1 || b < 1 || a > GN || b > GN || a == b) { fprintf(stderr, "bad edge\n"); return 2; }
            GADJ(a-1,b-1) = GADJ(b-1,a-1) = 1; ne++; }
    }
    fclose(f);
    if (ne != m) { fprintf(stderr, "edge count mismatch\n"); return 2; }
    FILE *L = fopen(argv[2], "r"); if (!L) { perror("leaves"); return 2; }
    static int vs[MAXN];
    long id; int k;
    while (fscanf(L, "%ld %d %d", &id, &tau, &k) == 3) {
        if (k > MAXN) { fprintf(stderr, "leaf too big\n"); return 2; }
        for (int i = 0; i < k; i++) { if (fscanf(L, "%d", &vs[i]) != 1) { fprintf(stderr, "short leaf\n"); return 2; } vs[i]--; }
        n = k; W = (n + 63) / 64; if (W == 0) W = 1;
        /* min-width order */
        static int deg[MAXN], removed[MAXN];
        for (int i = 0; i < n; i++) { removed[i] = 0; deg[i] = 0; for (int j = 0; j < n; j++) deg[i] += GADJ(vs[i], vs[j]); }
        for (int pos = n - 1; pos >= 0; pos--) {
            int best = -1;
            for (int i = 0; i < n; i++) if (!removed[i] && (best < 0 || deg[i] < deg[best])) best = i;
            removed[best] = 1; orig[pos] = best;
            for (int j = 0; j < n; j++) if (GADJ(vs[best], vs[j]) && !removed[j]) deg[j]--;
        }
        memset(adj, 0, sizeof(word) * MAXW * n);
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (GADJ(vs[orig[i]], vs[orig[j]])) setbit(adj[i], j);
        word P[MAXW]; memset(P, 0, sizeof P);
        for (int i = 0; i < n; i++) setbit(P, i);
        csize = 0; found = 0; nodes = 0;
        if (tau <= 0) found = 1; else expand(P);
        if (found) {
            for (int i = 0; i < tau; i++) for (int j = i + 1; j < tau; j++)
                if (!GADJ(vs[orig[clique[i]]], vs[orig[clique[j]]])) { fprintf(stderr, "INTERNAL bad clique\n"); return 3; }
            printf("%ld SAT", id);
            for (int i = 0; i < tau; i++) printf(" %d", vs[orig[clique[i]]] + 1);
            printf("\n");
        } else printf("%ld UNSAT nodes=%lld\n", id, nodes);
        fflush(stdout);
    }
    return 0;
}
