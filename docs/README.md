# GroupMe MCP Documentation

This is the documentation for [GroupMe MCP](https://github.com/kalebjs/groupme-mcp), an MCP server that wraps the GroupMe API v3.

## Development

To preview the documentation locally:

1. Install the Mintlify CLI:

   ```bash
   npm i -g mint
   ```

2. Navigate to the `docs` directory and run:

   ```bash
   mint dev
   ```

3. Open http://localhost:3000 to view your changes.

## Editing

- Pages are MDX files with YAML frontmatter
- Configuration lives in `docs.json`
- Use [Mintlify components](https://mintlify.com/docs/component) for rich content
- Keep sentences concise — one idea per sentence
- Use sentence case for headings

## Troubleshooting

- Run `mint broken-links` to check for broken links
- Run `mint update` to ensure you have the latest CLI version
