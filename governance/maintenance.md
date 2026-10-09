---
type: MaintenancePolicy
title: Knowledge maintenance and publication
description: The repository is the authoring source for scoped Yesim product knowledge.
  Facts must have official sources. Editing a record does not prove it is current.
generated:
  by: codex/okf-repair
  at: '2026-10-08T15:12:31Z'
status: draft
audience: public
review_required: true
sources:
- id: source-1
  resource: ../spec.md
id: yesim:governance/maintenance
---

# Knowledge maintenance and publication

The repository is the authoring source for scoped Yesim product knowledge. Facts must have official sources. Editing a record does not prove it is current.

## Metadata
- `type` is required by OKF; `title`, `description`, `sources`, `generated`, `status`, `audience` are required by this repository's publishing profile.
- `generated` describes the actual writer and edit time.
- `verified` is added only after an actual source check. `human:` must never be used for an automated review.
- `stale_after` is an absolute recheck deadline, not proof of truth until that date.
- Legacy timestamps are preserved for history; they are not verification dates.
- `status: draft` and `review_required: true` mark unreviewed material. Unknown capability values remain unknown.

## Responsibility and recheck cadence
| Data | Owner to assign | Proposed cadence |
|---|---|---|
| Prices, promotion eligibility, tariff inventory | Product / developer / marketing | Source-triggered updates; daily checks if published |
| Coverage, operators, FUP, activation and compatibility | Product / support | On source change and at least monthly |
| Legal policies | Legal / support | On source change; monthly change detection |
| Company metrics and ratings | Brand / SEO | Monthly; preserve platform, date and metric definition |
| Localization | SEO / localization | After any shared fact changes |

Keep prices, live counts and plan conditions in dedicated records. FAQ answers link to them. Plan records require a plan ID, product relationship, supported destinations, data/billing unit, validity/activation rules, currency and price when applicable, source and observation time. Unknown fields are omitted or explicitly unknown, never invented.

Device records require model and regional variant, compatibility evidence and carrier-unlocked requirements. Country records require a country identifier and verified plan relationships. Locale records identify language separately from residence and travel destination.

## Publication
Run the validator before publishing. A public consumer pack includes only `audience: public`, stable, verified, fresh concepts, plus generated indexes; internal editorial files and draft review queues are excluded. 'Internal' is a semantic label, not access control in this public repo.

Publish reviewed HTML and Markdown on the official domain through a separate site change. Link from the help centre and update `/llms.txt` from the same verified facts. Preserve canonical URLs, language mapping and accessible text. Check source HTML, robots/CDN access, indexability and existing Schema.org against visible text before deployment.

No hosting or indexing is created by this repository change. Public chatbots are not guaranteed to discover or use the bundle. Explicit retrieval/file attachment is the controllable consumption path; search discovery is a separately measured experiment.

## Locale completeness

The language registry records all 44 website versions listed in `/llms.txt` as of 2026-10-08. This source check proves the listing, not endpoint availability or translation correctness. Recheck the list when the selector changes and reconcile canonical/hreflang separately. A locale does not imply a sales market, currency or support language.

Do not shorten existing useful local research solely for OKF. Keep scenarios, terminology, queries and source links; label editorial intent and unverified analytics. PL/RO and the 13 expanded locales retain product answers in `markets/` and full editorial research in linked `internal/seo/markets/` files. Fifteen detailed locale records now carry automated source and linguistic review and publish their native answer views. Human sign-off must be recorded separately if performed. The other 28 routing cards remain draft. Changes to shared product facts must trigger review of localized answer examples.

## Primary English reference

The owner designates English as the primary editorial language. `markets/en.md` connects reviewed product records and public-source answers; `internal/seo/markets/en.md` holds research proposals separately. This designation does not grant English wording legal precedence over current Product Descriptions or explicitly sourced local exceptions. The English reference has an automated public-source review, a seven-day recheck deadline and no implied human product or app-level approval. Recheck earlier on any source change; keep live prices and promotions outside permanent claims.

Review affected localized answer patterns whenever a shared definition changes. Verify local restrictions and purchase-channel exceptions with their own sources; do not silently apply a market-specific exception globally.

## Website build and freshness

Use [the publication plan](../docs/publication.md) for static HTML/Markdown and the [data model](data-model.md) for product-system fields and owners. `generated` stays in OKF for provenance; it is not shown in the clean site view. The site builder requires a fresh primary EN reference and rejects active HTML in content. It does not deploy or automatically remove a previously deployed expired release. Monitor published deadlines and recheck or withdraw stale releases.
