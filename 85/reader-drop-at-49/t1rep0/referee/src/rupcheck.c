/* referee rupcheck: independent STRICT RUP-only LRAT checker (no RAT accepted).
 *   rupcheck FILE.cnf [binary|text] < proof
 * Binary parsing mirrors Std.Tactic.BVDecide.LRAT.Parser.Binary (zero byte anywhere in a varint fails,
 * shift-28 excess check, ids must be positive, RAT hint lists rejected).
 * Every addition: lemma literals falsified; each hint must be LIVE (defined, not deleted); a hint
 * with a true literal is skipped (sound); 0 unassigned => conflict (success); 1 => propagate;
 * >=2 => FAIL. No conflict after the hints => FAIL (no pure-literal / RAT fallback, incl. empty clause).
 * Addition ids must not collide with a live id. Exit 0 only if an empty clause was derived by conflict
 * and every action before AND after it checked; exit 1 on any failure; exit 2 on usage/IO/parse error. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>

static int **cls; static long long cap; static long long *falseAt; static long long litcap;
static long long step;
static void die(const char*m){fprintf(stderr,"rupcheck: %s\n",m);exit(2);}
static void fail(const char*m,long long a,long long id){printf("FAIL: %s (%lld) at action id %lld\n",m,a,id);fflush(stdout);exit(1);}
static inline long long li(long long l){return l>0? 2*l : 2*(-l)+1;}
static void ensure_lit(long long l){ long long need=li(l>0?l:-l)+2; if(need>=litcap){ long long nc=need*2; falseAt=realloc(falseAt,nc*sizeof *falseAt); if(!falseAt)die("oom"); memset(falseAt+litcap,0,(nc-litcap)*sizeof *falseAt); litcap=nc; } }
static void ensure_id(long long id){ if(id>=cap){ long long nc=id*3/2+16; cls=realloc(cls,nc*sizeof *cls); if(!cls)die("oom"); memset(cls+cap,0,(nc-cap)*sizeof *cls); cap=nc; } }
static int *mk(long long *lits,long long n){ int*c=malloc((n+1)*sizeof(int)); if(!c)die("oom"); c[0]=(int)n; for(long long i=0;i<n;i++){ if(lits[i]==0||lits[i]>INT32_MAX||lits[i]<-INT32_MAX)die("bad lit"); c[i+1]=(int)lits[i]; ensure_lit(lits[i]); } return c; }

static long long nadd=0,ndel=0,ndelwarn=0,nsathint=0,ntaut=0,nonmono=0,lastid=0,maxid=0,emptyAt=-1,actions=0,nhints=0;
static long long *L,*H; static long long Lcap=1<<16,Hcap=1<<16;

static void add(long long id,long long *lits,long long n,long long *hints,long long nh){
  step++; int taut=0;
  for(long long i=0;i<n;i++){ ensure_lit(lits[i]); if(falseAt[li(-lits[i])]==step) taut=1; falseAt[li(lits[i])]=step; }
  int conflict=0;
  if(taut){ ntaut++; conflict=1; }
  for(long long k=0;k<nh && !conflict;k++){
    long long h=hints[k]; nhints++;
    if(h<=0 || h>=cap || !cls[h]) fail("hint not live/undefined",h,id);
    int*c=cls[h]; int un=0, unit=0, sat=0;
    for(int j=1;j<=c[0];j++){ long long m=c[j];
      if(falseAt[li(m)]==step) continue;
      if(falseAt[li(-m)]==step){ sat=1; break; }
      if(un==0){ un=1; unit=(int)m; } else if(m!=unit){ un=2; }
    }
    if(sat){ nsathint++; continue; }
    if(un==0){ conflict=1; break; }
    if(un>=2) fail("hint has >=2 unassigned literals",h,id);
    falseAt[li(-(long long)unit)]=step;
  }
  if(!conflict) fail("hints end without conflict (no RAT/pure-literal fallback here)",nh,id);
  ensure_id(id);
  if(cls[id]) fail("addition id collides with live clause",id,id);
  if(id<=lastid) nonmono++;
  cls[id]=mk(lits,n); lastid=id; if(id>maxid)maxid=id; nadd++;
  if(n==0 && emptyAt<0){ emptyAt=actions; printf("EMPTY CLAUSE derived by conflict: id %lld, action #%lld, %lld hints\n",id,actions,nh); }
}
static void del(long long *ids,long long n){ for(long long i=0;i<n;i++){ long long d=ids[i]; if(d<=0||d>=cap||!cls[d]){ndelwarn++;continue;} free(cls[d]); cls[d]=0; ndel++; } }

/* ---- binary input ---- */
static FILE*in; static int pk=-1;
static int peekb(void){ if(pk<0){ pk=fgetc(in); } return pk; }
static int getb(void){ int c=peekb(); pk=-1; return c; }
static long long rdlit(void){ uint64_t u=0; unsigned sh=0; for(;;){ int b=getb(); if(b==EOF)die("eof in varint"); if(sh==28 && (b & ~15)) die("Excessive literal (Std would fail)"); if(b==0) die("zero byte in varint (Std would fail)"); u|=(uint64_t)(b&127)<<sh; if(!(b&128))break; sh+=7; }
  long long idx=(long long)(u>>1); return (u&1)? -idx: idx; }
static void binary(void){
  for(;;){
    int c=getb(); if(c==EOF) break; actions++;
    long long nl=0,nh=0;
    if(c=='a'){
      long long id=rdlit(); if(id<=0) die("non-positive id");
      while(peekb()!=0){ if(peekb()==EOF)die("eof"); if(nl>=Lcap){Lcap*=2;L=realloc(L,Lcap*sizeof*L);} L[nl++]=rdlit(); }
      getb();
      while(peekb()!=0 && !(peekb()&1)){ if(peekb()==EOF)die("eof"); if(nh>=Hcap){Hcap*=2;H=realloc(H,Hcap*sizeof*H);} long long h=rdlit(); if(h<=0)die("bad hint"); H[nh++]=h; }
      if(peekb()!=0) fail("RAT hints present (strict RUP checker)",0,id);
      getb();
      add(id,L,nl,H,nh);
    } else if(c=='d'){
      while(peekb()!=0 && !(peekb()&1)){ if(peekb()==EOF)die("eof"); if(nh>=Hcap){Hcap*=2;H=realloc(H,Hcap*sizeof*H);} long long h=rdlit(); H[nh++]=h; }
      if(peekb()!=0) die("negative id in deletion");
      getb(); del(H,nh);
    } else die("expected a or d");
  }
}
/* ---- text input (toy tests) ---- */
static void text(void){
  long long id; char tok[64];
  while(fscanf(in,"%lld",&id)==1){
    actions++; long long nl=0,nh=0,x;
    if(fscanf(in," %63s",tok)!=1) die("eof");
    if(!strcmp(tok,"d")){ while(fscanf(in,"%lld",&x)==1 && x!=0){ if(nh>=Hcap){Hcap*=2;H=realloc(H,Hcap*sizeof*H);} H[nh++]=x; } del(H,nh); continue; }
    x=strtoll(tok,0,10);
    while(x!=0){ if(nl>=Lcap){Lcap*=2;L=realloc(L,Lcap*sizeof*L);} L[nl++]=x; if(fscanf(in,"%lld",&x)!=1)die("eof"); }
    while(fscanf(in,"%lld",&x)==1 && x!=0){ if(x<0) fail("RAT hint (strict)",x,id); if(nh>=Hcap){Hcap*=2;H=realloc(H,Hcap*sizeof*H);} H[nh++]=x; }
    add(id,L,nl,H,nh);
  }
}
int main(int argc,char**argv){
  if(argc<2) die("usage: rupcheck FILE.cnf [binary|text] < proof");
  int bin = !(argc>2 && !strcmp(argv[2],"text"));
  FILE*f=fopen(argv[1],"r"); if(!f) die("open cnf");
  long long V=0,C=0; char line[256];
  while(fgets(line,sizeof line,f)){ if(line[0]=='c')continue; if(sscanf(line,"p cnf %lld %lld",&V,&C)==2)break; die("no header"); }
  L=malloc(Lcap*sizeof*L); H=malloc(Hcap*sizeof*H); litcap=0; ensure_lit(V+1); ensure_id(C+1);
  long long n=0,x,nl=0;
  while(fscanf(f,"%lld",&x)==1){ if(x==0){ n++; ensure_id(n); cls[n]=mk(L,nl); nl=0; } else { if((x>0?x:-x)>V) die("cnf var > header V"); if(nl>=Lcap){Lcap*=2;L=realloc(L,Lcap*sizeof*L);} L[nl++]=x; } }
  if(!feof(f)) die("cnf: trailing junk"); if(nl) die("cnf: unterminated clause"); fclose(f);
  if(n!=C) die("cnf clause count != header");
  lastid=n; maxid=n;
  printf("cnf: V=%lld C=%lld parsed=%lld\n",V,C,n); fflush(stdout);
  in=stdin; if(bin) binary(); else text();
  printf("actions=%lld adds=%lld dels=%lld del_of_nonlive=%lld hints_used=%lld satisfied_hints_skipped=%lld taut_lemmas=%lld nonmonotone_ids=%lld last_id=%lld\n",actions,nadd,ndel,ndelwarn,nhints,nsathint,ntaut,nonmono,lastid);
  if(emptyAt<0){ printf("NOT VERIFIED: no empty clause\n"); return 1; }
  printf("RUP-VERIFIED (strict): empty clause at action #%lld\n",emptyAt); return 0;
}
