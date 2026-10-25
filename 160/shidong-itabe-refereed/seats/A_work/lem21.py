# Exhaustive check of Shi-Dong Lemma 2.1 (+ the proof's intermediate claims) for even k, primes k<p<P.
import sys
def primes(lo, hi):
    return [q for q in range(lo, hi) if q > 1 and all(q % r for r in range(2, int(q**.5)+1))]
tot = viol = claimA = claimB = nontriv = 0
for k in (4, 6, 8, 10, 12):
    for p in primes(k+1, 220):
        tau = [((k-1)*x)//p for x in range(p)]
        for s in range(p):
            for x0 in range(p):
                xs = [(x0 + i*s) % p for i in range(k)]
                if not all(tau[xs[i-1]] == tau[xs[k-i]] for i in range(1, k//2+1)):
                    continue
                tot += 1
                e = [int(xs[i+1] < xs[i]) for i in range(k-1)]
                if len(set(e)) != 1:
                    viol += 1; print("VIOLATION", k, p, s, x0, xs, e)
                # proof claims: s < p/(k-1) or s > (k-2)p/(k-1) (strict); all points in one interval
                if not ((k-1)*s < p or (k-1)*s > (k-2)*p):
                    claimA += 1; print("claimA fails", k, p, s, x0)
                if len(set(tau[x] for x in xs)) != 1:
                    claimB += 1; print("claimB fails", k, p, s, x0)
                if s not in (0,):
                    nontriv += 1
print(f"tau-symmetric digit APs checked={tot} (nonzero step: {nontriv})  carry violations={viol}  "
      f"step-gap claim failures={claimA}  one-interval claim failures={claimB}")
# negative control: odd k=5 (k-1=4 intervals) and a fake 'tau' with only 2 intervals must produce violations
def run(k, p, nint):
    bad = 0
    tau = [(nint*x)//p for x in range(p)]
    for s in range(p):
        for x0 in range(p):
            xs = [(x0 + i*s) % p for i in range(k)]
            if all(tau[xs[i-1]] == tau[xs[k-i]] for i in range(1, k//2+1)):
                e = [int(xs[i+1] < xs[i]) for i in range(k-1)]
                bad += len(set(e)) != 1
    return bad
print("control k=4,p=11 with only 2 intervals (i-1 == i+1 mod 2):", run(4, 11, 2), "(expect >0)")
print("control k=6,p=31 with only 2 intervals:", run(6, 31, 2), "(expect >0)")
sys.exit(1 if (viol or claimA or claimB) else 0)
