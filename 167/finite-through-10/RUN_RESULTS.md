# Recorded run results

## Complete constructive checker

Compiler command:

```sh
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic verify_167.cpp -o verify_167
```

For each order, input was `/bin/nauty-geng -cq N`.

| n | graphs | triangle-free | certified | total triangles | equality pairs | max cover nodes | seeded FNV-style-64 |
|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1 | 1 | 0 | 0 | 0 | 0 | `9b428d00c6017909` |
| 2 | 1 | 1 | 0 | 0 | 0 | 0 | `cc139250709993e3` |
| 3 | 2 | 1 | 1 | 1 | 0 | 1 | `3bcf2663e2ca6e9d` |
| 4 | 6 | 3 | 3 | 7 | 1 | 1 | `81e4df91e80afafd` |
| 5 | 21 | 6 | 15 | 48 | 2 | 1 | `7bb99b2c36e01bea` |
| 6 | 112 | 19 | 93 | 401 | 5 | 1 | `8f4594637f40648c` |
| 7 | 853 | 59 | 794 | 4,589 | 19 | 1 | `4a0b9705dbe3814d` |
| 8 | 11,117 | 267 | 10,850 | 86,317 | 99 | 1 | `e2e93eabc219c0c3` |
| 9 | 261,080 | 1,380 | 259,700 | 2,878,659 | 583 | 1 | `44e6512280961203` |
| 10 | 11,716,571 | 9,832 | 11,706,739 | 179,706,010 | 4,807 | 1 | `38c1f219f45f740c` |

Every invocation printed `PASS` and exited zero.

The stream-checksum column uses the checker's FNV-1a update rule with custom
initial seed `1469598103934665603`; it is intentionally labeled FNV-style,
rather than standard FNV-1a-64.

## Independent exact audit through order nine

Commands: `python3 independent_audit.py --max-n 8`, followed by the captured
order-nine run `python3 independent_audit.py --min-n 9 --max-n 9`.

```text
n=1 graphs=1 triangle_graphs=0 exact_tau_eq_2nu=0 sha256=ecf5de1a2ecc66a1876a832804c64f6b5125784e94c82285d9720621c613ab46
n=2 graphs=1 triangle_graphs=0 exact_tau_eq_2nu=0 sha256=fae4bfc454bd04363dcd5222772f2973b1193e1ff6f676e822a427323a677ef9
n=3 graphs=2 triangle_graphs=1 exact_tau_eq_2nu=0 sha256=5966edf890849db6cb03626431916231a81a30c9db9a4781a4a8f2e5dc7e6129
n=4 graphs=6 triangle_graphs=3 exact_tau_eq_2nu=1 sha256=d7da485669f2dc74b81c02f18774a07430937684896833d59f138b10debb5005
n=5 graphs=21 triangle_graphs=15 exact_tau_eq_2nu=2 sha256=8169b01acd1570bf0d464cb7b4cf17ebb263035dc664de84ce41b8dd9618e301
n=6 graphs=112 triangle_graphs=93 exact_tau_eq_2nu=5 sha256=9fd4d2161400fc5f302fe1adc8c2b1230c312a15b15d0e2a343a02d75dd5cbfa
n=7 graphs=853 triangle_graphs=794 exact_tau_eq_2nu=19 sha256=eca7b9f61b5f54fe98f23f8b4e2baf77be08cd392911e0655fc8b7a72640fae1
n=8 graphs=11117 triangle_graphs=10850 exact_tau_eq_2nu=99 sha256=37010dfb9ca35c86bcbfd488c3e4cadcb3e918dc8c6acebd81ea966e79c35a84
PASS exact independent census through n=8; total_connected=12113
n=9 graphs=261080 triangle_graphs=259700 exact_tau_eq_2nu=583 sha256=fe73f2b8aad1a653b6f3bee799efff369cc486688df5aeade62ce0b3b5889eb5
PASS exact independent census through n=9; total_connected=261080
```

Orders one through eight: wall time 4.16 s, peak RSS 47,252 KiB. Order nine:
wall time 4:10.74, peak RSS 381,536 KiB.

## Independent exact order-ten sample

Command: `python3 audit_order10_sample.py`

```text
PASS order10 residue=0/10007 graphs=2183 triangle_graphs=1764 exact_tau_eq_2nu=7 sha256=40cbafe5472c30956f15dffd03f8037bb0156065540d0b604f369573a33836d2
```

Wall time: 0.56 s. Peak RSS: 33,668 KiB.

## Sanitizer audit

The checker was compiled with
`-fsanitize=address,undefined -fno-omit-frame-pointer` and run on the complete
order-eight census. It printed the same order-eight row above, exited zero, and
reported no sanitizer finding.
