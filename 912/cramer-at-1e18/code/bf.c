// bf.c — brute force for Erdős #912.
// h(n) = number of distinct exponents in the prime factorisation of n!.
// Walk n = 1..N, keep e[p] = v_p(n!) and cnt[v] = #{p : e[p] = v}; h = #{v >= 1 : cnt[v] > 0}.
// Checks, for every step n -> m = n+1:
//   (A) |h(m) - h(n)| <= 1
//   (I) isolation: every prime q | m with q*q <= m has a value held by q alone, before (e) and after (e')
//       [the one known exception is m = 4, n = 3, where e(2) = e(3) = 1]
//   (R) jump rule, predicted from PRE-step counts only, ignoring every small prime factor:
//       if m has a prime factor Q with Q*Q > m, k = m/Q:
//           pred = [cnt_n(k) == 0] - [k >= 2 && cnt_n(k-1) == 1]
//       else pred = 0.     Then actual Δh must equal pred.
// Output: h(n) for n <= 10000 (b-file check), checkpoints, step statistics.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#ifndef ISOMUL
#define ISOMUL 1
#endif
#ifndef STEPBOUND
#define STEPBOUND 1
#endif

int main(int argc, char **argv) {
    uint64_t N = argc > 1 ? strtoull(argv[1], 0, 10) : 100000000ULL;
    const char *bfile = argc > 2 ? argv[2] : "bf_small.txt";
    uint64_t STEP = argc > 3 ? strtoull(argv[3], 0, 10) : 0;
    uint32_t *spf = calloc(N + 2, 4);
    uint32_t *e = calloc(N + 2, 4);
    uint32_t *cnt = calloc(N + 2, 4);
    if (!spf || !e || !cnt) { fprintf(stderr, "alloc failed\n"); return 2; }
    for (uint64_t i = 2; i <= N + 1; i++) if (!spf[i]) for (uint64_t j = i; j <= N + 1; j += i) if (!spf[j]) spf[j] = (uint32_t)i;
    FILE *fs = fopen(bfile, "w");
    int64_t h = 0;                      // h(1) = 0
    fprintf(fs, "1 0\n");
    uint64_t up = 0, down = 0, zero = 0, failA = 0, failI = 0, failR = 0, failQ = 0, iso_checks = 0;
    uint64_t next_cp = 10;
    for (uint64_t m = 2; m <= N; m++) {
        // factor m
        uint32_t ps[16], vs[16]; int np = 0; uint64_t t = m;
        while (t > 1) { uint32_t p = spf[t]; uint32_t v = 0; while (t % p == 0) { t /= p; v++; } ps[np] = p; vs[np] = v; np++; }
        // prediction from pre-step counts
        int64_t pred = 0; int haveQ = 0;
        uint32_t Q = ps[np - 1];
        if ((uint64_t)Q * Q > m) {
            haveQ = 1; uint64_t k = m / Q;
            if (!((Q <= m - 1 ? e[Q] : 0) == k - 1)) { failQ++; if (failQ < 20) fprintf(stderr, "EQ fail m=%llu\n", (unsigned long long)m); }
            #ifdef MUT_RULE
            pred = (cnt[k] == 0 ? 1 : 0);
#elif defined(MUT_INS)
            pred = - ((k >= 2 && cnt[k - 1] == 1) ? 1 : 0);
#else
            pred = (cnt[k] == 0 ? 1 : 0) - ((k >= 2 && cnt[k - 1] == 1) ? 1 : 0);
#endif
        }
        // isolation, before
        for (int i = 0; i < np; i++) {
            uint64_t q = ps[i];
            if (q * q <= ISOMUL * m) {
                iso_checks++;
                if (!(cnt[e[q]] == 1)) { if (m != 4) { failI++; if (failI < 20) fprintf(stderr, "ISO-before fail m=%llu q=%llu\n", (unsigned long long)m, (unsigned long long)q); } }
            }
        }
        // apply the step
        int64_t h0 = h;
        for (int i = 0; i < np; i++) {
            uint32_t p = ps[i];
            if (e[p] > 0) { cnt[e[p]]--; if (cnt[e[p]] == 0) h--; }
            e[p] += vs[i];
            if (cnt[e[p]] == 0) h++;
            cnt[e[p]]++;
        }
        // isolation, after
        for (int i = 0; i < np; i++) {
            uint64_t q = ps[i];
            if (q * q <= ISOMUL * m) {
                if (!(cnt[e[q]] == 1)) { failI++; if (failI < 20) fprintf(stderr, "ISO-after fail m=%llu q=%llu\n", (unsigned long long)m, (unsigned long long)q); }
            }
        }
        int64_t d = h - h0;
        if (d > STEPBOUND || d < -STEPBOUND) { failA++; if (failA < 20) fprintf(stderr, "STEP fail m=%llu d=%lld\n", (unsigned long long)m, (long long)d); }
        if (d == 1) up++; else if (d == -1) down++; else zero++;
        if (m != 4 && d != pred) { failR++; if (failR < 20) fprintf(stderr, "RULE fail m=%llu d=%lld pred=%lld haveQ=%d\n", (unsigned long long)m, (long long)d, (long long)pred, haveQ); }
        if (m <= 10000) fprintf(fs, "%llu %lld\n", (unsigned long long)m, (long long)h);
        if (STEP && (m % STEP == 0 || m % STEP == 7919 % STEP)) printf("S %llu %lld\n", (unsigned long long)m, (long long)h);
        if (m == next_cp) {
            double r = h / sqrt((double)m / log((double)m));
            printf("CP n=%llu h=%lld ratio=%.6f up=%llu down=%llu zero=%llu\n", (unsigned long long)m, (long long)h, r, (unsigned long long)up, (unsigned long long)down, (unsigned long long)zero);
            next_cp *= 10;
        }
    }
    fclose(fs);
    printf("N=%llu (steps n->n+1 with n+1 <= N) steps: up=%llu down=%llu zero=%llu | failA=%llu failI=%llu (checks %llu) failR=%llu failQ=%llu\n",
           (unsigned long long)N, (unsigned long long)up, (unsigned long long)down, (unsigned long long)zero,
           (unsigned long long)failA, (unsigned long long)failI, (unsigned long long)iso_checks, (unsigned long long)failR, (unsigned long long)failQ);
    return (failA || failI || failR || failQ) ? 1 : 0;
}
