#!/usr/bin/env python3
"""Export a fresh verified public consumer pack; never promote drafts."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

import yaml
from validate import inspect, link_target, timestamp

def eligible(meta, now):
    return (meta.get('audience') == 'public' and meta.get('status') == 'stable'
            and bool(meta.get('verified')) and not meta.get('review_required')
            and bool(meta.get('stale_after')) and timestamp(meta['stale_after']) > now)

def export(root, out, now=None):
    root,out = root.resolve(),out.resolve()
    now = now or datetime.now(timezone.utc)
    errors,_,records = inspect(root,now)
    if errors: raise ValueError('source validation failed: ' + '; '.join(errors))
    if out == root or root.is_relative_to(out): raise ValueError('unsafe export destination')
    if out.exists() and any(out.iterdir()): raise ValueError('destination must be absent or empty')
    selected = {rel:(meta,body) for rel,(meta,body) in records.items() if eligible(meta,now)}
    if not selected: raise ValueError('no fresh verified public concepts to export')
    out.mkdir(parents=True,exist_ok=True)
    for rel,(meta,body) in selected.items():
        source = root/rel
        def rewrite(m):
            label,value = m.group(1),m.group(2)
            target = link_target(root,source,value)
            if target is None: return m.group(0)
            dest = target.relative_to(root).as_posix()
            if dest in selected: return m.group(0)
            resource = records.get(dest,({},''))[0].get('resource')
            return f'[{label}]({resource})' if resource else label
        body = re.sub(r'\[([^\]\n]+)\]\(([^)\n]+)\)',rewrite,body)
        target = out/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text('---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True).strip()+'\n---\n'+body.strip()+'\n')
    primary = 'markets/en.md' if 'markets/en.md' in selected else None
    index = '---\nokf_version: "0.2"\n'
    if primary:
        index += 'primary_language: "en"\nprimary_reference: "markets/en.md"\n'
    index += '---\n\n# Yesim verified public consumer pack\n\n'
    index += 'Snapshot of reviewed public records. Current official product terms control. Draft, internal-editorial, reference-only and stale records are excluded.\n\n'
    if primary:
        index += '[Start with the primary English product reference](markets/en.md). Current purchased conditions and sourced local exceptions control.\n\n'
    index += '\n'.join(f'- [{meta["title"]}]({rel})' for rel,(meta,_) in sorted(selected.items()))+'\n'
    (out/'index.md').write_text(index)
    manifest = {'generated_at':now.isoformat(),'included':sorted(selected),'excluded':sorted(set(records)-set(selected))}
    if primary:
        manifest.update(primary_language='en', primary_reference=primary)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    errors,_,_ = inspect(out,now)
    if errors: raise ValueError('export validation failed: '+'; '.join(errors))
    return len(selected)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--now')
    args = parser.parse_args()
    try: count = export(args.root,args.out,timestamp(args.now) if args.now else None)
    except ValueError as exc: print(str(exc),file=sys.stderr); return 1
    print(f'Exported {count} verified public concepts to {args.out}')
    return 0

if __name__ == '__main__': sys.exit(main())
