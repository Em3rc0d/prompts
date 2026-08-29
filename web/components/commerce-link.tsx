"use client";

import type { MouseEvent, ReactNode } from "react";

const ATTRIBUTION_KEY = "pq:attribution";

type Props = {
  kind: "free" | "paid";
  children: ReactNode;
  className?: string;
};

type Attribution = {
  source?: string;
  medium?: string;
  campaign?: string;
  content?: string;
};

function readAttribution(): Attribution {
  try {
    return JSON.parse(sessionStorage.getItem(ATTRIBUTION_KEY) || "{}") as Attribution;
  } catch {
    return {};
  }
}

function attributedInternalUrl(path: string): string {
  const url = new URL(path, window.location.origin);
  const attribution = readAttribution();
  for (const [key, value] of Object.entries(attribution)) {
    if (value) url.searchParams.set(key, value);
  }
  return `${url.pathname}${url.search}`;
}

function attributedExternalUrl(rawUrl: string): string {
  const url = new URL(rawUrl);
  const attribution = readAttribution();
  const mapping: Record<keyof Attribution, string> = {
    source: "utm_source",
    medium: "utm_medium",
    campaign: "utm_campaign",
    content: "utm_content",
  };
  for (const [key, value] of Object.entries(attribution) as [keyof Attribution, string | undefined][]) {
    if (value) url.searchParams.set(mapping[key], value);
  }
  return url.toString();
}

export function CommerceLink({ kind, children, className = "btn btnPrimary" }: Props) {
  const freeExternal = process.env.NEXT_PUBLIC_FREE_PACK_URL;
  const checkoutConfigured = Boolean(process.env.NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL);
  const href = kind === "free"
    ? (freeExternal || "/api/free-pack/v1")
    : "/api/commerce/developer-pack/checkout";

  function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    window.dispatchEvent(new CustomEvent("pq:funnel", {
      detail: { event: kind === "free" ? "free_cta_clicked" : "paid_cta_clicked" },
    }));

    if (kind === "paid" && !checkoutConfigured) {
      event.preventDefault();
      window.dispatchEvent(new CustomEvent("pq:checkout-unavailable"));
      alert("Checkout configuration pending. Developer Pack v1 is READY, but live checkout is not configured yet.");
      return;
    }

    event.preventDefault();
    const destination = kind === "free" && freeExternal
      ? attributedExternalUrl(freeExternal)
      : attributedInternalUrl(href);
    window.location.assign(destination);
  }

  return <a className={className} href={href} onClick={handleClick}>{children}</a>;
}
