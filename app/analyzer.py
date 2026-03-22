from __future__ import annotations

import re

from app.lexicon import ASPECT_KEYWORDS, NEGATIONS, NEGATIVE_WORDS, POSITIVE_WORDS
from app.models import OpinionTarget, SentimentResponse


WORD_RE = re.compile(r"[a-zA-ZÀ-ÿ0-9_]+")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD_RE.finditer(text)]


def split_sentences(text: str) -> list[str]:
    parts = [part.strip() for part in SENTENCE_SPLIT_RE.split(text) if part.strip()]
    return parts or [text.strip()]


def score_tokens(tokens: list[str]) -> tuple[int, int, int]:
    positive = 0
    negative = 0

    for index, token in enumerate(tokens):
        previous = tokens[index - 1] if index > 0 else None
        negated = previous in NEGATIONS
        if token in POSITIVE_WORDS:
            if negated:
                negative += 1
            else:
                positive += 1
        if token in NEGATIVE_WORDS:
            if negated:
                positive += 1
            else:
                negative += 1

    neutral = max(len(tokens) - positive - negative, 0)
    return positive, negative, neutral


def sentiment_from_scores(positive: int, negative: int) -> str:
    if positive > negative:
        return "positive"
    if negative > positive:
        return "negative"
    return "neutral"


def confidence_scores(positive: int, negative: int, neutral: int) -> dict[str, float]:
    total = max(positive + negative + neutral, 1)
    return {
        "positive": round(positive / total, 4),
        "negative": round(negative / total, 4),
        "neutral": round(neutral / total, 4),
    }


def extract_opinions(sentence: str, include_opinion_mining: bool = True) -> list[OpinionTarget]:
    if not include_opinion_mining:
        return []

    lowered = sentence.lower()
    tokens = tokenize(sentence)
    positive, negative, neutral = score_tokens(tokens)
    scores = confidence_scores(positive, negative, neutral)
    sentiment = sentiment_from_scores(positive, negative)
    confidence = scores[sentiment]

    opinions: list[OpinionTarget] = []
    for target, aliases in ASPECT_KEYWORDS.items():
        if any(alias in lowered for alias in aliases):
            opinions.append(
                OpinionTarget(
                    target=target,
                    sentiment=sentiment,
                    confidence=confidence,
                    evidence=sentence[:160],
                )
            )
    return opinions


def analyze_text_locally(text: str, language: str = "pt", include_opinion_mining: bool = True) -> SentimentResponse:
    sentences = split_sentences(text)
    sentence_results: list[dict] = []
    all_opinions: list[OpinionTarget] = []
    total_positive = total_negative = total_neutral = 0

    for sentence in sentences:
        tokens = tokenize(sentence)
        positive, negative, neutral = score_tokens(tokens)
        total_positive += positive
        total_negative += negative
        total_neutral += neutral
        sentiment = sentiment_from_scores(positive, negative)
        scores = confidence_scores(positive, negative, neutral)
        sentence_results.append(
            {
                "text": sentence,
                "sentiment": sentiment,
                "confidence_scores": scores,
            }
        )
        all_opinions.extend(extract_opinions(sentence, include_opinion_mining=include_opinion_mining))

    overall_sentiment = sentiment_from_scores(total_positive, total_negative)
    overall_scores = confidence_scores(total_positive, total_negative, total_neutral)
    return SentimentResponse(
        provider="local_heuristic",
        language=language,
        sentiment=overall_sentiment,
        confidence_scores=overall_scores,
        opinions=all_opinions,
        sentences=sentence_results,
        warning="Resultado gerado localmente para demonstracao. Para producao, compare com Azure AI Language.",
    )
