from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from backend.analysis import compare_projects
from backend.config import load_settings
from backend.database import connect, init_db
from backend.models import CompareRequest, CompareResponse, SignupRequest, SubscriptionRequest
from backend.notifications import dispatch_notification
from backend.repository import (
    create_subscription,
    create_user_if_missing,
    list_recent_comparisons,
    list_recent_snapshots,
    list_repositories,
    list_subscribers_for_repository,
    log_notification,
    save_comparison,
    upsert_repository,
)
from workers.ingest import run_once

app = FastAPI(title='ClawsTrack', version='0.3.0')
settings = load_settings()
connection = connect(settings.database_url)
init_db(connection)

for repo in settings.monitored_repos:
    upsert_repository(connection, repo)


@app.get('/')
def index() -> FileResponse:
    index_file = Path('frontend/index.html')
    return FileResponse(index_file)


@app.get('/api/health')
def health() -> dict:
    return {
        'status': 'ok',
        'monitored_repositories': settings.monitored_repos,
        'notification_provider': settings.notification_provider,
    }


@app.post('/api/ingest')
def ingest_now() -> dict:
    events = run_once()
    return {'ingested_events': len(events)}


@app.get('/api/repositories')
def repositories() -> list[dict]:
    return list_repositories(connection)


@app.get('/api/snapshots')
def snapshots(limit: int = 20) -> list[dict]:
    return list_recent_snapshots(connection, limit=limit)


@app.get('/api/comparisons')
def comparisons(limit: int = 20) -> list[dict]:
    return list_recent_comparisons(connection, limit=limit)


@app.post('/api/compare', response_model=CompareResponse)
def compare(request: CompareRequest) -> CompareResponse:
    result = compare_projects(
        repositories=request.repositories,
        criteria=request.criteria,
        level=request.level,
        openai_api_key=settings.openai_api_key,
    )
    rationale = f"Comparison generated at level '{request.level}' for {len(request.repositories)} repositories."
    save_comparison(connection, request.model_dump(), result.model_dump(), rationale)
    return result


@app.post('/api/signup')
def signup(request: SignupRequest) -> dict:
    user_id = create_user_if_missing(connection, request.email)
    return {'user_id': user_id, 'email': request.email}


@app.post('/api/subscribe')
def subscribe(request: SubscriptionRequest) -> dict:
    repositories_by_url = {item['url']: item for item in list_repositories(connection)}
    if request.repository_url not in repositories_by_url:
        raise HTTPException(status_code=404, detail='Repository is not monitored by admin configuration')

    user_id = create_user_if_missing(connection, request.email)
    repository_id = repositories_by_url[request.repository_url]['id']
    create_subscription(connection, user_id, repository_id, request.criteria)

    return {
        'status': 'subscribed',
        'email': request.email,
        'repository': request.repository_url,
        'criteria': request.criteria,
    }


@app.post('/api/notify/{repository_id}')
def notify_subscribers(repository_id: int, message: str) -> dict:
    subscriptions = list_subscribers_for_repository(connection, repository_id)
    sent_count = 0
    for subscription in subscriptions:
        dispatch_notification(settings.notification_provider, subscription['email'], message)
        log_notification(connection, subscription['user_id'], repository_id, message, settings.notification_provider)
        sent_count += 1

    return {'repository_id': repository_id, 'sent': sent_count}
