import type { NextConfig } from "next";
const buildId =
  process.env.NEXT_PUBLIC_DATADOG_VERSION || `${new Date().getTime()}`;
const cdnPrefix = process.env.NEXT_PUBLIC_CDN_PREFIX + `${buildId}/`;

const nextConfig: NextConfig = {
  /* config options here */
  productionBrowserSourceMaps: true,
  assetPrefix: cdnPrefix.startsWith("https://") ? cdnPrefix : undefined,
  images: {
    domains: ["localhost", "fra1.digitaloceanspaces.com"],
  },
  generateBuildId: async () => {
    return buildId;
  },
  cacheMaxMemorySize: 0,
};

export default nextConfig;
