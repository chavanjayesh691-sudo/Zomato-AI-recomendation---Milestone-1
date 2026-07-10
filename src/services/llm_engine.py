from __future__ import annotations
import importlib
import json
import logging
import os
from typing import Any, Optional

from config.settings import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)


class LlmEngine:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", GROQ_API_KEY)
        self.model = model or os.getenv("GROQ_MODEL", GROQ_MODEL)
        self.client = self._load_client()

    def _load_client(self) -> Any | None:
        try:
            groq = importlib.import_module("groq")
            return groq.Groq(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            return None

    def parse_response(self, raw_content: str) -> dict[str, Any]:
        if not raw_content:
            raise ValueError("Empty response returned from LLM")
        cleaned = raw_content.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        if "{" in cleaned and "}" in cleaned:
            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1
            cleaned = cleaned[start:end]
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON returned from LLM: {raw_content}") from err

    def rank(self, prompt: str) -> dict[str, Any]:
        if self.client is None:
            raise RuntimeError("Groq SDK client is not available or API key is missing")

        logger.info(f"Dispatching prompt to Groq API (model: {self.model})...")
        kwargs = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }
        try:
            response = self.client.chat.completions.create(**kwargs, response_format={"type": "json_object"})
        except Exception:
            response = self.client.chat.completions.create(**kwargs)
        raw_content = response.choices[0].message.content or ""
        logger.info("Successfully received response from Groq API.")
        return self.parse_response(raw_content)

