// Smoke harness for erdosproblemaday.com: import the Worker, fetch routes with a stub DB.
import worker from "/home/exedev/ErdosProblemADay-1022-1500/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "507-openai-heilbronn-power-lower-bound-refereed";
const final = process.argv.includes("--final");
const notBloom = "not among the 25 on Bloom";
const checks = [
  ["/", 200, "Erd"],
  [`/day/${slug}`, 200, "every_large_n"], [`/day/${slug}`, 200, "Green77.green_77"], [`/day/${slug}`, 200, "erdos_507.lower"],
  [`/day/${slug}`, 200, "BigOSpeedrun.HeilbronnTriangle.Bound"], [`/day/${slug}`, 200, "3.18·10<sup>−236</sup>"],
  [`/day/${slug}`, 200, "propext"], [`/day/${slug}`, 200, "mathvet"],
  [`/day/${slug}`, 200, "!READING_PARAGRAPH"], [`/day/${slug}`, 200, "!WORLD_PARAGRAPH"], [`/day/${slug}`, 200, "!WORLD_REPLAYS_PARAGRAPH"],
  [`/day/${slug}`, 200, final ? "!LEANCHECKER_SENTENCE" : "LEANCHECKER_SENTENCE"],
  [`/day/${slug}`, 200, "!<p></p>"],
  ["/", 200, slug],
  ["/problem/507", 200, "507-openai-heilbronn"],
  ["/report/507", 200, notBloom], ["/report/507", 200, "every large n"], ["/report/507", 200, "!Bloom calls these claims"],
  ["/report/978", 200, notBloom], ["/problem/505", 200, notBloom], ["/problem/142", 200, notBloom], ["/problem/507", 200, notBloom],
  ["/report/971", 200, "!" + notBloom],
  ["/report/968", 200, "Bloom calls these claims"], ["/report/968", 200, "!" + notBloom],
  ["/board", 200, "open"],
  ["/day/978-openai-squarefree-quartics-refereed", 200, "Erdos978.erdos_978.parts.ii"],
  ["/submissions", 200, ""],
  ["/", 200, "!@@"], [`/day/${slug}`, 200, "!@@"], ["/problem/507", 200, "!@@"],
  ["/day/no-such-slug-xyz", 404, ""],
];
let bad = 0;
for (const [path, want, needle] of checks) {
  try {
    const res = await worker.fetch(new Request("https://erdosproblemaday.com" + path), env, ctx);
    const body = await res.text();
    const neg = needle.startsWith("!"); const nd = neg ? needle.slice(1) : needle;
    const ok = res.status === want && (nd === "" || (neg ? !body.includes(nd) : body.includes(nd)));
    console.log(`${ok ? "ok " : "BAD"} ${res.status} ${path} ${body.length}B${needle ? ` needle(${needle.slice(0,28)})=${body.includes(nd)}` : ""}`);
    if (!ok) bad++;
  } catch (e) { console.log(`BAD throw ${path}: ${e.message}`); bad++; }
}
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS");
process.exit(bad ? 1 : 0);
