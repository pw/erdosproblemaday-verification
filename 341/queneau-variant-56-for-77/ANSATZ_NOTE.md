# The dead-end ansatz (why the controller was searched for, not solved for)

Ansatz: keep Li's block positions and let the three rails be
  Y0 = {0} ∪ ⋃_k [4·8^k + s, 8·8^k + e],  Y1 = F1 ∪ ⋃_k [16·8^k + s1, 32·8^k + e1],  Y2 = F2 ∪ ⋃_k [64·8^k + s2, 128·8^k + e2]
with 0 ∈ Y1 and 0 ∈ Y2 as well (so that 0 + block = block in every sumset) and integer offsets s, e, s1, e1, s2, e2.
Under the strict sumset X ⊕ X an interval [a, b] (b > a) contributes [2a+1, 2b−1] from itself and [a, b] from 0 + [a, b];
the union is [a, 2b − 1] when 2a + 1 ≤ b + 1, i.e. for Li's 2:1 blocks. So for large k:
  Y0 ⊕ Y0 ⊇ [4·8^k + s, 16·8^k + 2e − 1]  ⇒  Y1's block = [16·8^k + 2e, 32·8^k + s − 1]:   s1 = 2e,  e1 = s − 1
  Y1 ⊕ Y1 ⊇ [16·8^k + s1, 64·8^k + 2e1 − 1] ⇒ Y2's block = [64·8^k + 2e1, 128·8^k + s1 − 1]: s2 = 2e1, e2 = s1 − 1
  Y2 ⊕ Y2 ⊇ [64·8^k + s2, 256·8^k + 2e2 − 1] ⇒ Y0's block = 1 + [256·8^k + 2e2, 512·8^k + s2 − 1]: s = 2e2 + 1, e = s2
Hence s = 2(2e − 1) + 1 = 4e − 1 and e = 2(s − 1) = 2s − 2, so s = 8s − 9, i.e. 7s = 9: no integer solution.
(Under the equal rule the same ansatz gives s = 2e2 + 2, e1 = s − 1, s1 = 2e + 1, … and Li's s = 0, e = −1 works
because his finite parts are not {0} on every rail — the ansatz is too narrow there too.)

What the search found (ic = 27) has Y0 on [8^k + 1, 2·8^k], i.e. at a different phase than 4·8^k, and 0 ∉ Y1 (Y1 = {1} ∪ …):
both assumptions of the ansatz fail, which is why solving within it could not find the controller. The forced dynamics
(gates.py / census.c) do not assume a shape at all.
