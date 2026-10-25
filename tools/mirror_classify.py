#!/usr/bin/env python3
"""Classify every file under verification/ as PUBLISH or WITHHOLD(reason) for the public mirror (github.com/pw/erdosproblemaday-verification).
Withheld = third-party copyrighted material (papers, arXiv/web captures, world-seat source dumps), staged-but-unsent correspondence,
and files carrying operator account details. Rules are path/extension based and deliberately err toward withholding.
Usage: mirror_classify.py <verification dir>  -> TSV "PUBLISH|reason<TAB>relpath" on stdout."""
import os, re, sys
ROOT = sys.argv[1]
THIRD_DIRS = {"sources","lit","literature","provenance","papers","raw","dl_misc","web","refs","references","pdfs"}
PAPER_EXT = {".pdf",".djvu",".ps",".epub"}
def classify(rel, full):
    parts = rel.split("/"); name = parts[-1]; low = name.lower(); ext = os.path.splitext(low)[1]
    if ext in PAPER_EXT: return "third-party paper (copyright)"
    if any(p.lower() in THIRD_DIRS for p in parts[:-1]): return "third-party source copy (copyright)"
    if ext == ".tex": return "third-party paper source (copyright)"
    CAPTURE = {"world","world_work","src","thirdparty","discussion","absmeta","live","mine","gh","prior","paper_tex","hindman_pdfs"}
    capdir = any(p.lower() in CAPTURE or p.lower().endswith("_src") or p.lower().endswith("_pdfs") or p.lower().endswith("_work") for p in parts[:-1])
    ours = re.match(r"(report|readme|notes?|summary|verdict|findings|world_report|seat_report)", low) or "report" in low
    if capdir and not ours and ext in {".txt",".html",".htm",".json",".xml",".md",".jsonl",".csv",".gz",".zip",".bib"}:
        return "web/source capture by a world or referee seat (third-party content)"
    if low.startswith("web_") or low.startswith("arxiv_") or low.startswith("arxiv-"): return "third-party web/arXiv capture (copyright)"
    if "/entry/" in "/"+rel and (re.search(r"note.*\.html$", low) or low.startswith("fc_issue_")): return "staged correspondence, not yet sent"
    try:
        head = open(full,"rb").read(1<<20)
    except Exception: return None
    if b"mhnin0@gmail.com" in head or b"p@pwhite.org" in head: return "operator account details"
    stem = os.path.splitext(full)[0]
    if ext in {".txt",".html",".htm",".md"} and any(os.path.exists(stem+e) for e in (".pdf",".PDF")): return "text dump of a third-party paper"
    if ext in {".txt",".html",".htm"} and len(head) > 20000:
        h = head[:6000].decode("utf8","replace")
        if re.search(r"arXiv:\s*\d{4}\.\d{4,5}|\bAbstract\b|\bABSTRACT\b|Journal of|Proceedings of|Mathematics Subject Classification", h):
            return "probable text dump of a third-party paper"
    if ext in {".html",".htm"}:
        h = head[:4000].decode("utf8","replace").lower()
        if "<!doctype html" in h or "<html" in h:
            if any(s in h for s in ("erdosproblems.com","mathoverflow","arxiv.org","github.com","wikipedia","<title>")) and "erdosproblemaday" not in h:
                return "third-party web page capture (copyright)"
    return None
out = []
for d, _, fs in os.walk(ROOT):
    for f in fs:
        full = os.path.join(d, f); rel = os.path.relpath(full, ROOT)
        out.append((rel, classify(rel, full)))
for rel, r in sorted(out): print(f"{r or 'PUBLISH'}\t{rel}")
