/* Independent exhaustive check (no SAT solver, no symmetry breaking) of the small facts
   the k(6,3) <= 32 argument uses.

   Mode "count n m": count labelled oriented graphs on n vertices with no transitive
   triangle and no independent m-set (plain backtracking over all n(n-1)/2 pairs, each
   none / i->j / j->i).
   Mode "glue8": count 14-vertex oriented graphs with no transitive triangle and no
   independent 4-set in which vertex 0 has N+(0) = {1,2,3}, N-(0) = {4,5} (mode glue8)
   or N+(0) = {1,2}, N-(0) = {3,4,5} (mode glue8r), and the non-neighbourhood {6..13}
   induces Bermond's graph (i -> i+1, i -> i-2 mod 8 on 6..13). Every other pair among
   0..13 is free (all three states tried).

   A transitive triangle is an ordered triple x->y, y->z, x->z. Pairs are assigned one at
   a time; a triangle is checked when its last pair is assigned; an m-set is rejected when
   its last pair is assigned 'none' and all its pairs are 'none'. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 16
static int n, m;
static int st[MAXN][MAXN];      /* -1 unassigned, 0 none, 1 i->j (stored at [i][j] and [j][i] as 1 / 2) */
static int npairs, pa[MAXN * MAXN], pb[MAXN * MAXN];
static long long count;
static int limit_print = 3;

/* state from a's point of view: 0 none, 1 a->b, 2 b->a, -1 unassigned */
static inline int arc(int a, int b) { return st[a][b] == 1; }

static int tt_ok(int a, int b) {
    for (int c = 0; c < n; c++) {
        if (c == a || c == b) continue;
        if (st[a][c] < 0 || st[b][c] < 0) continue;
        if (st[a][c] == 0 || st[b][c] == 0 || st[a][b] == 0) continue;
        /* all three adjacent: check every ordering for x->y, y->z, x->z */
        int v[3] = {a, b, c};
        for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) for (int z = 0; z < 3; z++) {
            if (x == y || y == z || x == z) continue;
            if (arc(v[x], v[y]) && arc(v[y], v[z]) && arc(v[x], v[z])) return 0;
        }
    }
    return 1;
}

/* is there an independent m-set containing a and b, all pairs assigned none? */
static int indep_rec(int *cand, int nc, int need) {
    if (need == 0) return 1;
    for (int i = 0; i < nc; i++) {
        int c = cand[i];
        int nxt[MAXN], k = 0;
        for (int j = i + 1; j < nc; j++) if (st[c][cand[j]] == 0) nxt[k++] = cand[j];
        if (k + 1 < need) continue;
        if (indep_rec(nxt, k, need - 1)) return 1;
    }
    return 0;
}

static int indep_ok(int a, int b) {
    if (st[a][b] != 0) return 1;
    int cand[MAXN], k = 0;
    for (int c = 0; c < n; c++) if (c != a && c != b && st[a][c] == 0 && st[b][c] == 0) cand[k++] = c;
    return !indep_rec(cand, k, m - 2);
}

static void setp(int a, int b, int s) {
    if (s < 0) { st[a][b] = st[b][a] = -1; return; }
    if (s == 0) { st[a][b] = st[b][a] = 0; return; }
    if (s == 1) { st[a][b] = 1; st[b][a] = 2; } else { st[a][b] = 2; st[b][a] = 1; }
}

static void rec(int k) {
    if (k == npairs) {
        count++;
        if (count <= limit_print && n > 8) {
            printf("solution %lld:", count);
            for (int i = 0; i < n; i++) { printf(" %d:", i); for (int j = 0; j < n; j++) if (st[i][j] == 1) printf("%d,", j); }
            printf("\n");
        }
        return;
    }
    int a = pa[k], b = pb[k];
    for (int s = 0; s < 3; s++) {
        setp(a, b, s);
        if (tt_ok(a, b) && indep_ok(a, b)) rec(k + 1);
    }
    setp(a, b, -1);
}

int main(int argc, char **argv) {
    memset(st, -1, sizeof st);
    if (argc >= 4 && !strcmp(argv[1], "count")) {
        n = atoi(argv[2]); m = atoi(argv[3]);
        npairs = 0;
        for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) { pa[npairs] = i; pb[npairs] = j; npairs++; }
        rec(0);
        printf("count n=%d m=%d: %lld labelled oriented graphs with no transitive triangle and no independent %d-set\n", n, m, count, m);
        return 0;
    }
    if (argc >= 2 && (!strcmp(argv[1], "glue8") || !strcmp(argv[1], "glue8r"))) {
        int rev = !strcmp(argv[1], "glue8r");
        n = 14; m = 4;
        int outs = rev ? 2 : 3;
        for (int w = 1; w <= 5; w++) setp(0, w, w <= outs ? 1 : 2);
        for (int w = 6; w < 14; w++) setp(0, w, 0);
        for (int i = 0; i < 8; i++) for (int j = 0; j < 8; j++) if (i < j) setp(6 + i, 6 + j, 0);
        for (int i = 0; i < 8; i++) { setp(6 + i, 6 + (i + 1) % 8, 1); setp(6 + i, 6 + (i + 6) % 8, 1); }
        /* sanity: the fixed part must itself be valid */
        for (int a = 0; a < 14; a++) for (int b = a + 1; b < 14; b++)
            if (st[a][b] >= 0 && (!tt_ok(a, b) || !indep_ok(a, b))) { printf("fixed part invalid at %d %d\n", a, b); return 1; }
        npairs = 0;
        for (int w = 1; w <= 5; w++) {
            for (int c = 6; c < 14; c++) { pa[npairs] = w; pb[npairs] = c; npairs++; }
            for (int v = 1; v < w; v++) { pa[npairs] = v; pb[npairs] = w; npairs++; }
        }
        rec(0);
        printf("%s: %lld completions (14 vertices, I_4-free, L_3-free, vertex 0 of degree 5 with I(0) = Bermond graph)\n", argv[1], count);
        return 0;
    }
    if (argc >= 7 && !strcmp(argv[1], "glue")) {
        /* glue N M dout din file: vertex 0 with N+(0) = 1..dout, N-(0) = next din,
           non-neighbourhood = the graph in file (adjacency list on h vertices). */
        n = atoi(argv[2]); m = atoi(argv[3]);
        int dout = atoi(argv[4]), din = atoi(argv[5]);
        int base = 1 + dout + din, h = n - base;
        for (int w = 1; w < base; w++) setp(0, w, w <= dout ? 1 : 2);
        for (int w = base; w < n; w++) setp(0, w, 0);
        for (int i = base; i < n; i++) for (int j = i + 1; j < n; j++) setp(i, j, 0);
        FILE *f = fopen(argv[6], "r"); char line[4096]; int rows = 0;
        while (fgets(line, sizeof line, f)) {
            if (line[0] == '#' || line[0] == '\n') continue;
            char *p = line; int v = strtol(p, &p, 10); if (*p == ':') p++;
            while (1) { char *q; long w = strtol(p, &q, 10); if (q == p) break; p = q; setp(base + v, base + (int)w, 1); }
            rows++;
        }
        fclose(f);
        if (rows != h) { printf("file has %d rows, expected %d\n", rows, h); return 1; }
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++)
            if (st[a][b] >= 0 && (!tt_ok(a, b) || !indep_ok(a, b))) { printf("fixed part invalid at %d %d\n", a, b); return 1; }
        npairs = 0;
        for (int w = 1; w < base; w++) {
            for (int c = base; c < n; c++) { pa[npairs] = w; pb[npairs] = c; npairs++; }
            for (int v = 1; v < w; v++) { pa[npairs] = v; pb[npairs] = w; npairs++; }
        }
        rec(0);
        printf("glue n=%d m=%d frame (%d,%d) I(0) from %s: %lld completions\n", n, m, dout, din, argv[6], count);
        return 0;
    }
    fprintf(stderr, "usage: verify_small count n m | glue8 | glue8r | glue N M dout din file\n");
    return 1;
}
