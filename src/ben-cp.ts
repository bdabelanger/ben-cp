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
const rootChangelogPath = path.resolve(__dirname, "../changelog.md");
const handoffPath = path.resolve(__dirname, "../handoff");

async function writeChangelogInternal(a: any, skillsPath: string, date: string): Promise<string[]> {
  const written: string[] = [];

  // Normalize subdirectories — accept legacy single string or new array
  const rawSubs: string[] = Array.isArray(a.subdirectories)
    ? a.subdirectories
    : a.subdirectory
      ? [String(a.subdirectory)]
      : [];

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

  const handoffRef = a.handoff ? `handoff/${String(a.handoff)}` : null;

  // --- Stage 1: Subdirectory changelogs (deepest first) ---
  for (const rawSub of rawSubs) {
    const subDir = rawSub.replace(/[^a-z0-9\-_]/gi, "");
    const subPath = path.resolve(skillsPath, subDir, "changelog.md");
    
    // Ensure the skill subdirectory exists before writing
    await fs.mkdir(path.dirname(subPath), { recursive: true });

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
    if (handoffRef) subEntry += `\n**Handoff:** \`${handoffRef}\`\n`;
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

  // Root entry: one-liner per file, pointer(s) to subdirectory changelogs
  const rootChanges = (a.completed_work as any[]).map((w: any) =>
    `- \`${w.path}\` — ${w.change}`
  ).join("\n");

  const subPointers = rawSubs.length > 0
    ? "\n\n**Detail logs:**\n" + rawSubs.map(s => `- \`skills/${s}/changelog.md\``).join("\n")
    : "";

  let rootEntry = `## [${newVersion}] — ${a.session_goal} (${date})${subPointers}\n\n**Changes:**\n${rootChanges}\n`;
  if (failedLines) rootEntry += `\n**Failed actions:**\n${failedLines}\n`;
  if (blockerLines) rootEntry += `\n**Blockers:**\n${blockerLines}\n`;
  if (handoffRef) rootEntry += `\n**Handoff:** \`${handoffRef}\`\n`;
  rootEntry += `\n**Next Tasks:**\n${nextLines}\n`;

  const updatedRoot = rootContent.replace("## [Unreleased]", `## [Unreleased]\n\n${rootEntry}`);
  await fs.writeFile(rootChangelogPath, updatedRoot, "utf-8");
  written.push(rootChangelogPath);

  return written;
}

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
          subdirectories: {
            type: "array",
            description: "skills/ subdirectories touched this session (e.g. ['okr-reporting', 'crypt-keeper']). A detailed entry is written to each skills/[name]/changelog.md before the root entry.",
            items: { type: "string" }
          },
          handoff: {
            type: "string",
            description: "Filename of the handoff that triggered this session (e.g. '2026-04-08-changelog-refactor-COMPLETE.md'). Omit if not handoff-driven. Added to both subdirectory and root entries."
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
      description: "Read a changelog. Pass scope='root' (default) for root changelog.md, or a subdirectory path like 'skills/okr-reporting' for a skill-level changelog. Call at session start to load recent context.",
      inputSchema: {
        type: "object",
        properties: {
          scope: {
            type: "string",
            description: "Which changelog to read. 'root' (default) reads root changelog.md. A subdirectory path like 'skills/okr-reporting' reads skills/okr-reporting/changelog.md."
          }
        }
      }
    },
    {
      name: "list_handoffs",
      description: "List open or completed handoffs",
      inputSchema: {
        type: "object",
        properties: {
          status: { type: "string", enum: ["READY", "COMPLETE", "ALL"], description: "Filter by status" },
          limit: { type: "number", description: "Maximum number of handoffs to return" }
        }
      }
    },
    {
      name: "read_handoff",
      description: "Read a specific handoff file",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Path relative to handoff/ directory" }
        },
        required: ["path"]
      }
    },
    {
      name: "write_handoff",
      description: "Create a new handoff file",
      inputSchema: {
        type: "object",
        properties: {
          title: { type: "string", description: "Short kebab-case title" },
          priority: { type: "string", enum: ["P1", "P2", "P3", "P4"] },
          content: { type: "string", description: "The execution plan or context" },
          assigned_to: { type: "string", description: "Agent assigned to the task" }
        },
        required: ["title", "priority", "content"]
      }
    },
    {
      name: "edit_handoff",
      description: "Edit an existing handoff file",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Path relative to handoff/ directory" },
          content: { type: "string", description: "New full content for the handoff" }
        },
        required: ["path", "content"]
      }
    },
    {
      name: "complete_handoff",
      description: "Mark a handoff as complete, move it, and write changelog entries.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Path to the open handoff (relative to handoff/ directory)" },
          summary: { type: "string", description: "One-paragraph summary of what was done" },
          session_goal: { type: "string", description: "For the changelog: what was accomplished?" },
          completed_work: {
            type: "array",
            items: {
              type: "object",
              properties: {
                path: { type: "string" },
                change: { type: "string" },
                status: { type: "string", enum: ["✅ Complete", "🟡 Partial", "⚠️ Needs review"] }
              },
              required: ["path", "change", "status"]
            }
          },
          next_tasks: { type: "array", items: { type: "string" } },
          subdirectories: { type: "array", items: { type: "string" } },
          version_bump: { type: "string", enum: ["patch", "minor", "major"] }
        },
        required: ["path", "summary", "session_goal", "completed_work", "next_tasks"]
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    if (name === "get_skill") {
      const rel = String(args?.relativePath);
      const normalized = rel.startsWith("skills/") ? rel.slice(7) : rel.startsWith("sop/") ? rel.slice(4) : rel;
      const fullPath = path.resolve(skillsPath, normalized);
      
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
      const written = await writeChangelogInternal(a, skillsPath, date);
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
      const scope = String((args as any)?.scope ?? "root").trim();
      let changelogPath: string;
      if (!scope || scope === "root") {
        changelogPath = path.resolve(__dirname, "../changelog.md");
      } else {
        // Accept 'skills/okr-reporting' or just 'okr-reporting'
        const normalized = scope.startsWith("skills/") ? scope.slice("skills/".length) : scope;
        const clean = normalized.replace(/[^a-z0-9\-_/]/gi, "");
        changelogPath = path.resolve(skillsPath, clean, "changelog.md");
      }
      try {
        const content = await fs.readFile(changelogPath, "utf-8");
        return { content: [{ type: "text", text: content }] };
      } catch {
        return { content: [{ type: "text", text: `No changelog found at: ${changelogPath}` }] };
      }
    }
    if (name === "list_handoffs") {
      const { status = "READY", limit } = args as any;
      const results: any[] = [];
      const dirs: string[] = [];
      
      if (status === "READY" || status === "ALL") dirs.push(path.join(handoffPath));
      if (status === "COMPLETE" || status === "ALL") dirs.push(path.join(handoffPath, "complete"));

      for (const dir of dirs) {
        try {
          const files = await fs.readdir(dir);
          for (const file of files) {
            if (!file.endsWith(".md")) continue;
            const fullPath = path.join(dir, file);
            const content = await fs.readFile(fullPath, "utf-8");
            
            // Basic metadata extraction
            const priorityMatch = content.match(/> \*\*Priority:\*\* (P\d)/);
            const statusMatch = content.match(/> \*\*STATUS:\*\* (.*?)$/m);
            const dateMatch = file.match(/^(\d{4}-\d{2}-\d{2})/);

            results.push({
              file,
              path: path.relative(path.resolve(handoffPath, ".."), fullPath),
              priority: priorityMatch ? priorityMatch[1] : "TBD",
              status: statusMatch ? statusMatch[1].trim() : (dir.endsWith("complete") ? "COMPLETE" : "READY"),
              date: dateMatch ? dateMatch[1] : "unknown"
            });
          }
        } catch (e) {
          // Ignore directory missing
        }
      }

      // Sort by date desc, then priority
      results.sort((a, b) => b.date.localeCompare(a.date) || a.priority.localeCompare(b.priority));
      const finalResults = limit ? results.slice(0, limit) : results;
      
      return { content: [{ type: "text", text: JSON.stringify(finalResults, null, 2) }] };
    }
    if (name === "read_handoff") {
      const { path: relPath } = args as any;
      const normalized = String(relPath).startsWith("handoff/") ? String(relPath).slice(8) : relPath;
      const fullPath = path.resolve(handoffPath, normalized);
      if (!fullPath.startsWith(handoffPath)) throw new Error("Access denied: Invalid path");
      
      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }
    if (name === "write_handoff") {
      const { title, priority, content, assigned_to = "Any" } = args as any;
      const date = new Date().toISOString().split('T')[0];
      const filename = `${date}-${priority.toLowerCase()}-${title.replace(/\s+/g, '-')}.md`;
      const fullPath = path.join(handoffPath, filename);

      const header = `# Implementation Plan: ${title}\n\n` +
        `> **Prepared by:** Antigravity (Gemini) (${date})\n` +
        `> **Assigned to:** ${assigned_to}\n` +
        `> **Vault root:** /Users/benbelanger/GitHub/ben-cp\n` +
        `> **Priority:** ${priority}\n` +
        `> **v1.0**\n` +
        `> **STATUS: 🔲 READY — pick up ${date}**\n\n` +
        `---\n\n`;

      await fs.writeFile(fullPath, header + content, "utf-8");
      return { content: [{ type: "text", text: `Handoff created: ${filename}` }] };
    }
    if (name === "edit_handoff") {
      const { path: relPath, content } = args as any;
      const normalized = String(relPath).startsWith("handoff/") ? String(relPath).slice(8) : relPath;
      const fullPath = path.resolve(handoffPath, normalized);
      if (!fullPath.startsWith(handoffPath)) throw new Error("Access denied: Invalid path");

      await fs.writeFile(fullPath, content, "utf-8");
      return { content: [{ type: "text", text: `Handoff updated: ${relPath}` }] };
    }
    if (name === "complete_handoff") {
      const a = args as any;
      const relPath = String(a.path);
      const normalized = relPath.startsWith("handoff/") ? relPath.slice(8) : relPath;
      const sourcePath = path.resolve(handoffPath, normalized);
      if (!sourcePath.startsWith(handoffPath)) throw new Error("Access denied: Invalid path");

      const date = new Date().toISOString().split('T')[0];
      const filename = path.basename(relPath, ".md");
      const targetFilename = `${filename}-COMPLETE.md`;
      const targetPath = path.join(handoffPath, "complete", targetFilename);

      // 1. Read and update the file content
      const content = await fs.readFile(sourcePath, "utf-8");
      const summaryHeader = `> **STATUS: ✅ COMPLETE — ${date}**\n\n${a.summary}\n\n**Changelog:** (see root changelog.md)\n`;
      
      const updatedContent = content.replace(/> \*\*STATUS: 🔲 READY.*$/m, summaryHeader);
      
      // 2. Move and Save
      await fs.mkdir(path.join(handoffPath, "complete"), { recursive: true });
      await fs.writeFile(targetPath, updatedContent, "utf-8");
      await fs.unlink(sourcePath);

      // 3. Trigger Changelog
      const changelogArgs = {
        ...a,
        handoff: `complete/${targetFilename}`
      };
      const written = await writeChangelogInternal(changelogArgs, skillsPath, date);

      return { content: [{ type: "text", text: `Handoff marked complete and moved to ${targetFilename}.\nChangelog entries written:\n${written.join("\n")}` }] };
    }
    throw new Error(`Tool not found: ${name}`);
  } catch (error: any) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);