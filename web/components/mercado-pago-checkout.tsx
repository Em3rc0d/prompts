"use client";

import Script from "next/script";
import { FormEvent, useEffect, useRef, useState } from "react";

type BrickController = { unmount?: () => void };
type MercadoPagoInstance = {
  bricks: () => {
    create: (
      type: string,
      containerId: string,
      settings: Record<string, unknown>
    ) => Promise<BrickController>;
  };
  yape?: (input: { phoneNumber: string; otp: string }) => {
    create?: () => Promise<{ id?: string } | string>;
  };
};
type MercadoPagoConstructor = new (publicKey: string, options?: Record<string, unknown>) => MercadoPagoInstance;

declare global {
  interface Window {
    MercadoPago?: MercadoPagoConstructor;
  }
}

type PaymentResult = {
  ok?: boolean;
  paymentId?: string;
  status?: string;
  entitled?: boolean;
  redirect?: string;
  error?: string;
};

function humanStatus(status?: string) {
  if (status === "pending" || status === "in_process") return "Mercado Pago is still processing the payment.";
  if (status === "rejected") return "Mercado Pago rejected the payment. Try another method or verify the entered data.";
  return status ? `Payment status: ${status}.` : "The payment could not be completed.";
}

export function MercadoPagoCheckout({
  publicKey,
  pricePenMinor,
  testMode = false
}: {
  publicKey: string;
  pricePenMinor: number;
  testMode?: boolean;
}) {
  const [sdkReady, setSdkReady] = useState(false);
  const [method, setMethod] = useState<"card" | "yape">("card");
  const [message, setMessage] = useState("");
  const [paymentId, setPaymentId] = useState("");
  const [locked, setLocked] = useState(false);
  const [yapeWorking, setYapeWorking] = useState(false);
  const attemptKey = useRef<string | null>(null);
  const controllerRef = useRef<BrickController | null>(null);
  const pricePen = pricePenMinor / 100;

  async function submitPayment(formData: Record<string, unknown>) {
    if (locked) return;
    if (!attemptKey.current) attemptKey.current = crypto.randomUUID();
    setMessage("Confirming payment with Mercado Pago…");

    let response: Response;
    try {
      response = await fetch("/api/commerce/verlune-premium/payment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Idempotency-Key": attemptKey.current
        },
        body: JSON.stringify(formData)
      });
    } catch {
      setMessage("The payment request could not reach Verlune. Retry without changing the payment details.");
      throw new Error("payment_network_error");
    }

    const payload = await response.json().catch(() => ({})) as PaymentResult;
    if (!response.ok) {
      if (response.status < 500) attemptKey.current = null;
      setMessage(payload.error === "provider_test_not_authorized"
        ? "This browser is not authorized for the private TEST checkout."
        : "Mercado Pago could not complete this attempt. No Premium access was granted.");
      throw new Error(payload.error ?? "payment_failed");
    }

    if (payload.paymentId) setPaymentId(payload.paymentId);
    if (payload.entitled) {
      setLocked(true);
      setMessage("Payment approved. Unlocking Verlune Premium…");
      window.location.assign(payload.redirect || "/app");
      return;
    }

    attemptKey.current = null;
    if (payload.status === "pending" || payload.status === "in_process") setLocked(true);
    setMessage(humanStatus(payload.status));
  }

  useEffect(() => {
    const MercadoPagoCtor = window.MercadoPago;
    if (!sdkReady || method !== "card" || !MercadoPagoCtor || locked) return;
    const MercadoPagoReady: MercadoPagoConstructor = MercadoPagoCtor;
    let cancelled = false;

    async function mount() {
      try {
        const mp = new MercadoPagoReady(publicKey, { locale: "es-PE" });
        const bricks = mp.bricks();
        const controller = await bricks.create("cardPayment", "verlune-card-payment-brick", {
          initialization: { amount: pricePen },
          customization: {
            paymentMethods: {
              minInstallments: 1,
              maxInstallments: 1
            }
          },
          callbacks: {
            onReady: () => setMessage(""),
            onSubmit: async (formData: Record<string, unknown>) => {
              await submitPayment(formData);
            },
            onError: () => setMessage("The Mercado Pago card form reported an error. Check the fields and try again.")
          }
        });
        if (cancelled) controller.unmount?.();
        else controllerRef.current = controller;
      } catch {
        setMessage("Mercado Pago checkout could not initialize.");
      }
    }

    mount();
    return () => {
      cancelled = true;
      controllerRef.current?.unmount?.();
      controllerRef.current = null;
    };
  }, [sdkReady, method, publicKey, pricePen, locked]);

  async function submitYape(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const MercadoPagoCtor = window.MercadoPago;
    if (locked || yapeWorking || !MercadoPagoCtor) return;
    setYapeWorking(true);
    setMessage("");

    const form = new FormData(event.currentTarget);
    const email = String(form.get("email") ?? "").trim();
    const phoneNumber = String(form.get("phone") ?? "").replace(/\D/g, "");
    const otp = String(form.get("otp") ?? "").replace(/\D/g, "");

    try {
      const mp = new MercadoPagoCtor(publicKey, { locale: "es-PE" });
      if (typeof mp.yape !== "function") throw new Error("yape_unavailable");
      const yape = mp.yape({ phoneNumber, otp });
      if (typeof yape.create !== "function") throw new Error("yape_unavailable");
      const resource = await yape.create();
      const token = typeof resource === "string" ? resource : resource?.id;
      if (!token) throw new Error("yape_token_missing");

      await submitPayment({
        token,
        payment_method_id: "yape",
        installments: 1,
        payer: { email }
      });
    } catch (error) {
      if (error instanceof Error && error.message === "payment_network_error") return;
      setMessage("Yape could not generate or process the payment token. Verify the phone and approval code.");
    } finally {
      setYapeWorking(false);
    }
  }

  return <div className="mpCheckout">
    <Script src="https://sdk.mercadopago.com/js/v2" strategy="afterInteractive" onLoad={() => setSdkReady(true)} />

    <div className="accessTrust">
      <p><strong>S/ {pricePen.toFixed(2)}</strong> · one-time payment · Verlune Premium</p>
      <p><strong>Secure fields.</strong> Card data, Yape phone and Yape approval code are tokenized by Mercado Pago and are not sent to Verlune.</p>
      {testMode ? <p><strong>TEST mode.</strong> Use only Mercado Pago test credentials and documented Yape test data.</p> : null}
    </div>

    <div className="actions">
      <button className={`btn ${method === "card" ? "btnPrimary" : "btnSecondary"}`} type="button" onClick={() => setMethod("card")} disabled={locked}>Card</button>
      <button className={`btn ${method === "yape" ? "btnPrimary" : "btnSecondary"}`} type="button" onClick={() => setMethod("yape")} disabled={locked}>Yape</button>
    </div>

    {method === "card"
      ? <div id="verlune-card-payment-brick" aria-live="polite" />
      : <form className="unlockForm" onSubmit={submitYape}>
          <label><span>Checkout email</span><input name="email" type="email" autoComplete="email" required disabled={locked || yapeWorking} /></label>
          <label><span>Yape phone</span><input name="phone" type="tel" inputMode="numeric" autoComplete="tel" pattern="[0-9]{9,15}" required disabled={locked || yapeWorking} /></label>
          <label><span>Yape approval code</span><input name="otp" type="text" inputMode="numeric" autoComplete="one-time-code" pattern="[0-9]{6}" required disabled={locked || yapeWorking} /></label>
          <button className="btn btnPrimary" type="submit" disabled={!sdkReady || locked || yapeWorking}>
            {yapeWorking ? "Processing…" : `Pay S/ ${pricePen.toFixed(2)} with Yape`}
          </button>
        </form>}

    {message ? <p className="notice" role="status">{message}</p> : null}
    {paymentId ? <p className="micro">Mercado Pago payment ID: <code>{paymentId}</code>. Keep it with your checkout email for access recovery.</p> : null}
  </div>;
}
