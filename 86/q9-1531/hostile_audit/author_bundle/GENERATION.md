# Generation record

The search used the same min-conflicts algorithm as the previously audited
1506-edge result. The bundled source differs by one non-semantic cleanup:
`seeds.size()` is explicitly cast to `int` after the cube size bounds it well
below `INT_MAX`, eliminating a strict `-Wconversion` warning. The heuristic is
provenance rather than a proof input; its fast 1505-to-1506 control is rebuilt
and checked by `reproduce.sh`.

1. Starting from `provenance/q9_edges_1506.json`, sequential extension found
   witnesses of every size from 1507 through 1530.  Targets 1507 through 1530
   used the recorded master seeds `708111507`, `708111508`, `708111509`, then
   `708110000 + target`; each output was checked immediately by the existing
   independent common-neighbour verifier.
2. One eight-thread 60-second attempt at 1531 did not finish with a witness.
   A second run from the 1530 certificate, master seed `861531002`, found the
   frozen 1531-edge raw output in about 69 seconds.
3. An eight-thread 180-second attempt at 1532, master seed `861532001`, was
   stopped by `timeout` with exit status 124 and no output certificate.

OpenMP makes the identity of the first winning thread schedule-dependent.
The bundle therefore does not promise byte-identical heuristic regeneration.
The canonical JSON changes only descriptive metadata from the preserved raw
output; its 1531-edge set is identical.  Reproduction verifies that explicit
edge set exhaustively and does not rerun the heuristic.

As a fast source-level positive control, the reproducer rebuilds the generator
and repeats the public-1505 to site-1506 extension with one thread and master
seed 1. It reproduces the same 1506-edge set. The JSON bytes differ only
because the preserved 1506 file records its original input path in metadata;
the comparison therefore ignores metadata and requires exact edge-set equality.
