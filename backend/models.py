from __future__ import annotations

from pydantic import BaseModel, Field


class Repository(BaseModel):
    id: int
    url: str
    name: str


class SnapshotCreate(BaseModel):
    repository_id: int
    event_type: str
    raw_payload: str


class CompareRequest(BaseModel):
    repositories: list[str] = Field(min_length=2)
    level: str = Field(default="summary")
    criteria: list[str] = Field(default_factory=lambda: ["features", "security", "use_case"])


class ScoreItem(BaseModel):
    repository: str
    score: float
    rationale: str


class CompareResponse(BaseModel):
    level: str
    criteria: list[str]
    scores: list[ScoreItem]
    confidence: float


class SignupRequest(BaseModel):
    email: str


class SubscriptionRequest(BaseModel):
    email: str
    repository_url: str
    criteria: str = "all"
