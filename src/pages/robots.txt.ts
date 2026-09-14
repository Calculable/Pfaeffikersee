import {site} from '../site';
export function GET() {
 return new Response(`User-agent: *
Allow: /
${site.indexable ? `Sitemap: ${new URL('/sitemap.xml',site.url).href}
` : ''}`,{headers:{'Content-Type':'text/plain; charset=utf-8'}});
}
