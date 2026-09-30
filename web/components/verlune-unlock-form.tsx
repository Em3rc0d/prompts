"use client";

import { FormEvent, useState } from "react";

export function VerluneUnlockForm({ nextPath = "/app" }: { nextPath?: string }) {
  const [state, setState] = useState<"idle" | "working" | "error">("idle");
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setState("working");
    setMessage("");

    const form = new FormData(event.currentTarget);
    const paymentId = String(form.get("paymentId") ?? "").trim();
    const email = String(form.get("email") ?? "").trim();

    try {
      const response = await fetch("/api/verlune/unlock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ paymentId, email, next: nextPath })
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        setState("error");
        setMessage(typeof payload?.message === "string" ? payload.message : "We could not unlock Premium with those details.");
        return;
      }
      window.location.assign(typeof payload?.redirect === "string" ? payload.redirect : "/app");
    } catch {
      setState("error");
      setMessage("Unlock is temporarily unavailable. Please try again.");
    }
  }

  return <form className="unlockForm" onSubmit={submit}>
    <label><span>Checkout email</span><input name="email" type="email" autoComplete="email" required disabled={state === "working"} /></label>
    <label><span>Mercado Pago payment ID</span><input name="paymentId" type="text" inputMode="numeric" autoComplete="off" spellCheck={false} required disabled={state === "working"} /></label>
    <button className="btn btnPrimary" type="submit" disabled={state === "working"}>{state === "working" ? "Checking payment…" : "Unlock Premium"}</button>
    {state === "error" ? <p className="formError" role="alert">{message}</p> : null}
    <p className="micro">Verlune reads the payment from Mercado Pago server-side and grants access only to the configured Premium product, price, account and approved status.</p>
  </form>;
}
