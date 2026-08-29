import { createHash } from "node:crypto";

export const runtime="nodejs";
const ORIGIN="https://prompt-quarry-mx9ioitln-faridmerinos-projects.vercel.app/api/free-pack/v1.1.0";
const EXPECTED_SIZE=23498;
const EXPECTED_SHA="55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32";
const FILENAME="prompt-quarry-developer-starter-v1.1.0.zip";

export async function GET(request){
  let upstream;
  try{upstream=await fetch(ORIGIN,{cache:"force-cache"});}
  catch(error){console.error("PQ_FREE_ORIGIN_ERROR",String(error));return Response.json({ok:false,error:"free_pack_origin_unreachable"},{status:502});}
  if(!upstream.ok)return Response.json({ok:false,error:"free_pack_origin_http_error",status:upstream.status},{status:502});
  const archive=Buffer.from(await upstream.arrayBuffer());
  const sha=createHash("sha256").update(archive).digest("hex");
  if(archive.length!==EXPECTED_SIZE||sha!==EXPECTED_SHA){
    console.error("PQ_FREE_INTEGRITY_FAILURE",JSON.stringify({size:archive.length,sha}));
    return Response.json({ok:false,error:"free_pack_integrity_failure",expected_size:EXPECTED_SIZE,observed_size:archive.length,expected_sha256:EXPECTED_SHA,observed_sha256:sha},{status:500});
  }
  const incoming=new URL(request.url);const attribution={};
  for(const key of ["source","medium","campaign","content"]){const raw=incoming.searchParams.get(key);if(!raw)continue;const value=raw.trim().slice(0,120).replace(/[^a-zA-Z0-9._:/-]/g,"-");if(value)attribution[key]=value;}
  console.info("PQ_FUNNEL_EVENT",JSON.stringify({event:"free_pack_acquired",product_id:"pq-developer-starter",product_version:"1.1.0",archive_sha256:sha,timestamp:new Date().toISOString(),...attribution}));
  return new Response(new Uint8Array(archive),{headers:{"Content-Type":"application/zip","Content-Disposition":`attachment; filename="${FILENAME}"`,"Content-Length":String(archive.length),"Cache-Control":"public, max-age=31536000, immutable",ETag:`"sha256-${sha}"`,"X-Prompt-Quarry-Version":"1.1.0","X-Prompt-Quarry-SHA256":sha}});
}
