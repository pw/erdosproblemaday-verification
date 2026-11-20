/* Independent recount of |A_min| for the band of y-smooth s in (T, Lam*T], Lam > y:
   enumerate y-smooth t <= T (t>=1); s = p*t is minimal with P-(s)=p iff p <= P-(t), p prime <= y, p*t > T.
   So |A_min| = sum_t #{p prime : floor(T/t) < p <= min(P-(t), y)}  (P-(1) := +inf).
   Per-p tallies via a difference array over prime indices. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
typedef unsigned long long u64;
static int P[2000], np, PI[20000]; static u64 T;
static void rec(u64 t, int k, int j0, u64 *cnt, long long *diff){
  (*cnt)++;                                  /* Psi tally */
  u64 f = T / t;
  if (f < (u64)P[j0]) { int lo = PI[f]; /* primes <= f have index < lo */ diff[lo]++; diff[j0+1]--; }
  for (int i = k; i < np; i++){ unsigned __int128 w = (unsigned __int128)t * P[i]; if (w > T) break; rec((u64)w, i, j0, cnt, diff); }
}
int main(int argc, char **argv){
  int y = atoi(argv[1]); T = strtoull(argv[2], 0, 10);
  char *c = calloc(y+1, 1); for (int i = 2; i <= y; i++) if (!c[i]) { P[np++] = i; for (int j = 2*i; j <= y; j += i) c[j] = 1; }
  for (int x = 0, k = 0; x <= y; x++){ while (k < np && P[k] <= x) k++; PI[x] = k; }
  long long *gdiff = calloc(np+2, sizeof(long long)); u64 psi = 1;
  /* t = 1: primes p in (T, y] */
  for (int i = 0; i < np; i++) if ((u64)P[i] > T) { gdiff[i]++; gdiff[i+1]--; }
  int nitems = 0; static int A[400000], B[400000];
  for (int j = 0; j < np; j++){ A[nitems] = j; B[nitems] = -1; nitems++; for (int i = j; i < np; i++){ A[nitems] = j; B[nitems] = i; nitems++; } }
  #pragma omp parallel
  { long long *diff = calloc(np+2, sizeof(long long)); u64 cnt = 0;
    #pragma omp for schedule(dynamic,1)
    for (int it = 0; it < nitems; it++){ int j = A[it], i = B[it];
      if ((u64)P[j] > T) continue;
      if (i < 0){ /* node t = P[j] alone, children handled by items (j,i) */
        cnt++; u64 f = T / P[j]; if (f < (u64)P[j]) { diff[PI[f]]++; diff[j+1]--; }
      } else { unsigned __int128 w = (unsigned __int128)P[j] * P[i]; if (w <= T) rec((u64)w, i, j, &cnt, diff); }
    }
    #pragma omp critical
    { for (int i = 0; i <= np; i++) gdiff[i] += diff[i]; psi += cnt; }
    free(diff); }
  long long run = 0, tot = 0; printf("y=%d T=%llu Psi(T)=%llu\nper p:", y, T, psi);
  for (int i = 0; i < np; i++){ run += gdiff[i]; tot += run; if (i < 12) printf(" %d:%lld", P[i], run); }
  printf("\ncore=%lld\n", tot); return 0; }
