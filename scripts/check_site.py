#!/usr/bin/env python3
"""Check a built site; --remote additionally checks its actual public deployment."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set();self.canonical=[];self.alternates={};self.lang=None;self.h1=0;self.noindex=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        if tag=='link' and a.get('hreflang'):self.alternates[a['hreflang']]=a.get('href')
        if tag=='meta' and a.get('name','').lower()=='robots' and 'noindex' in a.get('content','').lower():self.noindex=True

def check_local(root):
    root=root.resolve();manifest=json.loads((root/'manifest.json').read_text());base=manifest['base_url'];errors=[];pages={}
    expected={'index.html':base}
    expected.update({str(Path(r['path']).with_suffix('.html')):r['html_url'] for r in manifest['records']})
    for rel,url in expected.items():
        p=root/rel;doc=Page();doc.feed(p.read_text());pages[rel]=doc
        if doc.canonical!=[url]:errors.append(f'{rel}: canonical mismatch')
        if doc.h1!=1:errors.append(f'{rel}: expected one visible H1')
        if doc.noindex:errors.append(f'{rel}: unexpected noindex')
    for rel,doc in pages.items():
        for href in doc.links:
            u=urlsplit(href)
            if u.scheme or u.netloc:continue
            path=(root/rel).parent/unquote(u.path) if u.path else root/rel
            path=path.resolve()
            if not path.is_relative_to(root):errors.append(f'{rel}: link escapes release: {href}');continue
            if not path.exists():errors.append(f'{rel}: missing link: {href}');continue
            dest=pages.get(str(path.relative_to(root)))
            if dest and u.fragment and unquote(u.fragment) not in dest.ids:errors.append(f'{rel}: missing anchor: {href}')
        for lang,url in doc.alternates.items():
            if not url.startswith(base):errors.append(f'{rel}: alternate outside release: {url}');continue
            target=url[len(base):];other=pages.get(target)
            if not other:errors.append(f'{rel}: missing alternate: {url}');continue
            if lang!='x-default' and other.lang.lower()!=lang.lower():errors.append(f'{rel}: alternate language mismatch')
            if lang!='x-default' and other.alternates.get(doc.lang)!=expected[rel]:errors.append(f'{rel}: nonreciprocal alternate')
    return errors,manifest,len(pages)

def request(url):
    result={'url':url}
    try:
        with urlopen(Request(url,headers={'User-Agent':'Yesim-knowledge-verification/1.0'}),timeout=20) as r:
            data=r.read();result.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type',''),x_robots_tag=r.headers.get('X-Robots-Tag',''))
        result['body']=data.decode('utf-8')
    except (HTTPError,URLError,TimeoutError,UnicodeError) as e:
        result.update(status=getattr(e,'code',None),error=str(e))
    return result

def check_remote(manifest):
    base=manifest['base_url'];primary=base+'markets/en.html';preflight=request(primary)
    if preflight.get('status')!=200:return [f'{primary}: HTTP {preflight.get("status")}; deployment not verified'],[preflight]
    checks=[(base,'text/html'),(base+'llms.txt','text/plain'),(base+'markets/en.md','text/'),(base+'manifest.json','application/json'),(base+'sitemap.xml','xml')]
    checks.extend((r['html_url'],'text/html') for r in manifest['records'])
    origin=urlsplit(base);checks.append((f'{origin.scheme}://{origin.netloc}/robots.txt','text/plain'))
    errors=[];results=[]
    with ThreadPoolExecutor(max_workers=8) as pool:
        for (url,mime),result in zip(checks,pool.map(request,[x[0] for x in checks])):
            if result.get('status')!=200:errors.append(f'{url}: HTTP {result.get("status")}')
            elif mime not in result.get('content_type',''):errors.append(f'{url}: unexpected MIME {result.get("content_type")}')
            elif mime=='text/html' and 'noindex' in result.get('x_robots_tag','').lower():errors.append(f'{url}: X-Robots-Tag noindex')
            if result.get('status')==200 and mime=='text/html':
                page=Page();page.feed(result['body'])
                if page.canonical!=[url]:errors.append(f'{url}: live canonical mismatch')
                if page.h1!=1 or page.noindex:errors.append(f'{url}: live heading/indexability mismatch')
            # Robots/CDN rules and genuine crawler access still require separate monitoring.
            if url.endswith('/robots.txt'):result['robots_text']=result.get('body')
            result.pop('body',None);results.append(result)
    return errors,results

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('release',type=Path);parser.add_argument('--remote',action='store_true');parser.add_argument('--report',type=Path);args=parser.parse_args()
    errors,manifest,count=check_local(args.release);local_ok=not errors;remote=[]
    if args.remote and not errors:
        remote_errors,remote=check_remote(manifest);errors.extend(remote_errors)
    report={'html_pages':count,'local_checks':'passed' if local_ok else 'see errors','remote_requested':args.remote,'errors':errors,'remote':remote}
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'html_pages':count,'errors':errors,'remote_requested':args.remote},ensure_ascii=False))
    return bool(errors)

if __name__=='__main__':raise SystemExit(main())
