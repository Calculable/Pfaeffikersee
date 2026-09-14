"""One-time public-source importer. Do not rerun over manually edited content."""
from pathlib import Path
from source_html import parse,Node
from html import escape
from urllib.parse import urlsplit,unquote,urljoin
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'migration/source'; DEST=ROOT/'src/content/pages'
MANIFEST=ROOT/'migration/assets.json'
assets=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
def norm(s):return re.sub(r'\s+',' ',s or '').strip()
def local_asset(url):
 if not url:return ''
 if url.startswith('//'):url='https:'+url
 url=url.replace('http://static1.squarespace.com','https://static1.squarespace.com')
 if not any(s in urlsplit(url).netloc for s in ['squarespace','sqspcdn']):return url
 url=url.split('?')[0]
 if url not in assets:
  name=unquote(urlsplit(url).path.split('/')[-1]).replace('+','-')
  name=re.sub('[^a-zA-Z0-9._-]+','-',name).strip('-').lower()
  assets[url]='/media/'+hashlib.sha256(url.encode()).hexdigest()[:10]+'-'+name
 return assets[url]
def href(u):
 if not u:return ''
 u=u.strip()
 if u.startswith('/s/'):return local_asset('https://www.pfäffikersee.org'+u)
 if any(s in urlsplit(u).netloc for s in ['squarespace-cdn','static1.squarespace']):return local_asset(u)
 for host in ['https://www.pfäffikersee.org','http://www.pfäffikersee.org','https://pfäffikersee.org','https://triangle-roadrunner-8jz9.squarespace.com']:
  if u.startswith(host):return u[len(host):] or '/'
 return u

def inline(n):
 if not n.tag:return escape(re.sub(r'\s+',' ',n.data))
 if n.tag in ('style','script','noscript'):return ''
 s=''.join(inline(c) for c in n.children)
 if n.tag=='br':return '<br>'
 if n.tag=='a':
  u=href(n.attrs.get('href',''))
  return f'<a href="{escape(u,quote=True)}">{s}</a>' if u else s
 if n.tag in ('strong','b','em','i','code','sup','sub','s','u'):return f'<{n.tag}>{s}</{n.tag}>'
 return s

def text_md(n):
 if not n.tag:return '' if not n.data.strip() else inline(n)
 if n.tag in ('style','script','noscript'):return ''
 if n.tag in ['p','h1','h2','h3','h4','h5','h6','blockquote','li']:
  s=inline(n).strip()
  if not s or not norm(n.text()):return ''
  if n.tag.startswith('h') and len(n.tag)==2:return '\n\n'+'#'*int(n.tag[1])+' '+s+'\n\n'
  if n.tag=='li':return '- '+s+'\n'
  if n.tag=='blockquote':return '\n\n> '+s+'\n\n'
  return '\n\n'+s+'\n\n'
 if n.tag=='hr':return '\n\n---\n\n'
 return ''.join(text_md(c) for c in n.children)

def image_html(n):
 u=local_asset(n.attrs.get('data-src') or n.attrs.get('src',''))
 dim=n.attrs.get('data-image-dimensions','').split('x')
 w=n.attrs.get('width',dim[0] if len(dim)==2 else '')
 h=n.attrs.get('height',dim[1] if len(dim)==2 else '')
 return f'<img src="{escape(u,quote=True)}" alt="{escape(n.attrs.get("alt", ""),quote=True)}"'+(f' width="{w}" height="{h}"' if str(w).isdigit() and str(h).isdigit() else '')+' loading="lazy" decoding="async">'

def figure(n):
 imgs=n.all(lambda c:c.tag=='img' and c.parent.tag!='noscript')
 if not imgs:return ''
 im=image_html(imgs[0]);cap=n.all(lambda c:c.tag=='figcaption' or c.has('image-caption'))
 links=n.all(lambda c:c.tag=='a' and c.attrs.get('href'))
 if links and not cap:im=f'<a href="{escape(href(links[0].attrs["href"]),quote=True)}">{im}</a>'
 caption=''
 if cap:
  # Plain semantic HTML is intentionally used for image captions and project cards.
  def simple(c):
   if c.tag in ('p','h1','h2','h3','h4'):return '<'+c.tag+'>'+inline(c).strip()+'</'+c.tag+'>'
   if c.tag=='a':return inline(c)
   if c.tag in ('style','script'):return ''
   return ''.join(simple(x) for x in c.children) if c.tag else (escape(norm(c.data)) if c.data.strip() else '')
  caption='<figcaption>'+simple(cap[0])+'</figcaption>'
 cls='project-card' if n.has('design-layout-card') else 'content-figure'
 return f'\n\n<figure class="{cls}">\n{im}\n{caption}\n</figure>\n\n'

def embeds(n):
 result=[]
 for c in n.all(lambda c:c.tag=='iframe'):
  u=c.attrs.get('src','');title=c.attrs.get('title') or 'Video'
  result.append(f'<iframe class="video-embed" src="{escape(u,quote=True)}" title="{escape(title,quote=True)}" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe>')
 for c in n.all(lambda c:'data-html' in c.attrs):result.append(embeds(parse(c.attrs['data-html'])))
 for c in n.all(lambda c:'data-config-video' in c.attrs):
  d=json.loads(c.attrs['data-config-video']);u=d['alexandriaUrl'].replace('{variant}','mp4')
  result.append(f'<video controls playsinline preload="metadata" src="{local_asset(u)}" aria-label="Video"></video>')
 return '\n\n'+'\n\n'.join(result)+'\n\n'

def form(n):
 return '\n\n<!-- CONTACT_FORM -->\n\n'

def block(n):
 typ=n.attrs.get('data-definition-name',n.attrs.get('data-block-type'))
 if typ=='website.components.spacer':return ''
 if typ=='website.components.html':return ''.join(text_md(c) for c in n.all(lambda c:c.has('sqs-html-content')))
 if typ=='website.components.horizontalrule':return '\n\n---\n\n'
 if typ=='5':
  fs=n.all(lambda c:c.tag=='figure');return ''.join(figure(c) for c in fs) if fs else figure(n)
 if typ=='website.components.button':
  return '\n\n'+''.join('<p class="button-link">'+inline(c)+'</p>' for c in n.all(lambda c:c.tag=='a'))+'\n\n'
 if typ in ('website.components.video','website.components.embed','website.components.code'):return embeds(n)+''.join(text_md(c) for c in n.all(lambda c:c.tag=='p'))
 if typ=='website.components.map':
  d=json.loads(n.all(lambda c:'data-context' in c.attrs)[0].attrs['data-context'])['location'];lat=d.get('markerLat',d['mapLat']);lng=d.get('markerLng',d['mapLng'])
  u=f'https://www.openstreetmap.org/export/embed.html?bbox={lng-.045}%2C{lat-.025}%2C{lng+.045}%2C{lat+.025}&layer=mapnik&marker={lat}%2C{lng}'
  return f'\n\n<iframe class="map-embed" title="Karte: {escape(d.get("addressTitle",d.get("addressLine1","Ort")),quote=True)}" src="{escape(u,quote=True)}" loading="lazy"></iframe>\n<p><a href="https://www.openstreetmap.org/?mlat={lat}&amp;mlon={lng}#map=13/{lat}/{lng}">Karte öffnen</a></p>\n\n'
 if typ=='website.components.form':return form(n)
 if typ=='website.components.quote':
  return text_md(n)+'\n\n'+''.join(inline(c) for c in n.all(lambda c:c.tag=='figcaption'))+'\n\n'
 if typ=='62':
  cfg=n.all(lambda c:'data-settings' in c.attrs)[0]
  d=json.loads(cfg.attrs['data-settings']); t=d['dataTable']
  return '\n\n'+d.get('caption','')+'\n\n| Fläche | Anteil |\n| --- | ---: |\n'+''.join('| '+label+' | '+str(row[0]).replace('.',',')+' % |\n' for label,row in zip(t['sampleLabels'],t['data']))+'\n'
 if typ=='8':return '\n\n<div class="image-grid">\n'+''.join(figure(c) for c in n.all(lambda c:c.has('slide')))+'</div>\n\n'
 raise ValueError('Unimplemented block '+str(typ))

def walk(n):
 if n.has('sqs-block'):return block(n)
 if n.tag in ('script','style','noscript'):return ''
 if n.tag=='figure':return figure(n)
 if n.has('section-background'):
  imgs=n.all(lambda c:c.tag=='img');return '\n\n'+image_html(imgs[0])+'\n\n' if imgs else ''
 if n.has('blog-item-title'):return '\n\n# '+inline(n).strip()+'\n\n'
 if n.has('blog-item-meta-wrapper'):return '\n\n'+norm(n.text())+'\n\n'
 if n.has('blog-item-author-profile-wrapper'):return ''
 if n.has('item-pagination'):
  return '\n\n<nav class="page-pagination">'+''.join('<a href="'+escape(href(a.attrs['href']),quote=True)+'">'+norm(a.text()).replace('Weiter Weiter','Weiter').replace('Zurück Zurück','Zurück')+'</a>' for a in n.all(lambda c:c.tag=='a' and 'href' in c.attrs))+'</nav>\n\n'
 s=''.join(walk(c) for c in n.children)
 if n.tag=='section' and n.attrs.get('data-section-id'):
  sid=n.attrs['data-section-id'];s=f'\n\n<span id="page-section-{sid}"></span>\n\n'+s
 return s

def migrate(name):
 p=SOURCE/(name+'.html');r=parse(p.read_text());main=r.all(lambda c:c.tag=='main')[0]
 metas=[n.attrs for n in r.all(lambda c:c.tag=='meta') if n.attrs.get('name') in ['description','robots','author','keywords'] or n.attrs.get('property','').startswith('og:') or n.attrs.get('name','').startswith('twitter:') or n.attrs.get('itemprop')]
 title=r.all(lambda c:c.tag=='title')[0].text()
 route='/' if name=='home' else '/'+name.replace('__','/')
 meta={'title':title,'source': 'https://www.pfäffikersee.org'+route,'path':route,'seo':metas}
 for m in metas:
  if m.get('property')=='og:image' or m.get('name')=='twitter:image' or m.get('itemprop') in ['thumbnailUrl','image']:m['content']=local_asset(m['content'])
 body=walk(main)
 body=re.sub(r'\n{3,}','\n\n',body).strip()+'\n'
 out=DEST/(name.replace('__','/')+'.md');out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():raise RuntimeError('Refusing overwrite '+str(out))
 out.write_text('---\n'+json.dumps(meta,ensure_ascii=False,indent=2)+'\n---\n\n'+body)
 MANIFEST.write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
 print('Imported',route,'→',out.relative_to(ROOT))
if __name__=='__main__':
 for name in sys.argv[1:]:migrate(name)
