// Smoke harness for erdosproblemaday.com (pattern from the repo CLAUDE.md): import the Worker, fetch routes with a stub DB.
import worker from "/home/exedev/ErdosProblemADay-main/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "968-openai-large-prime-gaps-positive-proportion-refereed";
const checks = [
  ["/", 200, "Erd"],
  [`/day/${slug}`, 200, "Bridge968.lean"], [`/day/${slug}`, 200, "22,801,763,489"], [`/day/${slug}`, 200, "bombieriVinogradov"],
  ["/", 200, "968-openai-large-prime-gaps-positive-proportion-refereed"],
  ["/problem/968", 200, "968-openai-large-prime-gaps"], ["/board", 200, "open"],
  ["/day/802-openai-aeks-independence-refereed", 200, "374.7"], ["/day/551-openai-cycle-clique-ramsey-refereed", 200, "3,099 of 3,099 pass"],
  ["/problem/802", 200, "802-openai-aeks"], ["/problem/505", 200, "505-openai-borsuk"],
  ["/submissions", 200, ""],
  ["/", 200, "!@@"], [`/day/${slug}`, 200, "!@@"], ["/problem/968", 200, "!@@"],
  ["/day/no-such-slug-xyz", 404, ""],
];
let bad = 0;
for (const [path, want, needle] of checks) {
  try {
    const res = await worker.fetch(new Request("https://erdosproblemaday.com" + path), env, ctx);
    const body = await res.text();
    const neg = needle.startsWith("!"); const nd = neg ? needle.slice(1) : needle;
    const ok = res.status === want && (nd === "" || (neg ? !body.includes(nd) : body.includes(nd)));
    console.log(`${ok ? "ok " : "BAD"} ${res.status} ${path} ${body.length}B${needle ? ` needle=${body.includes(needle)}` : ""}`);
    if (!ok) bad++;
  } catch (e) { console.log(`BAD throw ${path}: ${e.message}`); bad++; }
}
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS");
process.exit(bad ? 1 : 0);
