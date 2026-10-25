#!/usr/bin/env python3
"""Mutation test of statement_match.py (03:00Z seat, 2026-10-23). Each mutant edits a COPY of the probe logs; the matcher
must exit 1 (mismatch / bad axioms) or 2 (cannot see). Run from the replay directory holding logs/ and statement_match.py."""
import shutil, subprocess, os, re, sys, tempfile
M = tempfile.mkdtemp(prefix='matchmut-')
def mut(name, fname, old, new, regex=False):
    d = f'{M}/{name}'; shutil.copytree('logs', d)
    if old is None: os.remove(f'{d}/{fname}')
    else:
        t = open(f'{d}/{fname}').read()
        t2 = re.sub(old, new, t, count=1) if regex else t.replace(old, new, 1)
        if t2 == t: print(name, 'ANCHOR NOT FOUND'); return False
        open(f'{d}/{fname}', 'w').write(t2)
    r = subprocess.run([sys.executable, 'statement_match.py', d], capture_output=True, text=True)
    print(f'{name:30s} rc={r.returncode}'); return r.returncode != 0
r = subprocess.run([sys.executable, 'statement_match.py', 'logs'], capture_output=True, text=True); print('baseline rc', r.returncode)
ok = r.returncode == 0
ok &= mut('pow2_to_pow3_solution', 'ax_JacobsthalImproved.log', '(nat_lit 2) (instOfNatNat (nat_lit 2))', '(nat_lit 3) (instOfNatNat (nat_lit 3))')
ok &= mut('const3_to_2_solution', 'ax_JacobsthalImproved.log', '(nat_lit 3)', '(nat_lit 2)')
ok &= mut('lt_m_to_le_m_solution', 'ax_Jacobsthal.log', '(@LT.lt.{0} Nat instLTNat i m)', '(@LE.le.{0} Nat instLENat i m)')
ok &= mut('card_le_to_lt_comparator', 'cmp_Jacobsthal.log', '@LE.le.{0} Nat instLENat (@Finset.card', '@LT.lt.{0} Nat instLTNat (@Finset.card')
ok &= mut('extra_axiom_solution', 'ax_Jacobsthal.log', '[propext, Classical', '[propext, sorryAx, Classical')
ok &= mut('sorry_removed_comparator', 'cmp_JacobsthalImproved.log', r'sorryAx(\.\{u\})?,\s*', '', regex=True)
ok &= mut('missing_file', 'cmp_Jacobsthal.log', None, None)
print('ALL MUTANTS CAUGHT' if ok else 'A MUTANT SURVIVED (or baseline failed)'); sys.exit(0 if ok else 1)
