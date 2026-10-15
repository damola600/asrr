import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  async rewrites() {
    return [
      {
        source: "/backend/:path*",
        destination:
          "https://asrr.onrender.com/:path*",
      },
    ];
  },

};

export default nextConfig;
