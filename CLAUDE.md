# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dev dependencies
uv sync --group dev

# Run the server locally (opens MCP Inspector in browser)
GROUPME_TOKEN=<token> uv run mcp dev src/groupme_mcp/main.py

# Run all tests
uv run --group dev pytest tests/ -v

# Run a single test
uv run --group dev pytest tests/test_client.py::test_list_groups -v

# Lint and format
uv run --group dev pre-commit run --all-files
```

## Architecture

The project is a thin MCP server over the GroupMe API v3. Source lives under `src/groupme_mcp/`, split across three files:

- **`src/groupme_mcp/client.py`** — `GroupMeClient`: async HTTP client wrapping the GroupMe REST API. Reads `GROUPME_TOKEN` from the environment at init. All methods are `async` and use `httpx.AsyncClient` per-request. The `_get`/`_post`/`_delete` helpers inject the token as a query param on every request.

- **`src/groupme_mcp/server.py`** — MCP tool definitions using `FastMCP`. Each `@mcp.tool()` function is a thin shim that delegates directly to `GroupMeClient`. Tools auto-generate `source_guid` (UUID) when the caller omits it, to prevent duplicate sends.

- **`src/groupme_mcp/main.py`** — Entry point; calls `mcp.run(transport="stdio")`.

## Tests

Tests use `pytest-httpx` (`HTTPXMock`) to intercept `httpx` requests without hitting the real API. `asyncio_mode = "auto"` is set in `pyproject.toml`, so `async` test functions run automatically without needing `@pytest.mark.asyncio`. Tests must set `GROUPME_TOKEN` in the environment before importing `client` (see the `os.environ.setdefault` at the top of test files).

## Getting a Token (OAuth)

`oauth/get_token.py` implements the GroupMe implicit OAuth flow using only the stdlib. It starts a local HTTP server, opens the authorize URL in your browser, and prints the token once GroupMe redirects back.

```bash
# Register http://localhost:8080/callback as your app's callback URL at
# https://dev.groupme.com/applications, then:
python oauth/get_token.py --client-id YOUR_CLIENT_ID
# or
GROUPME_CLIENT_ID=YOUR_CLIENT_ID python oauth/get_token.py --port 8080
```

The script prints `export GROUPME_TOKEN=...` once the token is received.

## Adding a New Tool

1. Add the async method to `GroupMeClient` in `src/groupme_mcp/client.py`.
2. Add a corresponding `@mcp.tool()` function in `src/groupme_mcp/server.py` that calls the client method.
3. Add tests in `tests/test_client.py` (HTTP-level) and `tests/test_server.py` (tool-level).
