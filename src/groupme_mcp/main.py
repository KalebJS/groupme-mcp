import os
import sys


def main() -> None:
    if "GROUPME_TOKEN" not in os.environ:
        print("Error: GROUPME_TOKEN is not set.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Get a token at https://dev.groupme.com/applications", file=sys.stderr)
        print("Then run:  GROUPME_TOKEN=<token> groupme-mcp", file=sys.stderr)
        sys.exit(1)

    from groupme_mcp.server import mcp

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
