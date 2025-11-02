"""
Tools for synset management in BabelNet.
"""

from typing import Optional, Dict, Any, List

from ..constants import LANGUAGE_MAP, POS_MAP
from ..http_client import BabelNetHTTPClient


def register_synset_tools(mcp: Any, client: BabelNetHTTPClient) -> None:
    """Register all synset-related tools."""
    
    @mcp.tool()
    def get_synsets(
        word: str,
        from_langs: List[str] = ["en"],
        to_langs: Optional[List[str]] = None,
        pos: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve all synsets (concepts) for a word in one or more languages.
        
        NOTE: Each request consumes 1 Babelcoin (daily limit: 1000).
        
        Args:
            word: The word to search for
            from_langs: Source languages (e.g., ['en', 'it']). Default: ['en']
            to_langs: Target languages for translations (optional)
            pos: Part-of-speech: 'noun', 'verb', 'adjective', 'adverb' (optional)
        
        Returns:
            Dictionary with the searched word and list of found synsets
        """
        poses = [POS_MAP.get(pos.lower())] if pos else None
        synset_ids = client.get_synset_ids(
            lemma=word,
            search_langs=[LANGUAGE_MAP.get(lang.lower(), lang).upper() for lang in from_langs],
            target_langs=[LANGUAGE_MAP.get(lang.lower(), lang).upper() for lang in to_langs] if to_langs else None,
            poses=[p for p in poses] if poses else None,
        )
        results: List[Dict[str, Any]] = []
        synset_ids = client.get_synset_ids(
            lemma=word,
            search_langs=[LANGUAGE_MAP.get(lang.lower(), lang).upper() for lang in from_langs],
            target_langs=[LANGUAGE_MAP.get(lang.lower(), lang).upper() for lang in to_langs] if to_langs else None,
            poses=[p for p in poses] if poses else None,
        )
        
        return {
            "word": word,
            "from_languages": from_langs,
            "to_languages": to_langs,
            "pos": pos,
            "total_synsets": len(synset_ids),
            "synsets": synset_ids,
        }
    
    @mcp.tool()
    def get_synset_by_id(
        synset_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve a specific synset by its BabelNet ID.
        Useful for getting complete details about a specific concept.
        
        NOTE: Each request consumes 1 Babelcoin.
        
        Args:
            synset_id: BabelNet synset ID (e.g., 'bn:00000356n')
        
        Returns:
            Dictionary with detailed synset information
        """
        synset = client.get_synset(synset_id)
        
        
        return synset
