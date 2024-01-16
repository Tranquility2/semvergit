"""Pytest configuration."""
from typing import Generator, List

import pytest
from git import Repo
from loguru import logger
from pytest import LogCaptureFixture, MonkeyPatch


@pytest.fixture(autouse=True)
def caplog(caplog: LogCaptureFixture) -> Generator:  # pylint: disable=redefined-outer-name
    """
    Make pytest work with loguru. See:
    https://loguru.readthedocs.io/en/stable/resources/migration.html#making-things-work-with-pytest-and-caplog
    """
    handler_id = logger.add(caplog.handler, format="{message}")
    yield caplog
    logger.remove(handler_id)


@pytest.fixture(autouse=True)
def mock_get_repo(monkeypatch: MonkeyPatch) -> None:
    """Mock get_repo."""

    def get_repo() -> str:
        return "test_repo"

    monkeypatch.setattr("semvergit.app.get_repo", get_repo)


@pytest.fixture(autouse=True)
def mock_get_active_branch(monkeypatch: MonkeyPatch) -> None:
    """Mock get_active_branch."""

    class MockBranch:  # pylint: disable=too-few-public-methods
        """MockBranch."""

        @property
        def name(self) -> str:
            """Name."""
            return "test_branch"

    def get_active_branch(repo: Repo) -> MockBranch:  # pylint: disable=unused-argument
        return MockBranch()

    monkeypatch.setattr("semvergit.app.get_active_branch", get_active_branch)


@pytest.fixture(autouse=True)
def mock_get_tags_with_prefix(monkeypatch: MonkeyPatch) -> None:
    """Mock get_tags_with_prefix."""

    def get_tags_with_prefix(repo: Repo, prefix: str) -> List[str]:  # pylint: disable=unused-argument
        return ["v0.0.1", "v0.0.2", "v0.0.3", "0.0.4"]

    monkeypatch.setattr("semvergit.app.get_tags_with_prefix", get_tags_with_prefix)


@pytest.fixture(autouse=True)
def mock_pull_remote(monkeypatch: MonkeyPatch) -> None:
    """Mock pull_remote."""

    def pull_remote(repo: Repo) -> None:  # pylint: disable=unused-argument
        pass

    monkeypatch.setattr("semvergit.app.pull_remote", pull_remote)


@pytest.fixture(autouse=True)
def mock_set_tag(monkeypatch: MonkeyPatch) -> None:
    """Mock set_tag."""

    def set_tag(repo: Repo, tag: str) -> str:  # pylint: disable=unused-argument
        return f"mock-set-tag-{tag}"

    monkeypatch.setattr("semvergit.app.set_tag", set_tag)
