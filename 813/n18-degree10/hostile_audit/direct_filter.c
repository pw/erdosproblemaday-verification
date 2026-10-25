/* Independent exhaustive filter for the order <=10 neighbourhood census.
 *
 * Input and output are graph6, one graph per line.  A graph is emitted iff
 * it has no K4 and every seven vertices contain a triangle.  This code was
 * written for the hostile audit and shares no implementation with the
 * producer's recursive census_tool filter.
 *
 * The second condition is checked by forming the union, over the graph's
 * triangles, of the seven-sets containing each triangle.  At order 10 there
 * are only 120 seven-sets, so two uint64_t words suffice.
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint64_t cover_lo[1 << 10];
static uint64_t cover_hi[1 << 10];
static uint64_t target_lo, target_hi;
static int prepared_n = -1;

static void prepare(int n) {
    uint16_t seven[120];
    int nseven = 0;
    if (n < 7 || n > 10) {
        fprintf(stderr, "direct_filter supports only orders 7..10\n");
        exit(2);
    }
    memset(cover_lo, 0, sizeof cover_lo);
    memset(cover_hi, 0, sizeof cover_hi);
    for (uint16_t s = 0; s < (1u << n); ++s)
        if (__builtin_popcount((unsigned)s) == 7) seven[nseven++] = s;

    for (uint16_t t = 0; t < (1u << n); ++t) {
        if (__builtin_popcount((unsigned)t) != 3) continue;
        for (int i = 0; i < nseven; ++i) {
            if ((seven[i] & t) != t) continue;
            if (i < 64) cover_lo[t] |= UINT64_C(1) << i;
            else cover_hi[t] |= UINT64_C(1) << (i - 64);
        }
    }
    if (nseven >= 64) target_lo = UINT64_MAX;
    else target_lo = nseven ? ((UINT64_C(1) << nseven) - 1) : 0;
    if (nseven <= 64) target_hi = 0;
    else target_hi = (UINT64_C(1) << (nseven - 64)) - 1;
    prepared_n = n;
}

static int parse_graph6(const char *line, uint16_t adj[10], int *n_out) {
    unsigned char first = (unsigned char)line[0];
    if (first < 70 || first > 73) return -1; /* orders 7..10 */
    int n = first - 63;
    memset(adj, 0, 10 * sizeof *adj);
    int remaining = 0, value = 0;
    const unsigned char *p = (const unsigned char *)line + 1;
    for (int v = 1; v < n; ++v) {
        for (int u = 0; u < v; ++u) {
            if (!remaining) {
                if (*p < 63 || *p > 126) return -1;
                value = *p++ - 63;
                remaining = 6;
            }
            if ((value >> (--remaining)) & 1) {
                adj[u] |= (uint16_t)(1u << v);
                adj[v] |= (uint16_t)(1u << u);
            }
        }
    }
    *n_out = n;
    return 0;
}

static int has_k4(const uint16_t adj[10], int n) {
    for (int a = 0; a < n; ++a)
        for (int b = a + 1; b < n; ++b) {
            if (!((adj[a] >> b) & 1)) continue;
            for (int c = b + 1; c < n; ++c) {
                if (!((adj[a] >> c) & 1) || !((adj[b] >> c) & 1)) continue;
                for (int d = c + 1; d < n; ++d)
                    if (((adj[a] >> d) & 1) && ((adj[b] >> d) & 1) &&
                        ((adj[c] >> d) & 1))
                        return 1;
            }
        }
    return 0;
}

static int every_seven_has_triangle(const uint16_t adj[10], int n) {
    uint64_t got_lo = 0, got_hi = 0;
    for (int a = 0; a < n; ++a)
        for (int b = a + 1; b < n; ++b) {
            if (!((adj[a] >> b) & 1)) continue;
            for (int c = b + 1; c < n; ++c) {
                if (((adj[a] >> c) & 1) && ((adj[b] >> c) & 1)) {
                    uint16_t t = (uint16_t)((1u << a) | (1u << b) | (1u << c));
                    got_lo |= cover_lo[t];
                    got_hi |= cover_hi[t];
                }
            }
        }
    return got_lo == target_lo && got_hi == target_hi;
}

int main(void) {
    char line[256];
    long long read_count = 0, write_count = 0;
    while (fgets(line, sizeof line, stdin)) {
        size_t len = strlen(line);
        while (len && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            line[--len] = 0;
        if (!len || !strcmp(line, ">>graph6<<")) continue;
        uint16_t adj[10];
        int n;
        if (parse_graph6(line, adj, &n)) {
            fprintf(stderr, "bad graph6 input at graph %lld\n", read_count);
            return 3;
        }
        if (n != prepared_n) prepare(n);
        ++read_count;
        if (!has_k4(adj, n) && every_seven_has_triangle(adj, n)) {
            puts(line);
            ++write_count;
        }
    }
    fprintf(stderr, "[independent direct_filter] read=%lld wrote=%lld\n",
            read_count, write_count);
    return 0;
}
