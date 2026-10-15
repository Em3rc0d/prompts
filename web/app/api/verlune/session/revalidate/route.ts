import { NextRequest, NextResponse } from "next/server";

import { safePremiumNextPath } from "@/lib/verlune-auth.server";
import {
  entitlementMatchesEmail,
  getVerlunePremiumEntitlementById,
  syncVerlunePremiumEntitlement,
  VerluneAccessError
} from "@/lib/verlune-access";
import {
  MercadoPagoApiError,
  readMercadoPagoPayment,
  verifyVerlunePremiumPayment
} from "@/lib/verlune-mercado-pago";
import {
  clearPremiumCookieOptions,
  hashCustomerEmail,
  parsePremiumSession,
  premiumCookieOptions,
  refreshedPremiumSession,
  signPremiumSession,
  VERLUNE_DEVICE_COOKIE,
  VERLUNE_SESSION_COOKIE
} from "@/lib/verlune-session";

export const runtime = "nodejs";

function unlockRedirect(request: NextRequest, reason: string, clear = false) {
  const response = NextResponse.redirect(new URL(`/unlock?reason=${encodeURIComponent(reason)}`, request.url), 303);
  if (clear) {
    response.cookies.set(VERLUNE_SESSION_COOKIE, "", clearPremiumCookieOptions);
    response.cookies.set(VERLUNE_DEVICE_COOKIE, "", clearPremiumCookieOptions);
  }
  return response;
}

function retryableOutageRedirect(request: NextRequest, session: NonNullable<ReturnType<typeof parsePremiumSession>>) {
  const response = NextResponse.redirect(new URL("/unlock?reason=revalidation-unavailable", request.url), 303);
  const blockedSession = { ...session, validatedAt: 0 };
  response.cookies.set(VERLUNE_SESSION_COOKIE, signPremiumSession(blockedSession), premiumCookieOptions(blockedSession));
  return response;
}

export async function GET(request: NextRequest) {
  const nextPath = safePremiumNextPath(request.nextUrl.searchParams.get("next"));
  const session = parsePremiumSession(request.cookies.get(VERLUNE_SESSION_COOKIE)?.value);
  if (!session) return unlockRedirect(request, "locked", true);

  try {
    if (session.v === 3 && session.provider === "verlune") {
      const entitlement = await getVerlunePremiumEntitlementById(session.entitlementId);
      if (!entitlement || entitlement.status !== "active") return unlockRedirect(request, "session-invalid", true);

      const payment = await readMercadoPagoPayment(entitlement.paymentId);
      const verification = verifyVerlunePremiumPayment(payment);
      const refreshedEntitlement = await syncVerlunePremiumEntitlement(verification);
      const emailMatches = Boolean(verification.customerEmail)
        && hashCustomerEmail(verification.customerEmail) === session.emailHash
        && entitlementMatchesEmail(entitlement, verification.customerEmail);

      if (!verification.entitled || !refreshedEntitlement || refreshedEntitlement.status !== "active" || !emailMatches) {
        return unlockRedirect(request, "session-invalid", true);
      }

      const refreshed = refreshedPremiumSession(session);
      const response = NextResponse.redirect(new URL(nextPath, request.url), 303);
      response.cookies.set(VERLUNE_SESSION_COOKIE, signPremiumSession(refreshed), premiumCookieOptions(refreshed));
      return response;
    }

    if (session.v === 2 && session.provider === "mercado_pago") {
      const payment = await readMercadoPagoPayment(session.paymentId);
      const verification = verifyVerlunePremiumPayment(payment);
      const emailMatches = verification.customerEmail &&
        hashCustomerEmail(verification.customerEmail) === session.emailHash;

      if (!verification.entitled || !emailMatches) return unlockRedirect(request, "session-invalid", true);

      const refreshed = refreshedPremiumSession(session);
      const response = NextResponse.redirect(new URL(nextPath, request.url), 303);
      response.cookies.set(VERLUNE_SESSION_COOKIE, signPremiumSession(refreshed), premiumCookieOptions(refreshed));
      return response;
    }

    return unlockRedirect(request, "session-invalid", true);
  } catch (error) {
    if (error instanceof MercadoPagoApiError && (error.status === 400 || error.status === 404)) {
      return unlockRedirect(request, "session-invalid", true);
    }
    if (error instanceof MercadoPagoApiError || error instanceof VerluneAccessError) {
      return retryableOutageRedirect(request, session);
    }
    return retryableOutageRedirect(request, session);
  }
}
