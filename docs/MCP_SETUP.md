# MCP Server Setup Guide

This guide walks through installing and using all Model Context Protocol (MCP) servers configured for Pong AI V2 on Windows. The instructions are based on the official README files published by each project (Playwright MCP, Serena, Sequential Thinking, MCP Knowledge Graph, and Perplexity API Platform MCP) that were fetched on 2025-10-09. Google searches returned CAPTCHA blocks, so each server was verified directly from its GitHub source.

> **Tip:** Keep Visual Studio Code open while you follow the steps so it can restart the servers after each change.

## 1. Prerequisites

- **Python 3.10+** with the [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager installed (used by Serena and Sequential Thinking).
- **Node.js 18+** and npm (required for Playwright, Knowledge Graph, and Perplexity servers that run through `npx`).
- A **Perplexity API key** and a **Context7 API key**.
- Optional but recommended: create the memory directory once before starting the Knowledge Graph server:
  ```powershell
  New-Item -ItemType Directory -Force "$env:USERPROFILE\.aim"
  ```

## 2. Environment Variables

The repository now includes a `.env` file with placeholders:
```
CONTEXT7_API_KEY=REPLACE_WITH_CONTEXT7_KEY
PERPLEXITY_API_KEY=REPLACE_WITH_PERPLEXITY_KEY
```

1. Replace the placeholders with your real keys.
2. Restart VS Code after updating `.env` so it picks up the values.

If you prefer, you can also set them permanently in PowerShell:
```powershell
setx CONTEXT7_API_KEY "your-context7-key"
setx PERPLEXITY_API_KEY "your-perplexity-key"
```
(Log out/in to use the keys everywhere.)

## 3. VS Code MCP Configuration

The global `mcp.json` file now contains entries for all servers:

- **Playwright** – launches with `npx @playwright/mcp@latest`.
- **Serena** – runs via `uvx` with the `ide-assistant` context and your project path.
- **Sequential Thinking** – runs via `uvx` pulling from `arben-adm/mcp-sequential-thinking`.
- **Knowledge Graph** – launches with `npx mcp-knowledge-graph` and writes memories to `%USERPROFILE%\.aim`.
- **Perplexity** – launches with `npx @perplexity-ai/mcp-server` and reads `PERPLEXITY_API_KEY` from your environment.
- **Context7** – already present, uses the hosted HTTP endpoint.

If the project moves, update the Serena `--project` argument to the new absolute path.

## 4. First-Time Installation Checks

1. **Playwright MCP**
   - VS Code will install it automatically on first use.
   - To install manually: `npm install -g @playwright/mcp`.

2. **Serena**
   - Ensure uv is installed (`pip install uv` or download the standalone binary).
   - On first run, Serena will create `C:\Users\Nexia\.serena` with configuration.
   - The `ide-assistant` context is recommended by the official README for IDE integrations.

3. **Sequential Thinking MCP**
   - `uvx` downloads dependencies into its cache automatically.
   - Optional: run tests from the README with `uvx --from git+https://github.com/arben-adm/mcp-sequential-thinking pytest`.

4. **MCP Knowledge Graph**
   - Creates memory files inside the `.aim` folder.
   - Every file starts with a safety marker; do not edit them manually.

5. **Perplexity MCP**
   - Requires a valid API key with sufficient quota.
   - You can switch models (e.g., `sonar-pro`, `sonar-reasoning-pro`) by passing flags when you run the server manually; the defaults match the README.

## 5. Verifying Each Server

After restarting VS Code:

1. Open Copilot / chat panel.
2. Type `/mcp list` (or use the MCP servers view) to confirm each server starts without errors.
3. Try a simple command for each server:
   - Playwright: "Take a snapshot of https://example.com" (server will request permission).
   - Serena: "Activate the project" followed by `C:\Users\Nexia\OneDrive\Escritorio\pong ai v2`.
   - Sequential Thinking: "Add a new thought".
   - Knowledge Graph: "Create an entity named Demo".
   - Perplexity: "Search for the latest pygame release".

If a server fails to start, open the **Output** > **Model Context Protocol** panel for logs. Common fixes include reinstalling Node.js, running `uv self update`, or re-entering API keys.

## 6. Keeping Things Updated

- **Playwright MCP**: update with `npm update -g @playwright/mcp`.
- **Serena & Sequential Thinking**: rerun their `uvx` commands (uv will fetch the latest release).
- **Knowledge Graph & Perplexity**: rerun `npx` with `-y` to refresh.

Because the instructions come straight from the official GitHub repositories, you do not need to search for alternate sources unless you want a fork with different features.

## 7. Troubleshooting Quick Reference

| Server | Typical Issue | Fix |
| ------ | ------------- | --- |
| Playwright | Node.js < 18 | Install current LTS from nodejs.org |
| Serena | uv missing | Install uv and restart terminal |
| Sequential Thinking | Windows path with spaces | Leave the provided path in quotes (already handled) |
| Knowledge Graph | Memory files missing | Run `New-Item -ItemType Directory -Force "$env:USERPROFILE\.aim"` |
| Perplexity | 401 errors | Re-check API key and quota |

With these steps, all five MCP servers (plus Context7) will be available inside VS Code. You can now combine them in Copilot/Cursor-style workflows without additional setup.
