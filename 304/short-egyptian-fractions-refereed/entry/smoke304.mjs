// Smoke harness for erdosproblemaday.com (pattern from the repo CLAUDE.md): import the Worker, fetch routes with a stub DB.
import worker from "/home/exedev/ErdosProblemADay-main/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "304-openai-short-egyptian-fractions-refereed";
const checks = [
  ["/", 200, "Erd"],
  [`/day/${slug}`, 200, "Bridge304.lean"], [`/day/${slug}`, 200, "245,765"], [`/day/${slug}`, 200, "CompositeSupplyFinal.lean"],
  ["/", 200, slug],
  ["/problem/304", 200, "304-openai-short-egyptian"], ["/problem/148", 200, "304-openai-short-egyptian"], ["/problem/293", 200, "304-openai-short-egyptian"],
  ["/report/304", 200, ""], ["/report/148", 200, ""], ["/report/293", 200, ""],
  ["/board", 200, "open"],
  ["/day/968-openai-large-prime-gaps-positive-proportion-refereed", 200, "22,801,763,489"], ["/day/51-a-no-answer-needs-smooth-shifted-primes", 200, ""],
  ["/problem/968", 200, "968-openai-large-prime-gaps"], ["/problem/416", 200, "416-openai-totient"],
  ["/submissions", 200, ""],
  ["/", 200, "!@@"], [`/day/${slug}`, 200, "!@@"], ["/problem/304", 200, "!@@"],
  ["/day/no-such-slug-xyz", 404, ""],
];
let bad = 0;
for (const [path, want, needle] of checks) {
  try {
    const res = await worker.fetch(new Request("https://erdosproblemaday.com" + path), env, ctx);
    const body = await res.text();
    const neg = needle.startsWith("!"); const nd = neg ? needle.slice(1) : needle;
    const ok = res.status === want && (nd === "" || (neg ? !body.includes(nd) : body.includes(nd)));
    console.log(`${ok ? "ok " : "BAD"} ${res.status} ${path} ${body.length}B${needle ? ` needle=${body.includes(nd)}` : ""}`);
    if (!ok) bad++;
  } catch (e) { console.log(`BAD throw ${path}: ${e.message}`); bad++; }
}
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS");
process.exit(bad ? 1 : 0);
