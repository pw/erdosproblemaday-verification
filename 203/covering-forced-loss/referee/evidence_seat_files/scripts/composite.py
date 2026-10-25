# e_n := |<2,3> <= (Z/n)^x| by closure (BFS), for n = 35, 91, 55 and the prime factors.
def gen_order(n):
    seen = {1}; frontier = [1]
    while frontier:
        nxt = []
        for x in frontier:
            for g in (2, 3):
                y = x * g % n
                if y not in seen: seen.add(y); nxt.append(y)
        frontier = nxt
    return len(seen)
for n, (p, q) in [(35, (5, 7)), (91, (7, 13)), (55, (5, 11))]:
    ep, eq, en = gen_order(p), gen_order(q), gen_order(n)
    print(f"e_{n} = {en};  e_{p}={ep}, e_{q}={eq}, product={ep*eq};  e_pq == e_p*e_q ? {en == ep*eq};  index [L_p+L_q : ...] -> [Z^2 : L_{p}+L_{q}] = e_p e_q / e_pq = {ep*eq//en}")
