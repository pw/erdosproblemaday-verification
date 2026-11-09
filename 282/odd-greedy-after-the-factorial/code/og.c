/* og.c -- odd greedy Egyptian-fraction expansion (distinct odd denominators, Erdős #282)
   followed WITHOUT the doubly-exponential denominators.

   State after the safe hand-off: x_k = a_k / b_k, gcd(a_k,b_k)=1, b_k odd, a_k small (uint64).
   Step: r = (-b_k) mod a_k; q = (b_k + r)/a_k; n_k = q if q odd else q+1; s_k = a_k n_k - b_k
         (= r or r + a_k); g_k = gcd(s_k, b_k n_k); a_{k+1} = s_k/g_k; b_{k+1} = b_k n_k / g_k.
   b_k is never stored; it is recomputed modulo whatever is needed by replaying the known
   operations from the exact base b_0, with modulus  need * prod_{j<k} a_j g_j.
   Terminates when a_k = 1 (final term 1/b_k).

   Distinct-denominator rule: handled exactly (mpz) in a prefix phase; once the unconstrained choice
   n is >= 5 and >= prev+2 the rule can never bind again (x' < 2/(n(n-2)) <= 1/n), so we hand off.  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <gmp.h>

#define KMAX 200000
typedef unsigned long ul;
static ul A[KMAX+2], S[KMAX+2], G[KMAX+2];
static mpz_t B0, C, M, bm, t, nm, tmp;
static long TRACE_N=0;   /* entries already written to the trace (prefix + modular) */
static ul PREFIX_MAX=0;  /* largest numerator seen in the exact prefix */

static ul gcdul(ul x, ul y){ while(y){ ul r=x%y; x=y; y=r;} return x; }

/* replay: return b_k mod need in bm (and leave M = need). Asserts every divisibility. */
static void replay(int k, ul need){
  mpz_mul_ui(M, C, need);
  mpz_mod(bm, B0, M);
  for(int j=0;j<k;j++){
    /* n_j = (b_j + s_j)/a_j */
    mpz_add_ui(t, bm, S[j]); mpz_mod(t, t, M);
    if(!mpz_divisible_ui_p(t, A[j])) { fprintf(stderr,"BUG: a_j does not divide b+s at j=%d\n",j); exit(3);}
    mpz_divexact_ui(nm, t, A[j]);
    mpz_divexact_ui(M, M, A[j]);              /* now everything is mod M/a_j */
    mpz_mod(bm, bm, M); mpz_mod(nm, nm, M);
    mpz_mul(bm, bm, nm); mpz_mod(bm, bm, M);  /* b_j n_j mod M */
    if(!mpz_divisible_ui_p(bm, G[j]) || !mpz_divisible_ui_p(M, G[j])) { fprintf(stderr,"BUG: g at j=%d\n",j); exit(3);}
    mpz_divexact_ui(bm, bm, G[j]); mpz_divexact_ui(M, M, G[j]);
  }
  if(mpz_cmp_ui(M, need)!=0){ fprintf(stderr,"BUG: modulus bookkeeping\n"); exit(3);}
}

/* run the modular engine from exact base (a0, B0).  returns number of terms (>=1), or -1 if cap hit.
   if trace!=NULL, writes numerators a_0..a_{K} */
static long run_modular(ul a0, long cap, FILE *trace, ul *maxnum){
  mpz_set_ui(C, 1); A[0]=a0; *maxnum=a0;
  for(long k=0;;k++){
    if(trace) fprintf(trace, TRACE_N++? ",%lu":"%lu", A[k]);
    if(A[k]==1) return k+1;
    if(k>=cap) return -1;
    ul a=A[k];
    if(a > (1UL<<30)){ fprintf(stderr,"numerator overflow guard a=%lu\n",a); exit(4);}
    replay(k, 2*a);
    ul b2 = mpz_get_ui(bm);                 /* b_k mod 2a */
    ul r = (a - (b2 % a)) % a;
    if(r==0){ fprintf(stderr,"BUG: a_k divides b_k (gcd invariant)\n"); exit(3);}
    ul q2 = ((b2 + r) % (2*a)) / a;         /* q mod 2 */
    ul s = q2 ? r : r + a;                  /* q odd -> n=q ; q even -> n=q+1 */
    replay(k, a*s);
    ul bas = mpz_get_ui(bm);                /* b_k mod a*s */
    ul nmod = ((bas + s) % (a*s)) / a;      /* n_k mod s */
    ul bmod = bas % s;
    ul bn = (ul)(((unsigned __int128)bmod * nmod) % s);
    ul g = gcdul(s, bn);
    S[k]=s; G[k]=g; A[k+1]=s/g; if(A[k+1]>*maxnum)*maxnum=A[k+1];
    mpz_mul_ui(C, C, a); mpz_mul_ui(C, C, g);
    if(k+1>KMAX){ fprintf(stderr,"KMAX\n"); exit(5);}
  }
}


/* ---- O(K) variant: carry b_k mod M forward; M is built at a replay point from predicted future
   consumption (ramp prediction a_{j+1}=a_j+1, g_j=1) with generous slack; every requirement is
   checked before use, and a failed requirement just triggers a fresh replay from the exact base. ---- */
#define T_AHEAD 256
static long run_modular_fast(ul a0, long cap, FILE *trace, ul *maxnum, long *nreplays){
  mpz_set_ui(C, 1); A[0]=a0; *maxnum=a0; *nreplays=0;
  mpz_t P, Mf, bf, tt, nn; mpz_inits(P, Mf, bf, tt, nn, NULL);
  long k=0; int have=0;
  for(;;){
    if(trace) fprintf(trace, TRACE_N++? ",%lu":"%lu", A[k]);
    if(A[k]==1){ mpz_clears(P,Mf,bf,tt,nn,NULL); return k+1; }
    if(k>=cap){ mpz_clears(P,Mf,bf,tt,nn,NULL); return -1; }
    ul a=A[k];
    if(a > (1UL<<30)){ fprintf(stderr,"numerator overflow guard a=%lu\n",a); exit(4);}
    /* need 2a*a*s | Mf with s<2a unknown: require 4a^3-ish via divisibility tests below */
    for(int attempt=0;;attempt++){
      if(!have){
        /* P = prod_{j=0}^{T} 2*(a+j)^2*(a+j+1) * (2a)! -free slack: also include 2a*a*(any s<2a) for this step */
        mpz_set_ui(P, 1);
        for(ul j=0;j<=T_AHEAD;j++){ mpz_mul_ui(P,P,2*(a+j)); mpz_mul_ui(P,P,(a+j)); mpz_mul_ui(P,P,(a+j+1)); }
        if(attempt>0){ /* misprediction: add lcm-ish slack for every s < 2a at this step */
          for(ul s=2;s<2*a;s++) if(!mpz_divisible_ui_p(P,s)) mpz_mul_ui(P,P,s);
          mpz_mul_ui(P,P,a); mpz_mul_ui(P,P,2*a);
        }
        /* replay to step k with need = P (P may exceed ulong: do the replay inline) */
        mpz_mul(Mf, C, P); mpz_mod(bf, B0, Mf);
        for(long j=0;j<k;j++){
          mpz_add_ui(tt, bf, S[j]); mpz_mod(tt, tt, Mf);
          if(!mpz_divisible_ui_p(tt, A[j])){ fprintf(stderr,"BUG fast replay a\n"); exit(3);}
          mpz_divexact_ui(nn, tt, A[j]); mpz_divexact_ui(Mf, Mf, A[j]);
          mpz_mod(bf, bf, Mf); mpz_mod(nn, nn, Mf); mpz_mul(bf, bf, nn); mpz_mod(bf, bf, Mf);
          if(!mpz_divisible_ui_p(bf, G[j]) || !mpz_divisible_ui_p(Mf, G[j])){ fprintf(stderr,"BUG fast replay g\n"); exit(3);}
          mpz_divexact_ui(bf, bf, G[j]); mpz_divexact_ui(Mf, Mf, G[j]);
        }
        (*nreplays)++; have=1;
      }
      if(!mpz_divisible_ui_p(Mf, 2*a)){ have=0; continue; }
      ul b2 = mpz_fdiv_ui(bf, 2*a);
      ul r = (a - (b2 % a)) % a;
      if(r==0){ fprintf(stderr,"BUG: a_k divides b_k (gcd invariant)\n"); exit(3);}
      ul q2 = ((b2 + r) % (2*a)) / a;
      ul s = q2 ? r : r + a;
      /* need a*s | Mf */
      mpz_set_ui(tt, a); mpz_mul_ui(tt, tt, s);
      if(!mpz_divisible_p(Mf, tt)){ have=0; if(attempt>3){fprintf(stderr,"fast: cannot satisfy\n"); exit(6);} continue; }
      /* n_k = (b_k + s)/a mod Mf/a ; b_{k+1} = b_k n_k / g mod Mf/(a g) */
      mpz_add_ui(tt, bf, s); mpz_mod(tt, tt, Mf);
      if(!mpz_divisible_ui_p(tt, a)){ fprintf(stderr,"BUG fast step a\n"); exit(3);}
      mpz_divexact_ui(nn, tt, a); mpz_divexact_ui(Mf, Mf, a);
      mpz_mod(bf, bf, Mf); mpz_mod(nn, nn, Mf);
      ul bmod = mpz_fdiv_ui(bf, s), nmod = mpz_fdiv_ui(nn, s);
      ul g = gcdul(s, (ul)(((unsigned __int128)bmod*nmod)%s));
      mpz_mul(bf, bf, nn); mpz_mod(bf, bf, Mf);
      if(!mpz_divisible_ui_p(bf, g) || !mpz_divisible_ui_p(Mf, g)){ have=0; continue; }
      mpz_divexact_ui(bf, bf, g); mpz_divexact_ui(Mf, Mf, g);
      S[k]=s; G[k]=g; A[k+1]=s/g; if(A[k+1]>*maxnum)*maxnum=A[k+1];
      mpz_mul_ui(C, C, a); mpz_mul_ui(C, C, g);
      if(k+1>KMAX){ fprintf(stderr,"KMAX\n"); exit(5);}
      break;
    }
    k++;
  }
}

/* exact prefix phase; returns terms used in prefix, sets (*pa, B0) to hand-off state, or returns
   negative total if it terminated inside the prefix (as -(terms)). */
static long prefix(ul a, const mpz_t b, ul *pa, FILE *trace){
  mpz_t bb, n, prev, nunc, num; mpz_inits(bb,n,prev,nunc,num,NULL);
  mpz_set(bb,b); mpz_set_ui(prev,1); long terms=0; ul aa=a;
  for(;;){
    /* nunc = least odd >= bb/aa */
    mpz_cdiv_q_ui(nunc, bb, aa); if(mpz_even_p(nunc)) mpz_add_ui(nunc,nunc,1);
    mpz_add_ui(n, prev, 2);
    if(mpz_cmp(nunc, n)>=0 && mpz_cmp_ui(nunc,5)>=0){ /* safe hand-off */
      *pa=aa; mpz_set(B0,bb); mpz_clears(bb,n,prev,nunc,num,NULL); return terms; }
    if(mpz_cmp(nunc,n)>0) mpz_set(n,nunc);
    if(trace) fprintf(trace, TRACE_N++? ",%lu":"%lu", aa);
    if(aa>PREFIX_MAX) PREFIX_MAX=aa;
    /* x - 1/n = (aa*n - bb)/(bb*n) */
    mpz_mul_ui(num, n, aa); mpz_sub(num, num, bb); terms++;
    if(mpz_sgn(num)==0){ mpz_clears(bb,n,prev,nunc,num,NULL); return -terms; }
    if(mpz_sgn(num)<0){ fprintf(stderr,"BUG prefix\n"); exit(3);}
    mpz_mul(bb, bb, n); mpz_t gg; mpz_init(gg); mpz_gcd(gg, num, bb); mpz_divexact(num,num,gg); mpz_divexact(bb,bb,gg); mpz_clear(gg);
    if(!mpz_fits_ulong_p(num)){ fprintf(stderr,"prefix numerator too big\n"); exit(4);}
    aa=mpz_get_ui(num); mpz_set(prev,n);
  }
}

static int FAST=0; static long NREP=0;
static long expand(ul a, const mpz_t b, long cap, FILE *trace, ul *maxnum){
  ul ha; TRACE_N=0; PREFIX_MAX=0; long pt = prefix(a, b, &ha, trace);
  if(pt<0){ *maxnum=PREFIX_MAX; return -pt; }
  long r = FAST ? run_modular_fast(ha, cap, trace, maxnum, &NREP) : run_modular(ha, cap, trace, maxnum);
  if(PREFIX_MAX > *maxnum) *maxnum = PREFIX_MAX;
  return r<0 ? -1 : pt + r;
}

int main(int argc, char **argv){
  mpz_inits(B0,C,M,bm,t,nm,tmp,NULL);
  if(getenv("OG_FAST")) FAST=1;
  if(argc>=2 && !strcmp(argv[1],"one")){          /* og one a b [cap] : print length + numerator trace */
    mpz_t b; mpz_init_set_str(b, argv[3], 10); ul mx; long cap = argc>4? atol(argv[4]) : KMAX-1;
    long L = expand(strtoul(argv[2],0,10), b, cap, stdout, &mx);
    printf("\nlength=%ld maxnum=%lu\n", L, mx); return 0;
  }
  if(argc>=2 && !strcmp(argv[1],"fact")){         /* og fact a N [cap] [trace|-] [mult] : a/(mult*N! - 1) */
    mpz_t b; mpz_init(b); mpz_fac_ui(b, atol(argv[3])); if(argc>6) mpz_mul_ui(b,b,atol(argv[6])); mpz_sub_ui(b,b,1); ul mx;
    long cap = argc>4? atol(argv[4]) : KMAX-1;
    FILE *tr = (argc>5 && strcmp(argv[5],"-")) ? fopen(argv[5],"w") : NULL;
    long L = expand(strtoul(argv[2],0,10), b, cap, tr, &mx);
    if(tr) fclose(tr);
    printf("a=%s N=%s mult=%s length=%ld maxnum=%lu replays=%ld\n", argv[2], argv[3], argc>6?argv[6]:"1", L, mx, NREP); return 0;
  }
  if(argc>=2 && !strcmp(argv[1],"scan")){         /* og scan blo bhi [cap] : all reduced a/b, odd b in [blo,bhi] */
    long blo=atol(argv[2]), bhi=atol(argv[3]); long cap = argc>4? atol(argv[4]) : 2000;
    static unsigned long hist[KMAX]; long best=0; unsigned long nfr=0, fail=0; mpz_t b; mpz_init(b);
    unsigned long long fp=1469598103934665603ULL;           /* FNV-1a over (b,a,len) */
    if(blo%2==0) blo++;
    for(long bb=blo; bb<=bhi; bb+=2){ mpz_set_ui(b,bb);
      for(long a=1;a<bb;a++){ if(gcdul(a,bb)!=1) continue; if(getenv("OG_THIRD") && 3*a>=bb) continue; ul mx; long L=expand(a,b,cap,NULL,&mx); nfr++;
        if(L<0){ fail++; printf("NOTERM %ld/%ld\n",a,bb); continue;}
        hist[L]++; unsigned long long v[3]={(unsigned long long)bb,(unsigned long long)a,(unsigned long long)L};
        for(int i=0;i<3;i++){ fp^=v[i]; fp*=1099511628211ULL; }
        if(L>=best){ if(L>best) best=L; printf("REC %ld/%ld len=%ld maxnum=%lu\n",a,bb,L,mx); } } }
    printf("fractions=%lu fail=%lu maxlen=%ld fnv=%016llx\nHIST", nfr, fail, best, fp);
    for(long i=0;i<=best;i++) if(hist[i]) printf(" %ld:%lu",i,hist[i]); printf("\n"); return 0;
  }
  fprintf(stderr,"usage: og one a b | og fact a N [cap] [trace] | og scan blo bhi [cap]\n"); return 1;
}
