# Audit bundle: candidate R(C4,K1,39)=46 proof

This is a hostile independent audit of `zach7036/c4-star-ramsey` at exact commit
`86a1c5055eea5e3891b2eeaea6c7ee1b3977bd33`.

Verdict: **PASS for the finite theorem `R(C4,K1,39)=46`; GAP for peer-reviewed status and for the
repository's unrelated claims.** The proof is spectral/moment based and does not depend on the
uncertified 144-case SAT log.

Run:

```bash
PYTHON=/path/to/python ./run_audit.sh
```

The selected Python needs the exact upstream dependencies in `upstream_ro/requirements.txt` to
rerun every supplied verifier. `independent_verify_f39.py` itself uses only the standard library.

No site file was edited or deployed.

