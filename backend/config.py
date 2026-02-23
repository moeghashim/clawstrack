from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv_if_present() -> None:
    env_file = Path('.env')
    if not env_file.exists():
        return

    for raw_line in env_file.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass(frozen=True)
class Settings:
    monitored_repos: list[str]
    openai_api_key: str | None
    database_url: str
    notification_provider: str


def _parse_repos(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []
    return [repo.strip() for repo in raw_value.split(',') if repo.strip()]


def load_settings() -> Settings:
    _load_dotenv_if_present()
    monitored_repos = _parse_repos(os.getenv('MONITORED_REPOS'))
    database_url = os.getenv('DATABASE_URL', 'sqlite:///./clawstrack.db')
    notification_provider = os.getenv('NOTIFICATION_PROVIDER', 'console')
    return Settings(
        monitored_repos=monitored_repos,
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        database_url=database_url,
        notification_provider=notification_provider,
    )
