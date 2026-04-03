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

// Automatically find the 'sop' folder relative to this file's location
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const sopPath = path.resolve(__dirname, "../sop");

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_sop",
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
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    if (name === "get_sop") {
      const fullPath = path.resolve(sopPath, String(args?.relativePath));
      
      // Prevent path traversal outside of the sopPath
      if (!fullPath.startsWith(path.resolve(sopPath))) {
        throw new Error("Access denied: Invalid path");
      }

      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }
    if (name === "list_vault") {
      const allItems = await fs.readdir(sopPath, { recursive: true, withFileTypes: true });
      const files = allItems
        .filter(dirent => dirent.isFile() && !dirent.name.startsWith('.'))
        .map(dirent => path.join(dirent.parentPath, dirent.name).replace(sopPath + path.sep, ''));

      return { content: [{ type: "text", text: files.join("\n") }] };
    }
    throw new Error(`Tool not found: ${name}`);
  } catch (error: any) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);