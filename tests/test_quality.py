import sys
import tempfile
from pathlib import Path
from datetime import datetime, timezone
import unittest

import yaml

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate import inspect
from export_public import export

NOW = datetime(2026,10,8,tzinfo=timezone.utc)

class KnowledgeQualityTests(unittest.TestCase):
    def make_bundle(self, root):
        (root/'index.md').write_text('---\nokf_version: "0.2"\n---\n\n# Index\n')
        meta = {'type':'Product','title':'Product','description':'Verified product fact.','sources':[{'id':'official','resource':'https://yesim.app/'}],'generated':{'by':'test/1','at':'2026-10-08T00:00:00Z'},'verified':[{'by':'test/1','at':'2026-10-08T00:00:00Z'}],'status':'stable','audience':'public','stale_after':'2026-11-01T00:00:00Z'}
        self.put(root,'product.md',meta,'# Product\n\nA sourced fact.[^official]\n\n[^official]: Official source\n')
        return meta

    def put(self,root,path,meta,body):
        target = root/path; target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text('---\n'+yaml.safe_dump(meta)+'---\n\n'+body)

    def test_broken_link_is_rejected_but_code_example_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); meta=self.make_bundle(root)
            self.put(root,'product.md',meta,'# Product\n\n[Missing](missing.md)\n```md\n[Example](example.md)\n```\n')
            errors,_,_=inspect(root,NOW)
            self.assertTrue(any('broken link missing.md' in e for e in errors))
            self.assertFalse(any('example.md' in e for e in errors))

    def test_stable_without_verification_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); meta=self.make_bundle(root); meta.pop('verified')
            self.put(root,'product.md',meta,'# Product\n')
            self.assertTrue(any('actual verification' in e for e in inspect(root,NOW)[0]))

    def test_timezone_and_unmapped_footnote_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); meta=self.make_bundle(root); meta['generated']['at']='2026-10-08T00:00:00'
            self.put(root,'product.md',meta,'# Product\n\nClaim.[^unknown]\n\n[^unknown]: Unknown\n')
            errors=inspect(root,NOW)[0]
            self.assertTrue(any('UTC offset' in e for e in errors))
            self.assertTrue(any('no sources[].id' in e for e in errors))

    def test_export_excludes_draft_internal_and_stale_and_repairs_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'source'; root.mkdir(); meta=self.make_bundle(root)
            for name,updates in [('draft',{'status':'draft','resource':'https://yesim.app/virtual-number/'}),('editorial',{'audience':'internal-editorial'}),('stale',{'stale_after':'2026-10-01T00:00:00Z'})]:
                self.put(root,name+'.md',dict(meta,**updates),'# '+name+'\n')
            self.put(root,'product.md',meta,'# Product\n\n[Draft](draft.md) [Editorial](editorial.md) [Stale](stale.md)\n')
            out=Path(tmp)/'export'
            self.assertEqual(export(root,out,NOW),1)
            self.assertFalse((out/'draft.md').exists())
            self.assertFalse((out/'editorial.md').exists())
            self.assertFalse((out/'stale.md').exists())
            self.assertIn('https://yesim.app/virtual-number/',(out/'product.md').read_text())
            self.assertEqual(inspect(out,NOW)[0],[])

    def test_export_does_not_overwrite_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'source'; root.mkdir(); self.make_bundle(root)
            out=Path(tmp)/'export'; out.mkdir(); (out/'keep').write_text('preserve')
            with self.assertRaises(ValueError): export(root,out,NOW)
            self.assertEqual((out/'keep').read_text(),'preserve')

if __name__ == '__main__': unittest.main()
