import worker from "/home/exedev/ErdosProblemADay-1021-1500/src/index.js";
import { writeFileSync } from "fs";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "51-a-no-answer-needs-smooth-shifted-primes";
const checks = [
  ["/", 200, "Erd"], ["/", 200, slug], ["/", 200, "!@@"],
  [`/day/${slug}`, 200, "17,776,474,638,307,328"], [`/day/${slug}`, 200, "Carmichael"], [`/day/${slug}`, 200, "15/8 + 3·2⁻⁵⁸"],
  [`/day/${slug}`, 200, "139,847,905"], [`/day/${slug}`, 200, "!_LINE"], [`/day/${slug}`, 200, "!@@"], [`/day/${slug}`, 200, "!undefined"],
  ["/problem/51", 200, slug], ["/progress", 200, ""], ["/board", 200, "open"],
  ["/day/416-openai-totient-count-asymptotic-refereed", 200, "139,847,905"], ["/day/341-the-last-seed-in-12-through-1e8", 200, ""],
  ["/submissions", 200, ""], ["/day/no-such-slug-xyz", 404, ""],
];
let bad = 0;
for (const [path, want, needle] of checks) {
  try {
    const res = await worker.fetch(new Request("https://erdosproblemaday.com" + path), env, ctx);
    const body = await res.text();
    if (path === `/day/${slug}`) writeFileSync("/home/exedev/MathDyad/erdos51/entry/rendered.html", body);
    const neg = needle.startsWith("!"); const nd = neg ? needle.slice(1) : needle;
    const ok = res.status === want && (nd === "" || (neg ? !body.includes(nd) : body.includes(nd)));
    console.log(`${ok ? "ok " : "BAD"} ${res.status} ${path} ${body.length}B needle=${needle}`);
    if (!ok) bad++;
  } catch (e) { console.log(`BAD throw ${path}: ${e.message}`); bad++; }
}
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS");
process.exit(bad ? 1 : 0);
