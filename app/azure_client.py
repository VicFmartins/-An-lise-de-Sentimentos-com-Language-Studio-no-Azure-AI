from __future__ import annotations

import os

import httpx

from app.models import OpinionTarget, SentimentResponse


class AzureLanguageClient:
    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT", "").rstrip("/")
        self.key = os.getenv("AZURE_LANGUAGE_KEY")

    @property
    def configured(self) -> bool:
        return bool(self.endpoint and self.key)

    def analyze_sentiment(self, text: str, language: str = "pt", include_opinion_mining: bool = True) -> SentimentResponse:
        if not self.configured:
            raise RuntimeError("Azure AI Language nao configurado.")

        params = {"api-version": "2023-04-01"}
        payload = {
            "kind": "SentimentAnalysis",
            "parameters": {
                "modelVersion": "latest",
                "opinionMining": include_opinion_mining,
            },
            "analysisInput": {
                "documents": [
                    {
                        "id": "1",
                        "language": language,
                        "text": text,
                    }
                ]
            },
        }
        response = httpx.post(
            f"{self.endpoint}/language/:analyze-text",
            params=params,
            headers={
                "Ocp-Apim-Subscription-Key": self.key,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        document = result["results"]["documents"][0]

        opinions: list[OpinionTarget] = []
        for sentence in document.get("sentences", []):
            for mined in sentence.get("opinions", []):
                opinions.append(
                    OpinionTarget(
                        target=mined["target"]["text"],
                        sentiment=mined["target"]["sentiment"].lower(),
                        confidence=max(mined["target"]["confidenceScores"].values()),
                        evidence=sentence["text"],
                    )
                )

        return SentimentResponse(
            provider="azure_ai_language",
            language=language,
            sentiment=document["sentiment"].lower(),
            confidence_scores={k.lower(): round(v, 4) for k, v in document["confidenceScores"].items()},
            opinions=opinions,
            sentences=[
                {
                    "text": sentence["text"],
                    "sentiment": sentence["sentiment"].lower(),
                    "confidence_scores": {k.lower(): round(v, 4) for k, v in sentence["confidenceScores"].items()},
                }
                for sentence in document.get("sentences", [])
            ],
            warning=None,
        )
