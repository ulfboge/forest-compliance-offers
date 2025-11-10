# Notion Sync Helper

This lightweight Node script pushes Markdown content from this repository into specific Notion pages so the team can co-edit in Cursor/GitHub and review/share in Notion.

## 1. Prerequisites

1. Create a Notion [integration token](https://www.notion.so/my-integrations).
2. Share the target Notion pages (or database) with that integration.
3. Install Node.js 18+ on your workstation.

## 2. Configure

1. From the repository root, copy the sample env file:

   ```bash
   cp tools/notion-sync/env.example .env
   ```

   Edit `.env` and paste your Notion integration token as `NOTION_API_TOKEN=...`.

2. Copy the config template and map repository files to Notion page IDs:

   ```bash
   cp tools/notion-sync/config.example.json tools/notion-sync/config.json
   ```

   Update `config.json` so each entry specifies:

   - `file`: path to the Markdown file in this repo
   - `page_id`: 32-character Notion page ID (without dashes)

3. Install dependencies:

   ```bash
   cd tools/notion-sync
   npm install
   cd ../..
   ```

## 3. Run

Whenever you want to sync the latest Markdown to Notion:

```bash
cd tools/notion-sync
npm run sync
cd ../..
```

The script will:

1. Read each file in `sync_map`.
2. Convert basic Markdown (headings, paragraphs, bullet lists) into Notion blocks.
3. Replace the target page’s content with the generated blocks.
4. Update the page property `Last Sync` (create a Date property with that name).

> Tip: schedule the command or add it as a Git hook if you want automatic syncs.

## 4. Notes & Limitations

- Currently supports headings (`#` to `###`), paragraphs, and bullet lists.
- Existing comments or discussion threads inside Notion remain intact.
- The script clears and rewrites page content on each run—avoid manual edits directly in those pages unless they are captured upstream in Markdown.
- Extend `markdownToBlocks` within `sync_to_notion.js` if you need richer formatting (numbered lists, callouts, etc.).

