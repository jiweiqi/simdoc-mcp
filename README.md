# SimDoc MCP Server

MCP (Model Context Protocol) server providing access to scientific simulation documentation through Claude Desktop and Cursor.

## For End Users

**Just want to use SimDoc?** You don't need to run this server yourself!

### Quick Setup (2 minutes)

**Step 1:** Locate your config file
- **Claude Desktop (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Desktop (Windows)**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Cursor**: `~/.cursor/mcp.json`

**Step 2:** Add SimDoc to your config

```json
{
  "mcpServers": {
    "simdoc": {
      "url": "http://simdoc.subspace-lab.com:8080/sse"
    }
  }
}
```

**Step 3:** Restart Claude Desktop or Cursor

**Step 4:** Try it out!

Ask Claude:
- "How do I simulate battery aging in PyBaMM?"
- "Show me Cantera reactor network examples"

---

## Features

- 🔍 Search scientific simulation documentation (PyBaMM, Cantera, and more)
- 🤖 AI-powered code snippet retrieval with relevance scoring
- 📚 Structured simulator metadata and version resolution
- 🔌 Works with Claude Desktop and Cursor
- 🚀 Hosted and maintained - no setup required

## Available MCP Tools

### `resolve-simulator-id`
Find simulators by name with metadata, versions, and trust scores.

**Example usage in Claude:**
> "What simulators are available for battery modeling?"

### `get-simulator-docs`
Search and retrieve code snippets from simulator documentation.

**Example usage in Claude:**
> "Show me PyBaMM examples for SEI layer growth"
> "How do I create a premixed flame in Cantera?"

---

## For Developers

This repository contains the open-source MCP server implementation. It's provided for transparency and as a reference for MCP protocol implementation.

### Running Your Own Instance (Optional)

If you want to run your own MCP server instance:

```bash
# 1. Clone the repository
git clone https://github.com/jiweiqi/simdoc-mcp.git
cd simdoc-mcp

# 2. Configure backend URL
cp .env.example .env
# Edit .env and set BACKEND_URL

# 3. Run with Docker Compose
docker-compose up -d
```

**Note:** You'll need access to a SimDoc backend API. The hosted version uses our internal backend.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | Required | SimDoc backend API endpoint |
| `HOST` | `0.0.0.0` | Server host to bind to |
| `PORT` | `8080` | Server port |
| `LOG_LEVEL` | `INFO` | Logging level |
| `TRANSPORT` | `sse` | MCP transport protocol |

---

## Architecture

```
┌──────────────┐
│ Claude/Cursor│  MCP Protocol over SSE
└──────┬───────┘
       │
┌──────▼───────┐
│ MCP Server   │  Port 8080 (FastMCP)
│ simdoc-mcp   │  This repository
└──────┬───────┘
       │ HTTP REST API
┌──────▼───────┐
│ Backend API  │  SimDoc backend
│              │  (Separate deployment)
└──────────────┘
```

This repository contains only the MCP protocol layer. The backend (search, indexing, AI summarization) is maintained separately.

---

## Supported Simulators

Currently available:
- **PyBaMM** - Python Battery Mathematical Modeling
- **Cantera** - Chemical kinetics, thermodynamics, and transport
- More coming soon!

---

## Troubleshooting

### Tools not appearing in Claude/Cursor

1. Verify config file location and syntax
2. Make sure you restarted Claude Desktop completely (quit and reopen)
3. Check the URL is correct: `http://simdoc.subspace-lab.com:8080/sse`

### Getting errors when using tools

The hosted server should be running 24/7. If you encounter issues, please open a GitHub issue.

---

## Contributing

This repository is maintained by the SimDoc team. We develop internally and sync to this public repo for transparency.

**Want to help?**
- Report issues if tools don't work
- Suggest new simulators to add
- Share feedback on search quality

We don't accept code contributions at this time, but appreciate bug reports and feature requests!

---

## Development

Development happens in our private repository and is synced here. This ensures:
- Quality control of the MCP implementation
- Coordination with backend development
- Consistent user experience

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Supports [Model Context Protocol](https://modelcontextprotocol.io/)
- Designed for scientific computing communities

---

## Support

- **Issues**: [GitHub Issues](https://github.com/jiweiqi/simdoc-mcp/issues)
- **Questions**: Open a GitHub issue with your question
