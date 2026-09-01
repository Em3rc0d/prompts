export type CommerceMode = "off" | "test" | "live";

export function parseCommerceMode(value: string | undefined): CommerceMode {
  if (value === "test" || value === "live") return value;
  return "off";
}

export function currentCommerceMode(): CommerceMode {
  return parseCommerceMode(process.env.DEVELOPER_PACK_COMMERCE_MODE);
}
