"""Compare OEIS A030541-A030546 and A031285 (David Broadhurst, 1999) with og's numerator sequences.
Cached OEIS JSON (fetched 2026-11-09) in oeis_cache/."""
import json, subprocess
names = {}
seqs = {}
for A in ["A030541","A030542","A030543","A030544","A030545","A030546","A031285"]:
    d = json.load(open(f"oeis_cache/{A}.json")); r = d if isinstance(d, list) else d["results"]; x = r[0]
    frac = x["name"].split("expansion of ")[1].split()[0] if "expansion of " in x["name"] else x["name"].split("algorithm for ")[1].split()[0]
    names[A] = frac; seqs[A] = x["data"].split(",")
ours = {}
for A, f in names.items():
    a, b = f.split("/")
    ours[f] = subprocess.run(["./og", "one", a, b], capture_output=True, text=True).stdout.split("\n")[0].split(",")
for A, f in names.items():
    hit = [g for g, u in ours.items() if u == seqs[A]]
    print(f"{A} named {f:>10}: data equals og's full sequence for {hit}  ({len(seqs[A])} numerators)")
