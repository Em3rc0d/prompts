import { createHmac, timingSafeEqual } from "node:crypto";
export const runtime="nodejs";
function loadConfig(){const webhookSecret=process.env.LEMONSQUEEZY_WEBHOOK_SECRET;const storeId=process.env.LEMONSQUEEZY_STORE_ID;const productId=process.env.LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID;const variantId=process.env.LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID;if(!webhookSecret||!storeId||!productId||!variantId)return null;return{webhookSecret,storeId,productId,variantId,allowTestMode:process.env.LEMONSQUEEZY_ALLOW_TEST_MODE==="true"};}
function signatureValid(rawBody,signature,secret){if(!signature||!secret)return false;const expected=createHmac("sha256",secret).update(rawBody).digest("hex");const a=Buffer.from(expected,"utf8");const b=Buffer.from(signature,"utf8");return a.length===b.length&&timingSafeEqual(a,b);}
function cleanAttribution(customData){if(!customData||typeof customData!=="object")return undefined;const out={};for(const key of ["source","medium","campaign","content"]){const raw=customData[key];if(typeof raw!=="string")continue;const value=raw.trim().slice(0,120).replace(/[^a-zA-Z0-9._:/-]/g,"-");if(value)out[key]=value;}return Object.keys(out).length?out:undefined;}
export async function POST(request){
  const config=loadConfig();if(!config)return Response.json({ok:false,error:"commerce_not_configured"},{status:503});
  const rawBody=await request.text();const signature=request.headers.get("x-signature")||"";const eventName=request.headers.get("x-event-name")||"";
  if(!signatureValid(rawBody,signature,config.webhookSecret))return Response.json({ok:false,error:"invalid_signature"},{status:401});
  let payload;try{payload=JSON.parse(rawBody);}catch{return Response.json({ok:false,error:"invalid_json"},{status:400});}
  if(eventName!=="order_created"||payload?.meta?.event_name!=="order_created")return Response.json({ok:true,ignored:true,reason:"unsupported_event"});
  const data=payload?.data;const attributes=data?.attributes;const item=attributes?.first_order_item;
  if(data?.type!=="orders"||!data?.id||!attributes)return Response.json({ok:false,error:"missing_order_shape"},{status:400});
  if(!item?.product_id||!item?.variant_id||!attributes?.store_id)return Response.json({ok:false,error:"missing_product_identity"},{status:400});
  if(attributes.status!=="paid")return Response.json({ok:true,ignored:true,reason:"order_not_paid"});
  if(String(attributes.store_id)!==config.storeId)return Response.json({ok:true,ignored:true,reason:"store_mismatch"});
  if(String(item.product_id)!==config.productId)return Response.json({ok:true,ignored:true,reason:"product_mismatch"});
  if(String(item.variant_id)!==config.variantId)return Response.json({ok:true,ignored:true,reason:"variant_mismatch"});
  const testMode=attributes.test_mode===true||item.test_mode===true;if(testMode&&!config.allowTestMode)return Response.json({ok:true,ignored:true,reason:"test_mode_not_allowed"});
  const evidence={event:"purchase_completed",source:"lemonsqueezy_webhook",evidence:"provider_signed_order_created",provider_order_id:data.id,provider_identifier:attributes.identifier,order_number:attributes.order_number,store_id:attributes.store_id,product_id:item.product_id,variant_id:item.variant_id,currency:attributes.currency,total:attributes.total,total_usd:attributes.total_usd,test_mode:testMode,created_at:attributes.created_at,attribution:cleanAttribution(payload?.meta?.custom_data)};
  console.info("PQ_COMMERCE_EVENT",JSON.stringify(evidence));
  return Response.json({ok:true,accepted:true,event:"purchase_completed",provider_order_id:data.id});
}
