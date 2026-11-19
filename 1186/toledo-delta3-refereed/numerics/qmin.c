// Minimise f(x) = x^T M x (M symmetric, row-major double) over boxes / +-1 vectors.
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

static uint64_t rs;
static inline uint64_t rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline double urand(void){ return (rnd() >> 11) * (1.0/9007199254740992.0); }

static void matvec(int N, const double *M, const double *x, double *g){
  for (int i=0;i<N;i++){ const double *r=M+(size_t)i*N; double s=0; for(int j=0;j<N;j++) s+=r[j]*x[j]; g[i]=s; }
}
static double fval(int N, const double *M, const double *x){
  double *g=malloc(sizeof(double)*N); matvec(N,M,x,g); double f=0; for(int i=0;i<N;i++) f+=x[i]*g[i]; free(g); return f;
}
double qval(int N, const double *M, const double *x){ return fval(N,M,x); }

// coordinate descent with exact 1-D minimisation on [-1,1]; returns sweeps used
int cd_box(int N, const double *M, double *x, int maxsweeps, double tol, unsigned long long seed){
  rs = seed*2654435761ULL + 88172645463325252ULL;
  double *g=malloc(sizeof(double)*N); int *perm=malloc(sizeof(int)*N);
  matvec(N,M,x,g);
  for(int i=0;i<N;i++) perm[i]=i;
  int sw;
  for(sw=0; sw<maxsweeps; sw++){
    for(int i=N-1;i>0;i--){ int j=rnd()%(i+1); int t=perm[i]; perm[i]=perm[j]; perm[j]=t; }
    double maxch=0;
    for(int k=0;k<N;k++){
      int i=perm[k]; const double *r=M+(size_t)i*N;
      double d=r[i], ri=g[i]-d*x[i], xn;
      if(d>0){ xn=-ri/d; if(xn>1) xn=1; if(xn<-1) xn=-1; }
      else xn = (ri>0)? -1.0 : 1.0;
      double dx=xn-x[i];
      if(dx!=0){ x[i]=xn; for(int j=0;j<N;j++) g[j]+=r[j]*dx; if(fabs(dx)>maxch) maxch=fabs(dx); }
    }
    if(maxch<tol) break;
  }
  free(g); free(perm); return sw;
}

// simulated annealing on +-1 vectors, single flips + interval flips. x in/out (best found).
// T geometric from T0 to T1 over 'steps' proposals. Returns best f.
double sa_pm1(int N, const double *M, double *x, long steps, double T0, double T1,
              double pblock, int maxblock, unsigned long long seed){
  rs = seed*2654435761ULL + 88172645463325252ULL;
  double *g=malloc(sizeof(double)*N), *best=malloc(sizeof(double)*N);
  matvec(N,M,x,g);
  double f=0; for(int i=0;i<N;i++) f+=x[i]*g[i];
  double fb=f; memcpy(best,x,sizeof(double)*N);
  double lr = log(T1/T0);
  for(long s=0;s<steps;s++){
    double T = T0*exp(lr*(double)s/(double)steps);
    if(pblock>0 && urand()<pblock){
      int L = 2 + (int)(urand()*(maxblock-1)); if(L>N) L=N;
      int l = rnd()%(N-L+1);
      double d1=0, d2=0;
      for(int i=l;i<l+L;i++){ d1+=x[i]*g[i]; const double *r=M+(size_t)i*N; for(int j=l;j<l+L;j++) d2+=x[i]*r[j]*x[j]; }
      double delta = -4*d1 + 4*d2;
      if(delta<=0 || urand()<exp(-delta/T)){
        for(int i=l;i<l+L;i++){ const double *r=M+(size_t)i*N; double c=-2*x[i]; for(int j=0;j<N;j++) g[j]+=r[j]*c; }
        for(int i=l;i<l+L;i++) x[i]=-x[i];
        f+=delta;
      }
    } else {
      int i=rnd()%N; const double *r=M+(size_t)i*N;
      double delta = -4*x[i]*(g[i]-r[i]*x[i]);
      if(delta<=0 || urand()<exp(-delta/T)){
        double c=-2*x[i]; for(int j=0;j<N;j++) g[j]+=r[j]*c; x[i]=-x[i]; f+=delta;
      }
    }
    if(f<fb-1e-9){ fb=f; memcpy(best,x,sizeof(double)*N); }
  }
  memcpy(x,best,sizeof(double)*N);
  fb = fval(N,M,x);   // recompute exactly from scratch
  free(g); free(best); return fb;
}

// 1-flip tabu search on +-1 vectors; returns best f, x <- best.
double tabu_pm1(int N, const double *M, double *x, long iters, int tenure, int tenrand, unsigned long long seed){
  rs = seed*2654435761ULL + 88172645463325252ULL;
  double *g=malloc(sizeof(double)*N), *best=malloc(sizeof(double)*N);
  long *tabu=calloc(N,sizeof(long));
  matvec(N,M,x,g);
  double f=0; for(int i=0;i<N;i++) f+=x[i]*g[i];
  double fb=f; memcpy(best,x,sizeof(double)*N);
  for(long it=1; it<=iters; it++){
    int bi=-1; double bd=INFINITY; int nties=0;
    for(int i=0;i<N;i++){
      double delta=-4*x[i]*(g[i]-M[(size_t)i*N+i]*x[i]);
      int ok = (tabu[i]<it) || (f+delta < fb-1e-9);
      if(!ok) continue;
      if(delta<bd-1e-12){ bd=delta; bi=i; nties=1; }
      else if(fabs(delta-bd)<=1e-12){ nties++; if(rnd()%nties==0) bi=i; }
    }
    if(bi<0) continue;
    const double *r=M+(size_t)bi*N; double c=-2*x[bi];
    for(int j=0;j<N;j++) g[j]+=r[j]*c;
    x[bi]=-x[bi]; f+=bd;
    tabu[bi]=it+tenure+(tenrand>0? (long)(rnd()%tenrand):0);
    if(f<fb-1e-9){ fb=f; memcpy(best,x,sizeof(double)*N); }
  }
  memcpy(x,best,sizeof(double)*N);
  fb=fval(N,M,x);
  free(g); free(best); free(tabu); return fb;
}
