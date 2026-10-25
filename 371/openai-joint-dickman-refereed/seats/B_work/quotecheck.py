import re,html
s=open('/tmp/oaimath/012/entry/entry371.js').read()
t=html.unescape(re.sub(r'<[^>]+>','',s)); t=re.sub(r'\s+',' ',t)
L=open('/tmp/oaimath/012/entry/lean_label.txt').read()
qs=["§4 supposes the decorrelation fails along some sequence of scales and passes to a limit profile",
"Then read §4's profile extraction","Prop. 7.1 states c","the Lean statement and proof of #928 as posed",
"A scan of all 1,837 source files for forbidden constructs found nothing in the proof",
"Its import closure is 1,837 modules and 221,524 lines","The joint law approaches its limit slowly and from below",
"with no hypotheses","An independent re-check by","Littlewood-strength","September, $300","The citations hold",
"which is stronger","positive proportion of n","Erdős and Pomerance posed it in 1978","Tao and Teräväinen proved it in natural density at almost all scales",
"that predicts 0.2806","Each of the eight inputs","a Chebyshev bound","should be strict","O(B50/P₀)","margin of 10","character for character",
"Their 2026 paper","explicit n₀","Two of the library's docstrings","An older conditional route","Seat R found the same consequence unprompted",
"141 of them","Formal Conjectures and #928 in Lean (ours)","refereed here"]
for q in qs:
    print(('OK   ' if q in t else ('LABEL' if q in L else 'MISS ')), q)
print('lean_label tail:',repr(L.strip()[-40:]))
