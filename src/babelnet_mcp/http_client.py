"""
Minimal HTTP client for BabelNet REST API.
"""

from typing import Any, Dict, List, Optional
import requests

BASE_URL = "https://babelnet.io/v9"



class BabelNetHTTPClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Accept-Encoding": "gzip"})

    def _get(self, path: str, params: Dict[str, Any]) -> Any:
        params = dict(params)
        params["key"] = self.api_key
        url = f"{BASE_URL}/{path}"
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_version(self) -> Dict[str, Any]:
        return self._get("getVersion", {})

    def get_synset_ids(
        self,
        lemma: str,
        search_langs: List[str],
        target_langs: Optional[List[str]] = None,
        poses: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"lemma": lemma}
        for lang in search_langs:
            params.setdefault("searchLang", [])
            params["searchLang"].append(lang.upper())
        if target_langs:
            for lang in target_langs:
                params.setdefault("targetLang", [])
                params["targetLang"].append(lang.upper())
        if poses:
            for pos in poses:
                params.setdefault("pos", [])
                params["pos"].append(pos.upper())
        return self._get("getSynsetIds", params)

    def get_synset(self, synset_id: str) -> Dict[str, Any]:
        # API returns a single synset JSON object
        return self._get("getSynset", {"id": synset_id})


    def get_senses(
        self,
        lemma: str,
        search_langs: List[str],
        target_langs: Optional[List[str]] = None,
        poses: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"lemma": lemma}
        for lang in search_langs:
            params.setdefault("searchLang", [])
            params["searchLang"].append(lang.upper())
        if target_langs:
            for lang in target_langs:
                params.setdefault("targetLang", [])
                params["targetLang"].append(lang.upper())
        if poses:
            for pos in poses:
                params.setdefault("pos", [])
                params["pos"].append(pos.upper())
        return self._get("getSenses", params)


    def get_outgoing_edges(self, synset_id: str, pointer: Optional[str] = None) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"id": synset_id}
        if pointer:
            params["pointer"] = pointer
        return self._get("getOutgoingEdges", params)


