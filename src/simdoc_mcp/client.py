"""HTTP client for communicating with the backend REST API."""

import logging
import os
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)


class BackendClient:
    """Client for the SimDoc backend REST API."""
    
    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        """Initialize the backend client.
        
        Args:
            base_url: Backend API base URL (defaults to BACKEND_URL env var)
            timeout: Request timeout in seconds
        """
        self.base_url = (base_url or os.getenv("BACKEND_URL", "http://localhost:8000")).rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )
        logger.info(f"Backend client initialized with base_url={self.base_url}")
    
    async def health_check(self) -> dict[str, Any]:
        """Check backend health status.
        
        Returns:
            Health status response
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        try:
            response = await self.client.get("/api/v1/health")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Health check failed: {e}")
            raise
    
    async def resolve_simulator(self, name: str) -> dict[str, Any]:
        """Resolve a simulator name to structured IDs.
        
        Args:
            name: Simulator name to search for
            
        Returns:
            Response with matched simulators
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        try:
            response = await self.client.post(
                "/api/v1/resolve",
                json={"name": name},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Resolve request failed for '{name}': {e}")
            raise
    
    async def search_snippets(
        self,
        simulator_id: str,
        topic: Optional[str] = None,
        max_tokens: int = 5000,
        max_results: int = 10,
    ) -> dict[str, Any]:
        """Search for code snippets in simulator documentation.
        
        Args:
            simulator_id: Simulator ID (e.g., '/cantera/cantera')
            topic: Optional topic to focus the search
            max_tokens: Maximum tokens to return
            max_results: Maximum number of snippets
            
        Returns:
            Response with code snippets
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        try:
            payload = {
                "simulator_id": simulator_id,
                "max_tokens": max_tokens,
                "max_results": max_results,
            }
            if topic:
                payload["topic"] = topic
            
            response = await self.client.post(
                "/api/v1/search",
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Search request failed for '{simulator_id}': {e}")
            raise
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

