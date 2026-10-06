# Launch readiness

This skill does not configure HubSpot, so most of this is a checklist for the client's admin. One check runs during research: public DNS. Put the results and the checklist in a **Launch readiness** section of the setup guide, and record the `deliverability` and `credit_budget` decisions in Selected Play.

## 1. DNS authentication (automated, read-only)

Prospecting emails go out from the sender's connected inbox, usually on the company's primary domain. Confirm the sending domain with the client; default to the company URL's domain until confirmed. If a shell with `dig` (or `nslookup`) is available, run:

```sh
dig +short MX example.com                      # infers mail provider (Google, Microsoft, other)
dig +short TXT example.com | grep -i spf       # SPF: expect one v=spf1 record
dig +short TXT _dmarc.example.com              # DMARC: expect v=DMARC1
dig +short TXT google._domainkey.example.com   # DKIM, Google Workspace
dig +short CNAME selector1._domainkey.example.com  # DKIM, Microsoft 365 (also selector2)
```

Interpret conservatively:

| Result | Report |
| --- | --- |
| SPF present, includes the inferred provider | Pass |
| SPF missing, or more than one SPF record | Fix before launch |
| DMARC present (any policy, including p=none) | Pass; note the policy |
| DMARC missing | Fix before launch; Google, Yahoo, and Microsoft require it for bulk senders and it protects the domain |
| DKIM found at a common selector | Pass |
| DKIM not found at common selectors | **Unverified**, not failed; the provider may use another selector. Ask the admin to confirm in the mail provider console |

Record the commands, date, and results in Evidence & Gaps. If no DNS tool is available, list these as admin checks instead and say the check was not run. Never claim inbox placement or reputation from DNS alone.

## 2. Admin checklist (manual)

| Check | Where | Threshold or expected state |
| --- | --- | --- |
| Sender inbox connected for each sending user and the fallback sender | HubSpot: user's connected inbox settings | Connected and sending |
| Contact list quality | Client's verification tool, or bounced contacts already in the segment | Bounce rate under 2% (aim under 1%); exclude known bounces |
| Spam complaints | Google Postmaster Tools for the domain, when volume is enough to report | Under 0.1%; 0.3% is the provider ceiling |
| Unsubscribe and opt-out handling | HubSpot sales email settings and subscription status | Opt-outs honored; reflected before enrollment |
| Early performance | Prospecting Agent performance view | Pause the play if bounces or negative replies rise sharply |

Keep these as thresholds to hold the play to, not things the skill can observe. At low prospecting volumes, Postmaster data may never appear; say so.

## 3. Exclusions

Turn these into filter specs for the play's segment or list. The admin builds them.

- Current customers, open opportunities, and contacts in active owner conversations (already in the skill's defaults).
- Competitors, partners, resellers, and the client's own employees.
- Contacts recently in another play or sequence: propose a cooldown period.
- Bounced, unsubscribed, or opted-out contacts.
- **Jurisdiction** (not legal advice; the client confirms with counsel):
  - Germany: B2B cold email generally needs prior consent. Default to excluding unless the client has consent.
  - Other EU countries: rules vary; GDPR requires a legitimate interest basis, a privacy notice at first contact, and an opt-out.
  - UK: corporate addresses can be emailed under legitimate interest with an opt-out; sole traders and some partnerships need consent.
  - Canada (CASL): needs consent; implied consent via conspicuous publication is narrow. Default to review.
  - US (CAN-SPAM): no opt-in, but accurate headers, a postal address, and opt-outs honored within 10 business days.

Use the Country property (or the client's equivalent) in the filter spec. Do not name internal property names until verified.

## 4. Credit budget

Give the formula, not a fixed price:

`estimated monthly credits = daily new contact suggestions limit × sending days per month × credits per recommended lead (current rate sheet) + tracked companies × monthly tracking credits`

Fill it with the client's chosen limit and the rate sheet values on the check date, cite the source and date, and note that additional steps can add usage. Suggest the client's billing admin set a credit limit. If the client is on the free trial, note that the clock starts at first publish: finish Test review first.

## 5. Stop signals

Name the conditions that pause the play: bounce rate over 2%, any spam complaint spike, a rise in negative replies or opt-outs, or a factual error found in review. Opens are unreliable and are not a success measure. Do not promise results.
