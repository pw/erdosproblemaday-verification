// model.c — finite-n expectations for J(n) under random-prime models (Erdős #912).
// J(n) = #{k : some prime p > s = isqrt(n) has floor(n/p) = k}; I_k = integers in (n/(k+1), n/k] with l > s.
// Models (independent per integer l):
//   Cramér:        P(l prime) = 1/log l                                    (G–I (1.8))
//   sieve model z: P(l prime) = theta_z/log l if gcd(l, P_z) = 1, else 0;  theta_z = prod_{p<=z} p/(p-1)
// For each model: E[J], Var[J] = sum p_k(1-p_k), expected u_r on k >= K0 (r <= 20), and a t-binned table
// (t = k / sqrt(n/log n)) compared with the ACTUAL nonempty flags read from hfast's bitset.
// log l is taken at the interval midpoint (relative variation of log l across I_k is < 1/(k log l)).
// Usage: model n K0 bitset_file
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>

#define NZ 8
static const int ZS[NZ] = {2, 3, 5, 7, 11, 13, 17, 19};
#define NB 120          /* t bins of width 0.05 on [0,6) */
#define BW 0.05
#define RMAX 21

static const char *NM[NZ+1] = {"cramer","z=2","z=3","z=5","z=7","z=11","z=13","z=17","z=19"};
static uint64_t isqrt64(uint64_t n) { uint64_t r = (uint64_t)sqrtl((long double)n); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }

int main(int argc, char **argv) {
    uint64_t n = strtoull(argv[1], 0, 10), K0 = strtoull(argv[2], 0, 10);
    const char *bsf = argv[3];
    uint64_t s = isqrt64(n), kmax = n / (s + 1);
    FILE *f = fopen(bsf, "rb"); uint64_t n2, km2; fread(&n2, 8, 1, f); fread(&km2, 8, 1, f);
    if (n2 != n || km2 != kmax) { fprintf(stderr, "bitset header mismatch %llu %llu\n", (unsigned long long)n2, (unsigned long long)km2); return 2; }
    uint64_t nb = kmax / 8 + 2; uint8_t *bs = malloc(nb); if (fread(bs, 1, nb, f) != nb) { fprintf(stderr, "short bitset\n"); return 2; } fclose(f);
    // coprime prefix tables
    uint32_t *tab[NZ]; uint64_t Pz[NZ], phiz[NZ]; double theta[NZ];
    { uint64_t P = 1, phi = 1; double th = 1; int pi = 0; static const int pr[] = {2,3,5,7,11,13,17,19};
      for (int z = 0; z < NZ; z++) { int p = pr[pi++]; P *= p; phi *= (p - 1); th *= (double)p / (p - 1);
        Pz[z] = P; phiz[z] = phi; theta[z] = th; tab[z] = malloc(4 * (P + 1)); tab[z][0] = 0;
        for (uint64_t x = 1; x <= P; x++) { int ok = 1; for (int j = 0; j <= z; j++) if (x % pr[j] == 0) { ok = 0; break; } tab[z][x] = tab[z][x - 1] + ok; } } }
    double scale = sqrt((double)n / log((double)n));
    // accumulators (model 0 = Cramér, 1..NZ = sieve models)
    double E[NZ + 1] = {0}, V[NZ + 1] = {0}, U[NZ + 1][RMAX]; memset(U, 0, sizeof U);
    double binE[NZ + 1][NB + 1]; memset(binE, 0, sizeof binE);
    uint64_t binK[NB + 1] = {0}, binA[NB + 1] = {0}, Jact = 0;
    #pragma omp parallel
    {
        double e[NZ + 1] = {0}, v[NZ + 1] = {0}, u[NZ + 1][RMAX], be[NZ + 1][NB + 1]; memset(u, 0, sizeof u); memset(be, 0, sizeof be);
        uint64_t bk[NB + 1] = {0}, ba[NB + 1] = {0}, ja = 0;
        #pragma omp for schedule(dynamic, 65536)
        for (uint64_t k = 1; k <= kmax; k++) {
            uint64_t a = n / (k + 1), b = n / k; if (a < s) a = s; if (b <= a) continue;
            uint64_t len = b - a; double mid = 0.5 * ((double)a + (double)b) + 0.5; double q = 1.0 / log(mid);
            int bin = (int)(k / scale / BW); if (bin > NB) bin = NB;
            int act = (bs[k / 8] >> (k % 8)) & 1; ja += act; bk[bin]++; ba[bin] += act;
            for (int m = 0; m <= NZ; m++) {
                uint64_t cntl; double qq;
                if (m == 0) { cntl = len; qq = q; }
                else { int z = m - 1; uint64_t P = Pz[z];
                       uint64_t Fb = (b / P) * phiz[z] + tab[z][b % P], Fa = (a / P) * phiz[z] + tab[z][a % P];
                       cntl = Fb - Fa; qq = theta[z] * q; }
                double lp0 = (double)cntl * log1p(-qq);           // log P(empty)
                double p0 = lp0 < -745 ? 0.0 : exp(lp0);
                double pk = 1.0 - p0;
                e[m] += pk; v[m] += pk * p0; be[m][bin] += pk;
                if (k >= K0) { // expected u_r, binomial(cntl, qq) via pmf recurrence
                    double pr = p0, ratio = qq / (1.0 - qq);
                    for (int r = 0; r < RMAX && (uint64_t)r <= cntl; r++) { u[m][r] += pr; pr = pr * (double)(cntl - r) / (double)(r + 1) * ratio; }
                }
            }
        }
        #pragma omp critical
        {
            for (int m = 0; m <= NZ; m++) { E[m] += e[m]; V[m] += v[m]; for (int r = 0; r < RMAX; r++) U[m][r] += u[m][r]; for (int i = 0; i <= NB; i++) binE[m][i] += be[m][i]; }
            for (int i = 0; i <= NB; i++) { binK[i] += bk[i]; binA[i] += ba[i]; } Jact += ja;
        }
    }
    printf("n=%llu s=%llu kmax=%llu K0=%llu scale=%.3f Jactual=%llu\n", (unsigned long long)n, (unsigned long long)s, (unsigned long long)kmax, (unsigned long long)K0, scale, (unsigned long long)Jact);
    printf("model    theta     E[J]            sd        (Jact-E)/sd   E[J]/scale\n");
    for (int m = 0; m <= NZ; m++) {
        double sd = sqrt(V[m]);
        printf("%-8s %7.4f  %14.2f  %9.2f  %+10.2f   %.6f\n", NM[m],
               m == 0 ? 1.0 : theta[m - 1], E[m], sd, ((double)Jact - E[m]) / sd, E[m] / scale);
    }
    printf("expected u_r on k>=K0 (r=0..%d):\n", RMAX - 1);
    for (int m = 0; m <= NZ; m++) { printf("U %-7s", NM[m]); for (int r = 0; r < RMAX; r++) printf(" %.1f", U[m][r]); printf("\n"); }
    printf("BINS t_lo  nk  actual  cramer  z=2 z=3 z=5 z=7 z=11 z=13 z=17 z=19\n");
    for (int i = 0; i <= NB; i++) if (binK[i]) {
        printf("B %.2f %llu %llu", i * BW, (unsigned long long)binK[i], (unsigned long long)binA[i]);
        for (int m = 0; m <= NZ; m++) printf(" %.2f", binE[m][i]); printf("\n"); }
    return 0;
}
