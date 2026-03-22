from fastapi import FastAPI

from app.analyzer import analyze_text_locally
from app.azure_client import AzureLanguageClient
from app.models import SentimentRequest, SentimentResponse


app = FastAPI(
    title="Sentiment Analysis Demo with Azure AI Language",
    version="1.0.0",
    description="API de analise de sentimentos com modo local explicavel e integracao opcional com Azure AI Language.",
)

azure_client = AzureLanguageClient()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "language-studio-sentimentos"}


@app.post("/api/sentiment/analyze", response_model=SentimentResponse)
def analyze_sentiment(payload: SentimentRequest) -> SentimentResponse:
    if azure_client.configured:
        return azure_client.analyze_sentiment(
            text=payload.text,
            language=payload.language,
            include_opinion_mining=payload.include_opinion_mining,
        )
    return analyze_text_locally(
        text=payload.text,
        language=payload.language,
        include_opinion_mining=payload.include_opinion_mining,
    )
