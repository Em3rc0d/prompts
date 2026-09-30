import { getVerlunePremiumCommerceState } from "@/lib/verlune-premium-commerce";

export async function GET(request: Request) {
  const commerce = getVerlunePremiumCommerceState();
  if (!commerce.purchaseAvailable) {
    return Response.json(
      {
        ok: false,
        error: "commerce_disabled",
        sale_status: commerce.publicSaleLive ? "LIVE" : "NOT_FOR_SALE",
        commerce_mode: commerce.mode,
        provider: "mercado_pago"
      },
      { status: 503 }
    );
  }

  const incoming = new URL(request.url);
  const destination = new URL("/checkout", request.url);
  for (const field of ["source", "medium", "campaign", "content"]) {
    const value = incoming.searchParams.get(field);
    if (value) destination.searchParams.set(field, value.slice(0, 120));
  }
  return Response.redirect(destination, 303);
}
