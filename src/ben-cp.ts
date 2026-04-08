import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";

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
      name: "write_changelog_entry",
      description: "Write a structured changelog entry at the end of a session. Writes a detailed entry to a subdirectory changelog first (if subdirectory provided), then a summary entry to root changelog.md. Call this at the end of every session.",
      inputSchema: {
        type: "object",
        properties: {
          session_goal: {
            type: "string",
            description: "One sentence: what was this session trying to accomplish?"
          },
          subdirectory: {
            type: "string",
            description: "The skills/ subdirectory primarily worked in this session (e.g. 'okr-reporting'). If provided, a detailed entry is written to skills/[subdirectory]/changelog.md first."
          },
          version_bump: {
            type: "string",
            enum: ["patch", "minor", "major"],
            description: "How to increment the root changelog version. patch=routine work, minor=structural changes/new skills, major=vault-wide rearchitecture. Defaults to patch."
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
            description: "Writes denied, failed, or left incomplete — critical for preventing repeat mistakes",
            items: {
              type: "object",
              properties: {
                attempted: { type: "string" },
                happened: { type: "string" },
                recommendation: { type: "string", description: "What to do instead (or avoid)" }
              },
              required: ["attempted", "happened", "recommendation"]
            }
          },
          kr_state: {
            type: "array",
            description: "State of any KR or task in progress (okr-reporting sessions)",
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
          blockers: {
            type: "array",
            description: "Unresolved blockers at session end",
            items: {
              type: "object",
              properties: {
                description: { type: "string" },
                needed_to_unblock: { type: "string" }
              },
              required: ["description", "needed_to_unblock"]
            }
          },
          next_tasks: {
            type: "array",
            description: "Ordered list of next tasks for the following session",
            items: { type: "string" }
          }
        },
        required: ["session_goal", "completed_work", "next_tasks"]
      }
    },
    {
      name: "run_status_report",
      description: "Run the Platform Weekly Status Report pipeline. Executes full_run.py --force for the specified team and returns the output path when complete.",
      inputSchema: {
        type: "object",
        properties: {
          team: {
            type: "string",
            enum: ["platform", "reporting"],
            description: "Team to run the report for. Defaults to 'platform'."
          }
        }
      }
    },
    {
      name: "get_changelog",
      description: "Read the root changelog.md. Call this at the start of a session to load context from previous sessions.",
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
    if (name === "write_changelog_entry") {
      const a = args as any;
      const date = new Date().toISOString().split('T')[0];
      const rootChangelogPath = path.resolve(__dirname, "../changelog.md");
      const written: string[] = [];

      // --- Build reusable sections ---
      const changesLines = (a.completed_work as any[]).map((w: any) =>
        `- \`${w.path}\` — ${w.change} ${w.status}`
      ).join("\n");

      const failedLines = (a.failed_actions ?? []).length > 0
        ? (a.failed_actions as any[]).map((f: any) =>
            `- **Attempted:** ${f.attempted}\n  **Happened:** ${f.happened}\n  **Recommendation:** ${f.recommendation}`
          ).join("\n")
        : null;

      const krLines = (a.kr_state ?? []).length > 0
        ? (a.kr_state as any[]).map((k: any) =>
            `- **${k.kr_name}** (\`${k.file_path}\`): ${k.blocker_status}` +
            (k.baseline ? ` — baseline ${k.baseline}` : "") +
            (k.target ? `, target ${k.target}` : "") +
            `\n  Next: ${k.next_action}`
          ).join("\n")
        : null;

      const blockerLines = (a.blockers ?? []).length > 0
        ? (a.blockers as any[]).map((b: any) =>
            `- ${b.description} — ${b.needed_to_unblock}`
          ).join("\n")
        : null;

      const nextLines = (a.next_tasks as string[]).map((t, i) =>
        `${i + 1}. ${t}`
      ).join("\n");

      // --- Stage 1: Subdirectory changelog (if provided) ---
      if (a.subdirectory) {
        const subDir = String(a.subdirectory).replace(/[^a-z0-9\-_]/gi, "");
        const subPath = path.resolve(skillsPath, subDir, "changelog.md");
        let subContent: string;
        try {
          subContent = await fs.readFile(subPath, "utf-8");
        } catch {
          const skillName = subDir.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase());
          subContent = `# ${skillName} Changelog\n\n> Detail log for \`skills/${subDir}/\`. See root \`changelog.md\` for version history.\n\n---\n\n## [Unreleased]\n`;
        }

        let subEntry = `## ${date} — ${a.session_goal}\n\n**Files changed:**\n${changesLines}\n`;
        if (krLines) subEntry += `\n**KR State:**\n${krLines}\n`;
        if (failedLines) subEntry += `\n**Failed actions:**\n${failedLines}\n`;
        if (blockerLines) subEntry += `\n**Blockers:**\n${blockerLines}\n`;
        subEntry += `\n**Next:** ${(a.next_tasks as string[])[0] ?? "—"}\n`;

        const updatedSub = subContent.replace("## [Unreleased]", `## [Unreleased]\n\n${subEntry}`);
        await fs.writeFile(subPath, updatedSub, "utf-8");
        written.push(subPath);
      }

      // --- Stage 2: Root changelog ---
      const rootContent = await fs.readFile(rootChangelogPath, "utf-8");

      // Auto-increment version
      const versionMatch = rootContent.match(/## \[(\d+)\.(\d+)\.(\d+)\]/);
      let newVersion = "1.0.0";
      if (versionMatch) {
        const [maj, min, pat] = [parseInt(versionMatch[1]), parseInt(versionMatch[2]), parseInt(versionMatch[3])];
        const bump = a.version_bump ?? "patch";
        newVersion = bump === "major" ? `${maj + 1}.0.0`
          : bump === "minor" ? `${maj}.${min + 1}.0`
          : `${maj}.${min}.${pat + 1}`;
      }

      // Root entry: one-liner per file + pointer to subdirectory if applicable
      const rootChanges = (a.completed_work as any[]).map((w: any) =>
        `- \`${w.path}\` — ${w.change}`
      ).join("\n");
      const subPointer = a.subdirectory
        ? `\n> Full detail: see \`skills/${a.subdirectory}/changelog.md\``
        : "";

      let rootEntry = `## [${newVersion}] — ${a.session_goal} (${date})${subPointer}\n\n**Changes:**\n${rootChanges}\n`;
      if (blockerLines) rootEntry += `\n**Blockers:**\n${blockerLines}\n`;
      rootEntry += `\n**Next Tasks:**\n${nextLines}\n`;

      const updatedRoot = rootContent.replace("## [Unreleased]", `## [Unreleased]\n\n${rootEntry}`);
      await fs.writeFile(rootChangelogPath, updatedRoot, "utf-8");
      written.push(rootChangelogPath);

      return { content: [{ type: "text", text: `Changelog entries written:\n${written.join("\n")}` }] };
    }
    if (name === "run_status_report") {
      const team = String((args as any)?.team ?? "platform");
      if (!["platform", "reporting"].includes(team)) {
        throw new Error(`Invalid team: '${team}'. Must be 'platform' or 'reporting'.`);
      }
      const scriptPath = path.resolve(skillsPath, "project-status-reports/scripts/full_run.py");
      const cwd = path.resolve(__dirname, "..");
      const cmdArgs = ["--force", "--team", team];

      const output = await new Promise<string>((resolve, reject) => {
        execFile("python3", [scriptPath, ...cmdArgs], { cwd, timeout: 300_000 }, (err, stdout, stderr) => {
          if (err) reject(new Error(stderr || err.message));
          else resolve(stdout || "Pipeline completed with no output.");
        });
      });

      return { content: [{ type: "text", text: output }] };
    }
    if (name === "get_changelog") {
      const rootChangelogPath = path.resolve(__dirname, "../changelog.md");
      try {
        const content = await fs.readFile(rootChangelogPath, "utf-8");
        return { content: [{ type: "text", text: content }] };
      } catch {
        return { content: [{ type: "text", text: "No changelog found." }] };
      }
    }
    throw new Error(`Tool not found: ${name}`);
  } catch (error: any) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);