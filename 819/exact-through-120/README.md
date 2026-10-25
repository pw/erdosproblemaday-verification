# Verification bundle: Erdős #819, exact `f(N)` for `81<=N<=120`

This directory is self-contained and was prepared under `/tmp`; neither
project repository was edited.

Files:

- `REPORT.md`: theorem, proof, live gate, table audit, and scope.
- `verify.py`: dependency-free exhaustive producer and 189 literal
  small-instance cross-checks.
- `producer_output.txt`: frozen producer transcript.
- `hostile_check.cpp`: independent count-array implementation.
- `hostile_output.txt`: optimized hostile transcript.
- `hostile_sanitized_output.txt`: byte-identical ASan+UBSan transcript.
- `live_page_capture.txt`, `live_discussion_capture.txt`: Bright Data live
  captures from 2026-08-12.
- `MANIFEST.sha256`: hashes for all published files in this directory.

Run `python3 verify.py` without `-O`; the script uses explicit failures rather
than assertions, but ordinary mode is the audited invocation.
