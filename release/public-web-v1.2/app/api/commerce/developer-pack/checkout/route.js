const ATTRIBUTION_FIELDS=["source","medium","campaign","content"];
function clean(value){if(!value)return undefined;const normalized=value.trim().slice(0,120);if(!normalized)return undefined;return normalized.replace(/[^a-zA-Z0-9._:/-]/g,"-");}
export async function GET(request){
  const checkoutUrl=process.env.NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL;
  if(!checkoutUrl)return Response.json({ok:false,error:"checkout_not_configured"},{status:503});
  let destination;
  try{destination=new URL(checkoutUrl);}catch{return Response.json({ok:false,error:"checkout_url_invalid"},{status:500});}
  if(destination.protocol!=="https:")return Response.json({ok:false,error:"checkout_url_must_use_https"},{status:500});
  const incoming=new URL(request.url);const attribution={};
  for(const field of ATTRIBUTION_FIELDS){const value=clean(incoming.searchParams.get(field));if(!value)continue;attribution[field]=value;destination.searchParams.set(`checkout[custom][${field}]`,value);}
  console.info("PQ_FUNNEL_EVENT",JSON.stringify({event:"checkout_started",product_id:"pq-developer-pack",product_version:"1.1.0",timestamp:new Date().toISOString(),...attribution}));
  return Response.redirect(destination,302);
}
