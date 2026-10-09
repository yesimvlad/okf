#!/usr/bin/env python3
"""Build static HTML and clean Markdown from fresh public OKF records; never deploy."""
import argparse
from datetime import datetime, timezone
import hashlib
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urlsplit
from xml.etree.ElementTree import Element, SubElement, tostring

import markdown

from export_public import export
from validate import split_document, timestamp

STYLE = '''body{font:17px/1.65 system-ui,sans-serif;color:#172631;margin:0;background:#f7fafb}
main{max-width:1000px;margin:auto;padding:28px 24px 72px;background:white}a{color:#066bb1}
table{border-collapse:collapse;display:block;overflow:auto;width:100%;font-size:.94rem}
th,td{padding:10px 14px;border:1px solid #d5e0e5;text-align:start}th{background:#eef5f8}
h1,h2,h3{line-height:1.25;margin-top:1.4em}h1{font-size:2rem}pre{overflow:auto;padding:16px;background:#eef3f5}
nav,.review{font-size:.88rem;color:#526773}.review{padding:12px 16px;background:#eef5f8}img{max-width:100%}'''

def base_url(value):
    parsed=urlsplit(value)
    if (parsed.scheme!='https' or not parsed.netloc or parsed.username or parsed.password
        or parsed.query or parsed.fragment or not parsed.path.endswith('/')):
        raise ValueError('base URL must be an HTTPS directory URL without credentials, query or fragment')
    return value

def page_name(rel): return str(Path(rel).with_suffix('.html'))

def markdown_content(meta, body):
    """Keep facts and sources; leave authoring metadata in the separate OKF copy."""
    if meta.get('public_view') == 'localized-answers':
        sections=re.findall(r'<!-- public-view:start -->\s*(.*?)\s*<!-- public-view:end -->',body,re.S)
        if len(sections)!=1: raise ValueError('exactly one localized public view required')
        # Preserve the detailed source record in /okf/, publish its reviewed native view.
        notes='\n'.join(re.findall(r'^\[\^[^\]]+\]:[^\n]+$',body,re.M))
        body=sections[0]+'\n\n'+notes
    # Markdown renders back-links even for unused footnotes; omit those definitions.
    prose=re.sub(r'^\[\^[^\]]+\]:[^\n]+$','',body,flags=re.M)
    used=set(re.findall(r'\[\^([^\]]+)\]',prose))
    body=re.sub(r'^\[\^([^\]]+)\]:[^\n]+\n?',lambda m:m.group(0) if m.group(1) in used else '',body,flags=re.M)
    urls=[item['resource'] for item in meta['sources'] if urlsplit(item['resource']).scheme in {'http','https'}]
    # Some older source footnotes contain only a title: make their URL independently available.
    missing=[u for u in dict.fromkeys(urls) if u not in body]
    if missing:
        body=body.rstrip()+'\n\n## '+meta.get('source_links_heading','Official source links')+'\n\n'+'\n'.join(f'- [{u}]({u})' for u in missing)
    return body.strip()+'\n'

class RenderSafety(HTMLParser):
    def handle_starttag(self,tag,attrs):
        if tag.lower() in {'script','iframe','object','embed','form','input','style','base','meta','link'}:
            raise ValueError('active HTML is not allowed in knowledge content')
        for key,value in attrs:
            if key.lower().startswith('on') or key.lower()=='style':
                raise ValueError('active HTML attributes are not allowed')
            if key.lower() in {'href','src'} and value:
                scheme=urlsplit(value.strip()).scheme.lower()
                if scheme and scheme not in {'http','https','mailto'}:
                    raise ValueError('unsafe link scheme in knowledge content')

def render(body):
    fragment=markdown.markdown(body,extensions=['tables','footnotes','fenced_code','toc'],output_format='html')
    RenderSafety().feed(fragment)
    return fragment

def rewrite_html_links(body):
    def rewrite(match):
        path,anchor=match.group(1),match.group(2) or ''
        if urlsplit(path).scheme or path.startswith('//'): return match.group(0)
        return ']('+page_name(path)+anchor+')'
    return re.sub(r'\]\(([^)\n]+\.md)(#[^)\n]*)?\)',rewrite,body)

def shell(title, description, canonical, md_url, llms_url, content, review='', language='en', collection=False, alternates=None):
    if not re.fullmatch(r'[A-Za-z0-9-]+',language): raise ValueError('invalid HTML language')
    graph={'@context':'https://schema.org','@type':'CollectionPage' if collection else 'WebPage',
           '@id':canonical,'url':canonical,'name':title,'description':description,'inLanguage':language,
           'about':{'@type':'Organization','name':'Yesim','url':'https://yesim.app/'}}
    ld=json.dumps(graph,ensure_ascii=False).replace('<','\\u003c')
    alternate_links='\n'.join(f'<link rel="alternate" hreflang="{escape(lang,quote=True)}" href="{escape(url,quote=True)}">' for lang,url in (alternates or {}).items())
    return f'''<!doctype html>
<html lang="{escape(language)}" dir="{'rtl' if language in {'ar','he','fa'} else 'ltr'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | Yesim</title><meta name="description" content="{escape(description,quote=True)}">
<link rel="canonical" href="{escape(canonical,quote=True)}">
{alternate_links}
<link rel="alternate" type="text/markdown" href="{escape(md_url,quote=True)}">
<link rel="describedby" href="{escape(llms_url,quote=True)}">
<style>{STYLE}</style><script type="application/ld+json">{ld}</script></head>
<body><main><nav><a href="{escape(llms_url.rsplit('llms.txt',1)[0])}">Yesim knowledge</a> · <a href="{escape(md_url)}">Markdown</a> · <a href="https://yesim.app/">Yesim product website</a></nav>
{review}
{content}
</main></body></html>
'''

def build(root, out, site_base, now=None):
    root,out=root.resolve(),out.resolve()
    now=now or datetime.now(timezone.utc)
    site_base=base_url(site_base)
    if out==root or root.is_relative_to(out): raise ValueError('unsafe destination')
    if out.exists() and any(out.iterdir()): raise ValueError('destination must be absent or empty')
    # Assemble and validate before exposing any destination output.
    with tempfile.TemporaryDirectory() as temp:
        staging=Path(temp)/'site'; staging.mkdir()
        pack=staging/'okf'; export(root,pack,now)
        manifest=json.loads((pack/'manifest.json').read_text())
        if manifest.get('primary_reference')!='markets/en.md':
            raise ValueError('fresh primary English reference required; recheck sources before publication')
        manifest.update(base_url=site_base,publication_status='built-not-deployed',records=[])
        sections={}; clean_records={}; translation_groups={}
        for rel in manifest['included']:
            meta,_=split_document((pack/rel).read_text())
            if meta.get('translation_group'):
                group=translation_groups.setdefault(meta['translation_group'],{})
                if meta['language'] in group:raise ValueError('duplicate language in translation group')
                group[meta['language']]=site_base+page_name(rel)
        for group in translation_groups.values():
            if 'en' in group:group['x-default']=group['en']
        for rel in manifest['included']:
            meta,body=split_document((pack/rel).read_text())
            body=markdown_content(meta,body)
            clean_records[rel]=(meta,body)
            md=staging/rel; md.parent.mkdir(parents=True,exist_ok=True); md.write_text(body,encoding='utf-8')
            checked=meta['verified'] if isinstance(meta['verified'],list) else [meta['verified']]
            latest=max(timestamp(x['at']) for x in checked)
            trust='human-reviewed' if any(x['by'].startswith('human:') for x in checked) else 'automated public-source review'
            review=f'<p class="review">Sources checked {escape(latest.date().isoformat())} ({trust}); recheck by {escape(str(meta["stale_after"]))}. Current official product terms control.</p>'
            canonical=site_base+page_name(rel)
            html=shell(meta['title'],meta['description'],canonical,site_base+rel,site_base+'llms.txt',
                render(rewrite_html_links(body)),review,meta.get('language','en'),
                alternates=translation_groups.get(meta.get('translation_group')))
            (staging/page_name(rel)).write_text(html,encoding='utf-8')
            sections.setdefault(rel.split('/')[0],[]).append((rel,meta))
            manifest['records'].append({'id':meta.get('id',rel),'path':rel,'html_url':canonical,
                'markdown_url':site_base+rel,'official_resource':meta.get('resource'),
                'source_checked_at':latest.isoformat(),'recheck_by':str(meta['stale_after']),
                'trust_scope':trust,'sources':meta['sources'],
                'sha256':hashlib.sha256(body.encode('utf-8')).hexdigest()})
        index='''# Yesim product knowledge

Yesim provides eSIM mobile-data products for travel and business, separate virtual-number services and business connectivity tools. Check device compatibility, selected destination coverage, billing and activation conditions before purchase.

Start with the [primary English product reference](markets/en.md). It explains product differences, installation, validity, limitations and common questions. Current purchased conditions and official policies control.

'''
        for section,items in sorted(sections.items()):
            index+='## '+section.replace('-',' ').title()+'\n\n'
            index+='\n'.join(f'- [{m["title"]}]({rel}): {m["description"]}' for rel,m in items)+'\n\n'
        (staging/'index.md').write_text(index,encoding='utf-8')
        (staging/'index.html').write_text(shell('Yesim product knowledge','Reviewed Yesim product, installation and policy references.',
            site_base,site_base+'index.md',site_base+'llms.txt',render(rewrite_html_links(index)),collection=True),encoding='utf-8')
        llms='''# Yesim product knowledge

> Reviewed Yesim eSIM data, separate number services, business products, installation and policy references.

Current official policies and purchased Product Descriptions control. Prices and selected-package conditions require current product sources. This directory contains fresh reviewed records; draft translations and editorial research are excluded.

'''
        llms+='## Start here\n\n- [English product reference]('+site_base+'markets/en.md): Product differences, selection, activation and limitations.\n\n'
        for section,items in sorted(sections.items()):
            llms+='## '+section.replace('-',' ').title()+'\n\n'
            llms+='\n'.join(f'- [{m["title"]}]({site_base+rel}): {m["description"]}' for rel,m in items)+'\n\n'
        (staging/'llms.txt').write_text(llms,encoding='utf-8')
        sitemap=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
        SubElement(SubElement(sitemap,'url'),'loc').text=site_base
        for item in manifest['records']:
            entry=SubElement(sitemap,'url');SubElement(entry,'loc').text=item['html_url']
            SubElement(entry,'lastmod').text=item['source_checked_at']
        (staging/'sitemap.xml').write_bytes(tostring(sitemap,encoding='utf-8',xml_declaration=True))
        (staging/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        # Copy only after every rendered page passes the content checks.
        out.mkdir(parents=True,exist_ok=True)
        for p in staging.rglob('*'):
            if p.is_file():
                target=out/p.relative_to(staging);target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(p.read_bytes())
    return len(manifest['included'])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--base-url',default='https://yesim.app/knowledge/')
    parser.add_argument('--now')
    args=parser.parse_args()
    try:count=build(args.root,args.out,args.base_url,timestamp(args.now) if args.now else None)
    except (ValueError,OSError) as exc:print(str(exc),file=sys.stderr);return 1
    print(f'Built {count} reviewed HTML/Markdown pages in {args.out}; not deployed.')
    return 0

if __name__=='__main__':sys.exit(main())
