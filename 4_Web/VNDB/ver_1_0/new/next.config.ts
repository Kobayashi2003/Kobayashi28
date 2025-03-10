import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: "/api/vndb/:path*",
        destination: `${process.env.VNDB_BASE_URL || "http://localhost:5000"}/:path*`,
      },
      {
        source: "/api/imgserve/:path*",
        destination: `${process.env.IMGSERVE_BASE_URL || "http://localhost:5001"}/:path*`,
      },
      {
        source: "/api/userserve/:path*",
        destination: `${process.env.USERSERVE_BASE_URL || "http://localhost:5002"}/:path*`,
      },
    ]
  }
};

export default nextConfig;
