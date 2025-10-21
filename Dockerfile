# Multi-stage build for smaller final image
FROM python:3.11-slim as builder

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files and source code for installation
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install dependencies
RUN uv pip install --system --no-cache -e .

# Final stage
FROM python:3.11-slim

# Install uv for running the app
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy installed packages and binaries from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BACKEND_URL=http://backend:8000
ENV HOST=0.0.0.0
ENV PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8080/sse', timeout=5)" || exit 1

# Run the application using FastMCP
CMD ["python", "-m", "simdoc_mcp.server"]

