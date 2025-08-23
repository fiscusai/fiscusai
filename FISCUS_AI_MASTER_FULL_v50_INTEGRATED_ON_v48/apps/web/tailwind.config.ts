import type { Config } from 'tailwindcss'
const config: Config = { content:["./app/**/*.{ts,tsx}","./components/**/*.{ts,tsx}"], theme:{ extend:{
  colors:{ mermer:"#F2F2F0", altin:"#C9A54A", fiscus:"#2D2D2D", kirmizi:"#7A1F1F", zeytin:"#6E6B5E" },
  fontFamily:{ display:["Cinzel","serif"], body:["Inter","ui-sans-serif","system-ui"] }
}} , plugins:[] }
export default config
