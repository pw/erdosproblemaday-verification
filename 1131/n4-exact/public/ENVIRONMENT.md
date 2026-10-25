# Reproduction environment

The release was built and verified with exactly:

```text
UTC build date: 2026-08-11
Platform: Linux 6.12.93 x86_64, glibc 2.39
Python: 3.12.3
SymPy: 1.14.0
mpmath: 1.3.0
Bash: 5.2.21
GNU coreutils sha256sum: 9.4
```

`verify_exact.py` enforces the recorded Python and SymPy versions.
`verify_numeric.py` additionally enforces the recorded mpmath version.
`verify_manifest.py` uses only the Python standard library so that integrity
can be checked before third-party code is imported.

Create the virtual environment outside the closed bundle, then select its
interpreter explicitly while running the package:

```text
python3.12 -m venv /tmp/erdos1131-public-venv
/tmp/erdos1131-public-venv/bin/pip install -r requirements-exact.txt
PYTHON=/tmp/erdos1131-public-venv/bin/python ./run_all.sh
```

For the optional numerical smoke check, install instead from
`requirements-numeric.txt` and append `--with-numeric` to the final command.
An in-tree virtual environment is deliberately rejected as an extra member.
Package versions are pinned but packages and their license texts are not
vendored here. `run_all.sh` accepts `PYTHON` only as one executable path and
uses that same interpreter for the manifest, exact, and numerical checks.
