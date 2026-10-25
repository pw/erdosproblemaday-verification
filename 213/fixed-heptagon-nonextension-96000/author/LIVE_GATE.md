# Live gate for Erdos problem 213

Accessed 2026-08-11 through the Bright Data browser path:
<https://www.erdosproblems.com/213>

The rendered page showed:

- status: `OPEN`;
- `0 claimed proofs for this problem`;
- `Currently working on this problem: None`;
- `Interested in collaborating: None`;
- `0 comments on this problem`;
- last edited: 16 October 2025;
- tags: geometry, distances.

The statement asks whether, for every `n >= 4`, there are `n` planar points
with no three collinear, no four concyclic, and all pairwise distances
integral. The page says the best construction to date is the seven-point
Kreisel-Kurz construction. It explicitly says `See also [130]`.

That cross-reference is material and is not hidden here. Problem 130 concerns
the chromatic and clique numbers of the integer-distance graph of an infinite
general-position set; problem 213 asks for finite complete integer-distance
sets of arbitrary order. The local site files contain only a SKIP marker for
130 and no statement or work product in that framework. Exact problem-number
213 references and the phrases `integer distance`, `integral distance`, and
`integral point set` were absent from both `src/index.js` and
`src/ledger_data.js` at the gate commit/worktree snapshot. Related distance-set
work on the site was inspected and did not contain this all-pairs-integral
construction problem.

The browser output also carried the site's standard warning that OPEN is the
owner's current belief and that an independent literature search is required.
That search is recorded in `LITERATURE.md`.
