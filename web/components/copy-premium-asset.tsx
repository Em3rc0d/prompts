"use client";

import { useState } from "react";

export function CopyPremiumAsset({ content }: { content: string }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  }

  return <button className="btn btnPrimary" type="button" onClick={copy}>
    {copied ? "Copied" : "Copy full asset"}
  </button>;
}
