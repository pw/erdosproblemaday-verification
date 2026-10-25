# Problem 213: bounded nonextension of one integral heptagon

This directory proves the following exact bounded statement:

> The published Kreisel-Kurz diameter-22,270 integral heptagon has no distinct
> planar point whose distances to all seven vertices are positive integers at
> most 96,000.

This is a theorem about extending one fixed seven-point metric. It is not a
lower bound for the minimum diameter of an arbitrary eight-point set, not a
proof that the heptagon is globally inclusion-maximal, and not a solution of
Erdos Problem 213.

- `author/` contains the metric, geometric reduction, complete C++ and Go
  scans, candidate residue, source snapshots, and logs. Its manifest hash is
  `8dc4ce03a4bc8e6e8873c314e11f2efefb9840bcb38b62f32d9b5ce2d979aa47`.
- `hostile_audit/` contains a third sum/difference traversal, an independent
  arbitrary-precision metric checker, a primary-source parser, boundary and
  coincidence tests, and the audit report. Its manifest hash is
  `edbdb1e8e105b8ff38bf34030e29eddb6c078b53cac8e44c88f6a4296b7a7dd4`.

The earlier 70,000 computation in Kreisel-Kurz concerns general-position sets
of a restricted characteristic. Since 2,002 is in that class, the new result
raises the overlapping general-position fixed-heptagon cutoff to 96,000. The
new computation separately allows the eighth point to create collinearities or
concyclicities; it does not imply that the older search covered such cases.

Run `./reproduce.sh` to verify both manifests and rerun all three exhaustive
scanners and the primary-source checks.
