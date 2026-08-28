"use client";

import { useEffect } from "react";

const ATTRIBUTION_KEY = "pq:attribution";

type Attribution = {
  source?: string;
  medium?: string;
  campaign?: string;
  content?: string;
};

type FunnelEvent = {
  event: string;
  product_id?: string;
  product_version?: string;
};

function readAttribution(): Attribution {
  try {
    return JSON.parse(sessionStorage.getItem(ATTRIBUTION_KEY) || "{}") as Attribution;
  } catch {
    return {};
  }
}

function captureAttribution(): Attribution {
  const params = new URLSearchParams(window.location.search);
  const previous = readAttribution();
  const next: Attribution = {
    source: params.get("utm_source") || previous.source,
    medium: params.get("utm_medium") || previous.medium,
    campaign: params.get("utm_campaign") || previous.campaign,
    content: params.get("utm_content") || previous.content,
  };
  sessionStorage.setItem(ATTRIBUTION_KEY, JSON.stringify(next));
  return next;
}

function emit(payload: FunnelEvent) {
  const mode = process.env.NEXT_PUBLIC_ANALYTICS_MODE || "off";
  const detail = {
    ...payload,
    timestamp: new Date().toISOString(),
    ...readAttribution(),
  };

  if (mode === "debug") console.info("[Prompt Quarry analytics]", detail);
  window.dispatchEvent(new CustomEvent("pq:analytics", { detail }));
}

export function FunnelTracker() {
  useEffect(() => {
    captureAttribution();

    if (window.location.pathname === "/") {
      emit({ event: "landing_view" });
    } else if (window.location.pathname.startsWith("/developer-pack")) {
      emit({ event: "paid_product_viewed", product_id: "pq-developer-pack", product_version: "1.0.0" });
    }

    const handler = (event: Event) => {
      const detail = (event as CustomEvent<FunnelEvent>).detail;
      if (detail?.event) emit(detail);
    };

    window.addEventListener("pq:funnel", handler);
    return () => window.removeEventListener("pq:funnel", handler);
  }, []);

  return null;
}
