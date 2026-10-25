import worker from "/home/exedev/ErdosProblemADay-main/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" }; const ctx = { waitUntil() {}, passThroughOnException() {} };
const get = async p => { const r = await worker.fetch(new Request("https://erdosproblemaday.com" + p), env, ctx); return [r.status, await r.text()]; };
const [s1, b1] = await get("/report/968"); console.log("report", s1, b1.length);
const [s2, b2] = await get("/day/968-openai-large-prime-gaps-positive-proportion-refereed");
for (const n of ["1,118 theorems and 175 lemmas", "/report/968", "kimihiro64", "untere Dichte", "397,737,673", "λ + λ²c<sub>G</sub>² + 1", "Claude Opus 5.5", "3,456 s", "Rosser–Schoenfeld", "at least half"]) console.log(b2.includes(n) ? "has " : "MISSING ", n);
const [s3, b3] = await get("/"); const i = b3.indexOf("ERDŐS AND PRACHAR"); console.log("home card:", i > 0 ? b3.slice(i - 40, i + 200).replace(/\s+/g, " ") : "card text not found verbatim");
