# SimDoc MCP Server

AI-powered code search for scientific simulation documentation. Search PyBaMM, Cantera, and other simulators directly from your AI coding assistant.

## 🚀 Quick Start

### Using the Public Hosted Service (Recommended)

SimDoc provides a **free public MCP server** - no installation required.

**Endpoint:** `https://simdoc.subspace-lab.com/sse`

**Step 1: Add SimDoc to your AI assistant**

Choose your tool:

<details>
<summary><b>Claude Desktop</b></summary>

**Config file location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Add this configuration:**
```json
{
  "mcpServers": {
    "simdoc": {
      "url": "https://simdoc.subspace-lab.com/sse"
    }
  }
}
```
</details>

<details>
<summary><b>Claude Code</b></summary>

**Config file location:**
- Project: `.mcp.json` (in project root)
- User: `~/.claude/settings.local.json`

**Add this configuration:**
```json
{
  "mcpServers": {
    "simdoc": {
      "type": "sse",
      "url": "https://simdoc.subspace-lab.com/sse"
    }
  }
}
```
</details>

<details>
<summary><b>Cursor</b></summary>

**Config file location:** `~/.cursor/mcp.json`

**Add this configuration:**
```json
{
  "mcpServers": {
    "simdoc": {
      "url": "https://simdoc.subspace-lab.com/sse"
    }
  }
}
```
</details>

<details>
<summary><b>Cline (VS Code)</b></summary>

**Setup:** Click "Configure MCP Servers" in Cline extension panel

**Add this configuration:**
```json
{
  "mcpServers": {
    "simdoc": {
      "url": "https://simdoc.subspace-lab.com/sse",
      "alwaysAllow": []
    }
  }
}
```
</details>

<details>
<summary><b>Windsurf</b></summary>

**Config file location:** Windsurf MCP settings

**Add this configuration:**
```json
{
  "mcpServers": {
    "simdoc": {
      "url": "https://simdoc.subspace-lab.com/sse"
    }
  }
}
```
</details>

**Step 2: Restart your AI assistant**

Completely quit and reopen your AI tool.

**Step 3: Try it!**

Ask your AI assistant:
- *"How do I simulate battery aging in PyBaMM?"*
- *"Show me Cantera reactor network examples"*
- *"How can I model battery degradation over drive cycles?"*

---

## 🎯 What You Get

### Available Simulators

| Simulator | Documentation | Examples |
|-----------|---------------|----------|
| **PyBaMM** | Battery modeling | 120+ files |
| **Cantera** | Chemical kinetics & thermodynamics | 98+ files |

### MCP Tools

- **`resolve-simulator-id`** - Find simulators by name with metadata
- **`get-simulator-docs`** - Search code snippets and documentation

### Example Queries

1. **Battery Simulations**
   - "How do I simulate SEI layer growth in PyBaMM?"
   - "Show me battery calendar aging examples"
   - "How to simulate realistic driving conditions?"

2. **Reactor Networks**
   - "Set up a continuously stirred reactor in Cantera"
   - "Calculate ignition delay times"

3. **Thermodynamics**
   - "How to calculate specific heat of gas mixtures?"
   - "Get entropy and enthalpy properties"

---

## 🏗️ How It Works

```
┌──────────────────┐
│ Your AI Client   │
│ (Claude/Cursor)  │
└────────┬─────────┘
         │
         │ HTTPS MCP Protocol
         │
┌────────▼─────────┐
│ SimDoc Service   │  https://simdoc.subspace-lab.com/sse
│ (Hosted)         │
└──────────────────┘
```

SimDoc provides MCP tools to search scientific simulation documentation. Just add the endpoint to your AI client and start asking questions.

---

## 🐛 Troubleshooting

### MCP tools not appearing in your AI client

1. **Verify config file location and syntax**
   ```bash
   # Claude Desktop (macOS)
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Validate JSON syntax
   python3 -m json.tool < config.json
   ```

2. **Check the URL is correct**
   - Should be: `https://simdoc.subspace-lab.com/sse`
   - Common mistake: Using `http://` instead of `https://`

3. **Restart your AI client completely**
   ```bash
   # Claude Desktop (macOS)
   killall Claude && open -a Claude
   ```

4. **Test the endpoint directly**
   ```bash
   curl https://simdoc.subspace-lab.com/sse
   # Expected: "event: endpoint" response
   ```

5. **Check your AI client's MCP logs**
   - Claude Desktop (macOS): `~/Library/Logs/Claude/mcp*.log`
   - Look for connection errors or timeout messages

---

## 📖 More Information

- **Example Queries**: [MCP Showcase](../md-files/MCP_SHOWCASE.md) - Real usage examples
- **Main Repository**: [SimDoc README](../README.md) - Full project overview
- **Report Issues**: [GitHub Issues](https://github.com/your-org/simdoc/issues)

---

## 🤝 Contributing

Contributions welcome! See the main repository for guidelines.

---

## 📝 License

MIT License - see LICENSE file for details.

---

**Built with** ❤️ **for the scientific computing community**
