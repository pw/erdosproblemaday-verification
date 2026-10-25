// Smoke harness for erdosproblemaday.com (pattern from the repo CLAUDE.md): import the Worker, fetch routes with a stub DB.
import worker from "/home/exedev/ErdosProblemADay-1022-0600/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "371-openai-joint-dickman-law-refereed";
const checks = [
  ["/", 200, "Erd"],
  [`/day/${slug}`, 200, "Erdos371.erdos_371"], [`/day/${slug}`, 200, "4,999,983,166"], [`/day/${slug}`, 200, "jbaelaw"], [`/day/${slug}`, 200, "propext"],
  [`/day/${slug}`, 200, "0.9627"], [`/day/${slug}`, 200, "0.3610"], [`/day/${slug}`, 200, "Icc 2 ⌊X⌋ vs Iio b"],
  [`/day/${slug}`, 200, "!REPLAY_"], [`/day/${slug}`, 200, "!LEAN_ROUTE"], [`/day/${slug}`, 200, "!LEAN_SEAT"], [`/day/${slug}`, 200, "!BRIDGE_AXIOMS"],
  [`/day/${slug}`, 200, "!PLACEHOLDER"], [`/day/${slug}`, 200, "!_TABLE"], [`/day/${slug}`, 200, "!LEANCHECKER_SENTENCE"],
  ["/", 200, slug],
  ["/problem/371", 200, "371-openai-joint-dickman"],
  ["/report/371", 200, "Update (22 Oct 2026)"],
  ["/report/928", 200, "Update (22 Oct 2026)"],
  ["/board", 200, "open"],
  ["/day/952-openai-gaussian-moat-refereed", 200, "Erdos952.erdos_952"],
  ["/submissions", 200, ""],
  ["/", 200, "!@@"], [`/day/${slug}`, 200, "!@@"], ["/problem/371", 200, "!@@"],
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
