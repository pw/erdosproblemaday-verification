// Smoke harness for erdosproblemaday.com (pattern from the repo CLAUDE.md): import the Worker, fetch routes with a stub DB.
import worker from "/home/exedev/ErdosProblemADay-1022-0300/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "952-openai-gaussian-moat-refereed";
const checks = [
  ["/", 200, "Erd"],
  [`/day/${slug}`, 200, "Erdos952.erdos_952"], [`/day/${slug}`, 200, "largest admissible"], [`/day/${slug}`, 200, "416 sets"], [`/day/${slug}`, 200, "disagree on none"], [`/day/${slug}`, 200, "!PENDING"], [`/day/${slug}`, 200, "580 points"], [`/day/${slug}`, 200, "propext"],
  [`/day/${slug}`, 200, "!SEATS_SUMMARY"], [`/day/${slug}`, 200, "!LEANCHECKER_SENTENCE"], [`/day/${slug}`, 200, "!READING_PARAGRAPH"],
  [`/day/${slug}`, 200, "!WORLD_PARAGRAPH"], [`/day/${slug}`, 200, "!EXTRA_LINKS"],
  ["/", 200, slug],
  ["/problem/952", 200, "952-openai-gaussian-moat"],
  ["/report/952", 200, "Correction (22 Oct 2026)"],
  ["/board", 200, "open"],
  ["/day/174-openai-euclidean-ramsey-classification-refereed", 200, "Bridge174"],
  ["/submissions", 200, ""],
  ["/", 200, "!@@"], [`/day/${slug}`, 200, "!@@"], ["/problem/952", 200, "!@@"],
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
