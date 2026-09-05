import { NextResponse } from "next/server";

const CLIENT_INTENT_EVENTS = new Set([
  "landing_view",
  "collections_viewed",
  "free_product_viewed",
  "free_cta_clicked",
  "starter_product_viewed",
  "starter_cta_clicked",
  "paid_product_viewed",
  "paid_cta_clicked",
]);

const DIMENSIONS = [
  "product_id",
  "product_version",
  "collection_id",
  "surface",
  "source",
  "medium",
  "campaign",
  "content",
] as const;

type Dimension = (typeof DIMENSIONS)[number];
type IntentBody = { event?: unknown } & Partial<Record<Dimension, unknown>>;

function clean(value: unknown): string | undefined {
  if (typeof value !== "string") return undefined;
  const compact = value.trim().replace(/[\r\n\t]/g, " ").slice(0, 96);
  return compact || undefined;
}

export async function POST(request: Request) {
  if (!request.headers.get("content-type")?.toLowerCase().startsWith("application/json")) {
    return NextResponse.json({ error: "content_type_must_be_json" }, { status: 415 });
  }

  let body: IntentBody;
  try {
    body = (await request.json()) as IntentBody;
  } catch {
    return NextResponse.json({ error: "invalid_json" }, { status: 400 });
  }

  const event = clean(body.event);
  if (!event || !CLIENT_INTENT_EVENTS.has(event)) {
    return NextResponse.json({ error: "event_not_allowed" }, { status: 400 });
  }

  const dimensions: Partial<Record<Dimension, string>> = {};
  for (const key of DIMENSIONS) {
    const value = clean(body[key]);
    if (value) dimensions[key] = value;
  }

  // This log is deliberately not purchase evidence. It contains only an
  // allowlisted client-intent event and compact non-PII merchandising dimensions.
  // Do not add browser session IDs, email/name fields, request headers, or IP data.
  console.info("PM_INTENT_EVENT", {
    schema: "prompt-machine-intent-v1",
    evidence_class: "UNTRUSTED_CLIENT_INTENT",
    received_at: new Date().toISOString(),
    event,
    ...dimensions,
  });

  return NextResponse.json(
    { accepted: true, evidence_class: "UNTRUSTED_CLIENT_INTENT" },
    {
      status: 202,
      headers: {
        "Cache-Control": "no-store",
      },
    },
  );
}
