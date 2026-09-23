import { NextRequest, NextResponse } from "next/server";

import { safePremiumNextPath } from "@/lib/verlune-auth.server";
import {
  activateLicenseKey,
  entitlementMatches,
  getVerluneAccessConfigState,
  normalizeEmail,
  validateLicenseKey
} from "@/lib/verlune-access";
import {
  newPremiumSession,
  premiumCookieOptions,
  signPremiumSession,
  VERLUNE_SESSION_COOKIE
} from "@/lib/verlune-session";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const configState = getVerluneAccessConfigState();
  if (!configState.ready) {
    return NextResponse.json(
      { ok: false, message: "Premium access is not configured on this deployment." },
      { status: 503 }
    );
  }

  const body = await request.json().catch(() => null) as
    | { licenseKey?: unknown; email?: unknown; next?: unknown }
    | null;

  const licenseKey = typeof body?.licenseKey === "string" ? body.licenseKey.trim() : "";
  const email = typeof body?.email === "string" ? normalizeEmail(body.email) : "";
  const nextPath = safePremiumNextPath(typeof body?.next === "string" ? body.next : "/app");

  if (licenseKey.length < 8 || licenseKey.length > 200 || !email || email.length > 320) {
    return NextResponse.json(
      { ok: false, message: "Enter the checkout email and license key from your receipt." },
      { status: 400 }
    );
  }

  try {
    // Validate identity before consuming an activation.
    const validation = await validateLicenseKey(licenseKey);
    const validationMatch = entitlementMatches(validation, email);
    if (!validationMatch.ok || !validation.license_key?.id) {
      return NextResponse.json(
        { ok: false, message: "That license and email do not match an active Verlune Premium purchase." },
        { status: 401 }
      );
    }

    const activation = await activateLicenseKey(licenseKey);
    const activationMatch = entitlementMatches(activation, email);
    if (!activationMatch.ok || !activation.instance?.id || !activation.license_key?.id) {
      return NextResponse.json(
        { ok: false, message: "The license is valid, but this browser could not be activated." },
        { status: 409 }
      );
    }

    const session = newPremiumSession({
      licenseKeyId: String(activation.license_key.id),
      instanceId: activation.instance.id,
      licenseKey,
      customerEmail: email
    });

    const response = NextResponse.json({ ok: true, redirect: nextPath });
    response.cookies.set(
      VERLUNE_SESSION_COOKIE,
      signPremiumSession(session),
      premiumCookieOptions(session)
    );
    return response;
  } catch {
    return NextResponse.json(
      { ok: false, message: "Premium access could not be verified right now. Please try again." },
      { status: 502 }
    );
  }
}
