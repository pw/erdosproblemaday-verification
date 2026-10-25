import json, sys, copy
recs = [json.loads(l) for l in open('c40.jsonl')]
out = []
# 1: bump a final weight in a class-1 record
r = copy.deepcopy(recs[0]); r['final']['options'][0][2] += 1; out.append(r)
# 2: spurious initial flag (bit 0 on first pair)
r = copy.deepcopy(recs[0]); r['initial'][0][2] |= 1; out.append(r)
# 3: drop rounds from a class-2 record with rounds
c2 = [x for x in recs if x['rounds']]
r = copy.deepcopy(c2[0]); r['rounds'] = []; out.append(r)
# 4: bump radius of a round witness option
r = copy.deepcopy(c2[1]); r['rounds'][0][0]['witness']['options'][0][1] = 2; r['rounds'][0][0]['witness']['options'][0][2] += 1; out.append(r)
# 5: duplicate base in final witness
r = copy.deepcopy(recs[0]); r['final']['options'].append(list(r['final']['options'][0])); out.append(r)
# 6: unmodified (must pass)
out.append(copy.deepcopy(c2[0]))
with open('neg.jsonl', 'w') as f:
    for r in out: f.write(json.dumps(r) + '\n')
print(len(out), 'class2 with rounds in c40:', len(c2))
