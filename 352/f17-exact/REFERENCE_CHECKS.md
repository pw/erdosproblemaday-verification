# Independent checks

## Live-page gate

The Erdős Problems main page and dedicated proof-claim page were fetched
through Bright Data twice on 2026-08-12 UTC before this computation. The
rendered state was:

- status `OPEN`;
- 17 comments;
- 0 claimed proofs;
- `Currently working on this problem: None`;
- interested collaborators `Vjeko_Kovac, JineonBaek, J_Koizumi_144`;
- dedicated proof page: `No proof claims have been submitted yet.`

Thus the site's stop gate was clear at the time of the run.

## Lower witness

Public source:
`KitaKen1/erdos352-koizumi-n-avoiding-witness-table`, commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`.

Command:

```bash
python3 scripts/verify_witnesses.py data/witnesses/n017_32.json
```

Output:

```text
| N | size | ok | min_gap | triples | sha256 | file |
|---:|---:|:---:|---:|---:|---|---|
| 17 | 32 | yes | 5 | 5984 | `d990dc0cc3a4` | `data/witnesses/n017_32.json` |
```

The embedded points exactly match the public list. The public canonical point
digest is
`d990dc0cc3a4dcdff1bf28adc3f5fba032cde647f940981e7a7a10f7810f2a39`.

## Upper branches

Public source: `KitaKen1/erdos352-koizumi-fn-upper-bound`, commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`.

Command:

```bash
python3 exact_bound.py --n 17 --max-color-vertices 0 --output reference_upper_n17.json
```

This separate implementation reported:

```text
normalized diameter cases: 125
cases with high points: 94
fixed-high branches: 9414
maximum outside B=(5,4): 32
B=(5,4), no-high: pool 40, pairwise/coloring upper total 33
```

It took 54.67 seconds (`user=54.44`, `sys=0.16`) and 125,948 KiB maximum
resident memory. The raw output is included as `reference_upper_n17.json`.
Its SHA-256 is
`f4e101b150b7a8f3539576d5b17f7fa00b1d8895a185f7fc7fa44fb3616183dd`.

The separate implementation deliberately stops at the pairwise relaxation
33. The two self-contained checkers in this directory supply and independently
audit the additional triple obstruction lowering that last branch to 32.
