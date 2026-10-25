# Reproduction environment

Author run: 2026-08-11 UTC on Linux x86_64.

```
g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
go version go1.22.2 linux/amd64
Python 3.12.3
Linux portalonce 6.12.93 #1 SMP Wed Jul 22 19:44:49 UTC 2026 x86_64
```

Gate repositories:

```
ErdosProblemADay HEAD  b62cecd6841040478c5626c102145a8ba8bdaf96
FormalConjectures HEAD 9118d083ffca1536f521f9a7d103201f537ea670
erdosproblems metadata 6929b78952e18c11d5cb28fe9438081ee1d49448
```

The site worktree was dirty because another agent was concurrently editing
`src/ledger_data.js`. The final scanned file hashes were:

```
b7111451218492db6756cc88dde0a8b98700d4c6f47e476171a02950b6d9af8b  src/index.js
9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052  src/ledger_data.js
```

The bundle does not modify or vendor either site source file.
