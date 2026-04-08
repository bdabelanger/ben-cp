import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const server = new Server(
  { name: "ben-cp", version: "2.0.0" },
  { capabilities: { tools: {} } }
);

// Automatically find the 'skills' folder relative to this file's location
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillsPath = path.resolve(__dirname, "../skills");

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_skill",
      description: "Read a Casebook SOP or Skill template from the repo",
      inputSchema: {
        type: "object",
        properties: {
          relativePath: { type: "string", description: "Path relative to /sop (e.g. 'rovo/rovo-sop.md')" }
        },
        required: ["relativePath"]
      }
    },
    {
      name: "list_vault",
      description: "List all files available in the SOP vault",
      inputSchema: { type: "object", properties: {} }
    },
    {
      name: "write_gemma_wrap_up",
      description: "Write a structured session wrap-up for Gemma to load at the start of the next session. Call this at the end of every Gemma session.",
      inputSchema: {
        type: "object",
        properties: {
          session_goal: {
            type: "string",
            description: "One sentence: what was this session trying to accomplish?"
          },
          completed_work: {
            type: "array",
            description: "Files created or successfully modified",
            items: {
              type: "object",
              properties: {
                path: { type: "string", description: "Full absolute path" },
                change: { type: "string", description: "What changed (one line)" },
                status: { type: "string", enum: ["✅ Complete", "🟡 Partial", "⚠️ Needs review"] }
              },
              required: ["path", "change", "status"]
            }
          },
          failed_actions: {
            type: "array",
            description: "Writes denied, failed, or left incomplete — critical for preventing Gemma repeating mistakes",
            items: {
              type: "object",
              properties: {
                attempted: { type: "string" },
                happened: { type: "string" },
                recommendation: { type: "string", description: "What Gemma should do instead (or avoid)" }
              },
              required: ["attempted", "happened", "recommendation"]
            }
          },
          kr_state: {
            type: "array",
            description: "State of any KR or task in progress",
            items: {
              type: "object",
              properties: {
                kr_name: { type: "string" },
                file_path: { type: "string" },
                baseline: { type: "string" },
                target: { type: "string" },
                blocker_status: { type: "string", enum: ["✅ Unblocked", "🟡 Partial", "🛑 Blocked"] },
                next_action: { type: "string" }
              },
              required: ["kr_name", "file_path", "blocker_status", "next_action"]
            }
          },
          do_not_touch: {
            type: "array",
            description: "Files Gemma must not modify without explicit instruction from Ben",
            items: {
              type: "object",
              properties: {
                path: { type: "string" },
                reason: { type: "string" }
              },
              required: ["path", "reason"]
            }
          },
          next_task: {
            type: "string",
            description: "One clear, specific task Gemma should propose at the start of the next session — written as a directive she can read aloud"
          }
        },
        required: ["session_goal", "completed_work", "next_task"]
      }
    },
    {
      name: "get_gemma_wrap_up",
      description: "Load the most recent Gemma session wrap-up. Call this at the start of every Gemma session to restore context from the previous session.",
      inputSchema: { type: "object", properties: {} }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    if (name === "get_skill") {
      const fullPath = path.resolve(skillsPath, String(args?.relativePath));
      
      // Prevent path traversal outside of the skillsPath
      if (!fullPath.startsWith(path.resolve(skillsPath))) {
        throw new Error("Access denied: Invalid path");
      }

      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }
    if (name === "list_vault") {
      const allItems = await fs.readdir(skillsPath, { recursive: true, withFileTypes: true });
      const files = allItems
        .filter(dirent => dirent.isFile() && !dirent.name.startsWith('.'))
        .map(dirent => path.join(dirent.parentPath, dirent.name).replace(skillsPath + path.sep, ''));

      return { content: [{ type: "text", text: files.join("\n") }] };
    }
    if (name === "write_gemma_wrap_up") {
      const a = args as any;
      const date = new Date().toISOString().split('T')[0];

      const completedSection = (a.completed_work ?? []).length > 0
        ? (a.completed_work as any[]).map((w: any) =>
            `- \`${w.path}\` — ${w.change} ${w.status}`
          ).join("\n")
        : "_None_";

      const failedSection = (a.failed_actions ?? []).length > 0
        ? (a.failed_actions as any[]).map((f: any) =>
            `- **Attempted:** ${f.attempted}\n  **Happened:** ${f.happened}\n  **Recommendation:** ${f.recommendation}`
          ).join("\n")
        : "_None_";

      const krSection = (a.kr_state ?? []).length > 0
        ? (a.kr_state as any[]).map((k: any) =>
            `- **${k.kr_name}** (\`${k.file_path}\`)\n` +
            (k.baseline ? `  - Baseline: ${k.baseline}\n` : "") +
            (k.target ? `  - Target: ${k.target}\n` : "") +
            `  - Blocker: ${k.blocker_status}\n` +
            `  - Next action: ${k.next_action}`
          ).join("\n")
        : "_None_";

      const doNotTouchSection = (a.do_not_touch ?? []).length > 0
        ? (a.do_not_touch as any[]).map((d: any) =>
            `- \`${d.path}\` — ${d.reason}`
          ).join("\n")
        : "_None_";

      const directive = `## 🔒 Directive Reminder
- Read AGENTS.md at /Users/benbelanger/GitHub/ben-cp/AGENTS.md before any action
- Read gemma-rules.md at /Users/benbelanger/GitHub/ben-cp/gemma-rules.md before any action
- ALWAYS read a file before writing or editing it
- Use edit_file for changes to existing files; write_file for NEW files only
- All SOP files go in /Users/benbelanger/GitHub/ben-cp/skills/
- OKR KR files go in /Users/benbelanger/GitHub/ben-cp/skills/okr-reporting/
- After creating any file, update the parent directory's index.md
- End every session by invoking the write_gemma_wrap_up tool`;

      const content = `# Gemma Session Wrap-Up — ${date}

## Session Goal
${a.session_goal}

## Completed Work
${completedSection}

## Failed or Incomplete Actions
${failedSection}

## Current KR / Task State
${krSection}

## Files Gemma Must NOT Touch
${doNotTouchSection}

## Immediate Next Task (Suggested)
${a.next_task}

${directive}
`;

      const wrapUpPath = path.resolve(skillsPath, "gemma-wrap-up-latest.md");
      await fs.writeFile(wrapUpPath, content, "utf-8");
      return { content: [{ type: "text", text: `Wrap-up written to ${wrapUpPath}` }] };
    }
    if (name === "get_gemma_wrap_up") {
      const wrapUpPath = path.resolve(skillsPath, "gemma-wrap-up-latest.md");
      try {
        const content = await fs.readFile(wrapUpPath, "utf-8");
        return { content: [{ type: "text", text: content }] };
      } catch {
        return { content: [{ type: "text", text: "No wrap-up found. This appears to be the first session." }] };
      }
    }
    throw new Error(`Tool not found: ${name}`);
  } catch (error: any) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);