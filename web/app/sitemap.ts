import type { MetadataRoute } from "next";

import { FREE_ASSETS } from "@/lib/verlune-free-catalog";

export default function sitemap(): MetadataRoute.Sitemap {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL?.trim();
  const indexingLive = process.env.NEXT_PUBLIC_INDEXING_MODE === "live";

  if (!siteUrl || !indexingLive) return [];

  const base = siteUrl.replace(/\/$/, "");
  const routes = [
    "/",
    "/free",
    "/premium",
    "/learn",
    "/learn/workflows-not-random-prompts",
    "/learn/test-ai-workflows",
    "/code-review",
    "/license"
  ];

  const staticEntries: MetadataRoute.Sitemap = routes.map((route) => ({
    url: `${base}${route}`,
    changeFrequency: route === "/" ? "weekly" : "monthly",
    priority: route === "/" ? 1 : route === "/free" || route === "/premium" ? 0.9 : 0.7
  }));

  const freeAssets: MetadataRoute.Sitemap = FREE_ASSETS.map((asset) => ({
    url: `${base}/free/asset/${encodeURIComponent(asset.id)}`,
    changeFrequency: "monthly",
    priority: 0.65
  }));

  return [...staticEntries, ...freeAssets];
}
