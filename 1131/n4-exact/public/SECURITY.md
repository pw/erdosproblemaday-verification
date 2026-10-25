# Integrity design and hostile checks

`run_all.sh` treats `MANIFEST.sha256.pin` as the in-archive bootstrap. Before
executing package Python, it checks the manifest digest against that pin,
preflights every listed member without opening it, and uses GNU `sha256sum` to
authenticate `verify_manifest.py`. It launches the authenticated verifier with
Python's isolated and safe-path flags. That verifier authenticates every
payload and requires the directory to contain exactly the listed payload plus
the manifest and pin. It rejects symlinks and every non-regular file.
The optional `PYTHON` environment variable selects one executable path, which
is then reused for all three isolated Python invocations.

The deterministic archive SHA-256 published separately is the external trust
root. The in-archive pin is not a signature and cannot by itself detect a
coordinated replacement of the pin and manifest.

Before release, the following hostile cases were exercised on temporary
copies and all exited nonzero:

* `python3 -O` and `python3 -OO` for every Python entry point;
* `PYTHONOPTIMIZE=1 ./run_all.sh`;
* an unlisted regular file and an unlisted `__pycache__` directory;
* a missing listed file;
* a listed file replaced by a symlink with identical content;
* a listed file replaced by a FIFO;
* an unlisted `hashlib.py` import-shadow payload;
* a false symbolic coefficient combined with regenerated manifest and pin;
* the same false symbolic checker invoked directly with `python3 -O`.

An AST scan found zero `assert` statements in all Python files. Verdicts use
explicit conditions and nonzero exits. The coordinated mathematical mutation
was rejected by the exact certificate even after its local integrity metadata
was regenerated.
