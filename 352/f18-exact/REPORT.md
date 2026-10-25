# Exact finite value `f(18)=34` for Erdős problem 352

In Koizumi's equivalent lattice model, a finite set `S` in `Z^2` is
`N`-avoiding when every triple `p,q,r`, with repetitions allowed, obeys

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

The largest size of such a set at `N=18` is exactly 34. This is a finite
computer-assisted result; it does not establish the uniform linear bound
needed to solve the continuous problem.

The lower bound is an existing 34-point witness. All 7,140 triples pass the
exact squared predicate `(A2-36)^2-4D2>0`, with minimum integer margin 21.

For the upper bound, normalize a diameter pair to `(0,0),B`. There are 140
possible `B` vectors. Exhausting the no-high branch and every fixed-high
branch gives 12,734 directly audited coloring certificates. Every branch is
at most 34 except the no-high pair relaxation for `B=(5,4)`, which gives 35.

That remaining pool has 42 candidates and 57 incompatibility edges. A
nine-edge matching forces any hypothetical compatible 33-subset to omit
exactly one endpoint per matching edge. Of the 512 choices, exactly two are
vertex covers. Their surviving 33-sets contain, respectively, the forbidden
triples

```text
(1,-1),(1,4),(6,1)     (1,-1),(1,4),(6,2)
(-1,2),(4,0),(4,5)     (-1,3),(4,0),(4,5).
```

Each has doubled area 25, squared diameter 34, and exact margin
`(25-36)^2-4*34=-15`. Thus the pool has at most 32 compatible candidates,
and restoring the diameter pair gives the upper bound 34.

See `README.md` for reproduction, provenance, hashes, and the independent
public implementation cross-check.
