// canonical form: fills key (canonical layers), lab (lab[p] = vertex at canonical position p)
static void canon(u64 R,u64 B,u128& key,int* lab){
    const int nv=2*n, mm=SETWORDSNEEDED(nv);
    graph g[MAXN*MAXM], cg[MAXN*MAXM]; int ptn[MAXN], orbits[MAXN]; statsblk stats; DEFAULTOPTIONS_GRAPH(opt);
    opt.getcanon=TRUE; opt.defaultptn=FALSE;
    EMPTYGRAPH(g,mm,nv);
    for(int k=0;k<m;k++){ if(R>>k&1) ADDONEEDGE(g,ea[k],eb[k],mm); if(B>>k&1) ADDONEEDGE(g,n+ea[k],n+eb[k],mm); }
    for(int i=0;i<n;i++) ADDONEEDGE(g,i,n+i,mm);
    for(int i=0;i<nv;i++){ lab[i]=i; ptn[i]=1; } ptn[n-1]=0; ptn[nv-1]=0;
    densenauty(g,lab,ptn,orbits,&opt,&stats,mm,nv,cg);
    for(int p=0;p<n;p++) if(lab[p]>=n){ fprintf(stderr,"internal: nauty did not preserve the layer order\n"); exit(2); }
    // key = the canonical graph folded back into one coloured K_n: layer-0 positions carry the red edges; layer-1 positions
    // are mapped to layer-0 positions through the rungs (tau), and the blue edges are read in those coordinates. This is a
    // complete invariant (the folded graph IS the position); reading the two layers alone would drop the rung matching.
    u64 Rc=0,Bc=0; int tau[MAXN];
    for(int p=0;p<n;p++){ set* row=GRAPHROW(cg,p,mm); int cnt=0; for(int q=n;q<nv;q++) if(ISELEMENT(row,q)){ tau[q-n]=p; cnt++; } if(cnt!=1){ fprintf(stderr,"internal: rung count %d at position %d\n",cnt,p); exit(2);} }
    for(int p=0;p<n;p++){ set* row=GRAPHROW(cg,p,mm); for(int q=p+1;q<n;q++) if(ISELEMENT(row,q)) Rc|=1ULL<<eidx[p][q]; }
    for(int q1=0;q1<n;q1++){ set* row2=GRAPHROW(cg,n+q1,mm); for(int q2=q1+1;q2<n;q2++) if(ISELEMENT(row2,n+q2)) Bc|=1ULL<<eidx[tau[q1]][tau[q2]]; }
    key=((u128)Rc<<64)|Bc;
}
