---
type: ReviewQueue
title: Product questions requiring confirmation
description: Public-source review establishes a snapshot, not app-level tests or human
  product approval. No review assignment or sign-off is claimed here.
generated:
  by: codex/okf-repair
  at: '2026-10-08T15:12:31Z'
status: draft
audience: public
review_required: true
sources:
- id: source-1
  resource: https://yesim.app/terms-of-service/
id: yesim:governance/open-questions
---

# Product questions requiring confirmation

| Question | Owner to assign | Publication rule |
|---|---|---|
| Which virtual-number SKUs include OTP, incoming calls, outgoing calls, incoming SMS and outgoing SMS? | Product / support | Do not infer capabilities from general marketing copy |
| What exact high-speed thresholds, reduced speeds, hotspot limits and reset timezone apply to each unlimited plan? | Product / network team | Store per-plan values only after confirmation |
| What exact activation/validity trigger applies to each fixed package? | Product / support | Separate purchase, profile installation, plan activation and connection |
| What are the exact annual expiry and rollover rules for unused Unlim Day Pass days? | Product / legal | Avoid unconditional 'never expires' wording |
| Are refund-policy and virtual-number statements consistent across website, app and languages? | Legal / content | Current policy controls; remove conflicting summaries |
| What canonical/hreflang mapping applies to RU product and virtual-number pages? | SEO / developer | Verify mapping before constructing localized URLs |
| Which offers and promotion codes are currently eligible in each market/currency? | Marketing / product | No universal code or fixed price without fresh evidence |

Public-source review establishes a snapshot, not app-level tests or human product approval. No review assignment or sign-off is claimed here.

## Production conflicts for Product/Legal

- Align Trial and Cruise refund claims with the current Refund Policy.
- Resolve Business Virtual Numbers no-KYC/anonymity wording against Terms §5.2 and Privacy Policy.
- Correct Trial eligibility/paid wording and number capabilities in the existing root llms.txt.
- Assign real owners and approve the publication/redistribution policy for Yesim materials.

See [the revision audit](../docs/revision-audit.md). These are unresolved source conflicts, not changes already made to production.
