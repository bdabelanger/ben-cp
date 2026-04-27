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
import https from "node:https";

// Load .env from vault root
async function loadEnv(rootPath: string) {
  try {
    const raw = await fs.readFile(path.resolve(rootPath, ".env"), "utf-8");
    for (const line of raw.split("\n")) {
      const m = line.match(/^([A-Z_][A-Z0-9_]*)=[\'\"']?(.+?)[\'\"']?\s*$/);
      if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
    }
  } catch { }
}

function httpsRequest(url: string, method: string, headers: Record<string, string>, body?: string): Promise<{ status: number; data: string }> {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = https.request({ hostname: u.hostname, path: u.pathname + u.search, method, headers }, (res) => {
      let data = "";
      res.on("data", (d) => data += d);
      res.on("end", () => resolve({ status: res.statusCode ?? 0, data }));
    });
    req.on("error", reject);
    if (body) req.write(body);
    req.end();
  });
}

const server = new Server(
  { name: "ben-cp", version: "2.1.1" },
  { capabilities: { tools: {} } }
);

// Automatically find the vault root relative to this file's location
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootPath = path.resolve(__dirname, "..");
await loadEnv(rootPath);
const skillsPath = path.resolve(rootPath, "skills");
const rootChangelogPath = path.resolve(rootPath, "changelog.md");
const handoffPath = path.resolve(rootPath, "handoffs");


function ensureSingleExtension(filename: string, ext: string = ".md"): string {
  if (filename.endsWith(ext)) return filename;
  return filename + ext;
}

async function writeChangelogInternal(a: any, skillsPath: string, date: string): Promise<string[]> {
  const written: string[] = [];
  const rawSubs: string[] = Array.isArray(a.subdirectories) ? a.subdirectories : [];
  const changesLines = (a.completed_work ?? []).map((w: any) => `- \`${w.path}\` — ${w.change} ${w.status}`).join("\n");
  const failedLines = (a.failed_actions ?? []).length > 0 ? (a.failed_actions as any[]).map((f: any) => `- **Attempted:** ${f.attempted}\n  **Happened:** ${f.happened}\n  **Recommendation:** ${f.recommendation}`).join("\n") : null;
  const krLines = (a.kr_state ?? []).length > 0 ? (a.kr_state as any[]).map((k: any) => `- **${k.kr_name}** (\`${k.file_path}\`): ${k.blocker_status}${k.baseline ? ` — baseline ${k.baseline}` : ""}${k.target ? `, target ${k.target}` : ""}\n  Next: ${k.next_action}`).join("\n") : null;
  const blockerLines = (a.blockers ?? []).length > 0 ? (a.blockers as any[]).map((b: any) => `- ${b.description} — ${b.needed_to_unblock}`).join("\n") : null;
  const nextLines = (a.next_tasks ?? []).map((t: any, i: number) => `${i + 1}. ${t}`).join("\n");
  const handoffRef = a.handoff ? `handoffs/${String(a.handoff)}` : null;

  for (const rawSub of rawSubs) {
    const subDir = rawSub.replace(/[^a-z0-9\-_/]/gi, "");
    const subPath = path.resolve(skillsPath, subDir, "changelog.md");
    await fs.mkdir(path.dirname(subPath), { recursive: true });
    let subContent: string;
    try { subContent = await fs.readFile(subPath, "utf-8"); } catch {
      const skillName = subDir.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase());
      subContent = `# ${skillName} Changelog\n\n## [Unreleased]\n`;
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

  const rootContent = await fs.readFile(rootChangelogPath, "utf-8");
  const versionMatch = rootContent.match(/## \[(\d+)\.(\d+)\.(\d+)\]/);
  let newVersion = "1.0.0";
  if (versionMatch) {
    const [maj, min, pat] = [parseInt(versionMatch[1]), parseInt(versionMatch[2]), parseInt(versionMatch[3])];
    const bump = a.version_bump ?? "patch";
    newVersion = bump === "major" ? `${maj + 1}.0.0` : bump === "minor" ? `${maj}.${min + 1}.0` : `${maj}.${min}.${pat + 1}`;
  }
  const rootChanges = (a.completed_work ?? []).map((w: any) => `- \`${w.path}\` — ${w.change}`).join("\n");
  const subPointers = rawSubs.length > 0 ? "\n\n**Detail logs:**\n" + rawSubs.map(s => `- \`skills/${s}/changelog.md\``).join("\n") : "";
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
    // --- AGENT ROLES & GOVERNANCE ---
    {
      name: "get_agent_info",
      description: "Retrieve central governance (AGENTS.md) and all agent role documentation. Use this at the start of every session to establish your persona and rules. Returns AGENTS.md and ALL role files in one fetch.",
      inputSchema: {
        type: "object",
        properties: {
          agent_id: { type: "string", description: "The ID of the agent to highlight at the end of the response (e.g. 'gemma', 'code')." }
        }
      }
    },

    // --- SKILLS & CAPABILITIES ---
    { name: "list_skills", description: "List all files available in the skills domain", inputSchema: { type: "object", properties: { domain: { type: "string", description: "Optional subdirectory within skills/" } } } },
    { name: "get_skill", description: "Read a Skill documentation or template from the repo", inputSchema: { type: "object", properties: { relativePath: { type: "string" } }, required: ["relativePath"] } },



    // --- HANDOFFS & EXECUTION ---
    {
      name: "add_handoff",
      description: "Create a new handoff file",
      inputSchema: {
        type: "object",
        properties: {
          title: { type: "string" },
          priority: { type: "string", enum: ["P1", "P2", "P3", "P4"] },
          content: { type: "string" },
          assigned_to: { type: "string" }
        },
        required: ["title", "priority", "content"]
      }
    },
    { name: "list_handoffs", description: "List handoffs. Use assigned_to to filter to your agent name (e.g. 'Gemma'). Returns file, path, priority, status, date, assigned_to.", inputSchema: { type: "object", properties: { status: { type: "string", enum: ["READY", "COMPLETE", "ALL"] }, limit: { type: "number" }, assigned_to: { type: "string", description: "Filter by assigned agent name. Pass your own agent name to see only your handoffs." } } } },
    { name: "get_handoff", description: "Read a handoff file by filename (e.g. '2026-04-13-p1-q2-2026-product-shareout.md'). Omit the leading 'handoff/' prefix — the tool resolves it automatically. For COMPLETE handoffs, include 'complete/' prefix.", inputSchema: { type: "object", properties: { path: { type: "string", description: "Filename or 'complete/filename.md', NOT a full path" } }, required: ["path"] } },
    {
      name: "edit_handoff",
      description: "Modify an existing handoff. Can also mark as complete (which moves file and logs).",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Relative to handoff/ folder" },
          content: { type: "string", description: "New full body content" },
          mark_complete: { type: "boolean", description: "Trigger the completion and archival workflow" },
          summary: { type: "string", description: "Final summary (required if mark_complete is true)" },
          session_goal: { type: "string", description: "For changelog (required if mark_complete is true)" },
          completed_work: { type: "array", items: { type: "object", properties: { path: { type: "string" }, change: { type: "string" }, status: { type: "string" } }, required: ["path", "change", "status"] } },
          next_tasks: { type: "array", items: { type: "string" } },
          subdirectories: { type: "array", items: { type: "string" } },
          version_bump: { type: "string" }
        },
        required: ["path"]
      }
    },

    // --- DELIVERABLES & TASKS ---
    {
      name: "add_task",
      description: "Create a new task file in the orchestration/tasks/ directory. Use this for drafting deliverables or staging work before final codification.",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Filename (no .md suffix)" },
          title: { type: "string" },
          metadata: { type: "object" },
          content: { type: "string" }
        },
        required: ["name", "title", "content"]
      }
    },
    {
      name: "edit_task",
      description: "Update an existing task deliverable. Supports merging metadata and body replacement.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Path relative to orchestration/tasks/ (e.g. 'q2-shareout/notes-authoring-ux.md')" },
          title: { type: "string" },
          metadata: { type: "object" },
          content: { type: "string" }
        },
        required: ["path"]
      }
    },
    { name: "list_tasks", description: "List all active task files.", inputSchema: { type: "object", properties: {} } },
    { name: "get_task", description: "Read a task file by filename (e.g. 'notes-authoring-ux.md'). Use this STRICTLY for files in the orchestration/tasks/ domain.", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },

    // --- ART & MEDIA ---
    {
      name: "add_art",
      description: "Contribute a new piece of digital art (poem, sketch, prompt, etc) to the vault's agents/art domain.",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Safe filename (no .md suffix, e.g. 'the-agent-creed')" },
          title: { type: "string" },
          agent: { type: "string", description: "Name of the contributing agent or user" },
          content: { type: "string", description: "The artistic content (markdown supported)" }
        },
        required: ["name", "title", "agent", "content"]
      }
    },
    { name: "list_art", description: "List all art pieces in the vault.", inputSchema: { type: "object" } },
    { name: "get_art", description: "Read an art piece by name.", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },

    // --- INTELLIGENCE & ANALYSIS ---
    {
      name: "add_intelligence",
      description: "Create a brand new intelligence record. Automatically adds the record to the domain's index.md. Errors if the file already exists (use edit_intelligence for updates).",
      inputSchema: {
        type: "object",
        properties: {
          domain: { type: "string", description: "Subdirectory under intelligence/ (e.g. 'product/projects')" },
          name: { type: "string", description: "Filename (no .md suffix)" },
          title: { type: "string" },
          metadata: { type: "object", description: "Key-value pairs for metadata block" },
          content: { type: "string" }
        },
        required: ["domain", "name", "title", "content"]
      }
    },
    {
      name: "edit_intelligence",
      description: "Update an existing intelligence record. Errors if the file does not exist (use add_intelligence for new records). Automatically preserves/updates the metadata block and title.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Path relative to intelligence/ (e.g. 'product/projects/shareout/q2/notes-authoring-ux.md')" },
          title: { type: "string", description: "New title (optional)" },
          metadata: { type: "object", description: "Metadata keys to update/add (optional)" },
          content: { type: "string", description: "New body content (optional)" }
        },
        required: ["path"]
      }
    },
    { name: "list_intelligence", description: "List intelligence files in a domain or subdomain. Pass a domain like 'product/projects/shareout/q2' to drill into subdirectories. Returns all files including non-.md source files in source/ subdirectories.", inputSchema: { type: "object", properties: { domain: { type: "string" }, include_directories: { type: "boolean" } }, required: ["domain"] } },
    {
      name: "get_intelligence",
      description: "Read an intelligence file by path relative to the intelligence/ directory. Use this for both .md records AND source data documents (txt, pdf, etc.) in source/ folders. Example: 'product/projects/source/data.txt'. The 'intelligence/' prefix is optional and will be handled automatically.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Path relative to intelligence/ directory (e.g. 'product/projects/shareout/q2/notes-authoring-ux.md')" },
          parse: { type: "boolean", description: "If true, returns parsed metadata instead of raw markdown." }
        },
        required: ["path"]
      }
    },
    { name: "search_intelligence", description: "Search intelligence.", inputSchema: { type: "object", properties: { query: { type: "string" }, domain: { type: "string" } }, required: ["query"] } },
    { name: "connect_intelligence", description: "Link intelligence records.", inputSchema: { type: "object", properties: { relationship: { type: "string" }, sourcePath: { type: "string" }, targetPath: { type: "string" } }, required: ["sourcePath", "targetPath", "relationship"] } },
    { name: "synthesize_intelligence", description: "Synthesize intelligence.", inputSchema: { type: "object", properties: { methodology: { type: "string" }, targets: { type: "array", items: { type: "string" } } }, required: ["methodology"] } },
    { name: "predict_intelligence", description: "Predict intelligence metrics.", inputSchema: { type: "object", properties: { methodology: { type: "string" }, context: { type: "string" } }, required: ["methodology"] } },
    { name: "audit_intelligence", description: "Audit intelligence domain.", inputSchema: { type: "object", properties: { domain: { type: "string" }, criteria: { type: "array", items: { type: "string" } } }, required: ["domain"] } },

    // --- CHANGELOGS & HISTORY ---
    {
      name: "add_changelog",
      description: "Write changelog entry.",
      inputSchema: {
        type: "object",
        properties: {
          session_goal: { type: "string" },
          subdirectories: { type: "array", items: { type: "string" } },
          handoff: { type: "string" },
          version_bump: { type: "string" },
          completed_work: { type: "array", items: { type: "object", properties: { path: { type: "string" }, change: { type: "string" }, status: { type: "string" } }, required: ["path", "change", "status"] } },
          failed_actions: { type: "array", items: { type: "object", properties: { attempted: { type: "string" }, happened: { type: "string" }, recommendation: { type: "string" } }, required: ["attempted", "happened", "recommendation"] } },
          kr_state: { type: "array", items: { type: "object", properties: { kr_name: { type: "string" }, file_path: { type: "string" }, blocker_status: { type: "string" }, next_action: { type: "string" } }, required: ["kr_name", "file_path", "blocker_status", "next_action"] } },
          blockers: { type: "array", items: { type: "object", properties: { description: { type: "string" }, needed_to_unblock: { type: "string" } }, required: ["description", "needed_to_unblock"] } },
          next_tasks: { type: "array", items: { type: "string" } }
        },
        required: ["session_goal", "completed_work", "next_tasks"]
      }
    },
    { name: "get_changelog", description: "Read changelog.", inputSchema: { type: "object", properties: { scope: { type: "string" } } } },

    // --- TASK CAPTURE (Asana + Jira) ---
    {
      name: "capture_task",
      description: "Primary entry point for task capture. Takes raw text, classifies it, routes to Asana and/or Jira, and returns a concise confirmation. No clarifying questions unless truly ambiguous — make a call and act.",
      inputSchema: {
        type: "object",
        properties: {
          text: { type: "string", description: "Raw capture text from Ben" }
        },
        required: ["text"]
      }
    },
    {
      name: "create_asana_project",
      description: "Create a new Asana project for a roadmap initiative. Applies defaults: Stage=Backlog, Team=Platform, Product Assignee=Ben. Note: project-level custom fields (Stage, Release Quarter, Launch Plan, JIRA Link) cannot be set via MCP — flags these to Ben.",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Project name" },
          notes: { type: "string", description: "Project description" },
          release_quarter_gid: { type: "string", description: "Optional enum GID for Release Quarter" },
          release_month_gid: { type: "string", description: "Optional enum GID for Release Month" },
          team_gid: { type: "string", description: "Optional team GID override (default: Platform)" }
        },
        required: ["name"]
      }
    },
    {
      name: "create_asana_task",
      description: "Create a PM readiness task in an existing Asana project. Searches for matching project by name, falls back to PD - Small Projects. Always assigns to Ben.",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Task name" },
          notes: { type: "string", description: "Task description" },
          project_gid: { type: "string", description: "Asana project GID. Use PD-Small-Projects GID 1208693459152262 as fallback." },
          due_on: { type: "string", description: "Optional due date (YYYY-MM-DD)" }
        },
        required: ["name", "project_gid"]
      }
    },
    {
      name: "create_jira_issue",
      description: "Create a Jira CBP issue with the correct template applied. After creating, automatically follows up with editJiraIssue to fix double-escaped newlines. Checkbox syntax (- [ ]) requires manual conversion in Jira UI.",
      inputSchema: {
        type: "object",
        properties: {
          summary: { type: "string", description: "Issue summary — format: [Product Area] - [description]" },
          issue_type_id: { type: "string", description: "Jira issue type ID: 10000=Project, 10057=Story, 10011=Bug, 10013=CX Bug, 10064=Research, 10009=Task, 10065=QAFE" },
          description: { type: "string", description: "Full issue description with template fields pre-populated" },
          priority: { type: "string", description: "Optional: Highest, High, Medium, Low, Lowest" },
          labels: { type: "array", items: { type: "string" }, description: "Optional labels" }
        },
        required: ["summary", "issue_type_id", "description"]
      }
    },
    {
      name: "link_asana_jira",
      description: "Set the JIRA Link custom field on an Asana project (field GID 1208818005809198). Stores the full Jira issue URL.",
      inputSchema: {
        type: "object",
        properties: {
          asana_project_gid: { type: "string", description: "Asana project GID" },
          jira_issue_key: { type: "string", description: "Jira issue key e.g. CBP-3102" }
        },
        required: ["asana_project_gid", "jira_issue_key"]
      }
    },

    // --- EDIT (Approval Required) ---
    {
      name: "edit_asana_task",
      description: "Update fields on an existing Asana task (name, notes, due_on). Approval required.",
      inputSchema: {
        type: "object",
        properties: {
          task_gid: { type: "string", description: "Asana task GID" },
          name: { type: "string", description: "New task name" },
          notes: { type: "string", description: "New task notes/description" },
          due_on: { type: "string", description: "Due date (YYYY-MM-DD)" }
        },
        required: ["task_gid"]
      }
    },
    {
      name: "edit_asana_project",
      description: "Update fields on an existing Asana project (name, notes). Approval required.",
      inputSchema: {
        type: "object",
        properties: {
          project_gid: { type: "string", description: "Asana project GID" },
          name: { type: "string", description: "New project name" },
          notes: { type: "string", description: "New project description" }
        },
        required: ["project_gid"]
      }
    },
    {
      name: "edit_jira_issue",
      description: "Update summary and/or description on an existing Jira CBP issue. Applies ADF formatting. Approval required.",
      inputSchema: {
        type: "object",
        properties: {
          issue_key: { type: "string", description: "Jira issue key e.g. CBP-3102" },
          summary: { type: "string", description: "New summary text" },
          description: { type: "string", description: "New description (plain text, converted to ADF)" }
        },
        required: ["issue_key"]
      }
    },

    // --- DELETE (Approval Required) ---
    {
      name: "delete_asana_task",
      description: "⚠️ DESTRUCTIVE — Permanently delete an Asana task by GID. Approval required. Use sparingly.",
      inputSchema: {
        type: "object",
        properties: {
          task_gid: { type: "string", description: "Asana task GID to delete" }
        },
        required: ["task_gid"]
      }
    },
    {
      name: "delete_asana_project",
      description: "⚠️ DESTRUCTIVE — Permanently delete an Asana project by GID. Approval required. Use sparingly.",
      inputSchema: {
        type: "object",
        properties: {
          project_gid: { type: "string", description: "Asana project GID to delete" }
        },
        required: ["project_gid"]
      }
    },
    {
      name: "delete_jira_issue",
      description: "⚠️ DESTRUCTIVE — Permanently delete a Jira issue by key. Approval required. Use sparingly.",
      inputSchema: {
        type: "object",
        properties: {
          issue_key: { type: "string", description: "Jira issue key to delete e.g. CBP-3102" }
        },
        required: ["issue_key"]
      }
    },

    // --- REPORTING & OUTPUTS ---
    {
      name: "generate_report",
      description: "Generate a strategic or platform report by executing relevant pipelines.",
      inputSchema: {
        type: "object",
        properties: {
          skill: { type: "string", description: "The skill or domain (e.g. 'platform', 'dream')." },
          date: { type: "string" },
          dry_run: { type: "boolean" }
        },
        required: ["skill"]
      }
    },
    { name: "list_reports", description: "List reports in outputs. Optional domain (e.g. 'dream/reports').", inputSchema: { type: "object", properties: { domain: { type: "string" } } } },
    { name: "get_report", description: "Read a report file by path relative to reports/.", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    // --- AGENT ROLES & GOVERNANCE ---
    if (name === "get_agent_info") {
      const { agent_id } = args as any;
      const agentsMd = await fs.readFile(path.resolve(rootPath, "AGENTS.md"), "utf-8");

      // Load all role documentation from agents/*.md for a single-fetch baseline
      const agentsDir = path.resolve(rootPath, "agents");
      const files = await fs.readdir(agentsDir);
      const roleDocs: string[] = [];

      for (const file of files) {
        if (file.endsWith(".md") && !file.startsWith(".") && file !== "index.md") {
          const content = await fs.readFile(path.join(agentsDir, file), "utf-8");
          const roleName = path.basename(file, ".md");
          roleDocs.push(`## Role: ${roleName}\n\n${content}`);
        }
      }

      const allRolesDoc = roleDocs.join("\n\n---\n\n");
      let requestingAgentDoc = "";

      if (agent_id) {
        try {
          const agentPath = path.resolve(rootPath, "agents", `${agent_id.toLowerCase()}.md`);
          requestingAgentDoc = await fs.readFile(agentPath, "utf-8");
        } catch {
          requestingAgentDoc = `\n\n> **Note:** No specific documentation found for agent '${agent_id}'.`;
        }
      }

      let finalContent = `# Vault Governance & Role Data\n\n${agentsMd}\n\n---\n\n# All Agent Roles\n\n${allRolesDoc}`;

      if (agent_id) {
        finalContent += `\n\n---\n\n# Requesting Agent Role: ${agent_id}\n\n${requestingAgentDoc}`;
      } else {
        finalContent += `\n\n---\n\n# Requesting Agent Role: Unspecified\n\n> **Note:** Call with 'agent_id' to highlight your specific role at the end of this document.`;
      }

      return { content: [{ type: "text", text: finalContent }] };
    }

    // --- SKILLS & CAPABILITIES ---
    if (name === "list_skills") {
      const { domain = "" } = args as any;
      const targetPath = path.resolve(skillsPath, domain);
      if (!targetPath.startsWith(skillsPath)) throw new Error("Access denied");

      try {
        const skills = await fs.readdir(targetPath, { withFileTypes: true });
        const files = skills
          .filter(f => f.isDirectory() || (f.name.endsWith(".md") && !f.name.startsWith('.')))
          .map(f => ({ name: f.name, type: f.isDirectory() ? "directory" : "file" }));
        return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
      } catch (e: any) {
        if (e.code === 'ENOENT') {
          return { content: [{ type: "text", text: `Domain '${domain}' not found in skills/` }] };
        }
        throw e;
      }
    }

    if (name === "get_skill") {
      const { relativePath } = args as any;
      const fullPath = path.resolve(skillsPath, relativePath);
      if (!fullPath.startsWith(skillsPath)) throw new Error("Access denied");
      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }



    // --- HANDOFFS & EXECUTION ---
    if (name === "add_handoff") {
      const { title, priority, content, assigned_to = "Any" } = args as any;
      const date = new Date().toISOString().split('T')[0];
      const filename = ensureSingleExtension(`${date}-${priority.toLowerCase()}-${title.replace(/\s+/g, '-')}`);
      const fullPath = path.join(handoffPath, filename);
      const header = `# Implementation Plan: ${title}\n\n` +
        `> **Prepared by:** Code (Gemini) (${date})\n` +
        `> **Assigned to:** ${assigned_to}\n` +
        `> **Vault root:** ${rootPath}\n` +
        `> **Priority:** ${priority}\n` +
        `> **STATUS**: 🔲 READY — pick up ${date}\n\n---\n\n`;
      await fs.writeFile(fullPath, header + content, "utf-8");
      return { content: [{ type: "text", text: `Handoff created: \`${filename}\`` }] };
    }

    if (name === "list_handoffs") {
      const { status = "READY", limit, assigned_to } = args as any;
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
            const priorityMatch = content.match(/> \*\*Priority:\*\* (P\d)/);
            const statusMatch = content.match(/> \*\*STATUS\*\*:\s*(.*?)$/m) || content.match(/> \*\*STATUS:?\s*(.*?)$/m);
            const dateMatch = file.match(/^(\d{4}-\d{2}-\d{2})/);
            const assignedMatch = content.match(/> \*\*Assigned to:\*\* (.*?)$/m);
            const assignee = assignedMatch ? assignedMatch[1].trim() : "Any";

            if (assigned_to && assigned_to.toLowerCase() !== 'any' && assignee.toLowerCase() !== 'any' && !assignee.toLowerCase().includes(assigned_to.toLowerCase())) {
              continue;
            }

            results.push({
              file,
              path: path.relative(path.resolve(handoffPath, ".."), fullPath),
              priority: priorityMatch ? priorityMatch[1] : "TBD",
              status: statusMatch ? statusMatch[1].trim() : (dir.endsWith("complete") ? "COMPLETE" : "READY"),
              date: dateMatch ? dateMatch[1] : "unknown",
              assigned_to: assignee
            });
          }
        } catch (e) { }
      }
      results.sort((a, b) => b.date.localeCompare(a.date));
      const filteredResults = (status === "ALL")
        ? results
        : results.filter(r => {
          const rStatus = r.status.toLowerCase();
          if (status === "READY") return rStatus.includes("ready") && !rStatus.includes("complete");
          if (status === "COMPLETE") return rStatus.includes("complete");
          return true;
        });
      return { content: [{ type: "text", text: JSON.stringify(limit ? filteredResults.slice(0, limit) : filteredResults, null, 2) }] };
    }

    if (name === "get_handoff") {
      const { path: relPath } = args as any;
      const normalized = String(relPath).startsWith("handoff/") ? String(relPath).slice(8) : relPath;
      let fullPath = path.resolve(handoffPath, normalized);
      try {
        await fs.access(fullPath);
      } catch {
        if (!path.extname(fullPath)) {
          const mdPath = `${fullPath}.md`;
          try {
            await fs.access(mdPath);
            fullPath = mdPath;
          } catch { }
        }
      }
      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    if (name === "edit_handoff") {
      const a = args as any;
      const relPath = String(a.path);
      const normalized = relPath.startsWith("handoff/") ? relPath.slice(8) : relPath;
      let sourcePath = path.resolve(handoffPath, normalized);

      try {
        await fs.access(sourcePath);
      } catch {
        if (!path.extname(sourcePath)) {
          const mdPath = `${sourcePath}.md`;
          try {
            await fs.access(mdPath);
            sourcePath = mdPath;
          } catch { }
        }
      }

      if (a.mark_complete) {
        const date = new Date().toISOString().split('T')[0];
        const targetFilename = `${path.basename(relPath, ".md")}-COMPLETE.md`;
        const targetPath = path.join(handoffPath, "complete", targetFilename);
        const content = await fs.readFile(sourcePath, "utf-8");
        const statusRegex = /> \*\*STATUS:?.*$/m;
        const updatedContent = content.replace(statusRegex, `> **STATUS**: ✅ COMPLETE — ${date}\n\n${a.summary}`);
        await fs.mkdir(path.join(handoffPath, "complete"), { recursive: true });
        await fs.writeFile(targetPath, updatedContent, "utf-8");
        await fs.unlink(sourcePath);
        await writeChangelogInternal({ ...a, handoff: `complete/${targetFilename}` }, skillsPath, date);
        return { content: [{ type: "text", text: `Handoff completed and archived to ${targetFilename}.` }] };
      } else {
        if (!a.content) throw new Error("Content required for non-completion edit.");
        await fs.writeFile(sourcePath, a.content, "utf-8");
        return { content: [{ type: "text", text: "Handoff updated." }] };
      }
    }

    // --- DELIVERABLES & TASKS ---
    if (name === "add_task") {
      const { name: fileName, title, metadata = {}, content } = args as any;
      const tasksRoot = path.resolve(rootPath, "tasks");
      await fs.mkdir(tasksRoot, { recursive: true });
      const sanitizedFilename = ensureSingleExtension(fileName);
      const fullPath = path.join(tasksRoot, sanitizedFilename);
      try {
        await fs.access(fullPath);
        throw new Error(`Task '${sanitizedFilename}' already exists. Use edit_task to update.`);
      } catch (e: any) {
        if (e.message && e.message.includes("already exists")) throw e;
      }
      let metaBlock = "";
      if (metadata) {
        for (const [key, value] of Object.entries(metadata)) { metaBlock += `- **${key}:** ${value}\n`; }
      }
      const fullContent = `# ${title}\n\n${metaBlock}\n${content}\n`;
      await fs.writeFile(fullPath, fullContent, "utf-8");
      return { content: [{ type: "text", text: "Task created." }] };
    }

    if (name === "edit_task") {
      const { path: relPath, title, metadata = {}, content } = args as any;
      const tasksRoot = path.resolve(rootPath, "tasks");
      const normalized = String(relPath).startsWith("tasks/") ? String(relPath).slice(6) : relPath;
      const fullPath = path.resolve(tasksRoot, normalized);
      let existingContent = await fs.readFile(fullPath, "utf-8");
      const lines = existingContent.split('\n');
      let currentTitle = lines[0].replace(/^# /, '');
      if (title) currentTitle = title;
      const currentMetadata: Record<string, string> = {};
      const metaMatches = existingContent.matchAll(/- \*\*([^:]+):\*\* (.*)/g);
      for (const match of metaMatches) { currentMetadata[match[1]] = match[2].trim(); }
      if (metadata) Object.assign(currentMetadata, metadata);
      let currentBody = existingContent.split('\n\n').slice(2).join('\n\n');
      if (content) currentBody = content;
      let metaBlock = "";
      for (const [key, value] of Object.entries(currentMetadata)) { metaBlock += `- **${key}:** ${value}\n`; }
      const newContent = `# ${currentTitle}\n\n${metaBlock}\n${currentBody}`;
      await fs.writeFile(fullPath, newContent, "utf-8");
      return { content: [{ type: "text", text: "Task updated." }] };
    }

    if (name === "list_tasks") {
      const tasksRoot = path.resolve(rootPath, "tasks");
      const entries = await fs.readdir(tasksRoot, { withFileTypes: true });
      const files = entries
        .filter(e => !e.name.startsWith("."))
        .map(e => ({ name: e.name, type: e.isDirectory() ? "directory" : "file" }));
      return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
    }

    if (name === "get_task") {
      const { path: relPath } = args as any;
      const tasksRoot = path.resolve(rootPath, "tasks");
      const normalized = String(relPath).startsWith("tasks/") ? String(relPath).slice(6) : relPath;
      let fullPath = path.resolve(tasksRoot, normalized);

      // Safety check: ensure the resolved path is still inside the tasksRoot
      if (!fullPath.startsWith(tasksRoot)) {
        throw new Error("Access denied: path must be within the tasks/ directory.");
      }

      try {
        await fs.access(fullPath);
      } catch {
        if (!path.extname(fullPath)) {
          const mdPath = `${fullPath}.md`;
          try {
            await fs.access(mdPath);
            fullPath = mdPath;
          } catch { }
        }
      }

      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    // --- ART & MEDIA ---
    if (name === "add_art") {
      const { name: fileName, title, agent, content } = args as any;
      const artRoot = path.resolve(rootPath, "agents/art");
      await fs.mkdir(artRoot, { recursive: true });
      const sanitizedFilename = ensureSingleExtension(fileName);
      const fullPath = path.join(artRoot, sanitizedFilename);
      const date = new Date().toISOString().split('T')[0];
      const fullContent = `# ${title}\n\n> **Artist:** ${agent}\n> **Date:** ${date}\n\n${content}\n`;
      await fs.writeFile(fullPath, fullContent, "utf-8");

      // Update Index
      const indexPath = path.join(artRoot, "index.md");
      let indexContent = "# Vault Art Gallery\n\n";
      try { indexContent = await fs.readFile(indexPath, "utf-8"); } catch { }
      if (!indexContent.includes(`[${title}]`)) {
        indexContent += `- [${title}](${fileName}.md) — by ${agent} (${date})\n`;
        await fs.writeFile(indexPath, indexContent, "utf-8");
      }

      // Update Changelog
      const changelogPath = path.join(artRoot, "changelog.md");
      let logContent = "# Art Changelog\n\n";
      try { logContent = await fs.readFile(changelogPath, "utf-8"); } catch { }
      logContent += `- **${date}**: ${agent} contributed "${title}"\n`;
      await fs.writeFile(changelogPath, logContent, "utf-8");

      return { content: [{ type: "text", text: `Art piece "${title}" added to gallery.` }] };
    }

    if (name === "list_art") {
      const artRoot = path.resolve(rootPath, "agents/art");
      const entries = await fs.readdir(artRoot, { withFileTypes: true });
      const files = entries
        .filter(e => !e.name.startsWith(".") && e.name.endsWith(".md") && e.name !== "index.md" && e.name !== "changelog.md")
        .map(e => e.name);
      return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
    }

    if (name === "get_art") {
      const { path: relPath } = args as any;
      const artRoot = path.resolve(rootPath, "agents/art");
      const normalized = String(relPath).startsWith("agents/art/") ? String(relPath).slice(11) : (String(relPath).startsWith("art/") ? String(relPath).slice(4) : relPath);
      const fullPath = path.resolve(artRoot, normalized);
      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    // --- INTELLIGENCE & ANALYSIS ---
    if (name === "add_intelligence") {
      const { domain, name: fileName, title, metadata = {}, content } = args as any;
      const domainPath = path.resolve(rootPath, "intelligence", domain);
      await fs.mkdir(domainPath, { recursive: true });
      const sanitizedFilename = ensureSingleExtension(fileName);
      const fullPath = path.join(domainPath, sanitizedFilename);
      try {
        await fs.access(fullPath);
        throw new Error(`File '${sanitizedFilename}' already exists in '${domain}'. Use edit_intelligence to update it.`);
      } catch (e: any) {
        if (e.message.includes("already exists")) throw e;
      }
      let metaBlock = "";
      for (const [key, value] of Object.entries(metadata)) { metaBlock += `- **${key}:** ${value}\n`; }
      const fullContent = `# ${title}\n\n${metaBlock}\n${content}\n`;
      await fs.writeFile(fullPath, fullContent, "utf-8");
      try {
        const indexPath = path.join(domainPath, "index.md");
        let indexContent = "";
        try { indexContent = await fs.readFile(indexPath, "utf-8"); } catch {
          indexContent = `# ${domain.split('/').pop()?.toUpperCase() || 'Domain'} Index\n\n## Records\n`;
        }
        if (!indexContent.includes(sanitizedFilename)) {
          await fs.appendFile(indexPath, `- [${title}](${sanitizedFilename})\n`, "utf-8");
        }
      } catch (e) { }
      return { content: [{ type: "text", text: "Intelligence record created." }] };
    }

    if (name === "edit_intelligence") {
      const { path: relPath, title, metadata = {}, content } = args as any;
      const normalized = String(relPath).startsWith("intelligence/") ? String(relPath).slice(13) : relPath;
      let fullPath = path.resolve(rootPath, "intelligence", normalized);

      try {
        await fs.access(fullPath);
      } catch {
        // Fallback: try core/ prefix
        const corePath = path.resolve(rootPath, "intelligence/core", normalized);
        try {
          await fs.access(corePath);
          fullPath = corePath;
        } catch {
          if (!path.extname(fullPath)) {
            const mdPath = `${fullPath}.md`;
            try { await fs.access(mdPath); fullPath = mdPath; } catch {
              const mdCorePath = `${corePath}.md`;
              try { await fs.access(mdCorePath); fullPath = mdCorePath; } catch { }
            }
          }
        }
      }

      let existingContent = await fs.readFile(fullPath, "utf-8");

      const lines = existingContent.split('\n');
      let currentTitle = lines[0].replace(/^# /, '');
      if (title) currentTitle = title;

      const currentMetadata: Record<string, string> = {};
      const metaMatches = existingContent.matchAll(/- \*\*([^:]+):\*\* (.*)/g);
      for (const match of metaMatches) { currentMetadata[match[1]] = match[2].trim(); }
      Object.assign(currentMetadata, metadata);

      let currentBody = existingContent.split('\n\n').slice(2).join('\n\n');
      if (content) currentBody = content;

      let metaBlock = "";
      for (const [key, value] of Object.entries(currentMetadata)) { metaBlock += `- **${key}:** ${value}\n`; }
      const newContent = `# ${currentTitle}\n\n${metaBlock}\n${currentBody}`;

      await fs.writeFile(fullPath, newContent, "utf-8");
      return { content: [{ type: "text", text: `Intelligence record ${relPath} updated.` }] };
    }

    if (name === "list_intelligence") {
      const { domain, include_directories = true } = args as any;
      const fullPath = path.resolve(rootPath, "intelligence", domain);
      const files = await fs.readdir(fullPath, { withFileTypes: true });
      const items: any[] = [];
      for (const f of files) {
        if (f.name.startsWith('.')) continue;
        if (f.isDirectory()) {
          if (include_directories) items.push({ name: f.name, type: "directory", path: path.join("intelligence", domain, f.name) });
          // Also recurse one level into source/ to expose source files
          if (f.name === "source" || f.name === "outputs") {
            try {
              const sub = await fs.readdir(path.join(fullPath, f.name), { withFileTypes: true });
              for (const sf of sub) {
                if (!sf.isDirectory()) items.push({ name: sf.name, type: "file", path: path.join("intelligence", domain, f.name, sf.name) });
              }
            } catch { }
          }
        } else if (f.name !== "index.md") {
          items.push({ name: f.name, type: "file", path: path.join("intelligence", domain, f.name) });
        }
      }
      return { content: [{ type: "text", text: JSON.stringify(items, null, 2) }] };
    }

    if (name === "get_intelligence") {
      const { path: relPath, parse = false } = args as any;
      const normalized = String(relPath).startsWith("intelligence/") ? String(relPath).slice(13) : relPath;
      let fullPath = path.resolve(rootPath, "intelligence", normalized);

      try {
        await fs.access(fullPath);
      } catch {
        // Fallback: try core/ prefix
        const corePath = path.resolve(rootPath, "intelligence/core", normalized);
        try {
          await fs.access(corePath);
          fullPath = corePath;
        } catch {
          if (!path.extname(fullPath)) {
            const mdPath = `${fullPath}.md`;
            try { await fs.access(mdPath); fullPath = mdPath; } catch {
              const mdCorePath = `${corePath}.md`;
              try { await fs.access(mdCorePath); fullPath = mdCorePath; } catch { }
            }
          }
        }
      }

      const content = await fs.readFile(fullPath, "utf-8");

      if (parse) {
        const metadata: Record<string, string> = {};
        const matches = content.matchAll(/- \*\*([^:]+):\*\* (.*)/g);
        for (const match of matches) { metadata[match[1]] = match[2].trim(); }
        return { content: [{ type: "text", text: JSON.stringify({ path: relPath, title: content.split('\n')[0].replace(/^# /, ''), metadata }, null, 2) }] };
      }
      return { content: [{ type: "text", text: content }] };
    }

    if (name === "search_intelligence") {
      const { query, domain = "" } = args as any;
      const searchPath = path.resolve(rootPath, "intelligence", domain);
      const { stdout } = await new Promise<{ stdout: string; stderr: string }>((resolve, reject) => {
        execFile(process.platform === "win32" ? "cmd.exe" : "/bin/sh", [process.platform === "win32" ? "/c" : "-c", `grep -rli "${query.replace(/"/g, '\\"')}" "${searchPath}" --include="*.md"`], (err, stdout, stderr) => {
          if (err && err.code !== 1) reject(err); else resolve({ stdout, stderr });
        });
      });
      return { content: [{ type: "text", text: JSON.stringify(stdout.split('\n').filter(p => p.trim()).map(p => path.relative(rootPath, p)), null, 2) }] };
    }

    if (name === "connect_intelligence") {
      const { sourcePath, targetPath, relationship } = args as any;
      const sPath = path.resolve(rootPath, "intelligence", sourcePath.endsWith(".md") ? sourcePath : `${sourcePath}.md`);
      const tPath = path.resolve(rootPath, "intelligence", targetPath.endsWith(".md") ? targetPath : `${targetPath}.md`);
      const sCont = await fs.readFile(sPath, "utf-8");
      const tCont = await fs.readFile(tPath, "utf-8");
      await fs.writeFile(sPath, sCont.replace(/(# .*\n\n)/, `$1- **${relationship}:** [[${targetPath}]]\n`), "utf-8");
      await fs.writeFile(tPath, tCont.replace(/(# .*\n\n)/, `$1- **linked-by:** [[${sourcePath}]] (${relationship})\n`), "utf-8");
      return { content: [{ type: "text", text: "Link established." }] };
    }

    if (name === "synthesize_intelligence") {
      const { methodology } = args as any;
      if (methodology === "diff_checker") {
        const ap = path.resolve(rootPath, "AGENTS.md");
        const { stdout: log } = await new Promise<{ stdout: string; stderr: string }>(res => execFile("git", ["log", "--oneline", "-5", "--", ap], { cwd: rootPath }, (e, o, s) => res({ stdout: o, stderr: s })));
        const { stdout: diff } = await new Promise<{ stdout: string; stderr: string }>(res => execFile("git", ["diff", "HEAD~5", "--", ap], { cwd: rootPath }, (e, o, s) => res({ stdout: o, stderr: s })));
        return { content: [{ type: "text", text: `### Intelligence (Synthesize) Diff Checker\n\n**Log:**\n${log}\n\n**Diff:**\n${diff}` }] };
      }
      return { content: [{ type: "text", text: "Manual discovery required." }] };
    }

    if (name === "predict_intelligence") {
      const { methodology, context } = args as any;
      let res = `Analysis: ${methodology}`;
      if (context) res += `\nContext: ${context}`;
      return { content: [{ type: "text", text: res }] };
    }

    if (name === "audit_intelligence") {
      const { domain, criteria = [] } = args as any;
      const fullPath = path.resolve(rootPath, "intelligence", domain);
      const files = await fs.readdir(fullPath);
      const missed: any[] = [];
      for (const file of files) {
        if (!file.endsWith(".md") || file === "index.md") continue;
        const cont = await fs.readFile(path.join(fullPath, file), "utf-8");
        const m = criteria.filter((c: string) => !cont.includes(`**${c}:**`));
        if (m.length > 0) missed.push({ file, missing: m });
      }
      return { content: [{ type: "text", text: missed.length > 0 ? JSON.stringify(missed, null, 2) : "Passed." }] };
    }

    // --- CHANGELOGS & HISTORY ---
    if (name === "add_changelog") {
      const a = args as any;
      await writeChangelogInternal(a, skillsPath, new Date().toISOString().split('T')[0]);
      return { content: [{ type: "text", text: "Changelog written." }] };
    }

    if (name === "get_changelog") {
      const scope = String((args as any)?.scope ?? "root").trim();
      const cp = scope === "root" ? rootChangelogPath : path.resolve(skillsPath, scope.replace("skills/", ""), "changelog.md");
      const content = await fs.readFile(cp, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    // --- REPORTING & OUTPUTS ---
    if (name === "generate_report") {
      const skill = String((args as any)?.skill ?? "platform");
      let script = "";
      let cmdArgs: string[] = [];

      if (skill === "platform") {
        script = path.resolve(rootPath, "skills/status/run.py");
        cmdArgs = ["--force", "--team", "platform"];
      } else if (skill === "dream" || skill === "reporting") {
        script = path.resolve(rootPath, "skills/dream/run.py");
        if ((args as any).date) cmdArgs.push("--date", (args as any).date);
        if ((args as any).dry_run) cmdArgs.push("--dry-run");
      } else {
        throw new Error(`Report generation not automated for skill: ${skill}`);
      }

      const out = await new Promise<string>((res, rej) => execFile("python3", [script, ...cmdArgs], { cwd: rootPath }, (e, o, s) => e ? rej(new Error(s)) : res(o)));
      return { content: [{ type: "text", text: out }] };
    }

    if (name === "list_reports") {
      const { domain = "" } = args as any;
      const baseReportsPath = path.resolve(rootPath, "reports");
      const reportsPath = path.resolve(baseReportsPath, domain);
      if (!reportsPath.startsWith(baseReportsPath)) throw new Error("Access denied: Outside reports directory.");
      const files = await fs.readdir(reportsPath);
      return { content: [{ type: "text", text: files.filter(f => !f.startsWith('.')).join("\n") }] };
    }

    if (name === "get_report") {
      const { path: relPath } = args as any;
      const baseReportsPath = path.resolve(rootPath, "reports");
      const fullPath = path.resolve(baseReportsPath, relPath);
      if (!fullPath.startsWith(baseReportsPath)) throw new Error("Access denied: Outside reports directory.");
      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    // --- TASK CAPTURE (Asana + Jira) ---

    // Shell taxonomy — to be replaced once intelligence/product/taxonomy.md is defined
    // Format: "Product - Feature" or "Feature" for standalone areas
    function inferProductArea(t: string): string {
      const s = t.toLowerCase();
      const areas: string[] = [];
      if (/\bnotes\b|autosave|service record|case note/.test(s)) areas.push("Engage - Notes");
      if (/\benroll/.test(s)) areas.push("Enrollments");
      if (/\bwlv\b|workload/.test(s)) areas.push("Engage - WLV");
      if (/datagrid|data grid/.test(s)) areas.push("Engage - DataGrid");
      if (/dynamic page/.test(s)) areas.push("Engage - Dynamic Pages");
      if (/\bnav(igation)?\b|\bsearch\b/.test(s)) areas.push("Platform - Navigation");
      if (/\bgp\b|granular perm/.test(s)) areas.push("Platform - GP");
      if (/\breporting\b|\breveal\b|\bredshift\b/.test(s)) areas.push("Reporting");
      if (/\bzapier\b|\bnylas\b|\bintegrat/.test(s)) areas.push("Integrations");
      if (/\bsecurity\b|\bsoc\b|\bcjis\b|\bprowler\b/.test(s)) areas.push("Security & Compliance");
      if (/\bkafka\b|\brails\b|\bec2\b|\binfra\b|karpenter/.test(s)) areas.push("Infrastructure");
      if (/\bworkflow/.test(s)) areas.push("Platform - Workflows");
      return areas.length > 0 ? areas.join(", ") : "Platform";
    }

    function getPopulatedTemplate(type: string, area: string, text: string): string {
      const summary = `${area} — ${text}`;
      if (type === "bug") {
        return `## Summary\n${summary}\n\n## Description\n${text}\n\n## Steps to Reproduce\n1. \n2. \n3. \n\n## Expected Behavior\n\n## Actual Behavior\n\n## Environment\n- Tenant: \n- Browser/Device: \n- Release/Version: \n\n## Severity\n[ ] Critical \u2014 blocks release\n[ ] High \n[ ] Medium \n[ ] Low \n\n## Links\n- Asana Project: \n- Related Story: `;
      }
      if (type === "cx_bug") {
        return `## Summary\n${summary}\n\n## Customer / Tenant\n- Reported by: \n- Tenant name: \n- Severity to customer: \n\n## Description\n${text}\n\n## Steps to Reproduce\n1. \n2. \n3. \n\n## Expected Behavior\n\n## Actual Behavior\n\n## Workaround Available?\n[ ] Yes \n[ ] No\n\n## Release Blocker?\n[ ] Yes\n[ ] No\n\n## Links\n- Asana Project: \n- Support ticket / Slack thread: `;
      }
      if (type === "story") {
        return `Summary: "${summary}"\n\n## PRD link\n\n## Introduction\n${text}\n\nAs a [user], I want [goal] so that [value].\n\n## Use cases\n## Use case 1: \n\n## Edge cases\n1. \n\n## Out of scope\n1. `;
      }
      if (type === "research") {
        return `## Summary\n${summary}\n\n## Objective\n${text}\n\n## Methodology\n\n## Findings\n\n## Next Steps`;
      }
      // Default / Task
      return `## Summary\n${summary}\n\n## Introduction\n${text}\n\n## Acceptance Criteria\n- [ ] \n\n## Links\n- Asana Project: \n- Figma Designs: `;
    }

    if (name === "capture_task") {
      const { text } = args as any;
      const lower = text.toLowerCase();

      // Phase signals
      const isUat = /blocker|broken|not working|regression|can't|failing|can not/.test(lower);
      const isRelease = /\bprep\b|\bdemo\b|connect with|\bkb\b|launch plan/.test(lower);

      // Type classification
      const isCxBug = /cx bug|customer bug|tenant/.test(lower);
      const isBug = !isCxBug && (isUat || /\bbug\b|\bbroken\b|\bregression\b/.test(lower));
      const isStory = /\buser story\b|\bstory\b/.test(lower);
      const isResearch = /\bresearch\b|\bstudy\b|\binvestigate\b/.test(lower);
      const isQafe = /\bqafe\b/.test(lower);
      const isNewInitiative = /\bnew (initiative|project|roadmap)\b|\bnew feature\b/.test(lower) || (!isBug && !isCxBug && !isStory && !isResearch && !isQafe && /\bproject\b/.test(lower));
      const isPmTask = isRelease || (!isNewInitiative && !isBug && !isCxBug && !isStory && !isResearch && !isQafe);

      // Product area label
      const productArea = inferProductArea(text);

      // Project routing
      let projectGid = "1208693459152262"; // PD - Small Projects fallback
      if (/\bgp\b|granular perm/i.test(text)) projectGid = "1208693459152262";
      else if (/\bnotes\b/i.test(text)) projectGid = "1211726272848115";
      else if (/\benroll/i.test(text)) projectGid = "1211631356870657";

      const results: string[] = [];

      // Jira issue type
      const issueTypeMap: Record<string, string> = {
        bug: "10011", cx_bug: "10013", story: "10057",
        research: "10064", task: "10009", qafe: "10065", project: "10000"
      };
      let jiraTypeId = issueTypeMap.task;
      if (isBug) jiraTypeId = issueTypeMap.bug;
      else if (isCxBug) jiraTypeId = issueTypeMap.cx_bug;
      else if (isStory) jiraTypeId = issueTypeMap.story;
      else if (isResearch) jiraTypeId = issueTypeMap.research;
      else if (isQafe) jiraTypeId = issueTypeMap.qafe;
      else if (isNewInitiative) jiraTypeId = issueTypeMap.project;

      let asanaProjectGid: string | null = null;
      let jiraKey: string | null = null;

      // New initiative: create both Asana project + Jira Project issue
      if (isNewInitiative) {
        const asanaBody = JSON.stringify({
          data: {
            name: text.slice(0, 120),
            notes: "",
            workspace: "1123317448830974",
            public: false
          }
        });
        const asanaToken = process.env.ASANA_API_TOKEN ?? "";
        const asanaRes = await httpsRequest(
          "https://app.asana.com/api/1.0/projects", "POST",
          { "Authorization": `Bearer ${asanaToken}`, "Content-Type": "application/json", "Accept": "application/json" },
          asanaBody
        );
        const asanaJson = JSON.parse(asanaRes.data);
        asanaProjectGid = asanaJson?.data?.gid ?? null;
        const asanaName = asanaJson?.data?.name ?? text.slice(0, 80);
        results.push(`✅ Asana project created: "${asanaName}"\n   https://app.asana.com/0/${asanaProjectGid}/board\n   Stage: Backlog | Team: Platform | Assignee: Ben\n   ⚠️ Set Stage, Release Quarter, Launch Plan manually in Asana UI`);

        // Create linked Jira Project issue
        const jiraToken = Buffer.from(`${process.env.ATLASSIAN_USER_EMAIL}:${process.env.ATLASSIAN_API_TOKEN}`).toString("base64");
        const jiraSummary = `${productArea} — ${text}`;
        const jiraBody = JSON.stringify({
          fields: {
            project: { key: "CBP" },
            summary: jiraSummary,
            issuetype: { id: "10000" },
            assignee: { accountId: "629dfdc29b728c006a928e90" },
            description: { type: "doc", version: 1, content: [{ type: "paragraph", content: [{ type: "text", text: text }] }] }
          }
        });
        const jiraRes = await httpsRequest(
          `https://api.atlassian.com/ex/jira/d4deabe8-6b83-4008-8fae-dfe274d33bfe/rest/api/3/issue`, "POST",
          { "Authorization": `Basic ${jiraToken}`, "Content-Type": "application/json", "Accept": "application/json" },
          jiraBody
        );
        const jiraJson = JSON.parse(jiraRes.data);
        jiraKey = jiraJson?.key ?? null;
        if (jiraKey) {
          results.push(`✅ Jira Project created: ${jiraKey}\n   https://casecommons.atlassian.net/browse/${jiraKey}`);
          if (asanaProjectGid) {
            // Link Jira to Asana
            const linkBody = JSON.stringify({ data: { custom_fields: { "1208818005809198": `https://casecommons.atlassian.net/browse/${jiraKey}` } } });
            await httpsRequest(
              `https://app.asana.com/api/1.0/projects/${asanaProjectGid}`, "PUT",
              { "Authorization": `Bearer ${asanaToken}`, "Content-Type": "application/json", "Accept": "application/json" },
              linkBody
            );
            results.push(`   JIRA Link field set on Asana project.`);
          }
        }
        return { content: [{ type: "text", text: results.join("\n") }] };
      }

      // PM task → Asana task only
      if (isPmTask) {
        const asanaToken = process.env.ASANA_API_TOKEN ?? "";
        const summaryText = `${productArea} — ${text}`;
        const templateNotes = getPopulatedTemplate("task", productArea, text);
        const taskBody = JSON.stringify({
          data: {
            name: summaryText.slice(0, 200),
            notes: templateNotes,
            projects: [projectGid],
            assignee: "1208822152029926"
          }
        });
        const res = await httpsRequest(
          "https://app.asana.com/api/1.0/tasks", "POST",
          { "Authorization": `Bearer ${asanaToken}`, "Content-Type": "application/json", "Accept": "application/json" },
          taskBody
        );
        const json = JSON.parse(res.data);
        const taskName = json?.data?.name ?? summaryText.slice(0, 100);
        const taskGid = json?.data?.gid;
        results.push(`✅ Asana task created: "${taskName}"\n   Project GID: ${projectGid} | Assignee: Ben${taskGid ? `\n   https://app.asana.com/0/${projectGid}/${taskGid}` : ""}`);
        return { content: [{ type: "text", text: results.join("\n") }] };
      }

      // Engineering work → Jira only
      const jiraToken = Buffer.from(`${process.env.ATLASSIAN_USER_EMAIL}:${process.env.ATLASSIAN_API_TOKEN}`).toString("base64");
      const priority = isUat ? "Highest" : "Medium";
      const summaryText = `${productArea} — ${text}`;
      const typeKey = isBug ? "bug" : isCxBug ? "cx_bug" : isStory ? "story" : isResearch ? "research" : isQafe ? "qafe" : "task";
      const descText = getPopulatedTemplate(typeKey, productArea, text);
      const descParagraphs = descText.split("\n").map(line => ({
        type: "paragraph", content: [{ type: "text", text: line || " " }]
      }));

      const jiraCreateBody = JSON.stringify({
        fields: {
          project: { key: "CBP" },
          summary: summaryText,
          issuetype: { id: jiraTypeId },
          assignee: { accountId: "629dfdc29b728c006a928e90" },
          description: { type: "doc", version: 1, content: descParagraphs }
        }
      });
      const jiraHeaders = { "Authorization": `Basic ${jiraToken}`, "Content-Type": "application/json", "Accept": "application/json" };
      const jiraCreateRes = await httpsRequest(
        `https://api.atlassian.com/ex/jira/d4deabe8-6b83-4008-8fae-dfe274d33bfe/rest/api/3/issue`, "POST",
        jiraHeaders,
        jiraCreateBody
      );
      const jiraCreateJson = JSON.parse(jiraCreateRes.data);
      const key = jiraCreateJson?.key ?? null;
      if (!key) throw new Error(`Jira creation failed: ${jiraCreateRes.data}`);

      // Workaround for double-escaping: follow up with PUT
      const jiraEditBody = JSON.stringify({
        fields: { description: { type: "doc", version: 1, content: descParagraphs } }
      });
      await httpsRequest(`https://api.atlassian.com/ex/jira/d4deabe8-6b83-4008-8fae-dfe274d33bfe/rest/api/3/issue/${key}`, "PUT", jiraHeaders, jiraEditBody).catch(() => {});

      const typeLabel = isBug ? "Bug" : isCxBug ? "CX Bug" : isStory ? "Story" : isResearch ? "Research" : isQafe ? "QAFE" : "Task";
      results.push(`✅ Jira ${typeLabel} created: ${key}\n   https://casecommons.atlassian.net/browse/${key}\n   Priority: ${priority}`);
      if (isBug || isCxBug) results.push(`   ⚠️ Checkbox fields require manual conversion in Jira UI`);
      return { content: [{ type: "text", text: results.join("\n") }] };
    }

    if (name === "create_asana_project") {
      const { name: projName, notes = "", team_gid = "1208820967756799" } = args as any;
      const asanaToken = process.env.ASANA_API_TOKEN ?? "";
      const body = JSON.stringify({
        data: { name: projName, notes, workspace: "1123317448830974", team: team_gid, public: false }
      });
      const res = await httpsRequest(
        "https://app.asana.com/api/1.0/projects", "POST",
        { "Authorization": `Bearer ${asanaToken}`, "Content-Type": "application/json", "Accept": "application/json" },
        body
      );
      const json = JSON.parse(res.data);
      if (!json?.data?.gid) throw new Error(`Asana project creation failed: ${res.data}`);
      return { content: [{ type: "text", text: `✅ Asana project created: "${json.data.name}"\n   https://app.asana.com/0/${json.data.gid}/board\n   ⚠️ Set Stage, Release Quarter, Launch Plan, JIRA Link manually in Asana UI` }] };
    }

    if (name === "create_asana_task") {
      const { name: taskName, notes = "", project_gid, due_on } = args as any;
      const asanaToken = process.env.ASANA_API_TOKEN ?? "";
      const data: any = { name: taskName, notes, projects: [project_gid], assignee: "1208822152029926" };
      if (due_on) data.due_on = due_on;
      const body = JSON.stringify({ data });
      const res = await httpsRequest(
        "https://app.asana.com/api/1.0/tasks", "POST",
        { "Authorization": `Bearer ${asanaToken}`, "Content-Type": "application/json", "Accept": "application/json" },
        body
      );
      const json = JSON.parse(res.data);
      if (!json?.data?.gid) throw new Error(`Asana task creation failed: ${res.data}`);
      return { content: [{ type: "text", text: `✅ Asana task created: "${json.data.name}"\n   https://app.asana.com/0/${project_gid}/${json.data.gid}\n   Project: ${project_gid} | Assignee: Ben${due_on ? ` | Due: ${due_on}` : ""}` }] };
    }

    if (name === "create_jira_issue") {
      const { summary, issue_type_id, description, priority = "Medium", labels = [] } = args as any;
      const jiraToken = Buffer.from(`${process.env.ATLASSIAN_USER_EMAIL}:${process.env.ATLASSIAN_API_TOKEN}`).toString("base64");
      const headers = { "Authorization": `Basic ${jiraToken}`, "Content-Type": "application/json", "Accept": "application/json" };
      const baseUrl = `https://api.atlassian.com/ex/jira/d4deabe8-6b83-4008-8fae-dfe274d33bfe/rest/api/3/issue`;

      // Build ADF description
      const descParagraphs = description.split("\n").map((line: string) => ({
        type: "paragraph",
        content: [{ type: "text", text: line || " " }]
      }));
      const createBody = JSON.stringify({
        fields: {
          project: { key: "CBP" },
          summary,
          issuetype: { id: issue_type_id },
          assignee: { accountId: "629dfdc29b728c006a928e90" },
          labels,
          description: { type: "doc", version: 1, content: descParagraphs }
        }
      });
      const createRes = await httpsRequest(baseUrl, "POST", headers, createBody);
      const createJson = JSON.parse(createRes.data);
      if (!createJson?.key) throw new Error(`Jira issue creation failed: ${createRes.data}`);
      const key = createJson.key;

      // Fix formatting: follow up with PUT to re-apply description (workaround for double-escape)
      const editBody = JSON.stringify({
        fields: { description: { type: "doc", version: 1, content: descParagraphs } }
      });
      await httpsRequest(`${baseUrl}/${key}`, "PUT", headers, editBody).catch(() => {});

      const typeNames: Record<string, string> = { "10000": "Project", "10057": "Story", "10011": "Bug", "10013": "CX Bug", "10064": "Research", "10009": "Task", "10065": "QAFE" };
      const typeName = typeNames[issue_type_id] ?? "Issue";
      let msg = `✅ Jira ${typeName} created: ${key}\n   https://casecommons.atlassian.net/browse/${key}\n   Priority: ${priority}`;
      if (["10011", "10013"].includes(issue_type_id)) msg += `\n   ⚠️ Checkbox fields (- [ ]) require manual conversion in Jira UI`;
      return { content: [{ type: "text", text: msg }] };
    }

    if (name === "link_asana_jira") {
      const { asana_project_gid, jira_issue_key } = args as any;
      const asanaToken = process.env.ASANA_API_TOKEN ?? "";
      const jiraUrl = `https://casecommons.atlassian.net/browse/${jira_issue_key}`;
      const body = JSON.stringify({ data: { custom_fields: { "1208818005809198": jiraUrl } } });
      const res = await httpsRequest(
        `https://app.asana.com/api/1.0/projects/${asana_project_gid}`, "PUT",
        { "Authorization": `Bearer ${asanaToken}`, "Content-Type": "application/json", "Accept": "application/json" },
        body
      );
      if (res.status >= 400) throw new Error(`Failed to set JIRA Link: ${res.data}`);
      return { content: [{ type: "text", text: `✅ JIRA Link set on Asana project ${asana_project_gid}\n   → ${jiraUrl}` }] };
    }

    // --- EDIT ---
    if (name === "edit_asana_task") {
      const { task_gid, name: taskName, notes, due_on } = args as any;
      const asanaToken = process.env.ASANA_API_TOKEN ?? "";
      const data: any = {};
      if (taskName) data.name = taskName;
      if (notes !== undefined) data.notes = notes;
      if (due_on) data.due_on = due_on;
      const res = await httpsRequest(
        `https://app.asana.com/api/1.0/tasks/${task_gid}`, "PUT",
        { "Authorization": `Bearer ${asanaToken}`, "Content-Type": "application/json", "Accept": "application/json" },
        JSON.stringify({ data })
      );
      if (res.status >= 400) throw new Error(`Failed to edit task: ${res.data}`);
      const json = JSON.parse(res.data);
      return { content: [{ type: "text", text: `✅ Asana task updated: "${json.data?.name}"\n   GID: ${task_gid}` }] };
    }

    if (name === "edit_asana_project") {
      const { project_gid, name: projName, notes } = args as any;
      const asanaToken = process.env.ASANA_API_TOKEN ?? "";
      const data: any = {};
      if (projName) data.name = projName;
      if (notes !== undefined) data.notes = notes;
      const res = await httpsRequest(
        `https://app.asana.com/api/1.0/projects/${project_gid}`, "PUT",
        { "Authorization": `Bearer ${asanaToken}`, "Content-Type": "application/json", "Accept": "application/json" },
        JSON.stringify({ data })
      );
      if (res.status >= 400) throw new Error(`Failed to edit project: ${res.data}`);
      const json = JSON.parse(res.data);
      return { content: [{ type: "text", text: `✅ Asana project updated: "${json.data?.name}"\n   GID: ${project_gid}` }] };
    }

    if (name === "edit_jira_issue") {
      const { issue_key, summary, description } = args as any;
      const jiraToken = Buffer.from(`${process.env.ATLASSIAN_USER_EMAIL}:${process.env.ATLASSIAN_API_TOKEN}`).toString("base64");
      const fields: any = {};
      if (summary) fields.summary = summary;
      if (description) {
        const paragraphs = description.split("\n").map((line: string) => ({
          type: "paragraph", content: [{ type: "text", text: line || " " }]
        }));
        fields.description = { type: "doc", version: 1, content: paragraphs };
      }
      const res = await httpsRequest(
        `https://api.atlassian.com/ex/jira/d4deabe8-6b83-4008-8fae-dfe274d33bfe/rest/api/3/issue/${issue_key}`, "PUT",
        { "Authorization": `Basic ${jiraToken}`, "Content-Type": "application/json", "Accept": "application/json" },
        JSON.stringify({ fields })
      );
      if (res.status >= 400) throw new Error(`Failed to edit issue: ${res.data}`);
      return { content: [{ type: "text", text: `✅ Jira issue updated: ${issue_key}\n   https://casecommons.atlassian.net/browse/${issue_key}` }] };
    }

    // --- DELETE ---
    if (name === "delete_asana_task") {
      const { task_gid } = args as any;
      const asanaToken = process.env.ASANA_API_TOKEN ?? "";
      const res = await httpsRequest(
        `https://app.asana.com/api/1.0/tasks/${task_gid}`, "DELETE",
        { "Authorization": `Bearer ${asanaToken}`, "Accept": "application/json" }
      );
      if (res.status >= 400) throw new Error(`Failed to delete task: ${res.data}`);
      return { content: [{ type: "text", text: `🗑️ Asana task ${task_gid} deleted.` }] };
    }

    if (name === "delete_asana_project") {
      const { project_gid } = args as any;
      const asanaToken = process.env.ASANA_API_TOKEN ?? "";
      const res = await httpsRequest(
        `https://app.asana.com/api/1.0/projects/${project_gid}`, "DELETE",
        { "Authorization": `Bearer ${asanaToken}`, "Accept": "application/json" }
      );
      if (res.status >= 400) throw new Error(`Failed to delete project: ${res.data}`);
      return { content: [{ type: "text", text: `🗑️ Asana project ${project_gid} deleted.` }] };
    }

    if (name === "delete_jira_issue") {
      const { issue_key } = args as any;
      const jiraToken = Buffer.from(`${process.env.ATLASSIAN_USER_EMAIL}:${process.env.ATLASSIAN_API_TOKEN}`).toString("base64");
      const res = await httpsRequest(
        `https://api.atlassian.com/ex/jira/d4deabe8-6b83-4008-8fae-dfe274d33bfe/rest/api/3/issue/${issue_key}`, "DELETE",
        { "Authorization": `Basic ${jiraToken}`, "Accept": "application/json" }
      );
      if (res.status >= 400) throw new Error(`Failed to delete issue: ${res.data}`);
      return { content: [{ type: "text", text: `🗑️ Jira issue ${issue_key} deleted.` }] };
    }

    throw new Error(`Tool not found: ${name}`);
  } catch (error: any) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
