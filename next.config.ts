import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/wgu-atlas",
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
