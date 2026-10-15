import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  async rewrites() {
    return [
      {
        source: "/backend/:path*",
        destination:
          "http://localhost:8000/:path*",
      },
    ];
  },

};

export default nextConfig;
