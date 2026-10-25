// Smoke harness for erdosproblemaday.com (pattern from the repo CLAUDE.md): import the Worker, fetch routes with a stub DB.
import worker from "/home/exedev/ErdosProblemADay-1022-1200/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "978-openai-squarefree-quartics-refereed";
const final = process.argv.includes("--final");
const checks = [
  ["/", 200, "Erd"],
  [`/day/${slug}`, 200, "Erdos978.erdos_978.parts.ii"], [`/day/${slug}`, 200, "756,674"], [`/day/${slug}`, 200, "179<sup>2</sup>"], [`/day/${slug}`, 200, "withdrew it on 15 October"],
  [`/day/${slug}`, 200, "propext"], [`/day/${slug}`, 200, "!READING_PARAGRAPH"], [`/day/${slug}`, 200, "!NUMBERS_PARAGRAPH"], [`/day/${slug}`, 200, "!SEAT_VERDICTS"], [`/day/${slug}`, 200, "!READING_M2"],
  [`/day/${slug}`, 200, final ? "!LEANCHECKER_SENTENCE" : "LEANCHECKER_SENTENCE"],
  ["/", 200, slug],
  ["/problem/978", 200, "978-openai-squarefree-quartics"],
  ["/report/978", 200, "75"],
  ["/board", 200, "open"],
  ["/day/952-openai-gaussian-moat-refereed", 200, "Erdos952.erdos_952"],
  ["/day/371-openai-joint-dickman-law-refereed", 200, "joint"],
  ["/submissions", 200, ""],
  ["/", 200, "!@@"], [`/day/${slug}`, 200, "!@@"], ["/problem/978", 200, "!@@"],
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
