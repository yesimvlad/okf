---
type: Product
title: Yesim Unlim Day Pass
description: An annual prepaid pack of unlimited-data usage days with its own activation
  and expiry conditions.
resource: https://yesim.app/unlim-day-pass/
sources:
- id: source-1
  resource: https://yesim.app/unlim-day-pass/
generated:
  by: codex/okf-repair
  at: '2026-10-08T15:12:31Z'
status: stable
audience: public
verified:
- by: codex/source-review
  at: '2026-10-08T15:12:31Z'
stale_after: '2026-11-07T15:30:00Z'
id: yesim:products/unlim-day-pass
---

# Yesim Unlim Day Pass

Unlim Day Pass is an annual global eSIM plan sold as a prepaid pack of unlimited-data days. It is separate from [Pay & Fly](pay-and-fly-esim.md).[^source-1]

| Property | Public-page description |
|---|---|
| Billing unit | A prepaid pack of plan days |
| Start of one day | Connection to a supported mobile network starts a 24-hour usage period |
| Next day | Another day is deducted when reconnecting after the previous 24 hours expire |
| Pack validity | One year; consult the applicable Product Description for the exact expiry |
| Coverage | The current destination list for this product, not all Yesim destinations |
| Remaining days | Use within the pack's validity; rollover requires purchasing a new plan before the existing plan expires |

The product page describes rollover for another 365 days from the new purchase. Do not describe unused days as unconditionally valid forever. Do not assume a calendar day or a midnight reset.[^source-1]

The public page uses both wording about days not expiring and conditions about annual validity and renewal. Treat the latter conditions as necessary; product-team confirmation of the exact expiry and rollover mechanics is recorded in [open questions](../governance/open-questions.md).

Unlimited data does not establish a guaranteed speed. Exact fair-use thresholds, reduced speeds, reset timing, and hotspot limits must come from the selected plan's terms.

# Related knowledge

- [Unlimited data](../concepts/unlimited-data.md)
- [Refund policy](../policies/refund-policy.md)
- [Pricing](pricing.md)

[^source-1]: Official Unlim Day Pass page, checked 2026-10-08.
