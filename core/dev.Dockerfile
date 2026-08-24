# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Create a working directory for the project
WORKDIR /core

# Keeps Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy the project source code
COPY . /core

# Install the rest of the project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Place executables in the environment at the front of the path
ENV PATH="/core/.venv/bin:$PATH"

# Run the application in development mode
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0"]
