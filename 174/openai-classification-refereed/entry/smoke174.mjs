// Smoke harness for erdosproblemaday.com (pattern from the repo CLAUDE.md): import the Worker, fetch routes with a stub DB.
import worker from "/home/exedev/ErdosProblemADay-1021-2100/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "174-openai-euclidean-ramsey-classification-refereed";
const checks = [
  ["/", 200, "Erd"],
  [`/day/${slug}`, 200, "Bridge174FC.lean"], [`/day/${slug}`, 200, "304 orbits"], [`/day/${slug}`, 200, "square {(±1,0),(0,±1)}"],
  [`/day/${slug}`, 200, "six-concyclic-lean"],
  [`/day/${slug}`, 200, "!PENDING_"], [`/day/${slug}`, 200, "!LEANCHECKER_"], [`/day/${slug}`, 200, "!RANDOM_SENTENCE"],
  ["/", 200, slug],
  ["/problem/174", 200, "174-openai-euclidean-ramsey"],
  ["/report/174", 404, ""],  // no July report for #174 (404 before this change too)
  ["/day/174-ramsey-pyramid-closure", 200, "Update, 21 October 2026"],
  ["/board", 200, "open"],
  ["/day/304-openai-short-egyptian-fractions-refereed", 200, "245,765"],
  ["/submissions", 200, ""],
  ["/", 200, "!@@"], [`/day/${slug}`, 200, "!@@"], ["/problem/174", 200, "!@@"],
  ["/day/no-such-slug-xyz", 404, ""],
];
let bad = 0;
for (const [path, want, needle] of checks) {
  try {
    const res = await worker.fetch(new Request("https://erdosproblemaday.com" + path), env, ctx);
    const body = await res.text();
    const neg = needle.startsWith("!"); const nd = neg ? needle.slice(1) : needle;
    const ok = res.status === want && (nd === "" || (neg ? !body.includes(nd) : body.includes(nd)));
    console.log(`${ok ? "ok " : "BAD"} ${res.status} ${path} ${body.length}B${needle ? ` needle(${needle.slice(0,24)})=${body.includes(nd)}` : ""}`);
    if (!ok) bad++;
  } catch (e) { console.log(`BAD throw ${path}: ${e.message}`); bad++; }
}
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS");
process.exit(bad ? 1 : 0);
