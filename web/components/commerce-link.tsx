"use client";

import type { MouseEvent, ReactNode } from "react";

const ATTRIBUTION_KEY = "pq:attribution";

type Props = { kind: "free" | "starter" | "paid"; children: ReactNode; className?: string };
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
  const publicFullSaleLive = process.env.NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS === "LIVE";
  const href = kind === "free"
    ? (freeExternal || "/api/free-pack/v1")
    : kind === "starter"
      ? "/starter-collection"
      : (publicFullSaleLive ? "/api/commerce/developer-pack/checkout" : "/developer-pack");

  function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    const detail = kind === "free"
      ? {
          event: "free_cta_clicked",
          product_id: "pq-developer-starter",
          product_version: "1.1.0",
          collection_id: "developer",
          surface: "free-library",
        }
      : kind === "starter"
        ? {
            event: "starter_cta_clicked",
            product_id: "pq-developer-starter-collection",
            product_version: "1.2.0-candidate",
            collection_id: "developer",
            surface: "starter-collection",
          }
        : {
            event: "paid_cta_clicked",
            product_id: "pq-developer-pack",
            product_version: "1.2.0-candidate",
            collection_id: "developer",
            surface: "full-collection",
          };

    window.dispatchEvent(new CustomEvent("pq:funnel", { detail }));
    if (kind === "free" && freeExternal) return;
    event.preventDefault();
    window.location.assign(internalUrl(href));
  }

  return <a className={className} href={href} onClick={handleClick}>{children}</a>;
}
