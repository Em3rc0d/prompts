"use client";

import type { MouseEvent, ReactNode } from "react";

const ATTRIBUTION_KEY = "pq:attribution";

type Props = { kind: "free" | "paid"; children: ReactNode; className?: string };
type Attribution = { source?: string; medium?: string; campaign?: string; content?: string };

function readAttribution(): Attribution {
  try { return JSON.parse(sessionStorage.getItem(ATTRIBUTION_KEY) || "{}") as Attribution; }
  catch { return {}; }
}

function internalUrl(path: string): string {
  const url = new URL(path, window.location.origin);
  for (const [key, value] of Object.entries(readAttribution())) if (value) url.searchParams.set(key, value);
  return `${url.pathname}${url.search}`;
}

export function CommerceLink({ kind, children, className = "btn btnPrimary" }: Props) {
  const freeExternal = process.env.NEXT_PUBLIC_FREE_PACK_URL;
  const checkoutConfigured = Boolean(process.env.NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL);
  const href = kind === "free" ? (freeExternal || "/api/free-pack/v1.1.0") : (checkoutConfigured ? "/api/commerce/developer-pack/checkout" : "/developer-pack");

  function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    window.dispatchEvent(new CustomEvent("pq:funnel", { detail: { event: kind === "free" ? "free_cta_clicked" : "paid_cta_clicked" } }));
    if (kind === "free" && freeExternal) return;
    event.preventDefault();
    window.location.assign(internalUrl(href));
  }

  return <a className={className} href={href} onClick={handleClick}>{children}</a>;
}
