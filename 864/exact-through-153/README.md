# Erdős #864: target-20 finite boundary

This bundle tests the computational claim that no valid 20-point set has
diameter at most 151 and supplies a valid 20-point witness of diameter 152.

Fast checks:

```bash
python3 verify_witness.py
python3 scan_construction.py
python3 verify_direct_logs.py
python3 compare_counts.py
sha256sum -c SHA256SUMS
```

Full rebuild:

```bash
g++ -O3 -DNDEBUG -std=c++17 search20_direct.cpp -o search20_direct
g++ -O3 -std=c++17 audit20_lowerhalf.cpp -o audit20_lowerhalf
MAX_JOBS=14 ./run_direct.sh
/usr/bin/time -v ./audit20_lowerhalf > audit_output.txt 2> audit_time.txt
python3 compare_counts.py
```

Exit status 2 from an exhaustive program means that it found and printed a
counterexample; status 0 means that the requested search was exhausted.
