---
type: EvaluationProtocol
title: LLM knowledge evaluation
description: Use at least 12 cases covering product identity, data-only limitations,
  Pay & Fly billing, Unlim Day Pass validity, activation versus installation, hotspot/FUP,
  regional device compatibility, virtual-number calls, third-party verification, home-SIM
  charges and refunds after insta
generated:
  by: codex/okf-repair
  at: '2026-10-08T15:12:31Z'
status: draft
audience: public
review_required: true
sources:
- id: source-1
  resource: ../evaluations/cases.yaml
---

# LLM knowledge evaluation

Use at least 12 cases covering product identity, data-only limitations, Pay & Fly billing, Unlim Day Pass validity, activation versus installation, hotspot/FUP, regional device compatibility, virtual-number calls, third-party verification, home-SIM charges and refunds after installation. `evaluations/cases.yaml` supplies source-backed seed cases.

Compare these modes separately: no web/no bundle; explicit fresh public consumer pack; web search without supplying the bundle. Use 3–5 independent runs per case in fresh conversations, preserve exact prompts and record model/version, date, language, mode, repo commit, answer, sources, claim correctness and omissions. Never mix connected-bundle accuracy with public discovery.

Score critical errors (billing, activation, expiry, refund eligibility), factual accuracy, unsupported guarantees, source support and completeness. Proposed connected-bundle target: zero critical errors and at least 95% correct checkable claims. These are targets, not achieved results.

Measure citation/mention rates separately in public web-search tests. A before/after difference alone does not establish that OKF caused it. No model benchmark has been run as part of this repository repair.
