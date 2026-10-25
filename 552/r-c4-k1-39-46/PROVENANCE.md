# Provenance

## Upstream candidate

- Repository: `https://github.com/zach7036/c4-star-ramsey`
- Commit: `86a1c5055eea5e3891b2eeaea6c7ee1b3977bd33`
- Tree: `347a884913671c9f9a060de868de8fdd63d4f6a1`
- Commit archive: `provenance/upstream_commit_86a1c505.tar`
- Git history bundle: `provenance/upstream_history_86a1c505.bundle`
- Clean extracted tree: `upstream_ro/`

`github_repo_20260811.json`, `github_commit_86a1c505_20260811.json`, and
`github_ls_remote_20260811.txt` freeze the public API/remote state. The remote `HEAD` matched the
audited commit at capture time.

## Established literature controls

`sources/ejcram18.pdf` is Radziszowski, *Small Ramsey Numbers*, DS1.18, whose Table IVa records
the prior interval `46..47`. `sources/zhang_broersma_chen_2014.pdf` supplies the correctly indexed
star-wheel equality. The extracted text layers are controls; the PDFs are the primary snapshots.

## Live state

`provenance/live_552_bright_20260811.txt` and `live_85_bright_20260811.txt` are contemporaneous
Bright Data captures made independently earlier on the same UTC date. They show `OPEN`, zero
claimed proofs, and no current worker. Standard web fetch returned HTTP 403 during this audit;
additional Bright attempts connected but did not complete navigation, so the successful frozen
same-date captures are retained with this limitation disclosed.

The GitHub repository itself is a current external proof claim even though it is not incorporated
into the live Erdos page.

## Other current claimant

`suitedaces_repo_metadata_20260811.json`, `suitedaces_repo_README_20260811.md`, and
`suitedaces_ls_remote_20260811.txt` record a second public, explicitly unreviewed claim of
`R(C4,K1,39)=46`, with observed `HEAD/main`
`d20470914e9f496e4b4fd47c4bcc38f6f832da6b`. These same-date snapshots were first captured in the
separate literature-table audit and copied here; `git ls-remote` was rerun for this bundle. The
second proof and its excluded large artifacts were not audited. These files are current-state and
priority controls only, not evidence for the PASS verdict.
