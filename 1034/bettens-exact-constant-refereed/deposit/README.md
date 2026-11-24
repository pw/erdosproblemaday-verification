# Verifying the proof

Use Python 3.9 or newer. Only the Python standard library is required.

Keep `verify.py`, `certificate.json.gz`, and `verification_model.json` in the
same folder. Leave `certificate.json.gz` compressed. Open a terminal in that
folder and run:

```sh
python verify.py certificate.json.gz verification_model.json
```

The verifier checks all 82 matrix blocks, all required signs, the complete
order-7 graph basis, and all 1,044 identity coefficients using exact arithmetic.
A successful run ends with:

```text
CERTIFICATE VERIFIED
```

To run the matrix checks serially, use:

```sh
python verify.py certificate.json.gz verification_model.json --workers 1
```
