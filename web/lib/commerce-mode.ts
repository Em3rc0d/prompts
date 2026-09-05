export type CommerceMode = "off" | "test" | "live";

export function parseCommerceMode(value: string | undefined): CommerceMode {
  if (value === "test" || value === "live") return value;
  return "off";
}

export function currentCommerceMode(envKey = "DEVELOPER_PACK_COMMERCE_MODE"): CommerceMode {
  return parseCommerceMode(process.env[envKey]);
}

export function currentStarterCommerceMode(): CommerceMode {
  return currentCommerceMode("STARTER_COLLECTION_COMMERCE_MODE");
}
