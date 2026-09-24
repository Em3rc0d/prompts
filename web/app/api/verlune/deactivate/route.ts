import { NextRequest, NextResponse } from "next/server";

import {
  deactivateLicenseKey,
  retrieveRawLicenseKey
} from "@/lib/verlune-access";
import {
  clearPremiumCookieOptions,
  fingerprintLicense,
  parsePremiumSession,
  VERLUNE_DEVICE_COOKIE,
  VERLUNE_SESSION_COOKIE
} from "@/lib/verlune-session";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const session = parsePremiumSession(request.cookies.get(VERLUNE_SESSION_COOKIE)?.value);
  if (!session) {
    const response = NextResponse.redirect(new URL("/unlock?reason=locked", request.url), 303);
    response.cookies.set(VERLUNE_SESSION_COOKIE, "", clearPremiumCookieOptions);
    response.cookies.set(VERLUNE_DEVICE_COOKIE, "", clearPremiumCookieOptions);
    return response;
  }

  try {
    const rawLicenseKey = await retrieveRawLicenseKey(session.licenseKeyId);
    if (fingerprintLicense(rawLicenseKey) !== session.licenseFingerprint) {
      const response = NextResponse.redirect(new URL("/unlock?reason=session-invalid", request.url), 303);
      response.cookies.set(VERLUNE_SESSION_COOKIE, "", clearPremiumCookieOptions);
      response.cookies.set(VERLUNE_DEVICE_COOKIE, "", clearPremiumCookieOptions);
      return response;
    }
    const deactivation = await deactivateLicenseKey(rawLicenseKey, session.instanceId);
    if (!deactivation.deactivated) {
      return NextResponse.redirect(new URL("/app/access?error=deactivation-failed", request.url), 303);
    }

    const response = NextResponse.redirect(new URL("/unlock?reason=deactivated", request.url), 303);
    response.cookies.set(VERLUNE_SESSION_COOKIE, "", clearPremiumCookieOptions);
    response.cookies.set(VERLUNE_DEVICE_COOKIE, "", clearPremiumCookieOptions);
    return response;
  } catch {
    return NextResponse.redirect(new URL("/app/access?error=deactivation-unavailable", request.url), 303);
  }
}
