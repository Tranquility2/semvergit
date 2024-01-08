"""Test app."""
import semver

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


def test_app_update() -> None:
    """Test app."""

    svg = SemverGit()
    test_version = semver.VersionInfo(1, 1, 1)
    svg.latest_version = test_version
    assert svg.update(bump_type=str(BumpType.PATCH)) == str(semver.VersionInfo(1, 1, 2))
