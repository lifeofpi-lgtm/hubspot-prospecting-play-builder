# HubSpot setup map and source refresh

Reference checked 2026-10-02 against the setup article dated 2026-09-30. Refresh before each run; a successful page retrieval is not proof that a client's account has the same interface or entitlement. The following mapping organizes preparation, not a universal UI contract.

## Official entry points

- [Prospecting Agent setup](https://knowledge.hubspot.com/prospecting/use-the-prospecting-agent): play editor, enrollment, review, testing, and performance.
- [Intent signals](https://knowledge.hubspot.com/reports/use-intent-signals): names, meanings, associations, and signal-based segmentation.
- [Buyer intent configuration](https://knowledge.hubspot.com/reports/configure-buyer-intent): visitor criteria (page path, minimum visits/visitors, time period up to 90 days, country, exclusions; up to 10 criteria).
- [Research intent](https://knowledge.hubspot.com/reports/use-research-intent): topics and company-level research.
- [Breeze context](https://knowledge.hubspot.com/ai/manage-breeze-context): Agent Hub context shared by all agents.
- [Product and services catalog](https://legal.hubspot.com/hubspot-product-and-services-catalog): current HubSpot Credits rates.

Follow current official links for a feature's details, permissions, subscription requirements, or credits when relevant. Do not pin prices or credit quantities into client copy; cite the rate sheet and its check date in the guide.

## Play editor map (documented 2026-09-30)

The editor has five tabs. Prepare content for each; the client enters it.

| Tab | Documented fields | What this skill prepares |
| --- | --- | --- |
| Audience | Source contacts for me; Target companies (Add segments); Signals (Edit signals; Research topics by Keyword or Company URL); Target personas (agent finds up to three matching contacts per company); Daily new contact suggestions limit | Segment criteria and exclusions as filter specs; selected signals; personas; a suggested daily limit tied to the credit budget |
| Selling context | Analyze from website; What does your company sell?; What is your value proposition?; What pain points does your company solve?; Which products and services do you want to sell? | Files 01 to 03; which Products & Services entries to select |
| Outreach | Select method: **Sequence** or **Adaptive** | See method section below |
| Guardrails | Send on behalf of (contact owner via a contact property, with Fallback sender, or single user); Tone (preset or brand voice); Adaptive only: multi-language and fallback language, Call to action; Execute on business days; Automated email send window; Default time zone | Sender routing, tone choice, CTA choice and Description text, send window |
| Automation | Review before sending or Send automatically | Review-mode recommendation |

**Test** generates a full sequence for a selected contact. Publish via Review and turn on. Edits apply only to newly enrolled contacts; contacts already enrolled stay on the version they enrolled under.

### Outreach method decides where instructions go

Ask which method the client will use before drafting outreach copy.

- **Adaptive**: one free-text **Advanced instructions** field, plus **Outreach frequency** (Minimum days between emails, Maximum emails per enrollment). The agent follows frequency settings regardless of instruction text. Deliver `04-advanced-instructions.txt`.
- **Sequence**: the client defines steps and business-day delays. Email steps can use **Smart subject**, **smart blocks**, and **Custom Prompt** blocks with **Smart block name** and **Prompt instructions**. There is no single Advanced instructions field. Deliver `04-sequence-steps.txt`: one section per step with delay, step purpose, smart block names, and prompt instructions. Repeat the core evidence and CTA rules briefly in each prompt, since each block is generated on its own.

### Call to action options (Adaptive)

Request contact to book a meeting (HubSpot or non-HubSpot link), Attach a HubSpot document, or Include a URL. Document and URL options take a **Description**. If the client uses either, draft the Description from what the resource actually contains; the resource must exist. The agent decides when to use configured CTAs.

### Character limits

HubSpot documents no character limits for these fields. This skill keeps Advanced Instructions below 10,000 characters based on an earlier account observation; label it observed, not documented, and re-check in the client's editor.

## Agent Hub context (outside the play)

Agents > Agent Hub > Context holds context that every agent uses: Business (brand kit, Products & services), Customers (ICPs, Personas), Team & Processes (**Email personality**), Custom (text or files), and Knowledge vaults. Prospecting agent admins can edit Products & services.

Ask the client to share or screenshot what is already there. Check for conflicts with the play copy, for example a different ICP, outdated products, or an email personality that contradicts the chosen tone. Recommend fixes in the guide; when nothing exists, offer draft Personas and Email personality text as optional extras, not required files.

## Native drafting features

HubSpot can draft the three Selling context fields itself (**Analyze from website**), and a beta workflow action, Infer company value proposition and ICP, generates selling profiles. When the client has run either, ask for the output and show what the skill's version changes: added scope boundaries, role-specific mechanisms, removed unsupported claims. Do not discard useful HubSpot wording out of preference.

## Enrollment routes (documented)

- Agent recommendations from **Monitored companies** (Recommended / All monitored companies).
- **Manage > Automations**, one play per trigger: When page is viewed; When form is submitted; When days since last engagement is more than x; When added to any list.
- Manual enrollment of contacts or companies.
- Breeze Assistant prompt, approved by the user.
- Workflow actions Enroll in / Unenroll in prospecting agent (beta, Sales Hub Pro or Enterprise).

There is no property mapping inside a play. CRM criteria such as Closed Lost become an active list feeding **When added to any list**, a segment under Target companies, or a workflow.

## Cost, trial, and access

Credits are consumed per recommended or manually enrolled lead, with additional steps per play settings; company tracking for intent signals is charged separately. Check the current rate sheet. The free trial clock starts when the first play is published, so do not publish until content passes Test. Required permissions: Prospecting agent admin to configure, Prospecting agent assignment to enroll. Several AI data-access settings must be on; sandboxes cannot run credit-consuming actions.

## Preparation worksheet

| Stage | Client decisions to prepare | Evidence or check needed |
| --- | --- | --- |
| Audience | Selected offer; company fit and exclusions; segments; personas; contact sourcing; daily suggestion limit; signals | Record proposed versus existing segments. Explain AND/OR logic; confirm account UI behavior before implementation. |
| Selling context | Three selling fields; Products & Services selection; Agent Hub conflicts | Confirm offer scope, buyer, proof, restrictions. |
| Outreach | Method; frequency or steps; instructions or step prompts; CTA option and Description | Preserve client choices; label limits observed vs documented. |
| Guardrails | Sender and fallback; tone or brand voice; language; send window and time zone | Record missing owners or time zones as pending. |
| Automation | Review mode; enrollment route; stop behavior; overlap handling | Verify before claiming readiness. |
| Launch readiness | Deliverability, exclusions, credit budget | See [launch readiness](launch-readiness.md). |
| Test | Representative sample contacts, all steps, relevance and factual checks | Distinguish illustrative emails from actual HubSpot Test output. |

## Default recommendations, adjustable by the client

Start with review before sending, one selected offer, and clear owner routing. Suggested starting frequency for Adaptive: Maximum emails per enrollment 3 to 4, Minimum days between emails 3 to 5; a weekly maximum is a more conservative option. Coordinate across plays so one contact is not in two. For Sequence, the same shape: 3 to 4 email steps, 3 to 5 business days apart. Label these recommendations; configure them through native controls, never through instruction text.

For the default reply-first approach, recommend not configuring the book-a-meeting CTA. The owner shares a calendar link after interest. If the client chooses the direct approach, configure that CTA and use the direct call-to-action section from the outreach methodology. Do not repeatedly re-enroll silent contacts to bypass stop conditions. These are setup notes, not extra instruction copy.

## Interface differences

An account observed on 2026-09-24 showed four navigation stages with guardrails inside Outreach, a 48-option native signal picker, three planned steps, and a 30-day duration; the 2026-09-30 documentation shows five tabs. Accounts and versions differ. For each run, record `documented`, `observed in this account`, or `unverified`. A screenshot count alone does not identify all available signals.
