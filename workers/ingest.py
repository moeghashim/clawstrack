from __future__ import annotations

from dataclasses import asdict, dataclass

from scrapling.fetchers import Fetcher

from backend.config import load_settings
from backend.database import connect, init_db
from backend.repository import save_snapshot, upsert_repository


@dataclass
class RepoEvent:
    repository_url: str
    event_type: str
    payload: dict


def _extract_text(response, selector: str, default_value: str = 'Unknown') -> str:
    value = response.css_first(selector)
    return value if value else default_value


def collect_repo_event(repository_url: str) -> RepoEvent:
    fetcher = Fetcher(auto_match=True)
    response = fetcher.get(repository_url)
    payload = {
        'url': repository_url,
        'status_code': response.status,
        'title': _extract_text(response, 'title::text'),
    }
    return RepoEvent(repository_url=repository_url, event_type='scrape_snapshot', payload=payload)


def collect_release_event(repository_url: str) -> RepoEvent:
    releases_url = repository_url.rstrip('/') + '/releases'
    fetcher = Fetcher(auto_match=True)
    response = fetcher.get(releases_url)

    payload = {
        'url': releases_url,
        'status_code': response.status,
        'page_title': _extract_text(response, 'title::text'),
        'latest_release_label': _extract_text(response, 'h1::text', default_value='No release detected'),
    }
    return RepoEvent(repository_url=repository_url, event_type='release_snapshot', payload=payload)


def run_once() -> list[RepoEvent]:
    settings = load_settings()
    connection = connect(settings.database_url)
    init_db(connection)

    events: list[RepoEvent] = []
    for repo_url in settings.monitored_repos:
        repository_id = upsert_repository(connection, repo_url)
        for collector in (collect_repo_event, collect_release_event):
            try:
                event = collector(repo_url)
            except Exception as exc:
                event = RepoEvent(
                    repository_url=repo_url,
                    event_type='ingest_error',
                    payload={'error': str(exc), 'collector': collector.__name__},
                )
            save_snapshot(connection, repository_id, event.event_type, asdict(event))
            events.append(event)
    return events


if __name__ == '__main__':
    ingested = run_once()
    print(f'ingested_events={len(ingested)}')
