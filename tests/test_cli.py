"""Test CLI."""
from click.testing import CliRunner
from pytest import LogCaptureFixture, MonkeyPatch

from semvergit.cli import cli

UPDATE_VERSION = "1.1.2"


class MockSemverGit:  # pylint: disable=too-few-public-methods
    """Mock SemverGit."""

    def update(self, bump_type: str) -> str:  # pylint: disable=unused-argument
        """Update."""
        return UPDATE_VERSION


def test_cli(caplog: LogCaptureFixture) -> None:
    """Test CLI."""
    runner = CliRunner()
    MonkeyPatch().setattr("semvergit.cli.SemverGit", MockSemverGit)
    result = runner.invoke(cli, ["--bump_type", "patch"])
    assert result.exit_code == 0
    assert caplog.messages == [f"New version: {UPDATE_VERSION}"]
