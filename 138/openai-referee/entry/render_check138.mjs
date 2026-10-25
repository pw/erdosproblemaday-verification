import worker from "/home/exedev/ErdosProblemADay-1015-0600/src/index.js";
import fs from "node:fs";
const stmt={bind(){return stmt},all:async()=>({results:[]}),first:async()=>null,run:async()=>({success:true})};
const env={DB:{prepare:()=>stmt},RESEND_API_KEY:""}, ctx={waitUntil(){},passThroughOnException(){}};
for (const path of ["/day/138-openai-superexponential-van-der-waerden-refereed","/problem/138","/"]) {
  const res=await worker.fetch(new Request("https://erdosproblemaday.com"+path),env,ctx); const html=await res.text();
  const txt=html.replace(/<script[\s\S]*?<\/script>/g,"").replace(/<[^>]+>/g," ").replace(/\s+/g," ");
  if (path.startsWith("/day")) { fs.writeFileSync("/tmp/oaimath/160/entry/rendered_138.html",html); fs.writeFileSync("/tmp/oaimath/160/entry/rendered_138.txt",txt); }
  console.log(path, res.status, html.length, "| written-before-release clause:", txt.includes("written before that release"), "| seven hostile:", txt.includes("even hostile seats"), "| card:", txt.includes("$500 QUESTION"), "| placeholders:", /\[\[|\{\{/.test(txt));
}
