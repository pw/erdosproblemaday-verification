// regular.c -- the regularity version of the rough-third construction (Della Pietra, paper eqs. H, T).
//
//   Omega_L(n,x) = sum over p^v || n with L <= p <= x of v.
//   n is (L,A,K)-regular  iff  Omega_L(n,x) <= A log(log x / log L) + K for every x >= L.
//   With q_1 <= q_2 <= ... the prime factors >= L of n (with multiplicity) this is
//        j - K <= m*(q_j) for all j,   m*(q) = floor(A log(log q/log L)) = #{m>=1 : q >= thr(L,A,m)},
//   thr(L,A,m) = ceil(L^exp(m/A)) certified in out/thresholds.txt (thresholds.py). So
//        Kmin(n;L,A) = max(0, max_j (j - m*(q_j)))  and  n is (L,A,K)-regular  iff  Kmin <= K.
//   Integer comparisons only.
//
//   H_N = { a : N/3 < a < N/2, lpf(a) >= L, a (L,A_h,K_h)-regular }
//   T_N = { b : ceil(N/2) <= b <= N,       b (L,A_t,K_t)-regular }
//   Gamma_N = heads of H_N in a relation 1/a = 1/b + 1/c with b<c in T_N;   A_N = T_N U (H_N \ Gamma_N).
//
// Pass 1 (top): segmented full factorisation of [ceil(N/2), N]; histogram of Kmin(b;L,A).
// Pass 2 (heads): segmented factorisation of (N/3,N/2); for every 7-rough a, every relation
//   (coprime divisors r<s of a with s(M-a) <= r a and s a <= r (N-a)); b = t r (r+s), c = t s (r+s)
//   with t = a/(rs); factor (r+s) by a small spf table and merge, so Kmin(b), Kmin(c) need no
//   big table.  conf(a;L,A_t) = min over relations of max(Kmin(b),Kmin(c)) (KC+1 = no relation).
//   Histogram over (Kmin(a;L,A_h), conf(a;L,A_t)).  Then for any K_h, K_t:
//     |T| = #{b: Kmin(b) <= K_t},  kept heads = #{a: L-rough, Kmin(a) <= K_h, conf(a) > K_t}.
//   K = "inf" means no regularity condition at all (all bins) -- that row must equal simple.c.
//
// usage: ./regular N THRESHOLDS [--selftest] [--dump L Aih Kh Ait Kt FILE]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>

typedef unsigned long long u64;
typedef unsigned __int128 u128;

#define NL 5
static const int LS[NL] = {7, 11, 13, 17, 23};
#define NA 4
static const char *ANAME[NA] = {"1.0001", "1.16312", "1.5", "2"};
#define MAXT 12
#define KC 15          // Kmin capped at KC (never reached for N <= 1e11: Omega_7(n) <= 13)
#define MAXF 16

static u64 thr[NL][NA][MAXT]; static int nthr[NL][NA];
static u64 N, M, LO, HI;
static uint32_t *primes; static int nprimes;
static uint32_t *spf; static u64 spfmax;

static inline int mstar(u64 q, int li, int ai) {
  int m = 0; while (m < nthr[li][ai] && thr[li][ai][m] <= q) m++; return m;
}
// factor list (p ascending, e) -> Kmin for every (L,A)
static void kmin_all(int nf, const u64 *p, const uint8_t *e, uint8_t out[NL][NA]) {
  for (int li = 0; li < NL; li++) for (int ai = 0; ai < NA; ai++) {
    int j = 0, k = 0;
    for (int f = 0; f < nf; f++) {
      if (p[f] < (u64)LS[li]) continue;
      j += e[f];
      int v = j - mstar(p[f], li, ai);
      if (v > k) k = v;
    }
    out[li][ai] = k > KC ? KC : k;
  }
}
// direct trial-division factorisation (selftest only)
static int factor_td(u64 n, u64 *p, uint8_t *e) {
  int nf = 0;
  for (u64 d = 2; d * d <= n; d++) if (n % d == 0) { uint8_t c = 0; while (n % d == 0) { n /= d; c++; } p[nf] = d; e[nf] = c; nf++; }
  if (n > 1) { p[nf] = n; e[nf] = 1; nf++; }
  return nf;
}

static void load_thr(const char *fn) {
  FILE *f = fopen(fn, "r"); if (!f) { perror(fn); exit(2); }
  char line[256];
  while (fgets(line, sizeof line, f)) {
    if (line[0] == '#') continue;
    int L, ai, m; char val[200];
    if (sscanf(line, "%d %d %d %199s", &L, &ai, &m, val) != 4) continue;
    int li = -1; for (int i = 0; i < NL; i++) if (LS[i] == L) li = i;
    if (li < 0 || ai >= NA) continue;
    u64 v = strlen(val) > 18 ? ~0ULL : strtoull(val, 0, 10);
    if (m != nthr[li][ai] + 1) { fprintf(stderr, "threshold order\n"); exit(2); }
    thr[li][ai][nthr[li][ai]++] = v;
  }
  fclose(f);
  for (int li = 0; li < NL; li++) for (int ai = 0; ai < NA; ai++)
    if (nthr[li][ai] == 0 || thr[li][ai][nthr[li][ai] - 1] <= N) { fprintf(stderr, "thresholds do not cover N\n"); exit(2); }
}

// histograms
static u64 topH[NL][NA][KC + 1];
static u64 headH[NL][NA][NA][KC + 1][KC + 2];   // [L][A_h][A_t][Kmin(a)][conf]
static u64 relcount[NL];
static uint8_t *topK_self;   // selftest: Kmin(b) from pass 1, [L][A] packed, for b in [M,N]
static u64 selfchecked, selfbad;

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: %s N THRESHOLDS [--selftest] [--dump L Aih Kh Ait Kt FILE]\n", argv[0]); return 2; }
  N = strtoull(argv[1], 0, 10);
  int selftest = 0; int dL = -1, dAh = 0, dKh = 0, dAt = 0, dKt = 0; const char *dumpf = 0;
  for (int i = 3; i < argc; i++) {
    if (!strcmp(argv[i], "--selftest")) selftest = 1;
    else if (!strcmp(argv[i], "--dump")) { dL = atoi(argv[i+1]); dAh = atoi(argv[i+2]); dKh = atoi(argv[i+3]); dAt = atoi(argv[i+4]); dKt = atoi(argv[i+5]); dumpf = argv[i+6]; i += 6; }
  }
  load_thr(argv[2]);
  M = (N + 1) / 2; LO = N / 3 + 1; HI = (N - 1) / 2;
  int dli = -1; if (dumpf) for (int i = 0; i < NL; i++) if (LS[i] == dL) dli = i;
  uint8_t *inA = dumpf ? calloc(N - LO + 1, 1) : 0;   // membership bitmap over [LO, N] for the dumped config

  u64 sq = 1; while ((sq + 1) * (sq + 1) <= N) sq++;
  char *comp = calloc(sq + 1, 1); primes = malloc(sizeof(uint32_t) * (sq + 1)); nprimes = 0;
  for (u64 i = 2; i <= sq; i++) if (!comp[i]) { primes[nprimes++] = i; for (u64 j = i * i; j <= sq; j += i) comp[j] = 1; }
  free(comp);
  spfmax = 3 * sq + 10;
  spf = calloc(spfmax + 1, sizeof(uint32_t));
  for (u64 i = 2; i <= spfmax; i++) if (!spf[i]) for (u64 j = i; j <= spfmax; j += i) if (!spf[j]) spf[j] = i;

  if (selftest) topK_self = malloc((N - M + 1) * NL * NA);

  // self-check of kmin on hand examples (L=7, A=2: thresholds 25,199,6131,...)
  {
    u64 ex[] = {77, 203, 1024, 343, 7 * 199, 7 * 11 * 13, 7 * 11 * 6131};
    printf("# hand examples Kmin(n; L=7, A) for A = 1.0001 1.16312 1.5 2\n");
    for (int i = 0; i < 7; i++) { u64 p[40]; uint8_t e[40]; int nf = factor_td(ex[i], p, e); uint8_t k[NL][NA]; kmin_all(nf, p, e, k);
      printf("#   n=%llu: %d %d %d %d\n", ex[i], k[0][0], k[0][1], k[0][2], k[0][3]); }
  }

  const u64 SEG = 1 << 18;
  // ---------- pass 1: top half ----------
  u64 nseg = (N - M + 1 + SEG - 1) / SEG;
  #pragma omp parallel
  {
    u64 *rem = malloc(sizeof(u64) * SEG); u64 *fp = malloc(sizeof(u64) * SEG * MAXF);
    uint8_t *fe = malloc(SEG * MAXF); uint8_t *nf = malloc(SEG);
    u64 lt[NL][NA][KC + 1]; memset(lt, 0, sizeof lt);
    #pragma omp for schedule(dynamic, 1)
    for (u64 sg = 0; sg < nseg; sg++) {
      u64 s0 = M + sg * SEG, s1 = s0 + SEG - 1; if (s1 > N) s1 = N;
      u64 len = s1 - s0 + 1;
      for (u64 i = 0; i < len; i++) { rem[i] = s0 + i; nf[i] = 0; }
      for (int k = 0; k < nprimes; k++) {
        u64 p = primes[k]; if (p * p > s1) break;
        for (u64 m = ((s0 + p - 1) / p) * p; m <= s1; m += p) {
          u64 i = m - s0; uint8_t e = 0; while (rem[i] % p == 0) { rem[i] /= p; e++; }
          fp[i * MAXF + nf[i]] = p; fe[i * MAXF + nf[i]] = e; nf[i]++;
        }
      }
      for (u64 i = 0; i < len; i++) {
        if (rem[i] > 1) { fp[i * MAXF + nf[i]] = rem[i]; fe[i * MAXF + nf[i]] = 1; nf[i]++; }
        uint8_t k[NL][NA]; kmin_all(nf[i], fp + i * MAXF, fe + i * MAXF, k);
        for (int li = 0; li < NL; li++) for (int ai = 0; ai < NA; ai++) lt[li][ai][k[li][ai]]++;
        if (topK_self) memcpy(topK_self + (s0 + i - M) * NL * NA, k, NL * NA);
        if (inA && k[dli][dAt] <= dKt) inA[s0 + i - LO] = 1;
      }
    }
    #pragma omp critical
    for (int li = 0; li < NL; li++) for (int ai = 0; ai < NA; ai++) for (int k = 0; k <= KC; k++) topH[li][ai][k] += lt[li][ai][k];
    free(rem); free(fp); free(fe); free(nf);
  }

  // ---------- pass 2: heads ----------
  nseg = (HI - LO + 1 + SEG - 1) / SEG;
  #pragma omp parallel
  {
    u64 *rem = malloc(sizeof(u64) * SEG); u64 *fp = malloc(sizeof(u64) * SEG * MAXF);
    uint8_t *fe = malloc(SEG * MAXF); uint8_t *nf = malloc(SEG);
    int DMAX = 200000;
    u64 *dv = malloc(sizeof(u64) * DMAX); uint32_t *dmask = malloc(sizeof(uint32_t) * DMAX);
    uint8_t (*dexp)[MAXF] = malloc(sizeof(uint8_t[MAXF]) * DMAX);
    int *ord = malloc(sizeof(int) * DMAX);
    u64 (*lh)[NA][NA][KC + 1][KC + 2] = calloc(NL, sizeof(u64[NA][NA][KC + 1][KC + 2]));
    u64 lrel[NL] = {0}, lself = 0, lbad = 0;
    #pragma omp for schedule(dynamic, 1)
    for (u64 sg = 0; sg < nseg; sg++) {
      u64 s0 = LO + sg * SEG, s1 = s0 + SEG - 1; if (s1 > HI) s1 = HI;
      u64 len = s1 - s0 + 1;
      for (u64 i = 0; i < len; i++) { rem[i] = s0 + i; nf[i] = 0; }
      for (int k = 0; k < nprimes; k++) {
        u64 p = primes[k]; if (p * p > s1) break;
        for (u64 m = ((s0 + p - 1) / p) * p; m <= s1; m += p) {
          u64 i = m - s0; uint8_t e = 0; while (rem[i] % p == 0) { rem[i] /= p; e++; }
          fp[i * MAXF + nf[i]] = p; fe[i * MAXF + nf[i]] = e; nf[i]++;
        }
      }
      for (u64 i = 0; i < len; i++) {
        u64 a = s0 + i;
        if (rem[i] > 1) { fp[i * MAXF + nf[i]] = rem[i]; fe[i * MAXF + nf[i]] = 1; nf[i]++; }
        int w = nf[i]; u64 *P = fp + i * MAXF; uint8_t *E = fe + i * MAXF;
        if (P[0] < 7) continue;
        uint8_t ka[NL][NA]; kmin_all(w, P, E, ka);
        // divisors with exponent vectors
        int nd = 1; dv[0] = 1; dmask[0] = 0; memset(dexp[0], 0, MAXF);
        for (int f = 0; f < w; f++) {
          int cur = nd; u64 pk = 1;
          for (int t = 1; t <= E[f]; t++) { pk *= P[f];
            for (int j = 0; j < cur; j++) { dv[nd] = dv[j] * pk; dmask[nd] = dmask[j] | (1u << f); memcpy(dexp[nd], dexp[j], MAXF); dexp[nd][f] = t; nd++; } }
        }
        // sort divisor indices by value (insertion sort on small arrays; qsort on keys otherwise)
        for (int j = 0; j < nd; j++) ord[j] = j;
        for (int j = 1; j < nd; j++) { int x = ord[j]; int k = j - 1; while (k >= 0 && dv[ord[k]] > dv[x]) { ord[k + 1] = ord[k]; k--; } ord[k + 1] = x; }
        uint8_t conf[NL][NA]; for (int li = 0; li < NL; li++) for (int ai = 0; ai < NA; ai++) conf[li][ai] = KC + 1;
        u128 MA = M - a, NA_ = N - a;
        int nrel = 0;
        for (int j = 0; j < nd; j++) for (int k = j + 1; k < nd; k++) {
          int ir = ord[j], is = ord[k];
          u128 r = dv[ir], s = dv[is];
          if (s * MA > r * (u128)a || s * (u128)a > r * NA_) break;
          if (dmask[ir] & dmask[is]) continue;       // not coprime
          nrel++;
          u64 x = dv[ir] + dv[is];                      // r+s < 3 sqrt(a)
          // factor x
          u64 xp[MAXF]; uint8_t xe[MAXF]; int xn = 0; u64 y = x;
          while (y > 1) { u64 p = spf[y]; uint8_t c = 0; while (y % p == 0) { y /= p; c++; } xp[xn] = p; xe[xn] = c; xn++; }
          // b = t r x, c = t s x ; exponents of a's primes in t r = E - e_s, in t s = E - e_r
          uint8_t kside0[NL][NA];
          for (int side = 0; side < 2; side++) {
            const uint8_t *drop = side == 0 ? dexp[is] : dexp[ir];
            u64 bp[2 * MAXF]; uint8_t be[2 * MAXF]; int bn = 0;
            int ia = 0, ix = 0;
            while (ia < w || ix < xn) {
              u64 pa = ia < w ? P[ia] : ~0ULL, px = ix < xn ? xp[ix] : ~0ULL;
              if (pa < px) { int ee = E[ia] - drop[ia]; if (ee) { bp[bn] = pa; be[bn] = ee; bn++; } ia++; }
              else if (px < pa) { bp[bn] = px; be[bn] = xe[ix]; bn++; ix++; }
              else { int ee = E[ia] - drop[ia] + xe[ix]; if (ee) { bp[bn] = pa; be[bn] = ee; bn++; } ia++; ix++; }
            }
            uint8_t kb[NL][NA]; kmin_all(bn, bp, be, kb);
            if (selftest) {
              u64 bval = side == 0 ? (u64)((u128)a * x / dv[is]) : (u64)((u128)a * x / dv[ir]);
              u64 val = 1; for (int f = 0; f < bn; f++) for (int t = 0; t < be[f]; t++) val *= bp[f];
              u64 tp[40]; uint8_t te[40]; int tn = factor_td(bval, tp, te); uint8_t kt[NL][NA]; kmin_all(tn, tp, te, kt);
              lself++;
              if (val != bval || memcmp(kt, kb, sizeof kb) || bval < M || bval > N || memcmp(topK_self + (bval - M) * NL * NA, kb, sizeof kb)) lbad++;
            }
            if (side == 0) memcpy(kside0, kb, sizeof kb);   // Kmin(b); combine with Kmin(c) below
            else for (int li = 0; li < NL; li++) for (int ai = 0; ai < NA; ai++) {
              uint8_t mx = kside0[li][ai] > kb[li][ai] ? kside0[li][ai] : kb[li][ai];
              if (mx < conf[li][ai]) conf[li][ai] = mx;
            }
          }
        }
        for (int li = 0; li < NL; li++) {
          if (P[0] < (u64)LS[li]) continue;
          lrel[li] += nrel;
          for (int ah = 0; ah < NA; ah++) for (int at = 0; at < NA; at++) lh[li][ah][at][ka[li][ah]][conf[li][at]]++;
        }
        if (inA && P[0] >= (u64)dL && ka[dli][dAh] <= dKh && conf[dli][dAt] > dKt) inA[a - LO] = 1;
      }
    }
    #pragma omp critical
    {
      for (int li = 0; li < NL; li++) { relcount[li] += lrel[li];
        for (int ah = 0; ah < NA; ah++) for (int at = 0; at < NA; at++) for (int x = 0; x <= KC; x++) for (int y = 0; y <= KC + 1; y++) headH[li][ah][at][x][y] += lh[li][ah][at][x][y]; }
      selfchecked += lself; selfbad += lbad;
    }
    free(rem); free(fp); free(fe); free(nf); free(dv); free(dmask); free(dexp); free(ord); free(lh);
  }

  // ---------- report ----------
  u64 topfull = N - M + 1;
  printf("# regularity construction N=%llu  top half %llu elements, heads (N/3,N/2)=[%llu,%llu]\n", N, topfull, LO, HI);
  if (selftest) printf("# selftest: %llu (b or c) values re-factored by trial division and compared with pass-1 Kmin: %llu mismatches\n", selfchecked, selfbad);
  printf("# Kmin histograms of the top half (count of b with Kmin = k), k = 0..%d\n", KC);
  for (int li = 0; li < NL; li++) for (int ai = 0; ai < NA; ai++) {
    printf("topKmin L=%d A=%s:", LS[li], ANAME[ai]); for (int k = 0; k <= KC; k++) printf(" %llu", topH[li][ai][k]); printf("\n"); }
  printf("# rows: L A_h K_h A_t K_t | |T| top_loss | regular_heads conflicted kept | |A| 2|A|-N excess deleted_frac_of_regular_heads\n");
  const int KS[] = {0, 1, 2, 3, 4, 99};  // 99 = inf (no regularity condition)
  for (int li = 0; li < NL; li++) for (int ah = 0; ah < NA; ah++) for (int at = 0; at < NA; at++) {
    for (int a1 = 0; a1 < 6; a1++) for (int a2 = 0; a2 < 6; a2++) {
      int Kh = KS[a1], Kt = KS[a2];
      int kh_hi = Kh >= KC ? KC : Kh, kt_hi = Kt >= KC ? KC : Kt;
      u64 T = 0; for (int k = 0; k <= kt_hi; k++) T += topH[li][at][k];
      u64 Hreg = 0, Conf = 0;
      for (int x = 0; x <= kh_hi; x++) for (int y = 0; y <= KC + 1; y++) { Hreg += headH[li][ah][at][x][y]; if (y <= kt_hi) Conf += headH[li][ah][at][x][y]; }
      u64 kept = Hreg - Conf, A = T + kept; long long tw = 2 * (long long)A - (long long)N;
      long long ex7 = (long long)(((__int128)tw * 10000000) / (2 * (__int128)N));
      u64 df6 = Hreg ? (u64)(((u128)Conf * 1000000) / Hreg) : 0;
      char sh[8], st[8]; if (Kh == 99) strcpy(sh, "inf"); else sprintf(sh, "%d", Kh); if (Kt == 99) strcpy(st, "inf"); else sprintf(st, "%d", Kt);
      printf("L=%d Ah=%s Kh=%s At=%s Kt=%s | %llu %llu | %llu %llu %llu | %llu %lld %s0.%07lld 0.%06llu\n",
             LS[li], ANAME[ah], sh, ANAME[at], st, T, topfull - T, Hreg, Conf, kept, A, tw, tw < 0 ? "-" : "", tw < 0 ? -ex7 : ex7, df6);
    }
  }
  for (int li = 0; li < NL; li++) printf("relations L=%d %llu\n", LS[li], relcount[li]);
  if (inA) {
    FILE *f = fopen(dumpf, "w"); u64 c = 0;
    for (u64 x = LO; x <= N; x++) if (inA[x - LO]) { fprintf(f, "%llu\n", x); c++; }
    fclose(f); printf("# dumped %llu elements for L=%d Ah=%s Kh=%d At=%s Kt=%d to %s\n", c, dL, ANAME[dAh], dKh, ANAME[dAt], dKt, dumpf);
  }
  return 0;
}
