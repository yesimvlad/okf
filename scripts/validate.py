#!/usr/bin/env python3
"""Validate the Yesim authoring profile; this is not a full OKF conformance tool."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml

LINK = re.compile(r'\[[^\]\n]+\]\(([^)\n]+)\)')
ACTOR = re.compile(r'^(?:human:|process:).+|^[^/\s]+/[^\s]+$')
SKIP = {'.git', '.venv', '__pycache__', 'dist'}

class UniqueKeyLoader(yaml.SafeLoader):
    """Reject silently overwritten metadata instead of approving ambiguous YAML."""

def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f'duplicate YAML key: {key}')
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping

UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def timestamp(value):
    if not isinstance(value, (str, datetime)):
        raise ValueError('expected an ISO 8601 timestamp')
    dt = value if isinstance(value, datetime) else datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('timestamp requires an explicit UTC offset')
    return dt

def split_document(text):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)', text, re.S)
    if not match:
        return None, text
    meta = yaml.load(match.group(1), Loader=UniqueKeyLoader)
    if not isinstance(meta, dict):
        raise ValueError('frontmatter must be a YAML mapping')
    return meta, match.group(2)

def markdown_files(root):
    return sorted(p for p in root.rglob('*.md') if not SKIP.intersection(p.relative_to(root).parts))

def link_target(root, source, value):
    target = value.strip().split(' "', 1)[0].strip('<>')
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    resolved = (root / path.lstrip('/') if path.startswith('/') else source.parent / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError('link escapes bundle root')
    return resolved

def inspect(root, now=None):
    root = root.resolve()
    now = now or datetime.now(timezone.utc)
    errors, warnings, records = [], [], {}
    record_ids = {}
    root_index = root/'index.md'
    if not root_index.exists():
        errors.append('index.md: missing bundle index')
    else:
        try:
            meta, _ = split_document(root_index.read_text())
            if not meta or str(meta.get('okf_version')) != '0.2':
                errors.append('index.md: expected okf_version 0.2')
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f'index.md: {exc}')

    for p in markdown_files(root):
        rel = p.relative_to(root).as_posix()
        text = p.read_text(encoding='utf-8')
        if not text.strip():
            errors.append(f'{rel}: empty document')
            continue
        try:
            meta, body = split_document(text)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f'{rel}: invalid YAML: {exc}')
            continue
        exempt = p.name in {'index.md','log.md','README.md'} or rel.startswith('docs/')
        if not exempt:
            if meta is None:
                errors.append(f'{rel}: missing concept frontmatter')
            else:
                for key in ('type','title','description','sources','generated','status','audience'):
                    if key not in meta:
                        errors.append(f'{rel}: missing publishing-profile field {key}')
                for key in ('type','title','description'):
                    if key in meta and (not isinstance(meta[key],str) or not meta[key].strip()):
                        errors.append(f'{rel}: {key} must be a nonempty string')
                if meta.get('id'):
                    key = meta['id']
                    if not isinstance(key,str): errors.append(f'{rel}: id must be a string')
                    elif key in record_ids: errors.append(f'{rel}: duplicate record id also in {record_ids[key]}')
                    else: record_ids[key] = rel
                if meta.get('status') not in {'draft','stable','deprecated'}:
                    errors.append(f'{rel}: invalid status')
                if meta.get('audience') not in {'public','internal-editorial','reference'}:
                    errors.append(f'{rel}: invalid audience')
                source_ids = set()
                sources = meta.get('sources')
                if not isinstance(sources,list) or not sources:
                    errors.append(f'{rel}: sources must be a nonempty list')
                    sources = []
                for item in sources:
                    if not isinstance(item,dict) or not isinstance(item.get('resource'),str) or not item['resource']:
                        errors.append(f'{rel}: each source needs resource')
                        continue
                    key = item.get('id')
                    if key:
                        if key in source_ids:
                            errors.append(f'{rel}: duplicate source ID {key}')
                        source_ids.add(key)
                    try:
                        target = link_target(root,p,item['resource'])
                        if target is not None and not target.exists():
                            errors.append(f'{rel}: missing source artifact {item["resource"]}')
                    except ValueError as exc:
                        errors.append(f'{rel}: source: {exc}')
                generated = meta.get('generated')
                if not isinstance(generated,dict) or not ACTOR.fullmatch(str(generated.get('by',''))):
                    errors.append(f'{rel}: generated.by requires an actor')
                else:
                    try: timestamp(generated.get('at'))
                    except (ValueError,TypeError) as exc: errors.append(f'{rel}: generated.at: {exc}')
                verified = meta.get('verified',[])
                if isinstance(verified,dict): verified = [verified]
                if not isinstance(verified,list):
                    errors.append(f'{rel}: verified must be a mapping or list')
                    verified = []
                for event in verified:
                    if not isinstance(event,dict) or not ACTOR.fullmatch(str(event.get('by',''))):
                        errors.append(f'{rel}: invalid verification actor')
                        continue
                    try: timestamp(event.get('at'))
                    except (ValueError,TypeError) as exc: errors.append(f'{rel}: verified.at: {exc}')
                if meta.get('status') == 'stable' and meta.get('audience') == 'public':
                    if not verified: errors.append(f'{rel}: public stable record requires actual verification')
                    if not meta.get('stale_after'): errors.append(f'{rel}: public stable record requires recheck deadline')
                    if meta.get('review_required'): errors.append(f'{rel}: stable record still requires review')
                if meta.get('stale_after'):
                    try:
                        if timestamp(meta['stale_after']) <= now: warnings.append(f'{rel}: stale; excluded from consumer export')
                    except (ValueError,TypeError) as exc: errors.append(f'{rel}: stale_after: {exc}')
                if meta.get('status') == 'draft': warnings.append(f'{rel}: draft; excluded from consumer export')
                footnote_body = '' if rel == 'spec.md' else re.sub(r'```.*?```','',body,flags=re.S)
                for label in set(re.findall(r'\[\^([^\]]+)\]',footnote_body)):
                    if label not in source_ids: errors.append(f'{rel}: footnote {label} has no sources[].id')
                    if not re.search(r'^\[\^'+re.escape(label)+r'\]:',body,re.M):
                        errors.append(f'{rel}: missing footnote definition {label}')
                records[rel] = (meta,body)
        # Specification examples refer to sample data outside this bundle.
        if rel == 'spec.md': continue
        clean = re.sub(r'```.*?```','',body,flags=re.S)
        clean = re.sub(r'`[^`\n]+`','',clean)
        for value in LINK.findall(clean):
            try:
                target = link_target(root,p,value)
                if target is not None and not target.exists(): errors.append(f'{rel}: broken link {value}')
            except ValueError as exc: errors.append(f'{rel}: {value}: {exc}')
    # Authored evaluation cases are checked structurally, never reported as executed runs.
    case_ids = set()
    for p in sorted((root/'evaluations').glob('*cases.yaml')):
        rel=p.relative_to(root).as_posix()
        try:
            data=yaml.load(p.read_text(encoding='utf-8'),Loader=UniqueKeyLoader)
            if not isinstance(data,dict) or not isinstance(data.get('cases'),list):
                raise ValueError('expected a mapping with cases list')
            for item in data['cases']:
                if not isinstance(item,dict): raise ValueError('case must be a mapping')
                for field in ('id','prompt','expected'):
                    if not isinstance(item.get(field),str) or not item[field].strip():
                        errors.append(f'{rel}: each case needs nonempty {field}')
                key=item.get('id')
                if isinstance(key,str):
                    if key in case_ids: errors.append(f'{rel}: duplicate evaluation id {key}')
                    case_ids.add(key)
                if not isinstance(item.get('critical'),bool):errors.append(f'{rel}: case {key} needs boolean critical')
                urls=item.get('sources')
                if not isinstance(urls,list) or not urls or any(not isinstance(u,str) or urlsplit(u).scheme not in {'http','https'} for u in urls):
                    errors.append(f'{rel}: case {key} needs official source URLs')
                if item.get('knowledge_record'):
                    target=link_target(root,root/'index.md',item['knowledge_record'])
                    if target is None or not target.exists(): errors.append(f'{rel}: case {key} has missing knowledge record')
        except (ValueError,TypeError,yaml.YAMLError) as exc:errors.append(f'{rel}: {exc}')
    return errors, warnings, records

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--now',help='ISO 8601 time for reproducible freshness checks')
    args = parser.parse_args()
    errors,warnings,records = inspect(args.root,timestamp(args.now) if args.now else None)
    for item in errors: print('ERROR:',item)
    print(f'Validated {len(records)} concepts; {len(errors)} errors; {len(warnings)} draft/staleness notices.')
    return 1 if errors else 0

if __name__ == '__main__': sys.exit(main())
