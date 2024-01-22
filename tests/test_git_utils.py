"""Test git_utils."""
from __future__ import annotations

from typing import Dict, List, Tuple, TypeVar

from git import Repo
from pytest import MonkeyPatch, mark

from semvergit.git_utils import (
    drywrap,
    get_active_branch,
    get_repo,
    get_tags_with_prefix,
    new_commit,
    pull_remote,
    push_remote,
    set_tag,
)

T = TypeVar("T")


def test_drywrap() -> None:
    """Test drywrap."""

    @drywrap
    def dry_tester(*args: Tuple, **kwargs: Dict) -> Tuple[Tuple, Dict]:
        """Dry tester."""
        return args, kwargs

    assert dry_tester("test", dry_run=True) is None
    assert dry_tester("test") == (("test",), {})
    assert dry_tester("test", dry_run=False) == (("test",), {})


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
    "test_tags, prefix, expected",
    [
        ([], "v", []),
        (["v0.0.1"], "v", ["v0.0.1"]),
        (["v0.0.1", "v0.0.2"], "v", ["v0.0.1", "v0.0.2"]),
        (["0.0.1"], "", ["0.0.1"]),
        (["0.0.1", "0.0.2"], "", ["0.0.1", "0.0.2"]),
        (["v0.0.1", "new123", "new_version"], "v", ["v0.0.1"]),
        (["v0.0.1", "dev123", "dev_version"], "dev", ["dev123", "dev_version"]),
    ],
)
def test_get_tags_with_prefix(test_tags: List[str], prefix: str, expected: List[str]) -> None:
    """Test get_tags_with_prefix."""

    test_repo = Repo()

    class TagMock:  # pylint: disable=too-few-public-methods
        """Tag mock."""

        def __init__(self, name: str) -> None:
            """Init."""
            self.name = name

    mock_tags = [TagMock(tag) for tag in test_tags]
    MonkeyPatch().setattr("semvergit.git_utils.Repo.tags", mock_tags)
    fetched_tags = get_tags_with_prefix(test_repo, prefix)
    if fetched_tags:
        for tag in fetched_tags:
            assert tag in expected
    else:
        assert fetched_tags == expected


def test_new_commit() -> None:
    """Test new_commit."""

    class MockCommit:  # pylint: disable=too-few-public-methods
        """Mock commit."""

        @property
        def hexsha(self) -> str:
            """Hexsha."""
            return "112233"

    class MockIndex:  # pylint: disable=too-few-public-methods
        """Mock index."""

        @staticmethod
        def commit(message: str) -> MockCommit:  # pylint: disable=unused-argument
            """Commit."""
            return MockCommit()

    test_repo = Repo()

    MonkeyPatch().setattr("semvergit.git_utils.Repo.index", MockIndex)
    result = new_commit(test_repo, "testmessage")
    assert result == "112233"


def test_set_tag() -> None:
    """Test set_tag."""

    def mock_create_tag(repo: Repo, tag: str) -> str:  # pylint: disable=unused-argument
        """Mock create_tag."""
        return tag

    test_repo = Repo()

    MonkeyPatch().setattr("semvergit.git_utils.Repo.create_tag", mock_create_tag)
    result = set_tag(test_repo, "testtag")
    assert result == "testtag"


def test_push_remote() -> None:
    """Test push_remote."""

    class RemoteMock:
        """Remote mock."""

        def __init__(self: T, name: str) -> None:
            """Init."""
            self.name = name

        def push(self: T, tag_str: str) -> None:  # pylint: disable=unused-argument
            """Push."""
            pass  # pylint: disable=unnecessary-pass

        @property
        def origin(self: T) -> T:
            """Origin."""
            return self

    test_repo = Repo()
    MonkeyPatch().setattr("semvergit.git_utils.Repo.remotes", RemoteMock("testrepo"))
    push_remote(test_repo, "testtag")
