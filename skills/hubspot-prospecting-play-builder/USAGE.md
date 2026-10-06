# Using this portable package

Keep this folder intact: `SKILL.md` links to its supporting references, assets, and optional Python helper. Supply the whole folder to an assistant that can read skill files. Follow that host's supported skill-import process if you want persistent discovery. This package does not install itself.

Start with:

> Use hubspot-prospecting-play-builder for https://your-company.com. Research first, help me select one Play, and guide me through preparing the content and setup kit.

Optional inputs: product documents, approved proof, audience preferences, current HubSpot screenshots, and relevant CRM exports. CRM access is not required. Store client inputs and generated kits outside this reusable folder.

The core workflow is Markdown and JSON. `agents/openai.yaml` supplies optional Codex interface metadata. The helper requires Python 3 and only its standard library; workbook creation uses whatever spreadsheet capability the host provides, with equivalent CSVs as the fallback. Web research still requires the host to provide browsing. If it cannot, the skill must disclose the limitation.

The result prepares one Play, a library of adaptable example Plays, copy for HubSpot, and configuration recommendations. It does not publish, enroll, or send. Review the setup guide and unresolved decisions before configuring HubSpot yourself.
