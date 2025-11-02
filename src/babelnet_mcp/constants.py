"""
Constants and mappings for BabelNet MCP (HTTP-only).
"""

from typing import Dict


# Language code to uppercase language tag mapping (as expected by HTTP API)
LANGUAGE_MAP: Dict[str, str] = {
    "en": "EN",
    "it": "IT",
    "es": "ES",
    "fr": "FR",
    "de": "DE",
    "pt": "PT",
    "zh": "ZH",
    "ja": "JA",
    "ru": "RU",
    "ar": "AR",
    "nl": "NL",
    "pl": "PL",
    "sv": "SV",
    "tr": "TR",
    "ko": "KO",
}

# POS string to HTTP API POS tag mapping
POS_MAP: Dict[str, str] = {
    "noun": "NOUN",
    "verb": "VERB",
    "adjective": "ADJECTIVE",
    "adverb": "ADVERB",
}

# Relation categories used for client-side filtering of edges
# Based on pointer.relationGroup or pointer.name fields in HTTP response
RELATION_GROUPS: Dict[str, str] = {
    "hypernym": "HYPERNYM",
    "hyponym": "HYPONYM",
    "meronym": "MERONYM",
    "holonym": "HOLONYM",
}

# Supported languages
SUPPORTED_LANGUAGES = list(LANGUAGE_MAP.keys())

# Supported POS tags
SUPPORTED_POS = list(POS_MAP.keys())

# Supported relation types (plus antonym and all)
SUPPORTED_RELATIONS = list(RELATION_GROUPS.keys()) + ["antonym", "all"]
