import {
  MercadoPagoApiError,
  readMercadoPagoPayment,
  verifyMercadoPagoWebhook,
  verifyVerlunePremiumPayment
} from "@/lib/verlune-mercado-pago";

export const runtime = "nodejs";

export async function POST(request: Request) {
  const secret = process.env.MP_WEBHOOK_SECRET?.trim() ?? "";
  if (secret.length < 16) {
    return Response.json({ ok: false, error: "webhook_not_configured" }, { status: 503 });
  }

  try {
    const signed = verifyMercadoPagoWebhook({
      url: request.url,
      headers: request.headers,
      secret
    });

    if (!/^\d+$/.test(signed.dataId)) {
      return Response.json({ ok: true, ignored: true, reason: "unsupported_resource" });
    }

    const payment = await readMercadoPagoPayment(signed.dataId);
    const verification = verifyVerlunePremiumPayment(payment);

    console.info("VERLUNE_MP_EVENT", JSON.stringify({
      event: "mercado_pago_payment_webhook",
      payment_id: verification.paymentId,
      matched: !verification.reason || verification.reason.startsWith("payment_"),
      status: verification.status,
      entitled: verification.entitled,
      timestamp: new Date().toISOString()
    }));

    return Response.json({
      ok: true,
      received: true,
      paymentId: verification.paymentId,
      status: verification.status,
      entitled: verification.entitled
    });
  } catch (error) {
    if (error instanceof MercadoPagoApiError) {
      return Response.json({ ok: false, error: error.code }, { status: error.status });
    }
    return Response.json({ ok: false, error: "webhook_failed" }, { status: 502 });
  }
}
