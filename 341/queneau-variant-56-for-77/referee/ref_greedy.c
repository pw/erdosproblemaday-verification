/* Referee's own greedy for Erdos #341 (rule D) and Queneau's variant (rule Q).
 * Written from the problem statement only (not from any project code).
 * Algorithm: direct representation search, NOT a bitset sieve.
 *   For each candidate t > max(seed), in increasing order, scan the already-selected
 *   elements u (ascending) with 2u <= t and test whether t-u is selected.
 *   rule Q: a representation needs u != t-u (distinct terms; for a strictly increasing
 *           sequence distinct indices <=> distinct values).
 *   rule D: u == t-u allowed.
 *   t is selected iff no representation exists.  Every element of the seed is kept as is
 *   (the rule applies only to terms after the seed).
 * Usage: ref_greedy Q|D LIMIT OUTFILE s1,s2,...,sk
 * Output: selected elements <= LIMIT, one per line (seed included).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage: %s Q|D LIMIT OUTFILE seedlist\n", argv[0]); return 2; }
    char rule = argv[1][0];
    if (rule != 'Q' && rule != 'D') { fprintf(stderr, "rule must be Q or D\n"); return 2; }
    long L = atol(argv[2]);
    unsigned char *in = calloc(L + 1, 1);
    uint32_t *el = malloc(sizeof(uint32_t) * (L + 1));
    long n = 0, smax = 0;
    char *s = strdup(argv[4]);
    for (char *tok = strtok(s, ","); tok; tok = strtok(NULL, ",")) {
        long v = atol(tok);
        if (v <= 0 || v > L) { fprintf(stderr, "bad seed element %ld\n", v); return 2; }
        if (v <= smax) { fprintf(stderr, "seed must be strictly increasing\n"); return 2; }
        in[v] = 1; el[n++] = (uint32_t)v; smax = v;
    }
    long seedn = n;
    for (long t = smax + 1; t <= L; t++) {
        int rep = 0;
        for (long i = 0; i < n; i++) {
            long u = el[i];
            if (2 * u > t) break;
            long v = t - u;
            if (v == u && rule == 'Q') continue;   /* equal summands forbidden under Q */
            if (in[v]) { rep = 1; break; }
        }
        if (!rep) { in[t] = 1; el[n++] = (uint32_t)t; }
    }
    FILE *f = fopen(argv[3], "w");
    for (long i = 0; i < n; i++) fprintf(f, "%u\n", el[i]);
    fclose(f);
    fprintf(stderr, "rule=%c limit=%ld seed_size=%ld total_selected=%ld last=%u\n",
            rule, L, seedn, n, el[n - 1]);
    return 0;
}
