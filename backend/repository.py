from __future__ import annotations

import json
import sqlite3


def upsert_repository(connection: sqlite3.Connection, url: str) -> int:
    name = url.rstrip('/').split('/')[-1]
    connection.execute(
        'INSERT OR IGNORE INTO repositories(url, name) VALUES (?, ?)',
        (url, name),
    )
    connection.commit()
    row = connection.execute('SELECT id FROM repositories WHERE url = ?', (url,)).fetchone()
    return int(row['id'])


def list_repositories(connection: sqlite3.Connection) -> list[dict]:
    rows = connection.execute('SELECT id, url, name FROM repositories ORDER BY id').fetchall()
    return [dict(row) for row in rows]


def save_snapshot(connection: sqlite3.Connection, repository_id: int, event_type: str, raw_payload: dict) -> None:
    connection.execute(
        'INSERT INTO snapshots(repository_id, event_type, raw_payload) VALUES (?, ?, ?)',
        (repository_id, event_type, json.dumps(raw_payload)),
    )
    connection.commit()


def list_recent_snapshots(connection: sqlite3.Connection, limit: int = 50) -> list[dict]:
    rows = connection.execute(
        '''
        SELECT s.id, r.url AS repository_url, s.event_type, s.raw_payload, s.created_at
        FROM snapshots s
        JOIN repositories r ON r.id = s.repository_id
        ORDER BY s.id DESC
        LIMIT ?
        ''',
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def save_comparison(connection: sqlite3.Connection, query: dict, scorecard: dict, rationale: str) -> None:
    connection.execute(
        'INSERT INTO comparisons(query, scorecard_json, rationale) VALUES (?, ?, ?)',
        (json.dumps(query), json.dumps(scorecard), rationale),
    )
    connection.commit()


def list_recent_comparisons(connection: sqlite3.Connection, limit: int = 25) -> list[dict]:
    rows = connection.execute(
        'SELECT id, query, scorecard_json, rationale, created_at FROM comparisons ORDER BY id DESC LIMIT ?',
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def create_user_if_missing(connection: sqlite3.Connection, email: str) -> int:
    connection.execute('INSERT OR IGNORE INTO users(email) VALUES (?)', (email,))
    connection.commit()
    row = connection.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
    return int(row['id'])


def create_subscription(connection: sqlite3.Connection, user_id: int, repository_id: int, criteria: str) -> None:
    connection.execute(
        'INSERT INTO subscriptions(user_id, repository_id, criteria) VALUES (?, ?, ?)',
        (user_id, repository_id, criteria),
    )
    connection.commit()


def list_subscribers_for_repository(connection: sqlite3.Connection, repository_id: int) -> list[dict]:
    rows = connection.execute(
        '''
        SELECT s.id AS subscription_id, s.user_id, s.repository_id, s.criteria, u.email
        FROM subscriptions s
        JOIN users u ON u.id = s.user_id
        WHERE s.repository_id = ?
        ''',
        (repository_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def log_notification(
    connection: sqlite3.Connection,
    user_id: int,
    repository_id: int,
    message: str,
    provider: str,
) -> None:
    connection.execute(
        'INSERT INTO notification_log(user_id, repository_id, message, provider) VALUES (?, ?, ?, ?)',
        (user_id, repository_id, message, provider),
    )
    connection.commit()
