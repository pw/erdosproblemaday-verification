#!/usr/bin/env python3
"""Finite all-future periodicity certificate (our July 2026 Lemma [a], /report/341) for EITHER summand rule.
Given a seed, a rule (equal|distinct) and a computed greedy prefix (elems file), propose (N,q) from the detected
gap period, then PROVE: T = P ∪ {x ≥ N : x mod q ∈ R} equals the greedy extension and is q-periodic from N, by
(1) T∩[1,M] = seed, (2) the recurrence x∈T ⟺ x∉T+T (resp. x ∉ {u+v : u,v∈T, u≠v}) for all M < x ≤ X0, computed
from scratch on the proposed T by FFT sumsets (not from the greedy run), (3) E+R = Z_q \ R where E=(P mod q)∪R.
Cutoff X0: equal rule X0 = 2N+q-2 (July lemma). Distinct rule X0 = 2N+2q-2, and the lemma's proof changes in one place:
for x > X0 a representation x=u+v (u≠v) has a tail summand (two P-elements sum to ≤ 2N-2); if the other summand is
p∈P then u≠v is automatic (x-p ≥ N > p); if both are tail elements with residues e,r∈R then — when e≠r — u = least
tail element ≡ e gives v = x-u ≥ N, v ≡ r, u≠v; when e = r the tail elements ≡ e in [N, x-N] number at least two
once x-2N+1 ≥ 2q, i.e. x ≥ 2N+2q-1, so one of them is not x/2 and gives a DISTINCT pair. Conversely x∈T+T (distinct)
forces x mod q ∈ E+R exactly as before. Hence for x > X0 the recurrence is the residue identity (3); below X0 it is
checked directly. (Gap found by the 2026-10-13 blind read: the first version used 2N+q-2 for both rules.)
Exit 0 = certified, 1 = not certified."""
import sys, numpy as np
def _main():
    rule, elems_path, qgap = sys.argv[1], sys.argv[2], int(sys.argv[3]); seed=[int(x) for x in sys.argv[4:]]
    distinct = (rule=='distinct')
    el=np.fromfile(elems_path,dtype='<u4').astype(np.int64); M=max(seed)
    assert el[:len(seed)].tolist()==seed
    # propose (N,q): find the earliest index K such that a_{n+qgap} = a_n + Q for all n >= K up to the end
    G=len(el); shifts=el[qgap:]-el[:-qgap]
    Q=int(shifts[-1]); ok=(shifts==Q)
    # earliest K with ok[K:] all True
    bad=np.nonzero(~ok)[0]; K=int(bad[-1])+1 if len(bad) else 0
    N=int(el[K]); print(f"rule={rule} seed={seed} proposed: gap period {qgap}, membership period q={Q}, onset term index {K} (0-based), N={N}")
    if K+qgap>=G: print("NOT CERTIFIED: periodic tail shorter than one period"); sys.exit(1)
    P=[int(x) for x in el if x<N]; R=sorted({int(x)%Q for x in el[K:K+qgap]})
    assert len(R)==qgap, (len(R),qgap)
    # build T up to L=2N+Q-2 (+ a margin) from the PROPOSAL only
    L=(2*N+2*Q-2) if distinct else (2*N+Q-2)
    L=max(L,M+1)   # 2026-10-15: when the proposed onset N <= max(seed) the lemma's check end can fall below the seed; build T through M+1 so the seed assertion and the (empty) recurrence range are well-defined
    T=np.zeros(L+1,dtype=bool); T[P]=True
    xs=np.arange(N,L+1); T[xs[np.isin(xs%Q,R)]]=True
    assert np.nonzero(T[:M+1])[0].tolist()==seed, "T∩[1,M] != seed"
    # pair sums of T up to L via FFT convolution (ordered-pair counts); distinct rule removes the u=v diagonal
    Lp=1
    while Lp<2*(L+1): Lp*=2
    F=np.fft.rfft(T.astype(np.float64),Lp); cnt=np.rint(np.fft.irfft(F*F,Lp)[:L+1]).astype(np.int64)
    if distinct:
        ev=np.arange(0,L+1,2); cnt[ev]-=T[ev//2].astype(np.int64)
    SS=cnt>0
    # recurrence check for M < x <= L
    x=np.arange(M+1,L+1); viol=x[(T[x])==(SS[x])]
    print(f"recurrence on ({M},{L}]: violations={len(viol)} first={viol[:5].tolist()}")
    E=sorted({p%Q for p in P}|set(R)); ER={(e+r)%Q for e in E for r in R}
    cond3 = (ER == set(range(Q))-set(R))
    print(f"E+R = Z_q \\ R : {cond3}  (|E|={len(E)} |R|={len(R)} |E+R|={len(ER)})")
    cert = (len(viol)==0) and cond3
    print("CERTIFIED" if cert else "NOT CERTIFIED")
    sys.exit(0 if cert else 1)
if __name__=="__main__":
    try: _main()
    except SystemExit: raise
    except Exception as e:
        print("TOOL ERROR:",type(e).__name__,e); sys.exit(3)   # 2026-10-15: a crash must never read as NOT CERTIFIED (referee item 19)
