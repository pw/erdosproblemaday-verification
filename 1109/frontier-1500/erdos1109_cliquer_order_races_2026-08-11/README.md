# Cliquer ordering races

These runs were launched only to prevent a few late hard negatives from
dominating the external audit. The preferred `reverse` audit was never
stopped and ultimately completed all 163 decisions, so none of these races
is load-bearing for the final result.

All graphs here are byte-for-byte copies of the corresponding DIMACS graph
used by the completed audit. `input_sha256.txt` records graph, solver-runner,
and runner-source hashes.

## Outcome

The `unweighted-coloring` run for `n=1489` finished first and independently
reported `No such clique found.` Its exact log is
`logs/n1489_unweighted-coloring.log`, SHA-256
`0cac9977a0db6b451265f21efcd080efe7b27bc313f6f50c872f4cc0b06bd2fd`.

Every other alternate was terminated only after the matching exact
`reverse` result had appeared in the primary Cliquer log. The UTC time, PID,
case, ordering where applicable, and reason are recorded in
`redundant_cancellations.log`. The per-case logs retain command, input hashes,
elapsed time to cancellation, and signal status. In the raw launcher result
files, `PARSE_ERROR` means that the deliberately cancelled process produced
neither a positive clique nor Cliquer's final negative line; it is not used
as a mathematical result.

The `default` races were stopped once it was noticed that Cliquer documents
`default` as an alias for `unweighted-coloring` on unweighted graphs. The
genuinely different capped orderings were `degree` and `none`, each invoked
through a 1800-second timeout. They too were cancelled when their reverse
counterpart finished.

An initial xargs launcher attempt failed before any solver started because
`race_dir` was not exported. Its output is retained as
`results_launcher_error.txt`; the corrected launcher hash follows it in
`input_sha256.txt`.

