import { NextRequest, NextResponse } from "next/server";

import {
  clearPremiumCookieOptions,
  VERLUNE_SESSION_COOKIE
} from "@/lib/verlune-session";

export async function POST(request: NextRequest) {
  const response = NextResponse.redirect(new URL("/unlock?reason=logged-out", request.url), 303);
  response.cookies.set(VERLUNE_SESSION_COOKIE, "", clearPremiumCookieOptions);
  return response;
}
