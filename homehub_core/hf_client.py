from __future__ import annotations

import os
from typing import Any

import httpx


class HuggingFaceClient:
    """Small inference wrapper with local fallback for offline dev."""

    def __init__(self) -> None:
        self.api_key = os.getenv("HF_API_KEY", "")
        self.base_url = os.getenv("HF_INFERENCE_URL", "https://api-inference.huggingface.co/models")
        self.default_model = os.getenv("HF_DEFAULT_MODEL", "google/flan-t5-base")

    async def infer(self, prompt: str, model: str | None = None) -> dict[str, Any]:
        if not self.api_key:
            return {
                "mode": "mock",
                "model": model or self.default_model,
                "output": f"[mocked inference] {prompt[:180]}",
            }

        endpoint = f"{self.base_url}/{model or self.default_model}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": prompt, "options": {"wait_for_model": True}}

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        return {"mode": "live", "model": model or self.default_model, "output": data}
