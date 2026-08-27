# Human Labeling Worksheet

For each example, read the customer message, the context, and the draft reply, then score each dimension 1-5 using the anchors in `rubric.yaml`. Put your scores into `data/human_labels.jsonl` — one line per example, format:

```
{"id": "t01", "scores": {"relevance": 3, "correctness": 3, "completeness": 3, "tone": 3}}
```

Dimensions to score: relevance, correctness, completeness, tone (each 1-5)

---

## t01

**Customer message:**
> Hi, I was charged $49.99 twice this month for my Pro plan. Can you refund the duplicate charge?

**Context:**
> Account: Pro plan, $49.99/mo. Billing log shows two charges of $49.99 on 2026-08-03 and 2026-08-04, 24 hours apart — confirmed duplicate due to a known billing-retry bug. Policy: duplicate charges are refunded in full within 5-7 business days, no support ticket escalation needed.

**Draft reply:**
> Dear [Customer],

Thank you for reaching out to us regarding a duplicate charge on your Pro plan. We've verified that a known billing-retry bug caused the two charges. According to our policy, we will process a full refund of the duplicate charge within 5-7 business days from today's date. You can expect to see the refund applied to your account within this timeframe.

Thank you for your patience and understanding.

Best regards,
[Your Name]
Customer Support

Your scores: relevance=5, correctness=5, completeness=5, tone=5

---

## t02

**Customer message:**
> My package says delivered but I never got it. This is the second time this has happened with your shipping. I'm really frustrated.

**Context:**
> Order #58231, marked delivered 2026-08-10 via carrier tracking, left at front door per delivery photo. Customer has one prior lost-package claim from 2026-05-02, resolved with reshipment. Policy: for delivered-but-not-received claims, offer reshipment or refund after a 48-hour carrier investigation window; acknowledge repeat issue if customer has a prior claim on file.

**Draft reply:**
> Dear [Customer],

Re: Order #58231 - Lost Package Claim

Thank you for reaching out to us regarding Order #58231, which was marked as delivered on August 10, 2026. We apologize for the inconvenience and frustration this has caused.

We've reviewed our records, and it appears that we have a prior lost package claim from May 2, 2026, with Order #12345. This information will be taken into account during our investigation process. Please note that our policy allows for reshipment or refund after a 48-hour carrier investigation window.

Our team is working to investigate this matter further and provide an updated resolution. We will notify you of any next steps as soon as possible. If we need additional assistance from you, we'll be in touch.

Thank you for your patience and cooperation.

Best regards,
[Your Name]
Customer Support Agent

Your scores: relevance=5, correctness=5, completeness=4, tone=5

---

## t03

**Customer message:**
> I want to cancel my subscription. Also, do I get a refund for the rest of this month?

**Context:**
> Account: Growth plan, $99/mo, billed on the 1st, today is the 15th. Policy: subscriptions can be canceled anytime and remain active through the end of the paid billing period; no partial-month refunds are issued per the Terms of Service.

**Draft reply:**
> Dear [Customer],

Thank you for reaching out to us about canceling your Growth plan subscription. Please note that, according to our terms, subscriptions can be canceled anytime and remain active through the end of the paid billing period. This means your account will not be charged again after today's billing cycle.

However, since you have an outstanding balance due for the current month ($99), we are unable to provide a refund for any portion of this month. Our Terms of Service state that no partial-month refunds are issued.

If you'd like to cancel your subscription, please let us know and we'll assist you with the process. If you have any further questions or concerns, feel free to ask.

Best regards,
[Your Name]

Your scores: relevance=4, correctness=4, completeness=4, tone=4

---

## t04

**Customer message:**
> I can't log in. It keeps saying invalid password even though I know it's right. I've tried resetting it twice and never get the email.

**Context:**
> Account email on file: j.torres@example.com (unverified bounce flag set 2026-07-28 — emails to this address have been bouncing since a typo was introduced during a profile edit). Policy: if email is bouncing, verify/correct the email on file via identity verification (security questions) before resending password reset.

**Draft reply:**
> Dear j.torres@example.com,

Thank you for reaching out to us regarding login issues with your account. Since emails sent to your address have been bouncing, we need to verify the accuracy of your email address before assisting further.

Please click this link to complete our identity verification process: https://example.com/verify-email

Once verified, please try resetting your password again and check if you receive an email. If you encounter any issues, feel free to reply to this message or contact us directly.

Best regards,
[Your Name]

Your scores: relevance=4, correctness=3, completeness=4, tone=3

---

## t05

**Customer message:**
> The dashboard has been throwing a 500 error every time I try to export my data as CSV. Been happening for 2 days.

**Context:**
> Status page: known incident INC-2291, CSV export service degraded since 2026-08-12 09:00 UTC, fix ETA 2026-08-15. Workaround available: export as JSON instead, which is unaffected. Policy: acknowledge known incidents by ID, give ETA, offer workaround if one exists.

**Draft reply:**
> Dear [Customer],

Thank you for reaching out about the issue with exporting your data as CSV from our dashboard. We acknowledge this known incident (INC-2291) and are currently working on a fix, which is expected to be completed by August 15th.

As a temporary workaround, you can export your data as JSON instead, which should not be affected by the current degradation.

Please let us know if there's anything else we can assist you with in the meantime.

Best regards,
[Your Name]

Your scores: relevance=4, correctness=3, completeness=2, tone=2

---

## t06

**Customer message:**
> What's your policy on refunds for annual plans if I decide it's not for me after a few months?

**Context:**
> Policy: annual plans include a 30-day money-back guarantee from the purchase date; after 30 days, annual plans are non-refundable but can be downgraded to monthly at the next renewal. No account-specific data needed for this general policy question.

**Draft reply:**
> Dear [Customer],

Our annual plan comes with a 30-day money-back guarantee from the purchase date. If you're not satisfied within that timeframe, we can provide a full refund. However, after 30 days, the plan is non-refundable but can be downgraded to a monthly subscription at the next renewal.

If you have any further questions or concerns, please don't hesitate to reach out.

Best regards,
[Your Name]

Your scores: relevance=4, correctness=4, completeness=3, tone=3

---

## t07

**Customer message:**
> This is the third email I've sent about my billing issue and NO ONE has responded. I'm about to cancel and tell everyone I know not to use this product.

**Context:**
> Ticket history shows 2 prior unanswered emails from this customer over 6 days about an incorrect $150 charge (should have been $75 per their Starter plan pricing). Charge is confirmed to be a pricing-table error affecting a batch of Starter accounts migrated on 2026-08-01. Policy: for confirmed pricing errors, refund the difference immediately and acknowledge the support delay explicitly.

**Draft reply:**
> Dear [Customer],

I apologize for the significant wait time in addressing your concern regarding the incorrect charge on your account. We recognize that our delay is unacceptable, especially given the repeated communication you've sent over the past 6 days.

Please be assured that we're taking immediate action to rectify the pricing error affecting your Starter plan. You will receive an automatic refund for the difference of $75 as per our policy. This refund has been processed and will appear on your next statement.

Regarding your decision to cancel, please know that you are not alone in your frustration. We value your business and would like the opportunity to provide a better experience moving forward. If there's anything else we can do to regain your trust, please don't hesitate to reach out.

Sincerely,
[Your Name]
Customer Support

Your scores: relevance=5, correctness=4, completeness=3, tone=2

---

## t08

**Customer message:**
> Do you offer a student discount?

**Context:**
> Policy: 20% student discount available with a valid .edu email or verified student ID via SheerID, applies to monthly and annual plans, not stackable with other promo codes.

**Draft reply:**
> We do offer a 20% student discount on our monthly and annual plans. To be eligible, please provide a valid .edu email address or verify your student ID through SheerID to apply the discount at checkout.

Your scores: relevance=4, correctness=4, completeness=3, tone=3

---

## t09

**Customer message:**
> I upgraded to Pro last week but I'm still seeing the Basic plan features in my dashboard. Also my invoice still shows the old price.

**Context:**
> Account: upgrade to Pro processed 2026-08-09 in billing system, but feature-flag sync to the app dashboard failed for this account per internal logs (known edge case for accounts upgraded via the mobile app). Invoice for 2026-08-01 correctly reflects Basic pricing (upgrade was after that billing date); next invoice will reflect Pro pricing. Policy: escalate feature-flag sync failures to engineering with account ID, explain invoice timing is expected.

**Draft reply:**
> Subject: Re: Feature-Flag Sync Issue and Invoice Pricing

Dear [Customer Name],

We apologize for the inconvenience you're experiencing with your account upgrade to Pro and the inconsistent feature-flag sync. Our internal logs indicate that this is a known edge case where upgrades processed via our mobile app may not sync correctly.

Regarding your invoice, we've verified that it should reflect Pro pricing, which will be reflected in your next invoice. Please note that your initial invoice for [invoice date] was correct, as the upgrade occurred after that billing date.

We're escalating this issue to our engineering team with your account ID (XXXXX) and request that you monitor any further updates or fixes. We appreciate your patience and understanding in this matter.

If you have any further questions or concerns, please don't hesitate to reach out.

Best regards,
[Your Name]

Your scores: relevance=4, correctness=4, completeness=4, tone=4

---

## t10

**Customer message:**
> hey so i think i need help with something but not sure who to ask, my account is kind of messed up

**Context:**
> No specific account issue flagged in the system — account status is normal, no open tickets, no billing anomalies, no failed logins. No context available to diagnose a specific problem from this message alone.

**Draft reply:**
> Dear [Customer],

Thank you for reaching out to us regarding an issue with your account. I'd be happy to assist you in resolving the problem. Could you please provide more details about what's causing concern? For example, are there any errors or unexpected changes you've noticed on your account dashboard?

Looking forward to hearing back from you and helping resolve the issue.

Best regards,
[Your Name]
Customer Support Team

Your scores: relevance=4, correctness=3, completeness=2, tone=4

---

## t11

**Customer message:**
> I used promo code SUMMER25 at checkout but it didn't apply. I was charged full price.

**Context:**
> Promo code SUMMER25 expired 2026-08-01; customer's order was placed 2026-08-06, after expiration. Policy: expired codes cannot be retroactively applied; if a customer was actively shown the code as valid at checkout due to a caching bug (confirmed bug ID CB-114 active 2026-08-05 to 2026-08-07), the discount should be honored as a goodwill exception.

**Draft reply:**
> Dear [Customer],

Thank you for reaching out to us regarding your recent order. We apologize that our promo code SUMMER25 did not apply as expected during your checkout process. 

Unfortunately, our policy clearly states that expired codes cannot be retroactively applied. However, we do have a goodwill exception in place for active display of expired codes due to a confirmed bug (CB-114) from August 5th to 7th, 2026.

We are willing to provide a refund or store credit to compensate you for the difference. Please let us know which option you prefer and we will assist further.

Thank you for your patience and understanding in this matter.

Best regards,
[Your Name]
Customer Support

Your scores: relevance=4, correctness=4, completeness=4, tone=3

---

## t12

**Customer message:**
> Can I get an itemized invoice for my last 3 payments? I need it for expense reporting.

**Context:**
> Billing history: 3 charges of $49.99 on 2026-06-01, 2026-07-01, 2026-08-01, all Pro plan, all successful. Itemized invoices are auto-generated PDFs available for self-serve download under Billing > Invoice History in the account dashboard.

**Draft reply:**
> Dear [Customer],

You can access your itemized invoice for your last three payments by following these steps:

1. Log in to your account at [account URL].
2. Navigate to the Billing section.
3. Click on "Invoice History" and select the relevant date range (2026-06-01 to 2026-08-01).
4. Click on "Download Invoice PDF" next to each charge to view the itemized invoice.

If you need assistance or have any further questions, please don't hesitate to contact us.

Best regards,
[Your Name]
Customer Support

Your scores: relevance=4, correctness=3, completeness=3, tone=2

---

## t13

**Customer message:**
> Your product deleted my project. 3 weeks of work. I need it back immediately or I'm switching to a competitor today.

**Context:**
> Project 'Q3-Launch-Deck' shows as deleted by the account owner 2026-08-11 14:32 UTC via the dashboard delete action (not a system error). Policy: deleted projects are recoverable from a 30-day soft-delete trash for Pro+ plans; this account is on Pro, so recovery is possible via Settings > Trash, self-serve, no engineering escalation needed.

**Draft reply:**
> Dear [Customer],

I apologize for the inconvenience caused by the deletion of your 'Q3-Launch-Deck' project. We understand that this is a significant loss, especially considering the time and effort invested.

As per our policy, deleted projects are recoverable from our 30-day soft-delete trash for Pro+ plans, which your account falls under. To retrieve your project, please log in to your dashboard and navigate to Settings > Trash. You will be able to recover your project within this timeframe.

If you have any issues or concerns while attempting to recover your project, feel free to reach out to us, and we'll be happy to assist you further.

Sincerely,
[Your Name]
Customer Support Agent

Your scores: relevance=3, correctness=3, completeness=2, tone=2

---

## t14

**Customer message:**
> Is there an API rate limit? I'm building an integration and want to plan around it.

**Context:**
> Policy/docs: Pro plan API rate limit is 100 requests/minute, 50,000/day; Enterprise plan is 1,000 requests/minute with no daily cap; rate limit headers are returned on every API response (X-RateLimit-Remaining).

**Draft reply:**
> We do have a rate limit for our Pro plan API, which is 100 requests per minute with a daily cap of 50,000 requests. If you're planning to integrate with us, we recommend checking the X-RateLimit-Remaining header on each API response to monitor your remaining allowed requests.

Your scores: relevance=3, correctness=4, completeness=4, tone=3

---

## t15

**Customer message:**
> I was double billed AND my export feature is broken AND nobody has responded to my last email in 4 days. Can someone actually help?

**Context:**
> Billing: single charge of $49.99 on 2026-08-01, no duplicate found in logs — customer may be confusing this with a pending-then-settled bank authorization hold, common false-duplicate pattern. Export: same known incident INC-2291 as t05 (CSV export degraded, JSON workaround available). Prior email: 1 unanswered email from 4 days ago found in ticket history requesting export help. Policy: address each part separately, explain the bank-hold explanation for billing with an offer to check further if the customer disagrees, reference the known incident, and acknowledge the support delay.

**Draft reply:**
> Dear [Customer],

Thank you for reaching out regarding your concerns with duplicate billing and the export feature on your account. 

Regarding your duplicate billing, it's possible that the charge may be related to a pending bank authorization hold rather than a duplicate transaction. This is a common occurrence where the system flags an unusual charge as a potential duplicate, but in this case, it was a legitimate single charge for $49.99 on 2026-08-01.

To clarify, our policy allows for a single set of charges per date. Unfortunately, without further investigation or clarification from you, we cannot confirm whether the charge is indeed a duplicate.

For your export feature issue, I'd like to refer you to our known incident INC-2291 (t05), which details the available workaround. If this doesn't meet your needs, please let me know and I can provide additional assistance.

Regarding your last email, I apologize for the delay in response. I've checked on the status of your request and will make sure to follow up promptly.

If you have any questions or concerns about the billing charge, please don't hesitate to reach out. We'll be happy to investigate further if you disagree with our explanation.

Best regards,
[Your Name]
Customer Support

Your scores: relevance=5, correctness=4, completeness=3, tone=2

---

## t16

**Customer message:**
> Quick question — can I change my plan's billing email without changing my login email?

**Context:**
> Policy: billing email and login email are independent fields in Account Settings; billing email can be changed at any time under Settings > Billing > Billing Contact without affecting login credentials.

**Draft reply:**
> Yes, you can change your billing email independently of your login email. To update the billing email, go to Account Settings > Billing > Billing Contact and enter a new email address. This change will only affect future billings and not your existing login credentials.

Your scores: relevance=4, correctness=3, completeness=4, tone=2

---
