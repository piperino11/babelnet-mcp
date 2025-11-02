"""
Tool for getting word definitions/meanings from BabelNet.
"""

import logging
from typing import Optional, Dict, Any, List
from ..http_client import BabelNetHTTPClient
from ..constants import LANGUAGE_MAP, POS_MAP

logger = logging.getLogger("babelnet-mcp")


def register_definition_tool(mcp: Any, client: BabelNetHTTPClient) -> None:
    """Register the definition/meaning tool."""
    
    @mcp.tool()
    def get_definition(
        word: str,
        from_langs: List[str] = ["en"],
        pos: Optional[str] = None,
        max_definitions: int = 20
    ) -> Dict[str, Any]:
        """
        Get definitions (glosses) for a word across all its meanings.
        
        This tool retrieves all synsets for a word and extracts their definitions,
        providing a comprehensive view of the word's various meanings.
        
        NOTE: Each request consumes 1 Babelcoin per synset (daily limit: 1000).
        
        Args:
            word: The word to get definitions for
            from_langs: Source languages to search in (e.g., ['en', 'it']). Default: ['en']
            pos: Part-of-speech filter: 'noun', 'verb', 'adjective', 'adverb' (optional)
            max_definitions: Maximum number of synsets to retrieve (default: 20)
        
        Returns:
            Dictionary containing:
            - word: the searched word
            - total_meanings: number of different meanings found
            - definitions: list of meanings with their glosses
        
        Example:
            >>> get_definition("bank", from_langs=["en"])
            {
                "word": "bank",
                "total_meanings": 3,
                "definitions": [
                    {
                        "synset_id": "bn:00008364n",
                        "pos": "NOUN",
                        "main_sense": "bank",
                        "glosses": [
                            {
                                "language": "EN",
                                "definition": "a financial institution that accepts deposits...",
                                "source": "WORDNET"
                            },
                            ...
                        ]
                    },
                    ...
                ]
            }
        """
        logger.info(f"Getting definitions for word: '{word}' (langs: {from_langs}, pos: {pos})")
        
        # Get synset IDs for the word
        poses = [POS_MAP.get(pos.lower())] if pos else None
        
        try:
            synset_ids = client.get_synset_ids(
                lemma=word,
                search_langs=[LANGUAGE_MAP.get(lang.lower(), lang).upper() for lang in from_langs],
                poses=[p for p in poses if p] if poses else None,
            )
            logger.info(f"Found {len(synset_ids)} synset IDs for '{word}'")
        except Exception as e:
            logger.error(f"Error getting synset IDs for '{word}': {e}")
            raise
        
        # Limit the number of synsets to retrieve
        synset_ids = synset_ids[:max_definitions]
        if len(synset_ids) < max_definitions:
            logger.debug(f"Using all {len(synset_ids)} synsets (requested max: {max_definitions})")
        else:
            logger.debug(f"Limited to {max_definitions} synsets out of {len(synset_ids)}")
        
        definitions: List[Dict[str, Any]] = []
        
        # For each synset, get full details and extract glosses
        for idx, item in enumerate(synset_ids, 1):
            sid = item.get("id")
            if not sid:
                logger.warning(f"Skipping synset without ID at position {idx}")
                continue
                
            try:
                logger.debug(f"Fetching synset {idx}/{len(synset_ids)}: {sid}")
                synset = client.get_synset(sid)
                
                # Extract glosses from synset
                glosses = synset.get("glosses", [])
                
                if not glosses:
                    logger.debug(f"No glosses found for synset {sid}")
                    continue
                
                logger.debug(f"Found {len(glosses)} glosses for synset {sid}")
                
                # Get main sense for this synset
                senses = synset.get("senses", [])
                main_sense = word
                if senses:
                    # Try to find a sense matching the search language
                    for sense in senses:
                        props = sense.get("properties", {})
                        if props.get("language", "").upper() in [lang.upper() for lang in from_langs]:
                            main_sense = props.get("lemma", {}).get("lemma", word)
                            break
                
                # Format glosses
                formatted_glosses = []
                for gloss in glosses:
                    formatted_glosses.append({
                        "language": gloss.get("language", ""),
                        "definition": gloss.get("gloss", ""),
                        "source": gloss.get("source", "")
                    })
                
                definitions.append({
                    "synset_id": sid,
                    "pos": item.get("pos", ""),
                    "main_sense": main_sense,
                    "glosses": formatted_glosses
                })
                
            except Exception as e:
                # Skip synsets that fail to load
                logger.warning(f"Failed to load synset {sid}: {e}")
                continue
        
        logger.info(f"Successfully retrieved {len(definitions)} definitions for '{word}'")
        
        return {
            "word": word,
            "from_languages": from_langs,
            "pos": pos,
            "total_meanings": len(definitions),
            "definitions": definitions
        }