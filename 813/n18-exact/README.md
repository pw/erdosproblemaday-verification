# Erdős problem 813: compact h(18)=5 bundle

This compact bundle supports the computer-assisted finite result

\[
h(18)=5.
\]

The exact confidence label is **PROVED (computer-assisted; solver
assertions)**.  The mathematical reductions, canonical census membership,
CNF semantics, and exact sweep coverage were independently audited.  The
complete d=7--d=12 UNSAT results do not have a retained DRAT/LRAT certificate
for every branch.  One difficult d=10 branch is included as a compressed,
independently replayable DRAT spot check.

Run the compact audit with only Python's standard library:

```bash
python3 verify_public.py
```

The bundled `drat-trim` executable targets Linux x86-64.  On another platform,
use:

```bash
python3 verify_public.py --skip-drat
```

`--quick` also skips the exhaustive `2^21` labelled check of the 71 order-7
non-neighbour types.

## What is and is not included

- `REPORT.md` gives the proof structure, exact counts, hashes, and caveat.
- `censuses/` contains all small H/M graph6 catalogs used for d=7--d=10,
  plus their independently generated parent catalogs.
- `audits/` contains the exact coverage-auditor outputs.
- `tools/audit_all_d7_d12.py` independently scans the offline raw logs and
  both earlier solver tables; its included transcript certifies gap-free
  degree coverage from 7 through 12.
- `prior_delta10/` is the earlier frozen d=11/d=12/order-13 bundle.
- `spot/` contains gzip-compressed DIMACS and DRAT for d=10 flat case 512188.
- `hostile_audit/` is the frozen independent publication-verdict bundle.
- `OFFLINE_RAW_LOGS.sha256` binds every complete raw sweep log in the included
  `SWEEP_LOGS.tar.zst` archive.

The 269MB raw logs are included as the 29MB compressed archive
`SWEEP_LOGS.tar.zst`, whose SHA256 is
`da4f63a9eba8cecd2449667acf9e9e6a6edabd07ed6953a1ce3e63f8669900a3`.
The full 454MB forensic bundle is `/tmp/erdos813_h18_exact/`, with manifest
SHA256
`42729713ce756273a519043d5ab51574ab0a7ec20d925ee52d0d8b743e0b2715`.
