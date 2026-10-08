# Yesim Open Knowledge Format bundle

Product knowledge for Yesim, following [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md). Start with the [primary English product reference](markets/en.md) or the [bundle index](index.md). English product facts have an automated public-source review; [English editorial proposals](internal/seo/markets/en.md) remain separately scoped drafts.

## Scope and trust

The authoring repository contains reviewed public concepts, drafts awaiting source review, and preserved editorial research. Being present in this repository does not make a claim verified. The current official policy and purchase-specific Product Description take precedence.

`verified.by: codex/source-review` records an automated reading of cited public sources. It is not human product approval or an app-level test. Record actual human review separately when it happens. See [maintenance](governance/maintenance.md) and [open questions](governance/open-questions.md).

`internal/seo/` is a consumer scope label, not privacy or access control: this GitHub repository is public. Editorial research is excluded from public consumer exports. If confidentiality is required, move that material to a private repository before publication.

## Validate

```bash
python -m pip install -r requirements.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

The validator checks the Yesim publishing profile, YAML, source IDs, timestamp offsets, trust/status requirements, file links and empty documents. Specification examples are excluded from bundle-link checking. Validation does not prove factual accuracy or external URL availability.

## Export for explicit LLM consumption

```bash
python scripts/export_public.py --out dist/public
```

Only public, stable, verified and fresh records are included. Links to omitted concepts resolve to their official resources when available, or become plain text. The generated pack and manifest are local outputs, not a deployment. They can be attached or indexed by a consumer supporting files/retrieval. Review consumer size limits separately.

## Official-site follow-up

Repository updates do not change yesim.app, the Help Center, robots rules, Schema.org, canonical/hreflang or the existing llms.txt. The reviewed facts should be reused for those site changes; see [site follow-up](docs/site-follow-up.md). No public-model learning, crawling, citations or recommendations are guaranteed.

## Licensing

The bundled [specification](spec.md) is attributed to GoogleCloudPlatform/open-knowledge-format and covered by its Apache-2.0 license; see [license](docs/OKF-LICENSE.txt). No blanket license for Yesim product materials is inferred. The owner should select an appropriate redistribution policy for those materials.

## Build the official-domain publication

```bash
python scripts/export_site.py --out dist/site-release --base-url https://yesim.app/knowledge/
```

This creates static HTML, clean Markdown, an OKF copy, llms.txt, sitemap and a source manifest. It excludes drafts and editorial research, keeps provenance in the OKF copy and shows a short review date on HTML. No files are deployed by this command. See [publication instructions](docs/publication.md), [revision findings](docs/revision-audit.md) and [data model](governance/data-model.md). Python 3.11 or newer is required.
