# Erdős #819 hostile replay record

Date: 2026-08-12 UTC

Producer bundle audited: `/tmp/erdos819_exact_81_120`

## Producer manifest and amendment

The amended producer manifest passed `sha256sum -c MANIFEST.sha256` for all
nine listed files.

```text
cb5eb429d37b4dfb4e4e356fec098b32b19ba6dfdc9980ae28773c62c92d641a  MANIFEST.sha256
a8d6309385f2e58b8bf76283030565d8ee40768a01534c02f9c6df598e3e83de  REPORT.md
```

Replacing the corrected collision paragraph in memory with the original
paragraph reconstructed the pre-amendment report digest exactly:

```text
b59e5839b82f51242cce8c059223419277742963a59e1ebdd99461304a6f5258
```

Thus the correction was the only report change.

## Fresh Python producer replay

Command:

```text
python3 /tmp/erdos819_exact_81_120/verify.py
```

The raw stdout is `producer_fresh_output.txt`, SHA-256
`92edda3f63622a2e8ec2cac0273c88ba7105999a00eee23ff75d7e4096612645`.
Its parsed JSON equals the frozen producer JSON in every field except the
documented runtime (`55.135558` fresh versus `56.973817` frozen), and both end
with `ALL CHECKS PASSED`.  The frozen stdout has SHA-256
`a8d26ca39c6711fd6f336705b901014e95bb16e058a80ef589948622fc625366`.

## Fresh C++ replays

The producer's `hostile_check.cpp` was freshly compiled and run as follows:

```text
g++ -O3 -std=c++20 -Wall -Wextra -pedantic hostile_check.cpp -o hostile_check
./hostile_check

g++ -O1 -g -std=c++20 -Wall -Wextra -pedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  hostile_check.cpp -o hostile_check_sanitized
ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=print_stacktrace=1 \
  ./hostile_check_sanitized
```

No sanitizer diagnostic was emitted.  The optimized fresh output, sanitized
fresh output, frozen optimized output, and frozen sanitized output are all
byte-identical, with SHA-256
`e51b7b57aa34410b69bff729195762db6f538bf064e066dd7bc94530467f627d`.
The two fresh raw outputs are included here.

## Independent literal fixed-last kernel check

Command:

```text
python3 fixed_last_literal_check.py \
  /tmp/erdos819_exact_81_120/verify.py
```

The checker literally enumerates the internal marks on 335 small fixed-last
instances and compares their definition-level Sidon existence to the
producer's recursive result.  All 335 agree.  Source and stdout are included.

## Deliberate exclusions

Two exploratory CP-SAT formulations were interrupted while still `UNKNOWN`
on their first case.  They produced no result and are not audit evidence;
their scratch sources and empty outputs are excluded.  Compiled binaries,
the temporary public-repository clone, copied producer sources, and duplicate
producer-bundle files are also excluded.
