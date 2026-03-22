from pydantic import BaseModel, Field


class SentimentRequest(BaseModel):
    text: str = Field(min_length=1)
    language: str = Field(default="pt")
    include_opinion_mining: bool = True


class OpinionTarget(BaseModel):
    target: str
    sentiment: str
    confidence: float
    evidence: str


class SentimentResponse(BaseModel):
    provider: str
    language: str
    sentiment: str
    confidence_scores: dict[str, float]
    opinions: list[OpinionTarget]
    sentences: list[dict]
    warning: str | None = None
