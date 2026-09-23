import { NextRequest, NextResponse } from "next/server";

import {
  deactivateLicenseKey,
  retrieveRawLicenseKey
} from "@/lib/verlune-access";
import {
  clearPremiumCookieOptions,
  fingerprintLicense,
  parsePremiumSession,
  VERLUNE_SESSION_COOKIE
} from "@/lib/verlune-session";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const session = parsePremiumSession(request.cookies.get(VERLUNE_SESSION_COOKIE)?.value);
  if (!session) {
    const response = NextResponse.redirect(new URL("/unlock?reason=locked", request.url), 303);
    response.cookies.set(VERLUNE_SESSION_COOKIE, "", clearPremiumCookieOptions);
    return response;
  }

  try {
    const rawLicenseKey = await retrieveRawLicenseKey(session.licenseKeyId);
    if (fingerprintLicense(rawLicenseKey) !== session.licenseFingerprint) {
      return NextResponse.json({ ok: false, message: "Session identity check failed." }, { status: 401 });
    }
    const deactivation = await deactivateLicenseKey(rawLicenseKey, session.instanceId);
    if (!deactivation.deactivated) {
      return NextResponse.json({ ok: false, message: "This browser could not be deactivated." }, { status: 502 });
    }

    const response = NextResponse.redirect(new URL("/unlock?reason=deactivated", request.url), 303);
    response.cookies.set(VERLUNE_SESSION_COOKIE, "", clearPremiumCookieOptions);
    return response;
  } catch {
    return NextResponse.json(
      { ok: false, message: "Deactivation is temporarily unavailable. Your local session was kept so you can retry." },
      { status: 502 }
    );
  }
}
