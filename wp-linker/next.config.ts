import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Disable Turbopack for build (Next.js 16 uses it by default).
     turbopack.root workaround for Japanese path issue. */
  turbopack: {
    root: "C:\\tmp\\wp-linker",
  },
};

export default nextConfig;
