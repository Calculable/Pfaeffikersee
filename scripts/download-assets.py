"""Download only referenced public assets. Existing files are kept."""
from pathlib import Path
import json,subprocess,concurrent.futures
root=Path(__file__).resolve().parents[1]
assets=json.loads((root/'migration/assets.json').read_text())
def get(item):
 url,rel=item;dest=root/'public'/rel.lstrip('/');dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists() and dest.stat().st_size:return
 proc=subprocess.run(['curl','-L','--fail','--silent','--show-error','--retry','2',url,'-o',str(dest)+'.part'],capture_output=True,text=True)
 if proc.returncode:return url+' '+proc.stderr.strip()
 Path(str(dest)+'.part').replace(dest)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 errors=[x for x in pool.map(get,assets.items()) if x]
print('Assets:',len(assets),'Errors:',len(errors),flush=True)
for e in errors:print(e,flush=True)
raise SystemExit(bool(errors))
