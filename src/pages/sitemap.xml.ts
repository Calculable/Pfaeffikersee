import {site} from '../site';
export function GET() {
 const pages=import.meta.glob('../content/pages/**/index.md',{eager:true});
 const urls=site.indexable ? Object.values(pages).map(page=>`<url><loc>${new URL(page.frontmatter.path,site.url).href}</loc></url>`).join('') : '';
 return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls}</urlset>`,{headers:{'Content-Type':'application/xml'}});
}
