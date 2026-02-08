# Build stage
FROM python:rc-slim AS builder
SHELL ["/bin/bash", "-c"]
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
# Sync dependencies without installing the project itself yet
RUN uv sync --frozen --no-dev --no-install-project

# Final stage
FROM python:rc-slim
WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY app ./app

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
