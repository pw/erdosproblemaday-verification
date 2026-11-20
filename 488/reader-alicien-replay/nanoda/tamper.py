# Negative control for nanoda (2026-11-20): give Erdos488.erdos_488_card_le_two (the export's last declaration) the TYPE
# of Erdos488.not_erdos_488, keeping its proof term. A sound checker must reject it.
# Usage: python3 tamper.py export.ndjson export_tamper_type.ndjson   (then nanoda_bin cfg_ctrl_tamper.json)
import json, sys
lines = open(sys.argv[1]).read().split('\n')
names = {}
for l in lines:
    if l.startswith('{"in"'):
        o = json.loads(l); names[o['in']] = o.get('str') or o.get('num')
def nm(i):
    out = []
    while i and i in names:
        e = names[i]; out.append(str(e.get('str', e.get('i', '?')))); i = e['pre']
    return '.'.join(reversed(out))
idx = {}
for i, l in enumerate(lines):
    if l.startswith('{"thm"'):
        o = json.loads(l); n = nm(o['thm']['name'])
        if n in ('Erdos488.not_erdos_488', 'Erdos488.erdos_488_card_le_two'): idx[n] = (i, o)
(i1, a), (i2, b) = idx['Erdos488.not_erdos_488'], idx['Erdos488.erdos_488_card_le_two']
assert i2 > i1
b['thm']['type'] = a['thm']['type']
lines[i2] = json.dumps(b, separators=(',', ':'))
open(sys.argv[2], 'w').write('\n'.join(lines))
print('tampered declaration on line', i2)
