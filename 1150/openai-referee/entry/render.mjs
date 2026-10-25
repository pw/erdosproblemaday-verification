import worker from "/home/exedev/ErdosProblemADay-0900/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" }; const ctx = { waitUntil() {}, passThroughOnException() {} };
for (const [path, needles] of [["/problem/1150", ["1150-openai-ultraflat-littlewood-refereed","CLOSED","Newer public claim","own1150".length?"kernel replay on 12 Oct 2026":""]], ["/progress", ["KERNEL REPLAY GREEN · NOT OURS","/day/1150-openai-ultraflat-littlewood-refereed"]], ["/day/1150-openai-ultraflat-littlewood-refereed", ["CLOSED","Our kernel replay","seven seats","it is updated when it lands","Labels"]], ["/", ["1150"]]]) {
  const res = await worker.fetch(new Request("https://erdosproblemaday.com" + path), env, ctx); const body = await res.text();
  console.log(res.status, path, body.length + "B", needles.filter(Boolean).map(n => `${n.slice(0,28)}=${body.includes(n)}`).join(" | "));
}
