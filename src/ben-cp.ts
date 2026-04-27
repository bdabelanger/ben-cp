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
  { name: "ben-cp", version: "2.1.1" },
  { capabilities: { tools: {} } }
);

// Automatically find the vault root relative to this file's location
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootPath = path.resolve(__dirname, "..");
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

      const skills = await fs.readdir(targetPath, { withFileTypes: true });
      const files = skills
        .filter(f => f.isDirectory() || (f.name.endsWith(".md") && !f.name.startsWith('.')))
        .map(f => ({ name: f.name, type: f.isDirectory() ? "directory" : "file" }));
      return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
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
      return { content: [{ type: "text", text: `Handoff created: ${filename}` }] };
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
      const tasksRoot = path.resolve(rootPath, "orchestration/tasks");
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
      const tasksRoot = path.resolve(rootPath, "orchestration/tasks");
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
      const tasksRoot = path.resolve(rootPath, "orchestration/tasks");
      const entries = await fs.readdir(tasksRoot, { withFileTypes: true });
      const files = entries
        .filter(e => !e.name.startsWith("."))
        .map(e => ({ name: e.name, type: e.isDirectory() ? "directory" : "file" }));
      return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
    }

    if (name === "get_task") {
      const { path: relPath } = args as any;
      const tasksRoot = path.resolve(rootPath, "orchestration/tasks");
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

    throw new Error(`Tool not found: ${name}`);
  } catch (error: any) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
