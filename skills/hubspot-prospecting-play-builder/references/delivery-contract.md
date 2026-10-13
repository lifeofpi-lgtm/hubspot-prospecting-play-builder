# Client kit delivery contract

Generate a separate client directory; never save client output inside the distributed skill. This contract lets the standard-library helper check completeness and fidelity. It does not constrain the prose in the guide.

## Required files

- `setup-guide.md`: research brief; selected offer/audience/motion; coaching for each field; source-grounded configuration recommendations; a **Launch readiness** section per [launch readiness](launch-readiness.md); pending decisions; ranked next three opportunities; preview checklist; what was and was not executed.
- `01-what-we-sell.txt`, `02-value-proposition.txt`, `03-pain-points.txt`, plus `04-advanced-instructions.txt` (Adaptive) or `04-sequence-steps.txt` (Sequence): plain text only, ready to paste when supported. No Markdown fences, commentary, citations, or unfinished placeholders. If evidence is insufficient for a field, leave it empty, mark the run draft, and record the gap instead of inventing copy.
- `illustrative-emails.md`: clearly labeled initial email and two follow-ups, each with subject, body, body word count, and factual basis or synthetic-scenario label. These are examples, not HubSpot-generated previews.
- `catalog.json`: run-specific copy of the packaged catalog, refreshed against the live table when possible. Keep names/source dates accurate and account availability explicit.
- `run.json`: manifest described below.
- `tables.json`: five populated table arrays described below.
- `play-workbook.xlsx` with the five tabs, or all five matching CSV files in `csv/`.

Deliver workbook plus guide/text to the client; machine-readable files support refresh and validation. Do not imply that planning output has changed HubSpot. Run `python3 scripts/kit.py validate-run /path/to/client-kit` before delivery.

## Manifest

`run.json` uses these fields:

| Field | Value |
| --- | --- |
| company_url | Supplied HTTP(S) company URL |
| prepared_on | ISO date, YYYY-MM-DD |
| selected_play_id | ID of the selected entry in Play Library |
| crm_mode | `none`, `export`, or `connector` |
| readiness | `draft` or `ready_for_preview`; this never means published |
| audience_confirmed / offer_confirmed | Boolean client decisions; do not mark inferred choices confirmed |
| catalog_status | `snapshot` or `refreshed` |
| catalog_refresh_source | Required for refreshed status: source URL or traceable source locator; catalog date must match this run |
| delivery_format | `xlsx` or `csv` |
| outreach_method | `adaptive` or `sequence`; decides the fourth copy file |

Additional useful fields may record preferences and pending settings. A URL-only run can be ready for a content preview while CRM mappings remain proposed, provided the selected Play does not depend on unverified CRM eligibility. Mark it draft when unresolved inputs materially affect its audience, offer, or feasibility.

## Table layout

`tables.json` is an object with exactly these five keys. Each value is an array of row objects; use scalar values, the exact column keys below, and no nested objects. Keep rows concise enough for a usable workbook. More detailed logic belongs in the guide. The helper prints errors for missing decisions, duplicate IDs, or missing signal coverage.

| Table / workbook tab | Column keys in order |
| --- | --- |
| Selected Play | `section`, `decision`, `recommendation`, `evidence_status`, `source_or_gap` |
| Signal Catalog | `signal_id`, `signal`, `category`, `object_level`, `meaning`, `prerequisites`, `use_cases`, `crm_reengagement`, `availability`, `source_url`, `checked_on` |
| CRM Reengagement | `mapping_id`, `trigger_type`, `trigger`, `required_data`, `associations`, `eligibility`, `timing`, `exclusions`, `owner`, `message_angle`, `enrollment_route`, `verification` |
| Play Library | `play_id`, `play`, `relationship`, `trigger`, `offer_angle`, `required_evidence`, `exclusions`, `cta`, `next_priority` |
| Evidence & Gaps | `item_id`, `type`, `claim_or_gap`, `source`, `checked_on`, `status`, `next_action` |

For Selected Play, include decisions named `offer`, `audience`, `persona`, `relationship`, `trigger`, `eligibility`, `exclusions`, `sender_owner`, `review_mode`, `outreach_method`, `cadence`, `send_window_timezone`, `cta_policy`, `stop_conditions`, `enrollment_route`, `deliverability`, and `credit_budget`. Extra decision rows are allowed. Use actual evidence statuses such as user-confirmed, supported, proposed, or pending.

Include every signal in the run's complete catalog exactly once. In `catalog.json`, `catalog_count` counts all rows; `documented_count` counts rows with `source_type: public_documentation`. Confirmed account-only additions use `source_type: account_observation`, their actual evidence locator, and an accurate date. Add those rows to both catalog and table, updating the total count without changing the public count. Do not add unverified names to satisfy a picker count. Public signals may remain unverified in the client's account.

CRM mappings must reference real field names only when verified. `proposed` means a blueprint; `schema verified; eligibility pending` distinguishes field availability from record eligibility. `verified` requires relevant data/associations and a supporting evidence locator in the guide. Do not show verified mappings in URL-only runs. Include CRM-only timing and renewal possibilities when relevant, or explain their irrelevance in Evidence & Gaps.

Use at least ten distinct Play Library rows adapted from the packaged library (it currently holds eleven). Mark unsuitable plays as not recommended and explain why rather than inventing fit. Rank only the best next opportunities; do not pretend all of them are ready. An approved resource must actually exist before a CTA offers it.

## Workbook and fallback

Use the host's spreadsheet tools/skill if available. Otherwise use an already available appropriate library. If no workbook authoring capability exists, use the helper's `export-csv` command; do not silently omit the tables or require a new subscription. CSV output is UTF-8 with BOM, properly quoted, and escapes formula-looking text. Explain that leading apostrophes protect literal content when importing.

For an XLSX, use the exact five tab names above, headers in row 1 and data from row 2. Freeze headers and identifier columns where useful; use filters, wrapped text, readable widths, adequate row heights, and restrained consistent styling. Preserve literal cell content rather than interpreting source text as formulas. Dates may be native spreadsheet dates formatted readably; source dates in JSON/CSV remain ISO. There are no business calculations requiring formulas in these reference tables.

Export `play-workbook.xlsx`. Inspect saved values against `tables.json`, verify every sheet visually with the host's render/preview tools when available, and report if visual validation was unavailable. Do not shrink text to conceal overflow. The helper checks saved sheet names and values but cannot assess layout. Keep test previews and build scripts out of the client-facing deliverable unless requested.

## Character limits and coverage

Count the entire Advanced Instructions text, including inserted Play-specific guidance and whitespace. Both code point and UTF-16 counts must be less than 10,000 (an observed limit, not a documented one); emoji can make them differ. Never silently truncate. Aim for useful headroom. Include a count table for all four paste-ready files in the setup guide, or save and link the helper's JSON validation report. Keep counts outside the text to paste. Record any other verified field limits separately rather than assuming the same limit everywhere.

The helper validates catalog rows against the run snapshot, not against the internet. A correct count does not establish live freshness or account availability. The packaged 49-signal set was reconciled against the documentation and one portal picker; a client's own picker may still differ (custom or integration signals, subscription gaps). Distinguish that reference observation from a newly inspected client account.
