import { NextRequest, NextResponse } from "next/server";

import { safePremiumNextPath } from "@/lib/verlune-auth.server";
import {
  activateLicenseKey,
  entitlementMatches,
  getVerluneAccessConfigState,
  LemonLicenseApiError,
  normalizeEmail,
  validateLicenseKey
} from "@/lib/verlune-access";
import {
  fingerprintLicense,
  newPremiumDeviceRef,
  newPremiumSession,
  parsePremiumDeviceRef,
  premiumCookieOptions,
  premiumDeviceCookieOptions,
  signPremiumDeviceRef,
  signPremiumSession,
  VERLUNE_DEVICE_COOKIE,
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

    const licenseKeyId = String(validation.license_key.id);
    const licenseFingerprint = fingerprintLicense(licenseKey);
    const existingDevice = parsePremiumDeviceRef(request.cookies.get(VERLUNE_DEVICE_COOKIE)?.value);

    let instanceId: string | null = null;
    if (
      existingDevice &&
      existingDevice.licenseKeyId === licenseKeyId &&
      existingDevice.licenseFingerprint === licenseFingerprint
    ) {
      const existingValidation = await validateLicenseKey(licenseKey, existingDevice.instanceId);
      const existingMatch = entitlementMatches(existingValidation, email);
      if (existingMatch.ok && existingValidation.instance?.id === existingDevice.instanceId) {
        instanceId = existingDevice.instanceId;
      }
    }

    if (!instanceId) {
      const activation = await activateLicenseKey(licenseKey);
      const activationMatch = entitlementMatches(activation, email);
      if (!activationMatch.ok || !activation.instance?.id || !activation.license_key?.id) {
        return NextResponse.json(
          { ok: false, message: "The license is valid, but this browser could not be activated." },
          { status: 409 }
        );
      }
      instanceId = activation.instance.id;
    }

    const session = newPremiumSession({
      licenseKeyId,
      instanceId,
      licenseKey,
      customerEmail: email
    });
    const device = newPremiumDeviceRef({ licenseKeyId, instanceId, licenseKey });

    const response = NextResponse.json({ ok: true, redirect: nextPath });
    response.cookies.set(
      VERLUNE_SESSION_COOKIE,
      signPremiumSession(session),
      premiumCookieOptions(session)
    );
    response.cookies.set(
      VERLUNE_DEVICE_COOKIE,
      signPremiumDeviceRef(device),
      premiumDeviceCookieOptions()
    );
    return response;
  } catch (error) {
    if (error instanceof LemonLicenseApiError) {
      const isClientRejectedValidation =
        error.operation === "validate" &&
        error.status >= 400 &&
        error.status < 500 &&
        error.status !== 429;

      if (isClientRejectedValidation) {
        return NextResponse.json(
          { ok: false, message: "That license and email do not match an active Verlune Premium purchase." },
          { status: 401 }
        );
      }

      if (error.operation === "activate") {
        return NextResponse.json(
          { ok: false, message: "This license could not activate another browser. Deactivate an old browser or check the activation limit." },
          { status: 409 }
        );
      }
    }

    return NextResponse.json(
      { ok: false, message: "Premium access could not be verified right now. Please try again." },
      { status: 502 }
    );
  }
}
