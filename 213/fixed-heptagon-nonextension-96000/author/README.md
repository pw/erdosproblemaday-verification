# Erdos 213: bounded nonextension of the 22270 heptagon

This frozen bundle proves one exact, deliberately narrow result:

> The published Kreisel-Kurz diameter-22270 integral heptagon has no eighth
> point whose distances to all seven vertices are positive integers at most
> 96000.

Read `PROOF.md` for the reduction and `LITERATURE.md` for the public 70000
comparison. `LIVE_GATE.md` records the mandatory live-page and collision
checks. The result does **not** prove that arbitrary eight-point sets have
diameter above 96000, and it does not solve Erdos problem 213.

Run:

```sh
./reproduce.sh
```

The script builds and runs the independent C++ and Go scanners, compares their
machine-readable summaries, validates the source matrix JSON, and checks the
frozen manifest when present.
