"use client";

import { useState } from "react";

export function CopyPremiumAsset({ content }: { content: string }) {
  const [copied, setCopied] = useState(false);
  const [failed, setFailed] = useState(false);

  async function copy() {
    setFailed(false);
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
      setFailed(true);
      window.setTimeout(() => setFailed(false), 2200);
    }
  }

  return <button
    className={`btn btnPrimary vCopyButton${copied ? " isCopied" : ""}${failed ? " isError" : ""}`}
    type="button"
    onClick={copy}
    aria-live="polite"
  >
    <span aria-hidden="true">{copied ? "✓" : failed ? "!" : "⧉"}</span>
    {copied ? "Copied" : failed ? "Copy failed" : "Copy full asset"}
  </button>;
}
