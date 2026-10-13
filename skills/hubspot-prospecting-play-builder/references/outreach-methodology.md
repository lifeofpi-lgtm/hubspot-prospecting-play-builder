# Outreach defaults and adaptation

Use the concise base in `assets/advanced-instructions-base.txt` as a starting point. Customize only the parts that change decisions for this buyer, offer, and motion. Do not append every source note or instruction from previous clients.

## Why these defaults

Justin Michael's public material emphasizes compression, specificity, and adaptable principles; his examples also include meeting requests. The no-first-call and owner-led-calendar policies here are program defaults, not universal JMM rules. [Author's introduction](https://www.linkedin.com/posts/michaeljustin_the-justin-michael-method-the-jmm-activity-6923646039899922432-Zn9a), [original summary](https://f.hubspotusercontent20.net/hubfs/6433523/The%20Justin%20Michael%20Method%E2%84%A2%20%28JMM%E2%84%A2%29.pdf).

Use the ideas that fit the client's brand and audience. Do not adopt aggressive pressure, rapid bursts, fabricated familiarity, or deliberate mistakes merely because they appear in an outbound framework. Do not claim any method guarantees response rates.

## Editable program choices

Explain these once, invite adjustments, and record the chosen version in the guide:

- First touch: aim for 35–60 body words. Follow-ups: 20–40. Allow an extra short sentence when essential context or credible proof improves understanding.
- Adapt order, opening, and sentence count. Keep one relevant issue and one clear CTA; no repeated explanation or second closing.
- Use a brief verified context or relevant work situation. Personalization must explain relevance, not show off research.
- Include proof only if it fits. Never invent an asset to create a resource-offer CTA.
- Each follow-up has a distinct job: make it concrete (an example of how the contribution works), sharpen the question, then close the loop. No two emails end with the same question or wording. Avoid empty bumps and catalog cycling.
- Cadence: 3 to 4 emails, 3 to 5 days apart, set through native controls (Adaptive: Maximum emails per enrollment and Minimum days between emails; Sequence: step count and delays). Follow-ups produce a large share of replies in public benchmarks, so a single email is rarely enough; a weekly maximum is the conservative option.
- Default to no first-email meeting request and no scheduling links in automated prospecting. The owner handles replies and shares the approved link after explicit meeting interest.

Client changes to length, tone, cadence, or CTA strategy are configurable choices. Make the actual instructions, examples, setup notes, and tests agree after a change. Do not call these preferences HubSpot requirements. User preferences cannot make an unsupported fact true or override product controls and contact opt-outs.

## Match the CTA section to the client's choice

The base's CALL TO ACTION AND MEETING LINKS section is written for the reply-first default. When the client chooses a direct approach (for example the direct tier of UC12, or a client who wants a meeting ask in the first touch), replace that whole section with the direct version below. Do not leave the reply-first section in place and add exceptions; the agent then receives two conflicting rules.

Direct version, tailored to the client's approved next step:

```text
CALL TO ACTION AND MEETING LINKS
This Play uses a direct approach: the first email may ask for a short conversation about the selected issue. Ask once per email, name a specific, modest commitment (for example a 15-minute call about the issue), and make it easy to decline. Use only the meeting link or CTA configured in Guardrails; never invent one. Do not escalate the ask because of opens, visits, or silence. Follow-ups keep their distinct jobs and may repeat the offer in different words, not the same closing.
```

One Play has one CTA approach. If a client wants warm-up for some tiers and direct for others, recommend one Play per approach, each with its own segment, instead of tier-conditional instructions in a single field. For Adaptive under the direct approach, the **Request contact to book a meeting** CTA in Guardrails is the native way to supply the link. Update the illustrative emails, setup guide, and `cta_policy` row so they all describe the same approach.

The reply and link table below applies to the reply-first default. Under the direct approach, the owner still handles replies; only the automated emails change.

## Ground the instructions with one client exemplar

Instructions made only of rules tend to produce flat, interchangeable emails. After tailoring the base, add one short first-touch exemplar built from verified client facts and a realistic (labeled) buyer situation, introduced as: "Example of shape and tone only. Do not reuse its wording or facts." Keep it under 70 words. Omit it when no verified facts support a credible example; never use a synthetic scenario inside paste-ready instructions.

## Adaptive versus Sequence

For **Adaptive**, deliver the tailored base as `04-advanced-instructions.txt`. For **Sequence**, deliver `04-sequence-steps.txt` instead: for each step, give the business-day delay, the step's job (first touch, make it concrete, sharpen the question, close the loop), suggested smart block names, and prompt instructions. Each smart block is generated separately, so each prompt repeats the essential evidence, length, and CTA rules in a few lines rather than referring to other steps. Keep headings plain text; no Markdown.

## Reply and link decisions under the default policy

| Response/evidence | Recommended action |
| --- | --- |
| Explicit interest in speaking, agreement to meet, or request for availability | Owner may share the approved calendar link with a relevant meeting purpose. |
| Acknowledges a problem | Owner addresses the issue and offers a specific reason to talk; do not treat this as agreement to meet. |
| Requests information or a resource | Provide the requested material first; no calendar link as a substitute. |
| No reply, opens, tracked visits, account intent, or several touches | No automatic calendar link or inference of consent. |
| Opt-out, refusal, hold, or timing objection | Honor the preference. Record any explicitly invited future follow-up and its scope. |

This is owner-handoff guidance, not permission for the agent to run an automated reply conversation. Keep configured stop conditions and actual product behavior distinct from policy recommendations.

## Quality review

Check the buyer can understand the relevance, contribution, and question. Remove repeated tension, generic industry commentary, unexplained jargon, unsupported diagnosis, and implied guarantees. A possible problem should remain conditional. An expansion headline does not prove ticket growth; a funding event does not prove a spending budget; a score improvement is not automatically risk reduction.

Evaluate illustrative examples against the chosen policy, including whether each follow-up does a different job and ends differently. Count words without treating the flexible target as a reason to delete meaning. Preview all steps in the actual product before any separate rollout. Suggested pilot outcomes are positive replies, qualified conversations, meetings held, and opportunities, with negative replies and opt-outs tracked separately. Do not claim tests or results that have not occurred.
