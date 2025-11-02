"""
Tools for sense management in BabelNet.
"""

from typing import Optional, Dict, Any, List

from ..constants import LANGUAGE_MAP, POS_MAP
from ..http_client import BabelNetHTTPClient


def register_sense_tools(mcp: Any, client: BabelNetHTTPClient) -> None:
    """Register all sense-related tools."""
    
    @mcp.tool()
    def get_senses(
        word: str,
        from_langs: List[str] = ["en"],
        pos: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve all senses of a word.
        Each sense represents a specific usage of the word in a synset.
        
        NOTE: Each request consumes 1 Babelcoin.
        
        Args:
            word: The word to search for
            from_langs: Source languages. Default: ['en']
            pos: Part-of-speech: 'noun', 'verb', 'adjective', 'adverb' (optional)
        
        Returns:
            Dictionary with the word and list of found senses
        """
        poses = [POS_MAP.get(pos.lower())] if pos else None
        synset_ids = client.get_senses(
            lemma=word,
            search_langs=[LANGUAGE_MAP.get(lang.lower(), lang).upper() for lang in from_langs],
            target_langs=None,
            poses=[p for p in poses] if poses else None,
        )        
        return {
            "word": word,
            "from_languages": from_langs,
            "pos": pos,
            "senses": synset_ids
        }
