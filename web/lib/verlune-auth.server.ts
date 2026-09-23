import "server-only";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import {
  parsePremiumSession,
  sessionNeedsRevalidation,
  VERLUNE_SESSION_COOKIE,
  type PremiumSession
} from "./verlune-session";

export function safePremiumNextPath(value: string | null | undefined): string {
  if (!value) return "/app";
  if (!value.startsWith("/app") || value.startsWith("//")) return "/app";
  return value;
}

export async function readPremiumSession(): Promise<PremiumSession | null> {
  const store = await cookies();
  return parsePremiumSession(store.get(VERLUNE_SESSION_COOKIE)?.value);
}

export async function requirePremiumSession(nextPath = "/app"): Promise<PremiumSession> {
  const session = await readPremiumSession();
  if (!session) redirect(`/unlock?reason=locked&next=${encodeURIComponent(safePremiumNextPath(nextPath))}`);
  if (sessionNeedsRevalidation(session)) {
    redirect(`/api/verlune/session/revalidate?next=${encodeURIComponent(safePremiumNextPath(nextPath))}`);
  }
  return session;
}
