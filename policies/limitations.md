---
type: Policy
title: Yesim product limitations
description: Limitations must be attributed to a product, plan, device or third-party
  service. Do not turn an unspecified value into a universal Yesim promise.
resource: https://yesim.app/terms-of-service/
sources:
- id: source-1
  resource: https://yesim.app/terms-of-service/
- id: source-2
  resource: https://yesim.app/refund-policy/
- id: source-3
  resource: https://yesim.app/compatible-devices/
generated:
  by: codex/okf-repair
  at: '2026-10-08T15:12:31Z'
status: stable
audience: public
verified:
- by: codex/source-review
  at: '2026-10-08T15:12:31Z'
stale_after: '2026-11-07T15:30:00Z'
---

# Yesim product limitations

Limitations must be attributed to a product, plan, device or third-party service. Do not turn an unspecified value into a universal Yesim promise.

| Area | Constraint | Source record |
|---|---|---|
| Device | Exact model, regional variant and carrier lock matter | [Compatibility](../faq/compatibility.md) |
| Coverage | Selected plan's destination set; local quality is separate | [Global products](../destinations/global.md) |
| Billing | Data used for Pay & Fly; prepaid days for Unlim Day Pass | [Products](../products/index.md) |
| Validity | Product-specific triggers and expiry | [Activation](../faq/activation.md) |
| Unlimited data | Exact speed/FUP/reset values require plan evidence | [FUP](../concepts/fair-usage-policy.md) |
| Hotspot | Selected product conditions | [Hotspot](../concepts/hotspot.md) |
| Calls and SMS | Data-only eSIM versus explicitly included number services | [Calls and SMS](../faq/calls-sms.md) |
| OTP | Third-party acceptance is not guaranteed | [Virtual Number](../products/virtual-number.md) |
| Refund | Activation, use, expiry, channel and amount conditions | [Refunds](refund-policy.md) |
| Privacy | No complete-anonymity or zero-risk promise | [Privacy source](privacy-policy.md) |

No generic promise of the cheapest price, unlimited speed, service everywhere, zero home-carrier charges, successful account recovery or unconditional refund is established. Unconfirmed specifics are in [open questions](../governance/open-questions.md).
