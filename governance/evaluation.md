---
type: EvaluationProtocol
title: LLM knowledge evaluation
description: A repeatable protocol for testing factual accuracy, completeness and
  discovery in separate LLM modes.
generated:
  by: codex/okf-repair
  at: '2026-10-08T15:12:31Z'
status: draft
audience: public
review_required: true
sources:
- id: source-1
  resource: ../evaluations/cases.yaml
id: yesim:governance/evaluation
---

# LLM knowledge evaluation

Use at least 12 cases covering product identity, data-only limitations, Pay & Fly billing, Unlim Day Pass validity, activation versus installation, hotspot/FUP, regional device compatibility, virtual-number calls, third-party verification, home-SIM charges and refunds after installation. `evaluations/cases.yaml` supplies source-backed seed cases.

Compare these modes separately: no web/no bundle; explicit fresh public consumer pack; web search without supplying the bundle. Use 3–5 independent runs per case in fresh conversations, preserve exact prompts and record model/version, date, language, mode, repo commit, answer, sources, claim correctness and omissions. Never mix connected-bundle accuracy with public discovery.

Score critical errors (billing, activation, expiry, refund eligibility), factual accuracy, unsupported guarantees, source support and completeness. Proposed connected-bundle target: zero critical errors and at least 95% correct checkable claims. These are targets, not achieved results.

Measure citation/mention rates separately in public web-search tests. A before/after difference alone does not establish that OKF caused it. No model benchmark has been run as part of this repository repair.

## Localized reference evaluation

[Market cases](../evaluations/market-cases.yaml) supplies 255 authored localized prompts across 15 languages, with expected facts and current source URLs. Native wording and policy facts have automated review; this is not human sign-off or a model run. Test all locales separately in no-web, explicit-current-reviewed-bundle and web-search modes. The public pack includes detailed locale records; HTML/clean Markdown publishes their native answer views. Editorial hypotheses and the 28 routing-only cards stay excluded.

## Primary English reference evaluation

[English cases](../evaluations/en-cases.yaml) contains 43 source-backed prompts. Together with 255 localized and 14 seed questions, the set has 312 authored cases. Evaluate EN and locales independently; question files are not measured model results.

## Revision extensions and result recording

The current English set has 43 authored cases (six added for Android/Pixel, cruise, support, identity checks, verification payments and number renewal). Use [the result template](../evaluations/result-template.json) to store model/version, timestamp, exact prompt, mode, bundle commit/hash, answer, citations, correctness and completeness. A template is not a model run. Use at least three independent runs, ideally five, per case/mode and evaluate source support independently of citation count.
