# Problem 149: exact Delta=4 strong-clique corollary

This frozen bundle audits a literature corollary for Erdős Problem 149. It is
not presented as our discovery.

Run:

```bash
./run_all.sh
```

The core exact result is

```text
max omega(L(G)^2) = 20
```

where the maximum is over finite simple graphs of maximum degree at most 4.
The parent strong-coloring question is not closed: the verified interval is

```text
20 <= max chi(L(G)^2) <= 21.
```

See `REPORT.md` for scope and provenance and `PROOF_AUDIT.md` for the source
typo and corrected fixed-constant reconstruction.
