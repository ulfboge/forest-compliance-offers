import { Client } from "@notionhq/client";
import fs from "fs/promises";
import path from "path";
import dotenv from "dotenv";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "../..");

dotenv.config({ path: path.resolve(repoRoot, ".env") });

const NOTION_TOKEN = process.env.NOTION_API_TOKEN;
if (!NOTION_TOKEN) {
  console.error(
    "Missing NOTION_API_TOKEN in .env (see tools/notion-sync/.env.example)."
  );
  process.exit(1);
}

const notion = new Client({ auth: NOTION_TOKEN });

const configPath = path.resolve(__dirname, "config.json");

async function loadConfig() {
  try {
    const data = await fs.readFile(configPath, "utf-8");
    return JSON.parse(data);
  } catch (err) {
    if (err.code === "ENOENT") {
      console.error(
        `Config file not found at ${configPath}. Copy config.example.json to config.json and edit mappings.`
      );
    } else {
      console.error("Failed to parse config.json:", err.message);
    }
    process.exit(1);
  }
}

function markdownToBlocks(markdown) {
  const blocks = [];
  const lines = markdown.split(/\r?\n/);
  let paragraphBuffer = [];

  const flushParagraph = () => {
    if (paragraphBuffer.length === 0) return;
    const text = paragraphBuffer.join(" ").trim();
    if (!text) {
      paragraphBuffer = [];
      return;
    }
    blocks.push(createParagraphBlock(text));
    paragraphBuffer = [];
  };

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();
    if (/^#{1,3}\s+/.test(line)) {
      flushParagraph();
      const level = line.match(/^#+/)[0].length;
      const content = line.replace(/^#{1,3}\s+/, "").trim();
      blocks.push(
        createHeadingBlock(Math.min(level, 3), content || "Untitled Heading")
      );
    } else if (line.trim() === "") {
      flushParagraph();
    } else if (/^[-*]\s+/.test(line)) {
      flushParagraph();
      const bulletText = line.replace(/^[-*]\s+/, "").trim();
      blocks.push(createBulletedListItem(bulletText));
    } else {
      paragraphBuffer.push(line);
    }
  }

  flushParagraph();
  return blocks;
}

function createHeadingBlock(level, text) {
  const key = `heading_${level}`;
  return {
    object: "block",
    type: key,
    [key]: {
      rich_text: [
        {
          type: "text",
          text: { content: text.slice(0, 2000) }
        }
      ]
    }
  };
}

function createParagraphBlock(text) {
  const chunks = chunkText(text, 2000);
  return {
    object: "block",
    type: "paragraph",
    paragraph: {
      rich_text: chunks.map((chunk) => ({
        type: "text",
        text: { content: chunk }
      }))
    }
  };
}

function createBulletedListItem(text) {
  const chunks = chunkText(text, 2000);
  return {
    object: "block",
    type: "bulleted_list_item",
    bulleted_list_item: {
      rich_text: chunks.map((chunk) => ({
        type: "text",
        text: { content: chunk }
      }))
    }
  };
}

function chunkText(text, size) {
  const output = [];
  for (let i = 0; i < text.length; i += size) {
    output.push(text.slice(i, i + size));
  }
  return output.length ? output : [""];
}

async function clearPageContent(pageId) {
  let cursor;
  const blockIds = [];
  do {
    const response = await notion.blocks.children.list({
      block_id: pageId,
      start_cursor: cursor,
      page_size: 100
    });
    response.results.forEach((block) => blockIds.push(block.id));
    cursor = response.has_more ? response.next_cursor : null;
  } while (cursor);

  for (const blockId of blockIds) {
    await notion.blocks.delete({ block_id: blockId });
  }
}

async function appendBlocks(pageId, blocks) {
  const chunkSize = 90;
  for (let i = 0; i < blocks.length; i += chunkSize) {
    const chunk = blocks.slice(i, i + chunkSize);
    await notion.blocks.children.append({
      block_id: pageId,
      children: chunk
    });
  }
}

async function syncFile(mapping) {
  const filePath = path.resolve(repoRoot, mapping.file);
  let markdown;
  try {
    markdown = await fs.readFile(filePath, "utf-8");
  } catch (err) {
    console.error(`Failed to read ${mapping.file}: ${err.message}`);
    return;
  }

  const pageId = mapping.page_id;
  if (!pageId) {
    console.warn(`Skipping ${mapping.file}: missing page_id in config.`);
    return;
  }

  console.log(`Syncing ${mapping.file} -> Notion page ${pageId}`);

  const blocks = markdownToBlocks(markdown);
  try {
    await clearPageContent(pageId);
    if (blocks.length) {
      await appendBlocks(pageId, blocks);
    }
    await notion.pages.update({
      page_id: pageId,
      properties: {
        "Last Sync": {
          date: { start: new Date().toISOString() }
        }
      }
    });
  } catch (err) {
    console.error(`Failed to update page ${pageId}: ${err.message}`);
  }
}

async function main() {
  const config = await loadConfig();
  if (!Array.isArray(config.sync_map)) {
    console.error("config.json must define a sync_map array.");
    process.exit(1);
  }

  for (const mapping of config.sync_map) {
    await syncFile(mapping);
  }
}

main().catch((err) => {
  console.error("Sync failed:", err);
  process.exit(1);
});

