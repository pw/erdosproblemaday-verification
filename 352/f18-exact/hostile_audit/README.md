# Erdős #352: hostile audit of `f(18)=34`

This frozen bundle independently audits the computational-only finite claim

```text
f(18) = 34
```

in Koizumi's lattice model.  It does not solve the continuous Erdős problem or
prove the needed uniform estimate `f(N)=O(N)`.

The main reproduction commands are:

```bash
python3 producer_reverify.py --min-n 18 --max-n 18 --json
python3 audit_352_n18.py
python3 audit_exception_exact_cover.py
python3 audit_strict_predicate.py
python3 focused_exception_audit.py
```

The producer and focused checker are assertion-based and must be run with
ordinary `python3`, not `python3 -O`.  The hostile full audit and the two small
hostile audits use explicit exceptions for load-bearing checks and also pass
under `python3 -O`.

`public_reference_upper.py` is the unmodified upstream reference implementation
at commit `7a4a19468771766cb4f20e10dfa5cf770cc2487b`.  With exact coloring disabled,
it independently reproduces the 140 diameter cases, 108 cases with high points,
12,594 fixed-high branches, and the unique 35-point pair relaxation at
`B=(5,4)`.  Its JSON output is frozen as `public_upper_n18.json`.

See `AUDIT_REPORT.md` for the verdict and reasoning, and `SHA256SUMS` for exact
file identities.
