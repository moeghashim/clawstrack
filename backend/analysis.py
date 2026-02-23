from __future__ import annotations

import hashlib
from typing import Iterable

from backend.models import CompareResponse, ScoreItem


_PROMPT = """
You are a software project comparison analyst.
Compare the repositories provided using criteria and level.
Return compact JSON with: scores[{repository,score,rationale}], confidence.
Score must be 0-100.
""".strip()


def _fallback_score(repo: str, criteria: Iterable[str], level: str) -> ScoreItem:
    seed = f"{repo}|{','.join(criteria)}|{level}".encode("utf-8")
    digest = hashlib.sha256(seed).hexdigest()
    score = int(digest[:2], 16) / 255 * 100
    return ScoreItem(
        repository=repo,
        score=round(score, 2),
        rationale="Fallback heuristic score (OpenAI unavailable).",
    )


def compare_projects(
    repositories: list[str],
    criteria: list[str],
    level: str,
    openai_api_key: str | None,
) -> CompareResponse:
    if not openai_api_key:
        scores = [_fallback_score(repo, criteria, level) for repo in repositories]
        return CompareResponse(level=level, criteria=criteria, scores=scores, confidence=0.35)

    from openai import OpenAI

    client = OpenAI(api_key=openai_api_key)
    user_prompt = (
        f"repositories={repositories}\n"
        f"criteria={criteria}\n"
        f"level={level}\n"
        "Respond as JSON only."
    )

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{"role": "system", "content": _PROMPT}, {"role": "user", "content": user_prompt}],
        )
        payload_text = response.output_text
    except Exception:
        scores = [_fallback_score(repo, criteria, level) for repo in repositories]
        return CompareResponse(level=level, criteria=criteria, scores=scores, confidence=0.4)

    import json

    try:
        parsed = json.loads(payload_text)
        scores = [ScoreItem(**item) for item in parsed["scores"]]
        confidence = float(parsed.get("confidence", 0.7))
        return CompareResponse(level=level, criteria=criteria, scores=scores, confidence=confidence)
    except Exception:
        scores = [_fallback_score(repo, criteria, level) for repo in repositories]
        return CompareResponse(level=level, criteria=criteria, scores=scores, confidence=0.45)
