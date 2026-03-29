/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
  trailingSlash: true,
  compress: true,
  experimental: {
    turbopack: false,
  },
};
module.exports = nextConfig;
