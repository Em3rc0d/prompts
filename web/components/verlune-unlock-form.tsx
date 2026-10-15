"use client";

import { FormEvent, useState } from "react";

export function VerluneUnlockForm({ nextPath = "/app" }: { nextPath?: string }) {
  const [state, setState] = useState<"idle" | "working" | "error">("idle");
  const [message, setMessage] = useState("");
  const [email, setEmail] = useState("");
  const [recoveryState, setRecoveryState] = useState<"idle" | "working">("idle");
  const [recoveryMessage, setRecoveryMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setState("working");
    setMessage("");

    const form = new FormData(event.currentTarget);
    const accessKey = String(form.get("accessKey") ?? "").trim();

    try {
      const response = await fetch("/api/verlune/unlock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ accessKey, email, next: nextPath })
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

  async function recover() {
    if (!email.trim()) {
      setRecoveryMessage("Enter your checkout email first.");
      return;
    }
    setRecoveryState("working");
    setRecoveryMessage("");
    try {
      const response = await fetch("/api/verlune/access-key/recover", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
      });
      const payload = await response.json().catch(() => ({}));
      setRecoveryMessage(typeof payload?.message === "string"
        ? payload.message
        : response.ok
          ? "If that email has an active purchase, its existing Access Key will be sent again."
          : "Recovery is temporarily unavailable.");
    } catch {
      setRecoveryMessage("Recovery is temporarily unavailable.");
    } finally {
      setRecoveryState("idle");
    }
  }

  return <form className="unlockForm" onSubmit={submit}>
    <label><span>Checkout email</span><input name="email" type="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)} disabled={state === "working"} /></label>
    <label><span>Verlune Access Key</span><input name="accessKey" type="text" autoComplete="off" spellCheck={false} placeholder="VLK1_…" required disabled={state === "working"} /></label>
    <button className="btn btnPrimary" type="submit" disabled={state === "working"}>{state === "working" ? "Checking access…" : "Unlock Premium"}</button>
    {state === "error" ? <p className="formError" role="alert">{message}</p> : null}
    <button className="textLink" type="button" onClick={recover} disabled={recoveryState === "working"}>
      {recoveryState === "working" ? "Sending…" : "Email me my Access Key again"}
    </button>
    {recoveryMessage ? <p className="micro" role="status">{recoveryMessage}</p> : null}
    <p className="micro">Your checkout email has one canonical Verlune Access Key. Recovery sends that same key again; it does not create a new one.</p>
  </form>;
}
