"""Test app."""

from typing import Callable, Optional

from pytest import CaptureFixture, LogCaptureFixture, mark
from semver import VersionInfo

from semvergit.app import BumpType, SemverGit


@mark.parametrize(
    "pull_branch, expected",
    [
        (
            False,
            [
                VersionInfo(0, 0, 1),
                VersionInfo(0, 0, 2),
                VersionInfo(0, 0, 3),
                VersionInfo(0, 0, 4),
            ],
        ),
        (
            True,
            [
                VersionInfo(0, 0, 1),
                VersionInfo(0, 0, 2),
                VersionInfo(0, 0, 3),
                VersionInfo(0, 0, 4),
            ],
        ),
        (
            False,
            [
                VersionInfo(0, 0, 1),
                VersionInfo(0, 0, 2),
                VersionInfo(0, 0, 3),
                VersionInfo(0, 0, 4),
            ],
        ),
        (
            True,
            [
                VersionInfo(0, 0, 1),
                VersionInfo(0, 0, 2),
                VersionInfo(0, 0, 3),
                VersionInfo(0, 0, 4),
            ],
        ),
    ],
)
def test_app(pull_branch: bool, expected: VersionInfo) -> None:
    """Test app."""

    svg = SemverGit(pull_branch=pull_branch)
    assert svg is not None
    assert svg.branch.name == "test_branch"
    assert svg.versions == expected
    assert svg.latest_version == VersionInfo(0, 0, 4)


@mark.parametrize(
    "dry_run",
    [
        True,
        False,
    ],
)
@mark.parametrize(
    "bump_type, expected_version",
    [
        (str(BumpType.MAJOR), VersionInfo(1, 0, 0)),
        (str(BumpType.MINOR), VersionInfo(0, 1, 0)),
        (str(BumpType.PATCH), VersionInfo(0, 0, 5)),
        (str(BumpType.PRERELEASE), VersionInfo(0, 0, 5, "dev.1")),
    ],
)
@mark.parametrize(
    "commit_message, auto_message",
    [
        ("testmessage", False),
        (None, True),
        (None, False),
    ],
)
@mark.parametrize(
    "version_file",
    [
        "test_version_file",
        None,
    ],
)
def test_app_update(  # pylint: disable=too-many-arguments
    caplog: LogCaptureFixture,
    mock_update_verion_file: Callable,  # pylint: disable=unused-argument
    bump_type: str,
    expected_version: VersionInfo,
    dry_run: bool,
    commit_message: Optional[str],
    auto_message: bool,
    version_file: str,
    capsys: CaptureFixture,
) -> None:
    """Test app."""
    svg = SemverGit()
    new_version = svg.update(
        bump_type, dry_run=dry_run, commit_message=commit_message, auto_message=auto_message, version_file=version_file
    )

    expected_tag_str = f"{svg.version_prefix}{str(expected_version)}"
    assert f"Created mock-set-tag-{expected_tag_str}" in caplog.messages
    if commit_message or auto_message:
        assert "✍️ Committing..." in caplog.messages
    if version_file:
        assert f"📝 Writing version to {version_file}..." in caplog.messages
        if not commit_message:
            assert "✍️ Committing..." in caplog.messages
    assert "📤 Pushing..." in caplog.messages
    assert capsys.readouterr().out == expected_tag_str
    assert new_version == expected_tag_str
    print(f"{caplog.messages=}")
    assert f"⭐ New version tag: {expected_tag_str}" in caplog.messages
