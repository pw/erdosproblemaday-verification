# Integration notes

This is an additive extension to the separately frozen `n<=32` package.  It
does not alter that checkpoint.

Suggested site path:

```text
verification/840/s-k-n-exact-33-37/
```

Suggested ledger text:

```text
Exact finite proxy extended again: every value of
s(k,n)=max{|A+A|:A subset [n], |A|=k} is now certified through n=37.  The new
producer enumerates exactly 2^36 translated subsets.  At terminal n=37, the
five nontrivial upper cells k=9..13 have independent CaDiCaL and Kissat UNSAT
results with replayed DRAT proofs (seven proof cases, because k=9 is split by
diameter).  Finite computational progress only; #840 remains open
asymptotically.
```

Suggested report addition:

```markdown
## 2026-08-12 exact extension through 37

The finite Pikhurko proxy is now exact through `n=37`; its terminal row is
\[
(s(k,37))_{k=1}^{37}=
(1,3,6,10,15,21,28,36,43,51,59,64,69,73,\ldots,73).
\]
The complete producer visited exactly `2^36` translated subsets.  At `n=37`,
the five nontrivial upper cells `k=9,...,13` were independently encoded from
the definition: CaDiCaL and Kissat both returned UNSAT, and all seven CaDiCaL
DRAT proof cases replayed successfully.  This extends exact finite data only;
the asymptotic quasi-Sidon problem remains open.
```

Before integration:

1. `python3 verify_bundle.py`
2. `python3 verify_bundle.py --replay-drat`
3. Preferably, when compute permits, `python3 verify_bundle.py --rerun-primary`
   (approximately 5.5 minutes on the production VM).
4. Add only the targeted #840 report/checker/bundle paths to commits.
5. Regenerate the site ledger, deploy, purge, and verify the canonical route.

If any one of the seven SAT/proof cases is absent or fails replay, do not
publish this extension; retain the already-audited `n<=32` checkpoint.
