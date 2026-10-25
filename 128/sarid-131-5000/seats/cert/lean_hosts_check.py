#!/usr/bin/env python3
"""Lean's 38 representative host masks (ClassificationSoundness.classificationHostMasks, bit e <-> edgeEnds e,
the lexicographic pair order) versus my two-route host census; and my verifier run on Lean's own representatives."""
import re, sys
sys.path.insert(0, '/tmp/erdos1800/seats/cert'); import myverify as mv
src = open('/tmp/erdos1800/claim/erdos-128-sparse-halves/lean/Erdos128/C4Certificate/ClassificationSoundness.lean').read()
blk = src[src.index('def classificationHostMasks'):src.index('theorem order6Codes_length')]
masks = [int(x) for x in re.findall(r'\d+', blk.split(':=', 1)[1])]
reps = [mv.adj_from_mask(m, 6) for m in masks]
print('Lean reps:', len(masks), ' all triangle-free:', all(mv.tri_free(a) for a in reps))
mine = {mv.canon6(a) for a in mv.hosts_geng()}
lean = [mv.canon6(a) for a in reps]
print('distinct classes among Lean reps:', len(set(lean)), ' equal to my 38 classes:', set(lean) == mine)
C = mv.coords(); E = mv.Expansion(reps, C); eps, terms = mv.load_cert()
ok, mins, need, worst = mv.check_fast(E, eps, terms)
print('my verifier on the Lean representative labellings: ok =', ok, ' min slack =', float(mins), ' eps needed =', float(need))
