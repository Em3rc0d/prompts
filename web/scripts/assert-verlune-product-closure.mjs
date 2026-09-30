import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const files = {
  premium: "app/premium/page.tsx",
  checkout: "app/checkout/page.tsx",
  checkoutComponent: "components/mercado-pago-checkout.tsx",
  payment: "app/api/commerce/verlune-premium/payment/route.ts",
  access: "lib/verlune-access.ts",
  accessKeyCore: "lib/verlune-access-key.ts",
  accessKeyTest: "scripts/test-verlune-access-key.mjs",
  unlockForm: "components/verlune-unlock-form.tsx",
  recovery: "app/api/verlune/access-key/recover/route.ts",
  provider: "lib/verlune-mercado-pago.ts",
  layout: "app/layout.tsx",
  home: "app/page.tsx",
  free: "app/free/page.tsx",
  unlock: "app/unlock/page.tsx",
  licensePage: "app/license/page.tsx",
  freeLicense: "../product/verlune-v1/free/LICENSE.md",
  env: ".env.example",
  catalog: "lib/verlune-premium-catalog.ts"
};

function read(rel) {
  const absolute = path.resolve(root, rel);
  if (!fs.existsSync(absolute)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: missing ${rel}`);
  return fs.readFileSync(absolute, "utf8");
}

const premium = read(files.premium);
const checkout = read(files.checkout);
const checkoutComponent = read(files.checkoutComponent);
const payment = read(files.payment);
const access = read(files.access);
const accessKeyCore = read(files.accessKeyCore);
const accessKeyTest = read(files.accessKeyTest);
const unlockForm = read(files.unlockForm);
const recovery = read(files.recovery);
const provider = read(files.provider);
const layout = read(files.layout);
const home = read(files.home);
const free = read(files.free);
const unlock = read(files.unlock);
const licensePage = read(files.licensePage);
const freeLicense = read(files.freeLicense);
const env = read(files.env);
const catalog = read(files.catalog);

for (const marker of ["VERLUNE PREMIUM","Already purchased? Unlock","Purchasing not open yet","getVerlunePremiumCommerceState",'/api/commerce/verlune-premium/checkout',"VERLUNE_PREMIUM_CANDIDATE_PRICE_USD"]) {
  if (!premium.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: Premium missing ${marker}`);
}
for (const marker of ["MercadoPagoCheckout","Cards + Yape","purchaseAvailable"]) {
  if (!checkout.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: checkout missing ${marker}`);
}
for (const marker of ["sdk.mercadopago.com/js/v2","minInstallments: 1","maxInstallments: 1"]) {
  if (!checkoutComponent.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: checkout component missing ${marker}`);
}
for (const marker of ["x-idempotency-key","premiumTestSessionMatches","newAccessKeyPremiumSession","provisionVerlunePremiumAccess","premium_already_owned","premium_purchase_in_progress","acquireVerlunePurchaseGuard","getVerlunePremiumEntitlementByEmail","VERLUNE_PREMIUM_PUBLIC_SALE_STATUS"]) {
  if (!payment.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: payment route missing ${marker}`);
}
for (const marker of ["https://api.mercadopago.com","/v1/payments","external_reference","collector_mismatch","environment_mismatch","amount_mismatch","product_mismatch","metadata_price_mismatch","payment_method_missing","VERLUNE_PREMIUM_PRICE_USD = 5","X-Idempotency-Key","installments_must_be_one","UUID_V4","MP_WEBHOOK_SECRET"]) {
  if (!provider.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: provider contract missing ${marker}`);
}

for (const marker of ["deriveVerluneEntitlementId","createVerluneAccessKey","verifyVerluneAccessKey","SYNC_ENTITLEMENT_SCRIPT","ACQUIRE_PURCHASE_GUARD_SCRIPT","RELEASE_PURCHASE_GUARD_SCRIPT","https://api.resend.com/emails","Idempotency-Key","VERLUNE_ENTITLEMENT_KV_REST_URL"]) {
  if (!access.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: canonical access layer missing ${marker}`);
}
for (const marker of ["VERLUNE_ACCESS_KEY_VERSION","deriveVerluneEntitlementIdWithSecret","createVerluneAccessKeyWithSecret","verifyVerluneAccessKeyWithSecret"]) {
  if (!accessKeyCore.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: Access Key core missing ${marker}`);
}
for (const marker of ["same_email_same_key=true","different_email_different_key=true","mutated key must fail verification"]) {
  if (!accessKeyTest.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: Access Key executable test missing ${marker}`);
}
for (const marker of ["Verlune Access Key","Email me my Access Key again","does not create a new one"]) {
  if (!unlockForm.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: unlock form missing ${marker}`);
}
for (const marker of ["createVerluneAccessKey","sendVerluneAccessEmail","allowVerluneRecoveryEmail","existing Access Key"]) {
  if (!recovery.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: recovery route missing ${marker}`);
}

if (!env.includes("VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=NOT_FOR_SALE")) throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: Premium sale must default fail-closed");
if (env.includes("VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=LIVE")) throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: example config must not enable public Premium sale");
for (const marker of ["VERLUNE_PREMIUM_PRICE_PEN_MINOR=1700","MP_ENVIRONMENT=test","MP_ALLOW_LIVE=false","MP_ACCESS_TOKEN=","MP_PUBLIC_KEY=","MP_COLLECTOR_ID=","MP_WEBHOOK_SECRET=","VERLUNE_ACCESS_KEY_SECRET_V1=","VERLUNE_ENTITLEMENT_KV_REST_URL=","VERLUNE_ENTITLEMENT_KV_REST_TOKEN=","VERLUNE_PURCHASE_GUARD_SECONDS=900","RESEND_API_KEY=","VERLUNE_ACCESS_FROM_EMAIL=","VERLUNE_SESSION_REVALIDATE_SECONDS=900"]) {
  if (!env.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: env missing ${marker}`);
}

if (!layout.includes('href="/premium">Premium</')) throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: primary navigation does not expose Premium discovery");
if (!layout.includes('href="/unlock">Unlock access')) throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: unlock is not separated as existing-purchase access");
if (layout.includes("app.lemonsqueezy.com/js/lemon.js")) throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: legacy Lemon script leaked into global layout");
for (const [surface, source] of [["home", home], ["free", free]]) if (!source.includes('href="/premium"')) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: ${surface} does not route Premium intent through /premium`);
if (!unlock.includes('href="/premium">← Explore Premium')) throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: unlock cannot return prospective buyers to Premium");

for (const marker of ["nineteen library assets","sixteen structured prompts","three structured workflows","No resale or redistribution"]) {
  if (!freeLicense.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: Free license missing ${marker}`);
}
if (!licensePage.includes("FREE_ASSETS.length") || !licensePage.includes("VERLUNE FREE LIBRARY")) throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: public license surface is not scoped to the full Free Library");

const promptIds = catalog.match(/id:\s*"VP-P-[^"]+"/g) ?? [];
const workflowIds = catalog.match(/id:\s*"VP-WF-[^"]+"/g) ?? [];
const builderIds = catalog.match(/id:\s*"VP-BUILDER-[^"]+"/g) ?? [];
const toolkitIds = catalog.match(/id:\s*"VP-TK-[^"]+"/g) ?? [];
if (promptIds.length !== 32 || workflowIds.length !== 5 || builderIds.length !== 2 || toolkitIds.length !== 2) {
  throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: Premium catalog expected 32/5/2/2, got ${promptIds.length}/${workflowIds.length}/${builderIds.length}/${toolkitIds.length}`);
}

console.log("VERLUNE PRODUCT CLOSURE P0 AUDIT: PASS");
console.log("premium_payment_provider=mercado_pago");
console.log("premium_launch_price_usd=5");
console.log("premium_local_price_pen=17.00");
console.log("premium_public_sale_default=NOT_FOR_SALE");
console.log("unlock=email+canonical_access_key+provider_readback");
console.log("access_key_uniqueness=product+normalized_email deterministic V1");
console.log("access_delivery=resend idempotent per-payment grant + same-key recovery");
console.log("duplicate_charge_guard=atomic email-scoped KV lock");
console.log("premium_launch_core=41_assets");
console.log("boundary=source/build contract only; real TEST/LIVE provider execution still required");
