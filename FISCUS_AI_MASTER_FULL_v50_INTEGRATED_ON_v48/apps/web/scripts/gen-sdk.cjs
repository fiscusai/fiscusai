const fs = require('fs'); const path = require('path');
const OUT = path.join(__dirname, '..', 'lib', 'sdk.gen.ts');
const api = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
const content = `// Auto-generated minimal SDK\nexport const API = '${'${api}'}' as string;\n`;
fs.writeFileSync(OUT, content); console.log('SDK updated:', OUT);
