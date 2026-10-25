#!/usr/bin/env python3
"""Collect fs/ results from /tmp/erdos85-fs into fs/out/ and print a per-cell table (kissat verdict, CaDiCaL+DRAT)."""
import csv, glob, os, shutil
from pathlib import Path
T = Path('/tmp/erdos85-fs'); O = Path(__file__).resolve().parent / 'out'; O.mkdir(exist_ok=True)
for f in ['cells.tsv', 'feas.out', 'h9.tsv', 'drat.tsv', 'er7ctl.out', 'er7ctl_r1b.out', 'erqctl.out', 'erdescend_hsb.out',
          'compctl.out', 'dratneg.out', 'slotcheck.out', 'h1norm_erctl.out', 't0/h7t0.out', 't0nohsb/h7t0.out', 'hsb/h7t1.out', 'h1/h1.out', 'h1n/h1n.out', 'h1n/h1n_slots.out']:
    if (T / f).exists(): shutil.copy(T / f, O / f.replace('/', '_'))
for f in ['sbtest.out', 'sbtest2.out']:
    p = Path(__file__).resolve().parent / f
    if p.exists(): shutil.copy(p, O / f)
rows = {}
for f in ['cells.tsv', 'feas.out', 'h9.tsv', 't0/h7t0.out', 't0nohsb/h7t0.out', 'hsb/h7t1.out', 'h1/h1.out', 'h1n/h1n.out', 'h1n/h1n_slots.out']:
    if not (T / f).exists(): continue
    for line in open(T / f):
        p = line.rstrip('\n').split('\t')
        if len(p) < 5 or not p[0].startswith('h'): continue
        rows.setdefault(p[0], []).append((p[2], p[3], p[4]))
drat = {}
if (T / 'drat.tsv').exists():
    for line in open(T / 'drat.tsv'):
        p = line.rstrip('\n').split('\t')
        if len(p) >= 4 and p[0].startswith('h'): drat[p[0]] = (p[1], p[3], p[2], p[4])
print('| cell | kissat (s) | cnf sha256/16 | CaDiCaL | drat-trim | DRAT bytes |')
print('|---|---|---|---|---|---|')
for c in sorted(rows):
    vs = [r for r in rows[c] if r[0] != 'UNKNOWN'] or rows[c]
    v = vs[-1]
    d = drat.get(c, ('', '', '', ''))
    print(f'| {c} | {v[0]} ({v[1]}) | {v[2]} | {d[0].replace("s ", "")} | {d[1].replace("s ", "")} | {d[2]} |')
