"""
BabelNet MCP Tools

This module contains all MCP tools for interacting with BabelNet.
"""

from .definition import register_definition_tool
from .synset import register_synset_tools
from .sense import register_sense_tools

__all__ = [
    "register_definition_tool",
    "register_synset_tools",
    "register_sense_tools"
]
