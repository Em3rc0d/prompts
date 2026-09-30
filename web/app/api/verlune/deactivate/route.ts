import { NextRequest, NextResponse } from "next/server";

import {
  clearPremiumCookieOptions,
  VERLUNE_DEVICE_COOKIE,
  VERLUNE_SESSION_COOKIE
} from "@/lib/verlune-session";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const response = NextResponse.redirect(new URL("/unlock?reason=deactivated", request.url), 303);
  response.cookies.set(VERLUNE_SESSION_COOKIE, "", clearPremiumCookieOptions);
  response.cookies.set(VERLUNE_DEVICE_COOKIE, "", clearPremiumCookieOptions);
  return response;
}
