"use client";

import type { MouseEvent, ReactNode } from "react";

const ATTRIBUTION_KEY = "pq:attribution";

type Attribution = { source?: string; medium?: string; campaign?: string; content?: string };

declare global {
  interface Window {
    createLemonSqueezy?: () => void;
    LemonSqueezy?: {
      Url?: {
        Open?: (url: string) => void;
      };
    };
  }
}

function readAttribution(): Attribution {
  try { return JSON.parse(sessionStorage.getItem(ATTRIBUTION_KEY) || "{}") as Attribution; }
  catch { return {}; }
}

function internalUrl(path: string): string {
  const url = new URL(path, window.location.origin);
  for (const [key, value] of Object.entries(readAttribution())) if (value) url.searchParams.set(key, value);
  return `${url.pathname}${url.search}`;
}

async function resolveCheckoutUrl(path: string): Promise<string | null> {
  const response = await fetch(internalUrl(path), {
    method: "GET",
    redirect: "manual",
    headers: { Accept: "application/json" },
  });

  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) {
    const payload = await response.json().catch(() => null) as { checkoutUrl?: unknown } | null;
    if (response.ok && typeof payload?.checkoutUrl === "string") return payload.checkoutUrl;
    return null;
  }

  return response.headers.get("location");
}

export function LemonCheckoutLink({
  href,
  children,
  className = "btn btnPrimary",
  onBeforeOpen,
}: {
  href: string;
  children: ReactNode;
  className?: string;
  onBeforeOpen?: () => void;
}) {
  async function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    onBeforeOpen?.();

    try {
      const location = await resolveCheckoutUrl(href);
      if (!location) {
        window.location.assign(internalUrl(href));
        return;
      }

      window.createLemonSqueezy?.();
      const open = window.LemonSqueezy?.Url?.Open;
      if (!open) {
        window.location.assign(location);
        return;
      }

      open(location);
    } catch {
      window.location.assign(internalUrl(href));
    }
  }

  return <a className={className} href={href} onClick={handleClick}>{children}</a>;
}
