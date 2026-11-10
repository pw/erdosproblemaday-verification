// hfast.c — exact h(n) for large n (Erdős #912).
// Identity used (proved on the page; Heyman–Miraj give h(n) = #{floor(n/p)}):
//   h(n) = pi(s) + J(n),  s = isqrt(n),
//   J(n) = #{k >= 1 : some prime p > s has floor(n/p) = k}.
// Region S: primes p in (s, floor(n/K0)]  <->  k >= K0  — segmented sieve, exact prime COUNT per k.
// Region M: k = 1..K0-1, interval (floor(n/(k+1)), floor(n/k)] — search for one prime (deterministic 64-bit MR).
// Usage: hfast n K0 [bitset_out]   (K0 = 0 -> choose so that the interval at K0 has ~40 expected primes)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>
typedef unsigned __int128 u128;

static uint64_t isqrt64(uint64_t n) { uint64_t r = (uint64_t)sqrtl((long double)n); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }
static uint64_t mulmod(uint64_t a, uint64_t b, uint64_t m) { return (uint64_t)((u128)a * b % m); }
static uint64_t powmod(uint64_t a, uint64_t e, uint64_t m) { uint64_t r = 1; a %= m; while (e) { if (e & 1) r = mulmod(r, a, m); a = mulmod(a, a, m); e >>= 1; } return r; }
static int is_prime64(uint64_t n) {
    if (n < 2) return 0;
    static const uint64_t sp[] = {2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71};
    for (int i = 0; i < 20; i++) { if (n == sp[i]) return 1; if (n % sp[i] == 0) return 0; }
    uint64_t d = n - 1; int r = 0; while (!(d & 1)) { d >>= 1; r++; }
    static const uint64_t B[] = {2, 325, 9375, 28178, 450775, 9780504, 1795265022};
    for (int i = 0; i < 7; i++) {
        uint64_t a = B[i] % n; if (a == 0) continue;
        uint64_t x = powmod(a, d, n); if (x == 1 || x == n - 1) continue;
        int ok = 0; for (int j = 1; j < r; j++) { x = mulmod(x, x, n); if (x == n - 1) { ok = 1; break; } }
        if (!ok) return 0;
    }
    return 1;
}

static uint32_t *small_primes; static int nsmall;
static void make_small(uint64_t lim) {
    char *c = calloc(lim + 1, 1); small_primes = malloc(sizeof(uint32_t) * (lim / 2 + 10)); nsmall = 0;
    for (uint64_t i = 2; i <= lim; i++) if (!c[i]) { small_primes[nsmall++] = (uint32_t)i; for (uint64_t j = i * i; j <= lim; j += i) c[j] = 1; }
    free(c);
}

#define SEG (1u << 21)   /* odd numbers per segment */
// sieve odd numbers in [lo, hi] (lo odd), call back per prime
static uint64_t count_primes_upto(uint64_t x) {   // pi(x), x <= ~1e10
    if (x < 2) return 0;
    uint64_t total = 1; // the prime 2
    uint64_t nseg = ((x - 1) / 2 + SEG - 1) / SEG; // odd numbers 3..x : index i -> 2i+3
    #pragma omp parallel for schedule(dynamic) reduction(+:total)
    for (uint64_t sg = 0; sg < nseg; sg++) {
        uint64_t lo = 3 + 2 * sg * SEG; uint64_t hi = lo + 2 * (SEG - 1); if (hi > x) hi = x; if (lo > x) continue;
        uint64_t len = (hi - lo) / 2 + 1; char *b = malloc(len); memset(b, 1, len);
        for (int i = 1; i < nsmall; i++) { uint64_t p = small_primes[i]; if (p * p > hi) break;
            uint64_t st = p * p; if (st < lo) { st = ((lo + p - 1) / p) * p; if (!(st & 1)) st += p; }
            for (uint64_t j = st; j <= hi; j += 2 * p) b[(j - lo) / 2] = 0; }
        uint64_t c = 0; for (uint64_t i = 0; i < len; i++) c += b[i];
        free(b); total += c;
    }
    return total;
}

int main(int argc, char **argv) {
    uint64_t n = strtoull(argv[1], 0, 10);
    uint64_t K0 = argc > 2 ? strtoull(argv[2], 0, 10) : 0;
    const char *bsout = argc > 3 ? argv[3] : 0;
    uint64_t s = isqrt64(n);
    if (K0 == 0) { // expected count at k: (n/k^2)/log(n/k) ~ 40
        double k = sqrt((double)n / (40.0 * log((double)n) / 2)); for (int it = 0; it < 30; it++) k = sqrt((double)n / (40.0 * log((double)n / k)));
        K0 = (uint64_t)k; }
    if (K0 < 2) K0 = 2;
    uint64_t P0 = n / K0; if (P0 < s) { P0 = s; }
    uint64_t kmax = n / (s + 1);            // largest k from a prime p > s
    make_small(isqrt64(P0) + 10 > isqrt64(s) + 10 ? isqrt64(P0) + 10 : isqrt64(s) + 10);
    fprintf(stderr, "n=%llu s=%llu K0=%llu P0=%llu kmax=%llu nsmall=%d\n", (unsigned long long)n, (unsigned long long)s, (unsigned long long)K0, (unsigned long long)P0, (unsigned long long)kmax, nsmall);
    double t0 = omp_get_wtime();
    uint64_t pis = count_primes_upto(s);
    fprintf(stderr, "pi(s)=%llu  (%.1fs)\n", (unsigned long long)pis, omp_get_wtime() - t0);
    // Region S: primes in (s, P0], exact count per k (k in [K0, kmax])
    uint64_t span = (kmax >= K0) ? kmax - K0 + 1 : 0;
    uint8_t *cnt = calloc(span + 1, 1);
    uint64_t lo0 = s + 1; if (!(lo0 & 1)) lo0++; if (lo0 < 3) lo0 = 3;
    uint64_t primesS = 0, sat = 0;
    if (P0 >= lo0) {
        uint64_t nseg = ((P0 - lo0) / 2 + 1 + SEG - 1) / SEG;
        #pragma omp parallel for schedule(dynamic) reduction(+:primesS,sat)
        for (uint64_t sg = 0; sg < nseg; sg++) {
            uint64_t lo = lo0 + 2 * sg * SEG; uint64_t hi = lo + 2 * (SEG - 1); if (hi > P0) hi = P0; if (lo > P0) continue;
            uint64_t len = (hi - lo) / 2 + 1; char *b = malloc(len); memset(b, 1, len);
            for (int i = 1; i < nsmall; i++) { uint64_t p = small_primes[i]; if (p * p > hi) break;
                uint64_t st = p * p; if (st < lo) { st = ((lo + p - 1) / p) * p; if (!(st & 1)) st += p; }
                for (uint64_t j = st; j <= hi; j += 2 * p) b[(j - lo) / 2] = 0; }
            for (uint64_t i = 0; i < len; i++) if (b[i]) { uint64_t p = lo + 2 * i; uint64_t k = n / p;
                if (k < K0 || k > kmax) { fprintf(stderr, "k out of range p=%llu k=%llu\n", (unsigned long long)p, (unsigned long long)k); exit(3); }
                uint8_t old = __atomic_fetch_add(&cnt[k - K0], 1, __ATOMIC_RELAXED); if (old == 255) sat++; primesS++; }
            free(b);
        }
    }
    // the prime 2 cannot be > s for n >= 4; ignore
    fprintf(stderr, "region S done: %llu primes (%.1fs) sat=%llu\n", (unsigned long long)primesS, omp_get_wtime() - t0, (unsigned long long)sat);
    if (sat) { fprintf(stderr, "count saturation\n"); return 4; }
    // Region M: k = 1..K0-1
    uint8_t *bitM = calloc(K0 / 8 + 2, 1);
    uint64_t emptyM = 0, mr_calls = 0;
    #pragma omp parallel for schedule(dynamic, 4096) reduction(+:emptyM,mr_calls)
    for (uint64_t k = 1; k < K0; k++) {
        uint64_t a = n / (k + 1), b = n / k; if (a < s) a = s;   // primes p in (a, b], p > s
        int found = 0;
        uint64_t x = b; if (x > 2 && !(x & 1)) x--;
        for (; x > a; x -= 2) { mr_calls++; if (is_prime64(x)) { found = 1; break; } if (x < 4) break; }
        if (found) __atomic_fetch_or(&bitM[k / 8], (uint8_t)(1u << (k % 8)), __ATOMIC_RELAXED); else emptyM++;
    }
    fprintf(stderr, "region M done: empty=%llu mr=%llu (%.1fs)\n", (unsigned long long)emptyM, (unsigned long long)mr_calls, omp_get_wtime() - t0);
    uint64_t JS = 0, ur[64]; memset(ur, 0, sizeof ur);
    for (uint64_t i = 0; i < span; i++) { if (cnt[i]) JS++; uint32_t c = cnt[i]; ur[c < 63 ? c : 63]++; }
    uint64_t JM = (K0 - 1) - emptyM;
    uint64_t h = pis + JS + JM;
    double ratio = h / sqrt((double)n / log((double)n));
    printf("n=%llu h=%llu pi_s=%llu J=%llu JS=%llu JM=%llu emptyM=%llu K0=%llu kmax=%llu ratio=%.6f\n",
           (unsigned long long)n, (unsigned long long)h, (unsigned long long)pis, (unsigned long long)(JS + JM), (unsigned long long)JS, (unsigned long long)JM,
           (unsigned long long)emptyM, (unsigned long long)K0, (unsigned long long)kmax, ratio);
    printf("ur(k>=K0):"); for (int r = 0; r < 20; r++) printf(" %llu", (unsigned long long)ur[r]); printf(" | >=20: ");
    uint64_t big = 0; for (int r = 20; r < 64; r++) big += ur[r]; printf("%llu\n", (unsigned long long)big);
    if (bsout) { // nonempty bitset for k = 1..kmax  (bit k)
        uint64_t nb = kmax / 8 + 2; uint8_t *bs = calloc(nb, 1);
        for (uint64_t k = 1; k < K0 && k <= kmax; k++) if (bitM[k / 8] >> (k % 8) & 1) bs[k / 8] |= 1u << (k % 8);
        for (uint64_t i = 0; i < span; i++) if (cnt[i]) { uint64_t k = K0 + i; bs[k / 8] |= 1u << (k % 8); }
        FILE *f = fopen(bsout, "wb"); fwrite(&n, 8, 1, f); fwrite(&kmax, 8, 1, f); fwrite(bs, 1, nb, f); fclose(f); free(bs);
    }
    fprintf(stderr, "total %.1fs\n", omp_get_wtime() - t0);
    return 0;
}
