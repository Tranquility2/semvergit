"""Test CLI."""
from string import Template

from click.testing import CliRunner
from pytest import LogCaptureFixture, MonkeyPatch, mark

from semvergit.cli import cli

BUMP_STRING = Template("<used $bump_type>")


class MockSemverGit:  # pylint: disable=too-few-public-methods
    """Mock SemverGit."""

    def update(self, bump_type: str) -> str:  # pylint: disable=unused-argument
        """Update."""
        return BUMP_STRING.substitute(bump_type=bump_type)


@mark.parametrize("bump_type", ["major", "minor", "patch", "prerelease"])
def test_cli(caplog: LogCaptureFixture, bump_type: str) -> None:
    """Test CLI."""
    runner = CliRunner()
    MonkeyPatch().setattr("semvergit.cli.SemverGit", MockSemverGit)
    result = runner.invoke(cli, ["--bump_type", bump_type])
    assert result.exit_code == 0
    assert caplog.messages == [f"New version: {BUMP_STRING.substitute(bump_type=bump_type)}"]


def test_cli_debug(caplog: LogCaptureFixture) -> None:
    """Test CLI debug."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--debug", "--bump_type", "patch"])
    assert result.exit_code == 0
    assert caplog.messages == [f"New version: {BUMP_STRING.substitute(bump_type='patch')}"]
