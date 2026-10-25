"""Scan a list of GitHub repos (read-only, via `gh api`) for Heilbronn/family-191 material
and for mentions of Blinov / Chen / their exponents.

Usage: python3 -I scan_repos.py repos.txt out_dir
repos.txt: one owner/name per line (first tab-separated field).
Writes out_dir/scan_results.json and saves every fetched text file under out_dir/files/.
"""
import json, os, re, subprocess, sys

PATH_RE = re.compile(r"heilbronn|(^|[^0-9])191([^0-9]|$)|triangle|blinov|littlebro|euler|canghaimeng", re.I)
TOKENS = ["Blinov", "littleBro", "heilbronn-triangle-bounds", "50893237", "50,893,237",
          "145278430", "145,278,430", "100866719", "100,866,719", "canghaimeng", "Qiuyu",
          "Euler", "Heilbronn", "reserved tag", "tagged_small_residue"]


def gh(args):
    r = subprocess.run(["gh", "api"] + args, capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout, r.stderr


def main():
    repos = [l.split("\t")[0].strip() for l in open(sys.argv[1]) if l.strip()]
    out = sys.argv[2]
    os.makedirs(os.path.join(out, "files"), exist_ok=True)
    results = {}
    for repo in repos:
        rc, so, se = gh([f"repos/{repo}/git/trees/HEAD?recursive=1"])
        entry = {"tree_ok": rc == 0, "err": se.strip()[:200] if rc else None, "path_hits": [], "token_hits": {}}
        paths = []
        if rc == 0:
            t = json.loads(so)
            entry["truncated"] = t.get("truncated")
            paths = [x["path"] for x in t.get("tree", []) if x["type"] == "blob"]
            entry["n_files"] = len(paths)
            entry["path_hits"] = [p for p in paths if PATH_RE.search(p)][:200]
        # text files to read: root README + path hits that look textual and small-ish
        to_read = [p for p in paths if p.lower() in ("readme.md", "readme.txt", "readme")]
        to_read += [p for p in entry["path_hits"] if re.search(r"\.(md|txt|tex|lean|json|yaml|yml|html|py)$", p, re.I)][:25]
        for p in to_read:
            rc2, body, _ = gh([f"repos/{repo}/contents/{p}", "-H", "Accept: application/vnd.github.raw"])
            if rc2 != 0:
                continue
            safe = (repo + "__" + p).replace("/", "__")[:200]
            with open(os.path.join(out, "files", safe), "w") as fh:
                fh.write(body)
            hits = {tok: body.count(tok) for tok in TOKENS if tok in body}
            if hits:
                entry["token_hits"][p] = hits
        results[repo] = entry
        print(repo, "tree_ok" if entry["tree_ok"] else "TREE_FAIL", len(entry["path_hits"]), entry["token_hits"] and list(entry["token_hits"].items())[:4], flush=True)
    json.dump(results, open(os.path.join(out, "scan_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
