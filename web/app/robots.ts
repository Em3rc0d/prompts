import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  const indexingLive = process.env.NEXT_PUBLIC_INDEXING_MODE === "live";
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL?.trim();

  if (!indexingLive) {
    return {
      rules: [{ userAgent: "*", disallow: "/" }]
    };
  }

  return {
    rules: [{
      userAgent: "*",
      allow: "/",
      disallow: ["/app", "/unlock", "/api/"]
    }],
    sitemap: siteUrl ? `${siteUrl.replace(/\/$/, "")}/sitemap.xml` : undefined
  };
}
