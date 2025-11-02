import argparse
import logging
import sys
from typing import Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: mcp package not installed. Run: pip install mcp")
    sys.exit(1)

from .config import config
from .http_client import BabelNetHTTPClient
from .tools import (
    register_definition_tool,
    register_synset_tools,
    register_sense_tools
)
from .constants import LANGUAGE_MAP, POS_MAP


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("babelnet-mcp")

# Initialize FastMCP server
mcp = FastMCP("BabelNet")


def check_configuration() -> bool:
    """Check if BabelNet is properly configured."""
    if not config.is_configured():
        logger.warning(
            "BabelNet is not configured via babelnet_conf.yml. "
            "You can also pass the API key via --api-key."
        )
    return config.is_configured()


def register_all_tools(client: BabelNetHTTPClient) -> None:
    """Register all MCP tools."""
    logger.info("Registering BabelNet MCP tools...")
    register_definition_tool(mcp, client)
    register_synset_tools(mcp, client)
    register_sense_tools(mcp, client)
    logger.info("All tools registered successfully")


def main() -> None:
    """Main entry point for the BabelNet MCP server."""

    # --- Parse CLI arguments ---
    parser = argparse.ArgumentParser(description="BabelNet MCP Server")
    parser.add_argument(
        "--api-key",
        type=str,
        help="BabelNet RESTful API key (used instead of config file)",
        required=False
    )
    args = parser.parse_args()

    logger.info("🚀 Starting BabelNet MCP Server...")
    logger.info("⚠️  NOTE: Each query consumes 1 Babelcoin (limit: 1000/day)")

    # --- Determine which API key to use ---
    api_key = args.api_key or config.api_key
    if not api_key:
        logger.error(
            "Missing BabelNet API key. Pass via --api-key or set RESTFUL_KEY in babelnet_conf.yml"
        )
        sys.exit(1)

    # --- Validate API key by calling getVersion ---
    try:
        client = BabelNetHTTPClient(api_key)

        response = client.get_synset_ids("babelnet",[LANGUAGE_MAP.get("en", "en").upper()])
        if isinstance(response, list):
            logger.info(f"✅ BabelNet API key validated successfully")
            logger.info(f"   Test query returned {len(response)} synset(s)")

    except Exception as e:
        logger.error(f"❌ Failed to validate BabelNet API key or reach API: {e}")
        sys.exit(1)

    # --- Register MCP tools ---
    try:
        register_all_tools(client)
    except Exception as e:
        logger.error(f"Error registering tools: {e}")
        sys.exit(1)

    # --- Run server ---
    logger.info("✅ Server ready - waiting for connections...")
    mcp.run()


if __name__ == "__main__":
    main()
