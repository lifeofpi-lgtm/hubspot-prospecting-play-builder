# Signal interpretation and CRM reengagement

Read `assets/signal-catalog.json` for the dated names and per-signal recommendations. Read `assets/crm-recipes.json` for proposed mapping patterns. The catalog definitions summarize factual event meanings; use-case and reengagement recommendations are this skill's analysis, not claims that HubSpot implements those plays automatically.

## Refresh and reconcile

Refresh the complete **Intent signal types** table from the official signal page, not just its shorter workflow-filter examples. Preserve source labels and date. Record additions, removals, or meaning changes in the run's evidence/gaps. Do not overwrite the installed skill snapshot during a client run; save its current catalog in the client kit.

The shipped snapshot contains 49 signals: 47 from the documentation (every row reconciled on 2026-10-13 against the page revision dated 2026-09-29) and 2 conversation signals, Key stakeholder identified and Painpoint, observed in a portal picker on 2026-09-25. Job change by UserGems is documented but needs the UserGems integration, so it shows in a picker only when installed; that is why the 2026-09-25 picker showed 48 native options. Picker labels can differ from documentation (for example Layoff, Research, Visitor intent); `ui_label` records the picker spelling. Portals can also show custom signals created for that portal. Note those in the run's evidence, but keep them out of the reusable catalog. Reconcile labels again when a client export, screenshot, or picker view is supplied. Never add fictional rows to match a count.

Research and Company Surge by Bombora use separate topic lists. Research intent topics are configured in the Play setup. Company Surge takes up to 12 Bombora topics selected on the signal itself, in addition to the Research topics.

Account availability starts as unverified. Distinguish documented intent events, observed Play-picker options, workflow events, and fields available in the client's subscription. A signal's presence in one surface does not prove availability in another. Keep aliases separate from canonical labels; for example, abbreviated UI labels may differ from documentation.

If the page cannot be refreshed, use the seed with its original date and `catalog_status: snapshot`. If it changes but the difference cannot be resolved, record the limitation and keep readiness provisional. Never stamp the seed with today's date and call it refreshed.

## Three types of evidence

| Type | Examples | Use |
| --- | --- | --- |
| External intent/news and contact changes | Research, expansion, hiring, job change | Investigate relevance and fit; does not establish an individual buyer's interest. |
| Native CRM signals | Budget mention; Deal timing | Verify recorded signal and supporting deal context. |
| CRM criteria/activities | Closed Lost, loss reason, renewal date, explicit follow-up date, known content engagement, owner activity | Combine real properties and recorded events into proposed eligibility rules. These are not additional native signals. |

Native CRM signal generation (Budget mention, Deal timing, Churn risk) requires the contact → company → existing deal association path. Documentation describes a 2-day cooling-off period, so similar mentions may not immediately generate another event. When tracking starts, the last 30 days of signals are backfilled; treat backfilled events by their actual dates. Treat missing signals as missing evidence, not proof that budget or timing is absent. [Signal reference](https://knowledge.hubspot.com/reports/use-intent-signals).

High-impact distinctions: Headcount increase concerns postings, not filled positions. Technology investment refers to public/government technology funding, not generic software purchases. News Event attendance is company-level and may be prospective; it is not proof that a named person attended. Email bounce and Job ended are hold/verification cues, not outreach opportunities. Research/visitor changes can be negative as well as positive.

## Read optional CRM data

Start with schema/column names and a relevant sample. Identify record IDs, contact-company-deal associations, ownership, current employer/title, lifecycle/deal stage, loss reason, dates, opt-out/hold state, active conversations, and supporting activities as needed. Use supplied labels until actual internal names or IDs are verified. Do not guess pipeline IDs, enum values, workflow support, or property names.

Use association IDs rather than display-name joins. Avoid joining a person to an old employer after a job change. Where multiple deals or conflicting histories exist, identify the relevant deal and route ambiguity to the owner. Unknown exclusions or permission fields mean review needed, not eligible. Do not compute account counts from anecdotes or partial samples.

Limit read-only connector queries to the selected motion. If unavailable or denied, offer exports or proceed with a blueprint; do not install connectors or solicit credentials. Source documents remain in the client's workspace; distribute only necessary summaries in the kit.

## Map to actionable reengagement

For each relevant signal, create a mapping or explain why it is only a hold/research cue. Include native source versus derived criterion, required fields/activities, associations, explicit AND/OR logic, proposed freshness window or dated invitation, exclusions, owner, message angle, route, and evidence status. Use `proposed` until actual fields and supporting records are checked; verified schema alone does not make a contact eligible.

Do not force an external trigger into every reengagement Play. The recipes include CRM-only timing and renewal motions. Time-based reengagement is a valid client choice when the segment defines it, for example Closed Lost after a set period or a meeting outcome of No show. When a reason to reach out exists, suggest leading with it. Avoid stale interest, unresolved loss reasons, changed employers, opted-out contacts, active deals, customers in a separate account motion, and overlapping outreach. Evaluate exceptions through the documented relationship and client choices, not an assumed blanket new-business policy.

Choose a documented route (see [HubSpot fields](hubspot-fields.md)): a native signal with a Target companies segment; an active list feeding the **When added to any list** automation (the usual home for CRM criteria such as Closed Lost, since plays have no property mapping); **When days since last engagement is more than x** for time-based reengagement; **When form is submitted** or **When page is viewed**; the beta workflow action (Sales Hub Pro or Enterprise); or owner-reviewed manual enrollment. These are implementation recommendations; do not activate them. Propose signal-specific lookbacks, explain why, and label them editable defaults rather than product limits. Do not bypass enrollment stops or re-enroll solely to increase touches.

## Rank next Plays

Use fit, relevance to an actual offer, strength/freshness of evidence, and data readiness. Provide up to three ranked choices with reasons and remaining prerequisites. Avoid false numeric precision or forecasting revenue from an intent score. Signals about incidents, layoffs, litigation, or financial distress generally call for owner review and restraint, not automatically manufactured urgency.
