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
    const licenseKey = String(form.get("licenseKey") ?? "").trim();
    const email = String(form.get("email") ?? "").trim();

    try {
      const response = await fetch("/api/verlune/unlock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ licenseKey, email, next: nextPath })
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
    <label>
      <span>Checkout email</span>
      <input name="email" type="email" autoComplete="email" required disabled={state === "working"} />
    </label>
    <label>
      <span>License key</span>
      <input name="licenseKey" type="text" autoComplete="off" spellCheck={false} required disabled={state === "working"} />
    </label>
    <button className="btn btnPrimary" type="submit" disabled={state === "working"}>
      {state === "working" ? "Checking access…" : "Unlock Premium"}
    </button>
    {state === "error" ? <p className="formError" role="alert">{message}</p> : null}
    <p className="micro">Your license is checked server-side. Verlune does not store the raw key in the browser session cookie.</p>
  </form>;
}
