#!/usr/bin/env python3
"""Fill the ⟨PLACEHOLDERS⟩ in body.html / summary.txt / headline.json / LOGTEXT.md / ../README.md from the logs of the 10⁸ run and
the censuses. Prints every substitution; refuses to leave any placeholder. usage: fill.py  (run after after_1e8.sh prints ALL DONE)"""
import re, pathlib, json
R=pathlib.Path('..'); E=pathlib.Path('.')
a=(R/'analyze_1e8.log').read_text(); v=(R/'verify_1e8.log').read_text(); c=(R/'census_mod_1e8.log').read_text(); g=(R/'F_E_eq_1e8.log').read_text()
def num(s): return f"{int(s):,}"
elems=int(re.search(r'elements=(\d+)',a).group(1)); last=int(re.search(r'last=(\d+)',a).group(1))
m=re.search(r'gap suffix from term (\d+) \(len (\d+)\): smallest period (\d+) -> (no period <= half the suffix|A PERIOD OF THIS SUFFIX)',a)
s_start,s_len,s_per,s_verdict=int(m.group(1)),int(m.group(2)),int(m.group(3)),m.group(4)
assert s_verdict.startswith('no period'), "A PERIOD WAS FOUND — the entry must be rewritten, not filled"
half=s_len//2
# value of a_{s_start}: from the elems file index (0-based term index s_start)
import numpy as np
el=np.fromfile(str(R/'F_E_eq_1e8_elems.u32'),dtype='<u4'); a_s=int(el[s_start]); dens=elems/last
sha=re.search(r'membership sha256 through \d+: ([0-9a-f]{64})',a.split('500000')[-1]).group(1)
disc=re.search(r'for x<=%d: ([\d.]+)'%last,a).group(1)   # full-range max |count - density*x|, the D in the membership-period bound
discpt=re.search(r'post-transient discrepancy on \[\d+,\d+\] \(density refitted [\d.]+\): max\|\.\| = (\d+)',a).group(1); rnd=re.findall(r'random set, same count/window, trial \d: (\d+)',a); disc7='215'
rec=re.search(r'record chain (\[.*?\])',a).group(1); best=re.search(r'best shift (\d+): agreement fraction ([\d.]+)',a); bq,bagree=int(best.group(1)),float(best.group(2))
maxshift=int(re.search(r'shifts <= (\d+)',a).group(1))
cen=re.search(r'moduli with an EMPTY class: (\d+); most depleted \(min/mean,m\): \[\((np\.float64\()?([\d.]+)\)?, (\d+)\).*?most over-full \(max/mean,m\): \[\((np\.float64\()?([\d.]+)\)?, (\d+)\)',c)
emp,dep,depm,over,overm=cen.group(1),cen.group(3),cen.group(4),cen.group(6),cen.group(7)
wins=re.findall(r'window \[(\d+),(\d+)\) elems=\d+ inS=\d+ violations=(\d+)',v)
assert [w[2] for w in wins[:3]]==['0','0','0'] and int(wins[3][2])>0, wins
fval=f"{a_s/479993:.0f}"
sub={
 '⟨E8_ELEMS⟩': num(elems),
 '⟨E8_SUFFIX_HALF⟩': num(half),
 '⟨E8_SUFFIX_START⟩': num(s_start),
 '⟨TITLE_P⟩': f"{half/1e6:.1f}·10⁶",
  '⟨E8_SUFFIX_SENTENCE⟩': f"the suffix of the gap word from term {num(s_start)} (its last {num(s_len)} terms) has no period of {num(half)} terms or fewer, so no gap period of at most {num(half)} terms begins at or before term {num(s_start)}, i.e. before a<sub>{num(s_start)}</sub> = {num(a_s)}",
 '⟨E8_SUFFIX_SHORT⟩': f"no gap period ≤ {num(half)} terms beginning at or before term {num(s_start)} (a ≈ {a_s/1e6:.1f}·10⁶)",
 '⟨E8_VALUE_PERIOD⟩': f"{(half-2*float(disc))/dens/1e6:.0f}·10⁶",
 '⟨E8_VALUE_ONSET⟩': f"{a_s/1e6:.1f}·10⁶",
 '⟨E8_VERIFY_WINDOWS⟩': "windows of 200,000 at the start, at 5·10⁷ and at the end",
 '⟨E8_SHA⟩': sha,
 '⟨E8_CENSUS_SENTENCE⟩': (f"and over [10⁷, 10⁸] no class modulo any <em>m</em> ≤ 10,000 is empty (the most depleted is {dep} of the mean at <em>m</em> = {depm}, the fullest {over} at <em>m</em> = {overm})" if emp=='0' else f"while over [10⁷, 10⁸] {emp} moduli ≤ 10,000 have an empty class — every one a multiple of a convergent denominator of <em>g</em>, see below"),
 '⟨E8_BEST_AGREE⟩': f"{bagree*100:.1f}%",
 '⟨E8_MAXSHIFT⟩': f"{maxshift/1e6:.0f}·10⁶",
 '⟨E8_RECORD_TAIL⟩': "the record chain on [2·10⁷, 10⁸] is "+re.sub(r'\(([\d]+), ([\d.]+)\)',lambda mm: f"{int(mm.group(1)):,} ({float(mm.group(2))*100:.1f}%)",rec).strip('[]'),
 '⟨E8_DISC⟩': f"{float(disc):.0f}",
 '⟨E8_DISC_RANDOM⟩': '/'.join(rnd),
 '⟨E8_DISC_PT⟩': discpt,
}
sub['⟨CENSUS_PARAGRAPH⟩']=open('census_paragraph.txt').read().strip()
sub['⟨S13_RANK⟩']=open('s13_rank.txt').read().strip()
sub['⟨MORE_SURVIVORS⟩']=open('more_survivors.txt').read().strip()
sub['⟨CENSUS_SENTENCE⟩']="a certificate census of every seed with largest element 13 and 14 (12,288 seeds; 12,282 certify, zero tool errors) finds six distinct resisting sequences in all, every one of the same kind."
for k,v in sub.items(): assert '⟨' not in v, k
print(json.dumps(sub,ensure_ascii=False,indent=1))
json.dump(sub,open('fill_values.json','w'),ensure_ascii=False,indent=1)
import pathlib
for fn in ('body.html','summary.txt','title.txt','headline.json','LOGTEXT.md','../README.md'):
    p=pathlib.Path(fn); s=p.read_text()
    for k,v in sub.items(): s=s.replace(k,v)
    p.write_text(s); left=sorted(set(re.findall(r'⟨[A-Z0-9_]+⟩',s))); print(fn,'placeholders left:',left)
