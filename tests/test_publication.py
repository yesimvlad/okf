import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import datetime, timezone

import yaml

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from export_site import build
from validate import inspect

NOW=datetime(2026,10,8,tzinfo=timezone.utc)

class PublicationTests(unittest.TestCase):
    def bundle(self,root):
        (root/'index.md').write_text('---\nokf_version: "0.2"\n---\n\n# Index\n')
        meta={'id':'yesim:markets/en','type':'Market','title':'English reference',
          'description':'Product knowledge.','language':'en','status':'stable','audience':'public',
          'sources':[{'id':'official','resource':'https://yesim.app/'}],
          'generated':{'by':'test/writer','at':'2026-10-08T00:00:00Z'},
          'verified':[{'by':'test/reviewer','at':'2026-10-08T00:00:00Z'}],
          'stale_after':'2026-11-01T00:00:00Z'}
        self.put(root,'markets/en.md',meta,'# English\n\n[Product](../products/esim.md)\n\n| Field | Value |\n|---|---|\n| Billing | Data |\n')
        self.put(root,'products/esim.md',dict(meta,id='yesim:products/esim',type='Product'),'# Product\n\nReviewed fact.\n')
        self.put(root,'internal/idea.md',dict(meta,id='editorial',status='draft',audience='internal-editorial'),'# Draft\n')
        return meta

    def put(self,root,rel,meta,body):
        p=root/rel;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text('---\n'+yaml.safe_dump(meta)+'---\n\n'+body)

    def test_clean_site_keeps_sources_tables_and_valid_links_without_frontmatter(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'source';root.mkdir();self.bundle(root)
            out=Path(temp)/'site'
            self.assertEqual(build(root,out,'https://yesim.app/knowledge/',NOW),2)
            md=(out/'markets/en.md').read_text();html=(out/'markets/en.html').read_text()
            self.assertFalse(md.startswith('---'))
            self.assertNotIn('test/writer',html)
            self.assertIn('https://yesim.app/',md)
            self.assertIn('<table>',html)
            self.assertIn('../products/esim.html',html)
            self.assertIn('type="text/markdown"',html)
            self.assertIn('Sources checked 2026-10-08',html)
            self.assertFalse((out/'internal/idea.md').exists())
            self.assertIn('generated:',(out/'okf/markets/en.md').read_text())
            manifest=json.loads((out/'manifest.json').read_text())
            self.assertEqual(manifest['publication_status'],'built-not-deployed')
            self.assertEqual(len(manifest['records']),2)
            self.assertNotIn('internal/idea.md',(out/'llms.txt').read_text())

    def test_stale_primary_stops_site_without_leaving_a_partial_release(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'source';root.mkdir();meta=self.bundle(root)
            self.put(root,'markets/en.md',dict(meta,stale_after='2026-10-01T00:00:00Z'),'# English\n')
            out=Path(temp)/'site'
            with self.assertRaisesRegex(ValueError,'fresh primary'):build(root,out,'https://yesim.app/knowledge/',NOW)
            self.assertFalse(out.exists())

    def test_localized_view_preserves_full_okf_and_has_reciprocal_alternates(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'source';root.mkdir();meta=self.bundle(root)
            meta['translation_group']='overview'
            meta['sources'].append({'id':'unused','resource':'https://yesim.app/unused/'})
            self.put(root,'markets/en.md',meta,'# English\n\n[^unused]: https://yesim.app/unused/\n')
            localized=dict(meta,id='yesim:markets/ar',language='ar',public_view='localized-answers',
                title='معلومات Yesim',source_links_heading='المصادر الرسمية')
            self.put(root,'markets/ar.md',localized,'# Internal scope\n\nPreserved research.\n\n<!-- public-view:start -->\n# معلومات Yesim\n\nإجابة. [^official]\n<!-- public-view:end -->\n\n[^official]: https://yesim.app/\n')
            out=Path(temp)/'site';build(root,out,'https://yesim.app/knowledge/',NOW)
            native=(out/'markets/ar.html').read_text();english=(out/'markets/en.html').read_text()
            self.assertIn('lang="ar" dir="rtl"',native)
            self.assertNotIn('Preserved research.',native)
            self.assertIn('Preserved research.',(out/'okf/markets/ar.md').read_text())
            self.assertIn('hreflang="en"',native)
            self.assertIn('hreflang="ar"',english)
            self.assertIn('hreflang="x-default"',native)
            self.assertNotIn('href="#fnref:unused"',english)
            self.assertIn('https://yesim.app/unused/',(out/'markets/en.md').read_text())
            # A missing/duplicated view must not silently publish the mixed-language body.
            self.put(root,'markets/ar.md',localized,'# Missing native view\n')
            with self.assertRaisesRegex(ValueError,'localized public view'):
                build(root,Path(temp)/'invalid','https://yesim.app/knowledge/',NOW)

    def test_active_content_is_rejected_before_release(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'source';root.mkdir();meta=self.bundle(root)
            self.put(root,'markets/en.md',meta,'# English\n\n<script>alert(1)</script>\n')
            out=Path(temp)/'site'
            with self.assertRaisesRegex(ValueError,'active HTML'):build(root,out,'https://yesim.app/knowledge/',NOW)
            self.assertFalse(out.exists())

    def test_existing_output_is_preserved_and_base_url_is_validated(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'source';root.mkdir();self.bundle(root)
            out=Path(temp)/'site';out.mkdir();(out/'keep').write_text('keep')
            with self.assertRaises(ValueError):build(root,out,'https://yesim.app/knowledge/',NOW)
            self.assertEqual((out/'keep').read_text(),'keep')
            with self.assertRaises(ValueError):build(root,Path(temp)/'new','https://user:secret@example.com/',NOW)

    def test_duplicate_yaml_and_case_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);self.bundle(root)
            p=root/'products/esim.md';p.write_text(p.read_text().replace('type: Product','type: Product\ntype: Other'))
            self.assertTrue(any('duplicate YAML key' in e for e in inspect(root,NOW)[0]))
            (root/'evaluations').mkdir()
            case={'id':'same','prompt':'Question?','expected':'Answer.','sources':['https://yesim.app/'],'critical':True}
            (root/'evaluations/cases.yaml').write_text(yaml.safe_dump({'cases':[case,case]}))
            self.assertTrue(any('duplicate evaluation id' in e for e in inspect(root,NOW)[0]))

if __name__=='__main__':unittest.main()
