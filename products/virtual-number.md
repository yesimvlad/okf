---
type: Product
title: Yesim Virtual Number
description: A Yesim Virtual Number is a number assigned on a temporary rental basis
  through the Yesim application. It is a separate product from an eSIM data plan.
  Exact capabilities depend on the Product Description for the selected number.
resource: https://yesim.app/virtual-number/
sources:
- id: source-1
  resource: https://yesim.app/virtual-number/
- id: source-2
  resource: https://yesim.app/terms-of-service/
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

# Yesim Virtual Number

A Yesim Virtual Number is a number assigned on a temporary rental basis through the Yesim application. It is a separate product from an eSIM data plan. Exact capabilities depend on the Product Description for the selected number.[^source-2]

| Capability | What may be stated |
|---|---|
| Phone number | Assigned for the applicable rental period |
| Mobile data | Not supplied by the virtual number itself |
| OTP reception | Verification-related incoming SMS and/or OTP calls where included |
| Person-to-person incoming calls | Only where Inbound Calls Service is expressly included |
| Outgoing calls | Only where Outbound Calls Service is expressly included |
| Incoming/outgoing SMS | Check the included service, allowances and destinations separately |
| Internet access | Required for the app-based communication functions |
| Renewal | Check subscription settings and rental terms |

The OTP Service is limited to verification-related inbound communications. It does not support person-to-person voice conversations or outbound calls/SMS. Other calling or messaging functionality must be expressly included in the applicable Product Description.[^source-2]

The website publishes verification-use pages, including WhatsApp and Telegram. A page about a service is not a guarantee that a selected number will be accepted by that service. Third-party platform acceptance is not guaranteed.[^source-2]

# Questions

## Does every Yesim eSIM include a number?
No. Do not infer number functionality from a data-only eSIM purchase.

## Can I make calls with every Yesim virtual number?
No universal calling capability has been established. Check whether the selected product explicitly includes incoming or outgoing calls. Messenger calls over mobile data are a separate mechanism.

## Does Yesim guarantee bank, WhatsApp or Telegram verification?
No. Check the selected number's capabilities and the third-party service's rules. Do not promise account recovery, unblocking, or successful registration.

## Can I retain a number indefinitely?
Do not assume this. Rental expiry and renewal apply; the Terms do not guarantee restoration of an expired number.[^source-2]

# Sources and related knowledge

- [Official product page](https://yesim.app/virtual-number/)
- [Calls and SMS FAQ](../faq/calls-sms.md)
- [Terms](../policies/terms-of-service.md)
- [Capabilities requiring product confirmation](../governance/open-questions.md)

[^source-1]: Official virtual-number page, checked 2026-10-08; its marketing wording does not establish every number's capabilities.
[^source-2]: Yesim Terms of Service, definitions of OTP and communication services, checked 2026-10-08.
