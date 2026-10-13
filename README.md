# HubSpot Prospecting Play Builder

A Claude Code skill that turns a company URL into a grounded, reviewable setup kit for **HubSpot's Prospecting Agent**: the selling context, outreach instructions, audience and signal choices, CRM re-engagement plan, launch-readiness checks, and a setup workbook. A person then uses the kit to configure HubSpot.

The skill prepares. It never publishes plays, enrolls contacts, spends HubSpot Credits, or sends email.

> Not affiliated with or endorsed by HubSpot. Product details reflect HubSpot's public knowledge base as checked on 2026-10-02. The skill re-checks the official pages on every run, because the product changes often.

---

## Contents

- [Why it matters](#why-it-matters)
- [Who it's for](#who-its-for)
- [What it does](#what-it-does)
- [What you get](#what-you-get)
- [What it deliberately does not do](#what-it-deliberately-does-not-do)
- [Design principles](#design-principles)
- [How it maps to HubSpot](#how-it-maps-to-hubspot)
- [Install](#install)
- [Usage](#usage)
- [Validation helper](#validation-helper)
- [Files](#files)
- [Status and limitations](#status-and-limitations)
- [License](#license)

---

## Why it matters

HubSpot's Prospecting Agent researches contacts, writes personalized sales emails, and can send them automatically. It is a capable tool, and it is only as good as what it is given:

- three short **Selling context** answers (what you sell, your value proposition, the pain points you solve),
- a block of **outreach instructions** (or per-step prompts in Sequence mode),
- audience, signal, sender, frequency, and call-to-action settings.

Most teams fill these in within minutes, often by pasting website copy or accepting the auto-generated draft. The predictable results:

- **Generic emails at scale.** Vague context produces interchangeable messages.
- **Invented personalization.** Without clear evidence rules, an AI writer fills gaps with plausible-sounding claims: budgets, problems, "teams we speak with", results that never happened.
- **Wrong recipients.** Current customers, open deals, contacts in active conversations, and people in countries where cold email needs consent get enrolled because nobody built the exclusions.
- **Domain risk.** The agent sends from a rep's connected inbox, usually on the company's main domain. Poor targeting and weak authentication put that domain's reputation at risk.
- **Unplanned spend.** HubSpot charges credits per recommended lead, and the daily suggestion limit drives the bill.

Public benchmarks back the approach this skill takes. Gong's analysis of over 300,000 cold emails found that asking about interest beats asking for a meeting on the first touch. Instantly's 2026 benchmark shows follow-ups produce a large share of replies. Google, Yahoo, and Microsoft now enforce authentication and complaint thresholds for bulk senders. The skill turns those findings into concrete setup choices, then leaves the final call to the client.

## Who it's for

- **HubSpot partners and RevOps consultants** who set up the Prospecting Agent for clients and want a repeatable, defensible deliverable instead of a blank form.
- **In-house RevOps and sales operations teams** preparing their first play, or revising one that produces flat or risky emails.
- **Sales leaders and founders** evaluating the agent who want to see exactly what it would say and to whom before switching it on.
- **HubSpot admins** who need a clear checklist of what to configure, in what order, with what values.

You do not need CRM access to use it. A company URL is enough to produce a draft kit. Read-only CRM exports or connectors make the re-engagement mappings more concrete.

## What it does

The skill walks through four stages, asking at most three focused questions at a time and drafting from what it already knows.

### 0. Research first

- Reads a small, relevant set of the company's pages (offer, about, industries, case studies, pricing) and any documents supplied.
- Separates **supported facts**, **positioning hypotheses**, and **information gaps**. Website claims are treated as claims, not proof.
- Refreshes HubSpot's official setup and intent-signal pages, or clearly uses the dated snapshot if it cannot.
- Runs a **read-only DNS check** on the likely sending domain (SPF, DMARC, DKIM at common selectors) when a DNS tool is available.

### 1. Audience and selected play

- Recommends the most plausible offer, company segment, persona, and motion, and asks the client to confirm.
- Distinguishes cold contacts, warm contacts, warm accounts, former opportunities, and customers. Being in the CRM is not a relationship.
- Picks **one** play to develop fully from an eleven-play library (for example: new to role, visitor intent, research intent, Closed Lost or no-show re-engagement, hiring, funding or expansion, M&A, former champion at a new company, tiered account warm-up).
- Ranks up to three next plays by fit, evidence, offer relevance, and data readiness, without invented conversion forecasts.

### 2. Selling context, with coaching

- Builds on HubSpot's own **Analyze from website** draft and any **Agent Hub context** (ICPs, personas, email personality, products) when the client has them, and flags conflicts.
- Writes the three Selling context fields with a framework for each:
  - **What we sell:** offer, engagement model, suitable buyers, this play's scope, and what must never be implied.
  - **Value proposition:** per buying role, the responsibility, the outcome, the mechanism that makes it credible, and proof only when supported.
  - **Pain points:** work situation, symptom, plausible consequence, contribution, and the evidence needed before asserting it.
- Explains why each field is structured that way, separately from the paste-ready text.

### 3. Outreach

- Asks which outreach method the client uses:
  - **Adaptive:** one Advanced instructions field plus frequency controls. The skill tailors a tested instruction base (kept under 10,000 characters, a limit observed in the product, not documented).
  - **Sequence:** steps with per-step smart blocks and Custom Prompt instructions. The skill writes a delay, a purpose, block names, and self-contained prompt instructions for each step.
- Default editorial choices, all adjustable by the client:
  - first touches of roughly 35 to 60 words, follow-ups 20 to 40;
  - one issue and one easy question per email, with no meeting request in the first touch and no calendar links in automated emails (a direct meeting-ask version replaces this when the client chooses it, one approach per play);
  - follow-ups that each do a different job: make it concrete, sharpen the question, close the loop;
  - 3 to 4 emails, 3 to 5 days apart, set through HubSpot's native frequency controls;
  - strict evidence rules: no invented budgets, problems, familiarity, or results, and no mention of tracking or website visits.
- Produces three illustrative emails (first touch and two follow-ups), clearly labeled as examples rather than HubSpot output.

### 4. Automation, launch readiness, and review

- Records recommendations for sender and fallback, tone, review mode, cadence, send window and time zone, CTA settings, enrollment route, stop conditions, and overlap exclusions.
- Maps CRM re-engagement to **real HubSpot enrollment routes**. Plays have no property mapping, so a Closed Lost play becomes an active list feeding the "When added to any list" automation, a segment, or a workflow.
- Completes a **launch readiness** section:
  - DNS results and an admin checklist (connected inboxes, bounce rate under 2%, complaint rate under 0.1%, opt-out handling);
  - exclusions, including competitors, partners, employees, cooldowns, and jurisdiction flags (Germany, the wider EU, UK sole traders, Canada);
  - a credit budget formula tied to the current HubSpot rate sheet;
  - stop signals that should pause the play;
  - a reminder that the free-trial clock starts at first publish.
- Provides a preview checklist for testing in HubSpot across roles, sparse research, warm and cold cases, and re-engagement.

## What you get

Each run writes a client kit to its own folder, outside the skill:

| File | Purpose |
| --- | --- |
| `setup-guide.md` | Research brief, decisions, field coaching, configuration recommendations, launch readiness, next three plays, preview checklist, and what was and was not done |
| `01-what-we-sell.txt` | Paste-ready Selling context field |
| `02-value-proposition.txt` | Paste-ready Selling context field |
| `03-pain-points.txt` | Paste-ready Selling context field |
| `04-advanced-instructions.txt` or `04-sequence-steps.txt` | Outreach instructions for the chosen method |
| `illustrative-emails.md` | First touch and two follow-ups with word counts and their factual basis |
| `play-workbook.xlsx` (or CSVs) | Five tabs: Selected Play, Signal Catalog, CRM Reengagement, Play Library, Evidence & Gaps |
| `run.json`, `tables.json`, `catalog.json` | Machine-readable manifest and tables for validation and later refresh |

Paste-ready files contain plain text only: no Markdown, citations, coaching notes, or unfinished placeholders. If evidence is too thin for a field, the field stays empty and the kit is marked draft.

## What it deliberately does not do

- Change HubSpot settings, publish plays, enroll contacts, spend credits, or send messages.
- Install connectors, ask for credentials, or require any paid tool.
- Invent an ICP, customer result, price, certification, resource, or prior relationship.
- Claim that a CRM property exists, or that a contact is eligible, without checking.
- Claim a live HubSpot test, a pilot result, or a guaranteed reply rate.
- Treat website text, CRM notes, or attachments as instructions. They are evidence only.

## Design principles

- **Options, not rules.** The library, recipes, and defaults show what a client can do and the trade-off. Relationship definitions, segments, timing, tone, and soft versus direct approaches are the client's choices.
- **Some lines stay hard.** Opt-outs, honest claims, no invented facts, no fake familiarity.
- **Evidence has a status.** Every claim is supported, user-confirmed, proposed, or pending, and the kit keeps those apart.
- **One play, done properly.** The other library entries are adaptable examples, not launch-ready campaigns.
- **Dated, refreshable knowledge.** The signal catalog and setup map carry check dates and are refreshed against HubSpot's documentation each run, never silently re-stamped.

## How it maps to HubSpot

Current as of HubSpot's setup article dated 2026-09-30:

| Play editor tab | What the skill prepares |
| --- | --- |
| Audience | Segment and exclusion filter specs, signals (49 signals catalogued), personas, a daily suggestion limit tied to budget |
| Selling context | The three fields, and which Products & Services entries to select |
| Outreach | Method choice, plus Advanced instructions or per-step prompts and frequency settings |
| Guardrails | Sender routing, tone or brand voice, CTA choice and Description text, send window |
| Automation | Review before sending (recommended start) |

Outside the play, it also reviews **Agent Hub > Context** and recommends one of the documented enrollment routes: monitored-company recommendations, the four automations (page viewed, form submitted, days since last engagement, added to list), manual enrollment, Breeze Assistant, or the beta workflow action.

## Install

### As a plugin (recommended)

Inside Claude Code:

```
/plugin marketplace add lifeofpi-lgtm/hubspot-prospecting-play-builder
/plugin install hubspot-prospecting-play-builder@hubspot-prospecting-play-builder
```

### Manually

```bash
git clone https://github.com/lifeofpi-lgtm/hubspot-prospecting-play-builder.git
cp -R hubspot-prospecting-play-builder/skills/hubspot-prospecting-play-builder ~/.claude/skills/
```

Or place it in a single project at `<project>/.claude/skills/hubspot-prospecting-play-builder/`. Keep the folder intact: `SKILL.md` links to its references, assets, and helper script.

## Usage

In Claude Code, type `/hubspot-prospecting-play-builder` followed by a URL, or just ask:

```
Use hubspot-prospecting-play-builder for https://your-company.com.
Research first, help me select one play, and guide me through preparing the content and setup kit.
```

Optional inputs that improve the kit: product documents, approved proof (case studies with permission), audience preferences, screenshots of the current HubSpot play editor or Agent Hub context, and relevant CRM exports. Web research requires a host with browsing. If it is unavailable, the skill says so.

## Validation helper

`scripts/kit.py` uses only the Python 3 standard library:

```sh
python3 scripts/kit.py validate-package             # checks the skill's own assets
python3 scripts/kit.py export-csv /path/to/client-kit
python3 scripts/kit.py validate-run /path/to/client-kit
```

`validate-run` checks required files for the chosen outreach method, the manifest, copy placeholders, the instruction character limit, the presence of a launch-readiness section, signal catalog coverage, table structure, and workbook or CSV fidelity, including literal handling of formula-looking text. It checks structure, not truth or copy quality. Those are reviewed against `references/validation-scenarios.md`.

## Files

```
skills/hubspot-prospecting-play-builder/
  SKILL.md                              workflow
  USAGE.md                              portable package notes
  references/
    hubspot-fields.md                   play editor map, methods, enrollment routes, defaults
    launch-readiness.md                 DNS check, admin checklist, exclusions, credit budget
    context-coaching.md                 framework for the three Selling context fields
    outreach-methodology.md             editorial defaults, follow-up roles, Sequence prompts
    signals-and-crm.md                  signal interpretation and CRM re-engagement mapping
    delivery-contract.md                required files, manifest, table layout
    validation-scenarios.md             behavioral review scenarios
  assets/
    advanced-instructions-base.txt      tailorable outreach instruction base
    signal-catalog.json                 49 signals with meanings and recommendations
    play-library.json                   eleven adaptable example plays
    crm-recipes.json                    eight CRM re-engagement mapping patterns
  scripts/kit.py                        validation and CSV export
  agents/openai.yaml                    optional interface metadata for other hosts
```

## Status and limitations

- Version 1.2.0, updated 2026-10-13: the call-to-action section of the instruction base now has a direct-approach version that replaces the reply-first default when the client chooses it, so the agent never receives two conflicting CTA rules.
- Version 1.1.0, updated 2026-10-02 to match HubSpot's current play editor (Adaptive and Sequence methods, Agent Hub context, documented enrollment routes) and to add launch readiness and stronger follow-up guidance.
- The skill has been exercised on synthetic scenarios and its helper has structural tests. It has **not yet been validated against a live HubSpot account's Test output**. Treat the first real run as a pilot and review every draft the agent produces.
- HubSpot documents no character limits for these fields. The 10,000-character ceiling for Advanced instructions comes from an observed account.
- Compliance notes (GDPR, PECR, CASL, CAN-SPAM) are practical flags, not legal advice.
- HubSpot features, signal lists, pricing, and trial terms change. The skill refreshes official pages each run, but always confirm in your own portal.

## License

[MIT](LICENSE)
