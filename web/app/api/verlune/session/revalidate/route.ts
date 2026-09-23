import { NextRequest, NextResponse } from "next/server";

import { safePremiumNextPath } from "@/lib/verlune-auth.server";
import {
  entitlementMatches,
  LemonAdminApiError,
  LemonLicenseApiError,
  retrieveRawLicenseKey,
  validateLicenseKey
} from "@/lib/verlune-access";
import {
  clearPremiumCookieOptions,
  fingerprintLicense,
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
  const response = NextResponse.redirect(
    new URL("/unlock?reason=revalidation-unavailable", request.url),
    303
  );

  // Preserve the signed entitlement reference for Retry, but force it stale so
  // every protected route keeps redirecting to revalidation until the provider succeeds.
  const blockedSession = { ...session, validatedAt: 0 };
  response.cookies.set(
    VERLUNE_SESSION_COOKIE,
    signPremiumSession(blockedSession),
    premiumCookieOptions(blockedSession)
  );
  return response;
}

export async function GET(request: NextRequest) {
  const nextPath = safePremiumNextPath(request.nextUrl.searchParams.get("next"));
  const session = parsePremiumSession(request.cookies.get(VERLUNE_SESSION_COOKIE)?.value);
  if (!session) return unlockRedirect(request, "locked", true);

  try {
    const rawLicenseKey = await retrieveRawLicenseKey(session.licenseKeyId);
    if (fingerprintLicense(rawLicenseKey) !== session.licenseFingerprint) {
      return unlockRedirect(request, "session-invalid", true);
    }

    const validation = await validateLicenseKey(rawLicenseKey, session.instanceId);
    const providerEmail = validation.meta?.customer_email ?? "";
    const identity = entitlementMatches(validation, providerEmail);
    const emailMatches = providerEmail && hashCustomerEmail(providerEmail) === session.emailHash;
    const instanceMatches = validation.instance?.id === session.instanceId;

    if (!identity.ok || !emailMatches || !instanceMatches) {
      return unlockRedirect(request, "session-invalid", true);
    }

    const refreshed = refreshedPremiumSession(session);
    const response = NextResponse.redirect(new URL(nextPath, request.url), 303);
    response.cookies.set(
      VERLUNE_SESSION_COOKIE,
      signPremiumSession(refreshed),
      premiumCookieOptions(refreshed)
    );
    return response;
  } catch (error) {
    const rejectedLicense =
      error instanceof LemonLicenseApiError &&
      error.operation === "validate" &&
      error.status >= 400 &&
      error.status < 500 &&
      error.status !== 429;

    const missingOrRejectedAdminLicense =
      error instanceof LemonAdminApiError &&
      (error.status === 404 || error.status === 410);

    if (rejectedLicense || missingOrRejectedAdminLicense) {
      // A provider-side entitlement rejection is not an outage. Invalidate the browser authorization.
      return unlockRedirect(request, "session-invalid", true);
    }

    // Network, rate-limit and upstream 5xx failures remain retryable and fail closed.
    // The session is retained only as a stale retry token; it cannot authorize Premium.
    return retryableOutageRedirect(request, session);
  }
}
