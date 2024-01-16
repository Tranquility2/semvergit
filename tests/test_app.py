"""Test app."""
import semver
from pytest import CaptureFixture, LogCaptureFixture, mark

from semvergit.app import BumpType, SemverGit


def test_app() -> None:
    """Test app."""

    svg = SemverGit()
    assert svg is not None
    assert svg.branch.name == "test_branch"
    assert svg.versions == [
        semver.VersionInfo(0, 0, 1),
        semver.VersionInfo(0, 0, 2),
        semver.VersionInfo(0, 0, 3),
        semver.VersionInfo(0, 0, 4),
    ]
    assert svg.latest_version == semver.VersionInfo(0, 0, 4)


@mark.parametrize(
    "quiet, dry_run",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
@mark.parametrize(
    "bump_type, expected_version",
    [
        (str(BumpType.MAJOR), semver.VersionInfo(1, 0, 0)),
        (str(BumpType.MINOR), semver.VersionInfo(0, 1, 0)),
        (str(BumpType.PATCH), semver.VersionInfo(0, 0, 5)),
        (str(BumpType.PRERELEASE), semver.VersionInfo(0, 0, 5, "dev.1")),
    ],
)
def test_app_update(  # pylint: disable=too-many-arguments
    caplog: LogCaptureFixture,
    bump_type: str,
    expected_version: semver.VersionInfo,
    quiet: bool,
    dry_run: bool,
    capsys: CaptureFixture,
) -> None:
    """Test app."""
    svg = SemverGit()
    new_version = svg.update(bump_type, quiet=quiet, dry_run=dry_run)
    if not dry_run:
        result_str = f"mock-set-tag-{str(expected_version)}"
    else:
        result_str = str(expected_version)
    if quiet:
        assert capsys.readouterr().out == result_str
    assert new_version == result_str
    assert f"New version: {new_version}" in caplog.messages
