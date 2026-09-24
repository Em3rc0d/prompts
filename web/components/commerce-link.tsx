"use client";

import type { MouseEvent, ReactNode } from "react";
import { STARTER_CODE_REVIEW_RELEASE } from "@/lib/starter-code-review-release";
import { LemonCheckoutLink } from "./lemon-checkout-link";

const ATTRIBUTION_KEY = "pq:attribution";

type Props = { kind: "free" | "code-review" | "starter" | "paid"; children: ReactNode; className?: string };
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
    : kind === "code-review"
      ? "/api/commerce/starter-code-review/checkout"
      : kind === "starter"
      ? "/code-review"
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
      : kind === "code-review"
        ? { event: "starter_cta_clicked", product_id: STARTER_CODE_REVIEW_RELEASE.productId, product_version: STARTER_CODE_REVIEW_RELEASE.version, collection_id: "developer", surface: "code-review" }
        : kind === "starter"
        ? {
            event: "starter_cta_clicked",
            product_id: "prompt-machine-starter-collection",
            product_version: "1.0.0-candidate",
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
    if ((kind === "free" && freeExternal) || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();

    window.location.assign(internalUrl(href));
  }

  if (kind === "code-review" || (kind === "paid" && publicFullSaleLive)) {
    return <LemonCheckoutLink
      className={className}
      href={href}
      onBeforeOpen={() => {
        window.dispatchEvent(new CustomEvent("pq:funnel", { detail: kind === "code-review"
          ? { event: "starter_cta_clicked", product_id: STARTER_CODE_REVIEW_RELEASE.productId, product_version: STARTER_CODE_REVIEW_RELEASE.version, collection_id: "developer", surface: "code-review" }
          : { event: "paid_cta_clicked", product_id: "pq-developer-pack", product_version: "1.2.0-candidate", collection_id: "developer", surface: "full-collection" }
        }));
      }}
    >{children}</LemonCheckoutLink>;
  }

  return <a className={className} href={href} onClick={handleClick}>{children}</a>;
}
