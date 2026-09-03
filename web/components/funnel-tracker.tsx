"use client";

import { useEffect } from "react";

const ATTRIBUTION_KEY = "pq:attribution";
const SESSION_KEY = "pq:session-id";
const CLIENT_INTENT_EVENTS = new Set([
  "landing_view",
  "collections_viewed",
  "free_product_viewed",
  "free_cta_clicked",
  "starter_product_viewed",
  "starter_cta_clicked",
  "paid_product_viewed",
  "paid_cta_clicked",
]);

type Attribution = { source?: string; medium?: string; campaign?: string; content?: string };
type FunnelEvent = {
  event: string;
  product_id?: string;
  product_version?: string;
  collection_id?: string;
  surface?: string;
};

function readAttribution(): Attribution {
  try { return JSON.parse(sessionStorage.getItem(ATTRIBUTION_KEY) || "{}") as Attribution; }
  catch { return {}; }
}

function captureAttribution(): void {
  const params = new URLSearchParams(window.location.search);
  const previous = readAttribution();
  const next: Attribution = {
    source: params.get("utm_source") || previous.source,
    medium: params.get("utm_medium") || previous.medium,
    campaign: params.get("utm_campaign") || previous.campaign,
    content: params.get("utm_content") || previous.content,
  };
  sessionStorage.setItem(ATTRIBUTION_KEY, JSON.stringify(next));
}

function sessionId(): string {
  const existing = sessionStorage.getItem(SESSION_KEY);
  if (existing) return existing;
  const created = crypto.randomUUID();
  sessionStorage.setItem(SESSION_KEY, created);
  return created;
}

function observeIntent(payload: FunnelEvent): void {
  if (!CLIENT_INTENT_EVENTS.has(payload.event)) return;

  void fetch("/api/analytics/intent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...payload, ...readAttribution() }),
    cache: "no-store",
    credentials: "same-origin",
    keepalive: true,
  }).catch(() => {
    // Analytics is best-effort and must never block the customer workflow.
  });
}

function emit(payload: FunnelEvent) {
  const detail = { ...payload, timestamp: new Date().toISOString(), session_id: sessionId(), ...readAttribution() };
  if ((process.env.NEXT_PUBLIC_ANALYTICS_MODE || "off") === "debug") console.info("[Prompt Machine analytics]", detail);
  observeIntent(payload);
  window.dispatchEvent(new CustomEvent("pq:analytics", { detail }));
}

export function FunnelTracker() {
  useEffect(() => {
    captureAttribution();
    sessionId();

    const path = window.location.pathname;
    if (path === "/") {
      emit({ event: "landing_view", surface: "home" });
    } else if (path === "/collections") {
      emit({ event: "collections_viewed", surface: "collections" });
    } else if (path.startsWith("/free/developer-starter-pack")) {
      emit({
        event: "free_product_viewed",
        product_id: "pq-developer-starter",
        product_version: "1.1.0",
        collection_id: "developer",
        surface: "free-library",
      });
    } else if (path.startsWith("/starter-collection")) {
      emit({
        event: "starter_product_viewed",
        product_id: "pq-developer-starter-collection",
        product_version: "1.2.0-candidate",
        collection_id: "developer",
        surface: "starter-collection",
      });
    } else if (path.startsWith("/developer-pack")) {
      emit({
        event: "paid_product_viewed",
        product_id: "pq-developer-pack",
        product_version: "1.2.0-candidate",
        collection_id: "developer",
        surface: "full-collection",
      });
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
