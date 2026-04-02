// ben-cp.ts - Personal MCP Server (SSE / Express Edition)
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { CallToolRequestSchema, ListToolsRequestSchema, Tool } from "@modelcontextprotocol/sdk/types.js";
import express from "express";
import fs from "fs/promises";
import path from "path";

// --- Interfaces ---
interface RequestError {
  status?: number;
  message?: string;
  body?: unknown;
}

interface ToolArguments {
  filename?: string;
}

// --- Helper Functions ---
function serializeError(error: unknown): object {
  if (error instanceof Error) {
    return { error: true, message: error.message, name: error.name };
  } else if (typeof error === 'object' && error !== null) {
    const errObj = error as RequestError;
    return { error: true, status: errObj.status, message: errObj.message || String(error) };
  }
  return { error: true, message: String(error) };
}

// --- Tool Definitions ---
const tools: Tool[] = [
  {
    name: "get_skill_template",
    description: "Read a Markdown skill template or SOP from the local Skill Vault on the Desktop.",
    inputSchema: {
      type: "object",
      properties: {
        filename: { type: "string", description: "The exact name of the .md file (e.g., 'sop.md')" }
      },
      required: ["filename"]
    }
  }
];

// --- Server Instance ---
function createMCPServer() {
  const server = new Server({ name: "ben-cp", version: "1.0.0" }, { capabilities: { tools: {} } });

  server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools }));

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: rawArgs } = request.params;
    const args = (rawArgs || {}) as ToolArguments;

    try {
      if (name === "get_skill_template") {
        const vaultPath = process.env.SKILL_VAULT_PATH || path.join(process.env.HOME || "", "Desktop", "SkillVault");
        const filePath = path.join(vaultPath, args.filename!);
        const content = await fs.readFile(filePath, "utf-8");
        return { content: [{ type: "text", text: content }] };
      }

      throw new Error(`Unknown tool: ${name}`);
    } catch (error) {
      return { content: [{ type: "text", text: JSON.stringify(serializeError(error), null, 2) }], isError: true };
    }
  });

  return server;
}

// --- SSE / Express Server ---
async function main() {
  const server = createMCPServer();
  const app = express();
  let transport: SSEServerTransport;

  app.get("/sse", async (req, res) => {
    transport = new SSEServerTransport("/messages", res);
    await server.connect(transport);
    console.error("🟢 Connected to BenCP via SSE");
  });

  app.post("/messages", async (req, res) => {
    if (!transport) return res.status(400).send("No active SSE connection");
    await transport.handlePostMessage(req, res);
  });

  const PORT = parseInt(process.env.PORT || '3001', 10);
  app.listen(PORT, () => {
    console.error(`🟢 BenCP MCP Server running on port ${PORT}`);
    console.error(`📁 Skill Vault: ${process.env.SKILL_VAULT_PATH || '~/Desktop/SkillVault'}`);
  });
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
