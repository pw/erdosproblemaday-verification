# Negative control: plant two bugs in exact.solve and confirm the brute-force cross-check catches each.
import random, exact
src = open('exact.py').read()
mutants = {
  'cap_at_1': src.replace("v = tuple(vval(b, p, e[p]) for p in P)", "v = tuple(vval(b, p, 1) for p in P)"),
  'drop_specials': src.replace("special = [(b, v) for b, v in vecs.items() if sum(v) >= 2]", "special = []"),
}
for name, code in mutants.items():
    assert code != src, name
    ns = {}; exec(compile(code.replace("if __name__ == '__main__':", "if False:"), name, 'exec'), ns)
    random.seed(708); caught = 0
    for trial in range(400):
        n = random.choice([2, 3, 4]); A = sorted(random.sample(range(2, 23), n)); x = random.randrange(0, 5000)
        try:
            g, _ = ns['solve'](A, x)
        except Exception:
            caught += 1; continue      # mutant crashed or its own certificate assertion fired
        gb, _ = exact.brute_min(A, x, max(g, 1) + 6)
        if gb != g: caught += 1
    print(name, 'caught on', caught, 'of 400')
