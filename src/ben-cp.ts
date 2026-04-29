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

// Load .env from repo root
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
  { name: "ben-cp", version: "2.2.0" },
  { capabilities: { tools: {} } }
);

// Automatically find the repo root relative to this file's location
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootPath = path.resolve(__dirname, "..");
await loadEnv(rootPath);
const skillsPath = path.resolve(rootPath, "skills");
const rootChangelogPath = path.resolve(rootPath, "changelog.md");
const handoffPath = path.resolve(rootPath, "reports/handoff");

interface TaxonomyRule {
  label: string;
  keywords: string[];
  regexes: RegExp[];
  isProduct: boolean;
  isFeature: boolean;
  isOverride: boolean;
}

let taxonomyRules: TaxonomyRule[] = [];

async function loadTaxonomy(): Promise<TaxonomyRule[]> {
  const taxonomyPath = path.resolve(rootPath, "governance/taxonomy.md");
  let content = "";
  try {
    content = await fs.readFile(taxonomyPath, "utf-8");
  } catch (err) {
    console.error("Failed to load taxonomy.md, using empty rules.");
    return [];
  }

  const productLabels = new Set<string>();
  const featureLabels = new Set<string>();

  // Extract Product labels
  const productSection = content.match(/## Products\n\n([\s\S]*?)\n---/);
  if (productSection) {
    const rows = productSection[1].split("\n").filter(r => r.startsWith("|") && !r.includes("---") && !r.includes("| Product |"));
    for (const row of rows) {
      const parts = row.split("|").map(p => p.trim());
      if (parts[1]) productLabels.add(parts[1]);
    }
  }

  // Extract Feature labels
  const featureSection = content.match(/## Features\n\n([\s\S]*?)\n---/);
  if (featureSection) {
    const rows = featureSection[1].split("\n").filter(r => r.startsWith("|") && !r.includes("---") && !r.includes("| Feature |"));
    for (const row of rows) {
      const parts = row.split("|").map(p => p.trim());
      if (parts[1]) featureLabels.add(parts[1]);
    }
  }

  const rules: TaxonomyRule[] = [];
  // Extract Inference Map
  const mapSection = content.match(/## Keyword Inference Map\n\n([\s\S]*?)\n---/);
  if (mapSection) {
    const rows = mapSection[1].split("\n").filter(r => r.startsWith("|") && !r.includes("---") && !r.includes("| Signal keywords |"));
    for (const row of rows) {
      const parts = row.split("|").map(p => p.trim());
      if (parts[1] && parts[2] && parts[1] !== "*(no match)*") {
        const keywords = parts[1].split(",").map(k => k.trim().toLowerCase());
        const label = parts[2];
        const regexes = keywords.map(k => new RegExp(`\\b${k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`, "i"));

        const isOverride = label.includes(" - ");
        const isProduct = productLabels.has(label);
        const isFeature = featureLabels.has(label);

        rules.push({ label, keywords, regexes, isProduct, isFeature, isOverride });
      }
    }
  }
  return rules;
}

// Initialize taxonomy
taxonomyRules = await loadTaxonomy();


function ensureSingleExtension(filename: string, ext: string = ".md"): string {
  if (filename.endsWith(ext)) return filename;
  return filename + ext;
}

function parseTaxonomy(content: string): string[] {
  // YAML frontmatter style
  const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (yamlMatch) {
    const taxLine = yamlMatch[1].match(/^taxonomy:\s*(.+)$/m);
    if (taxLine) return taxLine[1].split(',').map(t => t.trim());
  }
  // Legacy bold style (fallback)
  const boldMatch = content.match(/- \*\*taxonomy:\*\*\s*(.+)/i);
  if (boldMatch) return boldMatch[1].split(',').map(t => t.trim());
  return [];
}

function parseFrontmatter(block: string): Record<string, string> {
  const result: Record<string, string> = {};
  for (const line of block.split('\n')) {
    const m = line.match(/^(\w[\w_-]*):\s*(.+)$/);
    if (m) result[m[1]] = m[2].trim().replace(/^['"]|['"]$/g, '');
  }
  return result;
}

async function walkDir(dir: string): Promise<string[]> {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = await Promise.all(entries.map((entry) => {
    const res = path.resolve(dir, entry.name);
    return entry.isDirectory() ? walkDir(res) : res;
  }));
  return files.flat().filter(f => f.endsWith('.md'));
}

async function writeChangelogInternal(a: any, skillsPath: string, date: string): Promise<string[]> {
  const written: string[] = [];
  const changesLines = (a.completed_work ?? []).map((w: any) => `- \`${w.path}\` — ${w.change} ${w.status}`).join("\n");
  const failedLines = (a.failed_actions ?? []).length > 0 ? (a.failed_actions as any[]).map((f: any) => `- **Attempted:** ${f.attempted}\n  **Happened:** ${f.happened}\n  **Recommendation:** ${f.recommendation}`).join("\n") : null;
  const blockerLines = (a.blockers ?? []).length > 0 ? (a.blockers as any[]).map((b: any) => `- ${b.description} — ${b.needed_to_unblock}`).join("\n") : null;
  const nextLines = (a.next_tasks ?? []).map((t: any, i: number) => `${i + 1}. ${t}`).join("\n");
  const handoffRef = a.handoff ? `handoffs/${String(a.handoff)}` : null;

  const rootContent = await fs.readFile(rootChangelogPath, "utf-8");
  const versionMatch = rootContent.match(/## \[(\d+)\.(\d+)\.(\d+)\]/);
  let newVersion = "1.0.0";
  if (versionMatch) {
    const [maj, min, pat] = [parseInt(versionMatch[1]), parseInt(versionMatch[2]), parseInt(versionMatch[3])];
    const bump = a.version_bump ?? "patch";
    newVersion = bump === "major" ? `${maj + 1}.0.0` : bump === "minor" ? `${maj}.${min + 1}.0` : `${maj}.${min}.${pat + 1}`;
  }
  const rootChanges = (a.completed_work ?? []).map((w: any) => `- \`${w.path}\` — ${w.change}`).join("\n");
  let rootEntry = `## [${newVersion}] — ${a.session_goal} (${date})\n\n**Changes:**\n${rootChanges}\n`;
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
      name: "list_agents",
      description: "List all active agents and governance (AGENTS.md). Returns the AGENTS.md contract and the directory index for agent roles.",
      inputSchema: { type: "object" }
    },
    {
      name: "get_agent",
      description: "Get specific agent instructions. Use this to establish persona and rules. Returns the role file for the requested agent_id and the global repository index.",
      inputSchema: {
        type: "object",
        properties: {
          agent_id: { type: "string", description: "The ID of the agent to retrieve (e.g. 'cowork', 'code', 'local')." }
        },
        required: ["agent_id"]
      }
    },
    { name: "list_skills", description: "List all skills in the skills domain. Use this to discover available SOPs and pipelines. Optionally filter by subdirectory domain.", inputSchema: { type: "object", properties: { domain: { type: "string", description: "Optional subdirectory within skills/" } } } },
    { name: "get_skill", description: "Get a skill from the repo. Use this to learn how to execute repo procedures. Path must be relative to skills/.", inputSchema: { type: "object", properties: { relativePath: { type: "string" } }, required: ["relativePath"] } },

    // --- INTELLIGENCE ---
    {
      name: "search_intelligence",
      description: "Search intelligence by query, taxonomy, or both. At least one of query or taxonomy is required. domain optionally scopes the search.",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Full-text keyword search" },
          taxonomy: { type: "string", description: "Filter by taxonomy frontmatter field (e.g. 'Notes', 'Service Plan')" },
          domain: { type: "string", description: "Scope to intelligence subdirectory" }
        }
      }
    },
    {
      name: "list_intelligence",
      description: "List intelligence across the domain. Use this to discover available knowledge and source data. Filters by type or taxonomy. Recursive by default.",
      inputSchema: {
        type: "object",
        properties: {
          domain: { type: "string", description: "Optional sub-domain to filter by (e.g. 'product/projects')" },
          type: { type: "string", description: "Filter by frontmatter type (e.g. 'prd', 'intelligence')" },
          taxonomy: { type: "string", description: "Filter by taxonomy term" },
          include_directories: { type: "boolean", description: "Legacy parameter (ignored)" }
        }
      }
    },
    {
      name: "get_intelligence",
      description: "Get intelligence or source files from the domain. Use this to retrieve domain knowledge. Path must be relative to intelligence/.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Path relative to intelligence/." },
          parse: { type: "boolean", description: "If true, returns parsed metadata instead of raw markdown." }
        },
        required: ["path"]
      }
    },
    {
      name: "edit_intelligence",
      description: "Edit intelligence. Use this to update content or link records. Can also establish relationships between records.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Path relative to intelligence/." },
          title: { type: "string", description: "New title (optional)" },
          metadata: { type: "object", description: "Metadata keys to update/add (optional)" },
          content: { type: "string", description: "New body content (optional)" },
          relationship: { type: "string", description: "Optional relationship type for linking" },
          targetPath: { type: "string", description: "Optional target path for linking" }
        },
        required: ["path"]
      }
    },
    {
      name: "add_intelligence",
      description: "Add intelligence. Use this to codify new domain knowledge. Automatically updates the domain index.",
      inputSchema: {
        type: "object",
        properties: {
          domain: { type: "string", description: "Subdirectory under intelligence/." },
          name: { type: "string", description: "Filename (no .md suffix)" },
          title: { type: "string" },
          metadata: { type: "object", description: "Key-value pairs for metadata" },
          content: { type: "string" }
        },
        required: ["domain", "name", "title", "content"]
      }
    },

    // --- CHANGELOGS ---
    { name: "get_changelog", description: "Get the project changelog. Use this to understand recent session context and version history.", inputSchema: { type: "object" } },
    {
      name: "add_changelog",
      description: "Add a changelog. Use this to track functional or structural changes. Supports subdirectory and root synchronization.",
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

    // --- HANDOFFS ---
    { name: "list_handoffs", description: "List active handoffs. Use this to discover open implementation plans and cross-agent tasks. Can filter by status or assigned agent.", inputSchema: { type: "object", properties: { status: { type: "string", enum: ["READY", "COMPLETE", "ALL"] }, limit: { type: "number" }, assigned_to: { type: "string" } } } },
    { name: "get_handoff", description: "Get a handoff by filename. Use this to retrieve implementation plans. Omit 'handoff/' prefix from the path.", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
    {
      name: "add_handoff",
      description: "Add a handoff. Use this to stage cross-agent implementation plans.",
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
    {
      name: "edit_handoff",
      description: "Edit a handoff or mark it as complete. Use this to update plan progress. Completion automatically archives the file.",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string" },
          content: { type: "string" },
          mark_complete: { type: "boolean" },
          summary: { type: "string" },
          session_goal: { type: "string" },
          completed_work: { type: "array", items: { type: "object", properties: { path: { type: "string" }, change: { type: "string" }, status: { type: "string" } } } },
          next_tasks: { type: "array", items: { type: "string" } },
          subdirectories: { type: "array", items: { type: "string" } },
          version_bump: { type: "string" }
        },
        required: ["path"]
      }
    },

    // --- REPORTS ---
    { name: "list_reports", description: "List available reports. Use this to discover which skills have generated pipeline outputs. Optionally scope to a domain.", inputSchema: { type: "object", properties: { domain: { type: "string" } } } },
    { name: "get_report", description: "Get the latest report for a specific skill. Use this to access pipeline outputs. Pass the skill name (e.g., 'status', 'tasks')—do not provide a file path.", inputSchema: { type: "object", properties: { skill: { type: "string" } }, required: ["skill"] } },
    {
      name: "run_report",
      description: "Run a report pipeline. do NOT use to read. Follow with get_report.",
      inputSchema: {
        type: "object",
        properties: {
          skill: { type: "string" },
          date: { type: "string" },
          dry_run: { type: "boolean" }
        },
        required: ["skill"]
      }
    },

    // --- EXTERNAL SYNC (Asana + Jira) ---
    {
      name: "search_tasks",
      description: "Search keywords in the latest tasks report. Use this to find existing tasks and prevent duplication. Returns matching tasks with status and links.",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Search query (keyword, ID, or project name)" }
        },
        required: ["query"]
      }
    },
    {
      name: "add_task",
      description: "Add a task to external systems (Asana/Jira) via raw capture. Use this to stage new deliverables.",
      inputSchema: {
        type: "object",
        properties: {
          text: { type: "string", description: "Raw capture text" },
          acceptance_criteria: { type: "string" },
          figma_link: { type: "string" },
          asana_project_gid: { type: "string" }
        },
        required: ["text"]
      }
    },

    // --- ART & MEDIA ---
    { name: "list_art", description: "List all art. Use this to discover available sketches, poems, and creative artifacts.", inputSchema: { type: "object" } },
    { name: "get_art", description: "Get an art piece from the gallery. Use this to view creative artifacts. Returns the specific piece by name/path.", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
    {
      name: "add_art",
      description: "Add art to the gallery. Use this to contribute creative artifacts.",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string" },
          title: { type: "string" },
          agent: { type: "string" },
          content: { type: "string" }
        },
        required: ["name", "title", "agent", "content"]
      }
    },
    {
      name: "refresh_mcp",
      description: "Rebuilds the MCP server and cleans up duplicate or orphan processes. Use this to apply code changes and ensure only one instance per host app is running.",
      inputSchema: { type: "object" }
    },
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    // --- AGENT ROLES & GOVERNANCE ---
    if (name === "list_agents") {
      const agentsMd = await fs.readFile(path.resolve(rootPath, "AGENTS.md"), "utf-8");
      const agentsDir = path.resolve(rootPath, "governance/agents");
      const files = await fs.readdir(agentsDir);
      const roles = files.filter(f => f.endsWith(".md") && !f.startsWith(".") && !["index.md", "overview.md", "policies.md", "taxonomy.md"].includes(f));
      return { content: [{ type: "text", text: `## AGENTS.md\n\n${agentsMd}\n\n**Available Role Files:**\n${roles.join("\n")}` }] };
    }

    if (name === "get_agent") {
      const { agent_id } = args as any;
      const agentPath = path.resolve(rootPath, "governance/agents", `${agent_id.toLowerCase()}.md`);
      const agentsMdPath = path.resolve(rootPath, "AGENTS.md");
      const indexPath = path.resolve(rootPath, "index.md");
      try {
        const [agentsMdContent, agentContent, indexContent] = await Promise.all([
          fs.readFile(agentsMdPath, "utf-8").catch(() => "AGENTS.md not found."),
          fs.readFile(agentPath, "utf-8"),
          fs.readFile(indexPath, "utf-8").catch(() => "Index not found.")
        ]);
        return {
          content: [
            { type: "text", text: `## AGENTS.md\n\n${agentsMdContent}` },
            { type: "text", text: `# Role Documentation: ${agent_id}\n\n${agentContent}` },
            { type: "text", text: `## Repository Index\n\n${indexContent}` }
          ]
        };
      } catch (err) {
        throw new Error(`Agent role documentation for '${agent_id}' not found at ${agentPath}`);
      }
    }

    // --- SKILLS & CAPABILITIES ---
    if (name === "list_skills") {
      const { domain = "" } = args as any;
      const targetPath = path.resolve(skillsPath, domain);
      if (!targetPath.startsWith(skillsPath)) throw new Error("Access denied");

      try {
        const results: any[] = [];
        const walk = async (dir: string) => {
          const entries = await fs.readdir(dir, { withFileTypes: true });
          for (const entry of entries) {
            if (entry.name.startsWith('.')) continue;
            const full = path.join(dir, entry.name);
            if (entry.isDirectory()) {
              await walk(full);
            } else if (entry.name === "SKILL.md") {
              const content = await fs.readFile(full, "utf-8");
              const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
              let title = path.basename(dir);
              let type = "skill";
              if (fmMatch) {
                const fm = parseFrontmatter(fmMatch[1]);
                if (fm.title) title = fm.title;
                if (fm.type) type = fm.type;
              }
              results.push({
                path: path.relative(skillsPath, full),
                title,
                type,
                domain: `skills/${path.relative(skillsPath, dir)}`
              });
            }
          }
        };
        await walk(targetPath);
        return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
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

    if (name === "refresh_mcp") {
      // 1. Rebuild
      await new Promise((resolve, reject) => {
        execFile("npm", ["run", "build"], { cwd: rootPath }, (err, stdout, stderr) => {
          if (err) reject(new Error(stderr || stdout));
          else resolve(stdout);
        });
      });

      // 2. Identify and prune others
      const { stdout: pids } = await new Promise<{ stdout: string }>((res) =>
        execFile("pgrep", ["-f", "ben-cp.js"], (err, stdout) => res({ stdout }))
      );

      const otherPids = pids.split('\n').map(p => p.trim()).filter(p => p && p !== process.pid.toString());

      for (const pid of otherPids) {
        try { process.kill(parseInt(pid), 'SIGTERM'); } catch { }
      }

      // 3. Schedule self-restart
      setTimeout(() => process.exit(0), 1000);

      return {
        content: [{
          type: "text",
          text: `Build successful. Killed ${otherPids.length} other instance(s). This server will now restart to apply changes.`
        }]
      };
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
        `> **Repo root:** ${rootPath}\n` +
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
            if (file === "index.md") continue;
            const fullPath = path.join(dir, file);
            const content = await fs.readFile(fullPath, "utf-8");
            
            let priority = "TBD";
            let status = dir.endsWith("complete") ? "COMPLETE" : "READY";
            let assignee = "Any";
            let date = file.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] ?? "unknown";

            const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
            if (fmMatch) {
              const fm = parseFrontmatter(fmMatch[1]);
              priority = fm.priority ?? priority;
              status = fm.status ?? status;
              assignee = fm.assigned_to ?? assignee;
              if (fm.date) date = fm.date;
            } else {
              const priorityMatch = content.match(/> \*\*Priority:\*\* (P\d)/);
              const statusMatch = content.match(/> \*\*STATUS\*\*:\s*(.*?)$/m) || content.match(/> \*\*STATUS:?\s*(.*?)$/m);
              const assignedMatch = content.match(/> \*\*Assigned to:\*\* (.*?)$/m);
              if (priorityMatch) priority = priorityMatch[1];
              if (statusMatch) status = statusMatch[1].trim();
              if (assignedMatch) assignee = assignedMatch[1].trim();
            }

            if (assigned_to && assigned_to.toLowerCase() !== 'any' && assignee.toLowerCase() !== 'any' && !assignee.toLowerCase().includes(assigned_to.toLowerCase())) {
              continue;
            }

            results.push({
              file,
              path: path.relative(path.resolve(handoffPath, ".."), fullPath),
              priority,
              status,
              date,
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
        const targetFilename = `${path.basename(relPath, ".md")}-ARCHIVE.md`;
        const targetPath = path.join(handoffPath, "archive", targetFilename);
        const content = await fs.readFile(sourcePath, "utf-8");
        const statusRegex = /> \*\*STATUS:?.*$/m;
        const updatedContent = content.replace(statusRegex, `> **STATUS**: ✅ COMPLETE — ${date}\n\n${a.summary}`);
        await fs.mkdir(path.join(handoffPath, "archive"), { recursive: true });
        await fs.writeFile(targetPath, updatedContent, "utf-8");
        await fs.unlink(sourcePath);
        await writeChangelogInternal({ ...a, handoff: `archive/${targetFilename}` }, skillsPath, date);
        return { content: [{ type: "text", text: `Handoff completed and archived to ${targetFilename}.` }] };
      } else {
        if (!a.content) throw new Error("Content required for non-completion edit.");
        await fs.writeFile(sourcePath, a.content, "utf-8");
        return { content: [{ type: "text", text: "Handoff updated." }] };
      }
    }

    // --- ART & MEDIA ---
    if (name === "add_art") {
      const { name: fileName, title, agent, content } = args as any;
      const artRoot = path.resolve(rootPath, "intelligence/art");
      await fs.mkdir(artRoot, { recursive: true });
      const sanitizedFilename = ensureSingleExtension(fileName);
      const fullPath = path.join(artRoot, sanitizedFilename);
      const date = new Date().toISOString().split('T')[0];
      const fullContent = `# ${title}\n\n> **Artist:** ${agent}\n> **Date:** ${date}\n\n${content}\n`;
      await fs.writeFile(fullPath, fullContent, "utf-8");

      // Update Index
      const indexPath = path.join(artRoot, "overview.md");
      let indexContent = "# Art Gallery\n\n";
      try { indexContent = await fs.readFile(indexPath, "utf-8"); } catch { }
      if (!indexContent.includes(`[${title}]`)) {
        indexContent += `- [${title}](${fileName}.md) — by ${agent} (${date})\n`;
        await fs.writeFile(indexPath, indexContent, "utf-8");
      }

      return { content: [{ type: "text", text: `Art piece "${title}" added to gallery.` }] };
    }

    if (name === "list_art") {
      const artRoot = path.resolve(rootPath, "intelligence/art");
      const entries = await fs.readdir(artRoot, { withFileTypes: true });
      const files = entries
        .filter(e => !e.name.startsWith(".") && e.name.endsWith(".md") && !["index.md", "overview.md", "changelog.md"].includes(e.name))
        .map(e => e.name);
      return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
    }

    if (name === "get_art") {
      const { path: relPath } = args as any;
      const artRoot = path.resolve(rootPath, "intelligence/art");
      const normalized = String(relPath).startsWith("intelligence/art/") ? String(relPath).slice(17) : (String(relPath).startsWith("art/") ? String(relPath).slice(4) : relPath);
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
      return { content: [{ type: "text", text: "Intelligence record created." }] };
    }

    if (name === "edit_intelligence") {
      const { path: relPath, title, metadata = {}, content, relationship, targetPath } = args as any;
      const normalized = String(relPath).startsWith("intelligence/") ? String(relPath).slice(13) : relPath;
      let fullPath = path.resolve(rootPath, "intelligence", normalized);

      try {
        await fs.access(fullPath);
      } catch {
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
      let newContent = `# ${currentTitle}\n\n${metaBlock}\n${currentBody}`;

      // Handle embedded linking logic
      if (relationship && targetPath) {
        const tPath = path.resolve(rootPath, "intelligence", targetPath.endsWith(".md") ? targetPath : `${targetPath}.md`);
        const tCont = await fs.readFile(tPath, "utf-8");
        newContent = newContent.replace(/(# .*\n\n)/, `$1- **${relationship}:** [[${targetPath}]]\n`);
        await fs.writeFile(tPath, tCont.replace(/(# .*\n\n)/, `$1- **linked-by:** [[${relPath}]] (${relationship})\n`), "utf-8");
      }

      await fs.writeFile(fullPath, newContent, "utf-8");
      return { content: [{ type: "text", text: `Intelligence record ${relPath} updated${relationship ? " and linked" : ""}.` }] };
    }

    if (name === "list_intelligence") {
      const { domain = "", type, taxonomy } = args as any;
      const intelligenceRoot = path.resolve(rootPath, "intelligence");
      const targetPath = path.resolve(intelligenceRoot, domain);
      if (!targetPath.startsWith(intelligenceRoot)) throw new Error("Access denied");

      const items: any[] = [];
      const walk = async (dir: string) => {
        const entries = await fs.readdir(dir, { withFileTypes: true });
        for (const entry of entries) {
          if (entry.name.startsWith('.') || entry.name === "index.md" || entry.name === "changelog.md") continue;
          const full = path.join(dir, entry.name);
          if (entry.isDirectory()) {
            await walk(full);
          } else if (entry.name.endsWith(".md")) {
            const content = await fs.readFile(full, "utf-8");
            const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
            let itemType = null;
            let itemTaxonomy: string[] = [];
            let itemTitle = entry.name;
            let itemLinks = null;

            if (fmMatch) {
              const fm = parseFrontmatter(fmMatch[1]);
              itemType = fm.type || null;
              if (fm.taxonomy) itemTaxonomy = fm.taxonomy.split(',').map(t => t.trim());
              if (fm.title) itemTitle = fm.title;
              
              // Extract links sub-object if present
              const linksMatch = fmMatch[1].match(/links:\n((?:\s+[\w_-]+: .+\n?)*)/);
              if (linksMatch) {
                itemLinks = {};
                for (const line of linksMatch[1].split('\n')) {
                  const m = line.match(/^\s+([\w_-]+):\s*(.+)$/);
                  if (m) (itemLinks as any)[m[1]] = m[2].trim().replace(/^['"]|['"]$/g, '');
                }
              }
            } else {
              // Fallback to legacy scraping
              const titleMatch = content.match(/^# (.*)/);
              if (titleMatch) itemTitle = titleMatch[1];
              itemTaxonomy = parseTaxonomy(content);
              const typeMatch = content.match(/- \*\*type:\*\*\s*(.+)/i);
              if (typeMatch) itemType = typeMatch[1].trim();
            }

            // Apply filters
            if (type && itemType !== type) continue;
            if (taxonomy && !itemTaxonomy.some(t => t.toLowerCase().includes(taxonomy.toLowerCase()))) continue;

            items.push({
              path: path.relative(intelligenceRoot, full),
              title: itemTitle,
              type: itemType,
              domain: path.relative(intelligenceRoot, dir),
              taxonomy: itemTaxonomy.join(", "),
              links: itemLinks
            });
          } else {
            // Source files, etc
            items.push({
              name: entry.name,
              type: "file",
              path: path.relative(intelligenceRoot, full)
            });
          }
        }
      };

      await walk(targetPath);
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
        const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
        const metadata: Record<string, string> = {};
        let title = content.split('\n')[0].replace(/^# /, '');

        if (fmMatch) {
          const fm = parseFrontmatter(fmMatch[1]);
          Object.assign(metadata, fm);
          if (fm.title) title = fm.title;
        } else {
          const matches = content.matchAll(/- \*\*([^:]+):\*\* (.*)/g);
          for (const match of matches) { metadata[match[1]] = match[2].trim(); }
        }
        return { content: [{ type: "text", text: JSON.stringify({ path: relPath, title, metadata }, null, 2) }] };
      }
      return { content: [{ type: "text", text: content }] };
    }

    if (name === "search_intelligence") {
      const { query, taxonomy, domain = "" } = args as any;
      if (!query && !taxonomy) {
        throw new Error("At least one of 'query' or 'taxonomy' must be provided.");
      }

      const searchPath = path.resolve(rootPath, "intelligence", domain);
      let queryResults: Set<string> | null = null;
      let taxonomyResults: Set<string> | null = null;

      // Phase 1: Query (Grep)
      if (query) {
        const { stdout } = await new Promise<{ stdout: string; stderr: string }>((resolve, reject) => {
          execFile(process.platform === "win32" ? "cmd.exe" : "/bin/sh", [process.platform === "win32" ? "/c" : "-c", `grep -rli "${query.replace(/"/g, '\\"')}" "${searchPath}" --include="*.md"`], (err, stdout, stderr) => {
            if (err && err.code !== 1) reject(err); else resolve({ stdout, stderr });
          });
        });
        queryResults = new Set(stdout.split('\n').filter(p => p.trim()));
      }

      // Phase 2: Taxonomy (Walk + Parse)
      if (taxonomy) {
        const files = await walkDir(searchPath);
        taxonomyResults = new Set();
        for (const f of files) {
          const content = await fs.readFile(f, "utf-8");
          const tags = parseTaxonomy(content);
          if (tags.some(t => t.toLowerCase().includes(taxonomy.toLowerCase()) && t.toLowerCase() !== 'none')) {
            taxonomyResults.add(f);
          }
        }
      }

      // Phase 3: Combine
      let finalResults: string[];
      if (queryResults && taxonomyResults) {
        // Intersection
        finalResults = [...queryResults].filter(f => taxonomyResults!.has(f));
      } else {
        finalResults = [...(queryResults || taxonomyResults || [])];
      }

      return { content: [{ type: "text", text: JSON.stringify(finalResults.map(p => path.relative(rootPath, p)), null, 2) }] };
    }





    // --- CHANGELOGS & HISTORY ---
    if (name === "add_changelog") {
      const a = args as any;
      await writeChangelogInternal(a, skillsPath, new Date().toISOString().split('T')[0]);
      return { content: [{ type: "text", text: "Changelog written." }] };
    }

    if (name === "get_changelog") {
      const content = await fs.readFile(rootChangelogPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    // --- REPORTING & OUTPUTS ---
    if (name === "run_report") {
      const skill = String((args as any)?.skill ?? "");
      let script = "";
      let cmdArgs: string[] = [];

      if (skill === "status") {
        script = path.resolve(rootPath, "skills/status/run.py");
        cmdArgs = ["--force", "--team", "platform"];
      } else if (skill === "dream" || skill === "reporting") {
        script = path.resolve(rootPath, "skills/dream/run.py");
        if ((args as any).date) cmdArgs.push("--date", (args as any).date);
        if ((args as any).dry_run) cmdArgs.push("--dry-run");
      } else if (skill === "tasks") {
        script = path.resolve(rootPath, "skills/tasks/run.py");
      } else if (skill === "releasinator") {
        script = path.resolve(rootPath, "skills/releasinator/scripts/run.py");
        if ((args as any).date) cmdArgs.push("--release", (args as any).date);
      } else {
        throw new Error(`Report generation not automated for skill: ${skill}. Valid options: status, dream, tasks, releasinator.`);
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
      const { skill } = args as any;
      if (!skill) throw new Error("'skill' is required. e.g. get_report(skill='status')");
      const baseReportsPath = path.resolve(rootPath, "reports");
      const fullPath = path.resolve(baseReportsPath, String(skill), "report.md");
      if (!fullPath.startsWith(baseReportsPath)) throw new Error("Access denied: Outside reports directory.");
      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    // --- TASK CAPTURE (Asana + Jira) ---

    function inferProductArea(t: string): string {
      const s = t.toLowerCase();
      const matchedOverrides = new Set<string>();
      const matchedProducts = new Set<string>();
      const matchedFeatures = new Set<string>();

      for (const rule of taxonomyRules) {
        if (rule.regexes.some(re => re.test(s))) {
          if (rule.isOverride) matchedOverrides.add(rule.label);
          if (rule.isProduct) matchedProducts.add(rule.label);
          if (rule.isFeature) matchedFeatures.add(rule.label);
        }
      }

      if (matchedOverrides.size > 0) return Array.from(matchedOverrides).sort().join(", ");

      const overlaps = new Set([...matchedProducts].filter(x => matchedFeatures.has(x)));
      for (const label of overlaps) {
        if (matchedProducts.size > 1) {
          matchedProducts.delete(label);
        } else if (matchedFeatures.size > 1) {
          matchedFeatures.delete(label);
        } else {
          matchedFeatures.delete(label);
        }
      }

      const p = Array.from(matchedProducts).sort();
      const f = Array.from(matchedFeatures).sort();

      if (p.length > 0 && f.length > 0) return `${p.join(", ")} - ${f.join(", ")}`;
      if (p.length > 0) return p.join(", ");
      if (f.length > 0) return f.join(", ");
      return "";
    }

    function getPopulatedTemplate(type: string, area: string, text: string, options: any = {}): string {
      const summary = area ? `${area} — ${text}` : text;
      if (type === "bug") {
        let t = `## Summary\n${summary}\n\n## Description\n${text}\n\n## Steps to Reproduce\n1. \n2. \n3. \n\n## Expected Behavior\n\n## Actual Behavior\n\n## Environment\n- Tenant: \n- Browser/Device: \n- Release/Version: \n\n## Severity\n[ ] Critical \u2014 blocks release\n[ ] High \n[ ] Medium \n[ ] Low \n\n## Links\n- Asana Project: ${options.asana_link || ""}`;
        if (options.figma_link) t += `\n- Figma Designs: ${options.figma_link}`;
        return t;
      }
      if (type === "cx_bug") {
        return `## Summary\n${summary}\n\n## Customer / Tenant\n- Reported by: \n- Tenant name: \n- Severity to customer: \n\n## Description\n${text}\n\n## Steps to Reproduce\n1. \n2. \n3. \n\n## Expected Behavior\n\n## Actual Behavior\n\n## Workaround Available?\n[ ] Yes \n[ ] No\n\n## Release Blocker?\n[ ] Yes\n[ ] No\n\n## Links\n- Asana Project: ${options.asana_link || ""}\n- Support ticket / Slack thread: `;
      }
      if (type === "story") {
        let t = `Summary: "${summary}"\n\n## PRD link\n\n## Introduction\n${text}\n\nAs a [user], I want [goal] so that [value].\n\n## Use cases\n## Use case 1: \n\n## Edge cases\n1. \n\n## Out of scope\n1. `;
        if (options.acceptance_criteria) t += `\n\n## Acceptance Criteria\n${options.acceptance_criteria}`;
        if (options.figma_link || options.asana_link) {
          t += `\n\n## Links`;
          if (options.asana_link) t += `\n- Asana Project: ${options.asana_link}`;
          if (options.figma_link) t += `\n- Figma Designs: ${options.figma_link}`;
        }
        return t;
      }
      if (type === "research") {
        return `## Summary\n${summary}\n\n## Objective\n${text}\n\n## Methodology\n\n## Findings\n\n## Next Steps`;
      }
      // Default / Task
      let t = `## Summary\n${summary}\n\n## Introduction\n${text}`;
      if (options.acceptance_criteria) t += `\n\n## Acceptance Criteria\n${options.acceptance_criteria}`;
      if (options.figma_link || options.asana_link) {
        t += `\n\n## Links`;
        if (options.asana_link) t += `\n- Asana Project: ${options.asana_link}`;
        if (options.figma_link) t += `\n- Figma Designs: ${options.figma_link}`;
      }
      return t;
    }

    if (name === "search_tasks") {
      const { query } = args as any;
      const tasksReportPath = path.resolve(rootPath, "reports", "tasks", "report.md");
      try {
        const content = await fs.readFile(tasksReportPath, "utf-8");
        const lines = content.split("\n");
        const queryLower = query.toLowerCase();
        
        // Find matching task lines (bullet points with links)
        const matches = lines.filter(line => {
          const l = line.trim();
          return l.startsWith("- [") && l.toLowerCase().includes(queryLower);
        });
        
        if (matches.length === 0) {
          return { content: [{ type: "text", text: `🔍 No tasks matching "${query}" found in the latest report.` }] };
        }
        
        return { content: [{ type: "text", text: `🔍 Found ${matches.length} matching task(s) in the latest report:\n\n${matches.join("\n")}` }] };
      } catch (err: any) {
        throw new Error(`Failed to read task report for searching: ${err.message}`);
      }
    }

    if (name === "add_task") {
      const { text, acceptance_criteria, figma_link, asana_project_gid: overrideGid } = args as any;
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
      let projectGid = overrideGid || "1208693459152262"; // PD - Small Projects fallback
      if (!overrideGid) {
        if (/\bgp\b|granular perm/i.test(text)) projectGid = "1208693459152262";
        else if (/\bnotes\b/i.test(text)) projectGid = "1211726272848115";
        else if (/\benroll/i.test(text)) projectGid = "1211631356870657";
      }

      const asanaUrl = `https://app.asana.com/0/${projectGid}/board`;
      const options = { acceptance_criteria, figma_link, asana_link: asanaUrl };

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
        const jiraSummary = productArea ? `${productArea} — ${text}` : text;
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
        const summaryText = productArea ? `${productArea} — ${text}` : text;
        const templateNotes = getPopulatedTemplate("task", productArea, text, options);
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
      const summaryText = productArea ? `${productArea} — ${text}` : text;
      const typeKey = isBug ? "bug" : isCxBug ? "cx_bug" : isStory ? "story" : isResearch ? "research" : isQafe ? "qafe" : "task";
      const descText = getPopulatedTemplate(typeKey, productArea, text, options);
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

    throw new Error(`Tool not found: ${name}`);
  } catch (error: any) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
