from __future__ import annotations

import os
from pathlib import Path

from backend.config import load_settings
from backend.database import connect, init_db
from backend.repository import (
    create_subscription,
    create_user_if_missing,
    list_recent_comparisons,
    list_recent_snapshots,
    list_subscribers_for_repository,
    save_comparison,
    save_snapshot,
    upsert_repository,
)


def test_load_settings_reads_dotenv(tmp_path: Path) -> None:
    original_cwd = Path.cwd()
    os.chdir(tmp_path)
    try:
        (tmp_path / '.env').write_text(
            'MONITORED_REPOS=https://github.com/a/b,https://github.com/c/d\n'
            'DATABASE_URL=sqlite:///./custom.db\n'
            'NOTIFICATION_PROVIDER=console\n'
        )
        os.environ.pop('MONITORED_REPOS', None)
        os.environ.pop('DATABASE_URL', None)
        os.environ.pop('NOTIFICATION_PROVIDER', None)

        settings = load_settings()

        assert settings.monitored_repos == ['https://github.com/a/b', 'https://github.com/c/d']
        assert settings.database_url == 'sqlite:///./custom.db'
    finally:
        os.chdir(original_cwd)


def test_recent_history_queries_return_saved_data(tmp_path: Path) -> None:
    connection = connect(f"sqlite:///{tmp_path / 'test.db'}")
    init_db(connection)
    repository_id = upsert_repository(connection, 'https://github.com/example/project')

    save_snapshot(connection, repository_id, 'release_snapshot', {'v': '1.0.0'})
    save_comparison(
        connection,
        {'repositories': ['https://github.com/example/project', 'https://github.com/example/other']},
        {'scores': [{'repository': 'https://github.com/example/project', 'score': 99}]},
        'High feature velocity',
    )

    snapshots = list_recent_snapshots(connection, limit=5)
    comparisons = list_recent_comparisons(connection, limit=5)

    assert snapshots
    assert snapshots[0]['event_type'] == 'release_snapshot'
    assert comparisons
    assert comparisons[0]['rationale'] == 'High feature velocity'


def test_list_subscribers_for_repository_includes_email(tmp_path: Path) -> None:
    connection = connect(f"sqlite:///{tmp_path / 'subs.db'}")
    init_db(connection)
    repository_id = upsert_repository(connection, 'https://github.com/example/project')
    user_id = create_user_if_missing(connection, 'user@example.com')
    create_subscription(connection, user_id, repository_id, 'security')

    subscribers = list_subscribers_for_repository(connection, repository_id)

    assert len(subscribers) == 1
    assert subscribers[0]['email'] == 'user@example.com'
