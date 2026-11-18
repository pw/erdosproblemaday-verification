#!/usr/bin/env python3
"""Rebuild the cake_lpr negative controls of controls/controls_cake.txt from s21_587_1.cnf and its proof
s21_587_1.lrat (CaDiCaL 3.0.1 --lrat --no-binary; SHA-256 29be5fc9...0c98 = his ledger).  Writes:
  m_trunc.lrat            proof without its last 1000 lines (no empty clause)
  m_hint.lrat             one hint in an addition line near the middle decremented by one
  m_emptynohint.lrat      m_trunc + an empty clause with no hints
  m_emptybadhint.lrat     m_trunc + an empty clause whose only hint is clause 1 (already deleted)
  m_emptylivehint.lrat    m_trunc + an empty clause whose only hint is the last clause added (live, no conflict)
  m_dropclause.cnf        formula without its first clause (renumbers everything)
  m_weaken1.cnf           formula with clause 1 (-1 -2, cited by the first proof line) weakened in place to (-1 -2 3)
Run cake_lpr on each pair; only the intact pair may print 's VERIFIED UNSAT'."""
import random
lines = open('s21_587_1.lrat').read().splitlines(True); n = len(lines)
keep = lines[:n - 1000]
open('m_trunc.lrat', 'w').writelines(keep)
random.seed(7)
idx = [i for i in range(n // 3, 2 * n // 3) if ' d ' not in lines[i] and len(lines[i].split(' 0 ')[-1].split()) > 3]
i = idx[len(idx) // 2]; parts = lines[i].split(); z = parts.index('0'); h = parts[z + 1]
parts[z + 1] = str(int(h) - 1 if int(h) > 1 else int(h) + 1); mut = lines[:]; mut[i] = ' '.join(parts) + '\n'
open('m_hint.lrat', 'w').writelines(mut)
last = int(lines[n - 1001].split()[0])
open('m_emptynohint.lrat', 'w').writelines(keep + [f"{last + 1} 0 0\n"])
open('m_emptybadhint.lrat', 'w').writelines(keep + [f"{last + 1} 0 1 0\n"])
adds = [l for l in keep if l.split()[1] != 'd']; lid = adds[-1].split()[0]
newid = max(int(l.split()[0]) for l in keep) + 1
open('m_emptylivehint.lrat', 'w').writelines(keep + [f"{newid} 0 {lid} 0\n"])
cnf = open('s21_587_1.cnf').read().splitlines(True)
hdr = [l for l in cnf if l.startswith('p ')][0]; body = [l for l in cnf if not l.startswith(('p ', 'c '))]
v, c = hdr.split()[2:4]
open('m_dropclause.cnf', 'w').writelines([f"p cnf {v} {int(c) - 1}\n"] + body[1:])
j = [k for k, l in enumerate(cnf) if not l.startswith(('p', 'c'))][0]; assert cnf[j].strip() == '-1 -2 0'
w = cnf[:]; w[j] = '-1 -2 3 0\n'; open('m_weaken1.cnf', 'w').writelines(w)
print('mutated proof line', i, '; live hint clause', lid)
