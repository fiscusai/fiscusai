import withPWA from 'next-pwa'
const isProd = process.env.NODE_ENV === 'production'
const pwa = withPWA({ dest:'public', disable: !isProd })
export default pwa({ experimental:{ appDir:true } })
