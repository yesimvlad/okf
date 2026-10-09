---
type: PublishingProfile
title: Yesim knowledge data model and ownership
description: Entity relationships, required authoring fields and source ownership for product knowledge.
audience: reference
status: draft
generated:
  by: codex/repository-revision
  at: '2026-10-08T16:55:46Z'
sources:
  - id: source-1
    resource: ../spec.md
  - id: source-2
    resource: ../products/index.md
---

# Yesim knowledge data model and ownership

This is a Yesim authoring profile extending OKF, not a separate industry standard. Public concept IDs use `yesim:<repository path without .md>`. These knowledge-record IDs are not commercial tariff IDs or Schema.org types. Links identify record relationships; sources identify evidence.

| Entity | Required business fields | Authoritative source | Relationships | Publication / owner / refresh |
|---|---|---|---|---|
| Brand / legal entity | ID, name, legal name, registration, official URLs, source and check time | Company master data and legal pages | Offers products; owns official domains | Reviewed reference; Brand/Legal; on change |
| Product | ID, name, category, billing unit, capability scope, limitations, official source | Product owner and current product page | Brand, plans, instructions, policies | OKF plus HTML/Markdown; Product/Support; on change, weekly source check |
| Plan / offer | Real plan ID, product ID, data/billing unit, coverage set, activation trigger, usable validity, purchase/expiry rules, FUP, hotspot, source time | Product catalogue / checkout | Product, destinations, eligible purchaser conditions | Dedicated feed/reference; Product/Engineering; event-driven, daily if published |
| Price / promotion | Offer ID, amount, currency, unit, taxes/charges context, eligibility, start/end, purchase channel, observed time | Billing / checkout / promotion system | Plan or number SKU and market eligibility | Live feed; Product/Marketing; on change and daily checks |
| Destination | Identifier, display name, actual canonical URL, supported plan IDs, source time | Catalogue and plan destination lists | Plans; country/region/city navigation | Generated from catalogue; Product/SEO; on inventory change |
| Device variant | Manufacturer, exact model and regional code, eSIM evidence, OS context, carrier-lock requirement, source time | Current manufacturer documentation plus support compatibility registry | Installation guide and supported service | Reviewed registry; Support; on model/software change |
| Installation guide | Guide ID, device/OS scope, prerequisites, steps, removal/reinstall caveats, source | Help Center and tested app/device flow | Device, profile, activation and refund policy | HTML/Markdown; Support/Engineering; on flow change |
| Number SKU | Real SKU ID, number/service type, rental/renewal, inbound/outbound calls and SMS separately, OTP purpose, territorial/eligibility restrictions, source time | Number catalogue, Product Description, agreement | Number product, purchaser eligibility, policy | Dedicated feed/reference; Product/Legal; on change |
| Policy | Policy ID, official URL/version/effective date if published, scope, source-check time | Legal master and current official policy | Products, purchase channels, exceptions | Scoped summary linking full policy; Legal; immediate update on change |
| Locale | Language code, actual website URL, source mapping, review method/date/scope, local exception evidence | Language selector plus Localization/Product | Shared EN definitions and local official sources | Publish source-reviewed native answer views individually; Localization/SEO; after shared changes |

Source ownership must be assigned to actual staff by the owner. Role labels here propose responsibility and do not record sign-off.

## Persistent definitions versus changing inventory

Keep product distinctions, terminology, navigation and bounded instructions in this repository. Store price, tariff inventory, coverage lists, model variants and number functions in dedicated records generated from product systems. Join using real stable IDs, not display names or guessed URL slugs.

Unknown is different from false. For example, `outgoing_calls: unknown` means the purchased function has not been established; it must not be converted to either a promise or a blanket prohibition. A plan without a confirmed activation trigger is not ready for a precise validity answer.

## Proposed plan record

The example shows required information, not an existing Yesim tariff. Every `null` must be populated from the product system before publishing a live plan record.

```json
{
  "record_type": "plan",
  "id": null,
  "product_record": "yesim:products/esim",
  "billing_unit": null,
  "data_allowance": null,
  "destination_ids": null,
  "activation_trigger": null,
  "usable_validity": null,
  "activation_deadline": null,
  "fup": {"high_speed_allowance": null, "reduced_speed": null, "reset_rule": null},
  "hotspot": {"availability": "unknown", "limits": null},
  "offer": {"amount": null, "currency": null, "eligibility": null},
  "official_source": null,
  "observed_at": null,
  "publication_status": "requires-product-data"
}
```

## Update flow

Product-system/source change → affected shared records → EN reference and expected answers → affected locale records and source/linguistic review → validation → fresh export → website release → factual evaluation. Preserve explicitly sourced local exceptions. Do not refresh verification timestamps without checking evidence.

Price/coverage feeds are not implemented here because their authenticated product source and contracts are not available. Do not build a fabricated inventory to fill the shape.
