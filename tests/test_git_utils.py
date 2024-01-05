"""Test git_utils."""
from __future__ import annotations

from typing import List, TypeVar

from git import Repo
from pytest import MonkeyPatch, mark

from semvergit.git_utils import get_active_branch, get_repo, get_tags, pull_remote

T = TypeVar("T")


def test_get_repo() -> None:
    """Test get_repo."""
    MonkeyPatch().setattr("semvergit.git_utils.Repo.working_tree_dir", "/test")
    assert get_repo().working_tree_dir == "/test"
    assert isinstance(get_repo(), Repo)


def test_get_active_branch() -> None:
    """Test get_active_branch."""

    test_repo = Repo()

    class HeadMock:  # pylint: disable=too-few-public-methods
        """Head mock."""

        def __init__(self, reference: str) -> None:
            """Init."""
            self.reference = reference

        @property
        def name(self) -> str:
            """Name."""
            return self.reference

    MonkeyPatch().setattr("semvergit.git_utils.Repo.active_branch", HeadMock("thisisatest"))
    branch = get_active_branch(test_repo)
    assert branch.name == "thisisatest"


def test_pull_remote() -> None:
    """Test pull_remote."""

    class RemoteMock:
        """Remote mock."""

        def __init__(self: T, name: str) -> None:
            """Init."""
            self.name = name

        def pull(self: T) -> None:
            """Pull."""
            pass  # pylint: disable=unnecessary-pass

        @property
        def origin(self: T) -> T:
            """Origin."""
            return self

    test_repo = Repo()
    MonkeyPatch().setattr("semvergit.git_utils.Repo.remotes", RemoteMock("testrepo"))
    pull_remote(test_repo)


@mark.parametrize(
    "test_tags",
    [
        ([]),
        (["v0.0.1"]),
        (["v0.0.1", "v0.0.2"]),
    ],
)
def test_get_tags(test_tags: List[str]) -> None:
    """Test get_tags."""

    test_repo = Repo()

    class TagMock:  # pylint: disable=too-few-public-methods
        """Tag mock."""

        def __init__(self, name: str) -> None:
            """Init."""
            self.name = name

    mock_tags = [TagMock(tag) for tag in test_tags]
    MonkeyPatch().setattr("semvergit.git_utils.Repo.tags", mock_tags)
    fetched_tags = get_tags(test_repo)
    if fetched_tags:
        for tag in fetched_tags:
            assert tag.name in test_tags
    else:
        assert fetched_tags == test_tags
