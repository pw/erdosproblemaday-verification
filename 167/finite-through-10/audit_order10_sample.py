#!/usr/bin/env python3
"""Independent exact order-10 spot audit using a canonical nauty residue."""

import hashlib
import subprocess

import networkx as nx

from independent_audit import exact_values


def main():
    # nauty's res/mod mechanism chooses a deterministic slice without first
    # materialising the other 11.7 million connected order-10 graphs.
    cmd = ["/bin/nauty-geng", "-cq", "10", "0/10007"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    assert proc.stdout is not None
    count = nontrivial = equality = 0
    digest = hashlib.sha256()
    for raw in proc.stdout:
        raw = raw.strip()
        if not raw:
            continue
        digest.update(raw + b"\n")
        graph = nx.from_graph6_bytes(raw)
        assert len(graph) == 10 and nx.is_connected(graph)
        nu, tau = exact_values(graph)
        assert tau <= 2 * nu, (raw.decode(), nu, tau)
        count += 1
        nontrivial += bool(nu)
        equality += bool(nu and tau == 2 * nu)
    assert proc.wait() == 0
    print(
        f"PASS order10 residue=0/10007 graphs={count} "
        f"triangle_graphs={nontrivial} exact_tau_eq_2nu={equality} "
        f"sha256={digest.hexdigest()}"
    )


if __name__ == "__main__":
    main()
