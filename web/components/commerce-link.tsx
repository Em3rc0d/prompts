"use client";

import Link from "next/link";
import type { MouseEvent, ReactNode } from "react";

type Props = {
  kind: "free" | "paid";
  children: ReactNode;
  className?: string;
};

export function CommerceLink({ kind, children, className = "btn btnPrimary" }: Props) {
  const external = kind === "free"
    ? process.env.NEXT_PUBLIC_FREE_PACK_URL
    : process.env.NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL;
  const fallback = kind === "free" ? "/free/developer-starter-pack" : "/developer-pack";

  function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    window.dispatchEvent(new CustomEvent("pq:funnel", { detail: { event: kind === "free" ? "free_cta_clicked" : "paid_cta_clicked" } }));
    if (kind === "paid" && !external) {
      event.preventDefault();
      window.dispatchEvent(new CustomEvent("pq:checkout-unavailable"));
      alert("Checkout configuration pending. Developer Pack v1 is READY, but live checkout is not configured yet.");
    }
  }

  return <Link className={className} href={external || fallback} onClick={handleClick}>{children}</Link>;
}
