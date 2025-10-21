"""Simplified MCP server using FastMCP with SSE transport."""

import logging
import os
from typing import Any

from mcp.server.fastmcp import FastMCP, Context

from simdoc_mcp import __version__
from simdoc_mcp.client import BackendClient

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP(
    "simdocs",
    instructions="SimDoc provides search capabilities for scientific simulation documentation including PyBaMM, Cantera, and other simulators.",
)

# Configure server to listen on all interfaces
mcp.settings.host = os.getenv("HOST", "0.0.0.0")
mcp.settings.port = int(os.getenv("PORT", "8080"))

# Global backend client
backend_client: BackendClient = None


@mcp.tool()
async def resolve_simulator_id(name: str, ctx: Context) -> str:
    """
    Resolve a simulator name to a structured ID with metadata.

    Returns ranked matches with trust scores, versions, and descriptions.
    Use this before get-simulator-docs to find the correct simulator ID.

    Args:
        name: Simulator name to search for (e.g., 'cantera', 'pybamm')

    Returns:
        JSON string with simulator matches
    """
    global backend_client

    try:
        result = await backend_client.resolve_simulator(name)

        # Format the response
        if not result.get("matches"):
            return f"No simulators found matching '{name}'"

        # Build formatted response
        output = [f"Found {len(result['matches'])} simulator(s) matching '{name}':\n"]

        for sim in result["matches"]:
            output.append(f"\n**{sim['name']}** (ID: `{sim['id']}`)")
            output.append(f"  Description: {sim.get('description', 'N/A')}")
            output.append(f"  Trust Score: {sim.get('trust_score', 'N/A')}/10")
            output.append(f"  Versions: {', '.join(sim.get('versions', ['N/A']))}")
            output.append(f"  Default Version: {sim.get('default_version', 'N/A')}")

        return "\n".join(output)

    except Exception as e:
        logger.error(f"Error resolving simulator '{name}': {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def get_simulator_docs(
    simulator_id: str,
    topic: str = "",
    tokens: int = 5000,
    ctx: Context = None
) -> str:
    """
    Get code snippets and documentation for a specific simulator.

    Returns attributed code examples with source URLs and descriptions.
    You must call resolve-simulator-id first to get the simulator ID.

    Args:
        simulator_id: Simulator ID (e.g., 'cantera/cantera', 'pybamm/PyBaMM')
        topic: Optional topic to focus the search (e.g., 'flame', 'reactor', 'battery')
        tokens: Maximum tokens to return (default: 5000)

    Returns:
        Formatted code snippets with sources
    """
    global backend_client

    try:
        # Determine max_results based on tokens (rough estimate)
        max_results = min(10, max(1, tokens // 500))

        result = await backend_client.search_snippets(
            simulator_id=simulator_id,
            topic=topic if topic else None,
            max_tokens=tokens,
            max_results=max_results,
        )

        # Format the response
        snippets = result.get("snippets", [])
        if not snippets:
            return f"No documentation found for '{simulator_id}'" + (f" with topic '{topic}'" if topic else "")

        output = [
            f"Found {len(snippets)} code example(s) for **{simulator_id}**",
            f"Query: {result.get('query', topic or 'general documentation')}\n"
        ]

        for i, snippet in enumerate(snippets, 1):
            output.append(f"\n## Example {i}: {snippet.get('title', 'Untitled')}")
            output.append(f"**Source:** {snippet.get('source_url', 'N/A')}")
            output.append(f"**Description:** {snippet.get('description', 'N/A')}")
            if snippet.get('summary'):
                output.append(f"**Summary:** {snippet['summary']}")
            output.append(f"**Relevance:** {snippet.get('relevance_score', 0):.2f}")
            output.append(f"\n```{snippet.get('language', 'python')}")
            output.append(snippet.get('code', ''))
            output.append("```")

        output.append(f"\n**Total tokens:** ~{result.get('total_tokens', 0)}")

        return "\n".join(output)

    except Exception as e:
        logger.error(f"Error fetching docs for '{simulator_id}': {e}")
        return f"Error: {str(e)}"


def main():
    """Entry point for the MCP server."""
    global backend_client

    import asyncio

    async def init_backend():
        """Initialize backend connection."""
        global backend_client
        backend_url = os.getenv("BACKEND_URL", "http://host.docker.internal:8000")
        backend_client = BackendClient(base_url=backend_url)
        logger.info(f"SimDoc MCP Server v{__version__} starting...")
        logger.info(f"Backend URL: {backend_url}")

        # Test backend connection
        try:
            health = await backend_client.health_check()
            logger.info(f"Backend connection successful: {health}")
            logger.info(f"Simulators available: {health.get('simulators_available', [])}")
        except Exception as e:
            logger.error(f"Backend connection failed: {e}")
            logger.warning("Server will start but tools may not work until backend is available")

    # Initialize backend client synchronously before starting server
    asyncio.run(init_backend())

    # Get configuration from environment
    transport = os.getenv("TRANSPORT", "sse")  # sse or stdio

    logger.info(f"Starting server with {transport} transport")

    # Run with specified transport
    # FastMCP.run() will start its own event loop
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
