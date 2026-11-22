/* Seat O's own backtracker (written from scratch): counts labelled oriented graphs on n<=32
   vertices with no transitive triangle and no independent k-set, extending a partial
   assignment read from stdin.
   stdin: n k maxsol
          then lines "A i j" (arc i->j fixed) or "N i j" (i,j fixed non-adjacent), terminated by "E".
   Every remaining unordered pair is branched over {none, i->j, j->i}.
   A violation is detected exactly when its last pair is decided. */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint32_t u32;
static int n, k;
static long long maxsol, nsol = 0, nodes = 0;
static u32 OUT[32], IN[32], NON[32];
static int pi[600], pj[600], np = 0;
static int dec[32][32];

static int clique(u32 C, int r) {           /* is there an r-clique in the decided-none graph inside C? */
    if (r == 0) return 1;
    while (C) {
        int z = __builtin_ctz(C); C &= C - 1;
        if (__builtin_popcount(C) < r - 1) return 0;
        if (clique(C & NON[z], r - 1)) return 1;
    }
    return 0;
}
static int set_arc(int i, int j) {          /* returns 1 if a violation appears */
    OUT[i] |= 1u << j; IN[j] |= 1u << i; dec[i][j] = dec[j][i] = 1;
    if (OUT[i] & OUT[j]) return 1;          /* i->j, j->z, i->z */
    if (IN[i] & IN[j]) return 1;            /* z->i, i->j, z->j */
    if (OUT[i] & IN[j] & ~(1u << j) & ~(1u << i)) {  /* i->z, z->j with i->j */
        return 1;
    }
    return 0;
}
static void unset_arc(int i, int j) { OUT[i] &= ~(1u << j); IN[j] &= ~(1u << i); dec[i][j] = dec[j][i] = 0; }
static int set_non(int i, int j) {
    NON[i] |= 1u << j; NON[j] |= 1u << i; dec[i][j] = dec[j][i] = 1;
    return clique(NON[i] & NON[j], k - 2);
}
static void unset_non(int i, int j) { NON[i] &= ~(1u << j); NON[j] &= ~(1u << i); dec[i][j] = dec[j][i] = 0; }

static void dfs(int t) {
    nodes++;
    if (maxsol && nsol >= maxsol) return;
    if (t == np) {
        nsol++;
        if (nsol <= 3) {                       /* print the first solutions as arc lists */
            printf("SOL");
            for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (OUT[i] >> j & 1) printf(" %d>%d", i, j);
            printf("\n");
        }
        return;
    }
    int i = pi[t], j = pj[t];
    if (!set_non(i, j)) dfs(t + 1);
    unset_non(i, j);
    if (!set_arc(i, j)) dfs(t + 1);
    unset_arc(i, j);
    if (!set_arc(j, i)) dfs(t + 1);
    unset_arc(j, i);
}
int main(void) {
    if (scanf("%d %d %lld", &n, &k, &maxsol) != 3) return 2;
    if (n > 32 || k < 2) return 2;
    char c[4]; int a, b, bad = 0;
    while (scanf("%3s", c) == 1 && c[0] != 'E') {
        if (scanf("%d %d", &a, &b) != 2) return 2;
        if (a == b || a < 0 || b < 0 || a >= n || b >= n || dec[a][b]) { fprintf(stderr, "bad pair %d %d\n", a, b); return 2; }
        if (c[0] == 'A') bad |= set_arc(a, b); else bad |= set_non(a, b);
    }
    if (bad) { printf("fixed part already violates constraints\nCOUNT 0 nodes 0\n"); return 0; }
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (!dec[i][j]) { pi[np] = i; pj[np] = j; np++; }
    dfs(0);
    printf("free_pairs %d COUNT %lld nodes %lld%s\n", np, nsol, nodes, (maxsol && nsol >= maxsol) ? " (stopped at maxsol)" : "");
    return 0;
}
