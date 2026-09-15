import fs from "node:fs";
import path from "node:path";
const candidates=[".next/server/app-paths-manifest.json",".next/app-path-routes-manifest.json",".next/routes-manifest.json"];
let corpus="";const observed=[];
for(const file of candidates){const full=path.resolve(file);if(!fs.existsSync(full))continue;const text=fs.readFileSync(full,"utf8");corpus+=`\n${text}`;observed.push(file);}
if(!observed.length){console.error("GOLDEN PATH BUILD PARITY: FAIL — no Next route manifest found");process.exit(1);}
const required=["/","/free/developer-starter-pack","/developer-pack","/license","/api/free-pack/v1","/api/free-pack/v1.1.0","/api/commerce/developer-pack/checkout","/api/commerce/lemonsqueezy/webhook"];
const missing=required.filter(route=>!corpus.includes(route));
if(missing.length){console.error("GOLDEN PATH BUILD PARITY: FAIL",JSON.stringify({observed_manifests:observed,missing}));process.exit(1);}
console.log("GOLDEN PATH BUILD PARITY: PASS",JSON.stringify({observed_manifests:observed,required_routes:required}));
