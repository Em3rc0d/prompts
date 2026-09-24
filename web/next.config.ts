import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  outputFileTracingIncludes: {
    "/app/**": ["./.verlune-private/**/*"],
    "/api/verlune/**": ["./.verlune-private/**/*"]
  },
  async redirects() {
    return [
      { source: "/starter-collection", destination: "/code-review", permanent: true },
      { source: "/developer-pack", destination: "/code-review", permanent: true },
      { source: "/free/developer-starter-pack", destination: "/free", permanent: true },
      { source: "/collections", destination: "/code-review", permanent: true },
    ];
  },
};

export default nextConfig;
