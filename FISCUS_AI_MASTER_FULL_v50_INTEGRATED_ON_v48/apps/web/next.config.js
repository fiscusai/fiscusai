/** @type {import('next').NextConfig} */
const nextConfig = {
  async headers() {
    return [{
      source: '/(.*)',
      headers: [
        { key: 'Content-Security-Policy', value: `default-src 'self'; script-src 'self' 'unsafe-inline' https://plausible.io https://*.plausible.io; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com 'unsafe-inline'; img-src 'self' https: data: blob: data: blob:; connect-src 'self' https://plausible.io https://*.plausible.io https:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; report-uri /csp-report; report-to csp-endpoint;` },
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' }
      ]
    }];
  },
};

async headers() {
  const base = [{
    source: '/(.*)',
    headers: [
      { key: 'Service-Worker-Allowed', value: '/' }
    ]
  }];
  const prev = await (typeof nextConfig.headers === 'function' ? nextConfig.headers() : []);
  return [...prev, ...base];
},

module.exports = nextConfig;
