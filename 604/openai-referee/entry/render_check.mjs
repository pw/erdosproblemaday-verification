import worker from "/home/exedev/ErdosProblemADay-1014-1500/src/index.js";
import fs from "node:fs";
const stmt={bind(){return stmt},all:async()=>({results:[]}),first:async()=>null,run:async()=>({success:true})};
const env={DB:{prepare:()=>stmt},RESEND_API_KEY:""}, ctx={waitUntil(){},passThroughOnException(){}};
for (const path of ["/day/604-openai-weak-pinned-distances-refereed","/problem/604","/"]) {
  const html=await (await worker.fetch(new Request("https://erdosproblemaday.com"+path),env,ctx)).text();
  const txt=html.replace(/<script[\s\S]*?<\/script>/g,"").replace(/<[^>]+>/g," ").replace(/\s+/g," ");
  if (path.startsWith("/day")) fs.writeFileSync("/tmp/oaimath/604/entry/rendered_604.txt",txt);
  console.log(path, "| written-before-release clause:", txt.includes("written before that release"), "| alone.Fourth:", txt.includes("alone.Fourth"), "| Four findings:", txt.includes("Four findings"), "| eight hostile:", txt.includes("eight hostile seats"), "| 604 card:", txt.includes("#604'S FIRST QUESTION"));
}
