import {
  provisionVerlunePremiumAccess,
  syncVerlunePremiumEntitlement,
  VerluneAccessError
} from "@/lib/verlune-access";
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
    const provisioned = verification.entitled
      ? await provisionVerlunePremiumAccess(verification)
      : {
          entitlement: await syncVerlunePremiumEntitlement(verification),
          accessKey: null,
          emailSent: false
        };

    console.info("VERLUNE_MP_EVENT", JSON.stringify({
      event: "mercado_pago_payment_webhook",
      payment_id: verification.paymentId,
      matched: !verification.reason || verification.reason.startsWith("payment_"),
      status: verification.status,
      entitled: verification.entitled,
      entitlement_id: provisioned.entitlement?.entitlementId ?? null,
      access_email: provisioned.emailSent ? "sent" : verification.entitled ? "deferred" : "not_applicable",
      timestamp: new Date().toISOString()
    }));

    return Response.json({
      ok: true,
      received: true,
      paymentId: verification.paymentId,
      status: verification.status,
      entitled: verification.entitled,
      entitlementId: provisioned.entitlement?.entitlementId ?? null
    });
  } catch (error) {
    if (error instanceof MercadoPagoApiError || error instanceof VerluneAccessError) {
      return Response.json({ ok: false, error: error.code }, { status: error.status });
    }
    return Response.json({ ok: false, error: "webhook_failed" }, { status: 502 });
  }
}
