// Smoke harness for erdosproblemaday.com (pattern from the repo CLAUDE.md): import the Worker, fetch routes with a stub DB.
import worker from "/home/exedev/ErdosProblemADay-main/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = process.argv[2] || "505-openai-borsuk-fails-in-dimension-nine-refereed";
const checks = [
  ["/", 200, "Erd"],
  [`/day/${slug}`, 200, "Bridge505.lean"], ["/", 200, "conjecture fails in dimension nine: the projectors"], ["/day/986-openai-sharp-log-exponent-off-diagonal-ramsey-refereed", 200, "actual_prime_construction"],
  ["/problem/505", 200, "505-openai-borsuk"], ["/problem/986", 200, "986-openai-sharp-log"], ["/day/184-erdos-gallai-three-proofs-two-lean-replays-and-a-bridge", 200, "Coffey"],
  ["/board", 200, "open"],
  ["/submissions", 200, ""],
  ["/day/no-such-slug-xyz", 404, ""],
];
let bad = 0;
for (const [path, want, needle] of checks) {
  try {
    const res = await worker.fetch(new Request("https://erdosproblemaday.com" + path), env, ctx);
    const body = await res.text();
    const ok = res.status === want && (needle === "" || body.includes(needle));
    console.log(`${ok ? "ok " : "BAD"} ${res.status} ${path} ${body.length}B${needle ? ` needle=${body.includes(needle)}` : ""}`);
    if (!ok) bad++;
  } catch (e) { console.log(`BAD throw ${path}: ${e.message}`); bad++; }
}
// negative control: a route that must 404 is in the list; a thrown import error fails loud via the catch above.
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS");
process.exit(bad ? 1 : 0);
