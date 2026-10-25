s = open('mutate.py').read()
old = """    p = f'{W}/{name}.py'
    open(p, 'w').write(s)
    t0 = time.time()
    r = subprocess.run(['bash', '-c', f'ulimit -v 8000000; exec timeout 1800 nice -n 19 python3 -I {p}'], capture_output=True, text=True)
"""
new = """    p = f'{W}/{name}.py'
    assert s.count("    print(k,*counts)") == 1
    open(p, 'w').write(s.replace("    print(k,*counts)", "    print(k,*counts, flush=True)"))
    t0 = time.time()
    lim = int(os.environ.get('MUT_TIMEOUT', '900'))
    r = subprocess.run(['bash', '-c', f'ulimit -v 8000000; exec timeout {lim} nice -n 19 python3 -I {p}'], capture_output=True, text=True)
"""
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
old2 = "print(name, 'rc', r.returncode,"
assert s.count(old2) == 1
s = s.replace(old2, "print(name, 'rc', r.returncode, 'ks_done', [x[0] for x in rows],")
open('mutate.py', 'w').write(s)
print('patched')
