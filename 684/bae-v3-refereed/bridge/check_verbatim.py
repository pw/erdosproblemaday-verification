# Diff our copied FC definition + upper_bound statement against FC's file (whitespace-normalised).
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
fc = open(sys.argv[1]).read(); ours = open(sys.argv[2]).read()
fc_def = re.search(r'def smallPrimePart \(n k : ℕ\) : ℕ :=(.*?)\n\n', fc, re.S).group(1)
our_def = re.search(r'def smallPrimePart \(n k : ℕ\) : ℕ :=(.*?)\n\n', ours, re.S).group(1)
fc_ub = re.search(r'theorem erdos_684\.upper_bound :(.*?):= by', fc, re.S).group(1)
our_ub = re.search(r'def FCUpperBound : Prop :=(.*?)\n\n', ours, re.S).group(1)
ok = norm(fc_def) == norm(our_def) and norm(fc_ub) == norm(our_ub)
print("def:", norm(our_def)); print("ub :", norm(our_ub)); print("VERBATIM" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
