/* refdfs.c -- referee's independent exact profile for Erdos #301 blocks.
   x-space: candidate d -> x = L/d (L = lcm of candidates); a set is solution-free iff no chosen x
   is a sum of distinct smaller chosen x's.  F(t) in {F(prev), F(prev)+1}; a set of size F(prev)+1
   must contain the new element t (smallest x).  Decide it by include/exclude search over x ascending,
   reach = bitset of subset sums of chosen, bound = chosen + #{remaining x not in reach} >= K.
   usage: refdfs M Tmax     |   refdfs -n N   (F on {1..n}, n=1..N)       BUG=1 env: negative control */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64;
static int n, K, BUG;
static long long xs[128], ds[128];
static long long W;            /* words per bitset */
static u64 *buf;               /* (K+1) * W */
static long long nodes;
static int cur[128], sol[128];
static int Fprof[4096];   /* Fprof[k] = F(D[0..k]) computed so far (Russian-doll bound) */
static int RD;

static inline int getbit(const u64 *b, long long i) { return (b[i >> 6] >> (i & 63)) & 1; }
static void shift_or(u64 *dst, const u64 *src, long long s) {   /* dst = src | src<<s */
    long long ws = s >> 6; int bs = s & 63;
    for (long long i = W - 1; i >= 0; i--) {
        u64 v = src[i]; long long j = i - ws;
        if (j >= 0) { u64 p = src[j] << bs; if (bs && j >= 1) p |= src[j - 1] >> (64 - bs); v |= p; }
        dst[i] = v;
    }
}
static int dfs(int i, int c, const u64 *reach) {
    nodes++;
    if (c == K) { memcpy(sol, cur, sizeof(int) * K); return 1; }
    int avail = 0;
    for (int j = i; j < n; j++) if (!getbit(reach, xs[j])) avail++;
    if (c + avail < K) return 0;
    if (i >= n) return 0;
    if (RD && c + Fprof[n - 1 - i] < K) return 0;   /* chosen suffix = subset of D cap [1, d_i], itself solution-free */
    if (!getbit(reach, xs[i])) {
        u64 *nx = buf + (long long)(c + 1) * W;
        if (BUG == 1) { memcpy(nx, reach, W * 8); nx[xs[i] >> 6] |= 1ULL << (xs[i] & 63); } /* BUG: forgets multi-term sums */
        else shift_or(nx, reach, xs[i]);
        cur[c] = i;
        if (dfs(i + 1, c + 1, nx)) return 1;
    }
    return dfs(i + 1, c, reach);
}
static long long gcdll(long long a, long long b) { while (b) { long long t = a % b; a = b; b = t; } return a; }
/* decide: does D_cands (ds[0..n-1] ascending d) have a solution-free set of size K containing ds[n-1]? */
static int decide(int nc, int k) {
    long long L = 1;
    for (int j = 0; j < nc; j++) L = L / gcdll(L, ds[j]) * ds[j];
    n = nc; K = k;
    for (int j = 0; j < nc; j++) xs[j] = L / ds[nc - 1 - j];  /* ascending x */
    W = (xs[n - 1] >> 6) + 1;
    buf = calloc((size_t)(K + 1) * W, 8);
    if (!buf) { fprintf(stderr, "oom\n"); exit(3); }
    buf[0] = 1;                                   /* reach = {0} */
    shift_or(buf + W, buf, xs[0]);                /* forced: include new element (smallest x) */
    cur[0] = 0;
    int r = dfs(1, 1, buf + W);
    free(buf);
    return r;
}
int main(int argc, char **argv) {
    BUG = getenv("BUG") ? atoi(getenv("BUG")) : 0;
    RD = getenv("RD") ? atoi(getenv("RD")) : 0;
    long long D[4096]; int nd = 0;
    if (argc == 3 && strcmp(argv[1], "-n") == 0) {
        int N = atoi(argv[2]); for (int d = 1; d <= N; d++) D[nd++] = d;
    } else {
        long long M = atoll(argv[1]), T = atoll(argv[2]);
        for (long long d = 1; d <= T && d <= M; d++) if (M % d == 0) D[nd++] = d;
    }
    int F = 0;
    for (int k = 1; k <= nd; k++) {
        for (int j = 0; j < k; j++) ds[j] = D[j];
        nodes = 0;
        int inc = decide(k, F + 1);
        if (inc) F++;
        Fprof[k - 1] = F;
        printf("t=%lld n=%d F=%d h=%d nodes=%lld", D[k - 1], k, F, k - F, nodes);
        if (inc) { printf(" set="); for (int j = 0; j < F; j++) printf("%lld%s", ds[k - 1 - sol[j]], j + 1 < F ? "," : ""); }
        printf("\n"); fflush(stdout);
    }
    return 0;
}
