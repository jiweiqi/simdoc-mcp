# SimDoc MCP Server

MCP (Model Context Protocol) server providing access to scientific simulation documentation through Claude Desktop and Cursor.

## Features

- 🔍 Search scientific simulation documentation (PyBaMM, Cantera, and more)
- 🤖 AI-powered code snippet retrieval with relevance scoring
- 📚 Structured simulator metadata and version resolution
- 🔌 Easy integration with Claude Desktop and Cursor
- 🐳 Docker deployment for production use

## Quick Start

### Using Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/jiweiqi/simdoc-mcp.git
cd simdoc-mcp

# 2. Configure backend URL
cp .env.example .env
# Edit .env and set BACKEND_URL to a SimDoc backend API endpoint

# 3. Run with Docker Compose
docker-compose up -d

# 4. Verify it's running
curl http://localhost:8080/sse
```

### Using Python (Development)

```bash
# 1. Install with uv (recommended)
uv pip install -e .

# 2. Set backend URL
export BACKEND_URL=https://api.simdoc.example.com

# 3. Run the server
python -m simdoc_mcp.server
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | Required | SimDoc backend API endpoint |
| `HOST` | `0.0.0.0` | Server host to bind to |
| `PORT` | `8080` | Server port |
| `LOG_LEVEL` | `INFO` | Logging level |
| `TRANSPORT` | `sse` | MCP transport protocol |

### Claude Desktop Setup

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "simdoc": {
      "url": "http://localhost:8080/sse"
    }
  }
}
```

### Cursor Setup

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "simdoc": {
      "url": "http://localhost:8080/sse"
    }
  }
}
```

## Available MCP Tools

### `resolve-simulator-id`
Find simulators by name with metadata, versions, and trust scores.

### `get-simulator-docs`
Search and retrieve code snippets from simulator documentation.

## Backend API

This MCP server requires a SimDoc-compatible backend API. For access to a hosted backend or to run your own, please see the documentation.

## License

MIT License - see [LICENSE](LICENSE) file for details.
