# groupme-mcp

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that wraps the [GroupMe API v3](https://dev.groupme.com/docs/v3), letting AI assistants read and send GroupMe messages, manage groups, interact with bots, and more.

## Tools

| Category | Tools |
|---|---|
| **Groups** | `list_groups`, `list_former_groups`, `get_group`, `create_group`, `update_group`, `destroy_group`, `join_group`, `rejoin_group` |
| **Members** | `add_members`, `get_member_results`, `remove_member`, `update_membership` |
| **Messages** | `list_messages`, `send_message` |
| **Direct Messages** | `list_direct_messages`, `send_direct_message` |
| **Chats** | `list_chats` |
| **Likes** | `like_message`, `unlike_message` |
| **Bots** | `create_bot`, `post_as_bot`, `list_bots`, `destroy_bot` |
| **Users** | `get_me`, `update_user` |
| **Blocks** | `list_blocks`, `check_block`, `create_block`, `delete_block` |

## Requirements

- Python 3.12+
- A GroupMe access token — get one at [dev.groupme.com](https://dev.groupme.com) or use the [OAuth helper](#getting-a-token)

## Usage

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "groupme": {
      "command": "uvx",
      "args": ["groupme-mcp"],
      "env": {
        "GROUPME_TOKEN": "<your-token>"
      }
    }
  }
}
```

> Until published to PyPI, use `uv run` with `--directory` pointing to a local clone instead of `uvx`.

### Local development

```bash
git clone https://github.com/KalebJS/groupme-mcp
cd groupme-mcp
export GROUPME_TOKEN=<your-token>
uv run mcp dev main.py   # opens MCP Inspector in browser
```

## Getting a Token

`oauth/get_token.py` runs a local OAuth flow using only the Python stdlib — no extra dependencies.

1. Create an application at [dev.groupme.com/applications](https://dev.groupme.com/applications).
2. Set the callback URL to `http://localhost:8080/callback`.
3. Run the helper:

```bash
python oauth/get_token.py --client-id YOUR_CLIENT_ID
```

The script opens your browser, waits for the GroupMe redirect, and prints the token along with the `export` command to set it.

## Development

```bash
# Install dev dependencies
uv sync --group dev

# Install pre-commit hooks
uv run --group dev pre-commit install

# Run tests
uv run --group dev pytest tests/ -v

# Lint
uv run --group dev pre-commit run --all-files
```

## License

MIT
